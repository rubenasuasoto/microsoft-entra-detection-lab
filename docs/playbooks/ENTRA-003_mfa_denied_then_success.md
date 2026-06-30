# ENTRA-003 MFA denied repeatedly followed by success

## Trigger

Two MFA-denied sign-ins followed by a successful sign-in for the same user and source IP within fifteen minutes.

## Triage

- Contact the user through an approved channel.
- Review application, device, country and risk context.
- Check recent MFA registration and recovery events.

## Decision

Escalate if the user does not recognize the attempts or if the success follows repeated denial quickly.

## Tuning

Tune only known recovery or enrollment flows with owner and time-bounded evidence.
