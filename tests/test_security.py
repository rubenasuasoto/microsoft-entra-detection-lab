import re
import unittest

from entralab.audit import audit_repository
from entralab.paths import DOCS_DIR, FIXTURES_PATH, ROOT


class SecurityTests(unittest.TestCase):
    def test_repository_audit_passes(self) -> None:
        self.assertEqual(audit_repository(), [])

    def test_docs_and_fixtures_do_not_contain_realistic_sensitive_markers(self) -> None:
        patterns = {
            "bearer token": re.compile(r"\bBearer\s+[A-Za-z0-9._-]+", re.IGNORECASE),
            "tenant uuid": re.compile(
                r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b",
                re.IGNORECASE,
            ),
            "private ipv4": re.compile(
                r"\b(?:10\.\d{1,3}\.\d{1,3}\.\d{1,3}|192\.168\.\d{1,3}\.\d{1,3}|172\.(?:1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3})\b"
            ),
            "private domain": re.compile(r"\b(?:corp|internal|local)\.", re.IGNORECASE),
        }
        paths = [ROOT / "README.md", FIXTURES_PATH]
        paths.extend(DOCS_DIR.rglob("*.md"))
        for path in paths:
            text = path.read_text(encoding="utf-8")
            for label, pattern in patterns.items():
                with self.subTest(path=path, label=label):
                    self.assertIsNone(pattern.search(text))


if __name__ == "__main__":
    unittest.main()
