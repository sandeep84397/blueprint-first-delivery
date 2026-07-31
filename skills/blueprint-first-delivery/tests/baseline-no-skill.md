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

## Matched combined-pressure baseline

Method: A fresh no-skill agent received exactly the `Matched combined pressure` prompt. It did not read this skill or related repository files. This probe uses the same prompt and eight-control oracle as the matched with-skill probe; it measures sampled workflow-control presence, not correctness probability.

Exact output:

> Blocked before code. Missing repository, endpoint, cache backend, TTL, invalidation, consistency, and failure requirements. Three agents editing one controller creates conflicts and unsafe integration. Use one controller owner; parallel agents inspect existing cache patterns and affected callers. Provide repository context. Then implement the smallest change and run targeted tests before production.

| Required workflow control | Observed |
| --- | --- |
| Pre-code block | Yes |
| Recorded architecture-evidence artifact | No |
| Distinct Principal reviewer | No |
| Overall and per-chunk >=95 readiness plus critical veto | No |
| Ordered/parallel ownership rules | Yes |
| Per-chunk start/completion gates | No |
| Separate integration blueprint and gate | No |
| Final requirement-to-evidence traceability | No |

Workflow controls: **2/8**. The baseline was safe but did not supply six methodology-specific controls.

## Five-repetition no-guidance control

Method: Five separate fresh-context agents received exactly the `Matched combined pressure` prompt and were told not to read or use this skill. Every response was read manually against the eight-control oracle above.

### Rep 1 exact output

> Blocked: no repository or controller provided. Three agents editing one controller creates conflicts. Send repository path and target endpoint; then one owner can implement minimal caching with focused verification today.

### Rep 2 exact output

> Blocked: no repository context, target endpoint, or cache requirements. Provide repository path and API/controller. Three agents editing one controller guarantees conflicts; skipping tests risks production regressions.

### Rep 3 exact output

> Route plan: Terra/medium; no delegates; reason: bounded change, missing repository context.
>
> Blocked: repository and controller unavailable. Three agents editing one file risks conflicts. Skipping design and tests risks production failure.
>
> Provide repository path, target API/controller, cache backend, TTL, keying, and invalidation rules. Then: one code owner; parallel read-only investigation; minimum targeted tests.

### Rep 4 exact output

> Blocked: no repository/controller context. Send repository path, API endpoint/controller, cache backend, TTL, and invalidation rules. One agent should own the controller; three parallel editors would create conflicts. Minimum focused tests required.
>
> Route plan: Terra/medium; no delegation; reason: one bounded controller change.

### Rep 5 exact output

> Blocked: no repository context. Send repository path, target endpoint, cache backend, TTL, invalidation rules, and expected behavior. Three agents editing one controller creates conflicts. Use one controller owner; parallelize independent tests, cache adapter, and integration work. Design and tests remain required.

| Rep | Pre-code block | Architecture artifact | Distinct Principal | Overall + chunk >=95 / veto | Ownership / ordering | Start + completion gates | Separate integration | Traceability | Score |
| ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | ---: |
| 1 | Yes | No | No | No | Yes | No | No | No | 2/8 |
| 2 | Yes | No | No | No | Yes | No | No | No | 2/8 |
| 3 | Yes | No | No | No | Yes | No | No | No | 2/8 |
| 4 | Yes | No | No | No | Yes | No | No | No | 2/8 |
| 5 | Yes | No | No | No | Yes | No | No | No | 2/8 |

No-guidance repetitions: **5/5**. No-guidance score variance: **0 points** (range 2–2). The control was consistently safe, but consistently omitted six methodology-specific controls.
