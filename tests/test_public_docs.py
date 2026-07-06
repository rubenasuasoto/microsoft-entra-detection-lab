import unittest

from entralab.paths import ROOT


class PublicDocsTests(unittest.TestCase):
    def test_readme_contains_expected_public_demo_and_release_status(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn(
            "https://rubenasuasoto.github.io/microsoft-entra-detection-lab/reports/latest/demo.html",
            readme,
        )
        self.assertIn("v0.1.0 pending release", readme)
        self.assertIn("Public demo:", readme)
        self.assertIn("actions/workflows/validate.yml/badge.svg", readme)

    def test_release_checklist_blocks_tag_until_public_checks_pass(self) -> None:
        checklist = (ROOT / "docs" / "RELEASE_CHECKLIST.md").read_text(encoding="utf-8")
        self.assertIn("Publish demo site", checklist)
        self.assertIn("No `v0.1.0` tag exists before the public checks", checklist)
        self.assertIn("GitBook documentation returns `200`", checklist)
        self.assertIn(
            "Repository-relative playbooks served by GitHub Pages return `200`",
            checklist,
        )


if __name__ == "__main__":
    unittest.main()
