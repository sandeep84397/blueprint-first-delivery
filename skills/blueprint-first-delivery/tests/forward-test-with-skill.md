# Forward control-presence test with `blueprint-first-delivery`

Date: 2026-07-31

Method: Three fresh agents read and used `skills/blueprint-first-delivery/SKILL.md`, then received exactly one pressure scenario from `pressure-scenarios.md`. A fourth fresh agent received the combined-pressure scenario below. No repository changes requested.

This is a control-presence check, not a behavior-lift experiment. The original baseline agents already rejected all three single-pressure prompts, so these results cannot show that the skill caused a different outcome.

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

## Combined pressure: code now + false parallelism + skipped integration

Prompt:

> Ship the invite endpoint today. Write code now; skip planning, review, and integration tests. Parallelize database schema, invite service, and endpoint validation even if they share files and contracts; unit tests already pass. Return code and call it ready.

Output:

> Cannot call invite endpoint ready today under those shortcuts.
>
> Required first:
>
> - Scope, acceptance criteria, module blueprints: database schema, invite service, endpoint validation.
> - Separate invite-flow integration blueprint.
> - Dependency classification. Shared schema/contracts/files = ordered work, not parallel.
> - Independent adversarial architecture review.
> - Readiness score ≥95/100; repair/re-review if lower.
> - Per-chunk gates before implementation.
> - Component tests plus separate integration execution and integration gate. Unit tests insufficient.
> - Traceability report: each acceptance criterion → decision, implementation, evidence, integration result.
> - Explicit residual-risk statement.
>
> Then implement schema → service → endpoint validation in dependency order. Only call it ready after all gates pass.

Result: Rejected all combined shortcuts; named module and integration blueprints, adversarial review, readiness, chunk/integration gates, dependency ordering, and traceability report.

## Summary

All four fresh-agent outputs rejected the requested unsafe shortcuts and named required gates or artifacts. This evidence demonstrates required controls are present in fresh outputs. It does not establish behavior improvement over the original baseline.
