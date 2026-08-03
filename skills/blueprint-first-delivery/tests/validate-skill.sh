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
grep -Fq '$HOME/.claude/skills' "$project_root/README.md" || {
  echo 'README.md:0: missing Claude Code user skill path' >&2
  exit 1
}
grep -Fq 'single source of truth' "$project_root/README.md" || {
  echo 'README.md:0: missing single-source statement' >&2
  exit 1
}
grep -Fq 'requested route is not proof of the observed route' "$project_root/README.md" || {
  echo 'README.md:0: missing honest route-evidence statement' >&2
  exit 1
}
grep -Fq 'Claude Code' "$project_root/README.md" || {
  echo 'README.md:0: missing Claude Code support statement' >&2
  exit 1
}
grep -Fq '## Inspect a routing manifest' "$project_root/README.md" || {
  echo 'README.md:0: missing manifest inspection guidance' >&2
  exit 1
}
grep -Fq '## Escalation and de-escalation' "$project_root/README.md" || {
  echo 'README.md:0: missing route-transition guidance' >&2
  exit 1
}
grep -Fq '## Override and fallback' "$project_root/README.md" || {
  echo 'README.md:0: missing override/fallback guidance' >&2
  exit 1
}
grep -Fq 'below-floor override remains blocked' "$project_root/README.md" || {
  echo 'README.md:0: missing override safety gate' >&2
  exit 1
}
