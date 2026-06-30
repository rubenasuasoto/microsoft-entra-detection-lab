# ENTRA-005 Privileged role assignment

## Trigger

A successful assignment to Global Administrator or Privileged Role Administrator.

## Triage

- Validate initiator, assignee and target role.
- Confirm the change record and approval path.
- Review follow-on administrative activity.

## Decision

Escalate if the assignment lacks approval, targets an unexpected identity, or occurs outside the approved window.

## Tuning

Only tune with change evidence, approver, role, assignee and expiration.
