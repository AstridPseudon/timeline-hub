"""Bounded, source-only association of a project transcript with parent media."""
from __future__ import annotations

import copy
import json
import math
import re
from collections.abc import Mapping
from urllib.parse import quote

from astrid.core.timeline.authoring_bundle import _digest
from astrid.sdk.media_transcript import SCHEMA as TRANSCRIPT_SCHEMA
from astrid.sdk.media_transcript import transcript_document_id

from ._command_state import CommandError, equal

OP = "transcript.associate"
TRANSCRIPT_SCHEMA_REF = "astrid.transcript_segment/v1"
REFERENCES_SCHEMA = "media.transcript.references/v1"
_MEDIA_ID = re.compile(r"^sha256:[0-9a-f]{64}$")

_EXTENSION_ID = "haus.astrid.transcript-lane"
_CONTRIBUTION_ID = "transcript-caption-foundry"
_REVIEW_PREFIX = "transcript-source-review:"
_CAPTION_TRACK_ID = "transcript-caption-foundry-track"
_HOST_PROVENANCE_VERSION = 1


_CARRIER_PREFIX = ("config", "bundle")
_LEGACY_FIELDS = ("transcriptReferences", "sourceItemsBySchemaRef")


def _source_paths(state):
    """Return the one persisted App bundle path for the two source planes.

    The parent-level spellings were only used by the rejected source prototype.
    They are refused here rather than treated as a migration source or a second
    authority alongside the normal ``config.bundle`` carrier.
    """
    parent = state.bundle["parent"]
    for prefix in ((), ("config",), ("bundle",)):
        node = parent
        for token in prefix:
            node = node.get(token) if isinstance(node, Mapping) else None
        if isinstance(node, Mapping) and any(key in node for key in _LEGACY_FIELDS):
            raise CommandError("transcript source planes must use parent.config.bundle",
                               kind="unsupported_shape")
    config = parent.get("config")
    if not isinstance(config, Mapping):
        raise CommandError("parent config must be an object", kind="unsupported_shape")
    carrier = config.get("bundle")
    if carrier is not None and not isinstance(carrier, Mapping):
        raise CommandError("parent.config.bundle must be an object", kind="unsupported_shape")
    if isinstance(carrier, Mapping) and "sourceItemsBySchemaRef" in carrier:
        raise CommandError("transcript source items must use persisted itemsBySchemaRef",
                           kind="unsupported_shape")
    return _CARRIER_PREFIX


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
    value = state.get("parent", _path(prefix, "itemsBySchemaRef"))
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


def _encode_component(value):
    return quote(value, safe="-_.!~*'()")


def _transcript_prefixes(asset_id, source_id):
    source = _encode_component(source_id)
    return {
        "legacy": "transcript-source:" + source + ":segment:",
        "canonical": ("transcript-source:" + _encode_component(asset_id)
                      + ":source:" + source + ":segment:"),
    }


def _host_fingerprint(value):
    """Match App's host-owned FNV-1a fingerprint for JSON string values."""
    encoded = json.dumps(value, ensure_ascii=False, separators=(",", ":"),
                         allow_nan=False).encode("utf-8")
    hash_value = 0xCBF29CE484222325
    for byte in encoded:
        hash_value ^= byte
        hash_value = (hash_value * 0x100000001B3) & 0xFFFFFFFFFFFFFFFF
    return "astrid-fnv1a64-v1:" + format(hash_value, "016x")


def _caption_id(occurrence_id):
    return "transcript-caption-" + _host_fingerprint(occurrence_id).split(":", 1)[1]


def _identity_mapping(previous, incoming, asset_id, source_id):
    """Map only the App legacy ID spelling to its exact canonical replacement."""
    scope = _transcript_prefixes(asset_id, source_id)

    def belongs(item):
        return (isinstance(item, Mapping) and item.get("schemaRef") == TRANSCRIPT_SCHEMA_REF
                and isinstance(item.get("sourceArtifactRef"), Mapping)
                and item["sourceArtifactRef"].get("assetId") == asset_id
                and isinstance(item.get("payload"), Mapping)
                and item["payload"].get("sourceId") == source_id)

    previous_by_id = {}
    for item in previous:
        if not belongs(item):
            continue
        item_id = item.get("id")
        if item_id in previous_by_id:
            raise CommandError("ambiguous prior transcript identity", kind="identity_conflict")
        previous_by_id[item_id] = item

    segments = {}
    incoming_ids = set()
    for item in incoming:
        if not belongs(item):
            continue
        item_id = item.get("id")
        if item_id in incoming_ids:
            raise CommandError("ambiguous incoming transcript identity", kind="identity_conflict")
        incoming_ids.add(item_id)
        if not isinstance(item_id, str) or not item_id.startswith(scope["canonical"]):
            continue
        legacy_id = scope["legacy"] + item_id[len(scope["canonical"]):]
        old = previous_by_id.get(legacy_id)
        if old is None:
            continue
        if legacy_id in segments and segments[legacy_id] != item_id:
            raise CommandError("ambiguous transcript identity mapping", kind="identity_conflict")
        if item_id in segments.values() and segments.get(legacy_id) != item_id:
            raise CommandError("ambiguous transcript identity mapping", kind="identity_conflict")
        segments[legacy_id] = item_id
    return segments


def reconcile_transcript_references(config, all_previous, incoming, asset_id, source_id):
    """Purely reconcile the App's known generated caption/review references.

    Only the exact legacy-to-canonical source IDs produced by the transcript
    adapter are considered.  The returned config is a deep copy only when a
    proven reference changes; every other field retains its value and order.
    """
    segments = _identity_mapping(all_previous, incoming, asset_id, source_id)
    if not segments:
        return config
    if not isinstance(config, Mapping):
        raise CommandError("transcript reconciliation config is unsupported", kind="unsupported_shape")
    clips = config.get("clips", [])
    if not isinstance(clips, list):
        raise CommandError("transcript reconciliation clips are unsupported", kind="unsupported_shape")

    owners = {}
    for item in all_previous:
        if (not isinstance(item, Mapping) or item.get("schemaRef") != TRANSCRIPT_SCHEMA_REF
                or not isinstance(item.get("payload"), Mapping)
                or not isinstance(item["payload"].get("sourceId"), str)
                or not isinstance(item.get("sourceArtifactRef"), Mapping)):
            continue
        owner = (item["sourceArtifactRef"].get("assetId"), item["payload"]["sourceId"])
        item_id = item.get("id")
        aliases = [item_id]
        scope = _transcript_prefixes(*owner)
        if isinstance(item_id, str) and item_id.startswith(scope["canonical"]):
            aliases.append(scope["legacy"] + item_id[len(scope["canonical"]):])
        for alias in aliases:
            owners.setdefault(alias, set()).add(owner)

    media_suffixes = []
    for media in clips:
        if not isinstance(media, Mapping) or media.get("asset") != asset_id:
            continue
        media_id = media.get("id")
        if not isinstance(media_id, str):
            continue
        media_suffixes.extend(("@" + media_id, "@" + _encode_component(media_id)))

    occupied = {clip.get("id") for clip in clips if isinstance(clip, Mapping)}
    next_clips = copy.deepcopy(clips)
    clips_changed = False
    for index, clip in enumerate(clips):
        if not isinstance(clip, Mapping):
            continue
        app = clip.get("app")
        generated = app.get("__generated__") if isinstance(app, Mapping) else None
        provenance = generated.get("provenance") if isinstance(generated, Mapping) else None
        if (clip.get("track") != _CAPTION_TRACK_ID or not isinstance(generated, Mapping)
                or generated.get("extensionId") != _EXTENSION_ID
                or generated.get("contributionId") != _CONTRIBUTION_ID
                or not isinstance(provenance, Mapping)
                or provenance.get("sourceSchemaRef") != TRANSCRIPT_SCHEMA_REF
                or provenance.get("contractVersion") != _HOST_PROVENANCE_VERSION
                or not isinstance(provenance.get("sourceItemId"), str)):
            continue
        old_id = provenance["sourceItemId"]
        new_id = segments.get(old_id)
        if new_id is None:
            continue
        suffixes = list(dict.fromkeys(media_suffixes))
        if len(owners.get(old_id, set())) == 1:
            suffixes.extend(("", "@source", "@timeline"))
        matches = [suffix for suffix in suffixes if _caption_id(old_id + suffix) == clip.get("id")]
        if len(matches) > 1:
            raise CommandError("ambiguous transcript caption ownership", kind="identity_conflict")
        if not matches:
            # An exact generic caption with shared ownership cannot be safely
            # assigned to this asset; preserve the draft only by refusing it.
            if len(owners.get(old_id, set())) > 1 and _caption_id(old_id) == clip.get("id"):
                raise CommandError("ambiguous transcript caption ownership", kind="identity_conflict")
            continue
        new_clip_id = _caption_id(new_id + matches[0])
        if new_clip_id in occupied:
            raise CommandError("transcript caption destination is occupied", kind="identity_conflict")
        occupied.add(new_clip_id)
        next_clip = copy.deepcopy(clip)
        next_clip["id"] = new_clip_id
        next_clip["app"]["__generated__"]["provenance"]["sourceItemId"] = new_id
        next_clips[index] = next_clip
        clips_changed = True

    app = config.get("app")
    extension = app.get(_EXTENSION_ID) if isinstance(app, Mapping) else None
    next_extension = copy.deepcopy(extension) if isinstance(extension, Mapping) else None
    reviews_changed = False
    if isinstance(extension, Mapping):
        for old_id, new_id in segments.items():
            owners_for_id = owners.get(old_id, set())
            old_key = _REVIEW_PREFIX + _encode_component(old_id)
            new_key = _REVIEW_PREFIX + _encode_component(new_id)
            value = extension.get(old_key)
            if len(owners_for_id) > 1 and isinstance(value, Mapping):
                if (value.get("schemaVersion") == 1
                        and value.get("sourceSchemaRef") == TRANSCRIPT_SCHEMA_REF
                        and value.get("sourceItemId") == old_id):
                    raise CommandError("ambiguous transcript review ownership", kind="identity_conflict")
            if (len(owners_for_id) != 1 or not isinstance(value, Mapping)
                    or value.get("schemaVersion") != 1
                    or value.get("sourceSchemaRef") != TRANSCRIPT_SCHEMA_REF
                    or value.get("sourceItemId") != old_id):
                continue
            if new_key in next_extension:
                raise CommandError("transcript review destination is occupied", kind="identity_conflict")
            del next_extension[old_key]
            next_extension[new_key] = {**value, "sourceItemId": new_id}
            reviews_changed = True

    if not clips_changed and not reviews_changed:
        return config
    result = copy.deepcopy(config)
    if clips_changed:
        result["clips"] = next_clips
    if reviews_changed:
        result.setdefault("app", {})[_EXTENSION_ID] = next_extension
    return result


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
    refs_path, items_path = _path(prefix, "transcriptReferences"), _path(prefix, "itemsBySchemaRef")
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
    config = ctx.read("parent", ["config"])
    reconciled_config = reconcile_transcript_references(
        config, old_items, projected, asset_id, args["source_id"]
    )
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
    ctx.object("parent", list(prefix))
    ctx.write("parent", refs_path, next_refs)
    ctx.write("parent", items_path, next_map)
    if not equal(config.get("clips", []), reconciled_config.get("clips", [])):
        clip_path = (list(ctx.state.parent_clip_path)
                     if ctx.state.parent_clip_path == ("clips",)
                     else ["config", "clips"])
        ctx.write("parent", clip_path, reconciled_config["clips"])
    old_app = config.get("app") if isinstance(config, Mapping) else None
    new_app = reconciled_config.get("app") if isinstance(reconciled_config, Mapping) else None
    old_extension = old_app.get(_EXTENSION_ID) if isinstance(old_app, Mapping) else None
    new_extension = new_app.get(_EXTENSION_ID) if isinstance(new_app, Mapping) else None
    if not equal(old_extension, new_extension):
        ctx.write("parent", ["config", "app", _EXTENSION_ID], new_extension)


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
