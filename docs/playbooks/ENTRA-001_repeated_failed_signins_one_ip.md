# ENTRA-001 Repeated failed sign-ins from one IP

## Trigger

Five failed sign-ins in five minutes from the same source IP and application.

## Triage

- Confirm source ownership and whether it belongs to expected infrastructure.
- Review affected user, application and country context.
- Check whether the activity is tied to support testing or broken automation.

## Decision

Escalate when the source is unfamiliar, the failures continue, or the affected identity is sensitive.

## Tuning

Only tune trusted sources with a named owner, reason and review date.
