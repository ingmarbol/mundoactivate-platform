# Local idempotent event consumer

This lab demonstrates at-least-once delivery, duplicate detection, schema
validation, and dead-letter handling without creating cloud resources.

```bash
python3 event-driven/processor.py \
  --input event-driven/events.jsonl \
  --state event-driven/state.json \
  --dlq event-driven/dlq.jsonl
```

Run it twice. The first run processes two unique valid events, identifies one
duplicate, and sends one invalid event to the DLQ. The second run performs no
duplicate business effect.

Generated `state.json` and `dlq.jsonl` are local evidence and should not be
committed. Production requires a durable conditional-write idempotency store,
schema registry/validation, encryption, least-privilege identity, monitoring,
retention, and controlled redrive.
