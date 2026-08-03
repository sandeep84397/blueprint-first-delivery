# Blueprint-First Delivery

> Make AI-assisted software delivery more reliable by turning large, ambiguous work into small, reviewed, evidence-backed units.

## What this project does

Blueprint-First Delivery is a reusable workflow skill for Codex and Claude Code. It defines an observable outcome and evidence, reasons backward to prerequisites, checks forward feasibility against architecture, reconciles both views, then freezes modules before coding. It obtains independent architecture review, splits delivery into the smallest practical verifiable chunks, routes each chunk to the cheapest capable model, and validates integration against the original requirement.

It is designed for features, refactors, migrations, and other multi-part changes where one large implementation pass would carry too much ambiguity and rework risk.

This repository is the single source of truth for the shared workflow, routing policy, runtime mappings, templates, gates, and tests.

## The problem

Large, ambiguous tasks can overload an agent's working context. Important constraints and relationships become difficult to hold together, even when individual edits appear reasonable.

When a decision is missing, an agent can silently replace it with an assumption. This creates hallucination-like behavior: a plausible local answer that does not match the intended system.

Coding before a holistic design review discovers architecture mistakes late, when a correction may require broad refactoring rather than a small design change.

A large task may be only partly understood even when each local edit looks plausible. Passing a local test does not prove that the whole requirement was understood.

Individually passing components can still fail when their contracts, state ownership, or integration order disagree. Self-reported “95% confidence” is not objective evidence.

## Outcome-backward planning

Outcome-backward planning starts with observable acceptance evidence, then works backward through the conditions required to produce it while checking that those conditions are feasible in the current architecture. It surfaces late constraints earlier; it does not predict every future issue. Dates are constraints, not outcomes. When ambiguity would change behavior, the workflow asks users to resolve it before modules are frozen; until then, modules stay provisional. No implementation may begin before module freeze. Model routing occurs only after module freeze.

## How Blueprint-First Delivery solves it

The workflow enforces ten stages:

1. Outcome contract.
2. Architecture evidence.
3. Backward prerequisite analysis.
4. Forward feasibility analysis.
5. Reconciliation loop.
6. Module-freeze gate.
7. Chunk decomposition.
8. Readiness scoring and model routing.
9. Implementation and incremental integration.
10. Outcome and requirement verification.

```text
Observable outcome and acceptance evidence
  → Current architecture evidence
  → Backward prerequisites
  → Forward feasibility
  → Reconciliation and module freeze
  → Small evidence-ready chunks
  → Cheapest capable model per chunk
  → Incremental integration
  → Outcome traceability
```

## Evidence, not confidence

`>=95/100` measures collected readiness evidence. It is not a mathematical probability and does not guarantee defect-free software. The score records evidence for clarity, contracts, dependencies, testability, edge cases, independent review, and integration readiness. `BLOCKED` means readiness is unscorable, not a lower numeric score. A failed module-freeze gate leaves readiness unscorable.

## What you get

- Module blueprint.
- Outcome-Backward Plan.
- Blocker register.
- Reconciliation history.
- Module-freeze decision.
- Residual-risk record.
- Dependency graph.
- Chunk blueprints.
- Readiness scores and vetoes.
- Route manifest and history.
- Independent review record.
- Chunk evidence.
- Integration evidence.
- Final traceability report.

## Example: Offline profile editing

A broad offline profile-editing request first resolves source-of-truth ambiguity, backward conditions, forward sync feasibility, and reconciliation before any module split. It then freezes source-of-truth, conflict, retry, and persistence decisions. The data flow and ownership are reviewed before code begins.

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

Provide the observable outcome, objective acceptance evidence, constraints, known dependencies, and delivery deadline. The deadline is a constraint; it is not the outcome.

## Repository layout

```text
skills/blueprint-first-delivery/
  SKILL.md                 # Skill instructions
  references/              # Templates, rubric, and checklists
  references/outcome-backward-planning.md # Outcome-first planning guidance
  scripts/validate_skill.py # Dependency-free package validator
  tests/validate-skill.sh  # Package validation
  tests/outcome-backward-pressure-scenarios.md # Planning pressure scenarios
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
- No interactive graph or viewer is included; that work belongs to the separate semantic-zoom documentation project.
