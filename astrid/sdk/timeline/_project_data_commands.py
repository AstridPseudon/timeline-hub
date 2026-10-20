"""Bounded replacement/removal of one extension-owned project-data entry."""

from __future__ import annotations

import json
import re

from ._command_state import CommandError

_EXTENSION_ID = re.compile(r"^[a-z][a-z0-9_-]*(?:\.[a-z][a-z0-9_-]*)*$", re.IGNORECASE)
_RESERVED_KEYS = frozenset(("__proto__", "constructor", "prototype"))
_MAX_KEY_BYTES = 256
_MAX_ENTRY_BYTES = 64 * 1024
_MAX_EXTENSION_TOTAL_BYTES = 1 * 1024 * 1024
_MAX_ENTRIES_PER_EXTENSION = 128


def _json_bytes(value):
    try:
        encoded = json.dumps(
            value,
            allow_nan=False,
            ensure_ascii=False,
            separators=(",", ":"),
        ).encode("utf-8")
    except (TypeError, UnicodeError, ValueError) as exc:
        raise CommandError("project-data.write value must be finite JSON") from exc
    return len(encoded)


def _validate_target(target):
    if (
        not isinstance(target, str)
        or len(target) == 0
        or len(target) > 128
        or _EXTENSION_ID.fullmatch(target) is None
    ):
        raise CommandError("project-data.write requires an explicit extension target")


def _validate_key(key):
    if not isinstance(key, str) or not key or key != key.strip():
        raise CommandError("project-data.write requires an already-canonical project-data key")
    if len(key.encode("utf-8")) > _MAX_KEY_BYTES:
        raise CommandError("project-data.write project-data key exceeds 256 UTF-8 bytes")
    if key in _RESERVED_KEYS:
        raise CommandError(f"project-data.write project-data key {key!r} is reserved")


def _validate_limits(ctx, target, key, value):
    existing = ctx.state.get("parent", ["config", "app", target])
    if existing["state"] == "present" and existing["value"] is not None and not isinstance(
        existing["value"], dict
    ):
        # Let ctx.object report the malformed namespace through the same
        # authored-container path used by the other native commands.
        return
    namespace = dict(existing.get("value") or {})
    if _json_bytes(value) > _MAX_ENTRY_BYTES:
        raise CommandError("project-data.write value exceeds the 64 KiB entry limit")
    is_new_key = key not in namespace
    namespace[key] = value
    if is_new_key and len(namespace) > _MAX_ENTRIES_PER_EXTENSION:
        raise CommandError("project-data.write exceeds the 128-entry extension limit")
    total = sum(_json_bytes(entry) for entry in namespace.values())
    if total > _MAX_EXTENSION_TOTAL_BYTES:
        raise CommandError("project-data.write exceeds the 1 MiB extension limit")


def project_data_write(ctx, command):
    """Replace or remove exactly one key in the parent timeline's ``config.app`` map.

    The project catalog is deliberately outside the authoring bundle and is
    not reachable from this command.  Opaque JSON, including object keys that
    are special to JavaScript, remains ordinary authored data in Python's
    object model.
    """
    if command.get("select") != "parent":
        raise CommandError("project-data.write requires the parent timeline scope")
    args = command["args"]
    target, key, mode = args["target"], args["key"], args["mode"]
    _validate_target(target)
    _validate_key(key)
    ref, target_path = "parent", ["config", "app", target]

    if mode == "replace":
        value = args["value"]
        _json_bytes(value)
        _validate_limits(ctx, target, key, value)
        # Containers are part of the authored scope.  Recording them when they
        # are first created lets inverse restore absent/null target containers
        # exactly; existing namespaces are touched only at the requested key.
        ctx.object(ref, ["config"])
        ctx.object(ref, ["config", "app"])
        ctx.object(ref, target_path)
        ctx.write(ref, [*target_path, key], value)
        return

    if mode != "remove":
        raise CommandError('project-data.write only supports mode "replace" or "remove"')

    namespace = ctx.state.get(ref, target_path)
    if namespace["state"] == "absent":
        # Keep a missing target as a guarded no-op.  The project-data
        # container claim permits a disjoint namespace birth to replay.
        ctx.read(ref, target_path)
        return
    if namespace["value"] is not None and not isinstance(namespace["value"], dict):
        raise CommandError("intent container must be object or null", ref=ref, path=target_path)

    # Main treats null/empty namespaces as empty and removes the namespace.
    # A non-empty namespace removes only the declared leaf; clear() records an
    # absent leaf as absent, retaining the same-key guard for a no-op delete.
    app_path = ["config", "app"]
    app = ctx.state.get(ref, app_path)
    app_order = list(app["value"]) if app["state"] == "present" and isinstance(app["value"], dict) else None
    if namespace["value"] is None or not namespace["value"]:
        ctx.clear(ref, target_path, insertion_order=app_order)
    else:
        ctx.clear(ref, [*target_path, key])
        current = ctx.state.get(ref, target_path)
        if current["state"] == "present" and not current["value"]:
            ctx.clear(ref, target_path, insertion_order=app_order)

    app = ctx.state.get(ref, app_path)
    if app["state"] == "present" and isinstance(app["value"], dict) and not app["value"]:
        ctx.clear(ref, app_path)


PROJECT_DATA_INTENT = {}
