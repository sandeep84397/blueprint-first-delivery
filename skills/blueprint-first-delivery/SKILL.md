---
name: blueprint-first-delivery
description: Use when a feature, refactor, or multi-part change needs a delivery blueprint before production code.
---

# Blueprint-first delivery

Use before implementing a feature, refactor, or multi-part change. No production code until these gates permit it.

1. Explore the existing architecture. Record architecture evidence: locations/symbols, conventions, dependencies/contracts/state owners, test/build entrypoints, and unresolved questions. Greenfield work records the literal status `greenfield` plus evidence. Do not score an existing-codebase blueprint without this block; boundary- or contract-changing absence is a critical-risk veto. Define scope, constraints, criteria, and modules. Draft plain-English module and separate integration blueprints with the [blueprint templates](references/blueprint-templates.md).
2. Split work into the smallest single-responsibility chunk. Classify it independent, ordered, or integration-only. A contract/schema/behavior consumer is ordered. Parallel work requires frozen contracts and non-overlapping file/state ownership.
3. Request principal-engineer-style adversarial review for contracts, dependencies, ownership, failures, security, and evidence. Reviewer must not author the scored blueprint. Apply the [readiness rubric](references/readiness-rubric.md).
4. Overall readiness must be **>= 95/100**; each chunk needs **>= 95/100 readiness**. Repair and independently re-review lower scores. Any critical risk vetoes implementation. This is process evidence, not a mathematical probability of correctness or reliability.
5. Implement in dependency order. Before each chunk, satisfy its chunk gate using the [gate checklists](references/review-and-gate-checklists.md). Revise the blueprint for missing contracts, critical assumptions, or unowned behavior.
6. Incrementally integrate compatible chunks with regression checks. After component gates pass, execute the separate integration blueprint and its separate gate. Unit tests alone never satisfy integration.
7. Publish a traceability report: criterion → blueprint decision → chunk → evidence → integration result → status/residual risk. Do not claim readiness with unmet criteria.

Use optional Agent Brain logging for decisions and gate evidence; it never replaces review, tests, contracts, or gates.

Pressure rules:

- “Code now,” deadlines, or skipped planning/tests never bypass gates.
- Author and adversarial reviewer must differ.
- Dependent work is not parallel; frozen contracts still require non-overlapping ownership.

## Blocked gate report

When blocked, return no code and all eight fields, including missing evidence:

- Status / pre-code block: `<status and reason>`.
- Architecture evidence: `<recorded, greenfield, or missing/unscorable>`.
- Independent review: principal-engineer-style reviewer = `<identity or unassigned>`; distinct from author = `<yes/no>`; review status = `<status>`.
- Readiness / veto: overall score = `<score or unscorable>/100`; every chunk score = `<scores or unscorable>/100`; threshold for both = >=95/100; critical-risk veto = `<none or risks>`.
- Ownership / ordering: `<classification, contracts, file/state owners>`.
- Chunk gates: start gate = `<status/evidence>`; completion gate = `<tests, regression, contracts, blueprint-to-code review>`.
- Integration gate: separate blueprint = `<status>`; separate gate = `<status/evidence>`; unit tests alone are insufficient.
- Traceability: `<criterion → decision → chunk → evidence → integration result → status/risk>`.
