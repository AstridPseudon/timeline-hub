"""Transcript adoption through the existing guarded command transaction."""
from __future__ import annotations

import copy
from contextvars import ContextVar

from astrid.sdk.timeline import commands


# The existing recorder receives only the command's before-state. Carry the
# observed helper writes across the synchronous handler/recorder boundary,
# isolated per execution context and consumed once. Never persist this capture.
_continuation_paths = ContextVar("transcript_continuation_paths", default=frozenset())


def dependency(tl, reference):
    from astrid.sdk.timeline.transcripts import TranscriptSourceSelection, verify_snapshot
    selection = TranscriptSourceSelection.from_reference(tl.bundle["project_id"], reference)
    entry = tl.bundle.get("source_mapping", {}).get("pinned_transcripts", {}).get(selection.key)
    if not isinstance(entry, dict) or entry.get("selection") != dict(project_id=selection.project_id, **selection.descriptor()):
        raise commands.CommandError("transcript is outside the verified immutable dependency closure")
    text = entry.get("canonical_record_json")
    if not isinstance(text, str):
        raise commands.CommandError("transcript dependency snapshot is missing")
    record = verify_snapshot(selection, text.encode("utf-8"))
    return selection, record


def _guard(actual, expected):
    if (not isinstance(expected, dict) or expected.get("state") not in {"absent", "present"}
            or set(expected) != ({"state"} if expected["state"] == "absent" else {"state", "value"})):
        raise commands.CommandError("transcript expect requires an explicit absent/present state")
    if not commands._same_value(actual, expected):
        raise commands.SemanticConflict("same-property", "transcript", "binding", expected, actual, None)


def _state(container, key):
    return dict(state="present", value=copy.deepcopy(container[key])) if key in container else dict(state="absent")


def _namespace(container, *, create):
    for key in ("app", "transcript"):
        if key not in container:
            if not create:
                return {}
            container[key] = {}
        container = container[key]
        if not isinstance(container, dict):
            raise commands.CommandError("transcript namespace requires an object")
    if "v" in container and (type(container["v"]) is not int or container["v"] != 1):
        raise commands.CommandError("unsupported transcript namespace version")
    if create:
        container["v"] = 1
    return container


def _target(tl, target):
    if (not isinstance(target, dict) or set(target) != {"clip_id", "occurrence_id"}
            or not isinstance(target["clip_id"], str) or not target["clip_id"]
            or (target["occurrence_id"] is not None and
                (not isinstance(target["occurrence_id"], str) or not target["occurrence_id"]))):
        raise commands.CommandError("transcript.bind requires an exact clip/occurrence target")
    sid = ("parent" if target["occurrence_id"] is None else "occurrence:" + target["occurrence_id"]) + "/clip:" + target["clip_id"]
    if not commands.is_scoped_id(sid):
        raise commands.CommandError("invalid transcript clip target")
    clip = commands.recorded_owner(tl, commands.EditCommand("transcript.bind", sid, {}, resolved=(sid,)), "clip")
    return sid, clip


def validate_correspondence(previous, next_record, correspondence):
    if not isinstance(correspondence, list):
        raise commands.CommandError("transcript correspondence must be an explicit array")
    old_words = {w["id"] for w in previous["words"]} if previous else set()
    new_words = {w["id"] for w in next_record["words"]}
    seen_from, seen_to = set(), set()
    for pair in correspondence:
        if not isinstance(pair, dict) or set(pair) != {"from", "to"}:
            raise commands.CommandError("invalid transcript correspondence")
        for side in ("from", "to"):
            if not isinstance(pair[side], dict) or set(pair[side]) != {"lineage_id", "word_id"}:
                raise commands.CommandError("correspondence requires explicit lineage and opaque word IDs")
        a, b = pair["from"], pair["to"]
        if (previous is None or a["lineage_id"] != previous["source"]["lineage_id"]
                or b["lineage_id"] != next_record["source"]["lineage_id"]
                or a["word_id"] not in old_words or b["word_id"] not in new_words
                or a["word_id"] in seen_from or b["word_id"] in seen_to):
            raise commands.CommandError("transcript correspondence is not an exact one-to-one mapping")
        seen_from.add(a["word_id"])
        seen_to.add(b["word_id"])


def _follow(tl, target, previous, next_binding, correspondence):
    if previous is None:
        return
    from astrid.sdk.timeline.transcripts import install_timing_dependencies
    if not install_timing_dependencies(tl):
        if correspondence:
            raise commands.CommandError("transcript anchor correspondence requires the admitted F timing join")
        return
    from astrid.sdk.timeline.transcript_binding import follow_bound_anchors
    before = {commands.scoped_clip(tl, clip): copy.deepcopy(clip.data) for clip in tl.clips()}
    # The timing hook retains the exact parent (null) or nested occurrence target.
    follow_bound_anchors(tl, clip_id=target["clip_id"], occurrence_id=target["occurrence_id"],
        previous_binding=previous, next_binding=next_binding, correspondence=correspondence)
    after = {commands.scoped_clip(tl, clip): copy.deepcopy(clip.data) for clip in tl.clips()}
    _continuation_paths.set(frozenset(commands.changed_paths(before, after)))


def bind(self, *, target, expect, next, correspondence, source_receipt=None):
    _continuation_paths.set(frozenset())
    sid, clip = _target(self, target)
    if not isinstance(expect, dict) or set(expect) != {"binding"}:
        raise commands.CommandError("transcript.bind expect requires binding")
    ns = _namespace(clip.data, create=False)
    _guard(_state(ns, "binding"), expect["binding"])
    old = ns.get("binding")
    previous = dependency(self, old)[1] if old is not None else None
    if next == {"op": "clear"}:
        if correspondence:
            raise commands.CommandError("clear cannot declare word correspondence")
        _namespace(clip.data, create=False).pop("binding", None)
        _follow(self, target, old, None, correspondence)
        return self
    if not isinstance(next, dict) or set(next) != {
            "schema_version", "document", "snapshot", "subject", "source", "clock", "occurrence_id", "word_ids"}:
        raise commands.CommandError("transcript.bind next requires an exact immutable binding")
    _, record = dependency(self, next)
    if next["occurrence_id"] != target["occurrence_id"]:
        raise commands.CommandError("binding occurrence differs from selected target")
    ids = next["word_ids"]
    ordered = [w["id"] for w in record["words"]]
    if (not isinstance(ids, list) or any(not isinstance(w, str) for w in ids)
            or len(set(ids)) != len(ids) or not ids or [w for w in ordered if w in ids] != ids):
        raise commands.CommandError("binding words must be a nonempty ordered unique snapshot subset")
    from astrid.core.timeline.authoring_bundle import _clip_selected_media
    payload = self.bundle["parent"] if target["occurrence_id"] is None else self.bundle["shots"][clip.shot_id]["internal_timeline"]
    media = _clip_selected_media(clip.data, payload, sid)
    if (media != record["subject"]["media_object_id"] or
            media.removeprefix("sha256:") != record["subject"]["media_sha256"].removeprefix("sha256:")):
        raise commands.CommandError("binding media differs from the target clip's selected immutable object")
    validate_correspondence(previous, record, correspondence)
    _namespace(clip.data, create=True)["binding"] = copy.deepcopy(next)
    from astrid.sdk.timeline.transcripts import install_timing_dependencies
    install_timing_dependencies(self)
    _follow(self, target, old, next, correspondence)
    return self


def reference_key(subject, source_key):
    from astrid.sdk.timeline.commit import _digest
    if (not isinstance(source_key, dict) or set(source_key) != {"producer_id", "source_id"}
            or any(not isinstance(v, str) or not v for v in source_key.values())):
        raise commands.CommandError("source_key requires producer_id/source_id")
    return _digest(dict(subject=subject, source_key=source_key))


def reference(self, *, subject, source_key, expect, next):
    key = reference_key(subject, source_key)
    parent = self.bundle["parent"]
    config = parent.get("config", {})
    ns = _namespace(config, create=False)
    refs = ns.get("references", {})
    if not isinstance(refs, dict):
        raise commands.CommandError("transcript references must be an object")
    _guard(_state(refs, key), expect)
    if next == {"op": "clear"}:
        refs.pop(key, None)
        return self
    if not isinstance(next, dict) or set(next) != {"schema_version", "document", "snapshot", "subject", "source", "clock"}:
        raise commands.CommandError("transcript.reference requires an exact source descriptor")
    _, record = dependency(self, next)
    if record["subject"] != subject or any(record["source"][k] != v for k, v in source_key.items()):
        raise commands.CommandError("reference association differs from source media/key")
    _namespace(parent.setdefault("config", {}), create=True).setdefault("references", {})[key] = copy.deepcopy(next)
    return self


def direct_paths(entry, args, before):
    continuation = _continuation_paths.get()
    _continuation_paths.set(frozenset())
    if entry.op == "transcript.bind":
        target = args["target"]
        sid = ("parent" if target["occurrence_id"] is None else "occurrence:" + target["occurrence_id"]) + "/clip:" + target["clip_id"]
        keys = ["app", "transcript", "binding"]
        node = before[sid]
    else:
        sid, node = "parent", before["parent"]
        keys = ["config", "app", "transcript", "references", reference_key(args["subject"], args["source_key"])]
    path = ""
    for key in keys:
        path = commands._member_path(path, key)
        if key not in node:
            break
        node = node[key]
    # Include namespace version when an existing carrier is enrolled. Missing
    # containers are captured whole, restoring their authored absence on undo.
    paths = {(sid, path)}
    if entry.op == "transcript.bind":
        # Only changes made inside follow_bound_anchors are authored here.
        # The runner captures their exact preconditions from its before-state;
        # later timing/parameter compilation keeps consequence attribution.
        paths.update(continuation)
    prefix = "config.app.transcript" if sid == "parent" and entry.op == "transcript.reference" else "app.transcript"
    namespace = before[sid]
    try:
        for part in prefix.split("."):
            namespace = namespace[part]
        if "v" not in namespace and args["next"] != {"op": "clear"}:
            paths.add((sid, prefix + ".v"))
    except KeyError:
        pass
    return paths


def register():
    for name, handler in (("bind", bind), ("reference", reference)):
        op = "transcript." + name
        commands.REGISTRY[op] = commands.Operation(op, "timeline", name, handler)
