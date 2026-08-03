import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock


SKILL_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = SKILL_ROOT / "scripts" / "validate_skill.py"
REPO_ROOT = SKILL_ROOT.parents[1]
ROUTING_SCENARIO_FILE = "tests/model-routing-pressure-scenarios.md"
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
OUTCOME_BACKWARD_SCENARIO_FILE = "tests/outcome-backward-pressure-scenarios.md"
OUTCOME_BACKWARD_SCENARIO_ROWS = (
    ("OB01", "A completion date is offered without an observable end state", "Block; ask for outcome and acceptance evidence"),
    ("OB02", "Architecture evidence cannot prove a required contract", "Module freeze blocked; readiness unscorable"),
    ("OB03", "Backward and forward paths disagree about a producer", "Report conflict; rerun affected scope only"),
    ("OB04", "A user-owned source-of-truth decision is ambiguous", "Wait; no automatic rerun"),
    ("OB05", "Evidence contradicts one recorded condition", "Notify; preserve valid findings; allow one scoped rerun"),
    ("OB06", "The same unresolved trigger recurs without new evidence", "Hard block; no third pass"),
    ("OB07", "Proposed modules exist before reconciliation passes", "Modules provisional; no chunking or scoring"),
    ("OB08", "Outcome-backward gate passes with independent review", "Freeze modules; then chunk and route work"),
)
ROUTING_REQUIRED_FILES = (
    "references/model-routing.md",
    "references/runtime-mappings/codex.md",
    "references/runtime-mappings/claude-code.md",
)
NEW_PACKAGE_REQUIRED_FILES = ROUTING_REQUIRED_FILES + (
    "scripts/verify_global_boundary.py",
    "tests/test_verify_global_boundary.py",
)
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
OUTCOME_BACKWARD_REFERENCE_REQUIREMENTS = (
    ("references/outcome-backward-planning.md", "## Outcome contract", "missing observable-outcome contract"),
    ("references/outcome-backward-planning.md", "## Backward prerequisite pass", "missing backward-pass contract"),
    ("references/outcome-backward-planning.md", "## Prerequisite and blocker register", "missing blocker register"),
    ("references/outcome-backward-planning.md", "user-owned, evidence-owned, external, technical, contract, security, integration", "missing blocker classifications"),
    ("references/outcome-backward-planning.md", "## Forward feasibility pass", "missing forward-pass contract"),
    ("references/outcome-backward-planning.md", "## Reconciliation loop", "missing reconciliation contract"),
    ("references/outcome-backward-planning.md", "## Module-freeze gate", "missing module-freeze gate"),
    ("references/outcome-backward-planning.md", "## Analysis depth", "missing lightweight/full analysis policy"),
    ("references/outcome-backward-planning.md", "## Compatibility", "missing compatibility guidance"),
    ("references/outcome-backward-planning.md", "No third analysis pass", "missing repeated-trigger hard block"),
    ("references/outcome-backward-planning.md", "readiness is unscorable", "missing pre-score hard gate"),
    ("references/outcome-backward-planning.md", "No UI, viewer, HTML, extension, or GitHub Pages artifact", "missing visualization boundary"),
)
OUTCOME_BACKWARD_RECONCILIATION_FIELDS = (
    "Trigger ID",
    "Trigger type",
    "Discovered at stage",
    "Conflict",
    "Affected findings",
    "Preserved findings",
    "Invalidated findings",
    "Required input or evidence",
    "Owner",
    "Decision and rationale",
    "Rerun scope",
    "Rerun count",
    "State",
    "Module-freeze impact",
)
EXPECTED_RUBRIC_ROWS = (
    ("Requirement clarity", 15, "Deduct 5 for missing problem/outcome; deduct 5 for ambiguous in/out scope or constraints; deduct 5 for missing affected modules."),
    ("Blueprint completeness", 15, "Deduct 3 each for missing architecture evidence, module responsibility/data flow, state ownership, failure/rollback path, or separate integration blueprint."),
    ("Interfaces and contracts", 15, "Deduct 3 each for missing input, output, error, compatibility, or security/privacy boundary."),
    ("Dependency isolation", 10, "Deduct 5 for any unclassified dependency; deduct 5 for any false-independence, shared-state, or overlapping-ownership parallel claim."),
    ("Acceptance criteria", 10, "Deduct 2 for each missing, non-testable, or unmapped criterion, up to 10."),
    ("Testability", 15, "Deduct 5 for missing focused test strategy; deduct 5 for missing contract/integration/e2e/regression plan; deduct 5 for missing deterministic command plus oracle."),
    ("Edge-case handling", 10, "Deduct 2 each when failure/retry, rollback/recovery, security/authorization, concurrency/state conflict, or backward-compatibility edge handling is absent."),
    ("Independent review", 10, "Award 0 if author and reviewer are not distinct; otherwise deduct 5 if findings lack dispositions and deduct 5 if score/evidence is not recorded."),
)


class ValidateSkillTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.skill = Path(self.temp.name) / "blueprint-first-delivery"
        shutil.copytree(
            SKILL_ROOT,
            self.skill,
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store"),
        )

    def run_validator(self, *args, timeout=10):
        command = [sys.executable, str(VALIDATOR)]
        command.extend(str(arg) for arg in (args or (self.skill,)))
        return subprocess.run(command, capture_output=True, text=True, timeout=timeout)

    def assert_invalid(self, expected, mutate):
        mutate()
        result = self.run_validator()
        self.assertEqual(1, result.returncode, result.stderr)
        self.assertEqual("", result.stdout)
        self.assertIn(expected, result.stderr)

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

    def load_validator_module(self):
        spec = importlib.util.spec_from_file_location("blueprint_skill_validator", VALIDATOR)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def test_current_package_is_valid(self):
        result = self.run_validator()
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual("", result.stdout)

    def test_model_routing_pressure_file_exists(self):
        self.assertTrue((SKILL_ROOT / ROUTING_SCENARIO_FILE).is_file())

    def test_model_routing_pressure_rows_are_exact(self):
        text = (SKILL_ROOT / ROUTING_SCENARIO_FILE).read_text()
        for scenario_id, pressure_case, expected_result in ROUTING_SCENARIO_ROWS:
            row = f"| {scenario_id} | {pressure_case} | {expected_result} |"
            with self.subTest(scenario_id=scenario_id):
                self.assertIn(row, text)

    def test_outcome_backward_pressure_file_exists(self):
        self.assertTrue((SKILL_ROOT / OUTCOME_BACKWARD_SCENARIO_FILE).is_file())

    def test_outcome_backward_pressure_rows_are_exact(self):
        text = (SKILL_ROOT / OUTCOME_BACKWARD_SCENARIO_FILE).read_text()
        for scenario_id, pressure_case, expected_result in OUTCOME_BACKWARD_SCENARIO_ROWS:
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

    def test_outcome_backward_contract_files_exist(self):
        for relative in (
            "references/outcome-backward-planning.md",
            OUTCOME_BACKWARD_SCENARIO_FILE,
        ):
            with self.subTest(relative=relative):
                self.assertTrue((SKILL_ROOT / relative).is_file(), relative)

    def test_every_outcome_backward_reference_requirement_is_enforced(self):
        for relative, required, expected in OUTCOME_BACKWARD_REFERENCE_REQUIREMENTS:
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

    def test_every_outcome_backward_pressure_oracle_is_enforced(self):
        path = self.skill / OUTCOME_BACKWARD_SCENARIO_FILE
        original = path.read_text()
        for scenario_id, pressure_case, expected_result in OUTCOME_BACKWARD_SCENARIO_ROWS:
            row = f"| {scenario_id} | {pressure_case} | {expected_result} |"
            with self.subTest(scenario_id=scenario_id):
                path.write_text(original.replace(row, "| removed |", 1))
                try:
                    result = self.run_validator()
                    self.assertEqual(1, result.returncode, result.stderr)
                    self.assertIn(
                        f"outcome-backward pressure scenario mismatch: {scenario_id}",
                        result.stderr,
                    )
                finally:
                    path.write_text(original)

    def test_every_reconciliation_report_field_is_enforced(self):
        path = self.skill / "references" / "outcome-backward-planning.md"
        original = path.read_text()
        header = next(
            line for line in original.splitlines()
            if line.startswith("| Trigger ID |")
        )
        for field in OUTCOME_BACKWARD_RECONCILIATION_FIELDS:
            with self.subTest(field=field):
                mutated_header = header.replace(field, "removed", 1)
                path.write_text(original.replace(header, mutated_header, 1))
                try:
                    result = self.run_validator()
                    self.assertEqual(1, result.returncode, result.stderr)
                    self.assertIn(f"missing reconciliation report field: {field}", result.stderr)
                finally:
                    path.write_text(original)

    def test_model_routing_rejects_reported_light_and_deep_policy_escapes(self):
        path = self.skill / "references" / "model-routing.md"
        original = path.read_text()
        cases = (
            (
                "Light task-shape escape",
                "Only search, extraction, classification, summarization, or mechanical transformation qualifies for Light; implementation and open-ended design do not.",
                "missing Light task-shape restriction",
            ),
            (
                "Deep-floor inversion",
                "A single protected-risk trigger establishes Deep.",
                "A single protected-risk trigger establishes Standard.",
                "missing Deep hard-risk floor",
            ),
        )
        for case in cases:
            with self.subTest(case=case[0]):
                if len(case) == 3:
                    _, old, expected = case
                    mutated = original.replace(old, "", 1)
                else:
                    _, old, new, expected = case
                    mutated = original.replace(old, new, 1)
                self.assertNotEqual(original, mutated)
                path.write_text(mutated)
                try:
                    result = self.run_validator()
                    self.assertEqual(1, result.returncode, result.stderr)
                    self.assertIn(expected, result.stderr)
                finally:
                    path.write_text(original)

    def test_xhigh_route_semantics_are_enforced(self):
        path = self.skill / "references" / "model-routing.md"
        original = path.read_text()
        cases = (
            (
                "two-trigger alternative",
                "Within Deep, xhigh requires two independent high-risk triggers",
                "missing xhigh two-trigger alternative",
            ),
            (
                "stable-fingerprint alternative",
                "or an unresolved high-effort attempt with a stable root fingerprint.",
                "missing xhigh stable-fingerprint alternative",
            ),
            (
                "high-insufficient rationale",
                "Routing review records why high is insufficient.",
                "missing xhigh high-insufficient rationale",
            ),
            (
                "no automatic Maximum",
                "xhigh does not automatically select Maximum.",
                "missing xhigh no-automatic-Maximum rule",
            ),
        )
        for name, required, expected in cases:
            with self.subTest(name=name):
                self.assertIn(required, original)
                path.write_text(original.replace(required, "removed", 1))
                try:
                    result = self.run_validator()
                    self.assertEqual(1, result.returncode, result.stderr)
                    self.assertIn(expected, result.stderr)
                finally:
                    path.write_text(original)

    def test_parallel_dependency_semantics_are_enforced(self):
        path = self.skill / "references" / "model-routing.md"
        original = path.read_text()
        cases = (
            (
                "completed-common-prerequisite allowance",
                "Completed or common prerequisites do not block parallel work.",
                "missing completed-prerequisite parallel allowance",
            ),
            (
                "unfinished-member dependency block",
                "Parallel is blocked only by a dependency on another parallel-group member's unfinished output,",
                "missing unfinished-member parallel dependency block",
            ),
        )
        for name, required, expected in cases:
            with self.subTest(name=name):
                self.assertIn(required, original)
                path.write_text(original.replace(required, "removed", 1))
                try:
                    result = self.run_validator()
                    self.assertEqual(1, result.returncode, result.stderr)
                    self.assertIn(expected, result.stderr)
                finally:
                    path.write_text(original)

    def test_light_predicates_and_standard_default_are_enforced(self):
        path = self.skill / "references" / "model-routing.md"
        original = path.read_text()
        cases = (
            ("exact responsibility/output", "Light requires exact responsibility and output.", "missing Light exact responsibility/output predicate"),
            ("frozen contracts/inputs", "Light requires frozen contracts and inputs.", "missing Light frozen contracts/inputs predicate"),
            ("local reversible blast radius", "Light requires a local, reversible blast radius.", "missing Light local/reversible predicate"),
            ("no protected risks", "Light requires no protected-risk trigger.", "missing Light protected-risk predicate"),
            ("objective oracle", "Light requires an objective oracle.", "missing Light objective-oracle predicate"),
            ("eligible task shape", "Only search, extraction, classification, summarization, or mechanical transformation qualifies for Light; implementation and open-ended design do not.", "missing Light task-shape restriction"),
            ("failed predicate result", "Failure of any Light predicate requires Standard or higher.", "missing Light failure result"),
            ("Standard default", "Otherwise use Standard for normal bounded implementation.", "missing Standard default"),
        )
        for name, required, expected in cases:
            with self.subTest(name=name):
                self.assertIn(required, original)
                path.write_text(original.replace(required, "removed", 1))
                try:
                    result = self.run_validator()
                    self.assertEqual(1, result.returncode, result.stderr)
                    self.assertIn(expected, result.stderr)
                finally:
                    path.write_text(original)

        inverted = original.replace(
            "Otherwise use Standard for normal bounded implementation.",
            "Otherwise use Light for normal bounded implementation.",
            1,
        )
        path.write_text(inverted)
        try:
            result = self.run_validator()
            self.assertEqual(1, result.returncode, result.stderr)
            self.assertIn("missing Standard default", result.stderr)
        finally:
            path.write_text(original)

    def test_maximum_or_eligibility_and_exclusions_are_enforced(self):
        path = self.skill / "references" / "model-routing.md"
        original = path.read_text()
        cases = (
            (
                "xhigh evidence alternative",
                "Maximum is eligible when an xhigh Deep attempt gives concrete evidence the central problem remains unresolved",
                "missing Maximum xhigh-evidence alternative",
            ),
            (
                "indivisible critical-risk alternative",
                "or the hardest single critical-risk decision cannot be decomposed without losing the problem",
                "missing Maximum indivisible-critical-risk alternative",
            ),
            (
                "principal rationale alternative",
                "or principal review records why high and xhigh are insufficient.",
                "missing Maximum principal-rationale alternative",
            ),
            (
                "exceptional classification",
                "Maximum is exceptional.",
                "missing Maximum exceptional classification",
            ),
            (
                "routine implementation exclusion",
                "Maximum is not routine implementation, retry without diagnosis, or multiple independent workstreams.",
                "missing Maximum routine-work exclusion",
            ),
        )
        for name, required, expected in cases:
            with self.subTest(name=name):
                self.assertIn(required, original)
                path.write_text(original.replace(required, "removed", 1))
                try:
                    result = self.run_validator()
                    self.assertEqual(1, result.returncode, result.stderr)
                    self.assertIn(expected, result.stderr)
                finally:
                    path.write_text(original)

        inverted = original.replace(
            "Maximum is exceptional.",
            "Maximum is routine implementation.",
            1,
        )
        path.write_text(inverted)
        try:
            result = self.run_validator()
            self.assertEqual(1, result.returncode, result.stderr)
            self.assertIn("missing Maximum exceptional classification", result.stderr)
        finally:
            path.write_text(original)

    def test_every_model_routing_semantic_rule_is_enforced(self):
        module = self.load_validator_module()
        path = self.skill / "references" / "model-routing.md"
        original = path.read_text()
        self.assertEqual(26, len(module.POLICY_SEMANTIC_REQUIREMENTS))
        for scenario_id, required, expected in module.POLICY_SEMANTIC_REQUIREMENTS:
            with self.subTest(scenario_id=scenario_id):
                self.assertIn(required, original)
                path.write_text(original.replace(required, "removed", 1))
                try:
                    result = self.run_validator()
                    self.assertEqual(1, result.returncode, result.stderr)
                    self.assertIn(expected, result.stderr)
                finally:
                    path.write_text(original)

    def test_routing_contract_files_exist(self):
        for relative in ROUTING_REQUIRED_FILES:
            with self.subTest(relative=relative):
                self.assertTrue((SKILL_ROOT / relative).is_file(), relative)

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

    def test_light_effort_only_self_promotion_is_rejected(self):
        path = self.skill / "references" / "runtime-mappings" / "codex.md"
        original = path.read_text()
        light_model = self.mapping_model(original, "Light")
        path.write_text(
            self.replace_mapping_cell(
                original,
                "Light",
                5,
                f"`{light_model}` / `medium`",
            )
        )
        try:
            result = self.run_validator()
            self.assertEqual(1, result.returncode, result.stderr)
            self.assertIn(
                "higher fallback must target a higher tier for Light",
                result.stderr,
            )
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

    def test_skill_stays_under_500_words(self):
        skill = (SKILL_ROOT / "SKILL.md").read_text()
        self.assertLess(len(skill.split()), 500)

    def test_usage_error_is_exit_two(self):
        result = self.run_validator("one", "two")
        self.assertEqual(2, result.returncode)
        self.assertEqual("validate_skill.py:0: usage: validate_skill.py <skill-directory>\n", result.stderr)

    def test_unknown_skill_metadata_is_rejected(self):
        path = self.skill / "SKILL.md"

        def mutate():
            path.write_text(path.read_text().replace("description:", "unknown: value\ndescription:", 1))

        self.assert_invalid("SKILL.md:3: expected description metadata", mutate)

    def test_duplicate_openai_key_is_rejected(self):
        path = self.skill / "agents" / "openai.yaml"

        def mutate():
            path.write_text(path.read_text() + '  display_name: "Duplicate"\n')

        self.assert_invalid("openai.yaml:5: unexpected metadata", mutate)

    def test_yaml_control_colon_in_description_is_rejected(self):
        path = self.skill / "SKILL.md"

        def mutate():
            path.write_text(path.read_text().replace("feature, refactor", "feature: refactor", 1))

        self.assert_invalid("SKILL.md:3: invalid description", mutate)

    def test_default_prompt_must_name_the_skill(self):
        path = self.skill / "agents" / "openai.yaml"

        def mutate():
            path.write_text(path.read_text().replace("$blueprint-first-delivery", "the skill"))

        self.assert_invalid("openai.yaml:4: default_prompt must contain $blueprint-first-delivery", mutate)

    def test_missing_architecture_exploration_contract_is_rejected(self):
        path = self.skill / "SKILL.md"

        def mutate():
            text = path.read_text()
            marker = "1. Explore the existing architecture"
            if marker in text:
                start = text.index(marker)
                end = text.index("\n2. ", start)
                text = text[:start] + "1. Define scope and modules.\n" + text[end + 1 :]
            path.write_text(text)

        self.assert_invalid("SKILL.md:0: missing architecture exploration requirement", mutate)

    def test_architecture_evidence_is_an_unscorable_hard_gate(self):
        skill = (SKILL_ROOT / "SKILL.md").read_text()
        rubric = (SKILL_ROOT / "references" / "readiness-rubric.md").read_text()
        checklist = (SKILL_ROOT / "references" / "review-and-gate-checklists.md").read_text()
        self.assertIn("Do not score an existing-codebase blueprint", skill)
        self.assertIn("literal status `greenfield`", skill)
        self.assertIn("unscorable", rubric)
        self.assertIn("Do not score", checklist)

    def test_blocked_gate_report_has_all_eight_required_fields(self):
        skill = (SKILL_ROOT / "SKILL.md").read_text()
        for field in (
            "## Blocked gate report",
            "Status / pre-code block:",
            "Architecture evidence:",
            "Independent review:",
            "Readiness / veto:",
            "Ownership / ordering:",
            "Chunk gates:",
            "Integration gate:",
            "Traceability:",
            "principal-engineer-style reviewer =",
            "distinct from author =",
            "overall score =",
            "every chunk score =",
            "threshold for both = >=95/100",
            "start gate =",
            "completion gate =",
            "separate blueprint =",
            "separate gate =",
        ):
            with self.subTest(field=field):
                self.assertIn(field, skill)

    def test_core_workflow_removals_are_rejected(self):
        cases = (
            ("SKILL.md", "principal-engineer-style adversarial review", "missing independent adversarial review"),
            ("SKILL.md", "Before each chunk, satisfy its chunk gate", "missing per-chunk gate requirement"),
            ("SKILL.md", "execute the separate integration blueprint", "missing separate integration workflow"),
            ("SKILL.md", "Publish a traceability report", "missing final traceability requirement"),
            ("SKILL.md", "Pressure rules:", "missing pressure-resistance rules"),
            ("tests/pressure-scenarios.md", "## Premature coding", "missing premature-coding pressure scenario"),
        )
        for relative, required, expected in cases:
            with self.subTest(relative=relative, required=required):
                path = self.skill / relative
                original = path.read_text()
                self.assertIn(required, original)
                path.write_text(original.replace(required, "removed", 1))
                result = self.run_validator()
                self.assertEqual(1, result.returncode, result.stderr)
                self.assertIn(expected, result.stderr)
                path.write_text(original)

    def test_behavior_evidence_artifacts_cannot_be_placeholders(self):
        cases = (
            ("tests/pressure-scenarios.md", "missing premature-coding pressure scenario"),
            ("tests/baseline-no-skill.md", "missing matched no-skill behavior probe"),
            ("tests/forward-test-with-skill.md", "missing matched with-skill behavior probe"),
        )
        for relative, expected in cases:
            with self.subTest(relative=relative):
                path = self.skill / relative
                original = path.read_text()
                path.write_text("placeholder\n")
                result = self.run_validator()
                self.assertEqual(1, result.returncode, result.stderr)
                self.assertIn(expected, result.stderr)
                path.write_text(original)

    def test_behavior_evidence_has_five_reps_per_variant_and_variance_review(self):
        baseline = (SKILL_ROOT / "tests" / "baseline-no-skill.md").read_text()
        forward = (SKILL_ROOT / "tests" / "forward-test-with-skill.md").read_text()
        self.assertIn("No-guidance repetitions: **5/5**", baseline)
        self.assertIn("No-guidance score variance: **0 points**", baseline)
        self.assertIn("Final guided repetitions: **5/5**", forward)
        self.assertIn("Final guided score variance: **0 points**", forward)
        self.assertIn("Compressed-final guided repetitions: **5/5**", forward)
        self.assertIn("Compressed-final score variance: **0 points**", forward)
        self.assertIn("Pre-tightening scores: **3, 4, 4, 3, 3**", forward)

    def test_design_label_matches_frozen_rubric(self):
        design = (REPO_ROOT / "docs" / "superpowers" / "specs" / "2026-07-31-blueprint-first-delivery-design.md").read_text()
        rubric = (SKILL_ROOT / "references" / "readiness-rubric.md").read_text()
        self.assertIn("| Edge-case handling | 10 |", design)
        self.assertIn("| Edge-case handling | 10 |", rubric)

    def test_rubric_rows_weights_and_deductions_are_exact(self):
        path = self.skill / "references" / "readiness-rubric.md"

        def mutate():
            path.write_text(path.read_text().replace("| Requirement clarity | 15 |", "| Requirement clarity | 14 |", 1))

        self.assert_invalid("readiness-rubric.md:0: readiness rubric does not match approved scoring contract", mutate)

    def test_rubric_deduction_wording_and_values_are_exact(self):
        path = self.skill / "references" / "readiness-rubric.md"

        def mutate():
            path.write_text(path.read_text().replace("Deduct 5 for missing problem/outcome", "Deduct 4 for missing problem/outcome", 1))

        self.assert_invalid("readiness-rubric.md:0: readiness rubric does not match approved scoring contract", mutate)

    def test_every_rubric_row_weight_and_deduction_is_enforced(self):
        module = self.load_validator_module()
        self.assertEqual(EXPECTED_RUBRIC_ROWS, module.RUBRIC_ROWS)
        self.assertEqual(100, sum(weight for _, weight, _ in EXPECTED_RUBRIC_ROWS))
        path = self.skill / "references" / "readiness-rubric.md"
        original = path.read_text()
        for name, weight, deduction in EXPECTED_RUBRIC_ROWS:
            row = f"| {name} | {weight} |  | {deduction} |"
            with self.subTest(name=name, field="weight"):
                path.write_text(original.replace(row, f"| {name} | {weight + 1} |  | {deduction} |", 1))
                result = self.run_validator()
                self.assertEqual(1, result.returncode, result.stderr)
                self.assertIn("readiness rubric does not match approved scoring contract", result.stderr)
            with self.subTest(name=name, field="deduction"):
                path.write_text(original.replace(row, row.replace(deduction, deduction + " Changed."), 1))
                result = self.run_validator()
                self.assertEqual(1, result.returncode, result.stderr)
                self.assertIn("readiness rubric does not match approved scoring contract", result.stderr)
        path.write_text(original)

    def test_rubric_validator_enforces_100_point_invariant_independently(self):
        module = self.load_validator_module()
        rubric = (self.skill / "references" / "readiness-rubric.md").read_text()
        changed_rows = tuple(
            (name, 14 if name == "Testability" else weight, deduction)
            for name, weight, deduction in module.RUBRIC_ROWS
        )
        changed_rubric = rubric.replace("| Testability | 15 |", "| Testability | 14 |", 1)
        with mock.patch.object(module, "RUBRIC_ROWS", changed_rows):
            with self.assertRaises(module.PackageError) as caught:
                module._validate_rubric(changed_rubric)
        self.assertIn("readiness rubric does not match approved scoring contract", str(caught.exception))

    def test_old_rubric_row_is_rejected(self):
        path = self.skill / "references" / "readiness-rubric.md"

        def mutate():
            path.write_text(path.read_text() + "\n| Scope and acceptance criteria | 15 |  | old |\n")

        self.assert_invalid("readiness-rubric.md:0: legacy readiness rubric row present", mutate)

    def test_arbitrary_extra_rubric_row_is_rejected(self):
        path = self.skill / "references" / "readiness-rubric.md"

        def mutate():
            path.write_text(path.read_text() + "\n| Extra evidence | 1 | 0 | Deduct 1. |\n")

        self.assert_invalid("readiness-rubric.md:0: readiness rubric does not match approved scoring contract", mutate)

    def test_rubric_total_row_is_exact(self):
        path = self.skill / "references" / "readiness-rubric.md"

        def mutate():
            path.write_text(path.read_text().replace("| **Total** | **100** |", "| **Total** | **999** |", 1))

        self.assert_invalid("readiness-rubric.md:0: readiness rubric does not match approved scoring contract", mutate)

    def test_crlf_metadata_is_accepted(self):
        for relative in ("SKILL.md", "agents/openai.yaml"):
            path = self.skill / relative
            path.write_bytes(path.read_text().replace("\n", "\r\n").encode())
        result = self.run_validator()
        self.assertEqual(0, result.returncode, result.stderr)

    def test_bare_cr_is_rejected(self):
        path = self.skill / "agents" / "openai.yaml"
        path.write_bytes(path.read_bytes().replace(b"\n", b"\r", 1))
        result = self.run_validator()
        self.assertEqual(1, result.returncode)
        self.assertIn("agents/openai.yaml:1: bare CR newline is not allowed", result.stderr)

    def test_mixed_lf_and_crlf_are_rejected(self):
        path = self.skill / "agents" / "openai.yaml"
        path.write_bytes(path.read_bytes().replace(b"\n", b"\r\n", 1))
        result = self.run_validator()
        self.assertEqual(1, result.returncode)
        self.assertIn("agents/openai.yaml:2: mixed newline styles are not allowed", result.stderr)

    def test_json_escape_is_accepted(self):
        path = self.skill / "agents" / "openai.yaml"
        text = path.read_text().replace("Blueprint-First Delivery", "Blueprint-First \\u0044elivery")
        path.write_text(text)
        result = self.run_validator()
        self.assertEqual(0, result.returncode, result.stderr)

    def test_lone_surrogate_escape_is_rejected(self):
        path = self.skill / "agents" / "openai.yaml"

        def mutate():
            path.write_text(path.read_text().replace('  display_name: "Blueprint-First Delivery"', r'  display_name: "\ud800"'))

        self.assert_invalid("agents/openai.yaml:2: display_name contains a surrogate code point", mutate)

    def test_del_control_escape_is_rejected(self):
        path = self.skill / "agents" / "openai.yaml"

        def mutate():
            path.write_text(path.read_text().replace('  display_name: "Blueprint-First Delivery"', r'  display_name: "\u007f"'))

        self.assert_invalid("agents/openai.yaml:2: invalid display_name control character", mutate)

    def test_name_minimum_and_maximum_are_accepted(self):
        for name in ("a", "a" * 64):
            with self.subTest(name=name):
                renamed = Path(self.temp.name) / name
                shutil.copytree(self.skill, renamed)
                skill_md = renamed / "SKILL.md"
                skill_md.write_text(skill_md.read_text().replace("name: blueprint-first-delivery", f"name: {name}", 1))
                result = self.run_validator(renamed)
                self.assertEqual(0, result.returncode, result.stderr)

    def test_invalid_name_characters_and_length_are_rejected(self):
        for name in ("-a", "a-", "a--b", "a_b", "a" * 65):
            with self.subTest(name=name):
                renamed = Path(self.temp.name) / name
                shutil.copytree(self.skill, renamed)
                skill_md = renamed / "SKILL.md"
                skill_md.write_text(skill_md.read_text().replace("name: blueprint-first-delivery", f"name: {name}", 1))
                result = self.run_validator(renamed)
                self.assertEqual(1, result.returncode, result.stderr)
                self.assertIn("SKILL.md:2: invalid skill name", result.stderr)

    def test_description_minimum_and_maximum_are_accepted(self):
        path = self.skill / "SKILL.md"
        original = path.read_text()
        current = original.splitlines()[2]
        for description in ("Use when " + "x" * 11, "Use when " + "x" * 491):
            with self.subTest(length=len(description)):
                path.write_text(original.replace(current, f"description: {description}", 1))
                result = self.run_validator()
                self.assertEqual(0, result.returncode, result.stderr)
        path.write_text(original)

    def test_description_outside_boundaries_is_rejected(self):
        path = self.skill / "SKILL.md"
        original = path.read_text()
        current = original.splitlines()[2]
        for description in ("Use when " + "x" * 10, "Use when " + "x" * 492):
            with self.subTest(length=len(description)):
                path.write_text(original.replace(current, f"description: {description}", 1))
                result = self.run_validator()
                self.assertEqual(1, result.returncode, result.stderr)
                self.assertIn("SKILL.md:3: invalid description", result.stderr)
        path.write_text(original)

    def test_openai_scalar_minimums_and_maximums_are_accepted(self):
        path = self.skill / "agents" / "openai.yaml"
        original = path.read_text()
        cases = (
            ("D", "S" * 25, "$blueprint-first-delivery"),
            ("D" * 64, "S" * 64, "$blueprint-first-delivery" + "x" * (500 - len("$blueprint-first-delivery"))),
        )
        for display, short, prompt in cases:
            with self.subTest(display=len(display), short=len(short), prompt=len(prompt)):
                lines = original.splitlines()
                lines[1] = f"  display_name: {json.dumps(display)}"
                lines[2] = f"  short_description: {json.dumps(short)}"
                lines[3] = f"  default_prompt: {json.dumps(prompt)}"
                path.write_text("\n".join(lines) + "\n")
                result = self.run_validator()
                self.assertEqual(0, result.returncode, result.stderr)
        path.write_text(original)

    def test_openai_scalars_outside_boundaries_are_rejected(self):
        path = self.skill / "agents" / "openai.yaml"
        original = path.read_text()
        cases = (
            (1, "", "display_name must be 1-64 characters"),
            (1, "D" * 65, "display_name must be 1-64 characters"),
            (2, "S" * 24, "short_description must be 25-64 characters"),
            (2, "S" * 65, "short_description must be 25-64 characters"),
            (3, "", "default_prompt must be 1-500 characters"),
            (3, "$blueprint-first-delivery" + "x" * 476, "default_prompt must be 1-500 characters"),
        )
        for index, value, expected in cases:
            with self.subTest(index=index, length=len(value)):
                lines = original.splitlines()
                key = ("display_name", "short_description", "default_prompt")[index - 1]
                lines[index] = f"  {key}: {json.dumps(value)}"
                path.write_text("\n".join(lines) + "\n")
                result = self.run_validator()
                self.assertEqual(1, result.returncode, result.stderr)
                self.assertIn(expected, result.stderr)
        path.write_text(original)

    def test_missing_file_uses_line_zero(self):
        path = self.skill / "references" / "blueprint-templates.md"
        path.unlink()
        result = self.run_validator()
        self.assertEqual(1, result.returncode)
        self.assertIn("blueprint-templates.md:0: missing required file", result.stderr)

    def test_missing_root_is_runtime_exit_two(self):
        result = self.run_validator(Path(self.temp.name) / "missing")
        self.assertEqual(2, result.returncode)
        self.assertEqual("", result.stdout)
        self.assertIn(":0: cannot resolve skill directory", result.stderr)

    def test_bom_is_rejected(self):
        path = self.skill / "SKILL.md"
        path.write_bytes(b"\xef\xbb\xbf" + path.read_bytes())
        result = self.run_validator()
        self.assertEqual(1, result.returncode)
        self.assertIn("SKILL.md:1: UTF-8 BOM is not allowed", result.stderr)

    def test_invalid_utf8_reports_line_number_not_byte_offset(self):
        path = self.skill / "references" / "blueprint-templates.md"
        path.write_bytes(b"valid first line\ninvalid: \xff\n")
        result = self.run_validator()
        self.assertEqual(1, result.returncode)
        self.assertIn("blueprint-templates.md:2: invalid UTF-8", result.stderr)

    def test_missing_final_newline_is_rejected(self):
        path = self.skill / "agents" / "openai.yaml"
        path.write_bytes(path.read_bytes().rstrip(b"\r\n"))
        result = self.run_validator()
        self.assertEqual(1, result.returncode)
        self.assertIn("openai.yaml:4: final newline is required", result.stderr)

    def test_oversized_metadata_is_rejected(self):
        path = self.skill / "agents" / "openai.yaml"
        path.write_bytes(b"x" * (256 * 1024 + 1))
        result = self.run_validator()
        self.assertEqual(1, result.returncode)
        self.assertIn("openai.yaml:0: file exceeds 262144 bytes", result.stderr)

    def test_exact_256_kib_metadata_file_is_accepted(self):
        path = self.skill / "SKILL.md"
        raw = path.read_bytes()
        path.write_bytes(raw + b"x" * (256 * 1024 - len(raw) - 1) + b"\n")
        self.assertEqual(256 * 1024, path.stat().st_size)
        result = self.run_validator()
        self.assertEqual(0, result.returncode, result.stderr)

    def test_reference_file_is_not_subject_to_metadata_size_limit(self):
        path = self.skill / "references" / "blueprint-templates.md"
        raw = path.read_bytes()
        path.write_bytes(raw + b"x" * (256 * 1024 + 1 - len(raw) - 1) + b"\n")
        result = self.run_validator()
        self.assertEqual(0, result.returncode, result.stderr)

    def test_short_description_minimum_is_enforced(self):
        path = self.skill / "agents" / "openai.yaml"
        lines = path.read_text().splitlines()
        lines[2] = f"  short_description: {json.dumps('x' * 24)}"
        path.write_text("\n".join(lines) + "\n")
        result = self.run_validator()
        self.assertEqual(1, result.returncode)
        self.assertIn("openai.yaml:3: short_description must be 25-64 characters", result.stderr)

    def test_boundary_length_metadata_is_accepted(self):
        path = self.skill / "agents" / "openai.yaml"
        lines = path.read_text().splitlines()
        lines[1] = f"  display_name: {json.dumps('D' * 64)}"
        lines[2] = f"  short_description: {json.dumps('S' * 25)}"
        path.write_text("\n".join(lines) + "\n")
        result = self.run_validator()
        self.assertEqual(0, result.returncode, result.stderr)

    def test_unexpected_top_level_file_is_rejected(self):
        path = self.skill / "unexpected.txt"
        path.write_text("unexpected\n")
        result = self.run_validator()
        self.assertEqual(1, result.returncode)
        self.assertIn("unexpected.txt:0: unexpected top-level entry", result.stderr)

    def test_nested_external_symlink_is_rejected(self):
        external = Path(self.temp.name) / "external.md"
        external.write_text("external\n")
        os.symlink(external, self.skill / "references" / "external.md")
        result = self.run_validator()
        self.assertEqual(1, result.returncode)
        self.assertIn("external.md:0: nested symlink is not allowed", result.stderr)

    def test_required_fifo_is_rejected_without_blocking(self):
        path = self.skill / "agents" / "openai.yaml"
        path.unlink()
        os.mkfifo(path)
        try:
            result = self.run_validator(timeout=1)
        except subprocess.TimeoutExpired:
            self.fail("validator blocked while opening a required FIFO")
        self.assertEqual(1, result.returncode, result.stderr)
        self.assertIn("agents/openai.yaml:0: required path is not a regular file", result.stderr)

    def test_optional_fifo_is_rejected(self):
        path = self.skill / "tests" / "optional.fifo"
        os.mkfifo(path)
        result = self.run_validator(timeout=1)
        self.assertEqual(1, result.returncode, result.stderr)
        self.assertIn("tests/optional.fifo:0: non-regular package entry is not allowed", result.stderr)

    def test_tree_traversal_io_error_is_runtime_diagnostic(self):
        module = self.load_validator_module()
        with mock.patch.object(module.Path, "iterdir", side_effect=PermissionError("denied")):
            with self.assertRaises(module.RuntimeValidationError) as caught:
                module.validate(str(self.skill))
        self.assertEqual(".:0: cannot traverse skill directory: denied", str(caught.exception))

    def test_nested_internal_symlink_is_rejected(self):
        os.symlink(
            self.skill / "references" / "blueprint-templates.md",
            self.skill / "references" / "internal.md",
        )
        result = self.run_validator()
        self.assertEqual(1, result.returncode)
        self.assertIn("internal.md:0: nested symlink is not allowed", result.stderr)

    def test_root_symlink_is_accepted(self):
        linked = Path(self.temp.name) / "linked-skill"
        os.symlink(self.skill, linked)
        result = self.run_validator(linked)
        self.assertEqual(0, result.returncode, result.stderr)

    def test_cache_directory_is_rejected(self):
        cache = self.skill / "scripts" / "__pycache__"
        cache.mkdir()
        (cache / "validator.pyc").write_bytes(b"cache")
        result = self.run_validator()
        self.assertEqual(1, result.returncode)
        self.assertIn("__pycache__:0: cache or platform artifact is not allowed", result.stderr)

    def test_wrapper_call_graph_is_acyclic_and_complete(self):
        wrapper = (SKILL_ROOT / "tests" / "validate-skill.sh").read_text()
        harness = (SKILL_ROOT / "tests" / "test-validator-negative-fixtures.sh").read_text()
        self.assertIn("scripts/validate_skill.py", wrapper)
        self.assertIn("test-validator-negative-fixtures.sh", wrapper)
        self.assertIn("scripts/validate_skill.py", harness)
        self.assertNotIn("tests/validate-skill.sh", harness)
        self.assertIn('test "$status" -eq 1', harness)
        self.assertIn("grep -Fq", harness)

    def test_metadata_outside_fixture_is_isolated(self):
        fixture = (SKILL_ROOT / "tests" / "fixtures" / "metadata-outside-frontmatter.md").read_text()
        self.assertEqual("name: blueprint-first-delivery\n", fixture)

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


if __name__ == "__main__":
    unittest.main()
