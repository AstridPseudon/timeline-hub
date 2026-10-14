"""Project canonical v2/v3 declared resources for source packaging."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from astrid.core.pack.canonical import BundledCatalog, CanonicalPackError


@dataclass(frozen=True)
class SourceResourceClosure:
    paths: tuple[str, ...]
    errors: tuple[str, ...] = ()

    @property
    def ok(self) -> bool:
        return not self.errors


def check_source_resource_closure(repository_root: str | Path) -> SourceResourceClosure:
    root = Path(repository_root).expanduser().resolve()
    errors: list[str] = []
    paths: set[str] = set()
    try:
        catalog = BundledCatalog.from_root(root / "astrid" / "packs")
    except CanonicalPackError as exc:
        return SourceResourceClosure((), (f"invalid bundled catalog: {exc}",))
    for entry in catalog.entries:
        owner = entry.root.resolve()
        for handle in (entry.manifest, *entry.resource_handles):
            if handle.kind.startswith("content:"):
                continue
            relative = f"astrid/packs/{entry.id}/{handle.path}"
            paths.add(relative)
            try:
                resolved = handle.resolved.resolve()
                if not resolved.is_relative_to(owner):
                    errors.append(f"{relative}: resolved outside owner root")
                if handle.file_kind != "file" or not resolved.is_file():
                    errors.append(f"{relative}: declared handle is not a regular file")
            except OSError as exc:
                errors.append(f"{relative}: cannot inspect resolved handle: {exc}")
    # V3 moved the core authored guidance from ``skill/`` to ``docs/``. Keep
    # the legacy fallback for a V2 source snapshot, but never report a V3
    # checkout as incomplete merely because its old path is absent.
    core_candidates = (
        root / "astrid" / "packs" / "_core" / "docs" / "SKILL.md",
        root / "astrid" / "packs" / "_core" / "skill" / "SKILL.md",
    )
    core_skill = next((path for path in core_candidates if path.is_file()), None)
    if core_skill is None:
        expected = ", ".join(path.relative_to(root).as_posix() for path in core_candidates)
        errors.append(f"core census guidance is not a regular file (expected one of: {expected})")
    else:
        paths.add(core_skill.relative_to(root).as_posix())
    return SourceResourceClosure(tuple(sorted(paths)), tuple(sorted(set(errors))))


def declared_source_resource_paths(repository_root: str | Path) -> tuple[str, ...]:
    closure = check_source_resource_closure(repository_root)
    if not closure.ok:
        raise ValueError("source resource closure failed: " + "; ".join(closure.errors))
    return closure.paths


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=Path.cwd())
    args = parser.parse_args(argv)
    closure = check_source_resource_closure(args.root)
    print(json.dumps({"ok": closure.ok, "paths": closure.paths, "errors": closure.errors}))
    return 0 if closure.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())


__all__ = [
    "SourceResourceClosure",
    "check_source_resource_closure",
    "declared_source_resource_paths",
]
