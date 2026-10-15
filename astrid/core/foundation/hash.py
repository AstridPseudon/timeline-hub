"""Shared hash helpers for Astrid core."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Iterator, Mapping
from pathlib import Path
from typing import Any


def sha256_file(path: Path) -> str:
    """Return the SHA-256 hex digest of *path* using 1 MB chunked reads."""

    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_digest(digest: object) -> str:
    """Validate and return one lowercase bare SHA-256 digest.

    This is a neutral byte-identity primitive.  It deliberately has no
    filesystem, CAS, project, or media-ingest knowledge so live consumers can
    validate runtime-managed object handoffs without importing retired storage
    code.
    """

    if not isinstance(digest, str):
        raise TypeError("digest must be a string")
    if len(digest) != 64 or any(char not in "0123456789abcdef" for char in digest):
        raise ValueError("digest must be a lowercase 64-hex SHA-256")
    return digest


def canonical_json_digest(obj: Any) -> str:
    """Return the stable digest used by protocol identity contracts."""

    raw = json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


# These are source-tree roles, not a source-extension allowlist. Unknown files
# stay admitted: helpers, schemas, templates, prompts and built runtime assets
# need not be Python, nor live beside the entrypoint. In particular, docs can
# contain executable scripts and pinned runtime resources.
_EXECUTION_CACHE_DIRS = frozenset({
    ".git", "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache",
})
_DOCUMENTATION_NAMES = frozenset({"AGENTS.md", "README.md", "SKILL.md", "STAGE.md"})
_DOCUMENTATION_SECTIONS = frozenset({"reference", "references", "setup"})


def _is_execution_source(relative: Path, *, declared: bool = False) -> bool:
    """Admit tree members except known debris and conventional prose docs.

    Prose in docs root/reference/setup sections and folder guides is excluded;
    other docs subtrees may hold runtime assets (including Markdown prompts).
    Do not exclude build/dist trees, JSON, text, or all of docs: those can be
    required execution inputs. This is a bounded tree contract, not import or
    cross-capability dependency discovery.
    """
    if any(part in _EXECUTION_CACHE_DIRS for part in relative.parts[:-1]):
        return False
    if relative.name in {".git", ".DS_Store"} or relative.suffix in {".pyc", ".pyo"}:
        return False
    # A file explicitly named by the definition (e.g. a command argument or
    # schema URI) is a runtime input even if it has a documentation-shaped name.
    if declared:
        return True
    if relative.name in _DOCUMENTATION_NAMES:
        return False
    if relative.suffix in {".md", ".rst"}:
        if "guides" in relative.parts[:-1]:
            return False
        for index, part in enumerate(relative.parts[:-1]):
            if part == "docs" and (len(relative.parts) == index + 2
                                   or relative.parts[index + 1] in _DOCUMENTATION_SECTIONS):
                return False
    return True


def _definition_strings(value: Any) -> Iterator[str]:
    if isinstance(value, Mapping):
        for item in value.values():
            yield from _definition_strings(item)
    elif isinstance(value, (list, tuple)):
        for item in value:
            yield from _definition_strings(item)
    elif isinstance(value, str):
        yield value


def executor_definition_digest(executor_def: Any) -> str:
    """Bind a definition to its admitted source bytes, independent of checkout.

    Folder executors own their folder; external pack executors also own the
    imported pack tree, and Python actions own their pack's execution tree.
    The tree excludes only conventional prose docs and known generated caches;
    executable helpers, schemas and runtime resources remain admitted. Runtime
    authority still carries the actual absolute paths separately. Identity
    uses relative paths and contents, never timestamps or Python bytecode.
    Definitions with no filesystem source retain their existing digest.
    """
    payload = executor_def.to_dict() if hasattr(executor_def, "to_dict") else executor_def
    metadata = payload.get("metadata", {})
    roots: list[Path] = []
    if metadata.get("action_invocation"):
        roots.append(Path(metadata["pack_root"]).expanduser().resolve())
    else:
        folder = metadata.get("executor_root") or metadata.get("orchestrator_root")
        if folder:
            roots.append(Path(folder).expanduser().resolve())
            if payload.get("kind") == "external" and metadata.get("pack_root"):
                roots.append(Path(metadata["pack_root"]).expanduser().resolve())
    roots = list(dict.fromkeys(roots))
    if not roots:
        return canonical_json_digest(payload)
    # Folder discovery adds labels and inventories, including STAGE.md and
    # generated debris in assets/guides. Their presence must not reintroduce
    # excluded files through the definition. Execution bytes are covered below;
    # authority keeps the original metadata. Pack attachment changes `source`
    # to `pack`, so recognize the folder root rather than that display label.
    folder_root = metadata.get("executor_root") or metadata.get("orchestrator_root")
    if folder_root and metadata.get("source") in {"folder", "pack"}:
        folder_root = Path(folder_root).expanduser().resolve()
        inventory_fields = set()
        for key, expected in (("folder_id", folder_root.name),
                              ("stage_file", str(folder_root / "STAGE.md"))):
            if metadata.get(key) == expected:
                inventory_fields.add(key)
        for dirname, dir_key, files_key in (("assets", "assets_dir", "asset_files"),
                                            ("guides", "guides_dir", "guide_files")):
            if metadata.get(dir_key) == str(folder_root / dirname):
                inventory_fields.update((dir_key, files_key))
        payload = {**payload, "metadata": {
            key: value for key, value in metadata.items() if key not in inventory_fields
        }}

    def portable(value: Any) -> Any:
        if isinstance(value, Mapping):
            return {key: portable(item) for key, item in value.items()}
        if isinstance(value, (list, tuple)):
            return [portable(item) for item in value]
        if isinstance(value, str):
            for index, root in enumerate(roots):
                uri = root.as_uri()
                if value == uri or value.startswith(uri + "/"):
                    return f"source:{index}" + value[len(uri):]
                path = Path(value)
                if not path.is_absolute():
                    continue
                if path.is_relative_to(root):
                    return f"source:{index}/{path.relative_to(root).as_posix()}"
        return value

    declared_strings = set(_definition_strings(payload))
    sources = []
    for root in roots:
        if not root.is_dir():
            raise FileNotFoundError(f"admitted executor source root is missing: {root}")
        sources.append([
            (path.relative_to(root).as_posix(), sha256_file(path))
            for path in sorted(root.rglob("*"))
            if path.is_file() and _is_execution_source(
                path.relative_to(root), declared=bool(declared_strings.intersection({
                    path.relative_to(root).as_posix(), str(path), path.as_uri(),
                })),
            )
        ])

    return canonical_json_digest({"identity_version": 2, "definition": portable(payload), "sources": sources})


__all__ = [
    "canonical_json_digest",
    "executor_definition_digest",
    "sha256_file",
    "validate_digest",
]
