---
name: blueprint-first-delivery
description: Use when a feature, refactor, or multi-part change needs a delivery blueprint before production code.
---

# Blueprint-first delivery

Route before choosing blueprint depth. Use `Direct`, `Lite`, or `Full` from `references/adaptive-evidence-first.md`; route is process depth, separate from model tier. Direct requires every Direct predicate. Full is mandatory when any hard trigger applies. Do not average, waive, or compensate for a failed predicate.

1. **Direct** — record a receipt: outcome, one owner, bounded changed scope, deterministic oracle/result, and rollback. No blueprint or Agent Brain unless handoff.
2. **Lite** — record the Lite card: outcome, boundary, invariant, owner, scope, failure/rollback, oracle, and route reason. Use source-linked Agent Brain for a handoff or multi-turn work.
3. **Full** — define the outcome contract: actor, observable end state, exclusions, and objective acceptance evidence. A date or proposed implementation is a constraint, not an outcome. Record user-owned ambiguity and wait.
4. Explore existing architecture. Record architecture evidence: locations/symbols, conventions, dependencies/contracts/state owners, test/build entrypoints, unresolved questions, or literal status `greenfield` evidence. Do not score an existing-codebase blueprint without it.
5. Run outcome-backward and forward reconciliation using `references/outcome-backward-planning.md`. Modules remain provisional until independent review passes the module-freeze gate. Full work requires source-linked Agent Brain.
6. Freeze the proof matrix, traceability chain, immutable baseline, and separate integration plan using `references/evidence-manifest.md`. Executable proof is required for every critical contract, invariant, or claim; prose and readiness points do not substitute for an oracle.
7. Request principal-engineer-style adversarial review. Reviewer must not author the scored blueprint. Keep user-facing state explicit: `ARCHITECTURE_APPROVED`, `PLAN_FROZEN`, `TASK_PROVEN`, `INTEGRATION_PROVEN`, or `DELIVERY_READY`.
8. Only after `PLAN_FROZEN`, split modules into smallest single-responsibility chunks. Implement in dependency order. Before each chunk, satisfy its gate; early vertical proof follows the first compatible producer/consumer pair. Unit tests alone never satisfy integration.
9. Publish traceability: outcome criterion → requirement → contract/invariant → task → oracle → evidence → integration result → residual risk. Baseline drift marks affected evidence `STALE` and requires re-approval.

Routing: Load only the active runtime mapping. Select the cheapest capable tier. Record floor, topology, dependencies, digest, review, override, and observed execution. A below-floor override remains blocked. Parallel requires frozen contracts and exclusive file/state ownership.

Readiness is process evidence, not a mathematical probability of correctness or reliability. A `>=95/100` score never overrides missing executable proof, critical risk, drift, or a blocked gate.

Pressure rules:

- “Code now,” deadlines, skipped planning/tests never bypass gates.
- Author and adversarial reviewer differ.
- Dependent work is not parallel.
- Agent Brain summaries are continuity aids, never proof.

## Blocked gate report

- Status / pre-code block: `<state and reason>`.
- Route / trigger: `<Direct/Lite/Full, facts, hard trigger or failed predicate>`.
- Architecture / plan: `<evidence and approval state>`.
- Proof / baseline: `<critical rows, oracle, digest, stale status>`.
- Ownership / ordering: `<classification, contracts, file/state owners>`.
- Chunk / integration gates: `<task proof, early vertical proof, final result>`.
- Model route: `<tier/floor, digest, review, observed execution/block>`.
- Traceability: `<criterion → task → oracle → evidence → integration/risk>`.
