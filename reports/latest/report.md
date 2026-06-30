# Validation report

Defensive Microsoft Entra ID detection lab using synthetic sign-in and audit events.

**Pack fingerprint:** `ab6be44bc3b8`

## Summary

- Valid detections: 6/6
- Passing cases: 21/21
- Cases marked for tuning: 3

## Detections

| ID | Title | Source | Risk | Priority | Threshold | ATT&CK |
|---|---|---|---|---|---|---|
| ENTRA-001 | Repeated Failed Sign-ins From One IP | signIn | medium | P3 | 5 failed sign-ins in 5 minutes per IP and app | T1110 |
| ENTRA-002 | Failed Sign-ins Across Multiple Users | signIn | medium | P2 | 5 distinct users with failures in 10 minutes per IP and app | T1110.003 |
| ENTRA-003 | MFA Denied Repeatedly Followed By Success | signIn | high | P1 | 2 MFA denied failures followed by success in 15 minutes for the same user and IP | T1621, T1078 |
| ENTRA-004 | High-risk Sign-in Not Blocked | signIn | high | P1 | Successful medium or high risk sign-in where Conditional Access did not fail | T1078 |
| ENTRA-005 | Privileged Role Assignment | directoryAudit | high | P1 | Successful assignment to Global Administrator or Privileged Role Administrator | T1098 |
| ENTRA-006 | Application Credential Added | directoryAudit | medium | P2 | Successful application or service principal credential update | T1098.001 |

## Validation matrix

| Case | Rule | Category | Expected | Observed | Result | Disposition |
|---|---|---|---:|---:|---|---|
| ENTRA-001-POS | ENTRA-001 | positive | true | true | pass | keep |
| ENTRA-001-NEG | ENTRA-001 | negative | false | false | pass | keep |
| ENTRA-001-BOUNDARY | ENTRA-001 | boundary | false | false | pass | keep |
| ENTRA-002-POS | ENTRA-002 | positive | true | true | pass | keep |
| ENTRA-002-NEG | ENTRA-002 | negative | false | false | pass | keep |
| ENTRA-002-BOUNDARY | ENTRA-002 | boundary | false | false | pass | keep |
| ENTRA-003-POS | ENTRA-003 | positive | true | true | pass | keep |
| ENTRA-003-NEG | ENTRA-003 | negative | false | false | pass | keep |
| ENTRA-003-BOUNDARY | ENTRA-003 | boundary | false | false | pass | keep |
| ENTRA-003-TUNE | ENTRA-003 | false_positive | true | true | pass | tune |
| ENTRA-004-POS | ENTRA-004 | positive | true | true | pass | keep |
| ENTRA-004-NEG | ENTRA-004 | negative | false | false | pass | keep |
| ENTRA-004-BOUNDARY | ENTRA-004 | boundary | false | false | pass | keep |
| ENTRA-005-POS | ENTRA-005 | positive | true | true | pass | keep |
| ENTRA-005-NEG | ENTRA-005 | negative | false | false | pass | keep |
| ENTRA-005-BOUNDARY | ENTRA-005 | boundary | false | false | pass | keep |
| ENTRA-005-TUNE | ENTRA-005 | false_positive | true | true | pass | tune |
| ENTRA-006-POS | ENTRA-006 | positive | true | true | pass | keep |
| ENTRA-006-NEG | ENTRA-006 | negative | false | false | pass | keep |
| ENTRA-006-BOUNDARY | ENTRA-006 | boundary | false | false | pass | keep |
| ENTRA-006-TUNE | ENTRA-006 | false_positive | true | true | pass | tune |

## Scope

The report is generated from synthetic fixtures. It does not connect to Microsoft Graph, tenants, credentials, tokens or production logs.
