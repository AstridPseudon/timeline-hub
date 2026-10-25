"""Private D73 admission guard that runs before the pinned launcher."""

from __future__ import annotations

import hashlib
import json
import os
import sys
from pathlib import Path

from check import (
    AGENT,
    RUNTIME_SHA,
    parse_manifest,
    tuple_errors,
)


def runtime_lock_errors() -> list[str]:
    """Check the current Agent lock before the launcher can create evidence."""
    lock_path = AGENT / "runtime.lock.json"
    try:
        lock = json.loads(lock_path.read_text())
        errors = []
        if lock.get("source_commit") != RUNTIME_SHA:
            errors.append("runtime lock source_commit mismatch")
        if lock.get("producer") != "astrid-runtime":
            errors.append("runtime lock producer mismatch")
        files = lock.get("files")
        if not isinstance(files, dict) or len(files) != 15:
            errors.append("runtime lock file count mismatch")
            return errors
        for relative, entry in files.items():
            expected = entry.get("sha256", "").removeprefix("sha256:")
            path = AGENT / relative
            if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
                errors.append(f"runtime lock hash mismatch {relative}")
        return errors
    except (OSError, TypeError, ValueError, AttributeError):
        return [f"runtime lock unreadable: {lock_path}"]


def reject(errors: list[str]) -> int:
    print("D73 pre-admission: rejected before pinned launcher", file=sys.stderr)
    for error in errors:
        print(f"D73 pre-admission: {error}", file=sys.stderr)
    return 2


def main(argv: list[str]) -> int:
    if len(argv) < 5 or argv[3] != "--" or not argv[4:]:
        return reject(["usage: pre-dispatch.py MANIFEST LAUNCHER MODE -- COMMAND..."])

    manifest = Path(argv[0])
    launcher = Path(argv[1])
    mode = argv[2]
    errors: list[str] = []
    if not manifest.is_file():
        errors.append(f"missing manifest {manifest}")
        values = {}
    else:
        values, errors = parse_manifest(manifest.read_text())

    errors.extend(tuple_errors(values))
    errors.extend(runtime_lock_errors())
    expected_launcher = AGENT / "tools" / "p4-d73-pinned-launch.sh"
    if launcher.resolve() != expected_launcher:
        errors.append(f"launcher must be {expected_launcher}")
    if mode != "run":
        errors.append("named rows must use launcher mode run")
    for key in ("P4_D73_EVIDENCE", "P4_D73_REQUEST_ID"):
        if not os.environ.get(key):
            errors.append(f"missing launcher input {key}")

    if errors:
        return reject(errors)

    os.execv(str(launcher), [str(launcher), str(manifest), mode, "--", *argv[4:]])
    return 127


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
