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
  scripts/validate_skill.py # Dependency-free package validator
  tests/validate-skill.sh  # Package validation
```

## Install

Clone this repository, then link the skill into Codex's canonical user skills folder:

```sh
git clone https://github.com/sandeep84397/blueprint-first-delivery.git
mkdir -p "$HOME/.agents/skills"
ln -s "$PWD/blueprint-first-delivery/skills/blueprint-first-delivery" "$HOME/.agents/skills/blueprint-first-delivery"
```

Codex follows symlinked skill folders. Older installations may discover the
legacy ~/.codex/skills location, but do not keep the same skill active in both
locations because Codex does not merge duplicate names. Restart Codex if the
new skill does not appear.

## Use

Trigger the skill by naming it, for example:

```text
Use $blueprint-first-delivery to plan this feature.
Use $blueprint-first-delivery to assess readiness before implementation.
```

Provide the product goal, constraints, known dependencies, and delivery
deadline. The skill produces a scoped blueprint and readiness score with the
evidence required to pass its gate.

## Validate

From the repository root, run:

```sh
sh skills/blueprint-first-delivery/tests/validate-skill.sh
```

The repository validator requires CPython 3.9+ and POSIX `sh`. The core
package-profile validator uses only the Python standard library and is not a
general YAML parser.
