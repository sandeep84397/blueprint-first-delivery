# Cross-Runtime Model Routing — Design

**Status:** User-approved architecture; principal-engineer design review passed on 2026-08-03  
**Target runtimes:** Codex and Claude Code  
**Source of truth:** This repository

## Goal

Extend Blueprint-First Delivery so the AI assigns each approved implementation chunk to the cheapest model tier likely to complete it correctly. Treat the router like a principal engineer assigning work to peers: use evidence about task shape, risk, ambiguity, blast radius, and verifiability; do not rely on self-reported confidence.

The assignment must be visible, reviewable, portable between Codex and Claude Code, and revisable when new evidence appears.

## Scope and migration boundary

This change modifies only the `blueprint-first-delivery` repository during its implementation and validation phase.

- Do not edit global `CLAUDE.md`, `AGENTS.md`, Codex configuration, Claude configuration, or custom-agent files in this phase.
- Do not remove duplicated global guidance until the repository implementation has passed its validation gates and the user approves a separate migration pass.
- Support Codex and Claude Code. Claude.ai and direct Anthropic API workflows are out of scope.
- Preserve the existing blueprint, readiness, independent-review, chunk, integration, and traceability gates.
- The existing Codex symlink may observe repository changes automatically; this phase creates no additional installation or configuration mutations.

## Current architecture evidence

This design extends the following inspected repository contracts:

| Location | Current responsibility and constraint |
| --- | --- |
| `skills/blueprint-first-delivery/SKILL.md` | Provider-neutral seven-step delivery workflow. Requires architecture evidence, author/reviewer separation, >=95/100 readiness, per-chunk gates, separate integration, and final traceability. A unit test keeps this file below 500 words. |
| `skills/blueprint-first-delivery/agents/openai.yaml` | Codex-only discovery metadata. The current validator requires exactly four lines and a prompt containing `$blueprint-first-delivery`. It is an adapter, not shared workflow logic. |
| `skills/blueprint-first-delivery/references/` | Owns reusable blueprints, the exact 100-point rubric, and review/gate checklists. Routing belongs here as one shared policy plus isolated runtime mappings. |
| `skills/blueprint-first-delivery/scripts/validate_skill.py` | Dependency-free Python 3.9+ fixed-profile validator. `REQUIRED_FILES`, `ALLOWED_TOP_LEVEL`, and workflow string contracts must be extended intentionally. It currently hard-requires `agents/openai.yaml`. |
| `skills/blueprint-first-delivery/tests/test_validate_skill.py` | Copies the skill to a temporary directory and exercises positive and mutation-based negative validation. It owns package-contract and exact-rubric assertions. |
| `skills/blueprint-first-delivery/tests/validate-skill.sh` | Deterministic entrypoint: package validator, Python unit discovery, negative-fixture script, and README installation assertions. |
| `README.md` | Codex-only layout, symlink installation, usage, and validation instructions. It must become the Codex/Claude Code entrypoint without duplicating the core skill. |

Current state ownership:

- `SKILL.md` owns workflow sequencing and hard gates.
- Shared references own evidence schemas and decision rules.
- Runtime-mapping references own provider names, effort values, request mechanisms, and fallbacks.
- The validator owns package shape and static contract enforcement.
- Runtime agents own execution. This repository records requested and observed routes but does not control provider infrastructure.

Baseline verification executed from the repository root on 2026-08-03:

```sh
sh skills/blueprint-first-delivery/tests/validate-skill.sh
```

Oracle: exit status `0`; Python output reported `Ran 53 tests` and `OK`.

Resolved architecture assumptions:

- One shared `SKILL.md` serves both runtimes; no duplicated Claude-specific skill logic.
- Dynamic model switching is not assumed. Automatic execution uses a model-pinned subagent only when the active runtime exposes and verifies that mechanism.
- Claude Code supports model and effort selection on subagents. Codex supports model-pinned custom agents. Exact mechanisms stay inside their runtime mappings.
- When a runtime cannot pin or prove a model, the router remains recommendation-only and applies the floor rules below.
- Provider aliases and availability can drift, so every route records a mapping version and content digest.

## Design principles

1. **Cheapest capable route, not cheapest route.** A weak assignment that causes retries can cost more than a suitable first assignment.
2. **Evidence, not confidence language.** A routing decision records objective triggers. It is not a probability-of-correctness claim.
3. **Provider-neutral policy.** Shared rules use capability tiers. Provider-specific model names live only in runtime mappings.
4. **Tier and topology are separate.** Model capability answers who should do a chunk. Execution topology answers whether chunks may run concurrently.
5. **Risk floors override apparent simplicity.** A short authentication, security, concurrency, migration, or data-integrity change may require the Deep tier.
6. **Strong models do not replace gates.** Every route remains subject to blueprint approval, focused verification, integration, and final traceability.
7. **No false execution claims.** A recommendation is not proof that a runtime actually used the requested model.
8. **Re-route on evidence.** Escalate or de-escalate at explicit checkpoints instead of keeping an expensive model for the entire feature.

## Considered approaches

### Free-form AI recommendation

Let the AI select any model using unconstrained judgment.

Rejected because decisions would be inconsistent, hard to test, and vulnerable to both under-routing and expensive over-routing.

### Fixed phase mapping

Always assign design to a deep-reasoning model, implementation to a standard model, and mechanical work to a light model.

Rejected because phase labels do not represent risk. Some implementation work is architecture-heavy, while some design-document formatting is mechanical.

### Evidence-based capability router

Classify each chunk with provider-neutral predicates, map its tier to the active runtime, review the assignment with the blueprint, and change the route only when recorded evidence triggers a transition.

Selected because it is portable, auditable, testable, and cost-aware.

## Architecture

```text
Approved module blueprint
        ↓
Small implementation chunks
        ↓
Evidence-based route classification
        ├── Capability tier
        ├── Reasoning effort
        └── Execution topology
        ↓
Principal-engineer routing review
        ↓
Active runtime resolution
        ↓
Model-pinned subagent when available
        ↓
Implementation and focused verification
        ↓
Evidence-triggered escalation/de-escalation
        ↓
Separate integration gate and final traceability
```

The shared policy will live in a routing reference. Codex and Claude Code will each have a small runtime mapping. `SKILL.md` will invoke the shared policy, detect the active runtime, and load exactly one mapping. A chunk records its provider-neutral decision plus only the active runtime resolution; it does not copy the inactive provider's mapping.

Planned package shape:

```text
skills/blueprint-first-delivery/
  SKILL.md
  agents/
    openai.yaml
  references/
    model-routing.md
    runtime-mappings/
      codex.md
      claude-code.md
    blueprint-templates.md
    readiness-rubric.md
    review-and-gate-checklists.md
  tests/
    model-routing-pressure-scenarios.md
    test_validate_skill.py
  scripts/
    validate_skill.py
```

The shared routing policy must not contain literal provider model IDs. Runtime mappings may contain provider aliases, exact request mechanisms, supported effort values, availability checks, same-tier fallbacks, and a declared mapping version.

## Capability tiers

| Tier | Eligible work | Codex mapping | Claude Code mapping |
| --- | --- | --- | --- |
| Light | Exact search, extraction, classification, log/test summaries, and mechanical transformations with an objective oracle | Luna, low | Haiku, low |
| Standard | Normal implementation, debugging, tests, routine review, and bounded refactoring with clear requirements | Terra, medium | Sonnet, medium |
| Deep | Architecture, security, privacy, concurrency, data integrity, unresolved ambiguity, cross-cutting behavior, or repeated failed diagnosis | Sol, high by default; xhigh only with evidence | Opus, high by default; xhigh only with evidence |
| Maximum | The hardest unresolved single reasoning problem after Deep is insufficient, or an exceptional critical-risk decision | Sol, max | Opus, max |

Runtime mappings should prefer stable provider aliases over dated identifiers where supported. Exact actionable identifiers stay in the provider mapping, not the shared policy.

## Deterministic routing rules

Evaluate rules in this normative order:

1. Collect risk evidence and establish a hard minimum floor. Any Deep trigger sets the floor to Deep.
2. Evaluate exceptional Maximum eligibility. Maximum may raise the route but never lower the established floor.
3. When no Deep/Maximum floor applies, evaluate every Light predicate.
4. Use Standard when Light is ineligible and no higher floor applies.

When a transition occurs, the effective tier is `max(next tier, established risk floor)`.

### Light eligibility

A chunk may use Light only when all conditions are true:

- responsibility and expected output are exact;
- contracts and inputs are frozen;
- blast radius is local and reversible;
- no security, privacy, authorization, concurrency, persistence, migration, or data-integrity concern exists;
- an objective oracle can verify the result;
- work is search, extraction, classification, summarization, or mechanical transformation rather than open-ended design.

Failure of any predicate returns the chunk to Standard or higher.

### Standard default

Use Standard for normal bounded implementation, debugging, tests, routine review, and refactoring when Light is ineligible and no Deep/Maximum trigger exists.

### Deep triggers

Any one of these triggers establishes a Deep floor:

- an architecture or public-contract boundary is being created or changed;
- security, privacy, authorization, concurrency, persistence, migration, or data integrity is involved;
- a wrong decision has a high or irreversible blast radius;
- a critical requirement or ownership boundary remains ambiguous;
- correct behavior requires causal reasoning across multiple modules or runtimes;
- a Standard attempt exposes a wrong design assumption;
- two evidence-backed Standard attempts fail to resolve the same root problem.

Risk triggers win even when the diff or document is small.

For repeated-failure escalation, a root-problem fingerprint contains the acceptance criterion, deterministic command/oracle, stable failure signature, and suspected causal boundary. An attempt records one distinct hypothesis and the evidence produced by testing it. Count two failures only when two distinct, evidence-backed attempts retain the same fingerprint. Reset the count when the contract, oracle, failure signature, or causal boundary materially changes.

Within Deep, `xhigh` effort requires either two independent high-risk triggers or an unresolved high-effort attempt with a stable root-problem fingerprint. The routing review must record why high effort is insufficient. `xhigh` is not automatically Maximum.

### Maximum eligibility

Maximum is exceptional. It requires one of these:

- an xhigh Deep attempt produced concrete evidence that the central reasoning problem remains unresolved;
- the task is the hardest single critical-risk decision in the feature and cannot be decomposed further without losing the problem;
- a principal-engineer review records why high and xhigh effort are insufficient.

Maximum is not used for routine implementation, retries without diagnosis, or multiple independent workstreams.

## Execution topology

Topology defaults to `ordered`.

Use `parallel` only when two or more chunks have:

- approved, frozen, versioned contracts;
- no dependency on another member's unfinished output;
- non-overlapping file and state ownership;
- independently executable verification;
- a named integration owner and integration order.

The number of files does not prove independence. Each parallel child receives its own capability tier.

Parallelism is represented by a relational `parallel_group`, not only by a per-chunk boolean. Every member names its dependencies, versioned contract references, exclusive file/state ownership, integration owner, and integration order.

Codex Ultra, when available, is an orchestrator-level choice reserved for meaningful independent workstreams. It is neither a capability tier nor per-chunk reasoning effort and must not be used for one difficult task. Claude Code parallel execution uses eligible subagents under the same independence rules.

## Routing manifest

Every implementation chunk adds versioned evidence to its blueprint. The example shows one active Codex resolution; a Claude Code run records only `runtime: claude_code` and its active mapping.

```yaml
routing:
  schema_version: 1
  policy_version: 1
  decision_id: route-profile-repository-001
  chunk_id: profile-repository
  author: planner-agent-id
  decided_at: 2026-08-03T10:30:00Z
  tier: standard
  topology: ordered
  established_floor: standard
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
    runtime: codex
    mapping_file: references/runtime-mappings/codex.md
    mapping_version: 1
    mapping_sha256: <sha256-of-exact-mapping-file>
    requested_model: gpt-5.6-terra
    requested_effort: medium
    request_mechanism: model-pinned subagent
  escalation_triggers:
    - public contract becomes ambiguous
    - focused verification exposes a wrong design assumption
  deescalation_requirements:
    - current chunk has no active hard-floor trigger
    - governing decision and contracts are frozen and reviewed
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
      trigger: initial classification
      evidence_reference: docs/blueprints/profile.md#routing-evidence
      changed_at: 2026-08-03T10:30:00Z
  execution_evidence:
    status: unverified
    runtime: codex
    runtime_version: null
    observed_model: null
    observed_effort: null
    alias_resolution: null
    metadata_source: null
    observed_at: null
    fallback_chain: []
```

`execution_evidence.status` becomes `verified` only when runtime metadata proves the observed model and effort and records its source and timestamp. Otherwise reports must use `recommended`, `requested`, `inherited`, `unavailable`, `mismatch`, or `unverified`. A status word alone is never sufficient proof.

## Principal-engineer routing review

Routing review is part of the existing adversarial blueprint review. Review all chunk routes together instead of starting one expensive review session per chunk.

The reviewer must challenge:

- under-routing of high-risk or ambiguous work;
- over-routing of bounded, objectively verifiable work;
- false parallelism and incomplete relational evidence;
- missing escalation and de-escalation points;
- unsupported claims about the model actually executed;
- provider-specific model names leaking into the shared policy;
- author/reviewer identity collisions;
- unresolved findings or missing dispositions.

The blueprint cannot pass while a critical route dispute remains unresolved. A user may request an override, but the manifest must record the requested change, rationale, reviewer concern, and acknowledged risk. An override below the established risk floor remains gate-blocked and cannot be called approved or ready. The user may direct work outside this workflow, but the skill must continue reporting the readiness veto and residual risk.

## Escalation and de-escalation

Escalate when a recorded trigger fires. Reclassify the task instead of blindly retrying with a larger model. The new route is `max(next tier, established risk floor)`, so a newly discovered security boundary can move Light directly to Deep.

Examples:

- Standard implementation reveals an unresolved ownership boundary → Deep architecture analysis.
- Deep analysis freezes the contract → reassess bounded implementation for Standard.
- Standard implementation is complete and only exact test/log summarization remains → reassess for Light.
- xhigh Deep analysis remains unable to resolve one indivisible critical problem → Maximum after review.

A high-tier decision does not make every downstream chunk high-tier. De-escalation is allowed only when:

- the current chunk has no active hard-floor trigger;
- its governing decision and contracts are frozen and independently reviewed;
- an objective oracle exists;
- no critical finding remains open.

Every transition appends route-history evidence; history is never overwritten.

## Runtime execution contract

Automatic assignment means the orchestrator attempts to dispatch the chunk through the active mapping's documented model-pinned subagent mechanism. It does not mutate global runtime settings.

Each runtime mapping must define:

- exact tier-to-model and tier-to-effort resolution;
- how the model/effort request is passed to a subagent;
- how availability and supported effort are checked;
- how observed model/effort metadata can be obtained;
- declared same-tier fallbacks in preference order;
- behavior when pinning or verification is unavailable;
- mapping version and the command used to compute its SHA-256 digest.

The planner creates the provider-neutral decision. The principal reviewer reviews all routes in one batch. The orchestrator resolves only the active mapping immediately before dispatch. This avoids inactive-provider duplication and amortizes expensive review across the module blueprint.

## Runtime failure and fallback behavior

- If the selected model is unavailable, try declared same-tier fallbacks first, then the next capable tier upward. Record every attempted resolution in `fallback_chain`.
- Never silently downshift below a risk-established floor.
- A Deep or Maximum floor blocks implementation when the runtime cannot pin and verify a model satisfying that floor.
- Light or Standard may proceed on an inherited model only when no higher floor exists. Record the route as inherited/unverified and do not claim cost optimization was enforced.
- Maximum has no upward fallback. If no declared Maximum-capable model is available, block, decompose the problem further, or request a new reviewed mapping.
- If model metadata cannot be inspected, do not claim a specific model ran.
- If observed model or effort is below the requested floor, mark `mismatch` and block the chunk gate.
- If classification evidence conflicts, choose the higher tier and request principal review.
- If the active runtime is neither Codex nor Claude Code, stop at a provider-neutral recommendation; do not invent a mapping.

## Backward compatibility and single-source governance

Existing completed blueprints without `routing.schema_version` remain historical evidence and are not rewritten. Any legacy chunk that resumes implementation must receive a routing manifest and independent review before its next start gate. Final traceability labels untouched historical chunks `legacy-unrouted` instead of inventing route evidence.

One shared `SKILL.md` remains the workflow source. Runtime mappings are adapters, not copied workflows. Each adapter declares its version; route manifests bind to an exact adapter digest. Validator tests reject provider model identifiers outside runtime-mapping boundaries.

This phase does not mutate global files. Implementation evidence must record before/after SHA-256 values, or literal `absent`, for the known global Claude and Codex guidance/configuration files in scope and show they are unchanged. A later user-approved migration pass may link runtime installations to this repository, compare resolved symlink targets and package digests, and remove duplicated guidance.

## Validation strategy

Extend repository validation and pressure scenarios. Tests must cover:

1. mechanical extraction routes to Light only when all Light predicates pass;
2. bounded normal implementation routes to Standard;
3. a small security or concurrency change routes to Deep despite low line count;
4. a Light-shaped task with one Deep trigger routes directly to Deep;
5. conflicting triggers follow the normative precedence and highest floor;
6. Maximum and xhigh require their distinct evidence and review;
7. a Deep-to-Standard de-escalation remains blocked while security or concurrency risk persists;
8. repeated-failure counting requires a stable root fingerprint and resets after material change;
9. two dependent chunks remain ordered even when they touch different files;
10. independent chunks with frozen contracts may run in parallel;
11. a hidden dependency, overlapping state, stale contract, or missing integration owner blocks a parallel group;
12. downstream implementation de-escalates only after all structured requirements pass;
13. an unavailable model tries same-tier then higher-tier fallback without unsafe downshift;
14. unavailable Maximum blocks or decomposes because no upward tier exists;
15. Deep/Maximum pinning or execution evidence that is unverified blocks the chunk;
16. `verified` without runtime metadata fails validation;
17. an observed route below the requested floor becomes `mismatch` and blocks;
18. a below-floor override remains blocked and visible;
19. author/reviewer identity collision or unresolved review finding blocks readiness;
20. an unknown runtime remains recommendation-only;
21. the shared policy remains free of literal provider model IDs;
22. both runtime mapping documents exist, are complete, declare supported effort/fallback rules, and have versions;
23. mapping digest and alias/version drift are visible in execution evidence;
24. existing blueprints follow the legacy/resume compatibility rule;
25. final traceability contains initial route, every transition, observed execution evidence, override, and residual risk;
26. implementation evidence proves the defined global files were not mutated.

Existing package and pressure tests must continue to pass.

Deterministic repository command:

```sh
sh skills/blueprint-first-delivery/tests/validate-skill.sh
```

Oracle: exit status `0`; package validator emits no error; Python discovery reports all tests passed and `OK`; negative-fixture script exits `0`. Also run `git diff --check` with exit status `0`.

## Documentation design

The README will explain:

- one repository supports Codex and Claude Code;
- capability tiers and their current runtime mappings;
- repository-first installation for each runtime;
- how routing saves tokens without promising correctness;
- how to inspect a chunk's routing manifest;
- how escalation, de-escalation, override, and fallback work;
- that repository validation precedes removal of duplicated global guidance.

## Non-goals

- No statistical claim that a model or chunk is 95% correct.
- No automatic model benchmarking or price calculation.
- No provider selection between Codex and Claude Code.
- No support for Claude.ai or direct provider APIs.
- No global configuration cleanup in this implementation phase.
- No assumption that a stronger model can compensate for missing tests, unclear contracts, or skipped integration.
- No use of parallel agents solely because more than one file is involved.

## Acceptance criteria

- The AI assigns every implementation chunk a provider-neutral tier, effort, and topology using recorded evidence.
- Active-runtime resolution is singular, versioned, and digest-bound; inactive-provider mappings are not copied into chunk manifests.
- Codex and Claude Code mappings produce an actionable requested route for every tier.
- Principal review catches both under-routing and over-routing.
- Light, xhigh, and Maximum are guarded by explicit eligibility rules.
- Parallel groups contain relational dependency, ownership, contract, and integration evidence.
- Escalation and de-escalation prevent both repeated weak-model failures and expensive-model inheritance.
- Deep/Maximum execution cannot pass without proof that the established floor was met.
- Below-floor overrides remain gate-blocked.
- Runtime uncertainty is reported honestly.
- Legacy blueprints have an explicit resume rule.
- Routing evidence appears in chunk blueprints and final traceability.
- Validator and pressure tests cover the routing rules and both runtime mappings.
- README presents this repository as the single source of truth for Codex and Claude Code.
- No global Claude or Codex guidance is edited before a separately approved migration pass.
