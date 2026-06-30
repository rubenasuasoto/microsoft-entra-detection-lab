from __future__ import annotations

import json
from typing import Any

from .paths import MANIFEST_PATH


def load_manifest() -> dict[str, Any]:
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def detection_by_id(rule_id: str) -> dict[str, Any]:
    for detection in load_manifest()["detections"]:
        if detection["key"] == rule_id:
            return detection
    raise KeyError(f"Unknown detection id: {rule_id}")
