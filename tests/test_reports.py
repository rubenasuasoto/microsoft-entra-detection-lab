import unittest

from entralab.paths import REPORTS_DIR
from entralab.report import build_reports
from entralab.validation import run_validation


class ReportTests(unittest.TestCase):
    def test_reports_are_generated(self) -> None:
        run_validation()
        outputs = build_reports()
        self.assertEqual(
            outputs,
            [
                REPORTS_DIR / "report.md",
                REPORTS_DIR / "report.html",
                REPORTS_DIR / "validation-matrix.csv",
            ],
        )
        for output in outputs:
            with self.subTest(output=output):
                self.assertTrue(output.is_file())

    def test_report_contains_scope_and_detections(self) -> None:
        run_validation()
        build_reports()
        report = (REPORTS_DIR / "report.md").read_text(encoding="utf-8")
        self.assertIn("ENTRA-003", report)
        self.assertIn("synthetic", report)
        self.assertIn("does not connect to Microsoft Graph", report)


if __name__ == "__main__":
    unittest.main()
