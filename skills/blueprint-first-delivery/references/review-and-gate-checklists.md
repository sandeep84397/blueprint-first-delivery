# Review and gate checklists

## Principal-engineer-style adversarial blueprint review

- Reviewer is not the blueprint author.
- Architecture evidence is recorded: inspected locations, conventions, dependencies/contracts, state owners, test/build entrypoints, and unresolved questions or greenfield evidence.
- Do not score an existing-codebase blueprint without a complete architecture-evidence block. Boundary- or contract-affecting absence is an unresolved critical-risk veto.
- Challenge contracts, hidden dependencies, ownership, failure paths, security, and claimed evidence.
- All modules have scope, contracts, dependencies, verification, and risks.
- A separate integration blueprint covers every cross-module flow.
- Dependency classification is correct: independent, ordered, or integration-only. Parallel work has frozen contracts and non-overlapping file/state ownership.
- Readiness score is recorded. Below 95/100: return for repair.

## Chunk gate

Before starting a chunk:

- Prerequisite ordered chunks and shared contracts are complete or explicitly stable.
- Parallel chunks have frozen contracts and non-overlapping file/state ownership.
- Owner, acceptance criteria, and verification evidence are assigned.
- Boundary, error, security, compatibility, and rollback impacts are understood.

Before marking a chunk complete:

- Its focused tests and regression checks pass.
- A blueprint-to-code review confirms the implementation matches the approved scope, ownership, and acceptance criteria.
- Explicit contract verification confirms inputs, outputs, errors, compatibility, and boundary behavior.
- Its contract remains compatible with dependent chunks, with no unresolved critical assumption.
- Traceability report is updated.

## Integration gate

Run the separate integration blueprint only after relevant chunks are complete. This is separate from unit/component gates.

- Exercise cross-module flow, real boundary contracts, persistence/external effects, and failure paths.
- Verify authorization, observability, rollback/retry behavior, and backward compatibility where applicable.
- Incrementally integrate compatible chunks and run regression checks after each integration step.
- Record result in traceability report. Any failure blocks delivery and returns work to the affected blueprint/chunk.
