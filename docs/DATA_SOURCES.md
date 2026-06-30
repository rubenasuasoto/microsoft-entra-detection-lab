# Data sources

The lab models two Microsoft Entra log families with synthetic records only.

## Sign-in Logs

Synthetic `signIn` records use these stable fields:

- `createdDateTime`
- `userPrincipalName`
- `ipAddress`
- `appDisplayName`
- `resourceDisplayName`
- `clientAppUsed`
- `isInteractive`
- `conditionalAccessStatus`
- `status.errorCode`
- `status.failureReason`
- `riskLevelDuringSignIn`
- `riskState`
- `riskEventTypes_v2`
- `location.countryOrRegion`

Official references:

- <https://learn.microsoft.com/en-us/entra/identity/monitoring-health/concept-sign-ins>
- <https://learn.microsoft.com/en-us/graph/api/resources/signin>

## Audit Logs

Synthetic `directoryAudit` records use these fields:

- `activityDateTime`
- `activityDisplayName`
- `category`
- `operationType`
- `result`
- `initiatedBy`
- `targetResources`
- `modifiedProperties`

Official references:

- <https://learn.microsoft.com/en-us/entra/identity/monitoring-health/concept-audit-logs>
- <https://learn.microsoft.com/en-us/graph/api/resources/directoryaudit>

## Risk Field Note

Risk values in this lab are synthetic. In real tenants, risk field visibility and retention can depend on licensing, permissions and configuration.
