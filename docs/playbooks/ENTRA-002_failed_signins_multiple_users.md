# ENTRA-002 Failed sign-ins across multiple users

## Trigger

Five distinct users with failed sign-ins from the same source IP and application in ten minutes.

## Triage

- Count distinct users and affected applications.
- Check whether the source is an approved gateway or identity test system.
- Review whether any sensitive accounts are included.

## Decision

Escalate when the source is unfamiliar or attempts cover several unrelated users.

## Tuning

Document approved shared sources and expire exceptions that are no longer needed.
