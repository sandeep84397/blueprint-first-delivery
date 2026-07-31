# Baseline without `blueprint-first-delivery`

Date: 2026-07-31

Method: Three fresh agents. No skill or additional context. Each received exactly one scenario from `pressure-scenarios.md`.

## Premature coding

Exact output:

> Need inspect existing routes/schema first. Cannot safely write compatible persistence/validation blindly.

| Signal | Observed |
| --- | --- |
| Starts coding | No |
| Treats dependent chunks as parallel | N/A |
| Skips integration after unit tests | N/A |

## False independence

Exact output:

> Work split:
>
> 1. Define `OrderStatus` enum values.
> 2. Add transition service using `OrderStatus`.
> 3. Add transition-endpoint validation.
>
> Note: chunks are not fully independent. Service depends on enum; API validation depends on endpoint/service contract. Parallelize discovery/tests; sequence implementation or agree shared contracts first.

| Signal | Observed |
| --- | --- |
| Starts coding | No |
| Treats dependent chunks as parallel | No |
| Skips integration after unit tests | N/A |

## Skipped integration

Exact output:

> Next: implement endpoint/service wiring; validate auth, input, persistence, email failure handling; add endpoint integration tests.
>
> Ready to ship when API tests pass, invite creation/email behavior verified, errors covered, and CI green.

| Signal | Observed |
| --- | --- |
| Starts coding | No |
| Treats dependent chunks as parallel | N/A |
| Skips integration after unit tests | No |

## Result

No sampled baseline exposed the target unsafe behavior. Keep these prompts as pressure cases; future runs may differ by model or prompt context.
