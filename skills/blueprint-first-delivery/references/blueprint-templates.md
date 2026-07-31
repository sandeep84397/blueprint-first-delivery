# Blueprint templates

Write every blueprint in plain English. Create one blueprint per module or bounded change area, plus the separate integration blueprint below.

```md
## <module/change area>

### Purpose and scope
- Problem / user outcome:
- In scope:
- Out of scope:
- Acceptance criteria:

### Contract
- Inputs and validation:
- Outputs / API / events:
- State, schema, or migration:
- Error and rollback behavior:
- Security, authorization, privacy:

### Design
- Dependencies owned or consumed:
- Ordered prerequisites:
- Parallel work possible (only if frozen contracts and non-overlapping file/state ownership):
- File/state ownership per chunk:
- Implementation chunks and owners:

### Verification
- Unit/component evidence:
- Contract/e2e evidence:
- Integration evidence:
- Risks and assumptions:
```

# Integration blueprint template

```md
## Integration: <cross-module flow>

### Plain-English outcome
- User/business outcome:
- Modules and external systems involved:

### Frozen boundaries
- Contracts exercised:
- State transitions and file/state owners:
- Failure, retry, and rollback paths:

### Integration evidence
- End-to-end flow and expected result:
- Authorization, observability, compatibility checks:
- Acceptance criteria and traceability rows:
```

# Traceability report template

```md
| Acceptance criterion | Blueprint decision | Chunk | Evidence | Integration result | Status / residual risk |
| --- | --- | --- | --- | --- | --- |
| <criterion> | <decision> | <chunk> | <test/review> | <result> | <met/risk> |
```
