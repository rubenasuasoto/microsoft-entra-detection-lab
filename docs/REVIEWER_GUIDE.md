# Reviewer guide

This guide gives a short technical walkthrough for reviewers.

## Three-minute path

1. Open `reports/latest/demo.html`.
2. Select `ENTRA-003-POS`.
3. Review the timeline and matched fields.
4. Open the GitBook playbook link for `ENTRA-003`.
5. Compare the scenario with `reports/latest/report.html`.

## What To Look For

- The lab uses synthetic Entra sign-in and audit events.
- The oracle evaluates every scenario and compares expected vs observed results.
- Tuning cases remain visible as alerts where the safest default is analyst review.
- The demo is static HTML and does not make live network calls.

## Limits

The first release does not connect to Microsoft Graph, does not use a tenant, and does not include credentials, tokens, production logs, app registrations or uploads.
