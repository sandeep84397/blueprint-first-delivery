#!/usr/bin/env sh
set -eu

project_root=$(CDPATH= cd -- "$(dirname "$0")/../../.." && pwd)
skill_root=skills/blueprint-first-delivery
validator="$project_root/$skill_root/tests/validate-skill.sh"
fixtures="$project_root/$skill_root/tests/fixtures"

assert_rejected() {
  fixture=$1
  destination=$2
  temp_dir=$(mktemp -d)
  mkdir -p "$temp_dir/skills"
  cp -R "$project_root/$skill_root" "$temp_dir/skills/"
  cp "$project_root/README.md" "$temp_dir/README.md"
  cp "$fixtures/$fixture" "$temp_dir/$destination"

  if (cd "$temp_dir" && sh "$validator") >/dev/null 2>&1; then
    rm -rf "$temp_dir"
    echo "accepted invalid fixture: $fixture" >&2
    exit 1
  fi

  rm -rf "$temp_dir"
}

(cd "$project_root" && sh "$validator")
assert_rejected metadata-outside-frontmatter.md "$skill_root/SKILL.md"
assert_rejected missing-frontmatter-delimiters.md "$skill_root/SKILL.md"
assert_rejected malformed-display-name.yaml "$skill_root/agents/openai.yaml"
