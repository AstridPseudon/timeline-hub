"""Candidate normal first-use route for the farm's owned bench store.

This deliberately delegates creation and validation to the reviewed
``bench_store.Store`` API.  It never adopts an existing unknown root.
"""

from __future__ import annotations

import argparse
import importlib.util
import sys
from pathlib import Path


class Refused(RuntimeError):
    """The requested normal route is not safe for this root."""


def _absolute_directory(path: Path, label: str) -> Path:
    if not path.is_absolute() or path != path.resolve() or path.is_symlink() or not path.is_dir():
        raise Refused(f"{label} must be an existing physical directory")
    return path


def _load_store(module_path: Path):
    if not module_path.is_absolute() or module_path != module_path.resolve():
        raise Refused("bench-store helper must be an absolute physical path")
    if module_path.is_symlink() or not module_path.is_file():
        raise Refused("bench-store helper is missing or not a regular file")
    spec = importlib.util.spec_from_file_location("farm_agent_full_bench_store", module_path)
    if spec is None or spec.loader is None:
        raise Refused("bench-store helper cannot be loaded")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if not hasattr(module, "Store"):
        raise Refused("bench-store helper has no Store API")
    return module.Store


def _validate_store(store) -> None:
    """Run the store's supported ownership and inode checks before reading it."""

    with store.mutex():
        store._load()


def open_or_initialize(*, orch_root: Path, store_root: Path, bench_store: Path) -> tuple[str, str]:
    """Open a valid store or initialize only a truly absent store.

    The returned tuple is ``(mode, owner_id)``.  ``Store`` performs all owner,
    directory, mutex, index, and projection validation; this wrapper does not
    recreate any of those records.
    """

    orch_root = _absolute_directory(orch_root, "farm ORCH root")
    tests_dir = orch_root / "tests"
    _absolute_directory(tests_dir, "farm ORCH/tests")
    store_root = Path(store_root)
    if not store_root.is_absolute() or store_root != store_root.resolve() or store_root.is_symlink():
        raise Refused("bench-store root must be an absolute non-symlink path")
    Store = _load_store(Path(bench_store))

    try:
        if store_root.exists():
            if not store_root.is_dir():
                raise Refused("bench-store root is not a directory")
            mode = "reused"
            store = Store(store_root, tests_dir)
        else:
            mode = "initialized"
            store = Store.initialize(store_root, tests_dir)

        # Exercise the existing ownership/inode and index validators, then
        # reopen through the same supported constructor to prove owner
        # identity survives init.
        _validate_store(store)
        reopened = Store(store_root, tests_dir)
        _validate_store(reopened)
    except RuntimeError as exc:
        # The reviewed helper uses its own Refused subclass of RuntimeError.
        raise Refused(str(exc)) from exc
    owner_id = reopened.owner["id"]
    if not isinstance(owner_id, str) or not owner_id:
        raise Refused("store owner identity is empty")
    return mode, owner_id


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--orch-root", required=True, type=Path)
    parser.add_argument("--store-root", required=True, type=Path)
    parser.add_argument("--bench-store", required=True, type=Path)
    args = parser.parse_args(argv)
    try:
        mode, owner_id = open_or_initialize(
            orch_root=args.orch_root,
            store_root=args.store_root,
            bench_store=args.bench_store,
        )
    except (Refused, OSError, ValueError, TypeError, KeyError) as exc:
        print(f"REFUSED: {exc}", file=sys.stderr)
        return 2
    print(f"{mode} owner={owner_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
