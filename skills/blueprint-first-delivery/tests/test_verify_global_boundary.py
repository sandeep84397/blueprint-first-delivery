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

    def test_non_string_path_is_rejected(self):
        self.write_baseline([
            {"path": None, "state": "absent"},
        ])
        result = self.run_verifier()
        self.assertEqual(2, result.returncode)
        self.assertIn("invalid baseline", result.stderr)


if __name__ == "__main__":
    unittest.main()
