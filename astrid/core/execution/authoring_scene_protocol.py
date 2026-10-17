"""Closed private authoring wire contract. Correlation is never authority."""

from __future__ import annotations

import base64
import hashlib
import json
import math
import re

from .remotion_frame_owner import FrameOwnerError

PROTOCOL = "astrid.authoring-scene/v1"
OPERATION = "evaluate_scene"
PURPOSE = "authoring-preflight"
LIMIT = 1024 * 1024
CONTEXT_FIELDS = (
    "runtime_realm_id",
    "runtime_instance_id",
    "runtime_session_id",
    "executor_id",
    "host_instance_id",
    "source_epoch",
    "provider_id",
    "provider_digest",
    "source_digest",
    "dependency_digest",
    "renderer_closure",
    "owner_generation",
    "capability_digest",
    "executor_source_digest",
    "executor_dependency_digest",
)
INVOCATION_FIELDS = (
    "invocation_id",
    "actor",
    "actor_session",
    "project_id",
    "timeline_id",
    "request_id",
    "request_hash",
    "candidate_digest",
    "fence",
)
REQUEST_FIELDS = {
    "protocol",
    "operation",
    "purpose",
    "context",
    "invocation",
    "scene_digest",
    "scene",
    "dependencies",
    "frames",
}
REPLY_FIELDS = (REQUEST_FIELDS - {"scene", "dependencies"}) | {"dependencies_digest", "evaluation"}


def encoded(value):
    try:
        raw = json.dumps(
            value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False
        ).encode()
    except (ValueError, TypeError, RecursionError, UnicodeError) as exc:
        raise FrameOwnerError("malformed_frame") from exc
    if len(raw) + 1 > LIMIT:
        raise FrameOwnerError("oversized_frame")
    return raw


def digest(value):
    return "sha256:" + hashlib.sha256(encoded(value)).hexdigest()


def sha(value):
    return type(value) is str and re.fullmatch(r"sha256:[0-9a-f]{64}", value) is not None


def closed(value, fields):
    if type(value) is not dict or set(value) != set(fields):
        raise FrameOwnerError("invalid_fields")


def context(value):
    closed(value, CONTEXT_FIELDS)
    for key, item in value.items():
        if key == "owner_generation":
            if type(item) is not int or item < 1:
                raise FrameOwnerError("owner_generation_invalid")
        elif type(item) is not str or not item or len(item) > 512:
            raise FrameOwnerError("context_invalid")
    for key in (
        "provider_digest",
        "source_digest",
        "dependency_digest",
        "renderer_closure",
        "capability_digest",
        "executor_source_digest",
        "executor_dependency_digest",
    ):
        if not sha(value[key]):
            raise FrameOwnerError("context_digest_invalid")
    if value["provider_id"] != "astrid-v1":
        raise FrameOwnerError("provider_mismatch")


def invocation(value):
    closed(value, INVOCATION_FIELDS)
    if any(type(v) is not str or not v or len(v) > 512 for v in value.values()):
        raise FrameOwnerError("invocation_invalid")
    if not all(sha(value[k]) for k in ("actor_session", "request_hash", "candidate_digest")):
        raise FrameOwnerError("invocation_digest_invalid")


def frames(value):
    if (
        type(value) is not list
        or not 0 < len(value) <= 120
        or any(type(v) is not int or not 0 <= v <= 2**53 - 1 for v in value)
        or len(set(value)) != len(value)
    ):
        raise FrameOwnerError("frames_invalid")


def assets(scene):
    """Only immutable CAS media references cross; no caller locations survive."""
    closed(scene, {"timeline", "assets", "fps", "width", "height", "roles"})
    closed(scene["timeline"], {"theme", "clips", "tracks", "theme_overrides"})
    if (
        type(scene["timeline"]["clips"]) is not list
        or type(scene["timeline"]["tracks"]) is not list
        or type(scene["roles"]) is not dict
        or any(
            type(scene[k]) not in (int, float)
            or not math.isfinite(scene[k])
            or not 0 < scene[k] <= (240 if k == "fps" else 16384)
            for k in ("fps", "width", "height")
        )
    ):
        raise FrameOwnerError("scene_invalid")
    registry = scene.get("assets")
    closed(registry, {"assets"})
    if type(registry["assets"]) is not dict:
        raise FrameOwnerError("assets_invalid")
    for entry in registry["assets"].values():
        if type(entry) is not dict or set(entry) - {
            "media_id",
            "object_id",
            "content_sha256",
            "media_type",
            "size",
            "filename",
            "width",
            "height",
            "duration_seconds",
        }:
            raise FrameOwnerError("asset_location_forbidden")
        refs = [entry[k] for k in ("media_id", "object_id", "content_sha256") if k in entry]
        if not refs or not all(sha(v) and v == refs[0] for v in refs):
            raise FrameOwnerError("asset_identity_invalid")

    # Components/params cannot smuggle a path, URL, script or callback either.
    def visit(value, field=None):
        if isinstance(value, dict):
            for key, child in value.items():
                if key.lower() in {
                    "path",
                    "local_path",
                    "src",
                    "url",
                    "href",
                    "executable",
                    "callback",
                    "command",
                    "propspath",
                    "outputdir",
                }:
                    raise FrameOwnerError("scene_location_forbidden")
                visit(child, key)
        elif isinstance(value, list):
            for child in value:
                visit(child)
        elif (
            isinstance(value, str)
            and field not in {"text", "caption", "label", "title", "description"}
            and (
                value.startswith(("/", "./", "../", "~", "\\\\"))
                or re.search(r"(?:https?|file|data|javascript):", value, re.I)
            )
        ):
            raise FrameOwnerError("scene_location_forbidden")

    visit(scene)
    return {
        next(entry[k] for k in ("media_id", "object_id", "content_sha256") if k in entry)
        for entry in registry["assets"].values()
    }


def dependencies(value, expected):
    if type(value) is not dict or set(value) != expected:
        raise FrameOwnerError("dependency_mismatch")
    total = 0
    decoded = {}
    for oid, entry in value.items():
        closed(entry, {"media_type", "bytes"})
        if (
            type(entry["media_type"]) is not str
            or not entry["media_type"].startswith(("image/", "video/", "audio/"))
            or type(entry["bytes"]) is not str
        ):
            raise FrameOwnerError("dependency_invalid")
        try:
            raw = base64.b64decode(entry["bytes"], validate=True)
        except ValueError as exc:
            raise FrameOwnerError("dependency_invalid") from exc
        total += len(raw)
        if total > LIMIT or "sha256:" + hashlib.sha256(raw).hexdigest() != oid:
            raise FrameOwnerError("dependency_digest_invalid")
        decoded[oid] = raw
    return decoded


def validate_request(value, expected_context):
    encoded(value)
    closed(value, REQUEST_FIELDS)
    if (value["protocol"], value["operation"], value["purpose"]) != (PROTOCOL, OPERATION, PURPOSE):
        raise FrameOwnerError("purpose_mismatch")
    context(value["context"])
    if value["context"] != expected_context:
        raise FrameOwnerError("context_mismatch")
    invocation(value["invocation"])
    frames(value["frames"])
    if digest(value["scene"]) != value["scene_digest"]:
        raise FrameOwnerError("scene_digest_mismatch")
    return dependencies(value["dependencies"], assets(value["scene"]))


def validate_evaluation(value, batch):
    """Use renderer answer semantics, with complete scene results required."""
    encoded(value)
    if type(value) is not list or len(value) != len(batch):
        raise FrameOwnerError("evaluation_incomplete")
    for item, frame in zip(value, batch):
        closed(item, {"frame", "layers", "coverage", "content", "findings"})
        if (
            type(item["frame"]) is not int
            or item["frame"] != frame
            or item["coverage"] not in {"COVERED", "DIP", "GAP"}
            or item["content"] not in {"CONTENT", "EMPTY", None}
            or item["findings"] != []
            or type(item["layers"]) is not list
        ):
            raise FrameOwnerError("evaluation_incomplete")
        for layer in item["layers"]:
            closed(
                layer,
                {
                    "clipId",
                    "track",
                    "clipIndex",
                    "z",
                    "drawLocalFrame",
                    "ownFrame",
                    "transitionOpacity",
                    "opacity",
                    "visible",
                    "targetBounds",
                    "bounds",
                    "role",
                    "fullFrame",
                    "coverage",
                    "findings",
                    "dip",
                },
            )
            if (
                type(layer) is not dict
                or type(layer.get("clipId")) is not str
                or type(layer.get("visible")) is not bool
                or layer.get("findings") != []
            ):
                raise FrameOwnerError("evaluation_incomplete")
            if (
                any(type(layer[k]) is not str or not layer[k] for k in ("track", "role"))
                or type(layer["clipIndex"]) is not int
                or layer["clipIndex"] < 0
                or type(layer["z"]) is not int
                or any(
                    type(layer[k]) not in (int, float) or not math.isfinite(layer[k])
                    for k in ("drawLocalFrame", "ownFrame", "transitionOpacity")
                )
                or not 0 <= layer["transitionOpacity"] <= 1
                or any(type(layer[k]) is not bool for k in ("fullFrame", "dip"))
                or layer["coverage"] not in {"covered", "partial"}
            ):
                raise FrameOwnerError("evaluation_invalid")
            bounds = layer.get("bounds")
            if type(bounds) is not dict or bounds.get("status") != "known":
                raise FrameOwnerError("evaluation_incomplete")
            rect = bounds.get("rect")
            closed(rect, {"x", "y", "width", "height"})
            if (
                any(type(v) not in (int, float) or not math.isfinite(v) for v in rect.values())
                or rect["width"] < 0
                or rect["height"] < 0
            ):
                raise FrameOwnerError("evaluation_invalid")
            opacity = layer.get("opacity")
            if opacity is not None and (
                type(opacity) not in (int, float)
                or not math.isfinite(opacity)
                or not 0 <= opacity <= 1
            ):
                raise FrameOwnerError("evaluation_invalid")
    return value


def reply(request, evaluation):
    validate_evaluation(evaluation, request["frames"])
    return {
        **{k: v for k, v in request.items() if k not in {"scene", "dependencies"}},
        "dependencies_digest": digest(request["dependencies"]),
        "evaluation": evaluation,
    }


def validate_reply(value, request):
    encoded(value)
    closed(value, REPLY_FIELDS)
    expected = reply(request, value["evaluation"])
    if value != expected:
        raise FrameOwnerError("reply_binding_mismatch")
    return value["evaluation"]
