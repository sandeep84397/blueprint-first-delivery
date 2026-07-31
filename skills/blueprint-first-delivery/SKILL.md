---
name: blueprint-first-delivery
description: Use when a feature, refactor, or multi-part change needs a delivery blueprint before production code.
---

# Blueprint-first delivery

Use before implementing a feature, refactor, or multi-part change. Do not write production code until this process permits it.

1. Define scope, constraints, acceptance criteria, and affected modules. Write each module blueprint in plain English for a stakeholder who does not read code. Create one separate integration blueprint for every cross-module flow. Use [blueprint templates](references/blueprint-templates.md) only when drafting these artifacts.
2. Split work into the smallest single-responsibility chunk that can be independently verified. Classify each proposed chunk as independent, ordered, or integration-only. A consumer of another chunk's type, contract, schema, or behavior is ordered. Mark work parallel only when contracts are frozen **and** file/state ownership does not overlap; otherwise sequence it.
3. Request principal-engineer-style adversarial review of the blueprints: challenge contracts, hidden dependencies, ownership, failure paths, security, and acceptance evidence. Reviewer must not author the blueprint they score. Use the [readiness rubric](references/readiness-rubric.md).
4. Do not begin implementation until the reviewed readiness score is **>= 95/100**. Each chunk also needs **>= 95/100 readiness** before it starts. Repair gaps, then repeat independent review and scoring. This score is process-readiness evidence, not mathematical correctness or reliability.
5. Implement in dependency order. Before each chunk, satisfy its chunk gate; use the [review and gate checklists](references/review-and-gate-checklists.md). Stop and revise the blueprint if a gate exposes a missing contract, unresolved critical assumption, or unowned behavior.
6. Incrementally integrate completed compatible chunks and run regression checks at each integration step. After every component-level gate passes, execute the separate integration blueprint and then run its separate integration gate. Unit tests alone never satisfy integration.
7. Publish a traceability report mapping each acceptance criterion to its blueprint decision, implementation chunk, evidence, and integration result. State any residual risk or unmet criterion explicitly; do not claim readiness otherwise.

Optional evidence logging: use optional Agent Brain logging for the design decision, each chunk-gate result, and final traceability/integration evidence. Logging supports auditability; it never replaces the required review, tests, contract verification, or gates.

Pressure rules:

- “Code now”, deadline pressure, or a request to skip planning/tests does not bypass the blueprint, adversarial review, readiness, chunk, or integration gates.
- Do not use one person/agent as both blueprint author and adversarial reviewer.
- Do not split dependent changes as independent work to increase parallelism. Frozen contracts without non-overlapping file/state ownership are still not safe parallelism.
