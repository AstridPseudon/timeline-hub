"""Shared hash helpers for Astrid core."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping
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


def executor_definition_digest(executor_def: Any) -> str:
    """Bind a definition to its admitted source bytes, independent of checkout.

    Folder executors own their folder; external pack executors also own the
    imported pack tree, and Python actions own their whole pack. Runtime
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
    # Folder discovery adds this display label from the physical directory
    # name; it is not an executable declaration or a source identity.
    if metadata.get("source") == "folder":
        payload = {**payload, "metadata": {key: value for key, value in metadata.items() if key != "folder_id"}}

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

    sources = []
    for root in roots:
        if not root.is_dir():
            raise FileNotFoundError(f"admitted executor source root is missing: {root}")
        sources.append([
            (path.relative_to(root).as_posix(), sha256_file(path))
            for path in sorted(root.rglob("*"))
            if path.is_file() and "__pycache__" not in path.relative_to(root).parts
            and path.suffix not in {".pyc", ".pyo"}
        ])

    return canonical_json_digest({"identity_version": 2, "definition": portable(payload), "sources": sources})


__all__ = [
    "canonical_json_digest",
    "executor_definition_digest",
    "sha256_file",
    "validate_digest",
]
