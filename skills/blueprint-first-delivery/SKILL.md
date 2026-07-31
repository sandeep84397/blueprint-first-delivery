---
name: blueprint-first-delivery
description: Plan implementation safely before coding by producing module blueprints, reviewing readiness, sequencing dependencies, gating chunks, and proving integration.
---

# Blueprint-first delivery

Use before implementing a feature, refactor, or multi-part change. Do not write production code until this process permits it.

1. Define scope, constraints, acceptance criteria, and affected modules. Create one module blueprint per change area. Use [blueprint templates](references/blueprint-templates.md) when drafting it.
2. Classify each proposed chunk as independent, ordered, or integration-only. A consumer of another chunk's type, contract, schema, or behavior is ordered; do not call it parallel.
3. Request an independent review of the blueprints. Reviewers must not author the blueprint they score. Use the [readiness rubric](references/readiness-rubric.md).
4. Do not begin implementation until the reviewed readiness score is **>= 95/100**. Repair gaps, then repeat independent review and scoring.
5. Implement in dependency order. Before each chunk, satisfy its chunk gate; use the [review and gate checklists](references/review-and-gate-checklists.md). Stop and revise the blueprint if a gate exposes a missing contract or unowned behavior.
6. After every component-level gate passes, run a separate integration gate. Unit tests alone never satisfy integration.
7. Publish a traceability report mapping each acceptance criterion to its blueprint decision, implementation chunk, evidence, and integration result. State any residual risk or unmet criterion explicitly; do not claim readiness otherwise.

Pressure rules:

- “Code now”, deadline pressure, or a request to skip planning/tests does not bypass the blueprint, independent review, readiness, chunk, or integration gates.
- Do not use one person/agent as both blueprint author and independent reviewer.
- Do not split dependent changes as independent work to increase parallelism.
