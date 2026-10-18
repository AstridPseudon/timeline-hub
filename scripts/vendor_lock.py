#!/usr/bin/env python3
"""Consumer side of the producer-manifest / vendor.lock.json design (testing plan C1).

    python scripts/vendor_lock.py check <lock>                        local bytes vs lock (default lane, no producer)
    python scripts/vendor_lock.py check <lock> --producer <checkout>  lock vs the producer's manifest (boundary job)
    python scripts/vendor_lock.py update <lock> --producer <checkout> copy from the producer and rewrite the lock

Lock paths are relative to this repo's root. Never hand-edit a lock; run `update`.
Mirrors astrid-app/scripts/vendor-lock.mjs (same CLI, same messages); kept as a copy on purpose (R-5).
"""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
USAGE = "usage: vendor_lock.py check <lock> [--producer <checkout>] | update <lock> --producer <checkout>"


def digest(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def _read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _re_vendor(lock_path: Path, lock: dict, root: Path) -> str:
    try:
        shown = lock_path.relative_to(root).as_posix()
    except ValueError:
        shown = str(lock_path)
    return f"re-vendor with: python scripts/vendor_lock.py update {shown} --producer <{lock['producer']} checkout>"


def check(lock_path: Path, producer: Path | None = None, root: Path = ROOT) -> list[str]:
    """Return one line per problem (empty list means the lock holds)."""
    lock_path = Path(lock_path).resolve()
    lock = _read(lock_path)
    problems = []
    for consumer_path, entry in lock["files"].items():
        try:
            actual = digest(root / consumer_path)
        except OSError:
            problems.append(f"{consumer_path}: missing")
            continue
        if actual != entry["sha256"]:
            problems.append(f"{consumer_path}: edited locally")
    if problems:
        return [*problems, _re_vendor(lock_path, lock, root)]
    if producer is not None:
        manifest = _read(Path(producer) / lock["manifest"])
        changed = [e["from"] for e in lock["files"].values() if manifest["artifacts"].get(e["from"]) != e["sha256"]]
        # Only the vendored files count; the lock keeps producer_version as provenance.
        if changed:
            return [f"producer changed: {', '.join(changed)}", _re_vendor(lock_path, lock, root)]
    return []


def update(lock_path: Path, producer: Path, root: Path = ROOT) -> str:
    lock_path = Path(lock_path).resolve()
    producer = Path(producer).resolve()
    lock = _read(lock_path)
    manifest = _read(producer / lock["manifest"])
    for consumer_path, entry in lock["files"].items():
        target = root / consumer_path
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(producer / entry["from"], target)
        entry["sha256"] = digest(target)
        if manifest["artifacts"].get(entry["from"]) != entry["sha256"]:
            raise SystemExit(f"{entry['from']}: producer manifest is stale (run its artifact_manifest.py)")
    lock["producer_version"] = manifest["version"]
    lock["source_commit"] = subprocess.run(
        ["git", "-C", str(producer), "rev-parse", "HEAD"], check=True, capture_output=True, text=True
    ).stdout.strip()
    lock_path.write_text(json.dumps(lock, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return f"updated {_rel(lock_path, root)} from {lock['producer']} {lock['source_commit'][:12]}"


def _rel(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return str(path)


def main(argv: list[str]) -> int:
    if len(argv) < 2 or argv[0] not in ("check", "update"):
        print(USAGE, file=sys.stderr)
        return 1
    command, lock_arg, rest = argv[0], argv[1], argv[2:]
    producer: Path | None = None
    if "--producer" in rest:
        at = rest.index("--producer") + 1
        producer = Path(rest[at] if at < len(rest) else "").resolve()  # as the mjs: a missing value is the cwd
    if command == "update" and producer is None:
        print(USAGE, file=sys.stderr)
        return 1
    lock_path = Path(lock_arg).resolve()
    if command == "update":
        assert producer is not None
        print(update(lock_path, producer))
        return 0
    problems = check(lock_path, producer)
    if problems:
        print("\n".join(problems), file=sys.stderr)
        return 1
    print(f"ok {_rel(lock_path, ROOT)}{' (matches producer manifest)' if producer else ''}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
