"""Bounded, source-only association of a project transcript with parent media.

The source planes are authored parent payload fields.  This operation deliberately
does not own project-document CRUD or caption/review reconciliation; either of
those changes is refused before the first write until its native carrier exists.
"""
from __future__ import annotations

import copy
import json
import math
import re
from collections.abc import Mapping

from astrid.core.timeline.authoring_bundle import _digest
from astrid.sdk.media_transcript import SCHEMA as TRANSCRIPT_SCHEMA
from astrid.sdk.media_transcript import transcript_document_id

from ._command_state import CommandError

OP = "transcript.associate"
TRANSCRIPT_SCHEMA_REF = "astrid.transcript_segment/v1"
REFERENCES_SCHEMA = "media.transcript.references/v1"
_MEDIA_ID = re.compile(r"^sha256:[0-9a-f]{64}$")


def _source_paths(state):
    """Return the canonical parent-payload paths for the two source planes."""
    parent = state.bundle["parent"]
    locations = []
    for prefix in ((), ("config",), ("bundle",)):
        node = parent
        for token in prefix:
            node = node.get(token) if isinstance(node, Mapping) else None
        if not isinstance(node, Mapping):
            continue
        if any(key in node for key in ("transcriptReferences", "sourceItemsBySchemaRef")):
            locations.append(prefix)
    if len(locations) > 1:
        raise CommandError("transcript source planes have ambiguous parent ownership",
                           kind="unsupported_shape")
    return locations[0] if locations else ()


def _path(prefix, field):
    return [*prefix, field]


def _source_item_key(row):
    owner = row["sourceArtifactRef"]["assetId"]
    source = row["payload"]["sourceId"]
    return json.dumps([owner, source, row["id"]], ensure_ascii=False, separators=(",", ":"))


def source_item_selection(state, owner, members=()):
    if owner != "parent":
        raise CommandError("transcript source selection requires parent ownership")
    prefix = _source_paths(state)
    value = state.get("parent", _path(prefix, "sourceItemsBySchemaRef"))
    if value["state"] == "absent":
        rows = []
    elif value["state"] == "present" and isinstance(value["value"], dict):
        rows = value["value"].get(TRANSCRIPT_SCHEMA_REF, [])
        if rows is None:
            rows = []
    else:
        raise CommandError("transcript source item plane must be an object", kind="unsupported_shape")
    if not isinstance(rows, list):
        raise CommandError("transcript source item collection must be an array", kind="unsupported_shape")
    keys = []
    for row in rows:
        _validate_source_item(row)
        key = _source_item_key(row)
        if key in keys:
            raise CommandError("ambiguous existing transcript source-item identity",
                               kind="identity_conflict")
        keys.append(key)
    return {"key": "transcript.source-items", "query_version": 1, "owner": owner,
            "members": list(keys), "order": list(keys), "boundaries": list(keys),
            "policy": "guard-membership"}


def _validate_source_item(row):
    if not isinstance(row, Mapping):
        raise CommandError("transcript source item must be an object", kind="unsupported_shape")
    if (row.get("schemaRef") != TRANSCRIPT_SCHEMA_REF or not isinstance(row.get("id"), str)
            or not row["id"]):
        raise CommandError("unsupported transcript source-item envelope", kind="unsupported_shape")
    owner = row.get("sourceArtifactRef")
    payload = row.get("payload")
    provenance = row.get("provenance")
    if (not isinstance(owner, Mapping) or not isinstance(owner.get("assetId"), str)
            or not isinstance(payload, Mapping) or not isinstance(payload.get("sourceId"), str)
            or payload.get("segmentId") != row["id"]
            or not isinstance(provenance, Mapping)
            or not isinstance(provenance.get("adapterId"), str)
            or not isinstance(provenance.get("adapterVersion"), str)):
        raise CommandError("transcript source item lacks its raw owner or stable identity",
                           kind="unsupported_shape")


def _pin(args, key):
    pin = args.get(key)
    if pin is None:
        return None
    if (not isinstance(pin, Mapping) or set(pin) != {"document_id", "version", "content_digest"}
            or not isinstance(pin["document_id"], str) or not pin["document_id"].startswith("transcript:")
            or type(pin["version"]) is not int or pin["version"] < 1
            or not isinstance(pin["content_digest"], str)
            or not _MEDIA_ID.fullmatch(pin["content_digest"])):
        raise CommandError("exact transcript DocumentPin is required", kind="invalid_source")
    return dict(pin)


def _verified(pin, bundle):
    captures = [row for row in bundle.get("source_mapping", {}).get("pinned_documents", [])
                if isinstance(row, Mapping) and row.get("pin") == pin]
    if len(captures) != 1:
        raise CommandError("exact transcript source is missing or revoked; hydrate transcript_source(DocumentPin)",
                           kind="history_unavailable")
    source = captures[0].get("document")
    if (not isinstance(source, Mapping) or source.get("kind") != "media.transcript"
            or source.get("document_id") != pin["document_id"]
            or source.get("project_id") != bundle.get("project_id")
            or source.get("version") != pin["version"]
            or _digest(source.get("content")) != pin["content_digest"]):
        raise CommandError("transcript source does not match its exact DocumentPin",
                           kind="invalid_source")
    content = source.get("content")
    if (not isinstance(content, Mapping) or content.get("schema") != TRANSCRIPT_SCHEMA
            or not isinstance(content.get("media_id"), str) or not _MEDIA_ID.fullmatch(content["media_id"])
            or not isinstance(content.get("source_id"), str) or not content["source_id"]
            or pin["document_id"] != transcript_document_id(
                bundle["project_id"], content["media_id"], content["source_id"])):
        raise CommandError("transcript source identity is not canonical", kind="invalid_source")
    segments = content.get("segments")
    if not isinstance(segments, list) or not segments:
        raise CommandError("transcript source requires ordered segments", kind="invalid_source")
    segment_ids, word_ids = set(), set()
    for segment in segments:
        if not isinstance(segment, Mapping) or not isinstance(segment.get("id"), str) or not segment["id"]:
            raise CommandError("transcript segment identity is unsupported", kind="invalid_source")
        if segment["id"] in segment_ids:
            raise CommandError("ambiguous transcript segment identity", kind="identity_conflict")
        segment_ids.add(segment["id"])
        if not isinstance(segment.get("text"), str):
            raise CommandError("transcript segment text is unsupported", kind="invalid_source")
        start, end = segment.get("start"), segment.get("end")
        if (isinstance(start, bool) or isinstance(end, bool) or not isinstance(start, (int, float))
                or not isinstance(end, (int, float)) or not math.isfinite(start) or not math.isfinite(end)
                or start < 0 or end < start):
            raise CommandError("transcript segment timing is unsupported", kind="invalid_source")
        words = segment.get("words", [])
        if not isinstance(words, list):
            raise CommandError("transcript words must be an array", kind="invalid_source")
        for word in words:
            if (not isinstance(word, Mapping) or not isinstance(word.get("id"), str) or not word["id"]):
                raise CommandError("transcript word identity is unsupported", kind="invalid_source")
            if word["id"] in word_ids:
                raise CommandError("ambiguous transcript word identity", kind="identity_conflict")
            word_ids.add(word["id"])
            ws, we = word.get("start"), word.get("end")
            if (isinstance(ws, bool) or isinstance(we, bool) or not isinstance(ws, (int, float))
                    or not isinstance(we, (int, float)) or not math.isfinite(ws) or not math.isfinite(we)
                    or ws < start or we < ws or we > end):
                raise CommandError("transcript word is outside its segment", kind="invalid_source")
    return copy.deepcopy(source), copy.deepcopy(content)


def _project_items(source, content, asset_id):
    """Convert the already-verified canonical document to source envelopes."""
    return [{
        "id": segment["id"], "shape": "interval", "domain": "source_seconds",
        "extent": {"start": segment["start"], "end": segment["end"]},
        "schemaRef": TRANSCRIPT_SCHEMA_REF,
        "sourceArtifactRef": {"assetId": asset_id},
        "provenance": {"adapterId": "astrid.projectTranscript", "adapterVersion": "1"},
        "payload": {
            "sourceId": content["source_id"], "segmentId": segment["id"],
            "text": segment["text"],
            **({"speaker": segment["speaker"]} if "speaker" in segment else {}),
            **({"words": copy.deepcopy(segment["words"])} if "words" in segment else {}),
            "documentId": source["document_id"], "documentVersion": source["version"],
        },
    } for segment in content["segments"]]


def _reconciliation_needed(config, asset_id, old_ids, new_ids):
    """Detect changes that belong to the not-yet-carried caption/review reconciler."""
    if not isinstance(config, Mapping):
        return False
    clips = config.get("clips", [])
    if isinstance(clips, list):
        for clip in clips:
            if not isinstance(clip, Mapping) or clip.get("asset") != asset_id:
                continue
            generated = clip.get("app", {}).get("__generated__") if isinstance(clip.get("app"), Mapping) else None
            provenance = generated.get("provenance") if isinstance(generated, Mapping) else None
            if not isinstance(provenance, Mapping) or provenance.get("sourceSchemaRef") != TRANSCRIPT_SCHEMA_REF:
                continue
            if provenance.get("sourceItemId") not in new_ids:
                return True
    app = config.get("app")
    review = app.get("haus.astrid.transcript-lane") if isinstance(app, Mapping) else None
    if isinstance(review, Mapping):
        for row in review.values():
            if (isinstance(row, Mapping) and row.get("sourceSchemaRef") == TRANSCRIPT_SCHEMA_REF
                    and row.get("sourceItemId") not in new_ids):
                return True
    return False


def associate(ctx, command):
    asset_ref, args = command["select"], command["args"]
    if not isinstance(asset_ref, str) or not re.fullmatch(r"parent/asset:(?!.*::)[^/]+", asset_ref):
        raise CommandError("transcript association requires a parent asset", kind="unsupported_ownership")
    asset_id = asset_ref.removeprefix("parent/asset:")
    if args.get("asset_id") != asset_id:
        raise CommandError("transcript association asset selector differs from its owner",
                           kind="identity_conflict")
    asset = ctx.state.entity(asset_ref, optional=True)
    if not isinstance(asset, Mapping):
        raise CommandError("selected transcript asset is missing", kind="identity_conflict", ref=asset_ref)
    registry_media = asset.get("media_id", asset.get("content_sha256"))
    if registry_media != args["media_id"]:
        raise CommandError("selected asset media identity differs from transcript source", kind="invalid_source")
    new_pin = _pin(args, "document")
    old_pin = _pin(args, "previous_document")
    if new_pin is None:
        raise CommandError("new transcript DocumentPin is required", kind="invalid_source")
    _, content = _verified(new_pin, ctx.state.bundle)
    if content["media_id"] != args["media_id"] or content["source_id"] != args["source_id"]:
        raise CommandError("transcript source owner differs from command", kind="invalid_source")
    prefix = _source_paths(ctx.state)
    refs_path, items_path = _path(prefix, "transcriptReferences"), _path(prefix, "sourceItemsBySchemaRef")
    refs_state, items_state = ctx.state.get("parent", refs_path), ctx.state.get("parent", items_path)
    refs = {"schema": REFERENCES_SCHEMA, "associations": []} if refs_state["state"] == "absent" else refs_state.get("value")
    if refs is None:
        raise CommandError("transcript reference plane cannot be null", kind="unsupported_shape")
    if not isinstance(refs, Mapping) or refs.get("schema") != REFERENCES_SCHEMA or not isinstance(refs.get("associations"), list):
        raise CommandError("transcript reference plane is unsupported", kind="unsupported_shape")
    if refs_state["state"] == "absent":
        refs = {"schema": REFERENCES_SCHEMA, "associations": []}
    associations = copy.deepcopy(refs["associations"])
    owners = [row.get("assetId") for row in associations if isinstance(row, Mapping)]
    if len(owners) != len(associations) or len(owners) != len(set(owners)) or any(not isinstance(row.get("documentId"), str) for row in associations):
        raise CommandError("ambiguous transcript association ownership", kind="identity_conflict")
    previous = next((row for row in associations if row["assetId"] == asset_id), None)
    if (previous is None and old_pin is not None) or (previous is not None and (
            old_pin is None or old_pin["document_id"] != previous["documentId"])):
        raise CommandError("exact prior DocumentPin is required for replacement", kind="history_unavailable")
    if previous is not None:
        _, old_content = _verified(old_pin, ctx.state.bundle)
        if old_content["media_id"] != registry_media:
            raise CommandError("prior transcript source belongs to different media", kind="invalid_source")
    source_map = {} if items_state["state"] == "absent" else items_state.get("value")
    if not isinstance(source_map, dict):
        raise CommandError("transcript source item plane is unsupported", kind="unsupported_shape")
    old_items = source_map.get(TRANSCRIPT_SCHEMA_REF, [])
    if old_items is None and TRANSCRIPT_SCHEMA_REF in source_map:
        raise CommandError("transcript source item collection cannot be null", kind="unsupported_shape")
    if old_items is None:
        old_items = []
    if not isinstance(old_items, list):
        raise CommandError("transcript source item collection must be an array", kind="unsupported_shape")
    keys = []
    for row in old_items:
        _validate_source_item(row)
        key = _source_item_key(row)
        if key in keys:
            raise CommandError("ambiguous existing transcript source-item identity", kind="identity_conflict")
        keys.append(key)
    projected = _project_items({"document_id": new_pin["document_id"], "version": new_pin["version"]}, content, asset_id)
    new_ids = {row["id"] for row in projected}
    old_ids = {row["id"] for row in old_items if row["sourceArtifactRef"]["assetId"] == asset_id}
    config = ctx.read("parent", ["config"])
    if _reconciliation_needed(config, asset_id, old_ids, new_ids):
        raise CommandError("caption/review reconciliation would change unsupported data; follow up with a native reconciliation carrier",
                           kind="unsupported_reconciliation")
    ctx.select("transcript.source-items", "parent")
    ctx.read("parent", refs_path)
    ctx.read("parent", items_path)
    ctx.bind("transcript.owner", asset_ref)
    for row in projected:
        ctx.bind("transcript.segment:" + row["id"], asset_ref)
        for word in row["payload"].get("words", []):
            ctx.bind("transcript.word:" + word["id"], asset_ref)
    ctx.dependency("transcript.document", "transcript", new_pin)
    if old_pin is not None:
        ctx.dependency("transcript.previous", "transcript", old_pin)
    retained = [row for row in old_items if not (
        row["sourceArtifactRef"]["assetId"] == asset_id
        and (row["provenance"].get("adapterId") == "astrid.projectTranscript"
             or row["payload"].get("sourceId") == args["source_id"]))]
    next_refs = copy.deepcopy(refs)
    next_refs["associations"] = [row for row in associations if row["assetId"] != asset_id]
    next_refs["associations"].append({"assetId": asset_id, "documentId": new_pin["document_id"]})
    next_map = copy.deepcopy(source_map)
    next_map[TRANSCRIPT_SCHEMA_REF] = retained + projected
    ctx.write("parent", refs_path, next_refs)
    ctx.write("parent", items_path, next_map)


def capture_transcript_association(bundle, asset_id, *, document, previous_document=None):
    """Capture a source association from exact hydrated transcript pins."""
    from .commands import execute

    command = {"schema_version": 1, "op": OP, "version": "1",
               "select": "parent/asset:" + asset_id,
               "args": {"asset_id": asset_id, "media_id": "", "source_id": "",
                        "document": copy.deepcopy(document),
                        "previous_document": copy.deepcopy(previous_document),
                        "source_schema_ref": TRANSCRIPT_SCHEMA_REF}}
    pin = _pin(command["args"], "document")
    captures = [row for row in bundle.get("source_mapping", {}).get("pinned_documents", [])
                if row.get("pin") == pin]
    if len(captures) != 1:
        raise CommandError("capture requires exact hydrated transcript source")
    _, content = _verified(pin, bundle)
    command["args"]["media_id"], command["args"]["source_id"] = content["media_id"], content["source_id"]
    return execute(bundle, [command]).commands[0]
