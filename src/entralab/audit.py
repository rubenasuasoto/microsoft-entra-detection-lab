from __future__ import annotations

import re

from .paths import DOCS_DIR, FIXTURES_PATH, ROOT

FORBIDDEN_PATTERNS = {
    "tenant id placeholder shaped like uuid": re.compile(
        r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b",
        re.IGNORECASE,
    ),
    "bearer token": re.compile(r"\bBearer\s+[A-Za-z0-9._-]+", re.IGNORECASE),
    "private ipv4 address": re.compile(
        r"\b(?:10\.\d{1,3}\.\d{1,3}\.\d{1,3}|192\.168\.\d{1,3}\.\d{1,3}|172\.(?:1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3})\b"
    ),
}


def audit_repository() -> list[str]:
    findings: list[str] = []
    paths = [ROOT / "README.md", DOCS_DIR / "DATA_SOURCES.md", FIXTURES_PATH]
    paths.extend(DOCS_DIR.glob("*.md"))
    paths.extend((DOCS_DIR / "playbooks").glob("*.md"))
    for path in sorted(set(paths)):
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for label, pattern in FORBIDDEN_PATTERNS.items():
            if pattern.search(text):
                findings.append(f"{path.relative_to(ROOT)} contains {label}")
    return findings
