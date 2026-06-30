import json
import unittest

from entralab.paths import MANIFEST_PATH, PLAYBOOKS_DIR, RULES_DIR
from entralab.rules import load_manifest


class RuleTests(unittest.TestCase):
    def test_manifest_has_exactly_six_detections(self) -> None:
        manifest = load_manifest()
        self.assertEqual(len(manifest["detections"]), 6)
        self.assertEqual(
            [item["key"] for item in manifest["detections"]],
            ["ENTRA-001", "ENTRA-002", "ENTRA-003", "ENTRA-004", "ENTRA-005", "ENTRA-006"],
        )

    def test_each_detection_has_rule_and_playbook(self) -> None:
        for detection in load_manifest()["detections"]:
            with self.subTest(rule_id=detection["key"]):
                self.assertTrue((RULES_DIR / detection["file"]).is_file())
                self.assertTrue((PLAYBOOKS_DIR / detection["playbook"]).is_file())

    def test_manifest_json_is_valid(self) -> None:
        payload = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        self.assertEqual(payload["schema_version"], 1)


if __name__ == "__main__":
    unittest.main()
