# Adaptive evidence-first policy

Use the cheapest route that satisfies the exact predicates below. Route is a delivery-process decision; model routing remains in `model-routing.md`.

## Deterministic route

1. Select **Direct** only when every Direct predicate passes.
2. Select **Full** when any Full hard trigger applies.
3. Select **Lite** otherwise.

Do not compensate for a failed Direct predicate with a high readiness score. A missing oracle, unresolved fact, or handoff is not a minor deduction.

### Direct: every predicate must pass

- One observable behavior, module, and state owner.
- No public/shared contract, schema, persistence, lifecycle, concurrency, security, privacy, or external-system change.
- A deterministic oracle exists before work starts.
- Blast radius is reversible and the changed scope is bounded.
- No handoff or multi-turn continuity need.

Record outcome, owner, exact changed scope, oracle/result, and rollback in a Direct receipt. Any failed predicate routes to Lite or Full.

### Lite: bounded, non-trivial work

Lite covers a bounded change that is not Direct and has no Full trigger. Create a Lite card with outcome, boundary, invariant, owner, scope, failure/rollback, deterministic oracle, and route reason. Architecture discovery is proportionate, not a substitute for Full review.

Use source-linked Agent Brain whenever Lite crosses a handoff or multiple turns. A single short, self-contained Lite task may omit it.

### Full: any hard trigger is sufficient

- Public/shared contracts, multi-module responsibility, or more than one state owner on a causal path.
- Persistence, migration, recovery, deletion, integrity, concurrency, lifecycle, device, WebView, or security/privacy/authentication/money/irreversible effect.
- Unknown external behavior, external dependency uncertainty, missing deterministic oracle, or an unresolved critical assumption.

Full work has a module blueprint, proof matrix, immutable baseline, principal review, task gates, early integration proof, final integration gate, and source-linked Agent Brain. Outcome-backward and forward reconciliation runs only for Full.

## Approval states

`TRIAGED → ARCHITECTURE_APPROVED → PLAN_FROZEN → TASK_PROVEN → INTEGRATION_PROVEN → DELIVERY_READY`

`BLOCKED` and `STALE` invalidate the affected approval. A user-facing report states why the state changed, which proof/baseline is affected, the owner, and what input would unblock it. Architecture approval validates design feasibility; plan freeze validates traceability and future proof ownership; task proof validates implemented work; integration proof validates cross-boundary behavior; delivery readiness validates the complete outcome.

## Integration timing

For Full work, run an early vertical proof after the first compatible producer and consumer exist. It exercises the frozen boundary before remaining modules grow around an untested assumption. Final integration is still separate and covers the complete outcome.

## Parallel work

Parallel implementation needs frozen versioned contracts, exclusive file/state ownership, independent oracle, an integration owner, and integration order. Otherwise work is ordered. A route never authorizes false independence.

## Compatibility

Existing blueprints are historical. Apply this policy to new work and future affected tasks; do not rewrite an already-delivered artifact solely to add route metadata.

## Project boundary

No UI, viewer, HTML, extension, or GitHub Pages artifact belongs in this package. Interactive graph work belongs to its separate project.
