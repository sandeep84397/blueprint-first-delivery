# blueprint-first-delivery

Blueprint-first, evidence-gated delivery for Codex and Claude Code. This repository is the single source of truth for the shared workflow, routing policy, runtime mappings, templates, gates, and tests.

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

## Repository layout

```text
skills/blueprint-first-delivery/
  SKILL.md                 # Skill instructions
  references/              # Templates, rubric, and checklists
  scripts/validate_skill.py # Dependency-free package validator
  tests/validate-skill.sh  # Package validation
```

## Install for Codex

Clone this repository, then link the skill into Codex's canonical user skills folder:

```sh
git clone https://github.com/sandeep84397/blueprint-first-delivery.git
mkdir -p "$HOME/.agents/skills"
ln -s "$PWD/blueprint-first-delivery/skills/blueprint-first-delivery" "$HOME/.agents/skills/blueprint-first-delivery"
```

## Install for Claude Code

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

## Validate

From the repository root, run:

```sh
sh skills/blueprint-first-delivery/tests/validate-skill.sh
```

The repository validator requires CPython 3.9+ and POSIX `sh`. The core package-profile validator uses only the Python standard library and is not a general YAML parser.
