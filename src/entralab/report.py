from __future__ import annotations

import csv
import hashlib
import html
import json
from io import StringIO
from pathlib import Path
from typing import Any

from .paths import ARTIFACTS_DIR, MANIFEST_PATH, REPORTS_DIR, ensure_output_directories
from .rules import load_manifest


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _fingerprint() -> str:
    digest = hashlib.sha256()
    for path in sorted(MANIFEST_PATH.parent.glob("*")):
        if path.is_file():
            digest.update(path.name.encode())
            digest.update(path.read_text(encoding="utf-8").encode("utf-8"))
    return digest.hexdigest()[:12]


def _matrix_csv(cases: list[dict[str, Any]]) -> str:
    output = StringIO(newline="")
    fields = [
        "case_id",
        "rule_id",
        "category",
        "expected",
        "observed",
        "status",
        "disposition",
        "matched_event_count",
        "matched_fields",
        "note",
    ]
    writer = csv.DictWriter(output, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    for case in cases:
        row = dict(case)
        row["matched_fields"] = ";".join(case["matched_fields"])
        writer.writerow({field: row[field] for field in fields})
    return output.getvalue()


def _markdown(manifest: dict[str, Any], validation: dict[str, Any], fingerprint: str) -> str:
    summary = validation["summary"]
    lines = [
        "# Validation report",
        "",
        "Defensive Microsoft Entra ID detection lab using synthetic sign-in and audit events.",
        "",
        f"**Pack fingerprint:** `{fingerprint}`",
        "",
        "## Summary",
        "",
        f"- Valid detections: {summary['rules_valid']}/{summary['rules_total']}",
        f"- Passing cases: {summary['cases_passed']}/{summary['cases_total']}",
        f"- Cases marked for tuning: {summary['cases_tuning']}",
        "",
        "## Detections",
        "",
        "| ID | Title | Source | Risk | Priority | Threshold | ATT&CK |",
        "|---|---|---|---|---|---|---|",
    ]
    for item in manifest["detections"]:
        lines.append(
            f"| {item['key']} | {item['title']} | {item['log_source']} | {item['risk']} | "
            f"{item['triage_priority']} | {item['threshold']} | {', '.join(item['attack']) or 'Operational'} |"
        )
    lines.extend(
        [
            "",
            "## Validation matrix",
            "",
            "| Case | Rule | Category | Expected | Observed | Result | Disposition |",
            "|---|---|---|---:|---:|---|---|",
        ]
    )
    for case in validation["cases"]:
        lines.append(
            f"| {case['case_id']} | {case['rule_id']} | {case['category']} | "
            f"{str(case['expected']).lower()} | {str(case['observed']).lower()} | "
            f"{case['status']} | {case['disposition']} |"
        )
    lines.extend(
        [
            "",
            "## Scope",
            "",
            "The report is generated from synthetic fixtures. It does not connect to Microsoft Graph, tenants, credentials, tokens or production logs.",
            "",
        ]
    )
    return "\n".join(lines)


def _html_report(manifest: dict[str, Any], validation: dict[str, Any], fingerprint: str) -> str:
    summary = validation["summary"]
    cards = "".join(
        f"""
        <article class="detection">
          <div><span>{html.escape(item['key'])}</span><strong>{html.escape(item['title'])}</strong></div>
          <p>{html.escape(item['threshold'])}</p>
          <small>{html.escape(item['log_source'])} | {html.escape(item['risk'])} | {html.escape(item['triage_priority'])}</small>
        </article>
        """
        for item in manifest["detections"]
    )
    rows = "".join(
        f"""
        <tr>
          <td><strong>{html.escape(case['case_id'])}</strong><small>{html.escape(case['note'])}</small></td>
          <td>{html.escape(case['rule_id'])}</td>
          <td>{html.escape(case['category'])}</td>
          <td>{str(case['expected']).lower()}</td>
          <td>{str(case['observed']).lower()}</td>
          <td><span class="status {html.escape(case['status'])}">{html.escape(case['status'])}</span></td>
          <td><span class="status {html.escape(case['disposition'])}">{html.escape(case['disposition'])}</span></td>
        </tr>
        """
        for case in validation["cases"]
    )
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Microsoft Entra Detection Lab</title>
  <style>
    :root {{ --bg:#101418; --panel:#182026; --panel2:#12191f; --ink:#f2f7fb; --muted:#a9b6c1; --line:#33424d; --accent:#62d5b4; --blue:#8fc2ff; --amber:#f3c76f; }}
    * {{ box-sizing:border-box; }} body {{ margin:0; background:var(--bg); color:var(--ink); font:15px/1.5 "Segoe UI",Arial,sans-serif; }}
    header {{ padding:30px max(24px,calc((100vw - 1180px)/2)); background:var(--panel2); border-bottom:1px solid var(--line); }}
    h1 {{ margin:0; font-size:30px; }} h2 {{ margin:0 0 14px; font-size:18px; }} p {{ color:var(--muted); }}
    main {{ max-width:1180px; margin:0 auto; padding:24px; display:grid; gap:18px; }}
    section {{ border:1px solid var(--line); background:var(--panel); border-radius:8px; padding:18px; }}
    .fingerprint {{ font:12px Consolas,monospace; color:var(--muted); }}
    .metrics {{ display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:12px; }}
    .metric {{ border:1px solid var(--line); background:var(--panel2); border-radius:7px; padding:14px; }} .metric strong {{ display:block; font-size:26px; color:var(--accent); }}
    .detections {{ display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:12px; }}
    .detection {{ border:1px solid var(--line); background:var(--panel2); border-radius:7px; padding:14px; }} .detection span {{ color:var(--blue); font:12px Consolas,monospace; margin-right:10px; }} .detection small {{ color:var(--muted); }}
    .table-wrap {{ overflow:auto; }} table {{ width:100%; min-width:850px; border-collapse:collapse; }} th,td {{ padding:10px; border-bottom:1px solid var(--line); text-align:left; vertical-align:top; }} th, td small {{ color:var(--muted); }} td small {{ display:block; max-width:360px; }}
    .status {{ padding:3px 7px; border-radius:999px; background:#26352f; }} .pass,.keep {{ color:var(--accent); }} .fail {{ color:#ff9c91; }} .tune {{ color:var(--amber); }}
    .notice {{ border-left:3px solid var(--amber); padding-left:12px; }}
    @media (max-width:760px) {{ .metrics,.detections {{ grid-template-columns:minmax(0,1fr); }} h1 {{ font-size:24px; }} }}
  </style>
</head>
<body>
  <header><h1>Microsoft Entra Detection Lab</h1><p>Reproducible defensive detection engineering with synthetic Entra ID telemetry.</p><span class="fingerprint">pack {fingerprint}</span></header>
  <main>
    <section class="metrics">
      <div class="metric"><strong>{summary['rules_valid']}/{summary['rules_total']}</strong><span>Valid detections</span></div>
      <div class="metric"><strong>{summary['cases_passed']}/{summary['cases_total']}</strong><span>Passing cases</span></div>
      <div class="metric"><strong>{summary['cases_tuning']}</strong><span>Tuning cases</span></div>
    </section>
    <section><h2>Detection pack</h2><div class="detections">{cards}</div></section>
    <section><h2>Validation matrix</h2><div class="table-wrap"><table><thead><tr><th>Case</th><th>Rule</th><th>Category</th><th>Expected</th><th>Observed</th><th>Result</th><th>Decision</th></tr></thead><tbody>{rows}</tbody></table></div></section>
    <section><h2>Scope</h2><p class="notice">Synthetic lab only. No real tenants, credentials, tokens, production logs or live Graph calls.</p></section>
  </main>
</body>
</html>
"""


def build_reports() -> list[Path]:
    ensure_output_directories()
    validation = _load_json(ARTIFACTS_DIR / "validation.json")
    manifest = load_manifest()
    fingerprint = _fingerprint()
    markdown_path = REPORTS_DIR / "report.md"
    html_path = REPORTS_DIR / "report.html"
    matrix_path = REPORTS_DIR / "validation-matrix.csv"
    markdown_path.write_text(
        _markdown(manifest, validation, fingerprint), encoding="utf-8", newline="\n"
    )
    html_path.write_text(
        _html_report(manifest, validation, fingerprint), encoding="utf-8", newline="\n"
    )
    matrix_path.write_text(_matrix_csv(validation["cases"]), encoding="utf-8", newline="\n")
    return [markdown_path, html_path, matrix_path]
