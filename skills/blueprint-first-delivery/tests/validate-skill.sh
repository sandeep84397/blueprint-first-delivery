#!/usr/bin/env sh
set -eu

project_root=$(CDPATH='' cd -- "$(dirname "$0")/../../.." && pwd)
skill_root="$project_root/skills/blueprint-first-delivery"

python3 -B "$skill_root/scripts/validate_skill.py" "$skill_root"
python3 -B -m unittest discover -s "$skill_root/tests" -p 'test_*.py'
sh "$skill_root/tests/test-validator-negative-fixtures.sh"

# shellcheck disable=SC2016
grep -Fq '$HOME/.agents/skills' "$project_root/README.md" || {
  echo 'README.md:0: missing canonical user skill path' >&2
  exit 1
}
grep -Fq 'legacy ~/.codex/skills' "$project_root/README.md" || {
  echo 'README.md:0: missing legacy path compatibility note' >&2
  exit 1
}
