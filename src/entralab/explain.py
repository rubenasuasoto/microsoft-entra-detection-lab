from __future__ import annotations

from .paths import PLAYBOOKS_DIR
from .rules import detection_by_id, load_manifest


def playbook_path(rule_id: str) -> str:
    return detection_by_id(rule_id)["playbook"]


def format_rule_list() -> str:
    lines = ["Detections:"]
    for item in load_manifest()["detections"]:
        lines.append(f"- {item['key']}: {item['title']} ({item['risk']}/{item['triage_priority']})")
    return "\n".join(lines)


def format_detection(rule_id: str) -> str:
    item = detection_by_id(rule_id)
    return "\n".join(
        [
            f"{item['key']} - {item['title']}",
            f"Log source: {item['log_source']}",
            f"Threshold: {item['threshold']}",
            f"Risk: {item['risk']} / {item['triage_priority']}",
            f"Severity reason: {item['severity_reason']}",
            f"Tuning: {item['tuning']}",
            f"Playbook: {item['playbook']}",
        ]
    )


def format_playbook(rule_id: str) -> str:
    path = PLAYBOOKS_DIR / playbook_path(rule_id)
    if not path.is_file():
        raise FileNotFoundError(f"Missing playbook: {path}")
    return path.read_text(encoding="utf-8")


def narrative_parts(rule_id: str) -> dict[str, str]:
    item = detection_by_id(rule_id)
    return {
        "what_happened": item["narrative"]["what_happened"],
        "why_it_matters": item["narrative"]["why_it_matters"],
        "what_to_check_next": item["narrative"]["what_to_check_next"],
        "decision_example": item["narrative"]["decision_example"],
    }
