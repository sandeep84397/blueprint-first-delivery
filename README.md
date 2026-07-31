# blueprint-first-delivery

Blueprint-first, confidence-gated development skill for Codex. It turns a
request into an evidence-backed delivery blueprint, then requires a readiness
gate before implementation proceeds. The score measures readiness evidence,
not probability.

## Repository layout

```text
skills/blueprint-first-delivery/
  SKILL.md                 # Skill instructions
  references/              # Templates, rubric, and checklists
  tests/validate-skill.sh  # Package validation
```

## Install

Clone this repository, then copy the skill into Codex's local skills folder:

```sh
git clone <repository-url>
mkdir -p ~/.codex/skills
cp -R blueprint-first-delivery/skills/blueprint-first-delivery ~/.codex/skills/
```

Restart Codex or begin a new task after installation.

## Use

Trigger the skill by naming it, for example:

```text
Use blueprint-first-delivery to plan this feature.
Create a blueprint-first-delivery readiness assessment before implementation.
```

Provide the product goal, constraints, known dependencies, and delivery
deadline. The skill produces a scoped blueprint and readiness score with the
evidence required to pass its gate.

## Validate

From the repository root, run:

```sh
sh skills/blueprint-first-delivery/tests/validate-skill.sh
```
