# Review and gate checklists

## Independent blueprint review

- Reviewer is not the blueprint author.
- All modules have scope, contracts, dependencies, verification, and risks.
- Dependency classification is correct: independent, ordered, or integration-only.
- Readiness score is recorded. Below 95/100: return for repair.

## Chunk gate

Before starting a chunk:

- Prerequisite ordered chunks and shared contracts are complete or explicitly stable.
- Owner, acceptance criteria, and verification evidence are assigned.
- Boundary, error, security, compatibility, and rollback impacts are understood.

Before marking a chunk complete:

- Its acceptance criteria and component evidence pass.
- Its contract remains compatible with dependent chunks.
- Traceability report is updated.

## Integration gate

Run only after relevant chunks are complete. This is separate from unit/component gates.

- Exercise cross-module flow, real boundary contracts, persistence/external effects, and failure paths.
- Verify authorization, observability, rollback/retry behavior, and backward compatibility where applicable.
- Record result in traceability report. Any failure blocks delivery and returns work to the affected blueprint/chunk.
