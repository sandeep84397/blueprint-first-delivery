# Narrative-First README Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rewrite the public root README so a first-time visitor understands the problem, the solution, the workflow, and the value before installation and routing reference details.

**Architecture:** This is one documentation-only deliverable. `README.md` remains the public entry point and preserves every existing installation, compatibility, routing-safety, repository-layout, and validation contract while changing the information hierarchy to narrative-first.

**Tech Stack:** GitHub-flavored Markdown, POSIX `sh`, CPython 3.9+ repository validator.

## Global Constraints

- English only.
- Modify `README.md` only during implementation.
- Add no generated images, icons, badges, or decorative assets.
- Do not change skill behavior, routing policy, tests, runtime mappings, global Codex/Claude configuration, or duplicated global guidance.
- Readiness `>=95/100` is process evidence, never a correctness probability.
- Preserve `$HOME/.agents/skills`, `legacy ~/.codex/skills`, and `$HOME/.claude/skills` installation guidance.
- Preserve the exact safety statements required by the existing POSIX wrapper.

---

### Task 1: Rewrite the public README

**Files:**
- Modify: `README.md`
- Test: `skills/blueprint-first-delivery/tests/validate-skill.sh`

**Interfaces:**
- Consumes: approved design `docs/superpowers/specs/2026-08-03-readme-presentation-design.md`, existing installation commands, routing policy terminology, and wrapper assertions.
- Produces: a narrative-first public README with unchanged operational contracts.

- [ ] **Step 1: Prove the narrative sections are absent**

Run:

```sh
python3 -c 'from pathlib import Path; text=Path("README.md").read_text(); required=("## What this project does","## The problem","## How Blueprint-First Delivery solves it","## What you get","## Example: Offline profile editing","## Limitations"); missing=[item for item in required if item not in text]; assert not missing, missing'
```

Expected: exit `1`; assertion lists all or most of the six new narrative headings.

- [ ] **Step 2: Rewrite README with the approved information hierarchy**

Use this exact section order and content contract:

```markdown
# Blueprint-First Delivery

> Make AI-assisted software delivery more reliable by turning large, ambiguous work into small, reviewed, evidence-backed units.

## What this project does

Blueprint-First Delivery is a reusable workflow skill for Codex and Claude Code. It requires the AI to design a change in plain English before coding, obtain independent architecture review, split delivery into the smallest practical verifiable chunks, route each chunk to the cheapest capable model, and validate integration against the original requirement.

It is designed for features, refactors, migrations, and other multi-part changes where one large implementation pass would carry too much ambiguity and rework risk.

## The problem

Explain these five failure modes in short paragraphs or a compact table:

- large ambiguous tasks overload the agent's working context;
- missing decisions are silently replaced by assumptions, creating hallucination-like behavior;
- coding before holistic design review reveals architecture mistakes late, when fixes require broad refactoring;
- a large task may be only partly understood even when each local edit looks plausible;
- individually passing components can still fail when their contracts, state ownership, or integration order disagree.

Close with: self-reported “95% confidence” is not objective evidence.

## How Blueprint-First Delivery solves it

Explain the seven enforced stages:

1. Plain-English module blueprint.
2. Independent Principal Engineer review.
3. Small single-responsibility chunks with explicit dependencies and ownership.
4. Evidence-based Light, Standard, Deep, or Maximum model route.
5. Per-chunk start and completion gates.
6. Separate incremental integration blueprint and gate.
7. Final requirement-to-evidence traceability.

Include this compact workflow:

```text
Requirement
  → Plain-English blueprint
  → Independent design review
  → Small evidence-ready chunks
  → Cheapest capable model per chunk
  → Chunk verification
  → Incremental integration
  → End-to-end traceability
```

## Evidence, not confidence

State that `>=95/100` measures collected readiness evidence. It is not a mathematical probability and does not guarantee defect-free software. Mention clarity, contracts, dependencies, testability, edge cases, independent review, and integration readiness.

## What you get

List the concrete outputs: module blueprint, dependency graph, chunk blueprints, readiness scores and vetoes, route manifest/history, independent review record, chunk evidence, integration evidence, and final traceability report.

## Example: Offline profile editing

Show how one broad request becomes:

1. freeze source-of-truth, conflict, retry, and persistence decisions;
2. review data flow and ownership before code;
3. split contracts, local persistence, UI state, sync worker, and integration into bounded chunks;
4. run work in parallel only after frozen contracts and non-overlapping ownership prove independence;
5. integrate incrementally and verify offline edit → persistence → reconnect → sync → refreshed UI.

State that SOLID boundaries help decomposition but do not alone prove correctness.

## Runtime model routing

Preserve the existing Light/Standard/Deep/Maximum table and the exact sentence:

“The router selects the cheapest capable tier from evidence. A requested route is not proof of the observed route; execution evidence must record the runtime-observed model, effort, metadata source, and fallback chain.”

## Inspect a routing manifest

Preserve the current manifest-inspection guidance.

## Escalation and de-escalation

Preserve the current transition guidance.

## Override and fallback

Preserve the exact phrase “A below-floor override remains blocked.” and the current fallback safety rules.

## Install

Keep separate `### Codex` and `### Claude Code` subsections with the current clone, directory, and symlink commands. Preserve duplicate-skill and restart warnings.

## Use

Preserve both existing trigger examples and input guidance.

## Repository layout

Preserve the current tree and comments.

## Validate

Preserve the current validation command, CPython 3.9+, POSIX `sh`, standard-library, and non-general-YAML-parser statements.

## Limitations

State:

- no correctness guarantee;
- a stronger model cannot replace clear contracts or objective tests;
- safe parallelism requires relational independence evidence;
- local validation cannot prove an external Claude Code execution occurred;
- global configuration cleanup remains a separate explicitly approved migration.
```

- [ ] **Step 3: Verify all narrative sections are present**

Run the Step 1 command again.

Expected: exit `0`; no output.

- [ ] **Step 4: Run repository validation**

Run:

```sh
sh skills/blueprint-first-delivery/tests/validate-skill.sh
```

Expected: unittest ends with `OK`; README wrapper assertions pass.

- [ ] **Step 5: Verify scope and formatting**

Run:

```sh
git diff --check
git diff --name-only
```

Expected:

- `git diff --check` exits `0` with no output.
- `git diff --name-only` emits only `README.md`.

- [ ] **Step 6: Commit**

```sh
git add README.md
git commit -m "docs: explain Blueprint-First Delivery"
```
