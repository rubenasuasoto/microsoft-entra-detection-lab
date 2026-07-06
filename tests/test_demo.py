import unittest

from entralab.demo import GITBOOK_BASE_URL, SCOPE_NOTICE, build_demo
from entralab.paths import REPORTS_DIR


class DemoTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.demo_path = build_demo()
        cls.html = cls.demo_path.read_text(encoding="utf-8")
        cls.lower_html = cls.html.lower()

    def test_demo_is_generated_under_reports_latest(self) -> None:
        self.assertEqual(self.demo_path, REPORTS_DIR / "demo.html")
        self.assertTrue(self.demo_path.is_file())

    def test_demo_contains_detection_ids_and_case_categories(self) -> None:
        for rule_id in (
            "ENTRA-001",
            "ENTRA-002",
            "ENTRA-003",
            "ENTRA-004",
            "ENTRA-005",
            "ENTRA-006",
        ):
            with self.subTest(rule_id=rule_id):
                self.assertIn(rule_id, self.html)
        for category in ("positive", "negative", "boundary", "false_positive", "tune"):
            with self.subTest(category=category):
                self.assertIn(category, self.html)

    def test_demo_keeps_defensive_scope_visible(self) -> None:
        self.assertIn(SCOPE_NOTICE, self.html)
        self.assertIn("No real tenants", self.html)
        self.assertIn(
            "No real tenants, credentials, tokens, production logs or live Graph calls",
            self.html,
        )

    def test_demo_does_not_load_external_resources(self) -> None:
        forbidden = (
            "<script src",
            "http://",
            "<form",
            'type="file"',
            "fetch(",
            "xmlhttprequest",
            "sendbeacon",
        )
        for marker in forbidden:
            with self.subTest(marker=marker):
                self.assertNotIn(marker, self.lower_html)
        external_urls = [
            value
            for value in self.html.split('"')
            if value.startswith(("https://", "http://"))
        ]
        for url in external_urls:
            with self.subTest(url=url):
                self.assertTrue(url.startswith(GITBOOK_BASE_URL))

    def test_demo_links_playbooks(self) -> None:
        self.assertIn("<a", self.html)
        for rule_id in (
            "ENTRA-001",
            "ENTRA-002",
            "ENTRA-003",
            "ENTRA-004",
            "ENTRA-005",
            "ENTRA-006",
        ):
            with self.subTest(rule_id=rule_id):
                self.assertIn(f"Open {rule_id} playbook", self.html)
                self.assertIn(f"{GITBOOK_BASE_URL}playbooks/{rule_id.lower()}", self.html)

    def test_demo_exposes_guided_soc_controls(self) -> None:
        for expected in (
            "ruleSelect",
            "caseSelect",
            "For reviewers: 3-minute guided path",
            "Previous case",
            "Next case",
            "Event timeline",
            "Analyst narrative",
            "Matched fields",
            "ENTRA-003-POS",
        ):
            with self.subTest(expected=expected):
                self.assertIn(expected, self.html)


if __name__ == "__main__":
    unittest.main()
