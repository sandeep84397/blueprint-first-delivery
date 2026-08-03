# Cross-Runtime Model Routing Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add evidence-based per-chunk model routing for Codex and Claude Code while keeping this repository the single workflow source.

**Architecture:** Keep one provider-neutral `SKILL.md` and one shared routing policy. Resolve only the active runtime through isolated Codex and Claude Code mapping documents, record versioned routing evidence in each chunk blueprint, and enforce the contract through the existing dependency-free validator and pressure scenarios.

**Tech Stack:** Markdown Agent Skill, Python 3.9+ standard library, POSIX `sh`, `unittest`, Git.

## Global Constraints

- Work directly on `main`; do not create a worktree.
- Modify only `/Users/sandeepdhami/Documents/GitHub/blueprint-first-delivery`.
- Do not edit global `CLAUDE.md`, `AGENTS.md`, Codex/Claude configuration, or custom-agent files.
- Support Codex and Claude Code only; Claude.ai and direct API workflows remain out of scope.
- Keep exactly one shared `SKILL.md`; provider model identifiers may appear only in runtime-mapping references and repository-level documentation/specifications.
- Keep `SKILL.md` below 500 words.
- Keep the validator dependency-free and compatible with CPython 3.9+.
- Keep shell validation compatible with POSIX `sh`.
- Preserve all existing 53 tests and their exact rubric/workflow contracts.
- Use routing schema version `1`, policy version `1`, and mapping version `1`.
- Deep and Maximum routes cannot pass without verified execution evidence meeting the established floor.
- A below-floor override remains gate-blocked.
- Parallel execution requires relational dependency, contract, ownership, and integration evidence.
- Use RED → GREEN → focused regression → commit for every task.

## File Structure

- `skills/blueprint-first-delivery/references/model-routing.md`: provider-neutral tier, topology, transition, manifest, review, and floor rules.
- `skills/blueprint-first-delivery/references/runtime-mappings/codex.md`: Codex model/effort/request/fallback/verification mapping.
- `skills/blueprint-first-delivery/references/runtime-mappings/claude-code.md`: Claude Code model/effort/request/fallback/verification mapping.
- `skills/blueprint-first-delivery/SKILL.md`: concise workflow hook that makes routing mandatory before each chunk.
- `skills/blueprint-first-delivery/references/blueprint-templates.md`: versioned routing and relational parallel-group schema.
- `skills/blueprint-first-delivery/references/review-and-gate-checklists.md`: independent route review and route-aware start/completion gates.
- `skills/blueprint-first-delivery/tests/model-routing-pressure-scenarios.md`: deterministic routing, transition, fallback, and negative scenarios.
- `skills/blueprint-first-delivery/scripts/validate_skill.py`: package, provider-boundary, routing-contract, and pressure-contract validation.
- `skills/blueprint-first-delivery/scripts/verify_global_boundary.py`: deterministic absent-aware comparison against a committed baseline artifact.
- `skills/blueprint-first-delivery/tests/test_validate_skill.py`: mutation-based tests for every routing contract.
- `skills/blueprint-first-delivery/tests/test_verify_global_boundary.py`: portable verifier behavior tests using temporary paths.
- `skills/blueprint-first-delivery/tests/validate-skill.sh`: dual-runtime README assertions plus the existing validation call graph.
- `README.md`: Codex/Claude Code installation, usage, mapping, evidence, and single-source guidance.
- `docs/superpowers/reports/2026-08-03-cross-runtime-model-routing-global-baseline.json`: immutable pre-Task-1 boundary states.
- `docs/superpowers/reports/2026-08-03-cross-runtime-model-routing-global-baseline-anchor.json`: pre-Task-1 baseline commit and Git blob identity.
- `docs/superpowers/reports/2026-08-03-cross-runtime-model-routing-traceability.md`: final requirement-to-test/review evidence.

---

### Task 0: Commit the Reviewed Plan and Capture Scope Evidence

**Routing:**
- Tier: Light requested; Codex fallback Terra/low if Luna is unavailable.
- Topology: ordered.
- Evidence: exact Git operations and read-only hash collection with objective output.

**Files:**
- Commit: `docs/superpowers/plans/2026-08-03-cross-runtime-model-routing.md`
- Create: `docs/superpowers/reports/2026-08-03-cross-runtime-model-routing-global-baseline.json`
- Create: `docs/superpowers/reports/2026-08-03-cross-runtime-model-routing-global-baseline-anchor.json`
- Create: `docs/superpowers/reports/2026-08-03-cross-runtime-model-routing-traceability.md`
- Create: `skills/blueprint-first-delivery/scripts/verify_global_boundary.py`
- Create: `skills/blueprint-first-delivery/tests/test_verify_global_boundary.py`

**Interfaces:**
- Consumes: approved design and independently reviewed implementation plan.
- Produces: committed plan, clean pre-implementation repository state, and durable initial global-file evidence consumed by Task 5.

- [ ] **Step 1: Commit the reviewed plan before implementation**

```sh
git diff --check
git add docs/superpowers/plans/2026-08-03-cross-runtime-model-routing.md
git commit -m "docs: plan cross-runtime model routing"
git status --porcelain
```

Expected: `git diff --check` exits `0`; commit succeeds; `git status --porcelain` emits no output.

- [ ] **Step 2: Collect absent-aware initial global-file evidence**

Run this read-only POSIX loop:

```sh
for target in /Users/sandeepdhami/.claude/CLAUDE.md /Users/sandeepdhami/.codex/AGENTS.md /Users/sandeepdhami/.codex/config.toml
do
  if test -f "$target"
  then
    shasum -a 256 "$target"
  else
    printf 'absent  %s\n' "$target"
  fi
done
```

Expected: exactly three rows; each row contains a SHA-256 value or literal `absent` plus the exact path.

- [ ] **Step 3: Create the immutable baseline artifact and initial report**

Create `docs/superpowers/reports/2026-08-03-cross-runtime-model-routing-global-baseline.json` using `apply_patch`. It has exactly these top-level keys:

- `schema_version` with integer value `1`;
- `captured_before_task` with string value `Task 1`;
- `paths`, an ordered three-element array.

Each `paths` element has only `path` and `state`. Use the three exact paths from Step 2 in the same order. Each `state` is the exact emitted 64-character lowercase digest or literal `absent`. Do not add a timestamp, invented value, or deferred marker.

Create the traceability report with this exact initial content:

```markdown
# Cross-Runtime Model Routing Traceability

## Scope

Repository-only implementation for Codex and Claude Code. No global guidance, runtime configuration, or custom-agent mutation is authorized.

## Pre-implementation global state

Immutable baseline artifact: `docs/superpowers/reports/2026-08-03-cross-runtime-model-routing-global-baseline.json`

The baseline artifact records the three absent-aware SHA-256 states captured and committed before Task 1.

## Evidence limitation

Initial/final byte equality can prove equal boundary states. It cannot prove a file was never transiently modified. Repository write scope and tool/action logs provide the separate no-write audit trail.
```

Validate the JSON and re-run the Step 2 loop. The JSON values and fresh output must agree before commit:

```sh
python3 -m json.tool docs/superpowers/reports/2026-08-03-cross-runtime-model-routing-global-baseline.json
```

- [ ] **Step 4: Commit scope evidence**

```sh
git add docs/superpowers/reports/2026-08-03-cross-runtime-model-routing-global-baseline.json docs/superpowers/reports/2026-08-03-cross-runtime-model-routing-traceability.md
git commit -m "docs: capture model routing scope baseline"
git status --porcelain
```

Expected: commit succeeds; `git status --porcelain` emits no output.

- [ ] **Step 5: Persist the baseline commit and blob anchor**

Run:

```sh
git rev-parse HEAD
git rev-parse HEAD:docs/superpowers/reports/2026-08-03-cross-runtime-model-routing-global-baseline.json
```

The first command emits the full commit containing the original baseline artifact. The second emits that commit's Git blob OID for the artifact. Create `docs/superpowers/reports/2026-08-03-cross-runtime-model-routing-global-baseline-anchor.json` with `apply_patch`. It has exactly:

- `schema_version` with integer value `1`;
- `baseline_path` with the repository-relative baseline path used above;
- `baseline_commit` with the first exact command output;
- `baseline_blob_oid` with the second exact command output.

Validate and commit the anchor before Task 1:

```sh
python3 -m json.tool docs/superpowers/reports/2026-08-03-cross-runtime-model-routing-global-baseline-anchor.json
baseline_path="docs/superpowers/reports/2026-08-03-cross-runtime-model-routing-global-baseline.json"
baseline_commit_sha="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["baseline_commit"])' docs/superpowers/reports/2026-08-03-cross-runtime-model-routing-global-baseline-anchor.json)"
baseline_blob_oid="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["baseline_blob_oid"])' docs/superpowers/reports/2026-08-03-cross-runtime-model-routing-global-baseline-anchor.json)"
test "$(git rev-parse "$baseline_commit_sha:$baseline_path")" = "$baseline_blob_oid"
test "$(git rev-parse "HEAD:$baseline_path")" = "$baseline_blob_oid"
git add docs/superpowers/reports/2026-08-03-cross-runtime-model-routing-global-baseline-anchor.json
git commit -m "docs: anchor model routing scope baseline"
git status --porcelain
```

Expected: JSON is valid; commit succeeds; status is clean. The commit adding the anchor file becomes the independently discoverable Task 0 anchor. Do not amend, rebase, or replace either Task 0 evidence commit.

- [ ] **Step 6: Write portable RED tests for the boundary verifier**

Create `skills/blueprint-first-delivery/tests/test_verify_global_boundary.py`:

```python
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


REPO_ROOT = Path(__file__).resolve().parents[3]
SCRIPT = (
    REPO_ROOT
    / "skills"
    / "blueprint-first-delivery"
    / "scripts"
    / "verify_global_boundary.py"
)


class BoundaryVerifierTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.baseline = self.root / "baseline.json"

    @staticmethod
    def digest(value):
        return hashlib.sha256(value).hexdigest()

    def write_baseline(self, rows, schema_version=1):
        self.baseline.write_text(json.dumps({
            "schema_version": schema_version,
            "captured_before_task": "Task 1",
            "paths": rows,
        }))

    def run_verifier(self):
        return subprocess.run(
            [sys.executable, str(SCRIPT), str(self.baseline)],
            capture_output=True,
            text=True,
            timeout=10,
        )

    def test_equal_file_and_absent_states_pass(self):
        present = self.root / "present.txt"
        present.write_bytes(b"stable")
        absent = self.root / "absent.txt"
        self.write_baseline([
            {"path": str(present), "state": self.digest(b"stable")},
            {"path": str(absent), "state": "absent"},
        ])
        result = self.run_verifier()
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("PASS (2 paths unchanged)", result.stdout)

    def test_changed_file_is_rejected(self):
        target = self.root / "target.txt"
        target.write_bytes(b"after")
        self.write_baseline([
            {"path": str(target), "state": self.digest(b"before")},
        ])
        result = self.run_verifier()
        self.assertEqual(1, result.returncode, result.stderr)
        self.assertIn("boundary changed", result.stderr)

    def test_invalid_baseline_is_rejected(self):
        self.write_baseline([], schema_version=2)
        result = self.run_verifier()
        self.assertEqual(2, result.returncode)
        self.assertIn("invalid baseline", result.stderr)


if __name__ == "__main__":
    unittest.main()
```

Run:

```sh
python3 -B -m unittest discover -s skills/blueprint-first-delivery/tests -p 'test_verify_global_boundary.py'
```

Expected: RED because `verify_global_boundary.py` does not exist.

- [ ] **Step 7: Implement the deterministic boundary verifier**

Create `skills/blueprint-first-delivery/scripts/verify_global_boundary.py`:

```python
#!/usr/bin/env python3
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys


STATE_PATTERN = re.compile(r"(?:[0-9a-f]{64}|absent)")


class BaselineError(ValueError):
    pass


def file_state(path):
    if not path.exists():
        return "absent"
    if not path.is_file():
        return "not-a-regular-file"
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(65536), b""):
            digest.update(block)
    return digest.hexdigest()


def load_baseline(path):
    try:
        document = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as error:
        raise BaselineError(str(error)) from error
    if not isinstance(document, dict):
        raise BaselineError("baseline root must be an object")
    if set(document) != {"schema_version", "captured_before_task", "paths"}:
        raise BaselineError("baseline root contains unexpected fields")
    if document.get("schema_version") != 1:
        raise BaselineError("schema_version must be 1")
    if document.get("captured_before_task") != "Task 1":
        raise BaselineError("captured_before_task must be Task 1")
    rows = document.get("paths")
    if not isinstance(rows, list) or not rows:
        raise BaselineError("paths must be a non-empty list")
    seen = set()
    result = []
    for row in rows:
        if not isinstance(row, dict) or set(row) != {"path", "state"}:
            raise BaselineError("each path row must contain only path and state")
        target = Path(row["path"])
        state = row["state"]
        if not target.is_absolute():
            raise BaselineError("baseline paths must be absolute")
        if not isinstance(state, str) or STATE_PATTERN.fullmatch(state) is None:
            raise BaselineError("state must be a SHA-256 digest or absent")
        if str(target) in seen:
            raise BaselineError("baseline paths must be unique")
        seen.add(str(target))
        result.append((target, state))
    return result


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("baseline", type=Path)
    args = parser.parse_args(argv)
    try:
        rows = load_baseline(args.baseline)
        mismatches = []
        for target, expected in rows:
            observed = file_state(target)
            if observed != expected:
                mismatches.append((target, expected, observed))
    except (BaselineError, OSError) as error:
        print(f"invalid baseline: {error}", file=sys.stderr)
        return 2
    if mismatches:
        for target, expected, observed in mismatches:
            print(
                f"boundary changed: {target}: expected {expected}, observed {observed}",
                file=sys.stderr,
            )
        return 1
    print(f"Global boundary verification: PASS ({len(rows)} paths unchanged)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 8: Verify baseline provenance and commit the verifier**

```sh
python3 -B -m unittest discover -s skills/blueprint-first-delivery/tests -p 'test_verify_global_boundary.py'
python3 -B skills/blueprint-first-delivery/scripts/verify_global_boundary.py docs/superpowers/reports/2026-08-03-cross-runtime-model-routing-global-baseline.json
git diff --check
git add skills/blueprint-first-delivery/scripts/verify_global_boundary.py skills/blueprint-first-delivery/tests/test_verify_global_boundary.py
git commit -m "test: verify repository scope boundary"
git status --porcelain
```

Expected: three verifier tests pass; live verification prints `PASS (3 paths unchanged)`; diff check and commit succeed; status is clean. If live verification fails, stop. Do not modify the anchored baseline; a corrected, independently reviewed evidence artifact and anchor path are required before Task 1.

---

### Task 1: Shared Routing Policy and Runtime Mapping Contract

**Routing:**
- Tier/floor: Deep because this task creates public cross-runtime routing contracts.
- Topology: ordered.
- Codex: `gpt-5.6-sol`, high.
- Claude Code: `opus`, high.
- Evidence: public-contract change and cross-runtime causal behavior establish the approved Deep floor.
- Escalate effort to xhigh only if the same stable contract defect remains unresolved after a high-effort evidence-backed attempt.

**Files:**
- Create: `skills/blueprint-first-delivery/references/model-routing.md`
- Create: `skills/blueprint-first-delivery/references/runtime-mappings/codex.md`
- Create: `skills/blueprint-first-delivery/references/runtime-mappings/claude-code.md`
- Modify: `skills/blueprint-first-delivery/tests/test_validate_skill.py`
- Modify: `skills/blueprint-first-delivery/scripts/validate_skill.py`

**Interfaces:**
- Consumes: approved tier/floor/topology/runtime contracts from `docs/superpowers/specs/2026-08-03-cross-runtime-model-routing-design.md`.
- Produces: `NEUTRAL_ROUTING_FILES`, `_validate_model_routing(files)`, and three validated routing references consumed by Tasks 2–5.

- [ ] **Step 1: Write only the desired-state file test**

Add this constant at module scope:

```python
ROUTING_REQUIRED_FILES = (
    "references/model-routing.md",
    "references/runtime-mappings/codex.md",
    "references/runtime-mappings/claude-code.md",
)
```

Add this method inside the existing `ValidateSkillTests` class:

```python
    def test_routing_contract_files_exist(self):
        for relative in ROUTING_REQUIRED_FILES:
            with self.subTest(relative=relative):
                self.assertTrue((SKILL_ROOT / relative).is_file(), relative)
```

- [ ] **Step 2: Run tests and verify the intended RED**

```sh
python3 -B -m unittest discover -s skills/blueprint-first-delivery/tests -p 'test_validate_skill.py'
```

Expected: `test_routing_contract_files_exist` fails because the three routing references do not exist. No removal mutation runs against an absent file.

- [ ] **Step 3: Create the provider-neutral routing policy**

Create `references/model-routing.md` with these normative sections and exact rules:

```markdown
# Model routing policy

## Evaluation order

1. Establish a hard risk floor. Architecture/public-contract change, security, privacy, authorization, concurrency, persistence, migration, data integrity, irreversible blast radius, unresolved critical ambiguity, cross-module causal reasoning, a wrong design assumption, or two evidence-backed failures on one stable root fingerprint establish Deep.
2. Evaluate Maximum only for the hardest indivisible critical problem after xhigh evidence is insufficient.
3. When no Deep/Maximum floor applies, use Light only when scope and output are exact, contracts are frozen, risk is local/reversible, no protected-risk trigger exists, and an objective oracle exists.
4. Otherwise use Standard.

The effective transition is max(next tier, established floor). Cheapest capable means lowest tier allowed by this evidence, not cheapest model regardless of risk.

## Failure fingerprint

A root fingerprint records acceptance criterion, deterministic command/oracle, stable failure signature, and suspected causal boundary. Count two failures only for two distinct tested hypotheses with the same fingerprint. Reset after a material contract, oracle, signature, or causal-boundary change.

## Topology

Ordered is the default. Parallel requires a parallel group whose members record chunk IDs, dependencies, frozen contract IDs/versions/references, exclusive file/state ownership, independent verification, integration owner, and integration order. File count never proves independence.

## Runtime resolution

Load only the active runtime mapping. Record mapping path, version, SHA-256, requested model/effort, request mechanism, and observed execution metadata. Unknown runtimes remain recommendation-only.

Deep/Maximum require verified observed model and effort meeting the floor. Light/Standard may use inherited/unverified execution only when no higher floor applies and must not claim enforced cost optimization. Try declared same-tier fallback, then a higher tier; Maximum unavailable blocks or forces decomposition.

## Review, override, and transitions

Author and principal reviewer differ. Review catches under-routing, over-routing, false parallelism, unresolved findings, and false execution claims. A below-floor override remains blocked. De-escalation requires no current hard trigger, frozen reviewed decisions/contracts, an objective oracle, and no critical finding. Append every transition; never overwrite history.

## Compatibility

Completed blueprints without routing schema remain historical and are labeled legacy-unrouted. A legacy chunk must add schema version 1 and pass independent route review before implementation resumes. Unknown runtimes receive only the provider-neutral recommendation.
```

- [ ] **Step 4: Create the Codex runtime mapping**

Create `references/runtime-mappings/codex.md` with:

````markdown
# Codex runtime mapping

Mapping version: `1`

| Tier | Requested model | Effort | Same-tier fallback | Higher fallback |
| --- | --- | --- | --- | --- |
| Light | `gpt-5.6-luna` | `low` | none | `gpt-5.6-terra` / `low` |
| Standard | `gpt-5.6-terra` | `medium` | none | `gpt-5.6-sol` / `medium` |
| Deep | `gpt-5.6-sol` | `high` | none | `gpt-5.6-sol` / `max` only after Maximum review |
| Maximum | `gpt-5.6-sol` | `max` | none | blocked; decompose or review a new mapping |

## Request mechanism

Use a model-pinned custom subagent or a runtime call that explicitly accepts model and reasoning effort. A generic task label does not prove selection. Record the request metadata returned by the runtime.

## Availability and supported effort

Before dispatch, inspect the callable custom-agent/runtime metadata for the requested model and effort. If availability or effective effort cannot be observed, mark execution unverified. Deep and Maximum remain blocked. Deep may request xhigh only with policy evidence; Maximum uses max.

## Verification and fallback

Record runtime version, observed model, observed effort, metadata source, observation timestamp, alias resolution, and fallback chain. If the runtime cannot prove a Deep/Maximum floor, block. If Luna is unavailable, Light may promote to Terra/low and must record the promotion.

Codex Ultra is orchestrator-level parallel execution for at least two independently proven workstreams. It is not a chunk tier or a substitute for Maximum.

## Digest

Compute the mapping digest from the repository root:

```sh
shasum -a 256 skills/blueprint-first-delivery/references/runtime-mappings/codex.md
```
````

- [ ] **Step 5: Create the Claude Code runtime mapping**

Create `references/runtime-mappings/claude-code.md` with:

````markdown
# Claude Code runtime mapping

Mapping version: `1`

| Tier | Requested model | Effort | Same-tier fallback | Higher fallback |
| --- | --- | --- | --- | --- |
| Light | `haiku` | `low` | none | `sonnet` / `low` |
| Standard | `sonnet` | `medium` | none | `opus` / `medium` |
| Deep | `opus` | `high` | none | `opus` / `max` only after Maximum review |
| Maximum | `opus` | `max` | none | blocked; decompose or review a new mapping |

## Request mechanism

Use a Claude Code subagent whose frontmatter or invocation pins `model` and `effort`.

## Availability and supported effort

Inspect and record `CLAUDE_CODE_SUBAGENT_MODEL`, `CLAUDE_CODE_EFFORT_LEVEL`, organization `availableModels`, organization effort caps, and runtime-reported effective model/effort. Environment or organization overrides win over subagent frontmatter. Unsupported effort may fall downward; Deep/Maximum mismatches block.

## Verification and fallback

Record runtime version, requested alias, resolved/observed model, observed effort, metadata source, observation timestamp, and fallback chain. If the runtime cannot prove a Deep/Maximum floor, block. Unsupported effort fallback is not proof that the requested floor ran.

## Digest

Compute the mapping digest from the repository root:

```sh
shasum -a 256 skills/blueprint-first-delivery/references/runtime-mappings/claude-code.md
```
````

- [ ] **Step 6: Verify the file test turns GREEN**

```sh
python3 -B -m unittest discover -s skills/blueprint-first-delivery/tests -p 'test_validate_skill.py'
```

Expected: the new file-existence test passes and the original suite remains green.

- [ ] **Step 7: Write failing generic mapping/parser and leakage tests**

Add `NEW_PACKAGE_REQUIRED_FILES` at module scope. Add the helpers and tests inside `ValidateSkillTests`. They derive provider model values from mapping files; no provider model literal is duplicated:

```python
NEW_PACKAGE_REQUIRED_FILES = ROUTING_REQUIRED_FILES + (
    "scripts/verify_global_boundary.py",
    "tests/test_verify_global_boundary.py",
)
```

Inside `ValidateSkillTests`, add:

```python
    @staticmethod
    def replace_mapping_cell(text, tier, column, value):
        lines = text.splitlines()
        for index, line in enumerate(lines):
            if line.startswith(f"| {tier} |"):
                cells = line.split("|")
                cells[column] = f" {value} "
                lines[index] = "|".join(cells)
                return "\n".join(lines) + "\n"
        raise AssertionError(f"missing mapping tier: {tier}")

    @staticmethod
    def mapping_model(text, tier):
        row = next(
            line for line in text.splitlines()
            if line.startswith(f"| {tier} |")
        )
        return row.split("|")[2].strip().strip("`")

    def test_runtime_mapping_structure_is_enforced(self):
        for filename in ("codex.md", "claude-code.md"):
            path = self.skill / "references" / "runtime-mappings" / filename
            original = path.read_text()

            with self.subTest(filename=filename, mutation="missing tier"):
                path.write_text(original.replace("| Maximum |", "| Removed |", 1))
                try:
                    result = self.run_validator()
                    self.assertEqual(1, result.returncode, result.stderr)
                    self.assertIn(
                        "runtime mapping tiers must be exactly",
                        result.stderr,
                    )
                finally:
                    path.write_text(original)

            tiers = ("Light", "Standard", "Deep", "Maximum")
            for tier_index, tier in enumerate(tiers):
                wrong_same_effort = (
                    "`alternate` / `low`"
                    if tier == "Maximum"
                    else "`alternate` / `max`"
                )
                cases = (
                    ("empty model", 2, "", f"missing model for {tier}"),
                    ("wrong effort", 3, "`invalid`", f"invalid effort for {tier}"),
                    ("empty same-tier fallback", 4, "", "fallback cells must be non-empty"),
                    ("empty higher fallback", 5, "", "fallback cells must be non-empty"),
                    (
                        "same-tier fallback effort mismatch",
                        4,
                        wrong_same_effort,
                        f"invalid same-tier fallback for {tier}",
                    ),
                    (
                        "invalid higher fallback",
                        5,
                        "Standard" if tier == "Maximum" else "none",
                        (
                            "Maximum fallback must block"
                            if tier == "Maximum"
                            else f"higher fallback must declare model and effort for {tier}"
                        ),
                    ),
                )
                if tier != "Maximum":
                    source_tier = tier if tier_index == 0 else tiers[tier_index - 1]
                    lower_or_current_model = self.mapping_model(original, source_tier)
                    current_row = next(
                        line for line in original.splitlines()
                        if line.startswith(f"| {tier} |")
                    )
                    current_effort = current_row.split("|")[3].strip()
                    cases += ((
                        "higher fallback targets current or lower tier",
                        5,
                        f"`{lower_or_current_model}` / {current_effort}",
                        f"higher fallback must target a higher tier for {tier}",
                    ),)
                for mutation, column, value, expected in cases:
                    with self.subTest(
                        filename=filename,
                        tier=tier,
                        mutation=mutation,
                    ):
                        path.write_text(
                            self.replace_mapping_cell(original, tier, column, value)
                        )
                        try:
                            result = self.run_validator()
                            self.assertEqual(1, result.returncode, result.stderr)
                            self.assertIn(expected, result.stderr)
                        finally:
                            path.write_text(original)

            section_cases = (
                ("Mapping version: `1`", "missing mapping version"),
                ("## Request mechanism", "missing mapping section"),
                ("## Availability and supported effort", "missing mapping section"),
                ("## Verification and fallback", "missing mapping section"),
                ("## Digest", "missing mapping section"),
            )
            for marker, expected in section_cases:
                with self.subTest(filename=filename, marker=marker):
                    path.write_text(original.replace(marker, "removed", 1))
                    try:
                        result = self.run_validator()
                        self.assertEqual(1, result.returncode, result.stderr)
                        self.assertIn(expected, result.stderr)
                    finally:
                        path.write_text(original)

    def test_new_package_files_are_required(self):
        for relative in NEW_PACKAGE_REQUIRED_FILES:
            with self.subTest(relative=relative):
                path = self.skill / relative
                original = path.read_bytes()
                path.unlink()
                try:
                    result = self.run_validator()
                    self.assertEqual(1, result.returncode, result.stderr)
                    self.assertIn(
                        f"{relative}:0: missing required file",
                        result.stderr,
                    )
                finally:
                    path.write_bytes(original)

    def test_provider_model_value_leaking_into_shared_policy_is_rejected(self):
        mapping = (
            self.skill / "references" / "runtime-mappings" / "codex.md"
        ).read_text()
        provider_model = self.mapping_model(mapping, "Standard")
        path = self.skill / "references" / "model-routing.md"

        def mutate():
            path.write_text(
                path.read_text() + f"\nSelected provider model: {provider_model}\n"
            )

        original = path.read_text()
        try:
            self.assert_invalid(
                "provider model identifier outside runtime mappings",
                mutate,
            )
        finally:
            path.write_text(original)
```

Run:

```sh
python3 -B -m unittest discover -s skills/blueprint-first-delivery/tests -p 'test_validate_skill.py'
```

Expected: the new mutation tests fail because the current validator accepts malformed mappings and provider leakage.

- [ ] **Step 8: Implement package requirements, a generic mapping parser, and derived leakage**

Add all five entries from `NEW_PACKAGE_REQUIRED_FILES` to `REQUIRED_FILES`, then add:

```python
RUNTIME_MAPPING_FILES = (
    "references/runtime-mappings/codex.md",
    "references/runtime-mappings/claude-code.md",
)
NEUTRAL_ROUTING_FILES = (
    "SKILL.md",
    "references/model-routing.md",
    "references/blueprint-templates.md",
    "references/readiness-rubric.md",
    "references/review-and-gate-checklists.md",
)
MAPPING_TIERS = ("Light", "Standard", "Deep", "Maximum")
MAPPING_EFFORTS = {
    "Light": "`low`",
    "Standard": "`medium`",
    "Deep": "`high`",
    "Maximum": "`max`",
}
MAPPING_SECTIONS = (
    "## Request mechanism",
    "## Availability and supported effort",
    "## Verification and fallback",
    "## Digest",
)
FALLBACK_RELATION = re.compile(
    r"^`([^`]+)`\s*/\s*`(low|medium|high|xhigh|max)`(?:\s+.*)?$"
)
EFFORT_RANK = {"low": 0, "medium": 1, "high": 2, "xhigh": 3, "max": 4}

def _parse_runtime_mapping(relative: str, text: str) -> dict[str, dict[str, str]]:
    _require(text, "Mapping version: `1`", relative, "missing mapping version")
    for section in MAPPING_SECTIONS:
        _require(text, section, relative, f"missing mapping section: {section}")

    rows = {}
    for line in text.splitlines():
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if cells and cells[0] in MAPPING_TIERS:
            if len(cells) != 5:
                raise PackageError(relative, 0, "runtime mapping row must have five cells")
            tier, model, effort, same_tier, higher = cells
            if tier in rows:
                raise PackageError(relative, 0, f"duplicate runtime mapping tier: {tier}")
            if not model:
                raise PackageError(relative, 0, f"missing model for {tier}")
            if effort != MAPPING_EFFORTS[tier]:
                raise PackageError(relative, 0, f"invalid effort for {tier}")
            if not same_tier or not higher:
                raise PackageError(relative, 0, "fallback cells must be non-empty")
            if same_tier.casefold() != "none":
                same_match = FALLBACK_RELATION.fullmatch(same_tier)
                if (
                    same_match is None
                    or f"`{same_match.group(2)}`" != effort
                ):
                    raise PackageError(
                        relative,
                        0,
                        f"invalid same-tier fallback for {tier}",
                    )
            if tier == "Maximum":
                if not higher.casefold().startswith("blocked"):
                    raise PackageError(relative, 0, "Maximum fallback must block")
            elif FALLBACK_RELATION.fullmatch(higher) is None:
                raise PackageError(
                    relative,
                    0,
                    f"higher fallback must declare model and effort for {tier}",
                )
            rows[tier] = {
                "model": model.strip("`"),
                "effort": effort.strip("`"),
                "same_tier": same_tier,
                "higher": higher,
            }
    if tuple(rows) != MAPPING_TIERS:
        raise PackageError(
            relative,
            0,
            "runtime mapping tiers must be exactly Light, Standard, Deep, Maximum",
        )
    for tier_index, tier in enumerate(MAPPING_TIERS[:-1]):
        higher_match = FALLBACK_RELATION.fullmatch(rows[tier]["higher"])
        if higher_match is None:
            raise AssertionError("higher fallback syntax validated above")
        higher_model = higher_match.group(1).casefold()
        higher_effort = higher_match.group(2)
        later_models = {
            rows[later_tier]["model"].casefold()
            for later_tier in MAPPING_TIERS[tier_index + 1:]
        }
        current_model = rows[tier]["model"].casefold()
        current_effort = rows[tier]["effort"]
        targets_later_model = higher_model in later_models
        same_model_effort_promotes = (
            higher_model != current_model
            or EFFORT_RANK[higher_effort] > EFFORT_RANK[current_effort]
        )
        if not targets_later_model or not same_model_effort_promotes:
            raise PackageError(
                relative,
                0,
                f"higher fallback must target a higher tier for {tier}",
            )
    return rows

def _validate_model_routing(files: dict[str, str]) -> None:
    mappings = {
        relative: _parse_runtime_mapping(relative, files[relative])
        for relative in RUNTIME_MAPPING_FILES
    }
    provider_models = {
        row["model"].casefold()
        for mapping in mappings.values()
        for row in mapping.values()
    }
    for relative in NEUTRAL_ROUTING_FILES:
        folded = files[relative].casefold()
        for model in provider_models:
            match = re.search(
                rf"(?<![a-z0-9_.-]){re.escape(model)}(?![a-z0-9_.-])",
                folded,
            )
            if match:
                line = folded.count("\n", 0, match.start()) + 1
                raise PackageError(
                    relative,
                    line,
                    "provider model identifier outside runtime mappings",
                )

    requirements = (
        ("## Evaluation order", "missing routing evaluation order"),
        ("## Topology", "missing routing topology contract"),
        ("below-floor override remains blocked", "missing below-floor override gate"),
        ("## Compatibility", "missing routing compatibility contract"),
    )
    policy = files["references/model-routing.md"]
    for value, reason in requirements:
        _require(policy, value, "references/model-routing.md", reason)
```

Call `_validate_model_routing(files)` from `validate()` after metadata validation and before the existing rubric/workflow checks.

- [ ] **Step 9: Run focused and full tests**

Run:

```sh
python3 -B -m unittest discover -s skills/blueprint-first-delivery/tests -p 'test_validate_skill.py'
sh skills/blueprint-first-delivery/tests/validate-skill.sh
git diff --check
```

Expected: all tests pass; shell exits `0`; `git diff --check` emits no output.

- [ ] **Step 10: Commit Task 1**

```sh
git add skills/blueprint-first-delivery/references/model-routing.md skills/blueprint-first-delivery/references/runtime-mappings/codex.md skills/blueprint-first-delivery/references/runtime-mappings/claude-code.md skills/blueprint-first-delivery/scripts/validate_skill.py skills/blueprint-first-delivery/tests/test_validate_skill.py
git commit -m "feat: add cross-runtime model routing policy"
```

---

### Task 2: Route-Aware Blueprint, Review, and Chunk Gates

**Routing:**
- Tier/floor: Deep because this task changes the public workflow, manifest, review, and gate contracts.
- Topology: ordered after Task 1.
- Codex: `gpt-5.6-sol`, high.
- Claude Code: `opus`, high.
- Evidence: frozen design reduces ambiguity but does not remove the current public-contract risk floor.
- Escalate effort to xhigh only if preserving every hard workflow contract under the 500-word limit remains unresolved after one evidence-backed high-effort attempt.

**Files:**
- Modify: `skills/blueprint-first-delivery/tests/test_validate_skill.py`
- Modify: `skills/blueprint-first-delivery/scripts/validate_skill.py`
- Modify: `skills/blueprint-first-delivery/SKILL.md`
- Modify: `skills/blueprint-first-delivery/references/blueprint-templates.md`
- Modify: `skills/blueprint-first-delivery/references/review-and-gate-checklists.md`

**Interfaces:**
- Consumes: Task 1 routing policy and active runtime mapping contract.
- Produces: mandatory route manifest, relational parallel evidence, independent route review, route-aware start gate, and route traceability.

- [ ] **Step 1: Write the failing desired-state workflow test**

Add these methods inside the existing `ValidateSkillTests` class:

```python
    def test_route_aware_workflow_contract_is_required(self):
        skill = (SKILL_ROOT / "SKILL.md").read_text()
        template = (SKILL_ROOT / "references" / "blueprint-templates.md").read_text()
        checklist = (
            SKILL_ROOT / "references" / "review-and-gate-checklists.md"
        ).read_text()
        for value in (
            "cheapest capable tier",
            "Load only the active runtime mapping",
            "below-floor override",
            "observed execution",
        ):
            self.assertIn(value, skill)
        for value in (
            "schema_version: 1",
            "parallel_group:",
            "mapping_sha256:",
            "    status: pending\n    rationale: null\n    findings:",
            "route_history:",
            "execution_evidence:",
        ):
            self.assertIn(value, template)
        for value in (
            "under-routing and over-routing",
            "Deep or Maximum",
            "observed model and effort",
        ):
            self.assertIn(value, checklist)

```

- [ ] **Step 2: Run the focused tests and verify RED**

Run:

```sh
python3 -B -m unittest discover -s skills/blueprint-first-delivery/tests -p 'test_validate_skill.py'
```

Expected: new assertions fail on `cheapest capable tier`, `schema_version: 1`, and routing-review text.

- [ ] **Step 3: Add the concise routing hook to SKILL.md**

Replace workflow step 2 with:

```markdown
2. Split work into the smallest single-responsibility chunk. Classify it independent, ordered, or integration-only. Apply the [model routing policy](references/model-routing.md) and select the cheapest capable tier. Load only the active runtime mapping. Record versioned floor/topology/dependency evidence, mapping digest, transitions, independent review, override, and observed execution. A below-floor override remains blocked. A consumer is ordered. Parallel work requires relational frozen-contract and non-overlapping file/state ownership evidence.
```

In workflow step 5, replace its first sentence with:

```markdown
5. Implement in dependency order. Before each chunk, prove its route meets the established floor and satisfy its chunk gate using the [gate checklists](references/review-and-gate-checklists.md).
```

Add this blocked-report field:

```markdown
- Model route: `<tier/floor, topology/group, active mapping version/digest, reviewer, transitions, override status, observed execution or blocking evidence>`.
```

Keep every pre-existing validator-required literal and keep total word count below 500.

- [ ] **Step 4: Add the versioned routing template**

Append a `### Model routing` section inside the module blueprint code block. Use this exact field set:

```yaml
routing:
  schema_version: 1
  policy_version: 1
  decision_id: route-profile-repository-001
  chunk_id: profile-repository
  author: planner-agent-id
  decided_at: 2026-08-03T10:30:00Z
  tier: standard
  established_floor: standard
  topology: ordered
  evidence:
    task_shape: bounded implementation
    risk: low
    ambiguity: resolved
    blast_radius: local
    verification_oracle: focused automated tests
  dependency_evidence:
    depends_on: []
    parallel_group: null
    frozen_contracts:
      - id: profile-repository-v1
        version: 1
        reference: docs/blueprints/profile.md#profile-repository-v1
    file_ownership:
      - src/profile/repository/**
    state_ownership:
      - profile persistence writes
    integration_owner: integration-agent-id
    integration_order: 1
  active_runtime_resolution:
    runtime: active-runtime
    mapping_file: references/runtime-mappings/active-runtime.md
    mapping_version: 1
    mapping_sha256: recorded-before-dispatch
    requested_model: recorded-from-active-mapping
    requested_effort: recorded-from-active-mapping
    request_mechanism: model-pinned-subagent
  escalation_triggers:
    - public contract becomes ambiguous
  deescalation_requirements:
    - no current hard-floor trigger
    - governing decisions and contracts are frozen and reviewed
    - objective verification oracle exists
    - no critical review finding remains open
  override:
    requested: null
    rationale: null
    below_floor: false
    gate_status: not_applicable
  reviewer:
    identity: principal-reviewer-id
    independent_from_author: true
    status: pending
    rationale: null
    findings: []
    dispositions: []
    reviewed_at: null
  route_history:
    - from: null
      to: standard
      trigger: initial-classification
      evidence_reference: docs/blueprints/profile.md#routing-evidence
      changed_at: 2026-08-03T10:30:00Z
  execution_evidence:
    status: unverified
    runtime: active-runtime
    runtime_version: null
    observed_model: null
    observed_effort: null
    alias_resolution: null
    metadata_source: null
    observed_at: null
    fallback_chain: []
```

Extend the traceability table with `Route decision/history` and `Observed execution` columns.

- [ ] **Step 5: Add principal route review and route-aware gates**

Add these exact checklist bullets:

```markdown
- Review all chunk routes together; challenge under-routing and over-routing, false parallelism, risk-floor violations, unsupported execution claims, and expensive-tier inheritance.
- Routing author and principal reviewer differ. Every finding has a disposition.
- A below-floor override remains blocked and prevents readiness.
- Parallel groups record member chunk IDs, dependencies, frozen contract versions/references, exclusive file/state ownership, independent verification, integration owner, and integration order.
- Before a chunk starts, resolve only the active runtime mapping and verify its version/digest.
- Deep or Maximum starts only when runtime evidence can verify the requested floor.
- Completion evidence records observed model and effort, metadata source/time, fallback chain, route transitions, and mismatch status.
```

- [ ] **Step 6: Add complete failing removal-mutation coverage**

Add this constant at module scope:

```python
ROUTE_WORKFLOW_REQUIREMENTS = (
("SKILL.md", "cheapest capable tier", "missing cheapest-capable routing rule"),
("SKILL.md", "Load only the active runtime mapping", "missing active-runtime-only rule"),
("SKILL.md", "below-floor override", "missing below-floor override gate"),
("SKILL.md", "observed execution", "missing honest execution evidence"),
("references/blueprint-templates.md", "schema_version: 1", "missing routing schema version"),
("references/blueprint-templates.md", "parallel_group:", "missing relational parallel evidence"),
("references/blueprint-templates.md", "mapping_sha256:", "missing runtime mapping digest"),
("references/blueprint-templates.md", "    status: pending\n    rationale: null\n    findings:", "missing reviewer rationale"),
("references/blueprint-templates.md", "route_history:", "missing route transition history"),
("references/blueprint-templates.md", "execution_evidence:", "missing execution evidence schema"),
("references/review-and-gate-checklists.md", "under-routing and over-routing", "missing routing review challenge"),
("references/review-and-gate-checklists.md", "Deep or Maximum", "missing high-tier execution gate"),
("references/review-and-gate-checklists.md", "observed model and effort", "missing observed route evidence"),
)
```

Add this method inside `ValidateSkillTests`:

```python
    def test_every_route_workflow_requirement_is_enforced(self):
        for relative, required, expected in ROUTE_WORKFLOW_REQUIREMENTS:
            with self.subTest(relative=relative, required=required):
                path = self.skill / relative
                original = path.read_text()
                path.write_text(original.replace(required, "removed", 1))
                try:
                    result = self.run_validator()
                    self.assertEqual(1, result.returncode, result.stderr)
                    self.assertIn(expected, result.stderr)
                finally:
                    path.write_text(original)
```

Run:

```sh
python3 -B -m unittest discover -s skills/blueprint-first-delivery/tests -p 'test_validate_skill.py'
```

Expected: the new removal test fails because `_validate_workflow_contract` does not yet enforce the route requirements. All desired-state assertions already pass.

- [ ] **Step 7: Extend static validator requirements**

Add every tuple from `ROUTE_WORKFLOW_REQUIREMENTS` to the existing `requirements` tuple inside `_validate_workflow_contract`. Keep the exact value and diagnostic text identical.

- [ ] **Step 8: Verify GREEN and regressions**

Run:

```sh
python3 -B -m unittest discover -s skills/blueprint-first-delivery/tests -p 'test_validate_skill.py'
python3 -c 'from pathlib import Path; p=Path("skills/blueprint-first-delivery/SKILL.md"); assert len(p.read_text().split()) < 500'
sh skills/blueprint-first-delivery/tests/validate-skill.sh
git diff --check
```

Expected: every command exits `0`; unit output ends in `OK`.

- [ ] **Step 9: Commit Task 2**

```sh
git add skills/blueprint-first-delivery/SKILL.md skills/blueprint-first-delivery/references/blueprint-templates.md skills/blueprint-first-delivery/references/review-and-gate-checklists.md skills/blueprint-first-delivery/scripts/validate_skill.py skills/blueprint-first-delivery/tests/test_validate_skill.py
git commit -m "feat: require route evidence in delivery gates"
```

---

### Task 3: Model-Routing Pressure and Transition Scenarios

**Routing:**
- Tier: Standard.
- Topology: ordered after Task 2.
- Codex: `gpt-5.6-terra`, medium.
- Claude Code: `sonnet`, medium.
- Evidence: scenario matrix is bounded but requires cross-rule consistency; deterministic static oracle.

**Files:**
- Create: `skills/blueprint-first-delivery/tests/model-routing-pressure-scenarios.md`
- Modify: `skills/blueprint-first-delivery/tests/test_validate_skill.py`
- Modify: `skills/blueprint-first-delivery/scripts/validate_skill.py`

**Interfaces:**
- Consumes: Task 1 policy and Task 2 manifest/gate rules.
- Produces: 26 named scenarios with expected tier/topology/gate outcomes and mutation-enforced coverage.

- [ ] **Step 1: Write only the desired-state scenario-file test**

Add this constant at module scope:

```python
ROUTING_SCENARIO_FILE = "tests/model-routing-pressure-scenarios.md"
```

Add this method inside `ValidateSkillTests`:

```python
    def test_model_routing_pressure_file_exists(self):
        self.assertTrue((SKILL_ROOT / ROUTING_SCENARIO_FILE).is_file())
```

- [ ] **Step 2: Run tests and verify the intended RED**

```sh
python3 -B -m unittest discover -s skills/blueprint-first-delivery/tests -p 'test_validate_skill.py'
```

Expected: only the new desired-state test fails because the scenario file is absent.

- [ ] **Step 3: Create the complete scenario matrix**

Create the file with these exact rows:

```markdown
# Model-routing pressure scenarios

Run each case with a fresh routing decision. Record tier/floor, topology/group evidence, active runtime resolution, reviewer result, and gate status. Each complete row is the oracle.

| ID | Pressure case | Expected result |
| --- | --- | --- |
| R01 | Exact extraction; every Light predicate passes | Light |
| R02 | Bounded normal implementation; no protected risk | Standard |
| R03 | Five-line authorization change | Deep floor |
| R04 | Mechanical edit plus one concurrency trigger | Direct Light-to-Deep floor |
| R05 | Light and Deep signals conflict | Deep wins by precedence |
| R06 | Two independent high-risk triggers | Deep/xhigh only after review evidence |
| R07 | Hardest indivisible critical problem after xhigh failure | Maximum |
| R08 | No active hard trigger; decision and contracts frozen/reviewed; objective oracle exists; no critical finding | Standard de-escalation allowed |
| R09 | Security trigger remains after design freeze | Deep-to-Standard blocked |
| R10 | Two distinct hypotheses retain one criterion/oracle/signature/boundary fingerprint | Repeated-failure Deep trigger |
| R11 | Contract, oracle, signature, or causal boundary changes materially | Failure counter resets |
| R12 | Two files have a producer-consumer dependency | Ordered |
| R13 | Independent chunks have frozen versioned contracts, exclusive ownership, tests, integration owner/order | Parallel group allowed |
| R14 | Parallel candidates hide one dependency | Parallel blocked |
| R15 | Parallel candidates overlap state ownership | Parallel blocked |
| R16 | Parallel contract version is stale | Parallel blocked |
| R17 | Parallel group lacks integration owner or order | Parallel blocked |
| R18 | Requested model unavailable; declared same-tier fallback exists | Same-tier fallback recorded |
| R19 | Same-tier unavailable; higher capable tier exists | Promote and record fallback |
| R20 | Maximum model unavailable | Block or decompose |
| R21 | Deep/Maximum route cannot be pinned and verified | Start gate blocked |
| R22 | Verified claim lacks mapping version/digest, alias resolution, observed model/effort, source, or time | Evidence rejected |
| R23 | Observed model or effort is below floor | Mismatch; gate blocked |
| R24 | User requests below-floor override | Override recorded; readiness blocked |
| R25 | Reviewer equals author or finding remains unresolved | Review gate blocked |
| R26 | Unknown runtime or legacy blueprint resumes | Recommendation-only; add reviewed schema before start |
```

- [ ] **Step 4: Verify the file test turns GREEN**

```sh
python3 -B -m unittest discover -s skills/blueprint-first-delivery/tests -p 'test_validate_skill.py'
```

Expected: all tests pass before semantic enforcement is added.

- [ ] **Step 5: Write exact semantic oracle and removal-mutation tests**

Add a module-level `ROUTING_SCENARIO_ROWS` tuple containing the 26 exact `(id, pressure_case, expected_result)` values from Step 3. Do not shorten or normalize the text.

~~~python
ROUTING_SCENARIO_ROWS = (
    ("R01", "Exact extraction; every Light predicate passes", "Light"),
    ("R02", "Bounded normal implementation; no protected risk", "Standard"),
    ("R03", "Five-line authorization change", "Deep floor"),
    ("R04", "Mechanical edit plus one concurrency trigger", "Direct Light-to-Deep floor"),
    ("R05", "Light and Deep signals conflict", "Deep wins by precedence"),
    ("R06", "Two independent high-risk triggers", "Deep/xhigh only after review evidence"),
    ("R07", "Hardest indivisible critical problem after xhigh failure", "Maximum"),
    ("R08", "No active hard trigger; decision and contracts frozen/reviewed; objective oracle exists; no critical finding", "Standard de-escalation allowed"),
    ("R09", "Security trigger remains after design freeze", "Deep-to-Standard blocked"),
    ("R10", "Two distinct hypotheses retain one criterion/oracle/signature/boundary fingerprint", "Repeated-failure Deep trigger"),
    ("R11", "Contract, oracle, signature, or causal boundary changes materially", "Failure counter resets"),
    ("R12", "Two files have a producer-consumer dependency", "Ordered"),
    ("R13", "Independent chunks have frozen versioned contracts, exclusive ownership, tests, integration owner/order", "Parallel group allowed"),
    ("R14", "Parallel candidates hide one dependency", "Parallel blocked"),
    ("R15", "Parallel candidates overlap state ownership", "Parallel blocked"),
    ("R16", "Parallel contract version is stale", "Parallel blocked"),
    ("R17", "Parallel group lacks integration owner or order", "Parallel blocked"),
    ("R18", "Requested model unavailable; declared same-tier fallback exists", "Same-tier fallback recorded"),
    ("R19", "Same-tier unavailable; higher capable tier exists", "Promote and record fallback"),
    ("R20", "Maximum model unavailable", "Block or decompose"),
    ("R21", "Deep/Maximum route cannot be pinned and verified", "Start gate blocked"),
    ("R22", "Verified claim lacks mapping version/digest, alias resolution, observed model/effort, source, or time", "Evidence rejected"),
    ("R23", "Observed model or effort is below floor", "Mismatch; gate blocked"),
    ("R24", "User requests below-floor override", "Override recorded; readiness blocked"),
    ("R25", "Reviewer equals author or finding remains unresolved", "Review gate blocked"),
    ("R26", "Unknown runtime or legacy blueprint resumes", "Recommendation-only; add reviewed schema before start"),
)
~~~

Add these methods inside `ValidateSkillTests`:

```python
    def test_model_routing_pressure_rows_are_exact(self):
        text = (SKILL_ROOT / ROUTING_SCENARIO_FILE).read_text()
        for scenario_id, pressure_case, expected_result in ROUTING_SCENARIO_ROWS:
            row = f"| {scenario_id} | {pressure_case} | {expected_result} |"
            with self.subTest(scenario_id=scenario_id):
                self.assertIn(row, text)

    def test_every_model_routing_pressure_oracle_is_enforced(self):
        path = self.skill / ROUTING_SCENARIO_FILE
        original = path.read_text()
        for scenario_id, pressure_case, expected_result in ROUTING_SCENARIO_ROWS:
            row = f"| {scenario_id} | {pressure_case} | {expected_result} |"
            with self.subTest(scenario_id=scenario_id):
                path.write_text(original.replace(row, f"| {scenario_id} | removed | removed |", 1))
                try:
                    result = self.run_validator()
                    self.assertEqual(1, result.returncode, result.stderr)
                    self.assertIn(
                        f"routing pressure scenario mismatch: {scenario_id}",
                        result.stderr,
                    )
                finally:
                    path.write_text(original)
```

Run:

```sh
python3 -B -m unittest discover -s skills/blueprint-first-delivery/tests -p 'test_validate_skill.py'
```

Expected: exact desired-state assertions pass; removal mutations fail because the current validator still accepts altered semantic rows.

- [ ] **Step 6: Enforce exact scenario rows**

Add `ROUTING_SCENARIO_FILE = "tests/model-routing-pressure-scenarios.md"` and the same exact `ROUTING_SCENARIO_ROWS` tuple to `validate_skill.py`. Add the scenario file to `REQUIRED_FILES`, then add:

```python
def _validate_routing_scenarios(text: str) -> None:
    for scenario_id, pressure_case, expected_result in ROUTING_SCENARIO_ROWS:
        row = f"| {scenario_id} | {pressure_case} | {expected_result} |"
        _require(
            text,
            row,
            "tests/model-routing-pressure-scenarios.md",
            f"routing pressure scenario mismatch: {scenario_id}",
        )
```

Call `_validate_routing_scenarios(files[ROUTING_SCENARIO_FILE])` from `validate()`.

- [ ] **Step 7: Verify GREEN and commit**

```sh
sh skills/blueprint-first-delivery/tests/validate-skill.sh
git diff --check
```

Expected: shell exits `0`; all exact semantic mutation tests pass.

```sh
git add skills/blueprint-first-delivery/tests/model-routing-pressure-scenarios.md skills/blueprint-first-delivery/tests/test_validate_skill.py skills/blueprint-first-delivery/scripts/validate_skill.py
git commit -m "test: cover model routing pressure cases"
```

---

### Task 4: Codex and Claude Code README

**Routing:**
- Tier: Light requested; Codex fallback Terra/low if Luna is unavailable.
- Topology: ordered after Tasks 1–3.
- Codex: `gpt-5.6-luna`, low; declared fallback `gpt-5.6-terra`, low.
- Claude Code: `haiku`, low; declared fallback `sonnet`, low.
- Evidence: mechanical documentation from frozen mappings; shell grep oracle; low/reversible blast radius.

**Files:**
- Modify: `skills/blueprint-first-delivery/tests/validate-skill.sh`
- Modify: `README.md`

**Interfaces:**
- Consumes: exact runtime mappings and evidence semantics from Tasks 1–3.
- Produces: one public installation/usage contract for both supported runtimes.

- [ ] **Step 1: Add failing README assertions**

Append these checks to `validate-skill.sh`:

```sh
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
```

- [ ] **Step 2: Run wrapper and verify RED**

Run:

```sh
sh skills/blueprint-first-delivery/tests/validate-skill.sh
```

Expected: exit `1` with `missing Claude Code user skill path`.

- [ ] **Step 3: Rewrite README as the dual-runtime entrypoint**

The README must contain:

````markdown
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

## Install for Codex

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
````

Preserve the existing repository-layout, use, validation command, CPython 3.9+, POSIX `sh`, canonical Codex path, and legacy `~/.codex/skills` compatibility guidance.

- [ ] **Step 4: Verify GREEN and commit**

Run:

```sh
sh skills/blueprint-first-delivery/tests/validate-skill.sh
git diff --check
```

Expected: shell exits `0`; all README assertions pass.

Commit:

```sh
git add README.md skills/blueprint-first-delivery/tests/validate-skill.sh
git commit -m "docs: support Codex and Claude Code"
```

---

### Task 5: Integration, Two-Phase Independent Review, and Traceability

**Routing:**
- Implementation verification: Standard, Terra/medium or Sonnet/medium.
- Principal architecture review: Deep, Sol/high or Opus/high.
- QA review: Standard, Terra/medium or Sonnet/medium.
- Topology: ordered after Tasks 1–4; principal and QA reviews may run in parallel only after the same immutable commit is available.
- Escalation: xhigh only if a stable unresolved cross-runtime contract defect survives high review.

**Files:**
- Modify: `docs/superpowers/reports/2026-08-03-cross-runtime-model-routing-traceability.md`
- Modify: `skills/blueprint-first-delivery/tests/test_validate_skill.py`
- Modify only if review finds a defect: files owned by Tasks 1–4, followed by their focused RED/GREEN cycle.

**Interfaces:**
- Consumes: all implementation commits and the approved design.
- Produces: objective final validation, implementation review, final-evidence review, scope-drift proof, requirement traceability, and publishable main.

- [ ] **Step 1: Verify the exact pre-review repository allowlist**

```sh
git status --porcelain
git log --oneline -8
```

Oracle: `git status --porcelain` emits no output. Every implementation commit matches one reviewed task; no uncommitted path is allowed.

- [ ] **Step 2: Run deterministic validation before review**

```sh
sh skills/blueprint-first-delivery/tests/validate-skill.sh
git diff --check
python3 -B skills/blueprint-first-delivery/scripts/validate_skill.py skills/blueprint-first-delivery
python3 -B skills/blueprint-first-delivery/scripts/verify_global_boundary.py docs/superpowers/reports/2026-08-03-cross-runtime-model-routing-global-baseline.json
```

Expected: all commands exit `0`; unit discovery ends in `OK`; validator emits no error; boundary verification prints `PASS (3 paths unchanged)`.

- [ ] **Step 3: Obtain independent implementation reviews**

Capture the full immutable implementation commit:

```sh
git rev-parse HEAD
baseline_path="docs/superpowers/reports/2026-08-03-cross-runtime-model-routing-global-baseline.json"
anchor_path="docs/superpowers/reports/2026-08-03-cross-runtime-model-routing-global-baseline-anchor.json"
traceability_path="docs/superpowers/reports/2026-08-03-cross-runtime-model-routing-traceability.md"
task0_anchor_commit_sha="$(git log --diff-filter=A --format=%H -- "$anchor_path")"
baseline_commit_sha="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["baseline_commit"])' "$anchor_path")"
baseline_blob_oid="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["baseline_blob_oid"])' "$anchor_path")"
git cat-file -e "$task0_anchor_commit_sha^{commit}"
git cat-file -e "$baseline_commit_sha^{commit}"
git merge-base --is-ancestor "$baseline_commit_sha" "$task0_anchor_commit_sha"
git merge-base --is-ancestor "$task0_anchor_commit_sha" HEAD
test "$(git rev-parse "$baseline_commit_sha:$baseline_path")" = "$baseline_blob_oid"
test "$(git rev-parse "HEAD:$baseline_path")" = "$baseline_blob_oid"
git diff --exit-code "$task0_anchor_commit_sha" -- "$baseline_path" "$anchor_path" "$traceability_path"
git log --format=%H "$task0_anchor_commit_sha"..HEAD -- "$baseline_path" "$anchor_path" "$traceability_path"
```

Oracle: the first command emits the implementation SHA; anchor discovery emits exactly one SHA; every status command exits `0`; the final `git log` emits no output. Any Task 1–4 touch—even a later revert—to the baseline, anchor, or initial report blocks review.

Dispatch one principal-engineer reviewer against:

- the approved design;
- provider-neutral boundary;
- active-runtime-only resolution;
- floor/override/parallel/fallback semantics;
- no global mutation.

Dispatch one QA reviewer against:

- all 26 scenario oracles;
- mutation tests;
- README installation assertions;
- exact validation commands;
- regression count and failures.

Both reviewers inspect that same 40-character commit. Neither reviewer edits files. Record the runtime-returned reviewer identities and commit SHA for the report. Any blocker returns to the owning task with a focused failing test before repair, creates a new implementation commit, and restarts Steps 1–3.

- [ ] **Step 4: Write the failing final-evidence test**

Add `import re` with the existing standard-library imports, then add this method inside `ValidateSkillTests`:

```python
    def test_cross_runtime_traceability_report_is_complete(self):
        path = (
            REPO_ROOT
            / "docs"
            / "superpowers"
            / "reports"
            / "2026-08-03-cross-runtime-model-routing-traceability.md"
        )
        text = path.read_text()
        for required in (
            "## Requirement evidence",
            "## Validation",
            "## Routing history",
            "## Global mutation proof",
            "## Final residual risk",
            "Principal review: PASS",
            "QA review: PASS",
            "Global boundary verifier exit status: 0",
            "Global boundary states equal: yes",
            "External Claude Code execution: not run; not claimed",
        ):
            with self.subTest(required=required):
                self.assertIn(required, text)
        self.assertNotIn("PASS required", text)
        self.assertNotIn("pending evidence", text)
        self.assertIn(
            "Package validation exit status: 0",
            text,
        )
        self.assertIn("Git diff check exit status: 0", text)
        self.assertIn("Standalone validator exit status: 0", text)
        self.assertIn("Unit-test oracle: OK", text)
        principal = re.search(
            r"Principal review: PASS by ([A-Za-z0-9_.@/-]+) "
            r"at commit ([0-9a-f]{40})",
            text,
        )
        qa = re.search(
            r"QA review: PASS by ([A-Za-z0-9_.@/-]+) "
            r"at commit ([0-9a-f]{40})",
            text,
        )
        reviewed = re.search(
            r"Reviewed implementation commit: ([0-9a-f]{40})",
            text,
        )
        self.assertIsNotNone(principal)
        self.assertIsNotNone(qa)
        self.assertIsNotNone(reviewed)
        self.assertNotEqual(principal.group(1), qa.group(1))
        self.assertEqual(principal.group(2), qa.group(2))
        self.assertEqual(principal.group(2), reviewed.group(1))
        count = re.search(r"Final test count: ([0-9]+)", text)
        self.assertIsNotNone(count)
        self.assertGreater(int(count.group(1)), 53)
        for task_number in range(6):
            self.assertIn(f"| Task {task_number} |", text)

        rows = re.findall(
            r"^\| (`/Users/sandeepdhami/[^|]+`) "
            r"\| (`(?:[0-9a-f]{64}|absent)`) "
            r"\| (`(?:[0-9a-f]{64}|absent)`) \| yes \|$",
            text,
            re.MULTILINE,
        )
        self.assertEqual(3, len(rows))
        expected_paths = {
            "`/Users/sandeepdhami/.claude/CLAUDE.md`",
            "`/Users/sandeepdhami/.codex/AGENTS.md`",
            "`/Users/sandeepdhami/.codex/config.toml`",
        }
        self.assertEqual(expected_paths, {path for path, _, _ in rows})
        for _, before, after in rows:
            self.assertEqual(before, after)

        baseline_path = (
            REPO_ROOT
            / "docs"
            / "superpowers"
            / "reports"
            / "2026-08-03-cross-runtime-model-routing-global-baseline.json"
        )
        baseline = json.loads(baseline_path.read_text())
        expected_baseline = {
            row["path"]: row["state"]
            for row in baseline["paths"]
        }
        report_baseline = {
            path.strip("`"): before.strip("`")
            for path, before, _ in rows
        }
        self.assertEqual(expected_baseline, report_baseline)

        anchor_path = (
            REPO_ROOT
            / "docs"
            / "superpowers"
            / "reports"
            / "2026-08-03-cross-runtime-model-routing-global-baseline-anchor.json"
        )
        anchor = json.loads(anchor_path.read_text())
        task0_anchor = re.search(
            r"Task 0 anchor commit: ([0-9a-f]{40})",
            text,
        )
        baseline_commit = re.search(
            r"Baseline commit: ([0-9a-f]{40})",
            text,
        )
        baseline_blob = re.search(
            r"Baseline blob OID: ([0-9a-f]{40,64})",
            text,
        )
        self.assertIsNotNone(task0_anchor)
        self.assertIsNotNone(baseline_commit)
        self.assertIsNotNone(baseline_blob)
        self.assertEqual(anchor["baseline_commit"], baseline_commit.group(1))
        self.assertEqual(anchor["baseline_blob_oid"], baseline_blob.group(1))
```

Run:

```sh
python3 -B -m unittest discover -s skills/blueprint-first-delivery/tests -p 'test_validate_skill.py'
```

Expected: the new test fails because the Task 0 report intentionally lacks final review, validation, routing-history, post-state, and residual-risk evidence.

Record the exact integer from unittest's `Ran N tests` output. This is the count inserted in Step 5; do not infer or estimate it.

- [ ] **Step 5: Collect absent-aware post-state and complete the report**

Run the same read-only loop used in Task 0:

```sh
for target in /Users/sandeepdhami/.claude/CLAUDE.md /Users/sandeepdhami/.codex/AGENTS.md /Users/sandeepdhami/.codex/config.toml
do
  if test -f "$target"
  then
    shasum -a 256 "$target"
  else
    printf 'absent  %s\n' "$target"
  fi
done
```

For each exact path, compare the emitted post-state value with its already committed pre-state value. A mismatch blocks completion. Use `apply_patch` to preserve Task 0 content and append these sections with actual outputs and reviewer identities.

Capture the immutable Task 0 anchor, baseline commit, and baseline blob:

```sh
anchor_path="docs/superpowers/reports/2026-08-03-cross-runtime-model-routing-global-baseline-anchor.json"
task0_anchor_commit_sha="$(git log --diff-filter=A --format=%H -- "$anchor_path")"
baseline_commit_sha="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["baseline_commit"])' "$anchor_path")"
baseline_blob_oid="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["baseline_blob_oid"])' "$anchor_path")"
printf '%s\n%s\n%s\n' "$task0_anchor_commit_sha" "$baseline_commit_sha" "$baseline_blob_oid"
python3 -B skills/blueprint-first-delivery/scripts/verify_global_boundary.py docs/superpowers/reports/2026-08-03-cross-runtime-model-routing-global-baseline.json
```

The first output block has exactly three non-empty IDs in anchor/commit/blob order. The verifier must exit `0` and print `PASS (3 paths unchanged)`.

Use the structure below. Between its `## Requirement evidence` heading and table, add these exact evidence lines:

- `Principal review: PASS by`, followed by the actual principal reviewer identity, `at commit`, and the full Step 3 SHA.
- `QA review: PASS by`, followed by the actual QA reviewer identity, `at commit`, and the same full Step 3 SHA.
- `Reviewed implementation commit:`, followed by that same full SHA.
- `Task 0 anchor commit:`, followed by the first captured ID.
- `Baseline commit:`, followed by the second captured ID.
- `Baseline blob OID:`, followed by the third captured ID.

The remainder is:

```markdown
## Requirement evidence

| Requirement | Implementation files | Automated evidence | Independent review | Status / residual risk |
| --- | --- | --- | --- | --- |
| Provider-neutral cheapest-capable routing | model-routing.md, SKILL.md | validator mutation tests | principal PASS | PASS |
| Active Codex and Claude Code mappings | runtime mapping references | generic parser/mutation tests | principal PASS | PASS |
| Relational safe parallelism | blueprint template and gate checklist | R12–R17 exact oracles | principal and QA PASS | PASS |
| Honest execution and fallback | policy and runtime mappings | R18–R23 exact oracles | principal and QA PASS | PASS |
| Below-floor override block | policy and gate checklist | R24 exact oracle | principal PASS | PASS |
| Legacy/unknown-runtime behavior | policy and pressure scenarios | R26 exact oracle | QA PASS | PASS |
| Dual-runtime documentation | README.md | POSIX wrapper assertions | QA PASS | PASS |

## Validation

Package validation exit status: 0

Git diff check exit status: 0

Standalone validator exit status: 0

Unit-test oracle: OK

Global boundary verifier exit status: 0

Add `Final test count:` followed by the exact integer emitted by the final test run. The integer must be greater than the 53-test baseline.

## Routing history

| Task | Requested route | Observed route evidence | Transition/fallback | Result |
| --- | --- | --- | --- | --- |

Add exactly six rows beginning `| Task 0 |` through `| Task 5 |`. Each row records requested tier/model/effort, runtime-verifiable actual route or honest unverified limitation, escalation/de-escalation, fallback, and result.

## Global mutation proof

| Path | Before | After | Equal |
| --- | --- | --- | --- |

Add exactly three rows. Wrap path and both hash-or-absent values in backticks. Use `yes` only when before equals after.

Global boundary states equal: yes

## Final residual risk

Local tests validate package contracts and documented pressure oracles. Boundary-state equality does not prove the global files were never transiently modified; the authorized write scope and tool log provide separate evidence.

External Claude Code execution: not run; not claimed
```

Do not write PASS unless both independent reviewers passed the same immutable implementation commit.

- [ ] **Step 6: Verify final evidence turns GREEN**

```sh
python3 -B -m unittest discover -s skills/blueprint-first-delivery/tests -p 'test_*.py'
sh skills/blueprint-first-delivery/tests/validate-skill.sh
python3 -B skills/blueprint-first-delivery/scripts/verify_global_boundary.py docs/superpowers/reports/2026-08-03-cross-runtime-model-routing-global-baseline.json
git diff --check
```

Expected: unittest reports `OK` and the same exact `Ran N tests` count recorded in the report; all wrapper tests pass; the report test proves reviewer identity/commit equality and three syntactically valid equal boundary values; `git diff --check` emits no output. If the count differs, patch the report with the observed count and repeat this step.

- [ ] **Step 7: Commit final evidence**

```sh
git add docs/superpowers/reports/2026-08-03-cross-runtime-model-routing-traceability.md skills/blueprint-first-delivery/tests/test_validate_skill.py
git commit -m "docs: record model routing validation"
```

- [ ] **Step 8: Review the immutable final-evidence commit**

Extract the report's immutable SHAs and prove the baseline precedes the reviewed implementation commit, while every post-review change stays inside the two evidence-owned files:

```sh
reviewed_implementation_sha="$(awk '/^Reviewed implementation commit: / {print $4}' docs/superpowers/reports/2026-08-03-cross-runtime-model-routing-traceability.md)"
task0_anchor_commit_sha="$(awk '/^Task 0 anchor commit: / {print $5}' docs/superpowers/reports/2026-08-03-cross-runtime-model-routing-traceability.md)"
baseline_commit_sha="$(awk '/^Baseline commit: / {print $3}' docs/superpowers/reports/2026-08-03-cross-runtime-model-routing-traceability.md)"
baseline_blob_oid="$(awk '/^Baseline blob OID: / {print $4}' docs/superpowers/reports/2026-08-03-cross-runtime-model-routing-traceability.md)"
baseline_path="docs/superpowers/reports/2026-08-03-cross-runtime-model-routing-global-baseline.json"
anchor_path="docs/superpowers/reports/2026-08-03-cross-runtime-model-routing-global-baseline-anchor.json"
traceability_path="docs/superpowers/reports/2026-08-03-cross-runtime-model-routing-traceability.md"
git cat-file -e "$reviewed_implementation_sha^{commit}"
git cat-file -e "$task0_anchor_commit_sha^{commit}"
git cat-file -e "$baseline_commit_sha^{commit}"
test "$(git log --diff-filter=A --format=%H -- "$anchor_path")" = "$task0_anchor_commit_sha"
test "$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["baseline_commit"])' "$anchor_path")" = "$baseline_commit_sha"
test "$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["baseline_blob_oid"])' "$anchor_path")" = "$baseline_blob_oid"
test "$(git rev-parse "$baseline_commit_sha:$baseline_path")" = "$baseline_blob_oid"
test "$(git rev-parse "HEAD:$baseline_path")" = "$baseline_blob_oid"
git merge-base --is-ancestor "$baseline_commit_sha" "$task0_anchor_commit_sha"
git merge-base --is-ancestor "$task0_anchor_commit_sha" "$reviewed_implementation_sha"
git merge-base --is-ancestor "$reviewed_implementation_sha" HEAD
git diff --exit-code "$task0_anchor_commit_sha" -- "$baseline_path" "$anchor_path"
git log --format=%H "$task0_anchor_commit_sha".."$reviewed_implementation_sha" -- "$baseline_path" "$anchor_path" "$traceability_path"
git diff --name-only "$reviewed_implementation_sha"..HEAD
git status --porcelain
```

Oracle:

- all recorded commit IDs are valid and the report matches the anchor JSON;
- the anchor file's unique first-add commit equals the recorded Task 0 anchor;
- both the baseline commit and current baseline path resolve to the recorded blob OID;
- baseline commit → Task 0 anchor → reviewed implementation commit → `HEAD` ancestry holds;
- baseline and anchor content remain identical to Task 0, and the scoped `git log` emits no pre-review touch to baseline, anchor, or traceability report;
- `git diff --name-only "$reviewed_implementation_sha"..HEAD` emits exactly:
  - `docs/superpowers/reports/2026-08-03-cross-runtime-model-routing-traceability.md`
  - `skills/blueprint-first-delivery/tests/test_validate_skill.py`
- `git status --porcelain` emits no output.

Dispatch the principal and QA reviewers again. Both independently inspect immutable `HEAD`, the complete evidence-only range from the recorded implementation SHA through `HEAD`, final validation output, reviewer identities/SHAs, exact count, committed baseline binding, live boundary-verifier result, and boundary rows. Neither edits files. Push remains blocked unless both pass.

If an evidence-only defect is repaired, commit it and repeat both final reviews against the new immutable `HEAD`. If any Task 1–4 implementation file changes after the recorded implementation SHA, discard the stale review claim from the report and restart Steps 1–8 with a new implementation review commit. Make no change after both final reviewers pass.

- [ ] **Step 9: Final clean verification and publish**

```sh
sh skills/blueprint-first-delivery/tests/validate-skill.sh
python3 -B skills/blueprint-first-delivery/scripts/verify_global_boundary.py docs/superpowers/reports/2026-08-03-cross-runtime-model-routing-global-baseline.json
git diff --check
git status --short --branch
git push origin main
```

Expected: tests pass; no unstaged/staged changes; branch publishes all approved commits to `origin/main`.
