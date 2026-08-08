import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SKILL_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = SKILL_ROOT / "scripts" / "validate_evidence_manifest.py"


def digest(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


class EvidenceManifestValidationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def write_manifest(self, manifest):
        path = self.root / "manifest.json"
        path.write_text(json.dumps(manifest), encoding="utf-8")
        return path

    def run_validator(self, manifest, workspace=None, *args):
        command = [sys.executable, str(VALIDATOR)]
        if workspace is not None:
            command.extend(("--workspace", str(workspace)))
        command.extend(args or (str(self.write_manifest(manifest)),))
        return subprocess.run(command, capture_output=True, text=True, timeout=10)

    def assert_valid(self, manifest, workspace=None):
        result = self.run_validator(manifest, workspace)
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual("", result.stdout)

    def assert_invalid(self, manifest, expected, workspace=None):
        result = self.run_validator(manifest, workspace)
        self.assertEqual(1, result.returncode, result.stderr)
        self.assertEqual("", result.stdout)
        self.assertIn(expected, result.stderr)

    def baseline(self, path=None, value=None):
        files = []
        if path is not None:
            files.append({"path": path, "sha256": digest(value)})
        return {
            "git_ref": "0123456789abcdef",
            "contract_digests": ["contract-v1"],
            "owned_paths": [item["path"] for item in files],
            "files": files,
            "evidence_digest": digest("evidence"),
        }

    def direct_manifest(self):
        return {
            "schema_version": 1,
            "task_id": "copy-change",
            "route": "direct",
            "state": "TASK_PROVEN",
            "route_facts": {"modules": 1, "state_owners": 1, "handoff": False},
            "baseline": self.baseline(),
            "direct_receipt": {
                "outcome": "Copy is corrected",
                "owner": "copy-module",
                "oracle_id": "test_copy",
                "changed_scope": ["src/copy.py"],
                "result": "passed",
                "rollback": "revert the isolated change",
            },
        }

    def lite_manifest(self, handoff=True):
        return {
            "schema_version": 1,
            "task_id": "bounded-change",
            "route": "lite",
            "state": "TASK_PROVEN",
            "route_facts": {"modules": 1, "state_owners": 1, "handoff": handoff},
            "baseline": self.baseline(),
            "lite_card": {
                "outcome": "Bounded behavior is updated",
                "boundary": "presenter-local",
                "invariant": "invalid values remain rejected",
                "owner": "presenter",
                "scope": "one bounded behavior",
                "failure_rollback": "preserve prior behavior on validation failure",
                "oracle_id": "test_presenter",
                "ownership": ["src/presenter.py"],
                "route_reason": "no protected risk; Direct lacks existing oracle",
            },
            "agent_brain": {
                "required": handoff,
                "source_refs": ["docs/blueprints/presenter.md#INV-1"] if handoff else [],
            },
        }

    def full_manifest(self, state="PLAN_FROZEN"):
        proof_status = "PROOF_REQUIRED" if state == "PLAN_FROZEN" else "PROVEN"
        integration_result = "pending" if state == "PLAN_FROZEN" else "passed"
        final_gate = "pending" if state == "PLAN_FROZEN" else "passed"
        return {
            "schema_version": 1,
            "task_id": "profile-save",
            "route": "full",
            "state": state,
            "route_facts": {
                "modules": 2,
                "state_owners": 2,
                "handoff": True,
                "protected_risks": ["persistence"],
            },
            "baseline": self.baseline(),
            "proof_matrix": [{
                "requirement_id": "AC-1",
                "claim_id": "INV-ATOMIC-SAVE",
                "criticality": "critical",
                "owner": "repository",
                "status": proof_status,
                "task_id": "repository-save",
                "oracle_id": "test_atomic_save",
                "expected_result": "save is atomic",
                "evidence_ref": "tests/test_repository.py::test_atomic_save",
                "baseline_ref": "baseline",
                "integration_counterpart": "profile-presenter",
            }],
            "traceability": [{
                "requirement_id": "AC-1",
                "claim_id": "INV-ATOMIC-SAVE",
                "task_id": "repository-save",
                "oracle_id": "test_atomic_save",
                "evidence_ref": "tests/test_repository.py::test_atomic_save",
                "integration_result": integration_result,
            }],
            "agent_brain": {
                "required": True,
                "source_refs": ["docs/blueprints/profile.md#INV-ATOMIC-SAVE"],
            },
            "integration": {
                "required": True,
                "early_vertical_proof": "IT-profile-save",
                "final_gate": final_gate,
            },
        }

    def test_direct_manifest_is_valid(self):
        self.assert_valid(self.direct_manifest())

    def test_direct_requires_deterministic_oracle(self):
        manifest = self.direct_manifest()
        del manifest["direct_receipt"]["oracle_id"]
        self.assert_invalid(manifest, "Direct receipt missing oracle_id")

    def test_lite_handoff_requires_source_linked_agent_brain(self):
        manifest = self.lite_manifest()
        manifest["agent_brain"]["source_refs"] = []
        self.assert_invalid(manifest, "Lite handoff requires source-linked Agent Brain")

    def test_lite_without_handoff_does_not_require_agent_brain(self):
        self.assert_valid(self.lite_manifest(handoff=False))

    def test_full_plan_frozen_allows_named_future_proof(self):
        self.assert_valid(self.full_manifest())

    def test_full_delivery_ready_requires_critical_proof(self):
        manifest = self.full_manifest("DELIVERY_READY")
        manifest["proof_matrix"][0]["status"] = "PROOF_REQUIRED"
        self.assert_invalid(manifest, "critical proof is not PROVEN")

    def test_full_plan_frozen_rejects_critical_assumption(self):
        manifest = self.full_manifest()
        manifest["proof_matrix"][0]["status"] = "ASSUMPTION"
        self.assert_invalid(manifest, "critical proof cannot be ASSUMPTION")

    def test_full_requires_traceability_link_for_each_proof(self):
        manifest = self.full_manifest()
        manifest["traceability"] = []
        self.assert_invalid(manifest, "missing traceability row for AC-1 / INV-ATOMIC-SAVE")

    def test_full_cross_module_work_requires_early_vertical_proof(self):
        manifest = self.full_manifest()
        manifest["integration"]["early_vertical_proof"] = ""
        self.assert_invalid(manifest, "Full cross-module work requires early_vertical_proof")

    def test_full_requires_source_linked_agent_brain(self):
        manifest = self.full_manifest()
        manifest["agent_brain"]["source_refs"] = []
        self.assert_invalid(manifest, "Full work requires source-linked Agent Brain")

    def test_workspace_hash_mismatch_marks_evidence_stale(self):
        workspace = self.root / "workspace"
        changed = workspace / "src" / "profile.txt"
        changed.parent.mkdir(parents=True)
        changed.write_text("changed", encoding="utf-8")
        manifest = self.full_manifest()
        manifest["baseline"] = self.baseline("src/profile.txt", "old")
        self.assert_invalid(manifest, "baseline drift: src/profile.txt", workspace)

    def test_usage_error_is_exit_two(self):
        result = self.run_validator(self.direct_manifest(), None, "one", "two")
        self.assertEqual(2, result.returncode)
        self.assertEqual(
            "validate_evidence_manifest.py:0: usage: "
            "validate_evidence_manifest.py [--workspace PATH] <manifest.json>\n",
            result.stderr,
        )


if __name__ == "__main__":
    unittest.main()
