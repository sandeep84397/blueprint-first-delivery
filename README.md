# Blueprint-First Delivery

> Make AI-assisted software delivery more reliable by turning large, ambiguous work into small, reviewed, evidence-backed units.

## What this project does

Blueprint-First Delivery is a reusable workflow skill for Codex and Claude Code. It requires the AI to design a change in plain English before coding, obtain independent architecture review, split delivery into the smallest practical verifiable chunks, route each chunk to the cheapest capable model, and validate integration against the original requirement.

It is designed for features, refactors, migrations, and other multi-part changes where one large implementation pass would carry too much ambiguity and rework risk.

This repository is the single source of truth for the shared workflow, routing policy, runtime mappings, templates, gates, and tests.

## The problem

Large, ambiguous tasks can overload an agent's working context. Important constraints and relationships become difficult to hold together, even when individual edits appear reasonable.

When a decision is missing, an agent can silently replace it with an assumption. This creates hallucination-like behavior: a plausible local answer that does not match the intended system.

Coding before a holistic design review discovers architecture mistakes late, when a correction may require broad refactoring rather than a small design change.

A large task may be only partly understood even when each local edit looks plausible. Passing a local test does not prove that the whole requirement was understood.

Individually passing components can still fail when their contracts, state ownership, or integration order disagree. Self-reported “95% confidence” is not objective evidence.

## How Blueprint-First Delivery solves it

The workflow enforces seven stages:

1. Plain-English module blueprint.
2. Independent Principal Engineer review.
3. Small single-responsibility chunks with explicit dependencies and ownership.
4. Evidence-based Light, Standard, Deep, or Maximum model route.
5. Per-chunk start and completion gates.
6. Separate incremental integration blueprint and gate.
7. Final requirement-to-evidence traceability.

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

`>=95/100` measures collected readiness evidence. It is not a mathematical probability and does not guarantee defect-free software. The score records evidence for clarity, contracts, dependencies, testability, edge cases, independent review, and integration readiness.

## What you get

- Module blueprint.
- Dependency graph.
- Chunk blueprints.
- Readiness scores and vetoes.
- Route manifest and history.
- Independent review record.
- Chunk evidence.
- Integration evidence.
- Final traceability report.

## Example: Offline profile editing

A broad offline profile-editing request first freezes source-of-truth, conflict, retry, and persistence decisions. The data flow and ownership are reviewed before code begins.

The work then splits into bounded contracts, local persistence, UI state, sync worker, and integration chunks. Work runs in parallel only after frozen contracts and non-overlapping ownership prove independence.

Integration proceeds incrementally, verifying offline edit → persistence → reconnect → sync → refreshed UI. SOLID boundaries help decomposition but do not alone prove correctness.

## Runtime model routing

| Tier | Work | Codex | Claude Code |
| --- | --- | --- | --- |
| Light | exact, bounded, objectively verifiable mechanical work | Luna / low | Haiku / low |
| Standard | normal implementation, debugging, tests, review | Terra / medium | Sonnet / medium |
| Deep | architecture, security, concurrency, ambiguity, cross-module diagnosis | Sol / high | Opus / high |
| Maximum | hardest indivisible critical reasoning problem | Sol / max | Opus / max |

The router selects the cheapest capable tier from evidence. A requested route is not proof of the observed route; execution evidence must record the runtime-observed model, effort, metadata source, and fallback chain.

## Inspect a routing manifest

For each chunk, inspect schema/policy version, tier and established floor, topology/dependency evidence, active mapping path/version/digest, escalation and de-escalation rules, independent reviewer, route history, override status, and observed execution. Deep/Maximum cannot start unless observed runtime evidence can prove the floor.

## Escalation and de-escalation

Escalate to max(next tier, established floor) when recorded evidence fires. De-escalate only when the current chunk has no hard trigger, governing decisions/contracts are frozen and reviewed, an objective oracle exists, and no critical finding remains open. Append every transition; never overwrite history.

## Override and fallback

A below-floor override remains blocked. If a model is unavailable, record the attempt, try a declared same-tier fallback, then a higher capable tier. Maximum has no upward fallback and must block, decompose, or receive a newly reviewed mapping. Never claim a requested or inherited route as observed without runtime metadata.

## Install

### Codex

Clone this repository, then link the skill into Codex's canonical user skills folder:

```sh
git clone https://github.com/sandeep84397/blueprint-first-delivery.git
mkdir -p "$HOME/.agents/skills"
ln -s "$PWD/blueprint-first-delivery/skills/blueprint-first-delivery" "$HOME/.agents/skills/blueprint-first-delivery"
```

### Claude Code

```sh
git clone https://github.com/sandeep84397/blueprint-first-delivery.git
mkdir -p "$HOME/.claude/skills"
ln -s "$PWD/blueprint-first-delivery/skills/blueprint-first-delivery" "$HOME/.claude/skills/blueprint-first-delivery"
```

Do not activate duplicate copies of the same skill name. Both runtime links should resolve to this repository package. Repository validation comes before any separately approved removal of duplicated global guidance.

Codex follows symlinked skill folders. Older installations may discover the legacy ~/.codex/skills location, but do not keep the same skill active in both locations because Codex does not merge duplicate names. Restart Codex if the new skill does not appear.

## Use

Trigger the skill by naming it, for example:

```text
Use $blueprint-first-delivery to plan this feature.
Use $blueprint-first-delivery to assess readiness before implementation.
```

Provide the product goal, constraints, known dependencies, and delivery deadline. The skill produces a scoped blueprint and readiness score with the evidence required to pass its gate.

## Repository layout

```text
skills/blueprint-first-delivery/
  SKILL.md                 # Skill instructions
  references/              # Templates, rubric, and checklists
  scripts/validate_skill.py # Dependency-free package validator
  tests/validate-skill.sh  # Package validation
```

## Validate

From the repository root, run:

```sh
sh skills/blueprint-first-delivery/tests/validate-skill.sh
```

The repository validator requires CPython 3.9+ and POSIX `sh`. The core package-profile validator uses only the Python standard library and is not a general YAML parser.

## Limitations

- No correctness guarantee.
- A stronger model cannot replace clear contracts or objective tests.
- Safe parallelism requires relational independence evidence.
- Local validation cannot prove an external Claude Code execution occurred.
- Global configuration cleanup remains a separate explicitly approved migration.
