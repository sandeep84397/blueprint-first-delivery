#!/usr/bin/env sh
set -eu

project_root=$(CDPATH='' cd -- "$(dirname "$0")/../../.." && pwd)
skill_root=skills/blueprint-first-delivery
validator="$project_root/$skill_root/scripts/validate_skill.py"
fixtures="$project_root/$skill_root/tests/fixtures"

assert_rejected() {
  fixture=$1
  destination=$2
  expected=$3
  mode=${4:-replace}
  temp_dir=$(mktemp -d)
  output="$temp_dir/validator-output"
  mkdir -p "$temp_dir/skills"
  cp -R "$project_root/$skill_root" "$temp_dir/skills/"
  cp "$project_root/README.md" "$temp_dir/README.md"
  if test "$mode" = append; then
    cat "$fixtures/$fixture" >>"$temp_dir/$destination"
  else
    cp "$fixtures/$fixture" "$temp_dir/$destination"
  fi

  set +e
  python3 "$validator" "$temp_dir/$skill_root" >"$output" 2>&1
  status=$?
  set -e
  if ! test "$status" -eq 1; then
    cat "$output" >&2
    rm -rf "$temp_dir"
    echo "wrong exit for invalid fixture: $fixture (got $status, expected 1)" >&2
    exit 1
  fi
  if ! grep -Fq -- "$expected" "$output"; then
    cat "$output" >&2
    rm -rf "$temp_dir"
    echo "wrong diagnostic for invalid fixture: $fixture" >&2
    exit 1
  fi

  rm -rf "$temp_dir"
}

assert_rejected metadata-outside-frontmatter.md "$skill_root/SKILL.md" "metadata outside frontmatter" append
assert_rejected missing-frontmatter-delimiters.md "$skill_root/SKILL.md" "SKILL.md:1: expected frontmatter delimiter"
assert_rejected malformed-display-name.yaml "$skill_root/agents/openai.yaml" "agents/openai.yaml:2: invalid quoted display_name"
