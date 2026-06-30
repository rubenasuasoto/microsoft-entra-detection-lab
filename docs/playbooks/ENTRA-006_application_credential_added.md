# ENTRA-006 Application credential added

## Trigger

A successful application or service principal credential update.

## Triage

- Confirm app owner and business purpose.
- Review credential type, expiration and change timing.
- Check app permissions and whether the change matches an approved rotation.

## Decision

Escalate when the app is sensitive, owner is unclear, or the change does not match rotation records.

## Tuning

Baseline approved credential rotation pipelines with owner, app, expiration and review date.
