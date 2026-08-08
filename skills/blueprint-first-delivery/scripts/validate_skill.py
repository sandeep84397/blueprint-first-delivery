#!/usr/bin/env python3
"""Validate the fixed blueprint-first-delivery skill package profile."""

from __future__ import annotations

import json
from pathlib import Path
import re
import sys
import unicodedata


MAX_FILE_BYTES = 256 * 1024
METADATA_FILES = {"SKILL.md", "agents/openai.yaml"}
ALLOWED_TOP_LEVEL = {"SKILL.md", "agents", "references", "scripts", "tests"}
ROUTING_SCENARIO_FILE = "tests/model-routing-pressure-scenarios.md"
OUTCOME_BACKWARD_SCENARIO_FILE = "tests/outcome-backward-pressure-scenarios.md"
ADAPTIVE_EVIDENCE_SCENARIO_FILE = "tests/adaptive-evidence-pressure-scenarios.md"
REQUIRED_FILES = (
    "SKILL.md",
    "agents/openai.yaml",
    "references/blueprint-templates.md",
    "references/model-routing.md",
    "references/outcome-backward-planning.md",
    "references/readiness-rubric.md",
    "references/adaptive-evidence-first.md",
    "references/evidence-manifest.md",
    "references/review-and-gate-checklists.md",
    "references/runtime-mappings/codex.md",
    "references/runtime-mappings/claude-code.md",
    "scripts/validate_skill.py",
    "scripts/validate_evidence_manifest.py",
    "scripts/verify_global_boundary.py",
    "tests/pressure-scenarios.md",
    "tests/baseline-no-skill.md",
    "tests/forward-test-with-skill.md",
    "tests/test_verify_global_boundary.py",
    "tests/validate-skill.sh",
    "tests/test-validator-negative-fixtures.sh",
    "tests/test_validate_skill.py",
    "tests/test_validate_evidence_manifest.py",
    ROUTING_SCENARIO_FILE,
    OUTCOME_BACKWARD_SCENARIO_FILE,
    ADAPTIVE_EVIDENCE_SCENARIO_FILE,
    "references/examples/direct-task-proven.json",
    "references/examples/lite-task-proven-handoff.json",
    "references/examples/full-plan-frozen.json",
)
RUNTIME_MAPPING_FILES = (
    "references/runtime-mappings/codex.md",
    "references/runtime-mappings/claude-code.md",
)
NEUTRAL_ROUTING_FILES = (
    "SKILL.md",
    "references/model-routing.md",
    "references/outcome-backward-planning.md",
    "references/blueprint-templates.md",
    "references/readiness-rubric.md",
    "references/review-and-gate-checklists.md",
    "references/adaptive-evidence-first.md",
    "references/evidence-manifest.md",
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
DESCRIPTION_RE = re.compile(r"Use when [A-Za-z0-9 ,.'()/+\-]+")
NAME_RE = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")

RUBRIC_ROWS = (
    ("Requirement clarity", 15, "Deduct 5 for missing problem/outcome; deduct 5 for ambiguous in/out scope or constraints; deduct 5 for missing affected modules."),
    ("Blueprint completeness", 15, "Deduct 3 each for missing architecture evidence, module responsibility/data flow, state ownership, failure/rollback path, or separate integration blueprint."),
    ("Interfaces and contracts", 15, "Deduct 3 each for missing input, output, error, compatibility, or security/privacy boundary."),
    ("Dependency isolation", 10, "Deduct 5 for any unclassified dependency; deduct 5 for any false-independence, shared-state, or overlapping-ownership parallel claim."),
    ("Acceptance criteria", 10, "Deduct 2 for each missing, non-testable, or unmapped criterion, up to 10."),
    ("Testability", 15, "Deduct 5 for missing focused test strategy; deduct 5 for missing contract/integration/e2e/regression plan; deduct 5 for missing deterministic command plus oracle."),
    ("Edge-case handling", 10, "Deduct 2 each when failure/retry, rollback/recovery, security/authorization, concurrency/state conflict, or backward-compatibility edge handling is absent."),
    ("Independent review", 10, "Award 0 if author and reviewer are not distinct; otherwise deduct 5 if findings lack dispositions and deduct 5 if score/evidence is not recorded."),
)
LEGACY_RUBRIC_ROWS = (
    "Scope and acceptance criteria",
    "Module boundaries and ownership",
    "Contracts and validation",
    "Dependencies and ordering",
    "Data, security, and failure handling",
    "Verification and integration blueprint",
    "Risks and traceability",
)
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
ADAPTIVE_EVIDENCE_SCENARIO_ROWS = (
    ("AE01", "Exact one-owner reversible change with deterministic oracle and no handoff", "Direct"),
    ("AE02", "Bounded implementation with one owner and no Full trigger", "Lite"),
    ("AE03", "Unknown external API behavior or unresolved external dependency", "Full"),
    ("AE04", "Persistence, migration, recovery, deletion, or integrity risk", "Full"),
    ("AE05", "Two modules or state owners on one causal path", "Full"),
    ("AE06", "Critical contract has prose but no named executable oracle", "Approval blocked"),
    ("AE07", "Baseline contract, owned file, or evidence digest changes", "Evidence STALE; re-approval required"),
    ("AE08", "Full work has Agent Brain summary without source references", "Gate blocked"),
    ("AE09", "Integration is deferred until the final milestone", "Early vertical proof required"),
    ("AE10", "Lite handoff lacks source-linked Agent Brain", "Gate blocked"),
)
OUTCOME_BACKWARD_WORKFLOW_REQUIREMENTS = (
    ("SKILL.md", "**Full** — define the outcome contract", "missing outcome-contract stage"),
    ("SKILL.md", "Run outcome-backward and forward reconciliation", "missing convergence-before-freeze gate"),
    ("SKILL.md", "Architecture / plan:", "missing blocked outcome-backward field"),
    ("references/blueprint-templates.md", "## Outcome-Backward Plan", "missing outcome-backward template"),
    ("references/blueprint-templates.md", "### Reconciliation history", "missing reconciliation-history template"),
    ("references/review-and-gate-checklists.md", "## Outcome-backward planning gate", "missing outcome-backward review gate"),
    ("references/review-and-gate-checklists.md", "No automatic rerun occurs before the answer.", "missing user-owned wait rule"),
    ("references/review-and-gate-checklists.md", "No third analysis pass", "missing repeated-trigger block"),
    ("references/readiness-rubric.md", "Outcome-backward planning is a separate pre-score gate.", "missing separate pre-score gate"),
    ("references/readiness-rubric.md", "If it is not `PASS`, readiness is **unscorable**.", "missing unscorable outcome-backward rule"),
)
ADAPTIVE_EVIDENCE_REQUIREMENTS = (
    ("SKILL.md", "Route before choosing blueprint depth.", "missing adaptive route gate"),
    ("SKILL.md", "Direct requires every Direct predicate", "missing Direct all-predicates gate"),
    ("SKILL.md", "Full is mandatory", "missing Full hard-trigger gate"),
    ("SKILL.md", "Executable proof is required", "missing executable-proof gate"),
    ("SKILL.md", "Use source-linked Agent Brain for a handoff", "missing Lite source-linked Agent Brain gate"),
    ("SKILL.md", "Full work requires source-linked Agent Brain.", "missing Full source-linked Agent Brain gate"),
    ("references/adaptive-evidence-first.md", "## Deterministic route", "missing deterministic route contract"),
    ("references/adaptive-evidence-first.md", "### Direct: every predicate must pass", "missing Direct predicate contract"),
    ("references/adaptive-evidence-first.md", "### Full: any hard trigger is sufficient", "missing Full trigger contract"),
    ("references/adaptive-evidence-first.md", "Outcome-backward and forward reconciliation runs only for Full.", "missing Full-only reconciliation rule"),
    ("references/adaptive-evidence-first.md", "## Approval states", "missing distinct approval states"),
    ("references/adaptive-evidence-first.md", "early vertical proof", "missing early integration proof"),
    ("references/evidence-manifest.md", "## Proof matrix", "missing proof matrix contract"),
    ("references/evidence-manifest.md", "`ASSUMPTION`, `BLOCKED`, or `STALE`", "missing critical proof state veto"),
    ("references/evidence-manifest.md", "## Immutable baseline and drift", "missing immutable baseline contract"),
    ("references/evidence-manifest.md", "mark affected evidence `STALE`", "missing drift invalidation contract"),
    ("references/evidence-manifest.md", "## Agent Brain continuity", "missing Agent Brain continuity contract"),
    ("references/blueprint-templates.md", "## Direct receipt template", "missing Direct receipt template"),
    ("references/blueprint-templates.md", "## Lite card template", "missing Lite card template"),
    ("references/blueprint-templates.md", "## Full evidence manifest template", "missing Full evidence manifest template"),
    ("references/blueprint-templates.md", "early_vertical_proof:", "missing early vertical proof template"),
    ("references/review-and-gate-checklists.md", "## Route gate", "missing route gate"),
    ("references/review-and-gate-checklists.md", "## Architecture approval", "missing architecture approval gate"),
    ("references/review-and-gate-checklists.md", "## Plan freeze", "missing plan freeze gate"),
    ("references/review-and-gate-checklists.md", "## Task proof", "missing task proof gate"),
    ("references/review-and-gate-checklists.md", "## Integration proof and delivery", "missing integration proof gate"),
    ("references/readiness-rubric.md", "does not replace executable proof", "missing readiness-proof boundary"),
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
POLICY_SEMANTIC_REQUIREMENTS = (
    ("R01", "Exact extraction with every Light predicate passes routes Light.", "missing exact-extraction Light result"),
    ("R02", "Otherwise use Standard for normal bounded implementation.", "missing Standard default"),
    ("R03", "A single protected-risk trigger establishes Deep.", "missing Deep hard-risk floor"),
    ("R04", "The effective transition is max(next tier, established floor).", "missing max tier-floor transition"),
    ("R05", "Deep wins over Light whenever their signals conflict.", "missing Deep precedence"),
    ("R06", "Deep/xhigh requires review evidence.", "missing Deep/xhigh review evidence"),
    ("R07", "Maximum is eligible when an xhigh Deep attempt gives concrete evidence the central problem remains unresolved,", "missing Maximum xhigh-evidence alternative"),
    ("R08", "De-escalation requires no current hard trigger, frozen reviewed decisions/contracts, an objective oracle, and no critical finding;", "missing de-escalation conditions"),
    ("R09", "a remaining security trigger blocks de-escalation.", "missing remaining-trigger de-escalation block"),
    ("R10", "Count two failures only for two distinct tested hypotheses with the same fingerprint.", "missing repeated-failure fingerprint rule"),
    ("R11", "Reset after a material contract, oracle, signature, or causal-boundary change.", "missing failure-counter reset rule"),
    ("R12", "Ordered is mandatory for a producer-consumer dependency.", "missing producer-consumer ordering rule"),
    ("R13", "Parallel requires a parallel group whose members record chunk IDs, dependencies, frozen current contract IDs/versions/references, exclusive file/state ownership, independent verification, integration owner, and integration order.", "missing relational parallel requirements"),
    ("R14", "Parallel is blocked only by a dependency on another parallel-group member's unfinished output,", "missing unfinished-member parallel dependency block"),
    ("R15", "overlapping state ownership,", "missing ownership parallel block"),
    ("R16", "stale contract version,", "missing stale-contract parallel block"),
    ("R17", "or missing integration owner/order.", "missing integration-order parallel block"),
    ("R18", "Try declared same-tier fallback, then a higher tier;", "missing fallback order"),
    ("R19", "never downshift.", "missing no-downshift fallback rule"),
    ("R20", "Maximum unavailable blocks or forces decomposition.", "missing Maximum-unavailable block"),
    ("R21", "Deep/Maximum require verified observed model and effort meeting the floor; active-runtime execution evidence alone proves this.", "missing Deep/Maximum execution proof"),
    ("R22", "mapping version/digest, alias resolution, observed model/effort, source, and time.", "missing execution-evidence fields"),
    ("R23", "An observed model or effort below the floor blocks the start gate.", "missing below-floor observed-evidence block"),
    ("R24", "A below-floor override remains blocked and readiness remains blocked.", "missing below-floor override block"),
    ("R25", "Author and principal reviewer differ; unresolved findings block review.", "missing independent-review block"),
    ("R26", "Unknown runtimes remain recommendation-only; legacy blueprints cannot resume implementation before schema review.", "missing legacy-or-unknown runtime rule"),
)
POLICY_ADDITIONAL_REQUIREMENTS = (
    ("Establish a hard risk floor before selecting a tier.", "missing hard-floor precedence"),
    ("Within Deep, xhigh requires two independent high-risk triggers", "missing xhigh two-trigger alternative"),
    ("or an unresolved high-effort attempt with a stable root fingerprint.", "missing xhigh stable-fingerprint alternative"),
    ("Routing review records why high is insufficient.", "missing xhigh high-insufficient rationale"),
    ("xhigh does not automatically select Maximum.", "missing xhigh no-automatic-Maximum rule"),
    ("Completed or common prerequisites do not block parallel work.", "missing completed-prerequisite parallel allowance"),
    ("Light requires exact responsibility and output.", "missing Light exact responsibility/output predicate"),
    ("Light requires frozen contracts and inputs.", "missing Light frozen contracts/inputs predicate"),
    ("Light requires a local, reversible blast radius.", "missing Light local/reversible predicate"),
    ("Light requires no protected-risk trigger.", "missing Light protected-risk predicate"),
    ("Light requires an objective oracle.", "missing Light objective-oracle predicate"),
    ("Only search, extraction, classification, summarization, or mechanical transformation qualifies for Light; implementation and open-ended design do not.", "missing Light task-shape restriction"),
    ("Failure of any Light predicate requires Standard or higher.", "missing Light failure result"),
    ("Maximum is exceptional.", "missing Maximum exceptional classification"),
    ("or the hardest single critical-risk decision cannot be decomposed without losing the problem,", "missing Maximum indivisible-critical-risk alternative"),
    ("or principal review records why high and xhigh are insufficient.", "missing Maximum principal-rationale alternative"),
    ("Maximum is not routine implementation, retry without diagnosis, or multiple independent workstreams.", "missing Maximum routine-work exclusion"),
)


class PackageError(Exception):
    def __init__(self, path: str, line: int, reason: str):
        super().__init__(reason)
        self.path = path
        self.line = line
        self.reason = reason

    def __str__(self) -> str:
        return f"{self.path}:{self.line}: {self.reason}"


class RuntimeValidationError(PackageError):
    pass


def _read_text(root: Path, relative: str) -> str:
    path = root / relative
    if not path.exists():
        raise PackageError(relative, 0, "missing required file")
    if path.is_symlink():
        raise PackageError(relative, 0, "nested symlink is not allowed")
    if not path.is_file():
        raise PackageError(relative, 0, "required path is not a regular file")
    try:
        resolved = path.resolve(strict=True)
        resolved.relative_to(root)
    except (OSError, ValueError) as exc:
        raise PackageError(relative, 0, "path escapes supplied skill directory") from exc
    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise RuntimeValidationError(relative, 0, f"cannot read file: {exc.strerror or exc}") from exc
    if relative in METADATA_FILES and len(raw) > MAX_FILE_BYTES:
        raise PackageError(relative, 0, f"file exceeds {MAX_FILE_BYTES} bytes")
    if raw.startswith(b"\xef\xbb\xbf"):
        raise PackageError(relative, 1, "UTF-8 BOM is not allowed")
    bare_cr = re.search(b"\r(?!\n)", raw)
    if bare_cr:
        line = raw.count(b"\n", 0, bare_cr.start()) + 1
        raise PackageError(relative, line, "bare CR newline is not allowed")
    lf_only_positions = [index for index, value in enumerate(raw) if value == 10 and (index == 0 or raw[index - 1] != 13)]
    if b"\r\n" in raw and lf_only_positions:
        line = raw.count(b"\n", 0, lf_only_positions[0]) + 1
        raise PackageError(relative, line, "mixed newline styles are not allowed")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        line = raw.count(b"\n", 0, exc.start) + 1
        raise PackageError(relative, line, "invalid UTF-8") from exc
    if not text.endswith(("\n", "\r\n")):
        raise PackageError(relative, len(text.splitlines()) or 1, "final newline is required")
    return text.replace("\r\n", "\n")


def _validate_tree(root: Path) -> None:
    try:
        entries = list(root.iterdir())
        paths = list(root.rglob("*"))
    except OSError as exc:
        raise RuntimeValidationError(".", 0, f"cannot traverse skill directory: {exc.strerror or exc}") from exc
    for entry in entries:
        if entry.name not in ALLOWED_TOP_LEVEL:
            raise PackageError(entry.name, 0, "unexpected top-level entry")
    for path in paths:
        relative = path.relative_to(root).as_posix()
        if path.is_symlink():
            raise PackageError(relative, 0, "nested symlink is not allowed")
        if path.name == "__pycache__" or path.suffix == ".pyc" or path.name == ".DS_Store":
            raise PackageError(relative, 0, "cache or platform artifact is not allowed")
        if not path.is_file() and not path.is_dir():
            if relative in REQUIRED_FILES:
                raise PackageError(relative, 0, "required path is not a regular file")
            raise PackageError(relative, 0, "non-regular package entry is not allowed")


def _validate_skill_md(root: Path, text: str) -> None:
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        raise PackageError("SKILL.md", 1, "expected frontmatter delimiter")
    if len(lines) < 4 or lines[1] != f"name: {root.name}":
        raise PackageError("SKILL.md", 2, "invalid name metadata")
    if len(lines) < 4 or not lines[2].startswith("description: "):
        raise PackageError("SKILL.md", 3, "expected description metadata")
    if len(lines) < 4 or lines[3] != "---":
        raise PackageError("SKILL.md", 4, "expected frontmatter delimiter")
    if len(root.name) > 64 or not NAME_RE.fullmatch(root.name):
        raise PackageError("SKILL.md", 2, "invalid skill name")
    description = lines[2][len("description: ") :]
    if not 20 <= len(description) <= 500 or not DESCRIPTION_RE.fullmatch(description):
        raise PackageError("SKILL.md", 3, "invalid description")
    if description != description.strip() or "  " in description:
        raise PackageError("SKILL.md", 3, "invalid description whitespace")
    for line_number, line in enumerate(lines[4:], 5):
        if re.match(r"^(name|description):", line):
            raise PackageError("SKILL.md", line_number, "metadata outside frontmatter")


def _decode_openai_value(line: str, key: str, line_number: int) -> str:
    prefix = f"  {key}: "
    if not line.startswith(prefix):
        raise PackageError("agents/openai.yaml", line_number, f"expected {key} metadata")
    encoded = line[len(prefix) :]
    try:
        value = json.loads(encoded)
    except json.JSONDecodeError as exc:
        raise PackageError("agents/openai.yaml", line_number, f"invalid quoted {key}") from exc
    if not isinstance(value, str):
        raise PackageError("agents/openai.yaml", line_number, f"{key} must be a string")
    if any(0xD800 <= ord(character) <= 0xDFFF for character in value):
        raise PackageError("agents/openai.yaml", line_number, f"{key} contains a surrogate code point")
    if any(unicodedata.category(character) == "Cc" for character in value):
        raise PackageError("agents/openai.yaml", line_number, f"invalid {key} control character")
    if value != value.strip():
        raise PackageError("agents/openai.yaml", line_number, f"invalid {key} whitespace")
    return value


def _validate_openai_yaml(text: str) -> None:
    lines = text.splitlines()
    if not lines or lines[0] != "interface:":
        raise PackageError("agents/openai.yaml", 1, "expected interface mapping")
    if len(lines) != 4:
        line = 5 if len(lines) > 4 else len(lines) + 1
        raise PackageError("agents/openai.yaml", line, "unexpected metadata")
    display_name = _decode_openai_value(lines[1], "display_name", 2)
    short_description = _decode_openai_value(lines[2], "short_description", 3)
    default_prompt = _decode_openai_value(lines[3], "default_prompt", 4)
    if not 1 <= len(display_name) <= 64:
        raise PackageError("agents/openai.yaml", 2, "display_name must be 1-64 characters")
    if not 25 <= len(short_description) <= 64:
        raise PackageError("agents/openai.yaml", 3, "short_description must be 25-64 characters")
    if not 1 <= len(default_prompt) <= 500:
        raise PackageError("agents/openai.yaml", 4, "default_prompt must be 1-500 characters")
    if "$blueprint-first-delivery" not in default_prompt:
        raise PackageError("agents/openai.yaml", 4, "default_prompt must contain $blueprint-first-delivery")


def _require(text: str, value: str, relative: str, reason: str) -> None:
    if value not in text:
        raise PackageError(relative, 0, reason)


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
    for _, value, reason in POLICY_SEMANTIC_REQUIREMENTS:
        _require(policy, value, "references/model-routing.md", reason)
    for value, reason in POLICY_ADDITIONAL_REQUIREMENTS:
        _require(policy, value, "references/model-routing.md", reason)
    for value, reason in requirements:
        _require(policy, value, "references/model-routing.md", reason)


def _validate_routing_scenarios(text: str) -> None:
    for scenario_id, pressure_case, expected_result in ROUTING_SCENARIO_ROWS:
        row = f"| {scenario_id} | {pressure_case} | {expected_result} |"
        _require(
            text,
            row,
            ROUTING_SCENARIO_FILE,
            f"routing pressure scenario mismatch: {scenario_id}",
        )


def _validate_outcome_backward_scenarios(text: str) -> None:
    for scenario_id, pressure_case, expected_result in OUTCOME_BACKWARD_SCENARIO_ROWS:
        row = f"| {scenario_id} | {pressure_case} | {expected_result} |"
        _require(
            text,
            row,
            OUTCOME_BACKWARD_SCENARIO_FILE,
            f"outcome-backward pressure scenario mismatch: {scenario_id}",
        )


def _validate_adaptive_evidence_scenarios(text: str) -> None:
    for scenario_id, pressure_case, expected_result in ADAPTIVE_EVIDENCE_SCENARIO_ROWS:
        row = f"| {scenario_id} | {pressure_case} | {expected_result} |"
        _require(
            text,
            row,
            ADAPTIVE_EVIDENCE_SCENARIO_FILE,
            f"adaptive-evidence pressure scenario mismatch: {scenario_id}",
        )


def _validate_adaptive_evidence_contract(files: dict[str, str]) -> None:
    for relative, value, reason in ADAPTIVE_EVIDENCE_REQUIREMENTS:
        _require(files[relative], value, relative, reason)


def _validate_outcome_backward_reference(files: dict[str, str]) -> None:
    for relative, required, reason in OUTCOME_BACKWARD_REFERENCE_REQUIREMENTS:
        _require(files[relative], required, relative, reason)
    text = files["references/outcome-backward-planning.md"]
    reconciliation_header = next(
        (
            line
            for line in text.splitlines()
            if line.startswith("| Trigger ID |")
        ),
        "",
    )
    for field in OUTCOME_BACKWARD_RECONCILIATION_FIELDS:
        _require(
            reconciliation_header,
            field,
            "references/outcome-backward-planning.md",
            f"missing reconciliation report field: {field}",
        )
    template_header = next(
        (
            line
            for line in files["references/blueprint-templates.md"].splitlines()
            if line.startswith("| Trigger ID |")
        ),
        "",
    )
    for field in OUTCOME_BACKWARD_RECONCILIATION_FIELDS:
        _require(
            template_header,
            field,
            "references/blueprint-templates.md",
            f"missing reconciliation template field: {field}",
        )


def _validate_rubric(text: str) -> None:
    for legacy in LEGACY_RUBRIC_ROWS:
        if f"| {legacy} |" in text:
            raise PackageError("references/readiness-rubric.md", 0, "legacy readiness rubric row present")
    if sum(weight for _, weight, _ in RUBRIC_ROWS) != 100:
        raise PackageError("references/readiness-rubric.md", 0, "readiness rubric does not match approved scoring contract")
    expected_table = (
        "| Area | Maximum | Awarded | Deductions |",
        "| --- | ---: | ---: | --- |",
        *(f"| {name} | {weight} |  | {deduction} |" for name, weight, deduction in RUBRIC_ROWS),
        "| **Total** | **100** |  | **Sum awarded points; record every deduction and repair.** |",
    )
    actual_table = tuple(line for line in text.splitlines() if line.startswith("|"))
    if actual_table != expected_table:
        raise PackageError("references/readiness-rubric.md", 0, "readiness rubric does not match approved scoring contract")
    _require(text, "No unresolved critical risk", "references/readiness-rubric.md", "missing critical-risk veto")
    _require(text, "Apply this complete rubric", "references/readiness-rubric.md", "missing per-chunk scoring requirement")
    _require(text, "unscorable", "references/readiness-rubric.md", "missing architecture-evidence hard gate")
    _require(text, "If it is not `PASS`, readiness is **unscorable**.", "references/readiness-rubric.md", "missing unscorable outcome-backward rule")


def _validate_workflow_contract(files: dict[str, str]) -> None:
    requirements = OUTCOME_BACKWARD_WORKFLOW_REQUIREMENTS + (
        ("SKILL.md", "Do not score an existing-codebase blueprint", "missing architecture-evidence hard gate"),
        ("SKILL.md", "literal status `greenfield`", "missing literal greenfield evidence rule"),
        ("SKILL.md", "principal-engineer-style adversarial review", "missing independent adversarial review"),
        ("SKILL.md", "Reviewer must not author", "missing author-reviewer separation"),
        ("SKILL.md", "Before each chunk, satisfy its gate", "missing per-chunk gate requirement"),
        ("SKILL.md", "early vertical proof follows the first compatible", "missing separate integration workflow"),
        ("SKILL.md", "Unit tests alone never satisfy integration", "missing unit-test-only integration veto"),
        ("SKILL.md", "Publish traceability:", "missing final traceability requirement"),
        ("SKILL.md", "Pressure rules:", "missing pressure-resistance rules"),
        ("SKILL.md", "## Blocked gate report", "missing blocked gate report"),
        ("SKILL.md", "Status / pre-code block:", "missing blocked status field"),
        ("SKILL.md", "Route / trigger:", "missing blocked route field"),
        ("SKILL.md", "Architecture / plan:", "missing blocked architecture-evidence field"),
        ("SKILL.md", "Proof / baseline:", "missing blocked proof field"),
        ("SKILL.md", "Ownership / ordering:", "missing blocked ownership field"),
        ("SKILL.md", "Chunk / integration gates:", "missing blocked chunk-gate field"),
        ("SKILL.md", "Traceability:", "missing blocked traceability field"),
        ("SKILL.md", "Agent Brain summaries are continuity aids", "missing Agent Brain boundary"),
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
        ("references/blueprint-templates.md", "Integration result", "missing integration traceability field"),
        ("references/review-and-gate-checklists.md", "Do not score an existing-codebase blueprint", "missing architecture checklist hard gate"),
        ("references/review-and-gate-checklists.md", "under-routing and over-routing", "missing routing review challenge"),
        ("references/review-and-gate-checklists.md", "Deep or Maximum", "missing high-tier execution gate"),
        ("references/review-and-gate-checklists.md", "observed model and effort", "missing observed route evidence"),
        ("references/review-and-gate-checklists.md", "focused tests", "missing focused-test completion gate"),
        ("references/review-and-gate-checklists.md", "blueprint-to-code review", "missing blueprint-to-code review gate"),
        ("references/review-and-gate-checklists.md", "Explicit contract verification", "missing contract verification gate"),
        ("references/review-and-gate-checklists.md", "no unresolved critical assumption", "missing critical-assumption veto"),
        ("tests/pressure-scenarios.md", "## Premature coding", "missing premature-coding pressure scenario"),
        ("tests/pressure-scenarios.md", "## False independence", "missing false-independence pressure scenario"),
        ("tests/pressure-scenarios.md", "## Skipped integration", "missing skipped-integration pressure scenario"),
        ("tests/pressure-scenarios.md", "## Matched combined pressure", "missing matched combined pressure scenario"),
        ("tests/baseline-no-skill.md", "## Matched combined-pressure baseline", "missing matched no-skill behavior probe"),
        ("tests/baseline-no-skill.md", "Workflow controls: **2/8**", "missing no-skill behavior oracle"),
        ("tests/baseline-no-skill.md", "No-guidance repetitions: **5/5**", "missing five-rep no-guidance evidence"),
        ("tests/baseline-no-skill.md", "No-guidance score variance: **0 points**", "missing no-guidance variance review"),
        ("tests/forward-test-with-skill.md", "## Matched combined-pressure probe with skill", "missing matched with-skill behavior probe"),
        ("tests/forward-test-with-skill.md", "Workflow controls: **8/8**", "missing with-skill behavior oracle"),
        ("tests/forward-test-with-skill.md", "Pre-tightening scores: **3, 4, 4, 3, 3**", "missing guided wording-refactor evidence"),
        ("tests/forward-test-with-skill.md", "Final guided repetitions: **5/5**", "missing five-rep guided evidence"),
        ("tests/forward-test-with-skill.md", "Final guided score variance: **0 points**", "missing guided variance review"),
        ("tests/forward-test-with-skill.md", "Compressed-final guided repetitions: **5/5**", "missing compressed-final five-rep evidence"),
        ("tests/forward-test-with-skill.md", "Compressed-final score variance: **0 points**", "missing compressed-final variance review"),
    )
    for relative, value, reason in requirements:
        if (
            relative == "SKILL.md"
            and value == "observed execution"
            and files[relative].count(value) < 2
        ):
            raise PackageError(relative, 0, reason)
        _require(files[relative], value, relative, reason)


def validate(root_argument: str) -> None:
    supplied = Path(root_argument)
    try:
        root = supplied.resolve(strict=True)
    except OSError as exc:
        raise RuntimeValidationError(str(supplied), 0, f"cannot resolve skill directory: {exc.strerror or exc}") from exc
    if not root.is_dir():
        raise RuntimeValidationError(str(supplied), 0, "skill root is not a directory")
    _validate_tree(root)
    files = {relative: _read_text(root, relative) for relative in REQUIRED_FILES}
    _validate_skill_md(root, files["SKILL.md"])
    _validate_openai_yaml(files["agents/openai.yaml"])
    _validate_model_routing(files)
    _validate_routing_scenarios(files[ROUTING_SCENARIO_FILE])
    _validate_outcome_backward_scenarios(files[OUTCOME_BACKWARD_SCENARIO_FILE])
    _validate_adaptive_evidence_scenarios(files[ADAPTIVE_EVIDENCE_SCENARIO_FILE])
    _validate_adaptive_evidence_contract(files)
    _validate_outcome_backward_reference(files)

    skill = files["SKILL.md"]
    templates = files["references/blueprint-templates.md"]
    checklist = files["references/review-and-gate-checklists.md"]
    rubric = files["references/readiness-rubric.md"]
    _require(skill, "4. Explore existing architecture", "SKILL.md", "missing architecture exploration requirement")
    _require(skill, "Record architecture evidence", "SKILL.md", "missing architecture evidence requirement")
    _require(skill, "smallest single-responsibility chunk", "SKILL.md", "missing smallest-chunk requirement")
    _require(skill, "`>=95/100` score", "SKILL.md", "missing per-chunk readiness threshold")
    _require(skill, "not a mathematical probability of correctness or reliability", "SKILL.md", "missing readiness limitation")
    _require(skill, "early vertical proof", "SKILL.md", "missing incremental integration requirement")
    _require(templates, "### Current architecture evidence", "references/blueprint-templates.md", "missing architecture evidence template")
    _require(checklist, "Architecture evidence is recorded", "references/review-and-gate-checklists.md", "missing architecture review gate")
    _validate_rubric(rubric)
    _validate_workflow_contract(files)


def main(argv: list[str]) -> int:
    if sys.version_info < (3, 9):
        print("python:0: CPython 3.9 or newer is required", file=sys.stderr)
        return 2
    if len(argv) != 2:
        print("validate_skill.py:0: usage: validate_skill.py <skill-directory>", file=sys.stderr)
        return 2
    try:
        validate(argv[1])
    except RuntimeValidationError as exc:
        print(exc, file=sys.stderr)
        return 2
    except PackageError as exc:
        print(exc, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
