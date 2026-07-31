# Blueprint templates

Create one blueprint per module or bounded change area.

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
- Independent work possible:
- Implementation chunks and owners:

### Verification
- Unit/component evidence:
- Contract/e2e evidence:
- Integration evidence:
- Risks and assumptions:
```

# Traceability report template

```md
| Acceptance criterion | Blueprint decision | Chunk | Evidence | Integration result | Status / residual risk |
| --- | --- | --- | --- | --- | --- |
| <criterion> | <decision> | <chunk> | <test/review> | <result> | <met/risk> |
```
