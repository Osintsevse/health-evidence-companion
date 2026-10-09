"""Wholly fictional fixtures; no patient data or network access."""
import csv
import hashlib
import io
import json
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "skills/health-record-import/scripts"))
import genetic_evidence as ge


class EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def candidates(self, name="calls.sqlite", classification="Pathogenic", copies=1, raw="1"*64,
                   staging="2"*64, gene="SYNTH1"):
        path = self.root/name
        manifest = {"schema":"dtc-clinvar-candidates-v1", "staging_sha256":staging,
                    "staging_metadata":{"source_sha256":raw},
                    "operator_declarations":{"assembly":"GRCh37","strand":"forward"},
                    "reference_manifest":{"assembly":"GRCh37","sha256":"3"*64},
                    "counts":{"candidate_records":copies}}
        row = {"source_line":7, "observation":{"rsid_raw":"rsSynthetic","genotype_raw":"AG"},
               "match":{"assembly":"GRCh37","chromosome":"1","position":100,"reference":"A","alternate":"G"},
               "clinvar":{"variation_id":"101","classification":classification,
                          "review_status":"reviewed_by_expert_panel",
                          "info":{"GENEINFO":gene+":999999","CLNDN":"Synthetic_condition"}},
               "flags":[], "priority_for_manual_review":classification=="Pathogenic"}
        with sqlite3.connect(path) as db:
            db.execute("CREATE TABLE metadata(key TEXT PRIMARY KEY,value_json TEXT)")
            db.execute("INSERT INTO metadata VALUES('manifest',?)",(json.dumps(manifest),))
            db.execute("CREATE TABLE candidates(id INTEGER PRIMARY KEY,source_line INTEGER,row_json TEXT)")
            for _ in range(copies):
                db.execute("INSERT INTO candidates(source_line,row_json) VALUES(?,?)",(7,json.dumps(row)))
        db.close()
        return path

    def genes(self):
        buffer = io.StringIO()
        writer = csv.writer(buffer)
        writer.writerow(["FILE CREATED: 2026-01-01"])
        writer.writerow(ge.GENE_FIELDS)
        writer.writerow(["+"]*len(ge.GENE_FIELDS))
        for disease, moi in (("Synthetic condition one","AD"),("Synthetic condition two","AR")):
            writer.writerow(["SYNTH1","HGNC:999999",disease,"MONDO:999999",moi,"SOP10","Definitive",
                             "https://search.clinicalgenome.org/kb/gene-validity","2026-01-01","Synthetic panel"])
        data=buffer.getvalue().encode()
        path=self.root/"genes.csv"
        path.write_bytes(data)
        manifest={"schema":"clingen-gene-validity-cache-v1","url":ge.GENE_URL,
                  "sha256":hashlib.sha256(data).hexdigest(),"curations":2,"file_created":"2026-01-01"}
        Path(str(path)+".manifest.json").write_text(json.dumps(manifest))
        return path

    def test_offline_enrichment_preserves_every_condition_and_priority(self):
        with patch("urllib.request.build_opener",side_effect=AssertionError("No network")):
            result=ge.enrich(self.candidates(),self.genes(),self.root/"review.json")
        row=result["rows"][0]
        self.assertEqual(len(row["genes"][0]["assertions"]),2)
        self.assertTrue(row["gene_level_only"])
        self.assertTrue(row["condition_match_not_established"])
        self.assertTrue(row["priority_for_manual_review_unchanged"])

    def test_absent_gene_curation_is_unknown_and_aliases_not_guessed(self):
        result=ge.enrich(self.candidates(gene="UNLISTED_SYNTH"),self.genes(),self.root/"review.json")
        self.assertEqual(result["rows"][0]["genes"][0]["status"],"not_curated_in_this_snapshot")
        self.assertEqual(result["counts"]["candidates_with_gene_curations"],0)

    def test_tampered_public_cache_refused(self):
        genes=self.genes()
        genes.write_bytes(genes.read_bytes()+b"\n")
        with self.assertRaisesRegex(ValueError,"checksum"):
            ge.enrich(self.candidates(),genes,self.root/"review.json")
        self.assertFalse((self.root/"review.json").exists())

    def test_unknown_csv_schema_refused(self):
        with self.assertRaisesRegex(ValueError,"header"):
            ge.parse_gene_csv(b"GENE,DISEASE\nSYNTH1,Synthetic\n")

    def test_changed_classification_and_duplicate_multiplicity_preserved(self):
        before=self.candidates("before.sqlite",copies=2)
        after=self.candidates("after.sqlite",classification="Benign")
        result=ge.compare(before,after,self.root/"diff.json")
        self.assertEqual(result["counts"]["changed_variant_observations"],1)
        self.assertEqual(len(result["changes"][0]["before"]),2)
        self.assertEqual(result["changes"][0]["after"][0]["classification"],"Benign")

    def test_same_snapshot_is_not_claimed_as_new_database(self):
        result=ge.compare(self.candidates("before.sqlite"),self.candidates("after.sqlite"),self.root/"diff.json")
        self.assertEqual(result["counts"]["changed_variant_observations"],0)
        self.assertEqual(result["counts"]["unchanged_variant_observations"],1)
        self.assertEqual(result["before"]["reference"],result["after"]["reference"])

    def test_comparing_different_raw_or_staged_inputs_refused(self):
        before=self.candidates()
        for key in ("raw","staging"):
            after=self.candidates(key+".sqlite",**{key:"4"*64})
            with self.assertRaises(ValueError):
                ge.compare(before,after,self.root/(key+".json"))

    def test_transfer_plan_is_minimal_and_never_grants_or_sends(self):
        calls=self.candidates(copies=2)
        with patch("urllib.request.build_opener",side_effect=AssertionError("No network")):
            plan=ge.plan_transfer(calls,["101"],"franklin","Review synthetic annotation",
                                  self.root/"plan.json")
        self.assertFalse(plan["consent_granted"])
        self.assertFalse(plan["transmitted"])
        self.assertEqual(len(plan["payload"]["variants"]),1)
        text=json.dumps(plan["payload"])
        self.assertNotIn("genotype",text)
        self.assertNotIn("rsSynthetic",text)
        self.assertNotIn("observation",text)
        self.assertEqual(len(plan["scope_sha256"]),64)

    def test_recipient_and_purpose_are_bound_to_plan_scope(self):
        calls=self.candidates()
        plans=[ge.plan_transfer(calls,["101"],provider,purpose,self.root/(str(i)+".json"))
               for i,(provider,purpose) in enumerate((("franklin","Purpose one"),
                                                      ("varsome","Purpose one"),
                                                      ("franklin","Purpose two")))]
        self.assertEqual(len({p["scope_sha256"] for p in plans}),3)

    def test_unselected_identifiers_and_unknown_provider_refused(self):
        calls=self.candidates()
        for ids,provider in ((["102"],"franklin"),(["101"],"unknown"),([],"franklin")):
            with self.assertRaises(ValueError):
                ge.plan_transfer(calls,ids,provider,"Synthetic purpose",self.root/"plan.json")

    def test_existing_outputs_and_partial_files_are_preserved(self):
        target=self.root/"review.json"
        target.write_text("original")
        with self.assertRaises(FileExistsError):
            ge.enrich(self.candidates(),self.genes(),target)
        self.assertEqual(target.read_text(),"original")
        part=self.root/"new.json.part"
        part.write_text("existing temporary")
        with self.assertRaises(FileExistsError):
            ge.save(self.root/"new.json",{})
        self.assertEqual(part.read_text(),"existing temporary")

    def test_private_output_in_public_checkout_refused(self):
        with self.assertRaisesRegex(ValueError,"outside"):
            ge.save(ge.ga.PUBLIC_ROOT/"fictional-private-review.json",{})

    def test_fresh_process_cli_enrichment(self):
        calls=self.candidates()
        genes=self.genes()
        output=self.root/"cli.json"
        run=subprocess.run([sys.executable,str(Path(ge.__file__)),"enrich","--candidates",str(calls),
                            "--genes",str(genes),"--output",str(output)],
                           capture_output=True,text=True,check=True)
        self.assertEqual(json.loads(run.stdout)["candidates"],1)
        self.assertEqual(json.loads(output.read_text())["counts"]["candidates"],1)


if __name__ == "__main__":
    unittest.main()
