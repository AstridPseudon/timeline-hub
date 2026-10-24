"""Runtime-backed Python editing with bounded function recomputation."""
from __future__ import annotations

import copy
from typing import Any, cast

from ._common import TimelineEditError
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


class Timeline(Checkout):
    """A local edit session whose only publication boundary is ``commit``.

    ``command`` stages registered semantic commands and their local preview.
    Checkout helpers/free bundle edits are captured by G3's document emitter.
    A commit function receives a fresh Timeline at each conflict head. It must
    keep external side effects out of its body because it can run three times.
    """

    def __init__(self, session, bundle, base, *, evaluating=False):
        # Initialize helper state without migrating/flattening the pinned bundle.
        super().__init__({})
        self.session = session
        self._basis = copy.deepcopy(base)
        self._evaluating = evaluating
        self._adopt(bundle)

    @classmethod
    def open(cls, project=None, timeline=None, *, client=None, outbox_path=None):
        return open(project, timeline, client=client, outbox_path=outbox_path)

    def _adopt(self, bundle):
        self.bundle = copy.deepcopy(bundle)
        self._runtime_document = self.bundle.get("source_mapping", {}).pop("_runtime_document", None)
        self._command_bundle = copy.deepcopy(self.bundle)
        self._commands: list[dict[str, Any]] = []
        self._steps: list[dict[str, Any]] = []
        self._free_edits = False
        self._journal.clear()
        self._refresh()

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
            plan = execute(bundle, commands)
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
            # Adopt the entire landed document, including the other writer's edits.
            bundle = bundle_from_document(result["data"]["canonical_document"])
            bundle["base_parent"]["publication_id"] = result["receipt"]["receipt_id"]
            self._adopt(bundle)
            self._basis = {"revision_id": result["data"]["accepted_revision_id"],
                           "publication_id": result["receipt"]["receipt_id"]}
        return result

    def commit(self, label_or_fn="Timeline edit", *, merge="fields", dry_run=False,
               reads=None, idempotency_key=None):
        """Accept all edits, or evaluate ``fn(timeline)`` at most three times.

        Only an explicit conflict permits reevaluation. Calling again after a
        transport/unknown outcome retries the durable original body/key first,
        even after reopening. Refused/invalid results never rerun the function.
        Omitted reads remain omitted; doc.patch then receives conservative atomic
        guarding from the provider. Preview never becomes this session's base.
        """
        if self._evaluating:
            raise TimelineEditError("a commit function cannot commit its own evaluation")
        if merge not in {"fields", "atomic"}:
            raise TimelineEditError("merge must be fields or atomic")
        function = label_or_fn if callable(label_or_fn) else None
        label = (getattr(function, "__name__", "Timeline edit") if function else label_or_fn)
        if not isinstance(label, str) or not label.strip():
            raise TimelineEditError("commit requires a nonempty label or a function")
        with self.session.outbox.locked():
            state = self.session._state()
        evaluation = state.get("evaluation") or {}
        count = evaluation.get("count", 0)
        if state["pending"] or state["flight"] is not None:
            # A known conflict may be recomputed; every other outcome must first
            # reconcile the exact original request, without invoking user code.
            conflict = state.get("conflict")
            if not conflict or conflict.get("details", {}).get("status") != "conflict":
                if (self.bundle != self._command_bundle
                        or self._commands and self._commands != state["pending"]):
                    raise TimelineEditError("local edits differ from the original request; reopen to reconcile it")
                try:
                    result = self.session.flush(idempotency_key=idempotency_key, dry_run=dry_run)
                except CommitConflict as exc:
                    conflict = exc.failure
                    with self.session.outbox.locked():
                        state = self.session._state()
                else:
                    return self._accepted(result)
            if conflict.get("details", {}).get("status") != "conflict":
                raise CommitConflict(conflict)
            if not function or evaluation.get("kind") != "function" or count >= 3:
                raise CommitConflict(conflict)
            base = _pin(conflict["details"]["current"])
            idempotency_key = None
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
                working = Timeline(self.session, bundle, base, evaluating=True)
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
                    working._commands, label=label, steps=steps, merge=effective_merge, reads=reads,
                    idempotency_key=idempotency_key, dry_run=dry_run, expected_state=state, base=base,
                    evaluation={"kind": "function" if function else "label", "count": count},
                )
            except CommitConflict as exc:
                if not function or exc.failure["details"].get("status") != "conflict" or count >= 3:
                    raise
                base = _pin(exc.failure["details"]["current"])
                idempotency_key = None
                with self.session.outbox.locked():
                    state = self.session._state()
                continue
            return self._accepted(result)

    def save(self, *args, **kwargs):
        raise TimelineEditError("use commit(label) to save a Runtime timeline")

    def publish(self, *args, **kwargs):
        raise TimelineEditError("use commit(label) to publish a Runtime timeline")


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
