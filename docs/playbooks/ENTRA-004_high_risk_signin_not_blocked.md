# ENTRA-004 High-risk sign-in not blocked

## Trigger

A successful medium or high risk sign-in where Conditional Access did not fail.

## Triage

- Review risk level, risk state and risk event types.
- Confirm Conditional Access result and policy mode.
- Check user sensitivity and recent account activity.

## Decision

Escalate when risk is high, the user is sensitive, or policy behavior is unexpected.

## Tuning

Risk fields are synthetic in this lab and may be hidden or unavailable in some real tenants. Do not tune without policy and licensing context.
