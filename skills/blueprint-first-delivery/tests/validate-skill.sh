#!/usr/bin/env sh
set -eu
root=skills/blueprint-first-delivery
for file in SKILL.md agents/openai.yaml references/blueprint-templates.md references/readiness-rubric.md references/review-and-gate-checklists.md; do
  test -f "$root/$file" || { echo "missing: $root/$file" >&2; exit 1; }
done
grep -q '^name: blueprint-first-delivery$' "$root/SKILL.md"
grep -q '95/100' "$root/SKILL.md"
grep -q 'integration' "$root/SKILL.md"
test -f README.md || { echo 'missing: README.md' >&2; exit 1; }
grep -q 'blueprint-first-delivery' README.md
grep -q 'skills/blueprint-first-delivery' README.md
