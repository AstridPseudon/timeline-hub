"""Exact speech boundaries and prepared, scoped SCRIPT-REFLOW intents.

Speech is prepared outside the authored transaction. Runtime resolves the three
managed references again on its request-bound port; no path or client is a take.
"""
from __future__ import annotations

import copy
import difflib
import hashlib
import json
import math
import re
from collections.abc import Mapping

from astrid.sdk import timeline_intent as intent
from astrid.sdk.timeline._common import TimelineEditError

PORTS = frozenset(("speech", "speech_words", "speech_manifest"))
DEFAULT_SETTINGS = dict(provider="edge-tts", voice="en-US-ChristopherNeural",
                        rate="+0%", volume="+0%", pitch="+0Hz")


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"),
                                    ensure_ascii=False, allow_nan=False).encode()).hexdigest()


def take_key(refs):
    if not isinstance(refs, dict) or set(refs) != PORTS:
        raise TimelineEditError("a take requires exactly speech, speech_words and speech_manifest")
    for ref in refs.values():
        if (not isinstance(ref, dict) or set(ref) != {"association_id", "object_id"}
                or not isinstance(ref["association_id"], str) or not ref["association_id"]
                or not isinstance(ref["object_id"], str)
                or not re.fullmatch(r"sha256:[0-9a-f]{64}", ref["object_id"])):
            raise TimelineEditError("invalid managed take reference")
    return digest(refs)


def validate_speech_boundary(text, rows):
    """Unicode whitespace separates exact tokens; nothing else is normalized.

    Each artifact row must contain precisely one token. Case, punctuation,
    numbers, Unicode code points and order compare exactly. This conservative
    metadata check makes no assertion about acoustic correctness.
    """
    if not isinstance(text, str) or not text.split() or not isinstance(rows, list) or not rows:
        raise TimelineEditError("speech needs exact nonempty text and complete word rows")
    tokens = []
    for row in rows:
        word = row.get("word") if isinstance(row, Mapping) else row[2] if isinstance(row, list) and len(row) in (3, 4) else None
        if not isinstance(word, str) or word.split() != [word]:
            raise TimelineEditError("each speech boundary row must be one exact token")
        tokens.append(word)
    if text.split() != tokens:
        raise TimelineEditError("speech words do not exactly match the complete ordered text tokens")


def validate_take(text, take, *, authored_words=None):
    """Validate a detached verified take before any authored edit or emission."""
    try:
        take_key(take["refs"])
        manifest, words, speech = take["manifest"], take["words"], take["speech"]
        audio = take["refs"]["speech"]["object_id"]
        duration = manifest["duration_seconds"]
        if (type(manifest.get("schema_version")) is not int or manifest["schema_version"] != 1
                or type(words.get("schema_version")) is not int or words["schema_version"] != 1
                or manifest["text"] != text
                or manifest["text_sha256"] != hashlib.sha256(text.encode()).hexdigest()
                or manifest["audio_sha256"] != audio[7:] or words["audio_sha256"] != audio[7:]
                or speech["object_id"] != audio
                or type(duration) not in (int, float) or not math.isfinite(duration) or duration <= 0
                or type(words["duration_seconds"]) not in (int, float)
                or type(speech["duration_seconds"]) not in (int, float)
                or duration != words["duration_seconds"] or duration != speech["duration_seconds"]
                or not isinstance(manifest["settings"], dict)
                or any(not isinstance(manifest["settings"].get(k), str) or not manifest["settings"][k]
                       for k in ("voice", "rate"))):
            raise TimelineEditError("speech text, audio, manifest or exact duration mismatch")
        rows = words["words"]
        validate_speech_boundary(text, rows)
        previous = 0
        for row in rows:
            start, end = row["start_s"], row["end_s"]
            if (any(type(v) not in (int, float) or not math.isfinite(v) for v in (start, end))
                    or not previous <= start < end <= duration):
                raise TimelineEditError("invalid finite ordered speech word timings")
            previous = end
        if authored_words is not None:
            raw = [{"start_s": r[0], "end_s": r[1], "word": r[2]} if isinstance(r, list)
                   else {k: v for k, v in r.items() if k != "id"} for r in authored_words]
            if digest(raw) != digest(rows):
                raise TimelineEditError("authored words differ from immutable speech artifact")
        return take
    except (KeyError, TypeError, ValueError, IndexError) as exc:
        if isinstance(exc, TimelineEditError):
            raise
        raise TimelineEditError(f"invalid speech artifacts: {exc}") from None


def scoped_line(item):
    oid, cid = item.get("occurrence_id"), item.get("clip_id")
    if oid is not None and (not isinstance(oid, str) or not oid):
        raise TimelineEditError("occurrence_id must be null or a nonempty string")
    if not isinstance(cid, str) or not cid:
        raise TimelineEditError("a line requires its exact clip_id")
    from astrid.sdk.timeline.commands import is_scoped_id
    sid = f"occurrence:{oid}/clip:{cid}" if oid is not None else f"parent/clip:{cid}"
    if not is_scoped_id(sid):
        raise TimelineEditError("invalid scoped narration identity")
    return sid


def line_clips(tl):
    from astrid.sdk.timeline.commands import scoped_clip
    return {scoped_clip(tl, c): c for c in tl.clips() if intent.line(c.data)}


def piece_key(clip):
    if intent.line_take(clip.data):
        from astrid.sdk.timeline.commands import scoped_clip
        return scoped_clip(clip._tl, clip)
    return clip.id


def validate_spec(spec):
    if (not isinstance(spec, dict) or set(spec) != {"version", "lines", "remove"}
            or type(spec["version"]) is not int or spec["version"] != 1
            or not isinstance(spec["lines"], list) or not isinstance(spec["remove"], list)):
        raise TimelineEditError("prepared script requires version:1, ordered lines and explicit remove")
    seen = set()
    for item in spec["lines"]:
        if (not isinstance(item, dict) or set(item) - {"occurrence_id", "clip_id", "segment", "text", "take", "gap_after_s"}
                or not {"clip_id", "segment", "text", "take"} <= set(item)
                or any(not isinstance(item[k], str) or not item[k] for k in ("segment", "text"))):
            raise TimelineEditError("invalid prepared narration line")
        sid = scoped_line(item)
        if sid in seen:
            raise TimelineEditError("duplicate scoped narration line")
        seen.add(sid)
        take_key(item["take"])
        if "gap_after_s" in item:
            gap = item["gap_after_s"]
            if type(gap) not in (int, float) or not math.isfinite(gap) or gap < 0:
                raise TimelineEditError("line gap must be finite and nonnegative")
    if (any(not isinstance(s, str) or s in seen for s in spec["remove"])
            or len(set(spec["remove"])) != len(spec["remove"])):
        raise TimelineEditError("removals must be unique and separate from retained lines")
    return spec


def apply_prepared(tl, spec):
    """Execute the existing apply-script operation with request-bound takes."""
    from astrid.sdk.timeline.commands import scoped_clip
    validate_spec(spec)
    clips = line_clips(tl)
    takes = getattr(tl, "_narration_takes", {})
    # Validate every line before touching even the detached bundle.
    for item in spec["lines"]:
        take = takes.get(take_key(item["take"]))
        if take is None:
            raise TimelineEditError("prepared script has no verified request-bound take")
        validate_take(item["text"], take)
        sid = scoped_line(item)
        existing = clips.get(sid)
        if existing is not None and intent.line(existing.data) != item["segment"]:
            raise TimelineEditError("a retained line cannot change its segment identity")
    if any(sid not in clips for sid in spec["remove"]):
        raise TimelineEditError("explicit narration removal is absent from the pinned base")
    touched = {c.shot_id for sid, c in clips.items() if sid in spec["remove"]}
    touched.update(c.shot_id for item in spec["lines"] if (c := clips.get(scoped_line(item))) is not None)
    touched.update(p["shot_id"] for item in spec["lines"] for p in tl.bundle.get("placements", [])
                   if p.get("occurrence_id") == item.get("occurrence_id"))
    # The new internal revision is narration authority. Retire stale legacy
    # descriptors in this same candidate (never advance mutable shot bindings).
    for shot_id in touched - {None}:
        payload = tl.bundle["shots"][shot_id]["payload"]
        if "text_bindings" in payload:
            payload["text_bindings"] = [b for b in payload["text_bindings"] if b.get("kind") != "voiceover_script"]
    old = tl._piece_gaps()
    points = {piece_key(c): max((w.end for w in tl.words() if (w.shot_id, w.clip_id) == (c.shot_id, c.id)), default=c.end)
              for c in clips.values()}
    pieces = tl._pieces()
    windows = []
    for sid in spec["remove"]:
        clip = clips[sid]
        following = next((c for c, _w in pieces if c.start > clip.start), None)
        windows.append((clip.start, following.start if following else points[piece_key(clip)] + (intent.gap_after(clip.data) or 0)))
        clip._remove_raw()
    for start, end in sorted(windows, reverse=True):
        tl.ripple_delete(start, end, keep_inside=True)
    scopes = {}
    for item in spec["lines"]:
        sid = scoped_line(item)
        scopes.setdefault(sid.rsplit("/clip:", 1)[0], []).append(sid)
    reorder = {}
    for scope, wanted in scopes.items():
        retained = [sid for sid in wanted if sid in clips]
        if retained != sorted(retained, key=lambda sid: clips[sid].start):
            reorder[scope] = min(clips[sid].start for sid in retained)
    previous = None
    for item in spec["lines"]:
        sid = scoped_line(item)
        take = takes[take_key(item["take"])]
        clip = clips.get(sid)
        if clip is None:
            oid = item.get("occurrence_id")
            placements = [p for p in tl.bundle.get("placements", []) if p.get("occurrence_id") == oid]
            if oid is not None and len(placements) != 1:
                raise TimelineEditError("new narration requires one exact occurrence")
            shot = placements[0]["shot_id"] if oid is not None else None
            internal = tl._internal(shot)
            if any(c.get("id") == item["clip_id"] for c in internal["clips"]):
                raise TimelineEditError("new narration clip identity already exists")
            from astrid.sdk.timeline.doc import _read_words
            start = (previous.start + _read_words(intent.words(previous.data))[-1][1] + (intent.gap_after(previous.data) or 0)
                     if previous is not None else tl._shot_start(shot))
            tl.insert_time(start, take["speech"]["duration_seconds"] + item.get("gap_after_s", .3))
            internal["clips"].append(dict(id=item["clip_id"], clipType="media", track="voice",
                                          at=start-tl._shot_start(shot), params={}))
            clip = next(c for c in tl.clips() if scoped_clip(tl, c) == sid)
        data = clip.data
        same = intent.line_take(data) == item["take"]
        if not same:
            audio = item["take"]["speech"]["object_id"]
            asset = "speech-" + audio[7:]
            entry = dict(object_id=audio, type="audio", duration=take["speech"]["duration_seconds"])
            registry = tl._registry(clip.shot_id)
            if asset in registry and registry[asset].get("object_id") != audio:
                raise TimelineEditError("speech registry key conflicts with pinned asset")
            registry[asset] = {**registry.get(asset, {}), **entry}
            data.update(asset=asset, **{"from": 0, "to": take["speech"]["duration_seconds"]})
            data.pop("hold", None)
            # Exact artifact rows, including provider metadata, are retained.
            rows = copy.deepcopy(take["words"]["words"])
            authored = ([[r["start_s"], r["end_s"], r["word"]] for r in rows]
                        if all(set(r) == {"start_s", "end_s", "word"} for r in rows) else rows)
            old_rows = intent.words(data)
            def token(row):
                return row[2] if isinstance(row, list) else row["word"]
            # Preserve existing word IDs only on exact equal runs. Candidate IDs
            # are not part of immutable artifact comparison; raw row values are.
            for block in difflib.SequenceMatcher(a=[token(r) for r in old_rows],
                    b=[token(r) for r in authored], autojunk=False).get_matching_blocks():
                for offset in range(block.size):
                    old_row, new_row = old_rows[block.a + offset], authored[block.b + offset]
                    wid = old_row[3] if isinstance(old_row, list) and len(old_row) == 4 else old_row.get("id") if isinstance(old_row, dict) else None
                    if wid is not None:
                        if isinstance(new_row, list):
                            new_row.append(wid)
                        else:
                            new_row["id"] = wid
            intent.set_line(data, item["segment"], authored)
            intent.set_line_take(data, item["take"])
            intent.set_line_text(data, item["text"])
        else:
            validate_take(item["text"], take, authored_words=intent.words(data))
        if "gap_after_s" in item:
            intent.set_gap_after(data, item["gap_after_s"])
        elif sid not in clips:
            intent.set_gap_after(data, .3)
        scope = sid.rsplit("/clip:", 1)[0]
        if scope in reorder:
            data["at"] = tl.quantize(reorder[scope]) - tl._shot_start(clip.shot_id)
            from astrid.sdk.timeline.doc import _read_words
            reorder[scope] = clip.start + _read_words(intent.words(data))[-1][1] + (intent.gap_after(data) or 0)
        previous = clip
    tl._mcache = None
    report = tl.reflow(gaps=old, points=points)
    wanted = [scoped_line(item) for item in spec["lines"]]
    actual = [scoped_clip(tl, c) for c, _words in tl._pieces() if scoped_clip(tl, c) in wanted]
    if actual != wanted:
        raise TimelineEditError("requested narration order crosses incompatible occurrence placements")
    return report


def script_intents(tl, script, *, gaps=False):
    """Adapt the established segments script to explicit scoped line intents."""
    if isinstance(script, dict) and script.get("version") == 1 and "lines" in script:
        return copy.deepcopy(script)
    if not isinstance(script, dict) or not isinstance(script.get("segments"), list):
        raise TimelineEditError("narration script requires a segments array")
    existing = line_clips(tl)
    lines, retained = [], set()
    first = next(iter(existing), None)
    previous_scope = None
    for raw in script["segments"]:
        if not isinstance(raw, dict) or not isinstance(raw.get("id"), str) or not raw["id"]:
            raise TimelineEditError("each script segment requires its exact id")
        segment = raw["id"]
        matches = [(sid, c) for sid, c in existing.items() if intent.line(c.data) == segment
                   and ("occurrence_id" not in raw or sid.startswith(
                       f"occurrence:{raw['occurrence_id']}/" if raw["occurrence_id"] is not None else "parent/"))
                   and ("clip_id" not in raw or c.id == raw["clip_id"])]
        if len(matches) > 1:
            raise TimelineEditError(f"segment {segment!r} requires occurrence_id and clip_id")
        if matches:
            sid, clip = matches[0]
            retained.add(sid)
            scope = sid.rsplit("/clip:", 1)[0]
            cid = clip.id
        else:
            scope = (f"occurrence:{raw['occurrence_id']}" if raw.get("occurrence_id") is not None else "parent") if "occurrence_id" in raw else previous_scope or (first.rsplit("/clip:", 1)[0] if first else "parent")
            cid = raw.get("clip_id", "voice-" + segment)
        oid = scope[len("occurrence:"):] if scope.startswith("occurrence:") else None
        item = dict(occurrence_id=oid, clip_id=cid, segment=segment, text=raw.get("text"))
        item.update({k: raw[k] for k in DEFAULT_SETTINGS if k in raw})
        if not matches or gaps:
            if "gap_after_s" in raw:
                item["gap_after_s"] = raw["gap_after_s"]
            elif not matches:
                item["gap_after_s"] = script.get("default_gap_after_s", .3)
        lines.append(item)
        previous_scope = scope
    return dict(version=1, lines=lines, remove=[sid for sid in existing if sid not in retained],
                **{k: script[k] for k in DEFAULT_SETTINGS if k in script})


def referenced_takes(value):
    if isinstance(value, Mapping):
        for key, child in value.items():
            if key == "take" and isinstance(child, dict) and set(child) & PORTS:
                take_key(child)
                yield child
            else:
                yield from referenced_takes(child)
    elif isinstance(value, list):
        for child in value:
            yield from referenced_takes(child)


def capture_takes(port, base, calls):
    """Resolve only original-request or pinned-base typed refs, once per take."""
    takes = {}
    # Only authored payloads, not provenance or historical base snapshots.
    payloads = [base.get("parent", {})] + [s["internal_timeline"] for s in base.get("shots", {}).values()]
    base_refs = [intent.line_take(c) for payload in payloads for c in payload.get("clips", [])
                 if intent.line_take(c) is not None]
    for refs in [*referenced_takes(calls), *base_refs]:
        key = take_key(refs)
        if key not in takes:
            if not callable(getattr(port, "narration_take", None)):
                raise TimelineEditError("Runtime request-bound narration_take is required")
            take = port.narration_take(copy.deepcopy(refs))
            if take.get("refs") != refs:
                raise TimelineEditError("Runtime returned a different managed take")
            validate_take(take["manifest"]["text"], take)
            takes[key] = copy.deepcopy(take)
    return takes


def candidate_narration(bundle, publication, takes):
    """Derive the full projection, including children absent from the delta."""
    parent = publication["parent_composition"]
    changed = {r["shot_id"]: r for r in publication["shot_revisions"]}
    internal_ids = {r["revision_id"]: r["timeline_id"]
                    for r in publication["dependency_manifest"]["internal_timelines"]}
    contexts = [(None, None, None, None, None, parent)]
    for occurrence in parent["occurrences"]:
        oid, sid, srid = (occurrence[k] for k in ("occurrence_id", "shot_id", "shot_revision_id"))
        shot = bundle["shots"][sid]
        source = bundle["source_mapping"]["shots"][sid]
        irid = changed[sid]["internal_timeline_revision_id"] if sid in changed else source["internal_timeline_revision_id"]
        contexts.append((oid, sid, srid, internal_ids[irid], irid, shot["internal_timeline"]))
    lines = []
    for oid, sid, srid, itid, irid, payload in contexts:
        for clip in payload.get("clips", []):
            refs = intent.line_take(clip)
            if refs is None:
                continue
            take = takes.get(take_key(refs))
            if take is None:
                raise TimelineEditError("candidate narration has an uncaptured take")
            validate_take(intent.line_text(clip), take, authored_words=intent.words(clip))
            asset = payload.get("registry", {}).get("assets", {}).get(clip.get("asset"), {})
            if asset.get("object_id") != refs["speech"]["object_id"]:
                raise TimelineEditError("authored speech asset differs from managed take")
            lines.append(dict(occurrence_id=oid, shot_id=sid, shot_revision_id=srid,
                              internal_timeline_id=itid, internal_revision_id=irid,
                              clip_id=clip["id"], segment=intent.line(clip), take=copy.deepcopy(refs),
                              line_digest="sha256:" + digest(clip)))
    return dict(version=1, lines=sorted(lines, key=lambda r: (r["occurrence_id"] is not None,
                                                            r["occurrence_id"] or "", r["clip_id"])))


def read_managed_take(client, project_id, refs):
    """Preparation-only managed reads. COMMIT always uses its request port."""
    from astrid.sdk.timeline.saved_publish import _workspace
    workspace = _workspace(client)
    take_key(refs)
    associations, documents = [], {}
    for port, ref in refs.items():
        association = workspace.get_managed_output(ref["association_id"])
        if (association.get("project_id") != project_id or association.get("object_id") != ref["object_id"]
                or association.get("output_port") != port or association.get("durability") != "durable"
                or association.get("lifecycle", {}).get("state") not in {"available", "promoted"}):
            raise TimelineEditError("speech preparation requires project-owned settled durable outputs")
        raw = workspace.get_object(ref["object_id"])["data"]
        if (not isinstance(raw, bytes) or len(raw) != association["size"]
                or "sha256:" + hashlib.sha256(raw).hexdigest() != ref["object_id"]):
            raise TimelineEditError("managed speech bytes differ from immutable output")
        if port != "speech":
            if association.get("media_type") != "application/json":
                raise TimelineEditError("speech auxiliaries must be JSON")
            documents[port] = json.loads(raw)
        elif not association.get("media_type", "").startswith("audio/"):
            raise TimelineEditError("speech output must be audio")
        associations.append(association)
    if len({(a["task_id"], a["attempt_id"]) for a in associations}) != 1:
        raise TimelineEditError("speech outputs must share one settled task attempt")
    audio = next(a for a in associations if a["output_port"] == "speech")
    take = dict(refs=copy.deepcopy(refs), manifest=documents["speech_manifest"], words=documents["speech_words"],
                speech={k: audio[k] for k in ("object_id", "size", "media_type")})
    take["speech"]["duration_seconds"] = take["manifest"]["duration_seconds"]
    return validate_take(take["manifest"]["text"], take)


def prepare_script(tl, script, *, client, preparation_id, allow_generation=True):
    """Prepare all changed/new takes using the existing idempotent capability.

    Returns a prepared OpCall and detached verification context. It edits no
    authored document, binding or journal; settled task outputs can remain if a
    later line fails. The caller records the single OpCall only after success.
    """
    from astrid.sdk.invocation import invoke
    if (not isinstance(preparation_id, str) or not preparation_id or not isinstance(script, dict)
            or type(script.get("version")) is not int or script["version"] != 1
            or not isinstance(script.get("lines"), list) or not isinstance(script.get("remove"), list)
            or set(script) - {"version", "lines", "remove", *DEFAULT_SETTINGS}):
        raise TimelineEditError("managed script requires version, ordered scoped lines and explicit remove")
    before = tl.document()
    base_revision = before.get("base_parent", {}).get("revision_id")
    if not isinstance(base_revision, str) or not base_revision:
        raise TimelineEditError("speech preparation requires a pinned base revision")
    project = before["project_id"]
    existing, takes, lines = line_clips(tl), {}, []
    for raw in script["lines"]:
        if not isinstance(raw, dict) or set(raw) - {"occurrence_id", "clip_id", "segment", "text", "take", "gap_after_s", *DEFAULT_SETTINGS}:
            raise TimelineEditError("invalid managed script line")
        item = {k: copy.deepcopy(v) for k, v in raw.items() if k not in DEFAULT_SETTINGS}
        sid = scoped_line(item)
        clip = existing.get(sid)
        old = intent.line_take(clip.data) if clip else None
        old_take = read_managed_take(client, project, old) if old is not None else None
        explicit_take = read_managed_take(client, project, item["take"]) if "take" in item else None
        inherited = explicit_take or old_take
        settings = {**DEFAULT_SETTINGS, **(inherited["manifest"]["settings"] if inherited else {}),
                    **{k: script[k] for k in DEFAULT_SETTINGS if k in script},
                    **{k: raw[k] for k in DEFAULT_SETTINGS if k in raw}}
        settings = {k: settings[k] for k in DEFAULT_SETTINGS}
        if any(not isinstance(v, str) or not v for v in settings.values()):
            raise TimelineEditError("resolved speech settings must be nonempty strings")
        text = item.get("text")
        if not isinstance(text, str) or not text.split():
            raise TimelineEditError("speech line requires exact nonempty text")
        if "take" in item:
            selected = explicit_take
        elif (old_take is not None and old_take["manifest"]["text"] == text
              and all(old_take["manifest"]["settings"].get(k, DEFAULT_SETTINGS[k]) == v for k, v in settings.items())):
            selected = old_take
        else:
            if not allow_generation:
                raise TimelineEditError("prepare managed speech takes before previewing a changed script")
            outcome = invoke("generation.generate_speech", kind="executor", client=client, project=project,
                             inputs={"text": text, **settings}, wait=True, read_managed_outputs=True,
                             idempotency_context=dict(operation="timeline.apply-script", preparation_id=preparation_id,
                                 base_revision_id=base_revision, line=sid, inputs_digest=digest({"text": text, **settings})))
            if not outcome.ok:
                raise TimelineEditError(f"speech preparation failed for {sid}: {outcome.error}")
            outputs = outcome.outputs.get("managed_outputs", [])
            refs = {p: [{k: a[k] for k in ("association_id", "object_id")} for a in outputs
                         if a.get("output_port") == p] for p in PORTS}
            if any(len(values) != 1 for values in refs.values()):
                raise TimelineEditError("speech task must settle exactly one output for every take port")
            selected = read_managed_take(client, project, {p: values[0] for p, values in refs.items()})
        validate_take(text, selected)
        if any(selected["manifest"]["settings"].get(k, DEFAULT_SETTINGS[k]) != v for k, v in settings.items()):
            raise TimelineEditError("selected speech take differs from resolved voice/rate settings")
        item["take"] = copy.deepcopy(selected["refs"])
        takes[take_key(item["take"])] = selected
        lines.append(item)
    spec = validate_spec(dict(version=1, lines=lines, remove=copy.deepcopy(script["remove"])))
    if before != tl.document():
        raise TimelineEditError("authored base changed during speech preparation")
    return dict(op="timeline.apply-script", select=None, args=dict(spec=spec)), takes


def apply_managed_script(tl, script, *, client, preparation_id, gaps=False, allow_generation=True):
    """SDK/CLI adapter: all preparation, then one ordinary atomic edit."""
    from astrid.sdk.timeline.commands import run
    command, takes = prepare_script(tl, script_intents(tl, script, gaps=gaps), client=client,
                                    preparation_id=preparation_id, allow_generation=allow_generation)
    previous = getattr(tl, "_narration_takes", None)
    tl._narration_takes = takes
    try:
        return run(tl, command)
    finally:
        if previous is None:
            tl.__dict__.pop("_narration_takes", None)
        else:
            tl._narration_takes = previous
