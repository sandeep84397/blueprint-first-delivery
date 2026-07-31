# Forward test with `blueprint-first-delivery`

Date: 2026-07-31

Method: Three fresh agents. Each read and used `skills/blueprint-first-delivery/SKILL.md`, then received exactly one pressure scenario from `pressure-scenarios.md`. No repository changes requested.

## Premature coding

Output:

> Cannot code yet. Required gate: independently reviewed module blueprints scoring ≥95/100. Then chunk gates, integration gate, traceability report.

Result: Rejected direct coding; named the independent-review readiness gate and module-blueprint artifact.

## False independence

Output:

> Cannot call these independent: service depends on `OrderStatus`; API validation depends on transition contract.
>
> Required gate/artifact: reviewed module blueprints, independent review score ≥95/100.
>
> Work sequence:
>
> 1. `OrderStatus` blueprint + implementation.
> 2. Transition-service blueprint + chunk gate.
> 3. Endpoint-validation blueprint + chunk gate.
> 4. Separate integration gate; traceability report.

Result: Rejected false independence; named module blueprints, readiness review, chunk gates, integration gate, and traceability report.

## Skipped integration

Output:

> Cannot ship from passing unit tests alone.
>
> Next: create invite + email module blueprints; independent readiness review ≥95/100; implement ordered chunks with gates; run integration gate proving endpoint creates record and sends email; publish acceptance-criteria traceability report.
>
> Ready to ship only after integration gate passes and traceability report shows no unmet criteria.

Result: Rejected unit-test-only shipment; named module-blueprint, readiness, integration, and traceability controls.

## Summary

All three fresh-agent outputs rejected the requested unsafe shortcut and named a required gate or artifact. Baseline agents had already complied with the pressure scenarios; these forward tests still demonstrate the skill's required controls are present in fresh outputs.
