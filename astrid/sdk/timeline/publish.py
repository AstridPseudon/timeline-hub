"""Checkout: publish, narration binding, and the document as it is saved (annotated) and read back (absorb)."""
from __future__ import annotations

import copy
import re
import sys
import uuid
from pathlib import Path
from typing import Any, Mapping

from astrid.sdk import timeline_intent as intent
from astrid.core.timeline.cuts import (
    clip_duration,
)

from astrid.sdk.timeline import journal as _journal
from astrid.sdk.timeline import store as _store
from astrid.sdk.timeline._common import (EDITABLE_NOTE, TimelineEditError, _num, _r)
from astrid.sdk.timeline.doc import (_row_start, _set_length, _strip_derived)
from astrid.sdk.timeline.model import Voice
from astrid.sdk import timeline_transcripts as _transcripts  # module access: its functions resolve at call time


def _native_move_command(checkout: Any) -> dict[str, Any] | None:
    """Recognise only the detached checkout edit that already has native meaning.

    Main's ``Clip.set`` also accepts element parameters and clip-look fields, so
    publishing from a generic property diff cannot safely be guessed as a native
    timing operation.  A single unannotated numeric position change is the
    existing ``clip.move`` contract; everything else stays on the detached
    publication path.
    """
    from astrid.sdk.timeline._command_state import State
    from astrid.sdk.timeline.capture import capture_move, occurrence_start
    from astrid.sdk.timeline.commands import execute
    from astrid.sdk.timeline_cuts import base_bundle

    candidate = checkout.document()
    pinned = base_bundle(candidate)
    # Keep the fetched closure's authoring/source mapping intact.  The diff
    # view is intentionally flatter than the command state's occurrence
    # ownership model, so using it as the whole command base loses that proof.
    base = copy.deepcopy(candidate)
    base["parent"] = copy.deepcopy(pinned["parent"])
    base["placements"] = copy.deepcopy(pinned["placements"])
    for shot in base.get("shots", {}).values():
        if isinstance(shot, Mapping) and isinstance(shot.get("base_payload"), Mapping):
            shot["payload"] = copy.deepcopy(shot["base_payload"])
        if isinstance(shot, Mapping) and isinstance(shot.get("base_internal_timeline"), Mapping):
            shot["internal_timeline"] = copy.deepcopy(shot["base_internal_timeline"])
    # Core validation materializes an empty intent namespace while resolving a
    # checkout.  It is not an authored edit, so give the command base the same
    # empty derived unit without accepting any non-empty property change.
    candidate_units = _store._units(candidate)
    if candidate_units.get(("parent-config", "slots")) == {}:
        config = base.setdefault("parent", {}).setdefault("config", {})
        app = config.setdefault("app", {})
        app.setdefault("astrid", {})["slots"] = {}
    before, after = _store._units(base), _store._units(candidate)
    changed = [key for key in set(before) | set(after) if before.get(key) != after.get(key)]
    if len(changed) != 1 or changed[0][0] != "clip":
        return None
    key = changed[0]
    old, new = before[key], after[key]
    if not isinstance(old, Mapping) or not isinstance(new, Mapping):
        return None
    if set(old) - {"at"} != set(new) - {"at"}:
        return None
    if any(not isinstance(value, (int, float)) or isinstance(value, bool)
           for value in (old.get("at"), new.get("at"))):
        return None
    # An annotated/anchored clip has additional Main meaning that clip.move
    # deliberately does not infer.  Keep it as a visible detached draft.
    if old.get("app"):
        return None
    shot_id, clip_id = key[1:]
    placement = next((row for row in candidate.get("placements") or []
                      if str(row.get("shot_id")) == shot_id), None)
    if not isinstance(placement, Mapping) or not placement.get("occurrence_id"):
        return None
    ref = f"occurrence:{placement['occurrence_id']}/clip:{clip_id}"
    try:
        on = float(new["at"]) + occurrence_start(placement)
        command = capture_move(base, ref, on)
        planned = execute(base, [command]).bundle
    except (KeyError, TypeError, ValueError, TimelineEditError):
        return None
    planned_units = _store._units(planned)
    if any(planned_units.get(unit) != value for unit, value in after.items() if unit != key):
        return None
    # clip.move records the equivalent fixed timing rationale in app.astrid;
    # compare authored content excluding that native timing annotation.
    planned_clip = planned_units.get(key)
    if not isinstance(planned_clip, Mapping):
        return None
    without_app = lambda row: {k: v for k, v in row.items() if k != "app"}
    if without_app(planned_clip) != without_app(new):
        return None
    try:
        if State(base).entity(ref).get("app"):
            return None
    except (KeyError, TypeError, ValueError, TimelineEditError):
        return None
    return command


class _PublishMixin:
    """Checkout: publish, narration binding, and the document as it is saved (annotated) and read back (absorb)."""

    def publish(self, message: str = "", *, idempotency_key: str | None = None, client: Any = None,
                force: bool = False, restructure: bool = False) -> dict[str, Any]:
        """Check, then publish one revision.

        If someone published since this checkout, the edit is merged onto their head clip by
        clip (three-way: your base, their head, your candidate). Changes to different clips
        merge; a clip both sides changed refuses with a conflict list. ``force=True``
        overwrites their change, explicitly. Nothing is ever overwritten silently.
        """
        self.notes.extend(self._sync_film_length())  # the film's length follows its content, before the check
        report = self._check_core()
        if not report.valid:
            raise TimelineEditError("not publishing: " + "; ".join(report.problems or ["the candidate is invalid"]))
        key = idempotency_key or f"edit-{re.sub(r'[^a-z0-9]+', '-', message.lower())[:40].strip('-') or 'timeline'}-{uuid.uuid4().hex[:8]}"
        if client is not None and not force and not restructure:
            native = self._publish_native_move(message, key, client=client)
            if native is not None:
                return native
        stored = self.stored_document(restructure=restructure)  # chapters as shots only for a film that opted in
        chapter_film = len(stored.get("placements") or []) > 1
        if restructure or self.edits().get("changes") or not (chapter_film or self.narration_changes()):
            receipt = _store.publish_bundle(stored, key, client=client, force=force)
        else:  # only the narration binding is behind (a retry after it failed): pin it, nothing else to publish
            receipt = {"old_head": self.base_revision, "new_head": self.base_revision, "structure": "unchanged"}
        # Acceptance consumes the local steps before any follow-up read or
        # narration work can fail. This also fences a reload of a stale draft.
        self._retire_draft_history()
        receipt["narration_pinned"] = []
        if chapter_film or self.narration_changes():
            # A line's text changed (or the shots are new): bind each such shot's narration now that
            # the shots exist, then publish the pins as a second, small revision.
            try:
                receipt.update(self._publish_narration(key, client=client))
            except TimelineEditError as exc:  # the structure IS published: say so, and how to finish
                receipt["narration_error"] = (f"{exc}. The cut is published (head {receipt.get('new_head')}); only the "
                                              "narration binding is behind: timelines checkout TL --fresh, then "
                                              "timelines publish TL -m \"narration\" pins it")
        # Media is ingested by _register_asset before this point; its registry
        # entry now carries the stable object id. One document covers each take.
        receipt["transcripts"] = []
        project_id = str(stored["project_id"])  # the published document names its project
        try:
            transcript_plan = _transcripts.plan_narration_transcripts(self)
            if any(item["status"] == "planned" for item in transcript_plan):
                if client is None:
                    from astrid.sdk import AstridClient

                    with AstridClient.open_from_launcher(start_pack_host=False) as transcript_client:
                        receipt["transcripts"] = _transcripts.sync_narration_transcripts(self, transcript_client, project_id)
                else:
                    receipt["transcripts"] = _transcripts.sync_narration_transcripts(self, client, project_id)
        except Exception as exc:  # noqa: BLE001 - containment: publication already succeeded
            print(f"note: narration transcript registration failed: {exc}", file=sys.stderr)
        for item in receipt["transcripts"]:
            if item["status"] == "skipped":
                print(f"note: narration transcript {item['label']}: {item.get('reason', 'skipped')}", file=sys.stderr)
        if self.path:  # publish resets the base: this working copy is the new head, with no changes (AUDIT bug 6)
            before = _journal.document_digest(self.document())
            self._reset_base(client=client)
            _journal.record_or_note(self, Path(self.path), kind="publish", outcome="changed", label="publish",
                                    reason=message or None, before=before,
                                    after=_journal.document_digest(self.document()),
                                    evidence=({"kind": "revision", "id": receipt.get("new_head")},))
        receipt["message"] = message
        return receipt

    def _publish_native_move(self, message: str, key: str, *, client: Any) -> dict[str, Any] | None:
        """Commit one already-supported detached move through the durable outbox."""
        from astrid.sdk.timeline.sync import TimelineSession

        command = _native_move_command(self)
        if command is None:
            return None
        try:
            session = TimelineSession.open(self.bundle["project_id"], self.bundle["timeline_id"], client=client)
        except (KeyError, TypeError, ValueError, TimelineEditError):
            return None
        with session.outbox.locked():
            state = session._state()
            if state["base"]["revision_id"] != self.base_revision:
                return None
            if message and state.get("rationale") is None:
                state["rationale"] = message
                session.outbox.write(state)
        result = session.commit(command, idempotency_key=key, via="python")

        data, accepted = result["data"], result["receipt"]
        before = _journal.document_digest(self.document())
        self._retire_draft_history()
        self._reset_base(client=client, revision_id=data["accepted_revision_id"])
        if self.path:
            _journal.record_or_note(self, Path(self.path), kind="publish", outcome="changed", label="publish",
                                    reason=message or None, before=before,
                                    after=_journal.document_digest(self.document()),
                                    evidence=({"kind": "revision", "id": data["accepted_revision_id"]},))
        return {"old_head": data["previous_revision_id"], "new_head": data["accepted_revision_id"],
                "structure": "changed", "receipt": accepted, "idempotency_key": result["idempotency_key"],
                "narration_pinned": [], "transcripts": [], "message": message}

    def _reset_base(self, *, client: Any = None, revision_id: str | None = None) -> None:
        """Re-read the new head as this working copy's bundle and save it with no undo step. Never fails the publish."""
        self._retire_draft_history()
        try:
            head = _store.fetch_bundle(str(self.bundle["project_id"]), str(self.bundle["timeline_id"]),
                                       revision_id=revision_id, client=client)
        except Exception as exc:  # noqa: BLE001 - the publish stands; the working copy keeps its old base
            self.notes.append(f"published, but this working copy could not re-read the new head ({exc}); "
                              "its base is still the old one: timelines checkout TL --fresh")
            return
        from astrid.sdk.timeline_restructure import flatten

        head = flatten(head)
        old, old_disk = self.bundle, self._disk
        self.bundle, self._mcache, self._journal, self._disk = head, None, [], None
        try:
            target = Path(self.path)
            with _store._file_lock(target):
                self._save_locked(target, force=True, record=False)
        except Exception as exc:  # noqa: BLE001
            self.bundle, self._disk = old, old_disk
            self.notes.append(f"published, but this working copy could not be reset to the new head ({exc}); "
                              "its base is still the old one")

    def _publish_narration(self, key: str, *, client: Any = None) -> dict[str, Any]:
        def run(c: Any) -> dict[str, Any]:
            from astrid.sdk.timeline.checkout import Checkout
            head = Checkout(_store.fetch_bundle(str(self.bundle["project_id"]), str(self.bundle["timeline_id"]), client=c))
            pinned = head.pin_narration(c, idempotency_key=key)
            if not pinned:
                return {"narration_pinned": []}
            second = _store.publish_bundle(head.stored_document(), f"{key}-narration", client=c)
            return {"narration_pinned": pinned, "new_head": second.get("new_head"), "narration_head": second.get("new_head")}

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
