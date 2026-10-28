"""Runtime-backed Python editing with bounded function recomputation."""
from __future__ import annotations

import copy
import hashlib
import uuid
from collections.abc import Mapping
from typing import Any, cast

from ._common import PARENT_SHOT, TimelineEditError
from .checkout import Checkout
from .sync import CommitConflict, TimelineSession, _pin


def emit_document_commands(before, after):
    """G3 owns this lossless bundle-to-command emitter and its patch semantics."""
    try:
        from .emitter import emit_document_commands as emit
    except ModuleNotFoundError as exc:
        if exc.name != "astrid.sdk.timeline.emitter":
            raise
        raise TimelineEditError("free edits require the G3 document emitter; use command() until it is available") from exc
    return emit(before, after)


def _imports_in_commands(commands):
    """Disclose catalog media referenced by a reviewed fixed command list."""
    imports, seen = [], set()

    def visit(value):
        if isinstance(value, Mapping):
            if all(isinstance(value.get(key), str) and value[key]
                   for key in ("object_id", "generation_id", "variant_id")):
                identity = tuple(value[key] for key in ("object_id", "generation_id", "variant_id"))
                if identity not in seen:
                    seen.add(identity)
                    imports.append({"object_id": identity[0], "generation_id": identity[1],
                                    "variant_id": identity[2], "catalog_write": True,
                                    "retained_on_undo": True})
            for child in value.values():
                visit(child)
        elif isinstance(value, list):
            for child in value:
                visit(child)

    visit(commands)
    return imports


def _clip_interval(clip):
    """Return a clip's timeline interval in seconds when its timing is known."""
    start = clip.get("at", clip.get("start"))
    if not isinstance(start, (int, float)) or isinstance(start, bool):
        return None
    if isinstance(clip.get("hold"), (int, float)) and not isinstance(clip.get("hold"), bool):
        end = start + clip["hold"]
    elif all(isinstance(clip.get(key), (int, float)) and not isinstance(clip.get(key), bool)
             for key in ("from", "to")):
        end = start + clip["to"] - clip["from"]
    else:
        return None
    return (float(start), float(end)) if end > start else None


def _effect_intervals(clip, interval, fps):
    """Get the temporal windows represented by common clip effect fields."""
    start, end = interval
    windows = []

    def duration(value):
        if not isinstance(value, Mapping):
            return None
        frames = value.get("durationFrames")
        seconds = value.get("duration")
        result = (frames / fps if isinstance(frames, (int, float)) and not isinstance(frames, bool)
                  else seconds if isinstance(seconds, (int, float)) and not isinstance(seconds, bool)
                  else None)
        return min(end - start, float(result)) if result and result > 0 else None

    for key in ("entrance", "exit", "transition"):
        effect = clip.get(key)
        length = duration(effect)
        if length is not None:
            windows.append((start, start + length) if key == "entrance" else (end - length, end))
    for key in ("effects", "animations"):
        entries = clip.get(key)
        if isinstance(entries, list):
            for effect in entries:
                if not isinstance(effect, Mapping):
                    continue
                length = duration(effect)
                offset_frames = effect.get("startFrame")
                offset = (offset_frames / fps if isinstance(offset_frames, (int, float))
                          and not isinstance(offset_frames, bool) else effect.get("start", 0))
                if length is not None and isinstance(offset, (int, float)) and not isinstance(offset, bool):
                    lo = max(start, start + offset)
                    hi = min(end, lo + length)
                    if hi > lo:
                        windows.append((lo, hi))
    return windows


def _changed_ranges(before, after):
    """Describe changed timeline time from exact accepted before/after bundles."""
    from ._command_state import equal

    def clips(bundle):
        parent = bundle.get("parent") if isinstance(bundle, Mapping) else None
        rows = parent.get("clips", []) if isinstance(parent, Mapping) else []
        return {str(row.get("id")): row for row in rows
                if isinstance(row, Mapping) and row.get("id") is not None}

    old, new = clips(before), clips(after)
    old_fps = before.get("parent", {}).get("config", {}).get("output", {}).get("fps", 30)
    new_fps = after.get("parent", {}).get("config", {}).get("output", {}).get("fps", 30)
    fps = float(old_fps) if isinstance(old_fps, (int, float)) and old_fps > 0 else 30.0
    if isinstance(new_fps, (int, float)) and new_fps > 0:
        fps = max(fps, float(new_fps))
    spans = []
    changed = set(old) | set(new)
    changed = {identity for identity in changed if not equal(old.get(identity), new.get(identity))}
    for identity in changed:
        for snapshot, peers in ((old, new), (new, old)):
            clip = snapshot.get(identity)
            if clip is None:
                continue
            interval = _clip_interval(clip)
            if interval is None:
                continue
            old_clip = old.get(identity, {})
            new_clip = new.get(identity, {})
            effect_keys = {"entrance", "exit", "transition", "effects", "animations"}
            effect_only = (old_clip.keys() | new_clip.keys()) and all(
                key in effect_keys or equal(old_clip.get(key), new_clip.get(key))
                for key in old_clip.keys() | new_clip.keys())
            if effect_only:
                before_effects = len(spans)
                for key in effect_keys:
                    if not equal(old_clip.get(key), new_clip.get(key)):
                        spans.extend(_effect_intervals(clip, interval, fps))
                if len(spans) == before_effects:
                    spans.append(interval)
            else:
                spans.append(interval)
            # A transition can affect the adjacent same-track clip as well.
            if any(not equal(old_clip.get(key), new_clip.get(key))
                   for key in ("exit", "transition", "effects", "animations")):
                affected = _effect_intervals(clip, interval, fps) or [interval]
                for neighbor in peers.values():
                    neighbor_interval = _clip_interval(neighbor)
                    if (neighbor_interval is not None and neighbor.get("track") == clip.get("track")
                            and neighbor.get("id") != identity):
                        for effect_start, effect_end in affected:
                            lo = max(effect_start, neighbor_interval[0])
                            hi = min(effect_end, neighbor_interval[1])
                            if hi > lo:
                                spans.append((lo, hi))
    def placements(bundle):
        rows = bundle.get("placements", []) if isinstance(bundle, Mapping) else []
        return {str(row.get("occurrence_id")): row for row in rows
                if isinstance(row, Mapping) and row.get("occurrence_id") is not None}

    old_placements, new_placements = placements(before), placements(after)
    for identity in old_placements.keys() | new_placements.keys():
        old_row, new_row = old_placements.get(identity), new_placements.get(identity)
        if equal(old_row, new_row):
            continue
        for row in (old_row, new_row):
            if row is None:
                continue
            placement = row.get("placement")
            start_ms = placement.get("start_ms") if isinstance(placement, Mapping) else None
            duration_ms = row.get("duration_ms")
            if (isinstance(start_ms, (int, float)) and not isinstance(start_ms, bool)
                    and isinstance(duration_ms, (int, float)) and not isinstance(duration_ms, bool)
                    and duration_ms > 0):
                spans.append((float(start_ms) / 1000, (float(start_ms) + float(duration_ms)) / 1000))
    merged = []
    for start, end in sorted((lo, hi) for lo, hi in spans if hi > lo):
        if merged and start <= merged[-1]["end"]:
            merged[-1]["end"] = max(merged[-1]["end"], end)
        else:
            merged.append({"start": start, "end": end})
    return merged


class Timeline(Checkout):
    """A local edit session whose only publication boundary is ``commit``.

    ``command`` stages registered semantic commands and their local preview.
    Checkout helpers/free bundle edits are captured by G3's document emitter.
    A commit function receives a fresh Timeline at each conflict head. It must
    keep external side effects out of its body because it can run three times.
    """

    def __init__(self, session, bundle, base, *, evaluating=False, media_cache=None,
                 identity_cache=None):
        # Initialize helper state without migrating/flattening the pinned bundle.
        super().__init__({})
        self.session = session
        self._basis = copy.deepcopy(base)
        self._evaluating = evaluating
        self._media_cache = copy.deepcopy(media_cache or {})
        self._identity_cache = copy.deepcopy(identity_cache or {})
        self._identity_ordinal = 0
        self._verified_media = []
        self._adopt(bundle)

    @classmethod
    def open(cls, project=None, timeline=None, *, client=None, outbox_path=None):
        return open(project, timeline, client=client, outbox_path=outbox_path)

    def _adopt(self, bundle):
        self.bundle = copy.deepcopy(bundle)
        self._base_bundle = copy.deepcopy(bundle)
        self._runtime_document = self.bundle.get("source_mapping", {}).pop("_runtime_document", None)
        self._command_bundle = copy.deepcopy(self.bundle)
        self._commands: list[dict[str, Any]] = []
        self._steps: list[dict[str, Any]] = []
        self._free_edits = False
        self._journal.clear()
        self._refresh()

    def add(self, source, *, at, hold=None, duration=None, track=None, id=None, clip_id=None, **options):
        """Stage media, retaining its exact content selection across reruns."""
        identity_ordinal = self._identity_ordinal
        if self._evaluating:
            self._identity_ordinal += 1
        from pathlib import Path

        local_path = Path(source).expanduser() if isinstance(source, (str, Path)) else None
        source_path = str(local_path.absolute()) if local_path is not None else None
        cached = next((entry for entry in (self._media_cache.values() if self._evaluating else ())
                       if source_path is not None and source_path in entry.get("sources", ())), None)
        native_media = (self._evaluating and
                        (isinstance(source, (Mapping, Path)) or cached is not None
                         or bool(local_path and local_path.is_file())
                         or bool(local_path and not options
                                 and (local_path.suffix or len(local_path.parts) > 1))
                         or duration is not None or id is not None))
        if not native_media:
            if duration is not None:
                options["duration"] = duration
            if id is not None:
                options["id"] = id
            if clip_id is not None:
                options["clip_id"] = clip_id
            return super().add(source, at=at, hold=hold, track=track, **options)
        if options:
            raise TimelineEditError("flat media add accepts only at, hold, track and id options")

        from astrid.sdk.timeline_media_replacement import _verified

        from .capture import number
        from .media_add import _placement_commands, _selection, existing_selectors
        from .model import Clip

        if id is not None and clip_id is not None:
            raise TimelineEditError("use only one of id or clip_id")
        clip_id = id if id is not None else clip_id
        if clip_id is not None and (not isinstance(clip_id, str) or not clip_id.strip()):
            raise TimelineEditError("media clip id must be a nonempty string")
        if clip_id is None and self._evaluating:
            slot = str(identity_ordinal)
            clip_id = self._identity_cache.setdefault(slot, "clip-" + uuid.uuid4().hex)
        on = number(at, "at")
        if on < 0:
            raise TimelineEditError("at must not be negative")
        if track is not None and (not isinstance(track, str) or not track.strip()):
            raise TimelineEditError("media track must be a nonempty track ID")
        if duration is not None and hold is not None:
            raise TimelineEditError("use only one of hold or duration")
        requested_duration = duration if duration is not None else hold
        if requested_duration is not None:
            requested_duration = number(requested_duration, "hold", positive=True)
        cache_key = cached["pin"]["object_id"] if cached is not None else None
        if cached is None and local_path is not None and local_path.is_file():
            from astrid.core.media import MediaProbeError
            from astrid.sdk.authoring_media import _metadata

            try:
                metadata = _metadata(local_path)
                payload = local_path.read_bytes()
            except (MediaProbeError, OSError, ValueError) as exc:
                raise TimelineEditError(f"invalid local media {str(local_path)!r}: {exc}; "
                                        "use a readable image, video, or audio file") from exc
            cache_key = metadata["digest"]
            if "sha256:" + hashlib.sha256(payload).hexdigest() != cache_key:
                raise TimelineEditError("local media changed during import; retry after the file is saved")
            cached = self._media_cache.get(cache_key)
        reused = None
        if cached is None and cache_key is not None:
            # Reuse media this project already imported (keyed by project + digest).
            transport = self.session.client._remote._transport
            reused = existing_selectors(transport, self.session.project_id, cache_key)
        if reused is not None:
            from astrid.sdk.timeline_media_replacement import _plain

            pin = _plain(self.session.client._remote._transport.get_project_media_selection(
                self.session.project_id, reused))
            pin, verified = _verified(self.session.client._remote._transport, self.session.project_id, pin)
        elif cached is None:
            pin, verified = _selection(self.session, self.bundle, source)
        else:
            pin = copy.deepcopy(cached["pin"])
            pin, verified = _verified(self.session.client._remote._transport, self.session.project_id, pin)
        if cache_key is not None and pin.get("object_id") != cache_key:
            raise TimelineEditError("local media changed during import; retry after the file is saved")
        kind = verified.get("media_type", "").split("/", 1)[0]
        if kind not in {"image", "video", "audio"}:
            raise TimelineEditError("verified media must be an image, video, or audio file")
        asset_alias = None
        if self._evaluating:
            identity = "\0".join(pin[key] for key in ("object_id", "generation_id", "variant_id"))
            identity_key = "asset:" + hashlib.sha256(identity.encode("utf-8")).hexdigest()
            asset_alias = self._identity_cache.setdefault(identity_key, "media-" + uuid.uuid4().hex)
        length = requested_duration if requested_duration is not None else number(
            verified.get("duration_seconds") or 1.0, "hold", positive=True)

        self._capture_free_edits()
        commands = _placement_commands(self.bundle, pin, verified, on=on, duration=length,
                                       track=track, clip_id=clip_id, asset_alias=asset_alias)
        from .commands import execute

        capture_bundle = (self._execution_bundle(self._command_bundle)
                          if self._runtime_document is not None else self._command_bundle)
        commands = execute(capture_bundle, commands,
                           verified_media=[*self._verified_media, copy.deepcopy(verified)]).commands
        self._verified_media.append(copy.deepcopy(verified))
        try:
            self._append(commands, label="Add media")
        except Exception:
            self._verified_media.pop()
            raise
        if cache_key is not None:
            entry = self._media_cache.setdefault(cache_key, {
                "pin": copy.deepcopy(pin), "sources": [],
                "imports": [{"object_id": pin["object_id"], "generation_id": pin["generation_id"],
                             "variant_id": pin["variant_id"], "catalog_write": True,
                             "retained_on_undo": True}] if reused is None else [],
            })
            if source_path not in entry.setdefault("sources", []):
                entry["sources"].append(source_path)
        identity = commands[-1]["args"]["row"]["id"]
        added = next((candidate for candidate in self._parent_clips() if candidate.get("id") == identity), None)
        if added is None:
            raise TimelineEditError("media capture did not create the requested clip")
        return Clip(self, PARENT_SHOT, added)

    def _execution_bundle(self, bundle):
        """Supply private canonical input from this evaluation's exact base pair."""
        if self._runtime_document is None:
            from .store import fetch_bundle

            source = fetch_bundle(
                self.session.project_id, self.session.timeline_id,
                revision_id=self._basis["revision_id"], publication_id=self._basis["publication_id"],
                client=self.session.client,
            )
            self._runtime_document = source["source_mapping"]["_runtime_document"]
        result = copy.deepcopy(bundle)
        result["source_mapping"]["_runtime_document"] = copy.deepcopy(self._runtime_document)
        return result

    @property
    def head(self):
        return copy.deepcopy(self._basis)

    def undo(self, steps: int | dict[str, list[str]] | None = 1, *,
             publications: list[str] | None = None, client: Any = None, **options: Any):
        """Undo local draft steps or dispatch an accepted-publication inverse.

        ``Checkout.undo`` owns the detached numeric draft history.  A Runtime
        timeline instead sends publication inverses through its already-open
        session, including the v2 publication-to-step selector.
        """
        if publications is None:
            return super().undo(cast(int, steps), client=client, **options)
        if steps is not None and not isinstance(steps, dict) and steps != 1:
            raise TimelineEditError("publication undo cannot be combined with draft steps")
        return self.session.undo(publications, steps=None if steps == 1 else steps, **options)

    def _capture_free_edits(self):
        if self.bundle != self._command_bundle:
            before, after = copy.deepcopy(self._command_bundle), copy.deepcopy(self.bundle)
            if self._runtime_document is not None or before.get("shots") != after.get("shots"):
                before, after = self._execution_bundle(before), self._execution_bundle(after)
            commands = emit_document_commands(before, after)
            if not commands:
                raise TimelineEditError("document emitter omitted local edits")
            self._append(commands, label="Edit document")
            self._free_edits = True

    def _append(self, commands, *, label, intent="", tags=(), reads=None):
        from .commands import CommandError, execute

        try:
            bundle = (self._execution_bundle(self._command_bundle)
                      if self._runtime_document is not None or any(command.get("op") == "doc.patch" for command in commands)
                      else self._command_bundle)
            plan = execute(bundle, commands, verified_media=self._verified_media)
        except CommandError as exc:
            if exc.kind == "unsupported_operation" and any(command.get("op") == "doc.patch" for command in commands):
                raise TimelineEditError(
                    "free edits require the G3 document emitter and the R1 doc.patch provider"
                ) from exc
            raise
        start = len(self._commands)
        patch = [copy.deepcopy(change) for command in commands if command["op"] == "doc.patch"
                 for change in command["args"]["changes"]]
        step = {"id": f"step-{len(self._steps) + 1}", "label": label, "intent": intent,
                "tags": list(tags), "command_ordinals": list(range(start, start + len(plan.commands))),
                "patch": patch}
        if reads is not None:
            step["reads"] = copy.deepcopy(reads)
        # Preserve caller guards; preview-generated captures omit the final
        # request/step reads. The provider captures against the pinned base.
        self._commands.extend(copy.deepcopy(commands))
        self._steps.append(step)
        self.bundle = copy.deepcopy(plan.bundle)
        self._runtime_document = self.bundle.get("source_mapping", {}).pop("_runtime_document", self._runtime_document)
        self._command_bundle = copy.deepcopy(self.bundle)
        self._refresh()

    def command(self, command, *, label="Timeline edit", intent="", tags=(), reads=None):
        """Stage one command/step without sending or writing local history.

        ``reads`` here declares dependencies at this step's sequential input;
        ``commit(reads=...)`` declares dependencies at batch entry.
        """
        if not self._evaluating:
            with self.session.outbox.locked():
                state = self.session._state()
                if state["pending"] or state["flight"] is not None:
                    raise TimelineEditError("reconcile the original request before another edit")
                if state["base"] != self._basis:
                    raise TimelineEditError("session base changed; reopen before editing")
        self._capture_free_edits()
        self._append([copy.deepcopy(command)], label=label, intent=intent, tags=tags, reads=reads)
        return self

    def move(self, select, on):
        """Stage a native move; commit the whole session with one label."""
        return self.command({"schema_version": 1, "op": "clip.move", "version": "1",
                             "select": select, "args": {"on": on}}, label="Move clip")

    def _accepted(self, result):
        from .commit import bundle_from_document

        if result["data"]["status"] != "preview":
            data = result["data"]
            previous_revision = data.get("previous_revision_id")
            previous_publication = data.get("previous_publication_id")
            accepted_revision = data.get("accepted_revision_id")
            if all(isinstance(value, str) and value for value in
                   (previous_revision, previous_publication, accepted_revision)):
                from .store import fetch_bundle

                if previous_revision == self._basis.get("revision_id"):
                    before = self._base_bundle
                else:
                    before = fetch_bundle(self.session.project_id, self.session.timeline_id,
                                          revision_id=previous_revision,
                                          publication_id=previous_publication,
                                          client=self.session.client)
                after = bundle_from_document(data["canonical_document"])
                ranges = _changed_ranges(before, after)
                data["changed_ranges"] = ranges
                result["changed_ranges"] = copy.deepcopy(ranges)
            # Adopt the entire landed document, including the other writer's edits.
            bundle = bundle_from_document(data["canonical_document"])
            bundle["base_parent"]["publication_id"] = result["receipt"]["receipt_id"]
            self._adopt(bundle)
            self._basis = {"revision_id": data["accepted_revision_id"],
                           "publication_id": result["receipt"]["receipt_id"]}
        return result

    def commit(self, label_or_fn="Timeline edit", *, label=None, merge="fields", dry_run=False,
               reads=None, key=None, idempotency_key=None):
        """Accept staged edits, a fixed command list, or evaluate ``fn`` up to three times.

        Only an explicit conflict permits reevaluation. Calling again after a
        transport/unknown outcome retries the durable original body/key first,
        even after reopening. Refused/invalid results never rerun the function.
        A command list is submitted as captured and never recaptured. Omitted
        reads remain omitted; doc.patch then receives conservative atomic
        guarding from the provider. Preview never becomes this session's base.
        """
        if self._evaluating:
            raise TimelineEditError("a commit function cannot commit its own evaluation")
        if key is not None and idempotency_key is not None:
            raise TimelineEditError("pass only one of key or idempotency_key")
        if key is not None:
            idempotency_key = key
        if merge not in {"fields", "atomic"}:
            raise TimelineEditError("merge must be fields or atomic")
        if dry_run:
            idempotency_key = None
        function = label_or_fn if callable(label_or_fn) else None
        commands = label_or_fn if isinstance(label_or_fn, list) else None
        if function:
            commit_label = label or getattr(function, "__name__", "Timeline edit")
        elif commands is not None:
            commit_label = label or "Timeline edit"
        else:
            if label is not None and label_or_fn != "Timeline edit":
                raise TimelineEditError("pass the commit label either positionally or by keyword")
            commit_label = label or label_or_fn
        if not isinstance(commit_label, str) or not commit_label.strip():
            raise TimelineEditError("commit requires a nonempty label or a function")
        if commands is not None:
            return self._commit_commands(commands, label=commit_label, merge=merge, dry_run=dry_run,
                                         reads=reads, idempotency_key=idempotency_key)
        if function:
            replay = self.session.resolve_acknowledged(idempotency_key, dry_run=dry_run)
            if replay is not None:
                return replay
        with self.session.outbox.locked():
            state = self.session._state()
        rejected = state.get("rejected")
        rejected_failure = rejected.get("failure") if isinstance(rejected, Mapping) else None
        rejected_details = rejected_failure.get("details") if isinstance(rejected_failure, Mapping) else None
        if isinstance(rejected_details, Mapping) and rejected_details.get("status") == "conflict":
            rejected_eval = rejected.get("evaluation") if isinstance(rejected, Mapping) else None
            attempts = rejected_eval.get("count") if isinstance(rejected_eval, Mapping) and rejected_eval.get("kind") == "function" else None
            raise CommitConflict(rejected_failure, attempts=attempts, fixed_list=True,
                                 label=label_or_fn if isinstance(label_or_fn, str) else label,
                                 timeline_id=self.session.timeline_id,
                                 project_id=self.session.project_id)
        evaluation = state.get("evaluation") or {}
        count = evaluation.get("count", 0)
        if function and state["flight"] is not None and evaluation.get("kind") == "function":
            flight = state["flight"]
            logical_key = flight.get("logical_key", flight["key"] if flight.get("explicit_key") else None)
            if logical_key is not None:
                if idempotency_key is not None and idempotency_key != logical_key:
                    raise TimelineEditError("retry the original function idempotency key")
                idempotency_key = logical_key
        if state["pending"] or state["flight"] is not None:
            # A known conflict may be recomputed; every other outcome must first
            # reconcile the exact original request, without invoking user code.
            conflict = state.get("conflict")
            if not conflict or conflict.get("details", {}).get("status") != "conflict":
                if (self.bundle != self._command_bundle
                        or self._commands and self._commands != state["pending"]):
                    raise TimelineEditError("local edits differ from the original request; reopen to reconcile it")
                try:
                    result = self.session.flush(idempotency_key=idempotency_key, dry_run=dry_run,
                                                release_conflict=not function)
                except CommitConflict as exc:
                    conflict = exc.failure
                    with self.session.outbox.locked():
                        state = self.session._state()
                        evaluation = state.get("evaluation") or evaluation
                else:
                    return self._accepted(result)
            if conflict.get("details", {}).get("status") != "conflict":
                raise CommitConflict(conflict)
            if not function or evaluation.get("kind") != "function" or count >= 3:
                raise CommitConflict(conflict, attempts=count if function and count >= 3 else None,
                                     label=commit_label, timeline_id=self.session.timeline_id,
                                     project_id=self.session.project_id)
            base = _pin(conflict["details"]["current"])
        else:
            if not function and state["base"] != self._basis:
                raise TimelineEditError("session base changed; reopen before committing")
            base = state["base"]
            count = 0

        while True:
            if function:
                if self._commands or self.bundle != self._command_bundle:
                    raise TimelineEditError("commit(fn) requires a clean local session")
                from .store import fetch_bundle

                bundle = fetch_bundle(self.session.project_id, self.session.timeline_id,
                                      revision_id=base["revision_id"], publication_id=base["publication_id"],
                                      client=self.session.client)
                saved_cache = evaluation.get("media_cache", {})
                saved_identities = evaluation.get("identity_cache", {})
                working = Timeline(self.session, bundle, base, evaluating=True,
                                   media_cache=saved_cache, identity_cache=saved_identities)
                function(working)
                count += 1
            else:
                working = self
            working._capture_free_edits()
            if not working._commands:
                raise TimelineEditError("no pending timeline edits")
            steps = copy.deepcopy(working._steps)
            effective_merge = merge
            if reads is None and (function or working._free_edits
                                  or any(command["op"] == "doc.patch" for command in working._commands)):
                effective_merge = "atomic"
                # Arbitrary Python may consult any part of the loaded closure.
                # Keep omitted batch reads distinct from an empty declaration,
                # and retain this conservative dependency at each step boundary.
                for step in steps:
                    step.setdefault("reads", []).append({"kind": "scope", "ref": "timeline", "path": []})
            try:
                result = self.session.submit(
                    working._commands, label=commit_label, steps=steps, merge=effective_merge, reads=reads,
                    idempotency_key=idempotency_key, dry_run=dry_run, expected_state=state, base=base,
                    evaluation={"kind": "function" if function else "label", "count": count,
                                "media_cache": copy.deepcopy(working._media_cache),
                                "identity_cache": copy.deepcopy(working._identity_cache)},
                )
            except CommitConflict as exc:
                if not function or exc.failure["details"].get("status") != "conflict" or count >= 3:
                    if function and count >= 3:
                        raise CommitConflict(exc.failure, attempts=count, label=commit_label,
                                             timeline_id=self.session.timeline_id,
                                             project_id=self.session.project_id) from exc
                    raise
                base = _pin(exc.failure["details"]["current"])
                with self.session.outbox.locked():
                    state = self.session._state()
                    evaluation = state.get("evaluation") or evaluation
                continue
            if dry_run:
                self._add_preview_diff(result, working.bundle)
            if function and count > 1:
                result["attempts"] = count
                result["data"]["attempts"] = count
                summary = result.get("summary", "")
                summary_base, separator, media = summary.partition(" Media:")
                result["summary"] = summary_base.rstrip(".") + f" after re-reading the timeline ({count} attempts)."
                if separator:
                    result["summary"] += " Media:" + media
                result["data"]["summary"] = result["summary"]
            return self._accepted(result)

    def _commit_commands(self, commands, *, label, merge, dry_run, reads, idempotency_key):
        """Submit an already captured list without rebuilding its guards or media pins."""
        if not commands:
            raise TimelineEditError("commit requires a nonempty command list")
        if self._commands or self.bundle != self._command_bundle:
            raise TimelineEditError("commit(command_list) requires a clean local session")
        with self.session.outbox.locked():
            state = self.session._state()
        if state["base"] != self._basis:
            raise TimelineEditError("session base changed; reopen before committing")
        steps = []
        for ordinal, command in enumerate(commands):
            patch = (copy.deepcopy(command.get("args", {}).get("changes", []))
                     if isinstance(command, Mapping) and command.get("op") == "doc.patch" else [])
            steps.append({"id": f"step-{ordinal + 1}", "label": label, "intent": "", "tags": [],
                          "command_ordinals": [ordinal], "patch": patch})
        try:
            result = self.session.submit(commands, label=label, steps=steps, merge=merge, reads=reads,
                                         idempotency_key=idempotency_key, dry_run=dry_run,
                                         expected_state=state, base=state["base"])
        except CommitConflict as exc:
            if exc.failure.get("details", {}).get("status") == "conflict":
                raise CommitConflict(exc.failure, label=label, fixed_list=True,
                                     timeline_id=self.session.timeline_id,
                                     project_id=self.session.project_id) from exc
            raise
        if not result.get("imports"):
            imports = _imports_in_commands(commands)
            if imports:
                result["imports"] = imports
                result["data"]["imports"] = copy.deepcopy(imports)
                summary = result.get("summary", "")
                result["summary"] = summary + f" Media: {len(imports)} file(s) in the catalog; undo keeps them."
                result["data"]["summary"] = result["summary"]
        if dry_run:
            self._add_preview_diff(result, self.bundle)
        return self._accepted(result)

    @staticmethod
    def _add_preview_diff(result, before_bundle):
        """Pair Runtime's preview commands with a diff of authored document fields."""
        from .commit import bundle_from_document
        from .emitter import _diff, _payload_for_emit, _root_pairs

        data = result.get("data", {})
        document = data.get("canonical_document")
        if isinstance(document, Mapping):
            after_bundle = bundle_from_document(document)
            changes = []
            for ref, before, after in _root_pairs(before_bundle, after_bundle):
                _diff(_payload_for_emit(ref, before), _payload_for_emit(ref, after), ref, (), changes)
            if not changes:
                changes = [{"op": command["op"], "ref": command.get("select"),
                            "args": copy.deepcopy(command["args"])}
                           for command in data.get("commands", [])]
            data.setdefault("diff", {"changes": changes})

    def save(self, *args, **kwargs):
        raise TimelineEditError("use commit(label) to save a Runtime timeline")

    def publish(self, *args, **kwargs):
        raise TimelineEditError("use commit(label) to publish a Runtime timeline")

    def duplicate(self, *, as_):
        """Create a named copy of this timeline, returning setup and copy results separately."""
        from astrid.sdk.timeline_duplicate import _duplicate_key, duplicate_timeline

        if not isinstance(as_, str) or not as_.strip():
            raise TimelineEditError("duplicate requires a nonempty destination name")
        return duplicate_timeline(
            self.session.project_id,
            self.session.timeline_id,
            slug=as_,
            client=self.session.client,
            idempotency_key=_duplicate_key(self.session.project_id, self.session.timeline_id, as_),
        )


def open(project=None, timeline=None, *, client=None, outbox_path=None):
    """Open a Runtime head, retaining any durable request awaiting reconciliation.

    With no explicit client, use the configured launcher connection. With no
    project/timeline, use Runtime's current project and normal timeline resolver.
    The optional outbox path isolates independent sessions in the same scope.
    """
    from astrid.sdk import AstridClient

    from .store import fetch_bundle

    client = client if client is not None else AstridClient.open_from_launcher(start_pack_host=False)
    session = TimelineSession.open(project, timeline, client=client, outbox_path=outbox_path)
    with session.outbox.locked():
        base = session._state()["base"]
    bundle = fetch_bundle(session.project_id, session.timeline_id,
                          revision_id=base["revision_id"], publication_id=base["publication_id"], client=client)
    return Timeline(session, bundle, base)
