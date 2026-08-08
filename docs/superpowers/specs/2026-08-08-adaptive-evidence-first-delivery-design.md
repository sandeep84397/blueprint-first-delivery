# Adaptive Evidence-First Delivery Design

**Status:** Approved 2026-08-08  
**Scope:** `blueprint-first-delivery` for Codex and Claude Code  
**Decision:** `dec_20260808_122727_f720fa`

## Goal

Make the skill cheaper for trivial work and more trustworthy for protected-risk work. A work-route decision chooses `Direct`, `Blueprint Lite`, or `Full Blueprint`; it is separate from the existing model-tier decision (`Light`, `Standard`, `Deep`, `Maximum`). A readiness score remains process evidence, never a probability of correctness.

## Problem statement

The current package requires outcome-backward planning, review, readiness, and integration for all work. It correctly guards many risky features, but it does not make planning depth explicit. Its static package validator proves that the guidance exists, not that a project's critical claims have executable proof, evidence has not drifted, or an integration risk was discovered early.

The revised design must avoid both failure modes:

- no heavy blueprint for a small, local, objectively proven change;
- no numeric score, polished prose, memory record, or reviewer assertion substituting for proof of a critical claim.

## Non-goals

- Mathematical correctness or reliability guarantees.
- Automatic discovery of every future blocker.
- Replacing tests, device probes, contracts, or independent review with Agent Brain.
- A UI, graph viewer, HTML artifact, extension, or GitHub Pages site.
- Replacing the existing provider-neutral model-routing policy or runtime mappings.

## Design

### 1. Adaptive work router

Run one bounded, structured triage before planning. It records only observable task facts: requested behavior, modules/boundaries touched, contract/state changes, protected-risk triggers, available oracle, reversibility, dependencies, and handoff need. It must choose exactly one work route and cite the facts that decided it.

| Work route | Entry rule | Required artifact | Minimum completion proof |
| --- | --- | --- | --- |
| `Direct` | Every Direct predicate passes | Direct receipt in the task record or final evidence | Focused deterministic test/oracle and changed-scope review |
| `Blueprint Lite` | No Full hard trigger; one or more Direct predicates fail | Compact task card | Named invariant, deterministic oracle, review of changed scope |
| `Full Blueprint` | Any Full hard trigger | Existing outcome-backward plan plus Evidence-First additions | Independent gates, critical proofs, early integration, final traceability |

`Direct` is allowed only when all predicates pass:

1. One exact observable behavior is requested.
2. One existing module and one state owner are affected.
3. No public/internal shared contract, schema, persistence, migration, lifecycle, concurrency, security, privacy, authorization, network/external-service behavior, or irreversible action changes.
4. A focused deterministic oracle already exists or is added in the same bounded change.
5. The blast radius is local and rollback is straightforward.
6. No unfinished producer-consumer dependency or multi-agent handoff exists.

Any one of these Full hard triggers selects `Full Blueprint`:

- public or shared contract change;
- persistence, migration, data recovery/deletion, or data-integrity risk;
- concurrency, lifecycle, background execution, platform/device behavior, or WebView boundary;
- security, privacy, authorization, money, or irreversible blast radius;
- external system/SDK behavior that is material or unverified;
- two or more modules/state owners or a cross-module causal dependency;
- no deterministic oracle for a material acceptance criterion;
- unresolved critical ambiguity, costly rollback, or a multi-agent handoff requiring frozen contracts.

`Blueprint Lite` covers all remaining bounded work. It contains exactly: outcome, affected boundary, invariant, owner, in/out scope, failure/rollback expectation, deterministic oracle, changed-file/state ownership, and route rationale. It does not use readiness scoring or a Principal review unless an observed hard trigger promotes it to Full.

The router records `route`, `facts`, `hard_triggers`, `promotions`, `reason`, and `oracle`. A new hard trigger promotes only the affected work; it never silently reclassifies a completed proof.

### 2. Evidence-First Full Blueprint

Full Blueprint preserves the current order:

```text
outcome contract → architecture evidence → backward pass → forward pass
→ reconciliation → module freeze → chunks → incremental integration → traceability
```

Before the readiness rubric, it adds a proof matrix. Every critical requirement, contract, invariant, recovery claim, or security boundary has one non-compensable row:

| Field | Meaning |
| --- | --- |
| `requirement_id` | Stable acceptance-criterion identifier |
| `claim_id` | Contract or invariant identifier |
| `criticality` | `critical` or `non-critical` |
| `owner` | Single accountable module/agent |
| `status` | `FACT`, `ASSUMPTION`, `PROOF_REQUIRED`, `PROVEN`, `BLOCKED`, or `STALE` |
| `oracle_id` | Test, deterministic command, device probe, or external evidence identifier |
| `expected_result` | Observable pass condition |
| `evidence_ref` | Source-relative evidence and result reference |
| `baseline_ref` | Immutable baseline that the proof applies to |
| `integration_counterpart` | Consumer/producer or `none` |

At `ARCHITECTURE_APPROVED` and `PLAN_FROZEN`, every critical row must have a named owner, an executable oracle, an expected result, a baseline reference, and either a verified fact or a named future task that will run the oracle. `ASSUMPTION`, `BLOCKED`, and `STALE` are prohibited. `PROOF_REQUIRED` is permitted only with that fully specified execution path. At `TASK_PROVEN`, every critical row owned by that task is `PROVEN`. At `INTEGRATION_PROVEN` and `DELIVERY_READY`, every exercised critical row is `PROVEN`; no critical row may remain `ASSUMPTION`, `PROOF_REQUIRED`, `BLOCKED`, or `STALE`.

A feasibility spike is mandatory before plan freeze whenever the cheapest credible proof can resolve a protected-risk assumption. The spike is a small experiment; it is not production implementation.

Readiness remains `>=95/100` only after every hard gate passes. The rubric cannot compensate for a missing critical proof. Its result means evidence completeness against the published rubric, not confidence that implementation will work.

### 3. Measurable task and review boundaries

Each implementation chunk owns one independently testable claim. It names one responsible owner, one invariant or contract behavior, its input/output boundary, one deterministic oracle, exclusive file/state ownership, and an integration counterpart. A chunk may change several files only when they jointly implement that one claim; file count never proves scope.

Reviewer calibration is structural, not personality-based. The reviewer must be independent from the author, use the same proof matrix and rubric, identify every challenged row, and record `finding_id`, severity, evidence checked, disposition, and affected approval state. An unresolved finding blocks the affected gate.

### 4. Explicit approval state

The skill exposes one current state for each work item:

```text
TRIAGED → ARCHITECTURE_APPROVED → PLAN_FROZEN → TASK_PROVEN
→ INTEGRATION_PROVEN → DELIVERY_READY
```

`BLOCKED` and `STALE` are terminal for the current approval until repair and re-review. The current state must state why it changed, which evidence changed, its owner, and the next decision required. This separates architecture approval, task-plan approval, implementation proof, and integration proof for users.

### 5. Early vertical integration

For Full Blueprint work with a cross-module flow, write the separate integration blueprint during plan freeze. After the earliest compatible producer and consumer exist, run a thin vertical proof across their real contract and primary failure route. Do not defer all cross-module proof to the final integration gate. Later integration still exercises complete acceptance, recovery, authorization, compatibility, and regression evidence.

### 6. Immutable traceability and drift

Traceability becomes machine-checkable. Each row links:

```text
requirement_id → claim_id → task_id → oracle_id → evidence_ref → integration_result
```

Each approval records a baseline: Git commit/tree identifier, relevant contract version/digest, exclusive owned file/state list, and evidence digest. A changed baseline, changed contract, changed oracle, non-owned file impact, or changed evidence result marks only affected rows `STALE`; those rows must be repaired and independently re-approved before they can support delivery.

The validator will validate schema and cross-reference completeness for example artifacts. It will not claim that arbitrary external commands or Claude Code sessions ran locally.

### 7. Agent Brain continuity

Agent Brain is mandatory for Full Blueprint work and for Lite work that crosses a turn, agent, or handoff. It records source-linked decisions, baseline references, proof rows, approvals, and stale/invalidation events. `Direct` work has no mandatory memory entry unless a handoff occurs.

Agents retrieve the smallest relevant packet rather than project history. Every record points to a current source path, symbol/contract identifier, baseline reference, and evidence reference. Agent Brain supplies continuity and retrieval; it is never proof by itself.

### 8. Cost-aware model routing

Work route and model tier are distinct:

- Route triage, evidence retrieval, static cross-reference checks, and mechanical manifest updates use the active runtime's cheapest verified capable tier.
- Normal implementation, tests, and bounded debugging use Standard unless the existing routing policy establishes a higher floor.
- Architecture synthesis, adversarial review, protected-risk feasibility analysis, and unresolved cross-module causal decisions use Deep.
- Maximum remains exceptional under the existing policy.

The router produces structured facts, not a full design narrative. Direct creates no blueprint; Lite uses the compact card; Full loads detailed references only when needed. Record, where runtime metadata is available, task route, selected model tier, effort, planning/evidence/implementation/verification token or usage data, rework, reopened contracts, and late integration failures. Missing provider telemetry is labeled unavailable, never invented.

## Compatibility

Existing completed plans remain historical. In-progress Full work receives an adaptive route plus a proof-matrix risk audit before its next affected task. Legacy records that lack a baseline or proof row are `STALE` for new approval, not retroactively declared invalid delivery.

## Validation strategy

The package must gain deterministic pressure scenarios, mutation tests, an example artifact, and documentation covering at least:

1. A trivial local change selects Direct and still requires a focused oracle.
2. A bounded non-trivial change selects Lite without Full-only ceremony.
3. Every protected-risk trigger selects Full even if the request calls it small.
4. A missing critical oracle/proof blocks approval despite a high numeric readiness score.
5. A changed baseline or contract marks affected evidence stale.
6. A Full cross-module flow requires an early vertical proof and a later final integration gate.
7. Agent Brain memory without a source/evidence reference is rejected for Full/handoff work.
8. Codex and Claude Code use the same provider-neutral policy and their runtime mappings remain isolated.

## Acceptance criteria

- The shared skill chooses Direct, Lite, or Full deterministically and explains the route from recorded facts.
- Outcome-backward/forward planning remains mandatory for Full work and reconciliation still precedes module freeze.
- Critical claims have executable proof obligations that cannot be offset by a score.
- Approval lifecycle, reviewer calibration, early integration, immutable traceability, and drift invalidation are explicit and validated.
- Agent Brain continuity is source-linked and mandatory only where it saves more context than it costs.
- Codex and Claude Code documentation share policy while retaining provider-specific mappings.
- Repository tests, validator, documentation, and examples prove the skill package contains the policy and rejects its removal.
