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
