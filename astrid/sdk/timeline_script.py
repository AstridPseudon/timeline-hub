"""A composition-scoped reader over the existing pinned text authority."""
from __future__ import annotations

from fractions import Fraction
from typing import Mapping

from astrid.sdk.contracts import DomainResult, ErrorObject


def _projected_narration(state, payload, placed, timeline, revision):
    """Consume Runtime's verified origin receipt, never a mutable text binding.

    Runtime verifies the original parent receipt against its immutable closure.
    Its parent ID is not the child ID or necessarily the inspected parent ID.
    Here we verify the wire projection and its exact selected child rows.
    """
    import re

    from astrid.sdk.timeline.narration import digest, take_key

    if (not isinstance(state, Mapping) or set(state) != {"projection", "digest", "parent_revision_id"}
            or not isinstance(state["parent_revision_id"], str) or not state["parent_revision_id"]):
        raise ValueError("invalid pinned narration state/parent")
    projection = state["projection"]
    if (not isinstance(projection, Mapping) or set(projection) != {"version", "lines"}
            or type(projection["version"]) is not int or projection["version"] != 1
            or not isinstance(projection["lines"], list)
            or state["digest"] != "sha256:" + digest(projection)):
        raise ValueError("invalid pinned narration projection/digest")
    selectors = ("occurrence_id", "shot_id", "shot_revision_id", "internal_timeline_id", "internal_revision_id")
    expected = (placed.get("occurrence_id"), placed.get("shot_id"), placed.get("shot_revision_id"), timeline, revision)
    if any(not isinstance(value, str) or not value for value in expected):
        raise ValueError("incomplete pinned narration selector")
    clips = payload.get("clips", [])
    if not isinstance(clips, list) or any(not isinstance(clip, Mapping) for clip in clips):
        raise ValueError("invalid pinned narration clips")
    selected, seen, previous = [], set(), None
    for line in projection["lines"]:
        if (not isinstance(line, Mapping)
                or set(line) != {*selectors, "clip_id", "segment", "take", "line_digest"}
                or any(not isinstance(line[key], str) or not line[key] for key in ("clip_id", "segment"))
                or not isinstance(line["line_digest"], str)
                or not re.fullmatch(r"sha256:[0-9a-f]{64}", line["line_digest"])):
            raise ValueError("invalid pinned narration line")
        pins = tuple(line[key] for key in selectors)
        if not (all(value is None for value in pins) or all(isinstance(value, str) and value for value in pins)):
            raise ValueError("invalid pinned narration child tuple")
        take_key(line["take"])
        key = (line["occurrence_id"] is not None, line["occurrence_id"] or "", line["clip_id"])
        if key in seen or (previous is not None and key < previous):
            raise ValueError("duplicate or unordered pinned narration line")
        seen.add(key)
        previous = key
        if line["occurrence_id"] != expected[0]:
            continue
        if pins != expected:
            raise ValueError("pinned narration child tuple mismatch")
        matches = [clip for clip in clips if clip.get("id") == line["clip_id"]]
        if len(matches) != 1 or line["line_digest"] != "sha256:" + digest(matches[0]):
            raise ValueError("pinned narration clip digest mismatch")
        app = matches[0].get("app")
        namespace = app.get("astrid") if isinstance(app, Mapping) else None
        if (not isinstance(namespace, Mapping) or not isinstance(namespace.get("text"), str) or not namespace["text"]
                or namespace.get("segment") != line["segment"] or namespace.get("take") != line["take"]):
            raise ValueError("pinned narration line differs from exact payload")
        selected.append(dict(clip_id=line["clip_id"], **namespace))
    return dict(text=" ".join(line["text"] for line in selected) + ("\n" if selected else ""), lines=selected)


def _pinned_narration(transport, project, timeline, placed):
    """Read only the exact internal pin advertised by this inspection page."""
    import hashlib
    import json
    revision = placed.get("internal_timeline_revision_id")
    read = getattr(transport, "get_project_timeline_revision", None)
    if not revision or not callable(read):
        return None  # legacy read-only transports do not supply internal data
    record = read(project, timeline, revision)
    if (not isinstance(record, Mapping) or record.get("revision_id") != revision
            or record.get("project_id") != project or record.get("timeline_id") != timeline
            or not isinstance(record.get("payload"), Mapping)):
        raise ValueError("script internal revision pin mismatch")
    payload = record["payload"]
    digest = "sha256:" + hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":"),
                                                ensure_ascii=False, allow_nan=False).encode()).hexdigest()
    if record.get("content_digest") != digest or placed.get("internal_timeline_digest", digest) != digest:
        raise ValueError("script internal revision digest mismatch")
    if "narration_state" in record:
        return _projected_narration(record["narration_state"], payload, placed, timeline, revision)
    clips = [c for c in payload.get("clips", []) if "take" in c.get("app", {}).get("astrid", {})]
    if not clips:
        return None
    clips.sort(key=lambda c: (c.get("at", 0), c["id"]))
    texts = []
    for clip in clips:
        namespace = clip["app"]["astrid"]
        if not isinstance(namespace.get("text"), str):
            raise ValueError("pinned narration is missing exact authored text")
        texts.append(namespace["text"])
    return dict(text=" ".join(texts) + "\n", lines=[dict(clip_id=c["id"], **c["app"]["astrid"]) for c in clips])


def read_composition_script(timelines, transport, project, ref, *, revision_id=None,
                            occurrence=None, kind="voiceover_script"):
    from astrid.sdk.remote import RemoteShots
    from astrid.sdk.workspace_client import WorkspaceClientError

    if not isinstance(kind, str) or not kind:
        return DomainResult.failure(ErrorObject("validation_error", "Script kind must be a nonempty string", {}))
    rows, cursor, pinned, snapshot = [], None, revision_id, None
    seen_cursors = set()
    reader = RemoteShots(transport)
    while True:
        inspected = timelines.inspect(project, ref, revision_id=pinned, occurrence=occurrence,
                                      limit=100, detail=True, cursor=cursor)
        if not inspected.ok:
            return inspected
        page = inspected.data
        if (not isinstance(page, Mapping) or not isinstance(page.get("revision_id"), str)
                or not page["revision_id"] or not isinstance(page.get("snapshot_digest"), str)
                or not page["snapshot_digest"]):
            return DomainResult.failure(ErrorObject("protocol_error", "Script requires a pinned composition", {}))
        if pinned is None:
            pinned, snapshot = page["revision_id"], page.get("snapshot_digest")
        elif page["revision_id"] != pinned:
            return DomainResult.failure(ErrorObject("integrity_error", "Script pagination changed revision", {}))
        if snapshot is None:
            snapshot = page.get("snapshot_digest")
        elif snapshot != page.get("snapshot_digest"):
            return DomainResult.failure(ErrorObject("integrity_error", "Script pagination changed snapshot", {}))
        selected_rows = page.get("selected", [])
        if not isinstance(selected_rows, list) or any(not isinstance(row, Mapping) for row in selected_rows):
            return DomainResult.failure(ErrorObject("protocol_error", "Invalid script occurrence rows", {}))
        for selected in selected_rows:
            if selected.get("role") != "target":
                continue
            placed = selected.get("occurrence", {})
            if not isinstance(placed, Mapping):
                return DomainResult.failure(ErrorObject("protocol_error", "Invalid script occurrence", {}))
            if not placed.get("occurrence_id"):
                continue  # Parent layers have no shot narration.
            descriptors = placed.get("text_bindings", [])
            if (not isinstance(descriptors, list)
                    or any(not isinstance(b, Mapping) or not isinstance(b.get("kind"), str) or not b["kind"]
                           for b in descriptors)):
                return DomainResult.failure(ErrorObject("protocol_error", "Invalid pinned text bindings", {}))
            bindings = [b for b in descriptors if b.get("kind") == kind]
            result = {
                key: placed.get(key) for key in (
                    "ordinal", "occurrence_id", "shot_id", "shot_revision_id", "name",
                    "start", "duration", "track_id", "internal_timeline_revision_id",
                )
            }
            result.update({"status": "missing" if not bindings else "present", "text": None, "bindings": []})
            if kind == "voiceover_script":
                try:
                    narration = _pinned_narration(transport, page.get("project_id", project),
                                                 page.get("timeline_id", ref), placed)
                except WorkspaceClientError as exc:
                    return DomainResult.failure(ErrorObject(exc.code, exc.message, exc.details))
                except (ValueError, TypeError, KeyError) as exc:
                    return DomainResult.failure(ErrorObject("integrity_error", str(exc), {}))
                if narration is not None:
                    result.update(status="empty" if narration["text"] == "" else "present",
                                  text=narration["text"], lines=narration["lines"],
                                  provenance="pinned_internal_timeline")
                    rows.append(result)
                    continue
            for binding in bindings:
                if (any(not isinstance(binding.get(key), str) or not binding[key]
                        for key in ("binding_id", "media_id", "content_hash"))
                        or binding["media_id"] != binding["content_hash"]
                        or type(binding.get("byte_size")) is not int or binding["byte_size"] < 0):
                    return DomainResult.failure(ErrorObject("protocol_error", "Incomplete pinned text descriptor", {}))
                verified = reader._text_binding_content(binding)
                if not verified.ok:
                    return verified
                pin = {key: value for key, value in verified.data.items() if key != "text"}
                pin["provenance"] = "registered_pin" if binding.get("event_stream_id") else "legacy_unregistered_pin"
                result["bindings"].append({**pin, "text": verified.data["text"]})
            if len(bindings) == 1:
                result["text"] = result["bindings"][0]["text"]
                result["status"] = "empty" if result["text"] == "" else "present"
            elif len(bindings) > 1:
                result["status"] = "multiple"
            rows.append(result)
        cursor = page.get("next_cursor")
        if not cursor:
            break
        if not isinstance(cursor, str):
            return DomainResult.failure(ErrorObject("protocol_error", "Invalid script cursor", {}))
        if cursor in seen_cursors:
            return DomainResult.failure(ErrorObject("protocol_error", "Repeated script cursor", {}))
        seen_cursors.add(cursor)
    rows.sort(key=lambda row: (Fraction(*row["start"]) if isinstance(row.get("start"), list) else Fraction(0), row.get("ordinal", 0)))
    return DomainResult.success({"revision_id": pinned, "snapshot_digest": snapshot,
                                 "kind": kind, "occurrences": rows})



def read_detached_copy_source(bundle):
    """Read the script pins and word producers of one supplied detached document.

    Unlike read_composition_script, this performs no remote reads. Its digest is
    explicitly labelled detached-document-sha256. Independent remote script and
    word reads are never asserted to share a snapshot.
    """
    from astrid.sdk.timeline.copy_sync import source_context
    return source_context(bundle)
