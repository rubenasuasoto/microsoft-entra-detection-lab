# Detection catalog

| ID | Detection | Source | Priority | Review focus |
|---|---|---|---|---|
| ENTRA-001 | Repeated Failed Sign-ins From One IP | signIn | P3 | Noisy source, broken automation or password guessing |
| ENTRA-002 | Failed Sign-ins Across Multiple Users | signIn | P2 | Password spraying indicator |
| ENTRA-003 | MFA Denied Repeatedly Followed By Success | signIn | P1 | MFA fatigue or suspicious authentication sequence |
| ENTRA-004 | High-risk Sign-in Not Blocked | signIn | P1 | Risk and Conditional Access control review |
| ENTRA-005 | Privileged Role Assignment | directoryAudit | P1 | Administrative role change review |
| ENTRA-006 | Application Credential Added | directoryAudit | P2 | App or service principal credential hygiene |

Each detection has positive, negative and boundary scenarios. Selected detections also include tuning scenarios that continue to alert until there is approved environment context.
