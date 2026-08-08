#!/usr/bin/env python3
"""Validate adaptive evidence-first work manifests without external dependencies."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys


ROUTES = {"direct", "lite", "full"}
STATES = {
    "TRIAGED",
    "ARCHITECTURE_APPROVED",
    "PLAN_FROZEN",
    "TASK_PROVEN",
    "INTEGRATION_PROVEN",
    "DELIVERY_READY",
    "BLOCKED",
    "STALE",
}
PLANNING_STATES = {"ARCHITECTURE_APPROVED", "PLAN_FROZEN"}
PROVEN_STATES = {"TASK_PROVEN", "INTEGRATION_PROVEN", "DELIVERY_READY"}
PROOF_FIELDS = (
    "requirement_id",
    "claim_id",
    "criticality",
    "owner",
    "status",
    "task_id",
    "oracle_id",
    "expected_result",
    "evidence_ref",
    "baseline_ref",
    "integration_counterpart",
)


class ManifestError(Exception):
    def __init__(self, reason: str):
        super().__init__(reason)
        self.reason = reason


class RuntimeValidationError(ManifestError):
    pass


def _require_mapping(value, label: str) -> dict:
    if not isinstance(value, dict):
        raise ManifestError(f"{label} must be an object")
    return value


def _require_list(value, label: str) -> list:
    if not isinstance(value, list):
        raise ManifestError(f"{label} must be an array")
    return value


def _require_string(mapping: dict, key: str, label: str | None = None) -> str:
    value = mapping.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ManifestError(f"{label or key} missing {key}")
    return value


def _require_bool(mapping: dict, key: str, label: str) -> bool:
    value = mapping.get(key)
    if not isinstance(value, bool):
        raise ManifestError(f"{label} missing {key}")
    return value


def _is_digest(value: str) -> bool:
    return len(value) == 64 and all(char in "0123456789abcdef" for char in value.casefold())


def _validate_baseline(manifest: dict) -> dict:
    baseline = _require_mapping(manifest.get("baseline"), "baseline")
    _require_string(baseline, "git_ref", "baseline")
    _require_list(baseline.get("contract_digests"), "baseline contract_digests")
    owned_paths = _require_list(baseline.get("owned_paths"), "baseline owned_paths")
    if not all(isinstance(path, str) and path for path in owned_paths):
        raise ManifestError("baseline owned_paths contains invalid path")
    evidence_digest = _require_string(baseline, "evidence_digest", "baseline")
    if not _is_digest(evidence_digest):
        raise ManifestError("baseline evidence_digest must be SHA-256")
    files = _require_list(baseline.get("files"), "baseline files")
    for item in files:
        file_entry = _require_mapping(item, "baseline file")
        path = _require_string(file_entry, "path", "baseline file")
        file_digest = _require_string(file_entry, "sha256", "baseline file")
        if path not in owned_paths:
            raise ManifestError(f"baseline file is not owned: {path}")
        if not _is_digest(file_digest):
            raise ManifestError(f"baseline digest must be SHA-256: {path}")
    return baseline


def _validate_direct(manifest: dict) -> None:
    receipt = _require_mapping(manifest.get("direct_receipt"), "Direct receipt")
    for key in ("outcome", "owner", "oracle_id", "changed_scope", "result", "rollback"):
        if key == "changed_scope":
            scope = _require_list(receipt.get(key), "Direct receipt changed_scope")
            if not scope or not all(isinstance(path, str) and path for path in scope):
                raise ManifestError("Direct receipt changed_scope must name changed files or state")
        else:
            _require_string(receipt, key, "Direct receipt")


def _source_linked_agent_brain(manifest: dict, message: str) -> None:
    brain = _require_mapping(manifest.get("agent_brain"), "Agent Brain")
    if brain.get("required") is not True:
        raise ManifestError(message)
    refs = _require_list(brain.get("source_refs"), "Agent Brain source_refs")
    if not refs or not all(isinstance(ref, str) and ref.strip() for ref in refs):
        raise ManifestError(message)


def _validate_lite(manifest: dict) -> None:
    card = _require_mapping(manifest.get("lite_card"), "Lite card")
    for key in (
        "outcome",
        "boundary",
        "invariant",
        "owner",
        "scope",
        "failure_rollback",
        "oracle_id",
        "route_reason",
    ):
        _require_string(card, key, "Lite card")
    ownership = _require_list(card.get("ownership"), "Lite card ownership")
    if not ownership or not all(isinstance(value, str) and value for value in ownership):
        raise ManifestError("Lite card ownership must be non-empty")
    facts = _require_mapping(manifest.get("route_facts"), "route_facts")
    handoff = _require_bool(facts, "handoff", "route_facts")
    if handoff:
        _source_linked_agent_brain(
            manifest,
            "Lite handoff requires source-linked Agent Brain",
        )


def _validate_full(manifest: dict) -> None:
    facts = _require_mapping(manifest.get("route_facts"), "route_facts")
    modules = facts.get("modules")
    if not isinstance(modules, int) or modules < 1:
        raise ManifestError("Full route_facts missing modules")
    _source_linked_agent_brain(manifest, "Full work requires source-linked Agent Brain")

    state = manifest["state"]
    proofs = _require_list(manifest.get("proof_matrix"), "proof_matrix")
    if not proofs:
        raise ManifestError("Full work requires proof_matrix")
    traceability = _require_list(manifest.get("traceability"), "traceability")
    trace_keys = set()
    for row in traceability:
        item = _require_mapping(row, "traceability row")
        key = (
            _require_string(item, "requirement_id", "traceability row"),
            _require_string(item, "claim_id", "traceability row"),
            _require_string(item, "task_id", "traceability row"),
            _require_string(item, "oracle_id", "traceability row"),
            _require_string(item, "evidence_ref", "traceability row"),
        )
        _require_string(item, "integration_result", "traceability row")
        trace_keys.add(key)

    for row in proofs:
        proof = _require_mapping(row, "proof row")
        for field in PROOF_FIELDS:
            _require_string(proof, field, "proof row")
        if proof["criticality"] not in {"critical", "non-critical"}:
            raise ManifestError("proof row criticality must be critical or non-critical")
        if proof["status"] not in {
            "FACT",
            "ASSUMPTION",
            "PROOF_REQUIRED",
            "PROVEN",
            "BLOCKED",
            "STALE",
        }:
            raise ManifestError("proof row has invalid status")
        trace_key = (
            proof["requirement_id"],
            proof["claim_id"],
            proof["task_id"],
            proof["oracle_id"],
            proof["evidence_ref"],
        )
        if trace_key not in trace_keys:
            raise ManifestError(
                "missing traceability row for "
                f"{proof['requirement_id']} / {proof['claim_id']}"
            )
        if proof["criticality"] != "critical":
            continue
        status = proof["status"]
        if state in PLANNING_STATES and status in {"ASSUMPTION", "BLOCKED", "STALE"}:
            raise ManifestError(f"critical proof cannot be {status}")
        if state in PROVEN_STATES and status != "PROVEN":
            raise ManifestError("critical proof is not PROVEN")

    if modules > 1:
        integration = _require_mapping(manifest.get("integration"), "integration")
        if integration.get("required") is not True:
            raise ManifestError("Full cross-module work requires integration")
        if not isinstance(integration.get("early_vertical_proof"), str) or not integration[
            "early_vertical_proof"
        ].strip():
            raise ManifestError("Full cross-module work requires early_vertical_proof")
        if state in {"INTEGRATION_PROVEN", "DELIVERY_READY"}:
            if integration.get("final_gate") != "passed":
                raise ManifestError("Full integration final_gate is not passed")


def _validate_manifest(manifest: dict) -> dict:
    _require_mapping(manifest, "manifest")
    if manifest.get("schema_version") != 1:
        raise ManifestError("schema_version must be 1")
    _require_string(manifest, "task_id", "manifest")
    route = manifest.get("route")
    if route not in ROUTES:
        raise ManifestError("route must be direct, lite, or full")
    state = manifest.get("state")
    if state not in STATES:
        raise ManifestError("state is invalid")
    _require_mapping(manifest.get("route_facts"), "route_facts")
    _validate_baseline(manifest)
    if route == "direct":
        _validate_direct(manifest)
    elif route == "lite":
        _validate_lite(manifest)
    else:
        _validate_full(manifest)
    return manifest


def _validate_workspace(baseline: dict, workspace: Path) -> None:
    try:
        root = workspace.resolve(strict=True)
    except OSError as exc:
        raise RuntimeValidationError(
            f"workspace cannot be resolved: {exc.strerror or exc}"
        ) from exc
    if not root.is_dir():
        raise RuntimeValidationError("workspace is not a directory")
    for item in baseline["files"]:
        relative = Path(item["path"])
        if relative.is_absolute() or ".." in relative.parts:
            raise ManifestError(f"baseline path escapes workspace: {item['path']}")
        candidate = root / relative
        try:
            resolved = candidate.resolve(strict=True)
            resolved.relative_to(root)
            actual = hashlib.sha256(resolved.read_bytes()).hexdigest()
        except (OSError, ValueError):
            actual = None
        if actual != item["sha256"]:
            raise ManifestError(
                f"baseline drift: {item['path']}; mark affected evidence STALE and re-approve"
            )


def _read_manifest(path_argument: str) -> dict:
    path = Path(path_argument)
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise RuntimeValidationError(
            f"manifest cannot be read: {exc.strerror or exc}"
        ) from exc
    try:
        value = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ManifestError(f"invalid JSON at line {exc.lineno}") from exc
    return _require_mapping(value, "manifest")


def _usage() -> str:
    return (
        "validate_evidence_manifest.py:0: usage: "
        "validate_evidence_manifest.py [--workspace PATH] <manifest.json>"
    )


def main(argv: list[str]) -> int:
    workspace = None
    arguments = argv[1:]
    if len(arguments) == 3 and arguments[0] == "--workspace":
        workspace = Path(arguments[1])
        manifest_argument = arguments[2]
    elif len(arguments) == 1:
        manifest_argument = arguments[0]
    else:
        print(_usage(), file=sys.stderr)
        return 2
    try:
        manifest = _validate_manifest(_read_manifest(manifest_argument))
        if workspace is not None:
            _validate_workspace(manifest["baseline"], workspace)
    except RuntimeValidationError as exc:
        print(f"validate_evidence_manifest.py:0: {exc.reason}", file=sys.stderr)
        return 2
    except ManifestError as exc:
        print(f"validate_evidence_manifest.py:0: {exc.reason}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
