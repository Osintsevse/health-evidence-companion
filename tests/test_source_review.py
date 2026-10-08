"""Synthetic tests of source-review planning invariants."""
import copy
import datetime as dt
import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location("source_review", Path(__file__).resolve().parents[1] / "scripts/source_review.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class ReviewQueueTests(unittest.TestCase):
    def sample(self):
        return {"id": "S01", "title": "Synthetic source", "url": "https://example.org/guideline", "region": "Synthetic", "retrieval_status": "selected section read", "use": "Synthetic fixture", "checked_on": "2026-01-01"}

    def test_inclusive_due_and_no_mutation(self):
        source = self.sample()
        before = copy.deepcopy(source)
        row = module.review_queue([source], dt.date(2026, 1, 31), 30)[0]
        self.assertTrue(row["due"])
        self.assertEqual(source, before)
        self.assertFalse(module.review_queue([source], dt.date(2026, 1, 30), 30)[0]["due"])

    def test_blocked_source_retains_access_limit(self):
        source = self.sample()
        source["retrieval_status"] = "Direct page failed 403; official excerpt only"
        row = module.review_queue([source], dt.date(2026, 1, 2))[0]
        self.assertTrue(row["limited_access_or_reading"])
        self.assertEqual(row["last_recorded_check"], "2026-01-01")
        self.assertEqual(row["reading_status"], source["retrieval_status"])

    def test_reject_invalid_planning_inputs(self):
        with self.assertRaises(ValueError):
            module.review_queue([self.sample()], dt.date(2026, 1, 2), 0)
        with self.assertRaises(ValueError):
            module.review_queue([self.sample()], dt.date(2025, 1, 2))
        with self.assertRaises(ValueError):
            module.review_queue([self.sample(), self.sample()], dt.date(2026, 1, 2))

    def test_every_source_retained_and_due_first(self):
        a = self.sample()
        b = dict(a, id="S02", checked_on="2026-02-01")
        rows = module.review_queue([b, a], dt.date(2026, 2, 15), 30)
        self.assertEqual([x["id"] for x in rows], ["S01", "S02"])

if __name__ == "__main__":
    unittest.main()
