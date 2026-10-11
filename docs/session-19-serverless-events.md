# Session 19 - Serverless and event-driven architecture

## Objective

Implement and explain an idempotent local consumer, then map its reliability,
security, observability, and cost controls to AWS and Azure.

## Scope

- Synthetic JSON events.
- Local Python consumer with duplicate detection and dead-letter output.
- No cloud deployment, credentials, customer data, or billable resources.

## Test procedure

Run the command in `event-driven/README.md` twice. Confirm the first execution
processes two unique events, detects a duplicate, and dead-letters one invalid
event. Confirm the second execution creates no duplicate side effect.

## Expected result and evidence

Share both command outputs, the generated state and DLQ after checking they
contain no sensitive data, and an explanation of the crash window between the
business effect and saving the idempotency state.

## Security and cost impact

The lab is local and synthetic. Production should use IAM Roles or Managed
Identities, conditional writes, encrypted queues, schema validation, bounded
retries, DLQ alarms, controlled redrive, and telemetry sampling.

## Cleanup

Remove generated `event-driven/state.json` and `event-driven/dlq.jsonl`.
No cloud cleanup is required.
