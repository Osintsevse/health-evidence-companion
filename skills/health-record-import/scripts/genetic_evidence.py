"""Offline genetics evidence enrichment, snapshot comparison and transfer planning.

Public download has a fixed endpoint and accepts no patient input. Other commands
never use a network. None of these operations diagnose or authorize disclosure.
"""
import argparse
from collections import Counter, defaultdict
import csv
import io
import json
import os
from pathlib import Path
import sqlite3
import urllib.request

import genetic_annotation as ga

VERSION = "1.0"
GENE_URL = "https://search.clinicalgenome.org/kb/gene-validity/download"
GENE_FIELDS = ("GENE SYMBOL", "GENE ID (HGNC)", "DISEASE LABEL",
               "DISEASE ID (MONDO)", "MOI", "SOP", "CLASSIFICATION",
               "ONLINE REPORT", "CLASSIFICATION DATE", "GCEP")
PROVIDERS = {
    "varsome": {"policy_review_status": "current terms require review",
                "documentation_url": "https://landing.varsome.com/varsome-api"},
    "franklin": {"policy_url": "https://go.genoox.com/pp_franklinbyqiagen",
                 "documentation_url": "https://help.genoox.com/en/"},
}


def publish(path, data):
    """Publish a new external file; never replace an existing review."""
    path = ga.external_output(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = Path(str(path) + ".part")
    owns = False
    try:
        with temporary.open("xb") as stream:
            owns = True
            stream.write(data)
        if os.name == "nt":
            temporary.rename(path)
        else:
            os.link(temporary, path)
            temporary.unlink()
        return path
    finally:
        if owns:
            temporary.unlink(missing_ok=True)


def save(path, data):
    return publish(path, (json.dumps(data, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))


def parse_gene_csv(data):
    lines = list(csv.reader(io.StringIO(data.decode("utf-8-sig"))))
    header = next((i for i, row in enumerate(lines) if tuple(row) == GENE_FIELDS), None)
    if header is None:
        raise ValueError("Unrecognized ClinGen gene-validity CSV header")
    rows = []
    for line, fields in enumerate(lines[header + 1:], header + 2):
        if not fields or all(not x or set(x) <= {"+"} for x in fields):
            continue
        if len(fields) != len(GENE_FIELDS):
            raise ValueError("Invalid ClinGen column count at line %d" % line)
        row = dict(zip(GENE_FIELDS, fields))
        if not row["GENE SYMBOL"] or not row["GENE ID (HGNC)"].startswith("HGNC:"):
            raise ValueError("Invalid ClinGen gene identity at line %d" % line)
        if not row["DISEASE ID (MONDO)"].startswith("MONDO:"):
            raise ValueError("Invalid ClinGen disease identity at line %d" % line)
        row["source_line"] = line
        rows.append(row)
    if not rows:
        raise ValueError("Empty ClinGen curation snapshot")
    created = next((row[0].removeprefix("FILE CREATED: ") for row in lines
                    if row and row[0].startswith("FILE CREATED: ")), None)
    return rows, created


def download_genes(output):
    """Download the full public summary, without private query parameters."""
    output = ga.external_output(output)
    sidecar = Path(str(output) + ".manifest.json")
    if output.exists() or sidecar.exists():
        raise FileExistsError(output)
    class NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):
            raise ValueError("Public evidence download redirects are refused")
    opener = urllib.request.build_opener(NoRedirect())
    with opener.open(GENE_URL, timeout=60) as response:
        if response.geturl() != GENE_URL:
            raise ValueError("Unexpected public endpoint")
        data = response.read(16 * 1024 * 1024 + 1)
    if len(data) > 16 * 1024 * 1024:
        raise ValueError("Public gene snapshot exceeds 16 MiB")
    rows, created = parse_gene_csv(data)
    import hashlib
    manifest = {"schema": "clingen-gene-validity-cache-v1", "url": GENE_URL,
                "retrieved_utc": ga.now(), "file_created": created,
                "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data),
                "curations": len(rows), "tool_version": VERSION,
                "integrity": "local SHA-256; HTTPS transport; no publisher signature"}
    publish(output, data)
    save(sidecar, manifest)
    return manifest


def load_genes(path):
    path = Path(path)
    sidecar = json.loads(Path(str(path) + ".manifest.json").read_text(encoding="utf-8"))
    if sidecar.get("schema") != "clingen-gene-validity-cache-v1" or sidecar.get("url") != GENE_URL:
        raise ValueError("Unrecognized ClinGen cache provenance")
    if sidecar.get("sha256") != ga.digest(path):
        raise ValueError("ClinGen cache checksum mismatch")
    rows, created = parse_gene_csv(path.read_bytes())
    if sidecar.get("curations") != len(rows) or sidecar.get("file_created") != created:
        raise ValueError("ClinGen cache metadata mismatch")
    by_gene = defaultdict(list)
    for row in rows:
        by_gene[row["GENE SYMBOL"]].append(row)
    return by_gene, sidecar


def load_candidates(path):
    db = sqlite3.connect(Path(path).resolve().as_uri() + "?mode=ro", uri=True)
    try:
        manifest = json.loads(db.execute("SELECT value_json FROM metadata WHERE key='manifest'").fetchone()[0])
        if manifest.get("schema") != "dtc-clinvar-candidates-v1":
            raise ValueError("Unsupported candidate dataset")
        records = [json.loads(raw) for (raw,) in db.execute("SELECT row_json FROM candidates ORDER BY id")]
        if manifest.get("counts", {}).get("candidate_records") != len(records):
            raise ValueError("Candidate count/provenance mismatch")
        return records, manifest
    finally:
        db.close()


def enrich(candidates, genes, output):
    records, manifest = load_candidates(candidates)
    by_gene, source = load_genes(genes)
    rows = []
    matched = 0
    for record in records:
        symbols = list(dict.fromkeys(part.split(":", 1)[0] for part in
                       str(record["clinvar"]["info"].get("GENEINFO", "")).split("|") if part))
        evidence = []
        for symbol in symbols:
            assertions = by_gene.get(symbol, [])
            evidence.append({"symbol": symbol, "status": "curations_found" if assertions else
                             "not_curated_in_this_snapshot", "assertions": assertions})
        matched += int(any(e["assertions"] for e in evidence))
        rows.append({"source_line": record["source_line"],
                     "variation_id": record["clinvar"]["variation_id"], "genes": evidence,
                     "gene_level_only": True, "condition_match_not_established": True,
                     "priority_for_manual_review_unchanged": record["priority_for_manual_review"]})
    result = {"schema": "private-genetic-gene-evidence-v1", "created_utc": ga.now(),
              "tool_version": VERSION, "candidate_sha256": ga.digest(candidates),
              "source_raw_sha256": manifest["staging_metadata"].get("source_sha256"),
              "reference": source, "counts": {"candidates": len(records),
                "candidates_with_gene_curations": matched, "without_gene_curations": len(records)-matched},
              "limitations": ["Exact gene symbols only; no alias inference",
                "A gene-disease assertion does not classify a variant or establish a patient diagnosis",
                "All diseases and inheritance modes retained; no phenotype/condition matching",
                "Absence of a curation is unknown, not benign or absence of disease",
                "ClinGen and ClinVar evidence can overlap; this is not independent voting"],
              "rows": rows}
    save(output, result)
    return result


def identity(record):
    m = record["match"]
    return (record["source_line"], m["assembly"], m["chromosome"], m["position"],
            m["reference"], m["alternate"])


def state(record):
    return {"variation_id": record["clinvar"]["variation_id"],
            "classification": record["clinvar"]["classification"],
            "review_status": record["clinvar"]["review_status"],
            "info": record["clinvar"]["info"], "flags": record["flags"],
            "priority_for_manual_review": record["priority_for_manual_review"]}


def compare(before, after, output):
    old, old_manifest = load_candidates(before)
    new, new_manifest = load_candidates(after)
    raw_old = old_manifest.get("staging_metadata", {}).get("source_sha256")
    raw_new = new_manifest.get("staging_metadata", {}).get("source_sha256")
    if not raw_old or raw_old != raw_new:
        raise ValueError("Cannot compare different or unidentified raw inputs")
    if not old_manifest.get("staging_sha256") or old_manifest.get("staging_sha256") != new_manifest.get("staging_sha256"):
        raise ValueError("Cannot compare different staged input bytes")
    if old_manifest.get("operator_declarations") != new_manifest.get("operator_declarations"):
        raise ValueError("Cannot compare different assembly/strand declarations")
    groups = []
    for records in (old, new):
        group = defaultdict(list)
        for record in records:
            group[identity(record)].append(state(record))
        groups.append(group)
    old_group, new_group = groups
    changes = []
    unchanged = 0
    for key in sorted(set(old_group) | set(new_group)):
        left, right = old_group.get(key, []), new_group.get(key, [])
        serialized = lambda states: Counter(json.dumps(s, sort_keys=True) for s in states)
        if serialized(left) == serialized(right):
            unchanged += 1
            continue
        status = "annotation_changed" if left and right else (
            "new_reference_match" if right else "no_match_in_new_snapshot_not_a_negative_test")
        changes.append({"identity": list(key), "change": status, "before": left, "after": right})
    result = {"schema": "private-genetic-comparison-v1", "created_utc": ga.now(),
              "tool_version": VERSION, "source_raw_sha256": raw_old,
              "before": {"sha256": ga.digest(before), "reference": old_manifest["reference_manifest"]},
              "after": {"sha256": ga.digest(after), "reference": new_manifest["reference_manifest"]},
              "counts": {"unchanged_variant_observations": unchanged, "changed_variant_observations": len(changes),
                         "before_records": len(old), "after_records": len(new)},
              "changes": changes,
              "limitations": ["Annotation differences are not newly confirmed biological variants",
                "Removed matches do not establish a negative clinical result",
                "A new analysis date does not imply a newer reference snapshot",
                "No network calls, medical decisions or patient notifications are performed"]}
    save(output, result)
    return result


def plan_transfer(candidates, selected_ids, provider, purpose, output, retention="unknown"):
    """Prepare a reviewable minimum payload; never submit or approve it."""
    if provider not in PROVIDERS:
        raise ValueError("Unsupported provider; review new integrations separately")
    selected = set(selected_ids)
    if not selected or len(selected) > 100 or any(not str(i).isdigit() for i in selected):
        raise ValueError("Select 1-100 exact ClinVar variation identifiers")
    if not purpose.strip():
        raise ValueError("A specific purpose is required")
    records, manifest = load_candidates(candidates)
    variants, found = {}, set()
    for record in records:
        identifier = record["clinvar"]["variation_id"]
        if identifier in selected:
            found.add(identifier)
            match = record["match"]
            variant = {k: match[k] for k in
                       ("assembly", "chromosome", "position", "reference", "alternate")}
            variants[json.dumps(variant, sort_keys=True)] = variant
    if found != selected:
        raise ValueError("Selected identifiers absent from candidate dataset")
    payload = {"variants": [variants[key] for key in sorted(variants)]}
    import hashlib
    result = {"schema": "private-genetic-transfer-plan-v1", "created_utc": ga.now(),
              "status": "awaiting_privacy_review_and_explicit_owner_consent",
              "provider": provider, "purpose": purpose,
              "provider_information": PROVIDERS[provider], "retention_terms": retention,
              "payload": payload,
              "payload_sha256": hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest(),
              "excluded": ["raw genotype file", "genotype tokens", "phenotype", "identity",
                           "family history", "private archive paths"],
              "consent_granted": False, "transmitted": False,
              "requirements": ["Review current contract, retention, training and sharing terms",
                "Show exact payload and recipient to the owner before consent",
                "Installation, generic processing permission and this plan are not consent",
                "Changed payload, recipient or purpose requires renewed consent",
                "An authorized host adapter must verify a scoped consent receipt before any transmission"]}
    scope = {key: result[key] for key in ("provider", "purpose", "payload", "provider_information", "retention_terms")}
    result["scope_sha256"] = hashlib.sha256(json.dumps(scope, sort_keys=True).encode()).hexdigest()
    save(output, result)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    download = commands.add_parser("download-genes")
    download.add_argument("--output", required=True)
    enrich_parser = commands.add_parser("enrich")
    enrich_parser.add_argument("--candidates", required=True)
    enrich_parser.add_argument("--genes", required=True)
    enrich_parser.add_argument("--output", required=True)
    diff = commands.add_parser("compare")
    for name in ("before", "after", "output"):
        diff.add_argument("--" + name, required=True)
    transfer = commands.add_parser("plan-transfer")
    transfer.add_argument("--candidates", required=True)
    transfer.add_argument("--variation-id", action="append", required=True)
    transfer.add_argument("--provider", choices=sorted(PROVIDERS), required=True)
    transfer.add_argument("--purpose", required=True)
    transfer.add_argument("--retention", default="unknown")
    transfer.add_argument("--output", required=True)
    args = vars(parser.parse_args())
    command = args.pop("command")
    if command == "plan-transfer":
        args["selected_ids"] = args.pop("variation_id")
    result = {"download-genes": download_genes, "enrich": enrich,
              "compare": compare, "plan-transfer": plan_transfer}[command](**args)
    print(json.dumps(result.get("counts", {"schema": result["schema"]}), ensure_ascii=False))


if __name__ == "__main__":
    main()
