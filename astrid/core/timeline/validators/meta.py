"""Validation for the opaque ``meta`` extension at authored timeline seams.

The contents of a namespace are deliberately not interpreted here.  This
module only checks the bounded JSON envelope needed to admit and preserve the
extension without allowing it to become a second reference or timing model.
"""

from __future__ import annotations

import json
import math
import re
from collections.abc import Mapping
from typing import Any

META_MAX_NAMESPACES = 64
META_MAX_NAMESPACE_BYTES = 65_536
META_MAX_BYTES = 262_144
META_MAX_CONTAINER_DEPTH = 32
META_NAMESPACE_RE = re.compile(r"^[a-z][a-z0-9]*(?:[.-][a-z0-9]+)*$")


class MetaValidationError(ValueError):
    """A structured validation failure for one admitted ``meta`` location."""

    def __init__(self, code: str, path: str, hint: str) -> None:
        self.code = code
        self.path = path
        self.hint = hint
        self.message = f"{path}: {hint}"
        self.details = {"code": code, "path": path, "hint": hint}
        super().__init__(self.message)


def _invalid(path: str, hint: str) -> MetaValidationError:
    return MetaValidationError("invalid_meta", path, hint)


def _limited(path: str, hint: str) -> MetaValidationError:
    return MetaValidationError("meta_limit_exceeded", path, hint)


def _validate_descendant(value: Any, path: str, *, depth: int) -> None:
    if value is None or isinstance(value, (str, bool, int)):
        return
    if isinstance(value, float):
        if not math.isfinite(value):
            raise _invalid(path, "must contain only finite JSON numbers")
        return
    if isinstance(value, dict):
        if depth > META_MAX_CONTAINER_DEPTH:
            raise _limited(
                path,
                f"nested containers must be at most {META_MAX_CONTAINER_DEPTH} levels below the namespace root",
            )
        for key, child in value.items():
            if not isinstance(key, str):
                raise _invalid(f"{path}.{key!r}", "object keys must be strings")
            _validate_descendant(child, f"{path}.{key}", depth=depth + 1)
        return
    if isinstance(value, list):
        if depth > META_MAX_CONTAINER_DEPTH:
            raise _limited(
                path,
                f"nested containers must be at most {META_MAX_CONTAINER_DEPTH} levels below the namespace root",
            )
        for index, child in enumerate(value):
            _validate_descendant(child, f"{path}[{index}]", depth=depth + 1)
        return
    raise _invalid(path, "must contain only finite JSON values")


def _canonical_bytes(value: Any, path: str) -> int:
    try:
        encoded = json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        ).encode("utf-8")
    except (TypeError, UnicodeError, ValueError) as exc:  # pragma: no cover - guarded by the walk above
        raise _invalid(path, "must contain only finite JSON values") from exc
    return len(encoded)


def validate_meta(meta: Any, *, path: str = "meta") -> None:
    """Validate one authored ``meta`` object without changing its value.

    ``meta`` is optional at its call sites; callers invoke this function only
    when the key is present.  No descendant is inspected for IDs, references,
    or schema-owned fields.
    """

    if not isinstance(meta, dict):
        raise _invalid(path, "must be an object; omit it or remove it explicitly to clear it")
    if len(meta) > META_MAX_NAMESPACES:
        raise _limited(path, f"must contain at most {META_MAX_NAMESPACES} namespaces")

    for namespace, value in meta.items():
        namespace_path = f"{path}.{namespace!s}"
        if not isinstance(namespace, str):
            raise _invalid(namespace_path, "namespace names must be strings")
        try:
            namespace.encode("ascii")
        except UnicodeEncodeError as exc:
            raise _invalid(namespace_path, "namespace must be 1–128 ASCII characters") from exc
        if not 1 <= len(namespace) <= 128 or META_NAMESPACE_RE.fullmatch(namespace) is None:
            raise _invalid(
                namespace_path,
                "namespace must match ^[a-z][a-z0-9]*(?:[.-][a-z0-9]+)*$ and be 1–128 ASCII characters",
            )
        if not isinstance(value, dict):
            raise _invalid(namespace_path, "namespace value must be an object and must not be null")
        _validate_descendant(value, namespace_path, depth=1)
        namespace_bytes = _canonical_bytes(value, namespace_path)
        if namespace_bytes > META_MAX_NAMESPACE_BYTES:
            raise _limited(
                namespace_path,
                f"namespace value must be at most {META_MAX_NAMESPACE_BYTES} canonical UTF-8 bytes",
            )

    total_bytes = _canonical_bytes(meta, path)
    if total_bytes > META_MAX_BYTES:
        raise _limited(path, f"meta must be at most {META_MAX_BYTES} canonical UTF-8 bytes")


def validate_timeline_meta_locations(config: Mapping[str, Any], *, path: str = "config") -> None:
    """Validate ``meta`` on a timeline config, its tracks, and its clips.

    This is intentionally an explicit allowlist of authored locations.  It
    does not walk arbitrary extension objects such as ``app`` or ``params``.
    """

    if "meta" in config:
        validate_meta(config["meta"], path=f"{path}.meta")
    for collection in ("tracks", "clips"):
        rows = config.get(collection)
        if not isinstance(rows, list):
            continue
        for index, row in enumerate(rows):
            if isinstance(row, Mapping) and "meta" in row:
                validate_meta(row["meta"], path=f"{path}.{collection}[{index}].meta")


__all__ = [
    "META_MAX_BYTES",
    "META_MAX_CONTAINER_DEPTH",
    "META_MAX_NAMESPACES",
    "META_MAX_NAMESPACE_BYTES",
    "META_NAMESPACE_RE",
    "MetaValidationError",
    "validate_meta",
    "validate_timeline_meta_locations",
]
