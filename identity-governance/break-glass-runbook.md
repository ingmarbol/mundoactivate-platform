# Break-glass runbook

## Trigger

Use only when normal federation, MFA/PIM activation, or the primary identity
provider is unavailable and a production recovery action cannot wait.

## Procedure

1. Declare an incident and record the ticket, severity, requester and approver.
2. Obtain two-person approval from Security and Platform Operations.
3. Retrieve one emergency credential from its independent protected location.
4. Use a hardened Privileged Access Workstation and the minimum emergency role.
5. Announce activation, start session recording and monitor audit events.
6. Perform only the approved recovery actions; do not use daily admin tooling.
7. End the session, rotate/reseal credentials and verify log delivery.
8. Review every command, restore normal federation and close temporary access.
9. Complete a post-incident review within two business days.

## Quarterly test evidence

- Successful authentication without depending on the normal identity provider.
- Alert received by Security Operations.
- Audit trail links incident, approver, identity, actions and timestamps.
- Credential storage remains independent and protected.
- No standing use outside tests or declared incidents.
