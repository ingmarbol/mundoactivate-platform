# Session 29 - Backup, Restore and Cyber Recovery

The lab validates policy and synthetic restore evidence. It does not create,
delete or restore cloud resources.

```bash
python3 recovery/validate_recovery.py \
  --plan recovery/recovery-plan.yaml \
  --evidence recovery/restore-evidence.csv
```

Expected: `RESULT: CYBER RECOVERY BASELINE VALID`.

Negative test: copy the plan, change `immutable: true` to `false`, and verify
that the validator exits non-zero.

Before a real drill, use an isolated sandbox, budget limits, approved recovery
points and a cleanup owner. Keep restore evidence, but never retain recovered
production data longer than necessary.
