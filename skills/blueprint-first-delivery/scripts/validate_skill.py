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
REQUIRED_FILES = (
    "SKILL.md",
    "agents/openai.yaml",
    "references/blueprint-templates.md",
    "references/readiness-rubric.md",
    "references/review-and-gate-checklists.md",
    "scripts/validate_skill.py",
    "tests/pressure-scenarios.md",
    "tests/baseline-no-skill.md",
    "tests/forward-test-with-skill.md",
    "tests/validate-skill.sh",
    "tests/test-validator-negative-fixtures.sh",
    "tests/test_validate_skill.py",
)
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


def _validate_workflow_contract(files: dict[str, str]) -> None:
    requirements = (
        ("SKILL.md", "Do not score an existing-codebase blueprint", "missing architecture-evidence hard gate"),
        ("SKILL.md", "literal status `greenfield`", "missing literal greenfield evidence rule"),
        ("SKILL.md", "principal-engineer-style adversarial review", "missing independent adversarial review"),
        ("SKILL.md", "Reviewer must not author", "missing author-reviewer separation"),
        ("SKILL.md", "Before each chunk, satisfy its chunk gate", "missing per-chunk gate requirement"),
        ("SKILL.md", "execute the separate integration blueprint", "missing separate integration workflow"),
        ("SKILL.md", "Unit tests alone never satisfy integration", "missing unit-test-only integration veto"),
        ("SKILL.md", "Publish a traceability report", "missing final traceability requirement"),
        ("SKILL.md", "Pressure rules:", "missing pressure-resistance rules"),
        ("SKILL.md", "## Blocked gate report", "missing blocked gate report"),
        ("SKILL.md", "Status / pre-code block:", "missing blocked status field"),
        ("SKILL.md", "Architecture evidence:", "missing blocked architecture-evidence field"),
        ("SKILL.md", "Independent review:", "missing blocked independent-review field"),
        ("SKILL.md", "principal-engineer-style reviewer =", "missing blocked principal-reviewer subfield"),
        ("SKILL.md", "distinct from author =", "missing blocked reviewer-separation subfield"),
        ("SKILL.md", "Readiness / veto:", "missing blocked readiness field"),
        ("SKILL.md", "overall score =", "missing blocked overall-score subfield"),
        ("SKILL.md", "every chunk score =", "missing blocked per-chunk-score subfield"),
        ("SKILL.md", "threshold for both = >=95/100", "missing blocked readiness-threshold subfield"),
        ("SKILL.md", "Ownership / ordering:", "missing blocked ownership field"),
        ("SKILL.md", "Chunk gates:", "missing blocked chunk-gate field"),
        ("SKILL.md", "start gate =", "missing blocked start-gate subfield"),
        ("SKILL.md", "completion gate =", "missing blocked completion-gate subfield"),
        ("SKILL.md", "Integration gate:", "missing blocked integration-gate field"),
        ("SKILL.md", "separate blueprint =", "missing blocked integration-blueprint subfield"),
        ("SKILL.md", "separate gate =", "missing blocked separate-gate subfield"),
        ("SKILL.md", "Traceability:", "missing blocked traceability field"),
        ("SKILL.md", "optional Agent Brain", "missing optional Agent Brain boundary"),
        ("references/blueprint-templates.md", "Integration result", "missing integration traceability field"),
        ("references/review-and-gate-checklists.md", "Do not score an existing-codebase blueprint", "missing architecture checklist hard gate"),
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

    skill = files["SKILL.md"]
    templates = files["references/blueprint-templates.md"]
    checklist = files["references/review-and-gate-checklists.md"]
    rubric = files["references/readiness-rubric.md"]
    _require(skill, "1. Explore the existing architecture", "SKILL.md", "missing architecture exploration requirement")
    _require(skill, "Record architecture evidence", "SKILL.md", "missing architecture evidence requirement")
    _require(skill, "smallest single-responsibility chunk", "SKILL.md", "missing smallest-chunk requirement")
    _require(skill, ">= 95/100 readiness", "SKILL.md", "missing per-chunk readiness threshold")
    _require(skill, "not a mathematical probability of correctness or reliability", "SKILL.md", "missing readiness limitation")
    _require(skill, "Incrementally integrate", "SKILL.md", "missing incremental integration requirement")
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
