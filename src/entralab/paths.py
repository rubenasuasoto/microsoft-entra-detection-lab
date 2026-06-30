from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RULES_DIR = ROOT / "rules"
MANIFEST_PATH = RULES_DIR / "manifest.json"
FIXTURES_PATH = ROOT / "tests" / "fixtures" / "scenarios.json"
DOCS_DIR = ROOT / "docs"
PLAYBOOKS_DIR = DOCS_DIR / "playbooks"
ARTIFACTS_DIR = ROOT / "artifacts"
REPORTS_DIR = ROOT / "reports" / "latest"


def ensure_output_directories() -> None:
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
