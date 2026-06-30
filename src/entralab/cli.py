from __future__ import annotations

import argparse
import json
import webbrowser

from .audit import audit_repository
from .demo import build_demo
from .explain import format_detection, format_playbook, format_rule_list
from .report import build_reports
from .validation import run_validation


def _audit() -> bool:
    findings = audit_repository()
    if findings:
        print("Repository audit failed:")
        for finding in findings:
            print(f"- {finding}")
        return False
    print("Repository audit: OK")
    return True


def _validate() -> bool:
    payload = run_validation()
    print(json.dumps(payload["summary"], ensure_ascii=False))
    return bool(payload["ok"])


def _report() -> bool:
    outputs = build_reports()
    for output in outputs:
        print(f"Generated {output}")
    return True


def _demo(open_browser: bool) -> bool:
    output = build_demo()
    print(f"Generated {output}")
    if open_browser:
        webbrowser.open(output.as_uri())
    return True


def _list_rules() -> bool:
    print(format_rule_list())
    return True


def _playbook(rule_id: str) -> bool:
    try:
        print(format_playbook(rule_id))
    except (FileNotFoundError, KeyError) as exc:
        print(str(exc))
        return False
    return True


def _explain(rule_id: str) -> bool:
    try:
        print(format_detection(rule_id))
    except KeyError as exc:
        print(str(exc))
        return False
    return True


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Safe Microsoft Entra ID detection lab")
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("audit", help="reject private or unsafe repository artifacts")
    subparsers.add_parser("validate", help="validate rules and synthetic fixtures")
    subparsers.add_parser("report", help="build validation reports")
    demo_parser = subparsers.add_parser("demo", help="build the local interactive demo")
    demo_parser.add_argument("--open", action="store_true", help="open the demo in a browser")
    subparsers.add_parser("list-rules", help="list detections and their playbooks")
    explain_parser = subparsers.add_parser("explain", help="explain one detection")
    explain_parser.add_argument("rule_id", help="detection id such as ENTRA-003")
    playbook_parser = subparsers.add_parser("playbook", help="print one detection playbook")
    playbook_parser.add_argument("rule_id", help="detection id such as ENTRA-001")
    subparsers.add_parser("all", help="run audit, validation and reports")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "audit":
        return 0 if _audit() else 1
    if args.command == "validate":
        return 0 if _validate() else 1
    if args.command == "report":
        return 0 if _report() else 1
    if args.command == "demo":
        return 0 if _demo(args.open) else 1
    if args.command == "list-rules":
        return 0 if _list_rules() else 1
    if args.command == "explain":
        return 0 if _explain(args.rule_id) else 1
    if args.command == "playbook":
        return 0 if _playbook(args.rule_id) else 1
    audit_ok = _audit()
    validation_ok = _validate()
    report_ok = _report() if validation_ok else False
    return 0 if all((audit_ok, validation_ok, report_ok)) else 1


if __name__ == "__main__":
    raise SystemExit(main())
