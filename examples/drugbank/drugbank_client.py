"""Read-only DrugBank DDI adapter. No patient-text input or local logging."""
import argparse
from datetime import datetime, timezone
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

ENDPOINT = "https://api.drugbank.com/v1/ddi"
LIMIT = 4 * 1024 * 1024


class DrugBankError(Exception):
    pass


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def connection_status():
    return {
        "provider": "DrugBank",
        "key_configured": bool(os.environ.get("DRUGBANK_API_KEY")),
        "requests_enabled": os.environ.get("DRUGBANK_ENABLE_REQUESTS") == "1",
        "live_connection_verified": False,
        "note": "Configuration presence does not verify credentials, license or connectivity.",
    }


def check_interactions(ids, kind="ingredient"):
    if kind not in ("ingredient", "product_concept"):
        raise DrugBankError("Use ingredient or product_concept identifiers.")
    pattern = r"DB[0-9]{5}" if kind == "ingredient" else r"DBPC[0-9]{6,7}"
    if not isinstance(ids, list) or not all(isinstance(x, str) and re.fullmatch(pattern, x) for x in ids):
        raise DrugBankError("Only validated DrugBank identifiers are accepted; no patient text.")
    ids = list(dict.fromkeys(ids))
    if not 2 <= len(ids) <= 40:
        raise DrugBankError("Supply between 2 and 40 distinct identifiers.")
    key = os.environ.get("DRUGBANK_API_KEY", "")
    if not key:
        raise DrugBankError("DRUGBANK_API_KEY is not configured.")
    if not key.isascii() or any(ord(c) < 33 or ord(c) > 126 for c in key):
        raise DrugBankError("Invalid key format; configure the provider API key as a secret.")
    if os.environ.get("DRUGBANK_ENABLE_REQUESTS") != "1":
        raise DrugBankError("External requests are disabled. Enable only after reviewing access, costs and data handling.")
    params = {
        "drugbank_id" if kind == "ingredient" else "product_concept_id": ",".join(ids),
        "include_references": "true",
    }
    if kind == "product_concept":
        params["match_routes"] = "true"
    request = urllib.request.Request(
        ENDPOINT + "?" + urllib.parse.urlencode(params),
        headers={"Authorization": key, "Accept": "application/json"}, method="GET",
    )
    # Never forward credentials to a redirected origin. No automatic retries:
    # each licensed request may be billable.
    try:
        with urllib.request.build_opener(NoRedirect()).open(request, timeout=20) as response:
            raw = response.read(LIMIT + 1)
    except urllib.error.HTTPError as exc:
        reasons = {401: "Credentials rejected", 403: "License or access denied", 429: "Rate limit reached"}
        raise DrugBankError(reasons.get(exc.code, "Provider HTTP error") + f" (HTTP {exc.code}).") from None
    except (urllib.error.URLError, TimeoutError, OSError):
        raise DrugBankError("Provider connection failed; interaction status is unknown.") from None
    if len(raw) > LIMIT:
        raise DrugBankError("Provider response too large; result was not accepted.")
    try:
        data = json.loads(raw)
    except (ValueError, UnicodeError):
        raise DrugBankError("Invalid provider response; interaction status is unknown.") from None
    if not isinstance(data, dict) or not isinstance(data.get("interactions"), list):
        raise DrugBankError("Unexpected provider response schema.")
    rows = data["interactions"]
    total = data.get("total_results")
    if type(total) is not int or total < 0 or not all(isinstance(row, dict) for row in rows):
        raise DrugBankError("Unexpected provider result count or interaction schema.")
    # The DDI documentation does not specify a pagination contract. Fail closed
    # if the declared count differs rather than inventing page parameters.
    if total != len(rows):
        raise DrugBankError("Incomplete provider result; confirm the DDI response contract with DrugBank.")
    return {
        "provider": "DrugBank",
        "queried_at_utc": datetime.now(timezone.utc).isoformat(),
        "identifier_kind": kind,
        "requested_identifiers": ids,
        "scope": "drug-drug interactions in this provider dataset",
        "result": "interactions_found" if rows else "no_interactions_returned",
        "interpretation": "No returned interaction does not establish safety. This is not a patient-specific assessment or prescription.",
        "route_limitation": "Ingredient IDs do not identify formulation or administration route." if kind == "ingredient" else "Verify product identity and administration route before interpreting results.",
        "provider_data": data,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--status", action="store_true")
    parser.add_argument("--kind", choices=["ingredient", "product_concept"], default="ingredient")
    parser.add_argument("ids", nargs="*")
    args = parser.parse_args()
    try:
        result = connection_status() if args.status else check_interactions(args.ids, args.kind)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except DrugBankError as exc:
        print(json.dumps({"error": str(exc), "interaction_status": "unknown"}), file=sys.stderr)
        sys.exit(1)
