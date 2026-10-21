"""Unplaced parent-owned source references backed by verified raw media."""
from __future__ import annotations

import copy
import re

from ._command_state import ABSENT, CommandError, equal
from ._materialization import capture_version

REFERENCE_NAMESPACE = ("config", "app", "astrid", "timeline_references")
_DIGEST = re.compile(r"sha256:[0-9a-f]{64}\Z")


def reference_path(reference_id):
    """Return the canonical authored path for one stable reference identity."""
    return [*REFERENCE_NAMESPACE, reference_id]


def _raw_verified(ctx, pin):
    matches = [row for row in ctx.verified_media if equal(row.get("raw_pin"), pin)]
    if not matches or any(not equal(row, matches[0]) for row in matches):
        raise CommandError(
            "timeline reference requires exact Runtime-verified raw media",
            kind="dependency_unavailable",
        )
    info = matches[0].get("media_info")
    if (not isinstance(info, dict) or info.get("object_id") != pin["media_id"]
            or not isinstance(info.get("media_type"), str) or not info["media_type"]
            or type(info.get("size")) is not int or info["size"] <= 0):
        raise CommandError(
            "timeline reference requires verified raw media metadata",
            kind="dependency_changed",
        )
    return info


def _validate_pin(pin):
    if (not isinstance(pin, dict) or set(pin) != {"media_id", "content_digest"}
            or not _DIGEST.fullmatch(pin.get("media_id", ""))
            or pin.get("content_digest") != pin["media_id"]):
        raise CommandError("timeline reference requires one exact media manifest pin")


def _registry_birth(ctx, reference_id, pin):
    """Reserve the stable identity through the existing parent asset birth."""
    ctx.read("parent/collection:asset")
    ctx.read("parent/asset:" + reference_id)
    if ctx.state.get("parent/asset:" + reference_id, []) != ABSENT:
        raise CommandError(
            "timeline reference identity is already occupied",
            kind="identity_collision",
            ref="parent/asset:" + reference_id,
        )

    parent = ctx.state.bundle["parent"]
    config = ctx.state.config("parent")
    registry_path = ["registry"] if "registry" in parent or "registry" not in config else [
        "config", "registry"]
    ctx.object("parent", registry_path)
    ctx.object("parent", [*registry_path, "assets"])
    # The registry entry intentionally uses the existing media identity shape;
    # raw metadata is a private verification result, never authored authority.
    return ctx.create_asset("parent", reference_id, copy.deepcopy(pin))


def timeline_reference(ctx, command):
    if command.get("select") != "parent":
        raise CommandError("timeline reference requires the parent scope")
    args = command["args"]
    reference_id, role, pin = args["reference_id"], args["role"], args["media"]
    _validate_pin(pin)
    _raw_verified(ctx, pin)

    reference = reference_path(reference_id)
    ctx.read("parent", reference)
    if ctx.state.get("parent", reference) != ABSENT:
        raise CommandError(
            "timeline reference identity is already occupied",
            kind="identity_collision",
            ref="parent",
            path=reference,
        )
    _registry_birth(ctx, reference_id, pin)

    # These containers are the existing namespaced parent carrier. Their
    # creation is recorded so inverse restores absent/null/malformed state
    # without touching unrelated application metadata.
    ctx.object("parent", ["config"])
    ctx.object("parent", ["config", "app"])
    ctx.object("parent", ["config", "app", "astrid"])
    ctx.object("parent", [*REFERENCE_NAMESPACE])
    ctx.write("parent", reference, {
        "version": 1,
        "reference_id": reference_id,
        "role": role,
        "media": copy.deepcopy(pin),
    })
    ctx.dependency("reference.media", "media", pin)
    ctx.bind("reference.owner", "parent")
    ctx.record["command"]["intent"] = {}


def capture_timeline_reference(bundle, reference_id, media, *, verified_media):
    """Capture an unplaced source reference using a verified raw-media read."""
    from .commands import execute

    command = {
        "schema_version": 1,
        "op": "timeline.reference",
        "version": capture_version(bundle, "parent"),
        "select": "parent",
        "args": {
            "reference_id": reference_id,
            "role": "source",
            "media": copy.deepcopy(media),
        },
        "intent": {},
    }
    return execute(bundle, [command], verified_media=verified_media).commands[0]
