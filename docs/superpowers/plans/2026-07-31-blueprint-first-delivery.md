# Blueprint-First Delivery Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish a portable Codex skill that enforces blueprint-first, confidence-gated delivery.

**Architecture:** A single discoverable skill provides the workflow. Three reference files hold fill-in templates, rubric, and gates. A shell validator checks package shape and required workflow language; pressure scenarios document agent behavior before and after the skill.

**Tech Stack:** Markdown, YAML, POSIX shell, GitHub.

## Global Constraints

- Name the skill `blueprint-first-delivery`.
- Require process-readiness score `>= 95/100`; never call it a correctness probability.
- Require plain-English module blueprint and principal-engineer-style adversarial review before code.
- Permit parallel work only with frozen contracts and non-overlapping file/state ownership.
- Treat integration as a separate blueprint, gate, and verification step.
- Keep Agent Brain optional.

---

### Task 1: Create failing package-contract test and baseline pressure evidence

**Files:**
- Create: `skills/blueprint-first-delivery/tests/validate-skill.sh`
- Create: `skills/blueprint-first-delivery/tests/pressure-scenarios.md`
- Create: `skills/blueprint-first-delivery/tests/baseline-no-skill.md`

**Interfaces:**
- Produces: `validate-skill.sh`, executable from the repository root with no arguments.
- Produces: three pressure scenarios: premature coding, false independence, skipped integration.

- [ ] **Step 1: Write the failing test**

```sh
#!/usr/bin/env sh
set -eu
root=skills/blueprint-first-delivery
for file in SKILL.md agents/openai.yaml references/blueprint-templates.md references/readiness-rubric.md references/review-and-gate-checklists.md; do
  test -f "$root/$file" || { echo "missing: $root/$file" >&2; exit 1; }
done
grep -q '^name: blueprint-first-delivery$' "$root/SKILL.md"
grep -q '95/100' "$root/SKILL.md"
grep -q 'integration' "$root/SKILL.md"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `sh skills/blueprint-first-delivery/tests/validate-skill.sh`

Expected: `FAIL` with `missing: skills/blueprint-first-delivery/SKILL.md`.

- [ ] **Step 3: Record baseline pressure behavior without the skill**

Run three fresh agents with only each scenario from `pressure-scenarios.md`. Record exact outputs and whether each agent starts coding, treats dependent chunks as parallel, or skips integration after unit tests.

- [ ] **Step 4: Commit**

```bash
git add skills/blueprint-first-delivery/tests
git commit -m "test: define skill package contract"
```

### Task 2: Implement the skill and reusable references

**Files:**
- Create: `skills/blueprint-first-delivery/SKILL.md`
- Create: `skills/blueprint-first-delivery/agents/openai.yaml`
- Create: `skills/blueprint-first-delivery/references/blueprint-templates.md`
- Create: `skills/blueprint-first-delivery/references/readiness-rubric.md`
- Create: `skills/blueprint-first-delivery/references/review-and-gate-checklists.md`
- Modify: `skills/blueprint-first-delivery/tests/validate-skill.sh`

**Interfaces:**
- Consumes: package contract and pressure scenarios from Task 1.
- Produces: a self-contained Codex skill and references discoverable by `SKILL.md` links.

- [ ] **Step 1: Preserve the Task 1 failing test unchanged**

Run: `sh skills/blueprint-first-delivery/tests/validate-skill.sh`

Expected: `FAIL` because the skill package does not exist.

- [ ] **Step 2: Implement minimal package**

Create concise imperative instructions that require the module blueprint, independent review, the `>= 95/100` readiness gate, dependency classification, chunk gates, separate integration gate, and traceability report. Link to each reference only when that artifact is needed.

- [ ] **Step 3: Run test to verify it passes**

Run: `sh skills/blueprint-first-delivery/tests/validate-skill.sh`

Expected: `PASS` with exit code `0`.

- [ ] **Step 4: Forward-test pressure scenarios with the new skill**

Run the same three prompts with a fresh agent instructed to use the skill. Record results in `skills/blueprint-first-delivery/tests/forward-test-with-skill.md`. Each output must reject its unsafe shortcut and name the required gate/artifact.

- [ ] **Step 5: Commit**

```bash
git add skills/blueprint-first-delivery
git commit -m "feat: add blueprint-first delivery skill"
```

### Task 3: Publish installation and usage guidance

**Files:**
- Modify: `README.md`
- Modify: `skills/blueprint-first-delivery/tests/validate-skill.sh`

**Interfaces:**
- Consumes: completed package from Task 2.
- Produces: clone/install/use instructions and a validator assertion for the README.

- [ ] **Step 1: Add a failing README assertion**

Append to `validate-skill.sh`:

```sh
test -f README.md || { echo 'missing: README.md' >&2; exit 1; }
grep -q 'blueprint-first-delivery' README.md
grep -q 'skills/blueprint-first-delivery' README.md
```

- [ ] **Step 2: Run test to verify it fails**

Run: `sh skills/blueprint-first-delivery/tests/validate-skill.sh`

Expected: `FAIL` because the starter README does not contain the skill name.

- [ ] **Step 3: Implement minimal README**

Include purpose, repository layout, install command using `~/.codex/skills`, trigger examples, and validation command. State that the score measures readiness evidence, not probability.

- [ ] **Step 4: Run full verification**

Run: `sh skills/blueprint-first-delivery/tests/validate-skill.sh && git diff --check`

Expected: `PASS` with no whitespace errors.

- [ ] **Step 5: Commit**

```bash
git add README.md skills/blueprint-first-delivery/tests/validate-skill.sh
git commit -m "docs: add skill installation guide"
```
