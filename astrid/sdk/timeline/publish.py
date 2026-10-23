"""Checkout: publish, narration binding, and the document as it is saved (annotated) and read back (absorb)."""
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
from typing import Any, Mapping

from astrid.sdk import timeline_intent as intent
from astrid.core.timeline.cuts import (
    clip_duration,
)

from astrid.sdk.timeline import store as _store
from astrid.sdk.timeline._common import (EDITABLE_NOTE, TimelineEditError, _num, _r)
from astrid.sdk.timeline.doc import (_row_start, _set_length, _strip_derived)
from astrid.sdk.timeline.model import Voice


_NARRATION_MEDIA_TYPE = "text/plain; charset=utf-8"


def _narration_descriptor(text: str) -> tuple[dict[str, Any], bytes]:
    """Return the exact managed-object descriptor and bytes for one narration line."""
    raw = text.encode("utf-8")
    digest = "sha256:" + hashlib.sha256(raw).hexdigest()
    return ({"object_id": digest, "digest": digest, "size": len(raw),
             "media_type": _NARRATION_MEDIA_TYPE}, raw)


def _narration_occurrence(bundle: Mapping[str, Any], shot_id: str) -> str:
    """Resolve a narration shot to its sole occurrence-owned binding target."""
    matches = [row for row in bundle.get("placements") or []
               if isinstance(row, Mapping) and row.get("shot_id") == shot_id]
    if len(matches) != 1 or not isinstance(matches[0].get("occurrence_id"), str):
        raise TimelineEditError(
            f"narration binding for shot {shot_id!r} requires one exclusive occurrence; "
            "the current Main shot binding has no commit-owned occurrence seam"
        )
    return "occurrence:" + matches[0]["occurrence_id"]


def _capture_narration_commands(
    bundle: dict[str, Any], changes: Mapping[str, str]
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Capture narration changes as native commands and update a local preview.

    Runtime re-verifies each descriptor at commit admission.  The local preview
    only supplies the exact command guards; it never authorizes a film write.
    """
    from astrid.sdk.timeline.commands import execute
    from astrid.sdk.timeline.native_text_binding import capture_text_binding_set

    local = copy.deepcopy(bundle)
    commands: list[dict[str, Any]] = []
    verified: list[dict[str, Any]] = []
    for shot_id, text in changes.items():
        owner = _narration_occurrence(local, shot_id)
        descriptor, raw = _narration_descriptor(text)
        verified_descriptor = {**descriptor, "utf8": True}
        command = capture_text_binding_set(
            local, owner, {"kind": "voiceover_script", "slot": None},
            text=descriptor, verified_text=[verified_descriptor],
        )
        commands.append(command)
        verified.append(verified_descriptor)
        local = execute(local, [command], verified_media=[verified_descriptor]).bundle
        # Keep the bytes alive through this helper's boundary.  The descriptor
        # is the custody witness; Runtime performs the authoritative read.
        if len(raw) != descriptor["size"]:
            raise TimelineEditError(f"narration source bytes changed for shot {shot_id!r}")
    return commands, verified


class _PublishMixin:
    """Checkout: publish, narration binding, and the document as it is saved (annotated) and read back (absorb)."""

    bundle: dict[str, Any]  # set by Checkout.__init__; declared so this mixin's readers are typed
    _journal: list[tuple[str, str | None]]

    def publish(self, message: str = "", *, idempotency_key: str | None = None, client: Any = None,
                force: bool = False, restructure: bool = False) -> dict[str, Any]:
        raise TimelineEditError("detached publication is retired; use timeline.open().commit(label)")

    def _reset_base(self, *, client: Any = None) -> None:
        """Re-read the new head as this working copy's bundle and save it with no undo step. Never fails the publish."""
        try:
            head = _store.fetch_bundle(str(self.bundle["project_id"]), str(self.bundle["timeline_id"]), client=client)
        except Exception as exc:  # noqa: BLE001 - the publish stands; the working copy keeps its old base
            self.notes.append(f"published, but this working copy could not re-read the new head ({exc}); "
                              "its base is still the old one: timelines checkout TL --fresh")
            return
        from astrid.sdk.timeline_restructure import flatten

        head = flatten(head)
        old, old_journal = self.bundle, list(self._journal)
        self.bundle, self._mcache, self._journal, self._disk = head, None, [], None
        try:
            target = Path(self.path)
            with _store._file_lock(target):
                self._save_locked(target, force=True, record=False)
        except Exception as exc:  # noqa: BLE001
            self.bundle, self._journal = old, old_journal
            self.notes.append(f"published, but this working copy could not be reset to the new head ({exc}); "
                              "its base is still the old one")

    def _publish_narration(self, key: str, *, client: Any = None) -> dict[str, Any]:
        def run(c: Any) -> dict[str, Any]:
            from astrid.sdk.timeline.checkout import Checkout
            from astrid.sdk.timeline.sync import TimelineSession

            project_id = str(self.bundle["project_id"])
            timeline_id = str(self.bundle["timeline_id"])
            session = TimelineSession.open(project_id, timeline_id, client=c)
            with session.outbox.locked():
                state = session._state()
            flight = state.get("flight")
            commit_key = f"{key}-narration"[:120]
            pinned: list[str] = []
            if flight is not None:
                try:
                    flight_body = json.loads(flight.get("body", "{}"))
                except (AttributeError, TypeError, ValueError):
                    flight_body = {}
                flight_commands = flight_body.get("commands")
                if (flight_body.get("label") != "Bind narration"
                        or not isinstance(flight_commands, list)
                        or not flight_commands
                        or not all(isinstance(command, Mapping)
                                   and command.get("op") == "text-binding.set"
                                   for command in flight_commands)):
                    raise TimelineEditError(
                        "another timeline request is awaiting reconciliation; retry that request before narration"
                    )
                # The durable flight owns the original key and body. A later
                # publish invocation may generate a new outer key, but must
                # still retry this exact narration request.
                occurrence_shots = {
                    str(row["occurrence_id"]): str(row["shot_id"])
                    for row in self.bundle.get("placements") or []
                    if isinstance(row, Mapping)
                    and isinstance(row.get("occurrence_id"), str)
                    and isinstance(row.get("shot_id"), str)
                }
                pinned = [
                    occurrence_shots.get(str(command["select"]).removeprefix("occurrence:"),
                                         str(command["select"]).removeprefix("occurrence:"))
                    for command in flight_commands
                    if isinstance(command.get("select"), str)
                ]
                result = session.flush(idempotency_key=flight["key"])
            else:
                if state.get("pending"):
                    raise TimelineEditError(
                        "another timeline request is pending; flush it before narration binding"
                    )
                bundle = session._bundle(state)
                changes = Checkout(bundle).narration_changes()
                if not changes:
                    return {"narration_pinned": []}
                pinned = list(changes)

                # Ingest the exact UTF-8 source bytes as ordinary project
                # media; the film-affecting association is made only by the
                # commit below.
                for shot_id, text in changes.items():
                    descriptor, raw = _narration_descriptor(text)
                    imported = c.media.import_bytes(
                        project=project_id, data=raw,
                        filename=f"narration-{shot_id}.txt",
                        media_type=_NARRATION_MEDIA_TYPE,
                        idempotency_key=f"{key}-narration-media-{shot_id}"[:120],
                    )
                    if getattr(imported, "ok", True) is False:
                        raise TimelineEditError(
                            f"could not retain narration source bytes for shot {shot_id}: "
                            f"{getattr(imported, 'error', imported)}"
                        )
                    returned = getattr(imported, "data", imported)
                    if isinstance(returned, Mapping):
                        returned_id = returned.get("object_id") or returned.get("digest")
                        if returned_id is not None and returned_id != descriptor["object_id"]:
                            raise TimelineEditError(
                                f"narration source custody mismatch for shot {shot_id}: "
                                f"Runtime retained {returned_id!r}, expected {descriptor['object_id']!r}"
                            )
                commands, _ = _capture_narration_commands(bundle, changes)
                steps = [{
                    "id": f"step-{index}",
                    "label": f"Bind narration for {shot_id}",
                    "intent": "bind narration script text",
                    "tags": ["narration", "voiceover_script"],
                    "command_ordinals": [index],
                    "patch": [],
                } for index, shot_id in enumerate(changes)]
                result = session.submit(
                    commands, label="Bind narration", steps=steps, merge="fields", reads=[],
                    idempotency_key=commit_key, expected_state=state, base=state["base"],
                    evaluation={"kind": "label", "count": 0},
                )
            accepted = result["data"]["accepted_revision_id"]
            return {"narration_pinned": pinned, "new_head": accepted, "narration_head": accepted}

        if client is not None:
            return run(client)
        from astrid.sdk import AstridClient

        with AstridClient.open_from_launcher(start_pack_host=False) as c:
            return run(c)

    # ---- narration: the script text each shot is bound to ---------------------------
    def _chapter_shots(self) -> list[tuple[str, float, float]]:
        """``(shot id, start, end)`` of the stored chapter shots this flat film was read from (empty: not a chapter film)."""
        from astrid.sdk.timeline_restructure import STRUCTURE_KEY, _rows

        stored = self.bundle.get(STRUCTURE_KEY)
        return [(str(r["shot_id"]), _row_start(r) / 1000.0, (_row_start(r) + _num(r.get("duration_ms"))) / 1000.0)
                for r in (_rows(stored) if stored else [])]

    def _narration_shot(self, line: Voice) -> str:
        """The shot a line's script belongs to: its chapter's shot in a chapter film, else the one shot."""
        chapters = self._chapter_shots()
        if not chapters:
            return line.clips[0].shot_id
        start = line.clips[0].start
        return next((sid for sid, a, _b in reversed(chapters) if a <= start + 1e-6), chapters[0][0])

    def _shot_payload(self, sid: str) -> dict[str, Any]:
        from astrid.sdk.timeline_restructure import STRUCTURE_KEY

        shots = self.bundle["shots"] if sid in self.bundle["shots"] else self.bundle[STRUCTURE_KEY]["shots"]
        return shots[sid].setdefault("payload", {})

    def narration(self) -> dict[str, str]:
        """``{shot_id: text}``: each shot's lines' script text, in order (what the shot's
        voiceover_script binding should hold). Only shots whose lines all declare their text."""
        by_shot: dict[str, list[Voice]] = {}
        for line in self.lines():
            by_shot.setdefault(self._narration_shot(line), []).append(line)
        out = {}
        for sid, lines in by_shot.items():
            if all(intent.line_text(v.clips[0].data) is not None for v in lines):
                out[sid] = " ".join(v.text for v in lines) + "\n"
        return out

    def narration_changes(self) -> dict[str, str]:
        """Shots whose narration differs from their bound voiceover_script (by content hash)."""
        import hashlib

        changed = {}
        for sid, text in self.narration().items():
            payload = self._shot_payload(sid)
            bound = next((b for b in payload.get("text_bindings") or [] if b.get("kind") == "voiceover_script"), None)
            digest = "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()
            if not bound or bound.get("content_hash") != digest:
                changed[sid] = text
        return changed

    def _matching_binding(self, client: Any, sid: str, text: str, bound: Mapping[str, Any] | None) -> dict[str, Any] | None:
        """The runtime's voiceover_script binding for ``sid`` iff its content hash is exactly ``text``'s (and it is the
        document's own binding when the document carries one); None otherwise, so the conflict is reported."""
        import hashlib

        from astrid.sdk.pagination import page_pair

        listed = client.shots.list_text_bindings(self.bundle["project_id"], shot_id=sid, kind="voiceover_script")
        page = page_pair(getattr(listed, "data", None)) if getattr(listed, "ok", False) else None
        if page is None or page[1] is not None:
            return None
        digest = "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()
        for row in page[0]:
            if (isinstance(row, Mapping) and row.get("shot_id") == sid and row.get("kind") == "voiceover_script"
                    and row.get("content_hash") == digest
                    and (not bound or not bound.get("binding_id") or row.get("binding_id") == bound.get("binding_id"))
                    and row.get("slot") == (bound or {}).get("slot")):
                return dict(row)
        return None

    def pin_narration(self, client: Any, *, idempotency_key: str) -> list[str]:
        """Register the changed narration per shot and pin it in the document (publish does this)."""
        pinned = []
        for sid, text in self.narration_changes().items():
            payload = self._shot_payload(sid)
            bound = next((b for b in payload.get("text_bindings") or [] if b.get("kind") == "voiceover_script"), None)
            expected = int((bound or {}).get("head") or 0)
            result = client.shots.set_text_binding(self.bundle["project_id"], shot_id=sid, kind="voiceover_script", text=text,
                                                    expected_head=expected,
                                                    idempotency_key=f"{idempotency_key}-narration-{sid}"[:120])
            err = getattr(result, "error", None)
            if getattr(result, "ok", True) is False and getattr(err, "code", None) == "conflict":
                # Adopt (never overwrite) a binding the document does not carry when the runtime already holds
                # exactly this text for this shot (an earlier pin whose document write was lost).
                adopted = self._matching_binding(client, sid, text, bound)
                if adopted is not None:
                    result = adopted
            pin = getattr(result, "data", result)
            if getattr(result, "ok", True) is False or not isinstance(pin, Mapping):
                raise TimelineEditError(f"could not register the narration for shot {sid}: {getattr(result, 'error', result)}")
            payload["text_bindings"] = [b for b in payload.get("text_bindings") or [] if b.get("kind") != "voiceover_script"] + [dict(pin)]
            (payload.get("metadata") or {}).pop("voiceover_script", None)
            pinned.append(sid)
        return pinned

    def document(self) -> dict[str, Any]:
        """The publishable candidate (derived `_` fields removed)."""
        doc = _strip_derived(copy.deepcopy(self.bundle))
        intent.migrate(doc)  # the candidate carries intent under app.astrid; unchanged shots reuse their old revisions and the merged candidate is published without a further migration (old revisions are never rewritten)
        return doc

    def stored_document(self, *, restructure: bool = False) -> dict[str, Any]:
        """The candidate as it is stored.

        Splitting into chapter shots is opt-in per film: only `timelines restructure`
        (``restructure=True``) or a film already stored as chapters (read back flat, so it
        carries its stored form) is split. Every other film is stored exactly as edited.
        """
        from astrid.sdk.timeline_restructure import STRUCTURE_KEY, split

        doc = self.document()
        return split(doc) if restructure or STRUCTURE_KEY in doc else doc

    def _annotated(self) -> dict[str, Any]:
        """The bundle plus derived, read-only helpers: an index and both clocks on every clip."""
        doc = _strip_derived(copy.deepcopy(self.bundle))
        intent.migrate(doc)
        index = {
            "note": EDITABLE_NOTE,
            "fps": self.fps,
            "duration_s": self.duration,
            "cuts": [{"n": c.n, "start": _r(c.start), "end": _r(c.end), "shot": c.shot,
                      "picture": c.picture.id if c.picture else None, "layers": [l.id for l in c.layers]} for c in self.cuts],
            "words": [[w.id, w.text, w.start, w.end] for w in self.words()],
        }
        for sid in self._shot_ids():
            start = self._shot_start(sid)
            for clip in doc["shots"][sid].get("internal_timeline", {}).get("clips", []):
                cs = start + _num(clip.get("at"))
                clip["_timeline"] = {"start": _r(cs), "end": _r(cs + clip_duration(clip))}
        return {"_index": index, **doc}

    def _absorb(self, raw: dict[str, Any]) -> dict[str, Any]:
        """Apply hand edits made in `_timeline` (timeline seconds), then drop every derived field."""
        bundle = raw
        rows = {str(r.get("shot_id")): r for r in bundle.get("placements") or []}
        for sid, shot in (bundle.get("shots") or {}).items():
            row = rows.get(sid)
            if row is None:
                continue
            start = _row_start(row) / 1000.0
            for clip in (shot.get("internal_timeline") or {}).get("clips", []):
                stamp = clip.get("_timeline")
                if not isinstance(stamp, Mapping):
                    continue
                cs = start + _num(clip.get("at"))
                ce = cs + clip_duration(clip)
                new_s, new_e = _num(stamp.get("start"), cs), _num(stamp.get("end"), ce)
                if abs(new_s - cs) > 1e-4 or abs(new_e - ce) > 1e-4:
                    if abs(new_s - cs) > 1e-4 and abs(new_e - ce) <= 1e-4:
                        new_e = new_s + (ce - cs)  # moved start only: keep the length
                    clip["at"] = _r(new_s - start)
                    _set_length(clip, new_e - new_s)
                    self.notes.append(f"{clip.get('id')}: applied your _timeline edit → at {clip['at']} (shot {sid})")
        bundle = _strip_derived(bundle)
        intent.migrate(bundle)  # checkout: legacy intent moves to app.astrid in the WORKING COPY (its pinned base copies are migrated too, so the move is not an edit)
        return bundle
