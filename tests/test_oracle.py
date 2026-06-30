import unittest

from entralab.oracle import evaluate_cases, load_cases
from entralab.validation import run_validation


class OracleTests(unittest.TestCase):
    def test_oracle_matches_every_expected_result(self) -> None:
        results = evaluate_cases()
        self.assertGreater(len(results), 0)
        for result in results:
            with self.subTest(case_id=result["case_id"]):
                self.assertEqual(result["status"], "pass")

    def test_each_detection_has_required_case_categories(self) -> None:
        cases = load_cases()
        rule_ids = {case["rule_id"] for case in cases}
        for rule_id in rule_ids:
            categories = {case["category"] for case in cases if case["rule_id"] == rule_id}
            with self.subTest(rule_id=rule_id):
                self.assertIn("positive", categories)
                self.assertIn("negative", categories)
                self.assertIn("boundary", categories)

    def test_tune_cases_remain_alerts_when_intended(self) -> None:
        results = {result["case_id"]: result for result in evaluate_cases()}
        tune_cases = [case for case in load_cases() if case.get("disposition") == "tune"]
        self.assertGreaterEqual(len(tune_cases), 1)
        for case in tune_cases:
            with self.subTest(case_id=case["case_id"]):
                self.assertTrue(case["expected_alert"])
                self.assertTrue(results[case["case_id"]]["observed"])

    def test_validation_payload_is_ok(self) -> None:
        payload = run_validation()
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["summary"]["rules_total"], 6)


if __name__ == "__main__":
    unittest.main()
