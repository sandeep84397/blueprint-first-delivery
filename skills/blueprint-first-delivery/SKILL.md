---
name: blueprint-first-delivery
description: Use when a feature, refactor, or multi-part change needs a delivery blueprint before production code.
---

# Blueprint-first delivery

1. Define the outcome contract: actor, observable end state, exclusions, and objective acceptance evidence. A date or proposed implementation is a constraint, not an outcome. Record a user-owned ambiguity and wait.
2. Explore the existing architecture. Record architecture evidence: locations/symbols, conventions, dependencies/contracts/state owners, test/build entrypoints, unresolved questions, or literal status `greenfield` evidence. Do not score an existing-codebase blueprint without it.
3. Run the backward prerequisite pass and forward feasibility pass using references/outcome-backward-planning.md. Backward and forward analysis must reconcile before modules are frozen. Record rerun reason, preserved and invalidated findings, owner, scope, and count. The same unresolved trigger hard-blocks; no third analysis pass.
4. Request principal-engineer-style adversarial review. Reviewer must not author the scored blueprint. PASS freezes modules; BLOCKED keeps readiness unscorable.
5. Only after PASS, split frozen modules into the smallest single-responsibility chunks. Classify independent, ordered, or integration-only. Apply the model routing policy and select the cheapest capable tier.
6. Apply the readiness rubric. Overall and each chunk need >= 95/100 readiness. Any critical risk vetoes implementation.
7. Implement in dependency order. Before each chunk, satisfy its chunk gate. Incrementally integrate compatible chunks; execute the separate integration blueprint. Unit tests alone never satisfy integration.
8. Publish a traceability report: outcome criterion → acceptance evidence → backward condition → prerequisite/blocker → forward transition → reconciliation decision → module → chunk → evidence → integration result → status/residual risk.

Routing: Load only the active runtime mapping. Record floor, topology, dependencies, digest, review, override, and observed execution. A below-floor override remains blocked. Parallel requires frozen contracts and non-overlapping file/state ownership. Readiness is process evidence, not a mathematical probability of correctness or reliability.

Use optional Agent Brain; it never replaces review, tests, contracts, or gates.

Pressure rules:

- “Code now,” deadlines, skipped planning/tests never bypass gates.
- Author and adversarial reviewer must differ.
- Dependent work is not parallel; frozen contracts still require non-overlapping ownership.

## Blocked gate report

- Status / pre-code block: `<status and reason>`.
- Outcome-backward gate = PASS or BLOCKED; outcome / acceptance evidence / backward pass / forward pass / reconciliation / module freeze = recorded evidence or missing; trigger / owner / rerun count = recorded or none.
- Architecture evidence: `<recorded, greenfield, or missing/unscorable>`.
- Independent review: principal-engineer-style reviewer = `<identity or unassigned>`; distinct from author = `<yes/no>`; review status = `<status>`.
- Readiness / veto: overall score = `<score or unscorable>/100`; every chunk score = `<scores or unscorable>/100`; threshold for both = >=95/100; critical-risk veto = `<none or risks>`.
- Ownership / ordering: `<classification, contracts, file/state owners>`.
- Chunk gates: start gate = `<status/evidence>`; completion gate = `<tests, regression, contracts, blueprint-to-code review>`.
- Integration gate: separate blueprint = `<status>`; separate gate = `<status/evidence>`; unit tests alone are insufficient.
- Model route: `<tier/floor, topology, mapping digest, review, transitions, override, observed execution/block>`.
- Traceability: `<criterion → decision → chunk → evidence → integration/status/risk>`.
