import io
import json
import os
import unittest
from unittest.mock import patch
import urllib.error
from urllib.parse import parse_qs, urlsplit
from drugbank_client import DrugBankError, NoRedirect, check_interactions, connection_status


class Tests(unittest.TestCase):
    def setUp(self):
        self.env = patch.dict(os.environ, {"DRUGBANK_API_KEY": "offline-test-key", "DRUGBANK_ENABLE_REQUESTS": "1"}, clear=True)
        self.env.start()
        self.addCleanup(self.env.stop)

    def call(self, data, ids=None, kind="ingredient"):
        with patch("urllib.request.build_opener") as mocked:
            mocked.return_value.open.return_value = io.BytesIO(json.dumps(data).encode())
            result = check_interactions(ids or ["DB00001", "DB00002"], kind)
            request = mocked.return_value.open.call_args.args[0]
            return result, request

    def test_references_retained_and_no_filters(self):
        data = {"interactions": [{"severity": "major", "references": {"articles": [{"ref_id": "synthetic"}]}}], "total_results": 1}
        result, request = self.call(data)
        self.assertEqual(result["provider_data"], data)
        self.assertEqual(request.get_header("Authorization"), "offline-test-key")
        query = parse_qs(urlsplit(request.full_url).query)
        self.assertEqual(set(query), {"drugbank_id", "include_references"})
        self.assertNotIn("offline-test-key", json.dumps(result))

    def test_empty_is_not_safe(self):
        result, _ = self.call({"interactions": [], "total_results": 0})
        self.assertEqual(result["result"], "no_interactions_returned")
        self.assertIn("does not establish safety", result["interpretation"])

    def test_no_patient_text(self):
        with patch("urllib.request.build_opener") as mocked:
            for ids in (["synthetic patient text", "DB00001"], ["DB00001"], ["DB00001", "DB00001"], ["DB00001"] * 41):
                with self.assertRaises(DrugBankError):
                    check_interactions(ids)
            mocked.assert_not_called()

    def test_missing_key_and_disabled_requests(self):
        for env in ({}, {"DRUGBANK_API_KEY": "test"}):
            with patch.dict(os.environ, env, clear=True), patch("urllib.request.build_opener") as mocked:
                with self.assertRaises(DrugBankError):
                    check_interactions(["DB00001", "DB00002"])
                mocked.assert_not_called()
                self.assertFalse(connection_status()["live_connection_verified"])

    def test_incomplete_and_bad_schema(self):
        for data in ({"interactions": [], "total_results": 1}, {"interactions": [], "total_results": True}, {"error": "unknown"}):
            with self.assertRaises(DrugBankError):
                self.call(data)

    def test_http_error_does_not_leak_body_or_secret(self):
        with patch("urllib.request.build_opener") as mocked:
            mocked.return_value.open.side_effect = urllib.error.HTTPError("https://api.drugbank.com", 403, "offline-test-key", {}, io.BytesIO(b"private payload"))
            with self.assertRaises(DrugBankError) as ctx:
                check_interactions(["DB00001", "DB00002"])
            self.assertNotIn("offline-test-key", str(ctx.exception))
            self.assertNotIn("private payload", str(ctx.exception))
            self.assertIn("403", str(ctx.exception))

    def test_product_route_matching(self):
        _, request = self.call({"interactions": [], "total_results": 0}, ["DBPC0248838", "DBPC0061207"], "product_concept")
        self.assertEqual(parse_qs(urlsplit(request.full_url).query)["match_routes"], ["true"])

    def test_no_redirect(self):
        self.assertIsNone(NoRedirect().redirect_request(None, None, 302, "", {}, "https://other.invalid"))


if __name__ == "__main__":
    unittest.main()
