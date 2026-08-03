# Review and gate checklists

## Outcome-backward planning gate

- Stable observable outcome and objective acceptance evidence are recorded.
- Backward prerequisites and forward feasibility converge before module freeze.
- No user-owned ambiguity remains unresolved. No automatic rerun occurs before the answer.
- Critical prerequisites are resolved; ownership, contracts, and integration owner are clear.
- An independent reviewer records the module-freeze decision.
- PASS is required before chunking. BLOCKED is required before readiness scoring.
- No third analysis pass is allowed for the same unresolved trigger without materially new evidence.

## Principal-engineer-style adversarial blueprint review

- Reviewer is not the blueprint author.
- Architecture evidence is recorded: inspected locations, conventions, dependencies/contracts, state owners, test/build entrypoints, and unresolved questions or greenfield evidence.
- Do not score an existing-codebase blueprint without a complete architecture-evidence block. Boundary- or contract-affecting absence is an unresolved critical-risk veto.
- Challenge contracts, hidden dependencies, ownership, failure paths, security, and claimed evidence.
- All modules have scope, contracts, dependencies, verification, and risks.
- A separate integration blueprint covers every cross-module flow.
- Dependency classification is correct: independent, ordered, or integration-only. Parallel work has frozen contracts and non-overlapping file/state ownership.
- Review all chunk routes together; challenge under-routing and over-routing, false parallelism, risk-floor violations, unsupported execution claims, and expensive-tier inheritance.
- Routing author and principal reviewer differ. Every finding has a disposition.
- A below-floor override remains blocked and prevents readiness.
- Parallel groups record member chunk IDs, dependencies, frozen contract versions/references, exclusive file/state ownership, independent verification, integration owner, and integration order.
- Readiness score is recorded. Below 95/100: return for repair.

## Chunk gate

Before starting a chunk:

- Prerequisite ordered chunks and shared contracts are complete or explicitly stable.
- Before a chunk starts, resolve only the active runtime mapping and verify its version/digest.
- Deep or Maximum starts only when runtime evidence can verify the requested floor.
- Parallel chunks have frozen contracts and non-overlapping file/state ownership.
- Owner, acceptance criteria, and verification evidence are assigned.
- Boundary, error, security, compatibility, and rollback impacts are understood.

Before marking a chunk complete:

- Its focused tests and regression checks pass.
- A blueprint-to-code review confirms the implementation matches the approved scope, ownership, and acceptance criteria.
- Explicit contract verification confirms inputs, outputs, errors, compatibility, and boundary behavior.
- Its contract remains compatible with dependent chunks, with no unresolved critical assumption.
- Completion evidence records observed model and effort, metadata source/time, fallback chain, route transitions, and mismatch status.
- Traceability report is updated.

## Integration gate

Run the separate integration blueprint only after relevant chunks are complete. This is separate from unit/component gates.

- Exercise cross-module flow, real boundary contracts, persistence/external effects, and failure paths.
- Verify authorization, observability, rollback/retry behavior, and backward compatibility where applicable.
- Incrementally integrate compatible chunks and run regression checks after each integration step.
- Record result in traceability report. Any failure blocks delivery and returns work to the affected blueprint/chunk.
