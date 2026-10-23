"""Duplicate a timeline into a new one, with new shot and occurrence ids.

Shot ids are global per project, so a duplicate can never reuse the source's
shot ids. The copy is built the way ``production/scripts/build_timeline.py``
builds a candidate: an authoring shot per source placement, each with its own
internal timeline, registry and placement row, published as one revision of
the new (empty) timeline.

Pure parts (``id_map``, ``copy_content``) take and return plain dicts; only
``duplicate_timeline`` talks to the runtime.
"""
from __future__ import annotations

import copy
import sys
import uuid
from collections.abc import Iterable, Mapping
from typing import Any

from astrid.core.timeline.astrid_ns import migrate_bundle
from astrid.sdk.timeline_checkout import Checkout, TimelineEditError
from astrid.sdk.timeline_editing import add_authoring_shot
from astrid.sdk.timeline_restructure import STRUCTURE_KEY, flatten

__all__ = ["duplicate_timeline", "id_map", "copy_content"]


def _commit_bundle(project: str, timeline: str, desired: Mapping[str, Any], *, label: str,
                   client: Any, idempotency_key: str) -> dict[str, Any]:
    """Commit a prepared bundle through the public session and G3 emitter.

    New closure identities must be introduced by the existing semantic carrier;
    authored parent and child content is then emitted as source-bound patches.
    Keeping the session's generated closure metadata avoids rebuilding Runtime
    identities in this caller.
    """
    from astrid.sdk.timeline import open as open_timeline
    from astrid.sdk.workspace_client import WorkspaceClientError

    checked = Checkout({})
    checked.bundle = copy.deepcopy(dict(desired))
    checked._refresh()
    report = checked._check_core()
    if not report.valid:
        raise TimelineEditError("not committing: " + "; ".join(report.problems or ["the candidate is invalid"]))
    session = open_timeline(project, timeline, client=client)
    with session.session.outbox.locked():
        state = session.session._state()
    flight = state["flight"]
    if flight is not None and flight["key"] == f"{idempotency_key}-narration"[:120]:
        # The cut already landed; recover its original receipt from Runtime
        # before reconciling the separate durable narration flight below.
        result = _copy_acceptance(client, project, timeline, state["base"]["publication_id"], idempotency_key)
    else:
        if not state["pending"] and flight is None:
            _stage_bundle(session, desired)
        # An unknown outcome owns its original body/key. Reconcile it before
        # capturing any new births or patches, including after a restart.
        result = session.commit(label, merge="atomic", idempotency_key=idempotency_key)
    data = result["data"]
    receipt = {
        "old_head": data.get("previous_revision_id"),
        "new_head": data.get("accepted_revision_id"),
        "structure": "changed",
        "receipt": result.get("receipt"),
        "idempotency_key": (result.get("receipt") or {}).get("idempotency_key", idempotency_key),
        "narration_pinned": [],
        "transcripts": [],
        "message": data.get("rationale", label),
    }
    try:
        narration = session._publish_narration(idempotency_key, client=client)
        receipt.update(narration)
    except (TimelineEditError, WorkspaceClientError) as exc:
        receipt["narration_error"] = (
            f"{exc}. The cut is published (head {receipt.get('new_head')}); only the narration binding is behind: "
            "retry the original commit to reconcile the durable narration commit"
        )
    from astrid.sdk import timeline_transcripts as transcripts

    try:
        if any(item["status"] == "planned" for item in transcripts.plan_narration_transcripts(session)):
            receipt["transcripts"] = transcripts.sync_narration_transcripts(session, client, project)
    except Exception as exc:  # noqa: BLE001 - the timeline commit is already durable
        print(f"note: narration transcript registration failed: {exc}", file=sys.stderr)
    for item in receipt["transcripts"]:
        if item["status"] == "skipped":
            print(f"note: narration transcript {item['label']}: {item.get('reason', 'skipped')}", file=sys.stderr)
    return receipt


def _copy_acceptance(client: Any, project: str, timeline: str, publication: str, key: str) -> dict[str, Any]:
    """Read the cut's receipt from the existing history, without a local ledger."""
    cursor = None
    seen = set()
    while True:
        page = client.timelines.history(project, timeline, cursor=cursor, limit=200)
        if not page.ok:
            raise TimelineEditError(f"could not read the accepted copy before narration retry: {page.error}")
        for entry in page.data["items"]:
            receipt = entry.get("receipt") or {}
            if receipt.get("receipt_id") == publication and receipt.get("idempotency_key") == key:
                return {"data": copy.deepcopy(receipt["result"]), "receipt": copy.deepcopy(receipt)}
        cursor = page.data.get("next_cursor")
        if cursor is None or cursor in seen:
            raise TimelineEditError("the original copy receipt is unavailable; reconcile the narration session directly")
        seen.add(cursor)


def _stage_bundle(session: Any, desired: Mapping[str, Any]) -> None:
    """Capture one structural copy using existing commands and payload patches."""
    from astrid.sdk.timeline._doc_patch import Closure
    from astrid.sdk.timeline.native_occurrence_create import capture_occurrence_create
    from astrid.sdk.timeline.native_occurrence_delete import capture_occurrence_delete

    if desired.get("base_parent", {}).get("revision_id") != session.head["revision_id"]:
        raise TimelineEditError("timeline head changed while preparing the copy; reopen before committing")
    desired_rows = {str(row["occurrence_id"]): row for row in desired.get("placements") or []}
    retired_rows = [row for row in session._command_bundle.get("placements") or []
                    if str(row["occurrence_id"]) not in desired_rows]

    # Births read their output track. Stage authored tracks before capturing
    # them, while leaving media/clip content for the final payload patch.
    tracks = copy.deepcopy(desired["parent"].get("config", {}).get("tracks", []))
    fallback_track = "timeline-copy-output"
    while any(track["id"] == fallback_track for track in tracks):
        fallback_track += "-copy"
    if any(not isinstance((row.get("placement") or {}).get("track", row.get("track")), str)
           for row in desired_rows.values()):
        # Legacy placements can have an implicit lane. Birth still requires an
        # explicit lane at its sequential boundary; the final patch restores
        # the original absent field and removes this temporary track.
        tracks.append({"id": fallback_track, "kind": "visual"})
    session.bundle["parent"].setdefault("config", {})["tracks"] = tracks
    session._capture_free_edits()
    for row in desired.get("placements") or []:
        shot_id = str(row["shot_id"])
        if any(item["occurrence_id"] == row["occurrence_id"]
               for item in session._command_bundle.get("placements") or []):
            continue
        shot = (desired.get("shots") or {}).get(shot_id) or {}
        payload = shot.get("payload") or {}
        placement = row.get("placement") or {}
        track = placement.get("track", row.get("track", fallback_track))
        start_ms = placement.get("start_ms", row.get("at_ms", 0))
        duration_ms = row.get("duration_ms")
        if not isinstance(start_ms, (int, float)) or not isinstance(duration_ms, (int, float)):
            raise TimelineEditError(f"copy of shot {shot_id!r} has invalid placement timing")
        command = capture_occurrence_create(
            session._command_bundle,
            str(row["occurrence_id"]),
            shot_id,
            name=str(payload.get("name") or ""),
            track=track,
            on=float(start_ms) / 1000.0,
            duration=float(duration_ms) / 1000.0,
        )
        session._append([command], label=f"Create shot {shot_id}")

    # Placement geometry is authored data; only closure links belong to Runtime.
    # Patch each complete canonical row without inventing or replacing its edges.
    for row in desired.get("placements") or []:
        rows = Closure(session._command_bundle).payload("parent")["occurrences"]
        actual = next(item for item in rows if item["occurrence_id"] == row["occurrence_id"])
        replacement = copy.deepcopy(dict(row))
        for key in ("occurrence_id", "shot_id", "shot_revision_id", "revision_id"):
            replacement.pop(key, None)
            if key in actual:
                replacement[key] = actual[key]
        if replacement != actual:
            change = {"op": "set", "ref": "parent", "path": ["occurrences", "occurrence_id:" + row["occurrence_id"]],
                      "before": {"state": "present", "value": actual}, "value": replacement}
            session._append([{"schema_version": 1, "op": "doc.patch", "version": "1", "select": None,
                              "args": {"changes": [change]}}], label=f"Copy placement {row['occurrence_id']}")
    current = copy.deepcopy(session._command_bundle)
    current["parent"] = copy.deepcopy(desired["parent"])
    for shot_id, shot in (desired.get("shots") or {}).items():
        if shot_id not in current.get("shots", {}):
            raise TimelineEditError(f"semantic occurrence creation omitted shot {shot_id!r}")
        payload = copy.deepcopy(shot["payload"])
        # The source's child revision pin is never a destination identity.
        payload.pop("internal_timeline_revision_id", None)
        if "internal_timeline_revision_id" in current["shots"][shot_id]["payload"]:
            payload["internal_timeline_revision_id"] = current["shots"][shot_id]["payload"]["internal_timeline_revision_id"]
        current["shots"][shot_id]["payload"] = payload
        current["shots"][shot_id]["internal_timeline"] = copy.deepcopy(shot["internal_timeline"])
    session.bundle = current
    session._capture_free_edits()
    # Keep old roots addressable until all payload patches have been captured.
    for row in retired_rows:
        command = capture_occurrence_delete(session._command_bundle, "occurrence:" + str(row["occurrence_id"]))
        session._append([command], label=f"Remove placement {row['occurrence_id']}")

# Payload fields that point at the source's own runtime records. They are not
# copied: the new shot gets its own records on the next publish.
_SOURCE_BOUND_PAYLOAD_KEYS = ("text_bindings", "internal_timeline_revision_id")


def _common_prefix(values: list[str]) -> str:
    if not values:
        return ""
    prefix = values[0]
    for value in values[1:]:
        while not value.startswith(prefix):
            prefix = prefix[:-1]
    # Cut back to a '-' boundary so suffixes stay whole words.
    return prefix[: prefix.rfind("-") + 1] if "-" in prefix else ""


def id_map(old_ids: Iterable[str], new_slug: str) -> dict[str, str]:
    """Map each old id to ``<new_slug>-<suffix>``, where suffix is the id after the ids' shared prefix.

    ``["p-ch01-a", "p-ch02-b"]`` with slug ``dup`` gives ``{"p-ch01-a": "dup-ch01-a", "p-ch02-b": "dup-ch02-b"}``.
    A single id keeps its whole text as the suffix. Old ids must be unique; the result is injective.
    """
    ids = [str(i) for i in old_ids]
    if len(set(ids)) != len(ids):
        raise TimelineEditError("cannot map duplicate source ids")
    prefix = _common_prefix(ids) if len(ids) > 1 else ""
    mapping: dict[str, str] = {}
    for old in ids:
        suffix = old[len(prefix):] or old
        mapping[old] = f"{new_slug}-{suffix}"
    if len(set(mapping.values())) != len(mapping):
        raise TimelineEditError("id mapping is not one-to-one; choose another slug")
    return mapping


def _remap_values(value: Any, mapping: Mapping[str, str]) -> Any:
    """Replace every string that is exactly a mapped id (values only, never substrings)."""
    if isinstance(value, str):
        return mapping.get(value, value)
    if isinstance(value, list):
        return [_remap_values(v, mapping) for v in value]
    if isinstance(value, dict):
        return {k: _remap_values(v, mapping) for k, v in value.items()}
    return value


def copy_content(source: Mapping[str, Any], target: Mapping[str, Any], *, new_slug: str) -> tuple[dict[str, Any], list[str]]:
    """Return a copy of ``target`` (keeping its provenance and identity) holding ``source``'s content.

    Shots, placements and occurrences get new ids (``id_map``). Returns ``(bundle, notes)``
    where notes say what was not carried over.
    """
    notes: list[str] = []
    placements = [dict(row) for row in source.get("placements") or []]
    shot_ids = [str(row["shot_id"]) for row in placements]
    occurrence_ids = [str(row["occurrence_id"]) for row in placements]
    shot_map = id_map(list(dict.fromkeys(shot_ids)), new_slug)  # a shot the source places twice is ONE shot
    occ_map = id_map(occurrence_ids, f"occ-{new_slug}")
    ids = {**shot_map, **occ_map}

    out = copy.deepcopy(dict(target))
    src_parent = source.get("parent") or {}
    out["parent"] = {
        **dict(out.get("parent") or {}),
        "config": copy.deepcopy(src_parent.get("config") or {}),
        "registry": _remap_values(copy.deepcopy(src_parent.get("registry") or {}), ids),
        "clips": _remap_values(copy.deepcopy(src_parent.get("clips") or []), ids),
    }
    out["shots"] = {}
    out["placements"] = []
    out["source_mapping"] = {"placements": {}, "shots": {}}

    text_bindings = 0
    for row in placements:
        old_shot = str(row["shot_id"])
        new_shot = shot_map[old_shot]
        src_shot = (source.get("shots") or {}).get(old_shot)
        if not isinstance(src_shot, Mapping):
            raise TimelineEditError(f"source shot {old_shot!r} has no content")
        if new_shot in out["shots"]:  # placed again: same shot, another occurrence
            again = _remap_values(copy.deepcopy(row), ids)
            again["shot_id"], again["occurrence_id"] = new_shot, occ_map[str(row["occurrence_id"])]
            out["placements"].append(again)
            out["source_mapping"]["placements"][again["occurrence_id"]] = copy.deepcopy(again)
            continue
        # Seed the shot the way build_timeline does (add_authoring_shot). Its base_* stays the empty seed
        # and the current content is the copy: that difference is what makes the compiler materialize it.
        shot = add_authoring_shot(out, shot_id=new_shot, occurrence_id=occ_map[str(row["occurrence_id"])],
                                  start_ms=(row.get("placement") or {}).get("start_ms", 0))
        payload = copy.deepcopy(dict(src_shot.get("payload") or src_shot.get("base_payload") or {}))
        text_bindings += len(payload.get("text_bindings") or [])
        for key in _SOURCE_BOUND_PAYLOAD_KEYS:
            payload.pop(key, None)
        payload["text_bindings"] = []
        shot["payload"] = payload
        shot["internal_timeline"] = _remap_values(copy.deepcopy(dict(src_shot.get("internal_timeline") or {})), shot_map)
        new_row = _remap_values(copy.deepcopy(row), ids)
        new_row["shot_id"] = new_shot
        new_row["occurrence_id"] = occ_map[str(row["occurrence_id"])]
        out["placements"][-1] = new_row  # replaces the placement add_authoring_shot appended
        out["source_mapping"]["placements"][new_row["occurrence_id"]] = copy.deepcopy(new_row)

    if text_bindings:
        from astrid.sdk.timeline_checkout import Checkout

        bound = Checkout(copy.deepcopy(out)).narration()
        if len(bound) == len(out.get("shots") or {}):
            notes.append(f"narration: bound again from each line's script text ({len(bound)} shots)")
        else:
            notes.append(f"{text_bindings} narration text binding(s) not copied (these lines declare no script text); "
                         "the words themselves are copied in each VO clip's app.words")
    migrate_bundle(out)  # the source may be an old revision: the copy carries intent under app.astrid
    assert_copy_equals_source(source, out, shot_map)
    return out, notes


def assert_copy_equals_source(source: Mapping[str, Any], copied: Mapping[str, Any], shot_map: Mapping[str, str]) -> None:
    """Prove ``copied`` is a faithful copy of ``source`` (its input) under ``shot_map``, or raise.

    This proves the copy equals the bundle it was given, not that the bundle is the right form of the film;
    ``_duplicate`` separately compares against what the source itself stores.

    Same number of placements; distinct source shots map to distinct new shots (a shot placed twice stays one shot
    placed twice); each placement keeps its start and length; each shot's clips are the source's, ids remapped.
    """
    src_rows, new_rows = list(source.get("placements") or []), list(copied.get("placements") or [])
    if len(src_rows) != len(new_rows):
        raise TimelineEditError(f"the copy has {len(new_rows)} placements, its source has {len(src_rows)}")
    if len(set(shot_map.values())) != len(shot_map):
        raise TimelineEditError("the copy maps distinct source shots onto one shot id")
    for a, b in zip(src_rows, new_rows):
        if shot_map.get(str(a["shot_id"])) != str(b["shot_id"]):
            raise TimelineEditError(f"placement of shot {a['shot_id']!r} was copied onto {b['shot_id']!r}, not {shot_map.get(str(a['shot_id']))!r}")
        if (a.get("placement") or {}) != (b.get("placement") or {}) or a.get("duration_ms") != b.get("duration_ms"):
            raise TimelineEditError(f"placement of shot {a['shot_id']!r} changed its start or length in the copy")
    if len({str(r["shot_id"]) for r in new_rows}) != len({str(r["shot_id"]) for r in src_rows}):
        raise TimelineEditError("the copy has a different number of distinct shots than its source")
    migrated: dict[str, Any] = copy.deepcopy(dict(source))
    migrate_bundle(migrated)  # the copy carries intent under app.astrid
    for old, new in shot_map.items():
        want = _remap_values(copy.deepcopy(dict((migrated["shots"][old].get("internal_timeline")) or {})), shot_map)
        got = (copied.get("shots") or {}).get(new, {}).get("internal_timeline") or {}
        if (want.get("clips") or []) != (got.get("clips") or []):
            raise TimelineEditError(f"shot {old!r} was not copied faithfully into {new!r} (its clips differ)")


def duplicate_timeline(project: str, source: str, *, slug: str | None = None, name: str | None = None,
                       revision_id: str | None = None, client: Any = None) -> dict[str, Any]:
    """Create a timeline with a copy of ``source``'s head (new shot ids) and publish it.

    Returns ``{"timeline_id", "slug", "source", "shots", "old_head", "new_head", "notes"}``.
    If the copy fails after the timeline exists, the error names that timeline so it can be archived.
    """
    if client is not None:
        return _duplicate(client, project, source, slug=slug, name=name, revision_id=revision_id)
    from astrid.sdk import AstridClient

    with AstridClient.open_from_launcher(start_pack_host=False) as opened:
        return _duplicate(opened, project, source, slug=slug, name=name, revision_id=revision_id)


def _duplicate(client: Any, project: str, source: str, *, slug: str | None, name: str | None,
               revision_id: str | None) -> dict[str, Any]:
    src = Checkout.open(project, source, revision_id=revision_id, client=client)
    report = src._check_core()  # all or nothing: refuse an invalid head BEFORE creating anything
    if not report.valid:
        raise TimelineEditError(f"not duplicating {source}: its head is not valid ("
                                + "; ".join((report.blocking or report.problems or ["invalid"])[:3]) + "); nothing was created")
    created = client.timelines.create_empty(
        project=project,
        timeline_id=slug or None,
        **({"name": name} if name is not None else {}),
        config=copy.deepcopy(dict((src.bundle.get("parent") or {}).get("config") or {})),
        idempotency_key=f"dup-{uuid.uuid4().hex}",
    )
    if not created.ok:
        error = getattr(created.error, "message", created.error)
        raise TimelineEditError(f"could not create the timeline: {error}")
    row = created.data if isinstance(created.data, Mapping) else {}
    new_id = str(row.get("timeline_id") or slug or "")
    if not new_id:
        raise TimelineEditError("the runtime created a timeline but returned no id")
    try:
        dst = Checkout.open(project, new_id, client=client)
        # A chapter film is read flat (ONE shot; its stored form is kept under structure_base). Copy the stored
        # form: copying the flat shot would store the duplicate as a single shot whose chapters all share one id.
        content = src.bundle.get(STRUCTURE_KEY) or src.bundle
        bundle, notes = copy_content(content, dst.bundle, new_slug=slug or new_id)
        dst.bundle = flatten(bundle)  # a chapter film is edited and published flat; publish splits it back into its stored form
        dst.notes.extend(notes)
        # What publish will store for the copy must have as many distinct shots as what the SOURCE stores. The source
        # side is read independently of `content`, so copying the wrong form of the source is caught here.
        copy_shots = {str(r["shot_id"]) for r in dst.stored_document()["placements"]}
        source_shots = {str(r["shot_id"]) for r in src.stored_document()["placements"]}
        if len(copy_shots) != len(source_shots):
            raise TimelineEditError(f"the copy would be stored with {len(copy_shots)} distinct shots, its source stores {len(source_shots)}")
        report = dst._check_core()
        if not report.valid:
            raise TimelineEditError("the copy is invalid: " + "; ".join(report.problems or [str(report)]))
        receipt = _commit_bundle(
            project,
            new_id,
            bundle,
            label=f"duplicate of {source}",
            client=client,
            idempotency_key=f"dup-{uuid.uuid4().hex}",
        )
    except Exception as exc:
        archived = client.timelines.archive(project, new_id)  # all or nothing: the empty timeline goes too
        if getattr(archived, "ok", False):
            raise TimelineEditError(f"{exc} (nothing kept: the new timeline {new_id!r} was archived again)") from exc
        raise TimelineEditError(f"{exc} (the empty timeline {new_id!r} was created and could not be archived: "
                                f"`timelines archive {new_id} --project {project}`)") from exc
    return {
        "timeline_id": new_id,
        "slug": slug,
        "source": source,
        "shots": len(bundle["shots"]),
        "old_head": receipt.get("old_head"),
        "new_head": receipt.get("new_head"),
        "notes": list(dst.notes),
    }
