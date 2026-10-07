# Chaos experiment checklist

## Preflight

- [ ] Context is local or development, never production.
- [ ] Steady state has been observed for five minutes.
- [ ] Hypothesis, target, duration, and maximum blast radius are explicit.
- [ ] Safety Officer can stop the experiment independently.
- [ ] Abort conditions and rollback are testable.
- [ ] No secrets or customer data are present in evidence.

## Execution

- [ ] Record start time and exact target.
- [ ] Inject one variable only.
- [ ] Observe user-facing SLI and Kubernetes events.
- [ ] Abort immediately if a threshold is crossed.
- [ ] Record steady-state restoration time.

## Debrief

- [ ] Mark hypothesis supported or not supported.
- [ ] Record availability and recovery time.
- [ ] Create corrective actions with owner and date.
- [ ] Verify cleanup and schedule a repeat.
