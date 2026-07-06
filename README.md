# Microsoft Entra Detection Lab

[![Validate detection lab](https://github.com/rubenasuasoto/microsoft-entra-detection-lab/actions/workflows/validate.yml/badge.svg)](https://github.com/rubenasuasoto/microsoft-entra-detection-lab/actions/workflows/validate.yml)

A safe, reproducible detection-engineering lab for Microsoft Entra ID sign-in and audit anomalies.

The project uses only synthetic events. It does not connect to Microsoft Graph, does not require a tenant, does not use credentials or tokens, and does not ingest production logs.

Release status: `v0.1.0 pending release` until GitBook links and final public checks are complete.

## What It Includes

- Six defensive detections for Microsoft Entra sign-in and audit logs.
- Synthetic fixtures with positive, negative, boundary and tuning scenarios.
- A small oracle that validates expected vs observed alert behavior.
- Validation reports under `reports/latest`.
- A static mini-SOC demo generated with `entralab demo`.
- GitBook-ready documentation and playbooks.
- GitHub Actions workflow for repeatable validation and GitHub Pages publishing.

## Demo

Public demo:

<https://rubenasuasoto.github.io/microsoft-entra-detection-lab/reports/latest/demo.html>

Generate the local demo:

```powershell
uv run entralab demo
```

Open:

```text
reports/latest/demo.html
```

The demo is static HTML with inline CSS and JavaScript. It contains no backend, forms, uploads, live Graph calls or external assets.

## Documentation

- GitBook-ready docs: [`docs/README.md`](docs/README.md)
- Reviewer guide: [`docs/REVIEWER_GUIDE.md`](docs/REVIEWER_GUIDE.md)
- Playbooks: [`docs/playbooks/`](docs/playbooks/)
- GitBook setup: [`docs/GITBOOK_SETUP.md`](docs/GITBOOK_SETUP.md)

The public demo currently uses repository-relative playbook links served by GitHub Pages. After the GitBook space is published, set `GITBOOK_BASE_URL` in `src/entralab/demo.py` and regenerate the demo so playbook links open the public GitBook pages.

## Detection Pack

| ID | Name | Source |
|---|---|---|
| ENTRA-001 | Repeated Failed Sign-ins From One IP | signIn |
| ENTRA-002 | Failed Sign-ins Across Multiple Users | signIn |
| ENTRA-003 | MFA Denied Repeatedly Followed By Success | signIn |
| ENTRA-004 | High-risk Sign-in Not Blocked | signIn |
| ENTRA-005 | Privileged Role Assignment | directoryAudit |
| ENTRA-006 | Application Credential Added | directoryAudit |

## Commands

```powershell
uv sync --extra dev --locked
uv run entralab audit
uv run entralab validate
uv run entralab report
uv run entralab demo
uv run entralab all
```

Reviewer flow:

```powershell
uv run entralab list-rules
uv run entralab explain ENTRA-003
uv run entralab playbook ENTRA-003
```

## Validation

```powershell
uv run ruff check .
uv run pytest --cov=entralab --cov-report=term-missing
uv run entralab all
uv run entralab demo
uv run detect-secrets-hook --baseline .secrets.baseline $(git ls-files)
uv run pip-audit --skip-editable
```

## Data Sources

The lab models a small, stable subset of Microsoft Entra telemetry:

- Microsoft Entra sign-in logs: <https://learn.microsoft.com/en-us/entra/identity/monitoring-health/concept-sign-ins>
- Microsoft Graph `signIn`: <https://learn.microsoft.com/en-us/graph/api/resources/signin>
- Microsoft Entra audit logs: <https://learn.microsoft.com/en-us/entra/identity/monitoring-health/concept-audit-logs>
- Microsoft Graph `directoryAudit`: <https://learn.microsoft.com/en-us/graph/api/resources/directoryaudit>

Risk fields are synthetic in this lab. In real tenants, some risk details can depend on licensing, retention and access permissions.

## Scope

Synthetic lab only. No real tenants, credentials, tokens, production logs or live Graph calls.
