# Adaptive Evidence-First Delivery Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a cost-aware Direct/Lite/Full work router and evidence-first proof system to the shared Codex and Claude Code skill without weakening existing outcome-backward or provider-neutral model-routing guarantees.

**Architecture:** Keep work-route policy provider-neutral and separate from model tiers. Add a standard-library evidence-manifest validator for actual proof/traceability artifacts, while the existing package validator continues to enforce required skill text, templates, examples, and pressure scenarios. Full work retains the outcome-backward flow; Direct and Lite use bounded receipts/cards rather than full blueprints.

**Tech Stack:** Markdown, JSON, Python 3.9+ standard library, POSIX `sh`, `unittest`.

## Global Constraints

- Work on `main`; user explicitly declined a worktree.
- Keep `SKILL.md` under 500 words and move detailed rules to `references/`.
- Do not add UI, HTML, a viewer, an extension, or GitHub Pages artifacts.
- Do not place provider model identifiers in shared policy; retain them only in runtime mappings.
- Preserve the existing `>=95/100` rubric and its wording; add non-compensable proof gates outside its additive score.
- Direct work still requires a deterministic oracle and changed-scope review.
- Full work preserves outcome-backward/forward reconciliation before module freeze.
- Never claim local validation proves an external Claude Code run.

## File Structure

- Create: `skills/blueprint-first-delivery/scripts/validate_evidence_manifest.py` — validate Direct/Lite/Full evidence artifacts and detect supplied baseline drift.
- Create: `skills/blueprint-first-delivery/tests/test_validate_evidence_manifest.py` — isolated TDD coverage for the manifest validator.
- Create: `skills/blueprint-first-delivery/references/adaptive-evidence-first.md` — canonical Direct/Lite/Full routing, proof, state, drift, Agent Brain, and cost policy.
- Create: `skills/blueprint-first-delivery/references/evidence-manifest.md` — JSON schema explanation, commands, and Direct/Lite/Full examples.
- Create: `skills/blueprint-first-delivery/references/examples/direct-task-proven.json`, `lite-task-proven-handoff.json`, and `full-plan-frozen.json` — valid reusable artifacts for the three routes.
- Create: `skills/blueprint-first-delivery/tests/adaptive-evidence-pressure-scenarios.md` — immutable pressure-oracle rows for the new policy.
- Modify: `skills/blueprint-first-delivery/scripts/validate_skill.py` — require new files and validate their canonical policy/scenario content.
- Modify: `skills/blueprint-first-delivery/tests/test_validate_skill.py` — mutation coverage for every new static contract.
- Modify: `skills/blueprint-first-delivery/SKILL.md` — route before planning; use Full-only outcome-backward/readiness workflow; expose state.
- Modify: `skills/blueprint-first-delivery/references/blueprint-templates.md` — Direct receipt, Lite card, Full proof matrix, state record, baseline, early-integration and traceability templates.
- Modify: `skills/blueprint-first-delivery/references/outcome-backward-planning.md` — make it Full-route guidance and preserve compatibility.
- Modify: `skills/blueprint-first-delivery/references/readiness-rubric.md` — retain score rows; add non-compensable proof preconditions.
- Modify: `skills/blueprint-first-delivery/references/review-and-gate-checklists.md` — route, proof, lifecycle, calibration, drift, and early-integration gates.
- Modify: `skills/blueprint-first-delivery/agents/openai.yaml` and `README.md` — describe adaptive use without breaking shared runtime mapping isolation.

---

### Task 1: Add the evidence-manifest validator with failing tests first

**Files:**
- Create: `skills/blueprint-first-delivery/tests/test_validate_evidence_manifest.py`
- Create: `skills/blueprint-first-delivery/scripts/validate_evidence_manifest.py`

**Interfaces:**
- Consumes: a JSON manifest path and optional `--workspace <path>`.
- Produces: exit `0` for a valid artifact, exit `1` for a policy/schema/drift failure, exit `2` for usage/runtime errors; diagnostics are `path:line: reason`.

- [ ] **Step 1: Write failing tests for route-specific required fields.**

```python
def test_direct_requires_deterministic_oracle(self):
    manifest = direct_manifest()
    del manifest["direct_receipt"]["oracle_id"]
    self.assert_invalid(manifest, "Direct receipt missing oracle_id")

def test_full_rejects_unproven_critical_claim_at_delivery_ready(self):
    manifest = full_manifest(state="DELIVERY_READY")
    manifest["proof_matrix"][0]["status"] = "PROOF_REQUIRED"
    self.assert_invalid(manifest, "critical proof is not PROVEN")
```

- [ ] **Step 2: Run tests to verify RED.**

Run: `python3 -m unittest skills/blueprint-first-delivery/tests/test_validate_evidence_manifest.py -v`  
Expected: `ModuleNotFoundError`, missing validator file, or failing assertions because no validator exists.

- [ ] **Step 3: Add the minimal validator contract.**

Implement a dependency-free JSON CLI with this manifest shape:

```json
{
  "schema_version": 1,
  "task_id": "profile-save",
  "route": "full",
  "state": "PLAN_FROZEN",
  "route_facts": {"modules": 2, "protected_risks": ["persistence"]},
  "baseline": {"git_ref": "<commit-or-tree>", "contract_digests": [], "owned_paths": [], "evidence_digest": "<sha256>"},
  "proof_matrix": [{"requirement_id": "AC-1", "claim_id": "INV-1", "criticality": "critical", "owner": "repository", "status": "PROOF_REQUIRED", "task_id": "repository-save", "oracle_id": "T-1", "expected_result": "save is atomic", "evidence_ref": "tests/test_repository.py::test_save", "baseline_ref": "baseline", "integration_counterpart": "profile-presenter"}],
  "traceability": [{"requirement_id": "AC-1", "claim_id": "INV-1", "task_id": "repository-save", "oracle_id": "T-1", "evidence_ref": "tests/test_repository.py::test_save", "integration_result": "pending"}],
  "agent_brain": {"required": true, "source_refs": ["docs/blueprints/profile.md#INV-1"]},
  "integration": {"required": true, "early_vertical_proof": "IT-1", "final_gate": "pending"}
}
```

Validate exact route values; Direct receipt fields; Lite-card fields; Full proof/traceability links; lifecycle status rules; required Agent Brain source refs for Full and Lite handoff; and the early-integration requirement for cross-module Full work. Accept `PROOF_REQUIRED` only at `ARCHITECTURE_APPROVED` or `PLAN_FROZEN` with a task and oracle. Reject `ASSUMPTION`, `BLOCKED`, or `STALE` on critical Full rows after architecture approval.

- [ ] **Step 3a: Add valid reusable manifest examples.**

Create `references/examples/direct-task-proven.json`, `lite-task-proven-handoff.json`, and `full-plan-frozen.json` from the same schema. The Lite handoff example must have `agent_brain.required: true` and non-empty `source_refs`; the Full example must contain a `PROOF_REQUIRED` critical row owned by a named future task and a named early vertical proof.

- [ ] **Step 4: Add baseline-drift verification tests, then implementation.**

```python
def test_workspace_hash_mismatch_marks_evidence_stale(self):
    workspace = self.make_workspace({"src/profile.txt": "changed"})
    manifest = full_manifest_with_baseline("src/profile.txt", sha256("old"))
    self.assert_invalid(manifest, "baseline drift: src/profile.txt", workspace)
```

`--workspace` must compare manifest-recorded SHA-256 file digests only for declared baseline paths. A mismatch exits `1`; the diagnostic directs the user to mark affected rows `STALE` and re-approve. The validator must not run arbitrary test commands or claim external runtime execution.

- [ ] **Step 5: Run RED then GREEN verification.**

Run: `python3 -m unittest skills/blueprint-first-delivery/tests/test_validate_evidence_manifest.py -v`  
Expected after implementation: all Direct, Lite, Full, lifecycle, Agent Brain, early-integration, cross-reference, and drift tests pass.

- [ ] **Step 6: Commit.**

```bash
git add skills/blueprint-first-delivery/scripts/validate_evidence_manifest.py \
  skills/blueprint-first-delivery/tests/test_validate_evidence_manifest.py
git commit -m "feat: validate evidence manifests"
```

### Task 2: Lock the adaptive static policy with pressure scenarios and mutation tests

**Files:**
- Create: `skills/blueprint-first-delivery/tests/adaptive-evidence-pressure-scenarios.md`
- Modify: `skills/blueprint-first-delivery/scripts/validate_skill.py`
- Modify: `skills/blueprint-first-delivery/tests/test_validate_skill.py`

**Interfaces:**
- Consumes: canonical policy phrases and scenario rows.
- Produces: `validate_skill.py` rejects a package when a required adaptive rule, required file, or pressure oracle is removed.

- [ ] **Step 1: Write failing package tests and scenario rows.**

Add `ADAPTIVE_EVIDENCE_SCENARIO_ROWS` to the test and validator with these exact oracle cases:

```text
AE01 exact local behavior + focused oracle + one owner → Direct
AE02 bounded behavior without Direct predicates and no hard trigger → Blueprint Lite
AE03 “small” schema/persistence/concurrency/security/cross-module task → Full Blueprint
AE04 98/100 with a critical PROOF_REQUIRED row at task completion → blocked
AE05 changed baseline digest for a declared path → affected evidence STALE
AE06 Full cross-module work lacks early vertical proof → plan/integration blocked
AE07 Full or Lite handoff Agent Brain entry lacks source/evidence reference → blocked
AE08 provider model name appears in shared adaptive policy → package rejected
```

Add mutation tests that remove each row, each policy requirement, each state value, and each manifest-validator required file. The initial package test must fail because the scenario file and constants do not exist.

- [ ] **Step 2: Run the package test to verify RED.**

Run: `python3 -m unittest skills/blueprint-first-delivery/tests/test_validate_skill.py -v`  
Expected: failures naming missing adaptive scenario, policy, manifest-validator, and mutation requirements.

- [ ] **Step 3: Extend `validate_skill.py` minimally.**

Add required-file constants for the new scripts, references, test module, and pressure file. Add validation functions that:

```python
def _validate_adaptive_evidence_scenarios(text: str) -> None: ...
def _validate_adaptive_evidence_reference(files: dict[str, str]) -> None: ...
def _validate_adaptive_evidence_workflow(files: dict[str, str]) -> None: ...
```

Use exact canonical requirements rather than broad keyword matching. Extend `NEUTRAL_ROUTING_FILES` to all new provider-neutral references so a Codex or Claude model identifier cannot leak into them.

- [ ] **Step 4: Run GREEN verification.**

Run: `python3 -m unittest skills/blueprint-first-delivery/tests/test_validate_skill.py -v`  
Expected: existing coverage plus every adaptive mutation test passes.

- [ ] **Step 5: Commit.**

```bash
git add skills/blueprint-first-delivery/tests/adaptive-evidence-pressure-scenarios.md \
  skills/blueprint-first-delivery/scripts/validate_skill.py \
  skills/blueprint-first-delivery/tests/test_validate_skill.py
git commit -m "test: lock adaptive evidence policy"
```

### Task 3: Implement the canonical policy, templates, and gates

**Files:**
- Create: `skills/blueprint-first-delivery/references/adaptive-evidence-first.md`
- Create: `skills/blueprint-first-delivery/references/evidence-manifest.md`
- Modify: `skills/blueprint-first-delivery/SKILL.md`
- Modify: `skills/blueprint-first-delivery/references/blueprint-templates.md`
- Modify: `skills/blueprint-first-delivery/references/outcome-backward-planning.md`
- Modify: `skills/blueprint-first-delivery/references/readiness-rubric.md`
- Modify: `skills/blueprint-first-delivery/references/review-and-gate-checklists.md`

**Interfaces:**
- Consumes: route facts, proof matrix, baseline, Agent Brain source refs, and integration ownership.
- Produces: Direct receipt, Lite task card, Full plan/state/proof matrix, evidence manifest, and final traceability report.

- [ ] **Step 1: Add static test assertions that require the new workflow.**

Examples to add before documentation changes:

```python
self.assertIn("## Adaptive work router", adaptive_reference)
self.assertIn("`Direct` is allowed only when all predicates pass", adaptive_reference)
self.assertIn("No critical row may be `ASSUMPTION`", adaptive_reference)
self.assertIn("TRIAGED → ARCHITECTURE_APPROVED", adaptive_reference)
self.assertIn("early vertical proof", checklist)
self.assertIn("Agent Brain is mandatory for Full", adaptive_reference)
```

- [ ] **Step 2: Run tests to verify RED.**

Run: `python3 -m unittest skills/blueprint-first-delivery/tests/test_validate_skill.py -v`  
Expected: adaptive reference/workflow mutations fail because canonical text and templates are absent.

- [ ] **Step 3: Add provider-neutral canonical references.**

`adaptive-evidence-first.md` must define Direct predicates, Full hard triggers, Lite fields, route promotion, proof states, lifecycle states, reviewer-calibration fields, baseline/drift semantics, Agent Brain applicability, early vertical integration, and cost telemetry. `evidence-manifest.md` must document the JSON schema, `validate_evidence_manifest.py` commands, and one valid example for every route.

- [ ] **Step 4: Update compact skill and templates.**

Keep the main skill below 500 words. Start with route selection, send detailed rules to the canonical reference, and run the existing outcome-backward flow only for Full. Add these template sections:

```text
Direct receipt: outcome / owner / oracle / changed scope / result / rollback
Lite card: outcome / boundary / invariant / owner / scope / failure / oracle / ownership / route reason
Full: proof matrix / approval state / baseline / reviewer findings / early vertical proof
Traceability: requirement_id → claim_id → task_id → oracle_id → evidence_ref → integration_result
```

Keep the existing eight rubric rows and 100-point total unchanged. Add the pre-score proof-matrix rule: a score cannot offset a missing critical oracle, owner, baseline, trace link, or required proof state.

- [ ] **Step 5: Update outcome/backward and gate references.**

State that outcome-backward/forward reconciliation is Full-only; completed legacy work stays historical; affected new approval needs the adaptive risk audit. Require explicit state transitions, reviewer finding disposition, source-linked Agent Brain records for Full/handoff Lite, and early vertical proof before the final integration gate.

- [ ] **Step 6: Run GREEN verification.**

Run: `python3 -m unittest skills/blueprint-first-delivery/tests/test_validate_skill.py -v`  
Expected: all static policy and mutation tests pass; `SKILL.md` remains below 500 words.

- [ ] **Step 7: Commit.**

```bash
git add skills/blueprint-first-delivery/SKILL.md \
  skills/blueprint-first-delivery/references
git commit -m "feat: add adaptive evidence-first workflow"
```

### Task 4: Update user documentation and runtime metadata

**Files:**
- Modify: `README.md`
- Modify: `skills/blueprint-first-delivery/agents/openai.yaml`
- Modify: `skills/blueprint-first-delivery/tests/test_validate_skill.py`

**Interfaces:**
- Consumes: provider-neutral route policy plus existing Codex/Claude runtime mappings.
- Produces: a user-facing explanation of when the skill skips heavy planning, when it escalates, how evidence is checked, and how to run validation.

- [ ] **Step 1: Write documentation assertions first.**

Add tests that require README phrases for `Direct`, `Blueprint Lite`, `Full Blueprint`, “readiness is process evidence,” source-linked Agent Brain, early vertical integration, and the evidence-manifest command. Require `openai.yaml` default prompt to name `$blueprint-first-delivery` and adaptive routing without inserting provider identifiers.

- [ ] **Step 2: Run tests to verify RED.**

Run: `python3 -m unittest skills/blueprint-first-delivery/tests/test_validate_skill.py -v`  
Expected: README/agent-metadata contract assertions fail.

- [ ] **Step 3: Update README and metadata.**

Add a route-selection table, a short route-versus-model-tier explanation, a Full-route evidence flow, manifest-validation command, limitations, and cost-measurement guidance. Explain that Agent Brain is navigation not proof. Retain the current install instructions and runtime mapping table. Keep provider model values confined to the existing mapping references/table.

- [ ] **Step 4: Run GREEN verification.**

Run: `python3 -m unittest skills/blueprint-first-delivery/tests/test_validate_skill.py -v`  
Expected: all documentation and metadata checks pass.

- [ ] **Step 5: Commit.**

```bash
git add README.md skills/blueprint-first-delivery/agents/openai.yaml \
  skills/blueprint-first-delivery/tests/test_validate_skill.py
git commit -m "docs: explain adaptive evidence-first delivery"
```

### Task 5: Run complete validation, inspect evidence, and publish

**Files:**
- Modify: `docs/superpowers/reports/2026-08-08-adaptive-evidence-first-delivery-traceability.md`

**Interfaces:**
- Consumes: implemented policy, manifest validator, package validator, test results, and Git baseline.
- Produces: a requirement-by-requirement final traceability record with honest residual risks.

- [ ] **Step 1: Write the failing traceability completeness check.**

Add a package test requiring the report to map every approved-design acceptance criterion to policy location, test/oracle, observed command result, and residual risk. It must distinguish package validation from external Codex/Claude execution.

- [ ] **Step 2: Run RED.**

Run: `python3 -m unittest skills/blueprint-first-delivery/tests/test_validate_skill.py -v`  
Expected: missing traceability-report assertion failure.

- [ ] **Step 3: Produce evidence and report.**

Run all of:

```bash
python3 -m unittest discover -s skills/blueprint-first-delivery/tests -p 'test_*.py'
sh skills/blueprint-first-delivery/tests/validate-skill.sh
python3 skills/blueprint-first-delivery/scripts/validate_evidence_manifest.py \
  skills/blueprint-first-delivery/references/examples/full-plan-frozen.json
git diff --check
```

Record exact exit status, test count, baseline commit, critical requirements, pressure scenarios, manifest validation, and residual risks. Do not state that a Claude Code run occurred unless observed runtime metadata proves it.

- [ ] **Step 4: Run GREEN and inspect the final diff.**

Run: `git status --short && git diff --check && git diff --stat d2c97658fd095d969fdeee52a62ffceea503f5b0..HEAD`  
Expected: clean format; all expected files accounted for; no unrelated changes.

- [ ] **Step 5: Commit and push after verification.**

```bash
git add docs/superpowers/reports/2026-08-08-adaptive-evidence-first-delivery-traceability.md \
  skills/blueprint-first-delivery/tests/test_validate_skill.py
git commit -m "test: verify adaptive evidence-first delivery"
git push origin main
```

## Plan Self-Review

- Spec coverage: tasks cover adaptive routing, evidence proofs, non-compensable readiness, lifecycle, early integration, immutable traceability, Agent Brain, cost-aware tiers, both runtimes, documentation, examples, tests, validation, and publication.
- Completeness scan: every task has concrete files, commands, interfaces, and expected test behavior.
- Boundary check: the work-route policy, manifest validator, static package validation, templates/gates, documentation, and final evidence are separate testable deliverables. Existing model mappings are preserved rather than rebuilt.
