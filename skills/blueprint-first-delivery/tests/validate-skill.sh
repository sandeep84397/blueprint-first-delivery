#!/usr/bin/env sh
set -eu
root=skills/blueprint-first-delivery

require() {
  pattern=$1
  file=$2
  label=$3
  if ! grep -Fq -- "$pattern" "$file"; then
    echo "missing requirement: $label ($file)" >&2
    exit 1
  fi
}

for file in SKILL.md agents/openai.yaml references/blueprint-templates.md references/readiness-rubric.md references/review-and-gate-checklists.md tests/pressure-scenarios.md tests/baseline-no-skill.md tests/forward-test-with-skill.md; do
  test -f "$root/$file" || { echo "missing: $root/$file" >&2; exit 1; }
done

# Dependency-free YAML/frontmatter shape checks. These assert the small,
# stable subset this package owns; a full YAML parser is intentionally not
# required just to validate skill metadata.
test "$(sed -n '1p' "$root/SKILL.md")" = '---' || { echo 'invalid SKILL.md frontmatter start' >&2; exit 1; }
test "$(sed -n '2p' "$root/SKILL.md")" = 'name: blueprint-first-delivery' || { echo 'invalid SKILL.md name in frontmatter' >&2; exit 1; }
description_line=$(sed -n '3p' "$root/SKILL.md")
printf '%s\n' "$description_line" | grep -Eq '^description: Use when .+$' || { echo 'invalid SKILL.md description in frontmatter' >&2; exit 1; }
test "$(sed -n '4p' "$root/SKILL.md")" = '---' || { echo 'invalid SKILL.md frontmatter end' >&2; exit 1; }
if sed -n '5,$p' "$root/SKILL.md" | grep -Eq '^(name|description):'; then
  echo 'invalid SKILL.md metadata outside frontmatter' >&2
  exit 1
fi
grep -Eq '^interface:$' "$root/agents/openai.yaml" || { echo 'invalid openai.yaml interface mapping' >&2; exit 1; }
grep -Eq '^  display_name: "([^"\\]|\\.)*"$' "$root/agents/openai.yaml" || { echo 'invalid quoted display_name' >&2; exit 1; }
grep -Eq '^  short_description: "([^"\\]|\\.)*"$' "$root/agents/openai.yaml" || { echo 'invalid quoted short_description' >&2; exit 1; }
grep -Eq '^  default_prompt: "([^"\\]|\\.)*"$' "$root/agents/openai.yaml" || { echo 'invalid quoted default_prompt' >&2; exit 1; }

require 'smallest single-responsibility chunk' "$root/SKILL.md" 'smallest single-responsibility chunks'
require '>= 95/100 readiness' "$root/SKILL.md" 'per-chunk readiness threshold'
require 'not a mathematical probability of correctness or reliability' "$root/SKILL.md" 'score limitation'
require 'optional Agent Brain' "$root/SKILL.md" 'optional Agent Brain evidence logging'
require 'focused tests' "$root/references/review-and-gate-checklists.md" 'focused chunk tests'
require 'blueprint-to-code review' "$root/references/review-and-gate-checklists.md" 'blueprint-to-code review'
require 'Explicit contract verification' "$root/references/review-and-gate-checklists.md" 'contract verification'
require 'no unresolved critical assumption' "$root/references/review-and-gate-checklists.md" 'critical-assumption veto'
require 'Incrementally integrate' "$root/SKILL.md" 'incremental integration'
require 'regression checks' "$root/SKILL.md" 'regression checks'
require 'Deductions' "$root/references/readiness-rubric.md" 'reproducible deductions'
require 'No unresolved critical risk' "$root/references/readiness-rubric.md" 'critical-risk veto'
require 'Integration result' "$root/references/blueprint-templates.md" 'integration traceability'
require 'pressure scenarios' "$root/tests/pressure-scenarios.md" 'pressure scenarios'
require 'Baseline' "$root/tests/baseline-no-skill.md" 'baseline pressure evidence'
require 'Forward' "$root/tests/forward-test-with-skill.md" 'forward pressure evidence'
test -f README.md || { echo 'missing: README.md' >&2; exit 1; }
require 'https://github.com/sandeep84397/blueprint-first-delivery.git' README.md 'exact clone URL'
require 'skills/blueprint-first-delivery' README.md 'skill installation path'
