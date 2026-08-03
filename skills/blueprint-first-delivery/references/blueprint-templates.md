# Blueprint templates

Write every blueprint in plain English. Create one blueprint per module or bounded change area, plus the separate integration blueprint below.

```md
## <module/change area>

### Current architecture evidence
- Existing codebase evidence, or literal `greenfield` status and evidence:
- Inspected locations / symbols:
- Relevant conventions and boundaries:
- Observed dependencies, contracts, and state owners:
- Current test / build entrypoints:
- Unresolved questions or assumptions:

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

### Model routing
routing:
  schema_version: 1
  policy_version: 1
  decision_id: route-profile-repository-001
  chunk_id: profile-repository
  author: planner-agent-id
  decided_at: 2026-08-03T10:30:00Z
  tier: standard
  established_floor: standard
  topology: ordered
  evidence:
    task_shape: bounded implementation
    risk: low
    ambiguity: resolved
    blast_radius: local
    verification_oracle: focused automated tests
  dependency_evidence:
    depends_on: []
    parallel_group: null
    frozen_contracts:
      - id: profile-repository-v1
        version: 1
        reference: docs/blueprints/profile.md#profile-repository-v1
    file_ownership:
      - src/profile/repository/**
    state_ownership:
      - profile persistence writes
    integration_owner: integration-agent-id
    integration_order: 1
  active_runtime_resolution:
    runtime: active-runtime
    mapping_file: references/runtime-mappings/active-runtime.md
    mapping_version: 1
    mapping_sha256: recorded-before-dispatch
    requested_model: recorded-from-active-mapping
    requested_effort: recorded-from-active-mapping
    request_mechanism: model-pinned-subagent
  escalation_triggers:
    - public contract becomes ambiguous
  deescalation_requirements:
    - no current hard-floor trigger
    - governing decisions and contracts are frozen and reviewed
    - objective verification oracle exists
    - no critical review finding remains open
  override:
    requested: null
    rationale: null
    below_floor: false
    gate_status: not_applicable
  reviewer:
    identity: principal-reviewer-id
    independent_from_author: true
    status: pending
    rationale: null
    findings: []
    dispositions: []
    reviewed_at: null
  route_history:
    - from: null
      to: standard
      trigger: initial-classification
      evidence_reference: docs/blueprints/profile.md#routing-evidence
      changed_at: 2026-08-03T10:30:00Z
  execution_evidence:
    status: unverified
    runtime: active-runtime
    runtime_version: null
    observed_model: null
    observed_effort: null
    alias_resolution: null
    metadata_source: null
    observed_at: null
    fallback_chain: []

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
| Acceptance criterion | Blueprint decision | Chunk | Route decision/history | Observed execution | Evidence | Integration result | Status / residual risk |
| --- | --- | --- | --- | --- | --- | --- | --- |
| <criterion> | <decision> | <chunk> | <route/transitions> | <model/effort/source/time/fallback> | <test/review> | <result> | <met/risk> |
```
