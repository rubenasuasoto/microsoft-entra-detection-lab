from __future__ import annotations

import json
from typing import Any

from .oracle import EVALUATORS, evaluate_cases, load_cases
from .paths import ARTIFACTS_DIR, RULES_DIR, ensure_output_directories
from .rules import load_manifest


def _validate_manifest(manifest: dict[str, Any]) -> list[str]:
    findings: list[str] = []
    detections = manifest.get("detections", [])
    if len(detections) != 6:
        findings.append("manifest must contain exactly 6 detections")
    keys = [item.get("key") for item in detections]
    if len(keys) != len(set(keys)):
        findings.append("manifest contains duplicate detection ids")
    required = {
        "key",
        "file",
        "title",
        "log_source",
        "required_fields",
        "threshold",
        "risk",
        "severity_reason",
        "triage_priority",
        "tuning",
        "playbook",
    }
    for item in detections:
        missing = sorted(required - set(item))
        if missing:
            findings.append(f"{item.get('key', 'unknown')} missing fields: {', '.join(missing)}")
        if item.get("key") not in EVALUATORS:
            findings.append(f"{item.get('key')} has no oracle evaluator")
        if not (RULES_DIR / str(item.get("file", ""))).is_file():
            findings.append(f"{item.get('key')} missing rule file")
    return findings


def run_validation() -> dict[str, Any]:
    ensure_output_directories()
    manifest = load_manifest()
    manifest_findings = _validate_manifest(manifest)
    cases = evaluate_cases()
    raw_cases = load_cases()
    rule_ids = {item["key"] for item in manifest["detections"]}
    categories_by_rule = {
        rule_id: {case["category"] for case in raw_cases if case["rule_id"] == rule_id}
        for rule_id in rule_ids
    }
    for rule_id, categories in sorted(categories_by_rule.items()):
        for required in ("positive", "negative", "boundary"):
            if required not in categories:
                manifest_findings.append(f"{rule_id} missing {required} case")
    summary = {
        "rules_total": len(manifest["detections"]),
        "rules_valid": len(manifest["detections"]) if not manifest_findings else 0,
        "cases_total": len(cases),
        "cases_passed": sum(1 for case in cases if case["status"] == "pass"),
        "cases_tuning": sum(1 for case in cases if case["disposition"] == "tune"),
    }
    payload = {
        "ok": not manifest_findings and summary["cases_total"] == summary["cases_passed"],
        "summary": summary,
        "findings": manifest_findings,
        "cases": cases,
    }
    (ARTIFACTS_DIR / "validation.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8", newline="\n"
    )
    return payload
