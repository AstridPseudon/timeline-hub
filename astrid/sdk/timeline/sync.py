"""Guarded timeline commands through the public Runtime client bridge.

The Runtime owns acceptance/history. This module retains only pending intent and
one exact request until its acknowledgement is durably applied.
"""
from __future__ import annotations

import copy
import hashlib
import json
import re
import shlex
import uuid
from urllib.parse import quote

from astrid.core.receipts.canonical import canonical_json
from astrid.core.receipts.contract import CommandReceipt
from astrid.sdk.timeline._common import TimelineEditError
from astrid.sdk.timeline.outbox import Outbox, request_bytes
from astrid.sdk.workspace_client import WorkspaceClientError


class CommitConflict(TimelineEditError):
    def __init__(self, failure):
        self.failure = copy.deepcopy(failure)
        super().__init__(failure.get("message", "timeline commit refused"))


def _connection(client):
    transport = client._remote._transport
    handshake = transport._last_handshake or {}
    identity = {"realm_id": handshake.get("realm_id"), "actor_id": handshake.get("actor_id")}
    if not all(isinstance(value, str) and value for value in identity.values()):
        raise TimelineEditError("timeline commands require an authenticated Runtime realm and actor")
    return identity


def _response(result):
    if not result.ok:
        error = result.error
        raise WorkspaceClientError(0, error.code, error.message, dict(error.details))
    return result.as_dict()


def _pin(value):
    if not isinstance(value, dict) or not all(isinstance(value.get(key), str) and value[key]
                                             for key in ("revision_id", "publication_id")):
        raise TimelineEditError("timeline has no verified publication; editing is unavailable")
    return {key: value[key] for key in ("revision_id", "publication_id")}


def _native_command(command):
    from astrid.sdk.timeline.commands import operations, validate_command

    command = copy.deepcopy(command)
    validate_command(command)
    if command["op"] not in operations():
        raise TimelineEditError("queue/commit requires a registered native operation")
    return command


def _ack(result, body, flight, identity):
    """Check acceptance identity, leaving full closure validation to Runtime."""
    from astrid.sdk.timeline.commands import validate_command

    def require(condition):
        if not condition:
            raise ValueError("invalid acceptance identity")

    try:
        data, receipt = result["data"], result["receipt"]
        require(isinstance(data, dict))
        for key in ("base_revision_id", "base_publication_id", "provider_version", "compiler_version"):
            require(isinstance(data[key], str) and data[key])
        require(all(data[key] == body[key] for key in ("base_revision_id", "base_publication_id")))
        require(isinstance(data["commands"], list) and data["commands"])
        for command in data["commands"]:
            validate_command(command)
        require(isinstance(data["id_map"], dict))
        if any(not isinstance(key, str) or not key or key != value for key, value in data["id_map"].items()):
            raise TimelineEditError("Runtime returned a nonidentity id_map; request remains in flight")
        document = data["canonical_document"]
        require(isinstance(document, dict) and type(document["schema_version"]) is int and document["schema_version"] == 1)
        require(document["project_id"] == body["project_id"] and document["timeline_id"] == body["timeline_id"])
        parent = document["parent_revision"]
        require(isinstance(parent, dict) and isinstance(parent["revision_id"], str) and parent["revision_id"])
        require(isinstance(parent["payload"], dict))
        for digest in (data["document_digest"], parent["content_digest"]):
            require(isinstance(digest, str) and re.fullmatch(r"sha256:[0-9a-f]{64}", digest))
        for key in ("shot_revisions", "internal_timeline_revisions"):
            require(isinstance(document[key], list) and all(isinstance(row, dict) for row in document[key]))
        manifest = document["dependency_manifest"]
        require(isinstance(manifest, dict))
        for key in ("shots", "internal_timelines", "media", "documents"):
            require(isinstance(manifest[key], list) and all(isinstance(row, dict) for row in manifest[key]))
        if body.get("dry_run", False):
            require(data["status"] == "preview" and receipt is None)
            _pin(data["evaluated_head"])
            require(not any(key in data for key in ("accepted_revision_id", "publisher", "accepted_publication_id")))
        else:
            require(data["status"] in {"accepted", "rebased"})
            CommandReceipt.from_dict(receipt)
            require(receipt["command_kind"] == "timeline.commit")
            require(receipt["project_id"] == body["project_id"] and receipt["idempotency_key"] == flight["key"])
            require(receipt["result"] == data and data["publisher"] == identity["actor_id"])
            invocation = {"operation": "commitTimeline", "path": flight["path"],
                          "publisher": identity["actor_id"], "request": body}
            require(receipt["request_hash"] == hashlib.sha256(canonical_json(invocation).encode()).hexdigest())
            require(data["accepted_revision_id"] == parent["revision_id"])
            previous = _pin({"revision_id": data["previous_revision_id"], "publication_id": data["previous_publication_id"]})
            base = {"revision_id": body["base_revision_id"], "publication_id": body["base_publication_id"]}
            require(receipt["receipt_id"] not in {previous["publication_id"], base["publication_id"]})
            if data["status"] == "accepted":
                require(data["rebased_onto"] is None and previous == base)
            else:
                require(_pin(data["rebased_onto"]) == previous and previous != base)
    except TimelineEditError:
        raise
    except (KeyError, TypeError, ValueError) as exc:
        raise TimelineEditError("invalid Runtime acknowledgement; request remains in flight") from exc
    return data, receipt


class TimelineSession:
    def __init__(self, client, outbox, identity, project_id, timeline_id):
        self.client, self.outbox, self.identity = client, outbox, identity
        self.project_id, self.timeline_id = project_id, timeline_id
        self.path = f"/v1/projects/{quote(project_id, safe='')}/timelines/{quote(timeline_id, safe='')}/commit"

    @classmethod
    def open(cls, project, timeline, *, client, outbox_path=None,
             base_revision_id=None, base_publication_id=None):
        from astrid.sdk.storage_root import resolve_runtime_data_root
        from astrid.sdk.timeline.store import resolve_ids

        base = None if base_revision_id is None and base_publication_id is None else _pin({
            "revision_id": base_revision_id, "publication_id": base_publication_id})
        identity = _connection(client)
        project_id, timeline_id, _ = resolve_ids(project, timeline, client=client)
        scope = {**identity, "project_id": project_id, "timeline_id": timeline_id}
        explicit_outbox = outbox_path is not None
        if outbox_path is None:
            name = hashlib.sha256(request_bytes(scope)).hexdigest() + ".json"
            outbox_path = resolve_runtime_data_root() / "timeline-outbox" / name
        session = cls(client, Outbox(outbox_path), identity, project_id, timeline_id)
        session._explicit_outbox = explicit_outbox
        while True:
            with session.outbox.locked():
                state = session.outbox.read()
                if state is not None:
                    if state["scope"] != scope:
                        raise TimelineEditError("outbox belongs to a different realm, actor, project or timeline")
                    if state["pending"] or state["flight"] is not None:
                        session._state()
                        if base is not None and state["base"] != base:
                            raise TimelineEditError("pending intent belongs to a different original base")
                        return session
            head = base or _pin(_response(client.timelines.history(project_id, timeline_id, limit=1))["data"]["head"])
            with session.outbox.locked():
                if _connection(client) != identity:
                    raise TimelineEditError("outbox identity changed while reading its head")
                if session.outbox.read() != state:
                    continue
                state = state or {"scope": scope, "pending": [], "flight": None}
                state["base"] = head
                session.outbox.write(state)
                break
        return session

    def _state(self):
        identity = _connection(self.client)
        state = self.outbox.read()
        if identity != self.identity or state["scope"] != {
            **identity, "project_id": self.project_id, "timeline_id": self.timeline_id,
        }:
            raise TimelineEditError("outbox identity changed; reconnect to its original realm and actor")
        return state

    def _bundle(self, state):
        from astrid.sdk.timeline.commands import execute
        from astrid.sdk.timeline.store import fetch_bundle

        bundle = fetch_bundle(self.project_id, self.timeline_id,
                              revision_id=state["base"]["revision_id"], client=self.client)
        return execute(bundle, state["pending"]).bundle if state["pending"] else bundle

    def queue_move(self, select, on):
        """Capture once against the original state plus earlier local commands."""
        from astrid.sdk.timeline.capture import capture_move

        return self._queue(lambda state: capture_move(self._bundle(state), select, on))

    def queue_proposal(self, proposal):
        """Persist the settled batch unchanged at its original admitted base."""
        from astrid.sdk.timeline.producer import build_producer_batch

        batch = build_producer_batch(proposal)
        if (batch['project_id'], batch['timeline_id']) != (self.project_id, self.timeline_id):
            raise TimelineEditError('proposal belongs to a different project or timeline')
        with self.outbox.locked():
            state = self._state()
            if state['pending'] or state['flight'] is not None:
                raise TimelineEditError('flush pending intent before queueing a proposal')
            state['base'] = {'revision_id': batch['base_revision_id'],
                             'publication_id': batch['base_publication_id']}
            state['pending'], state['rationale'] = batch['commands'], batch['rationale']
            self.outbox.write(state)
        return copy.deepcopy(batch['commands'])

    def queue(self, command):
        """Capture native intent over the original base plus pending commands.

        Supplied capture claims are verified by execute, never refreshed.
        """
        return self.queue_many([command])[0]

    def queue_many(self, commands):
        """Atomically capture a batch on the original base, staging its own prefix.

        Commands are registered EditCommands; supplied claims are never refreshed.
        Missing capture inputs fail before any command is added to the outbox.
        """
        from astrid.sdk.timeline.commands import execute

        commands = [_native_command(command) for command in commands]
        return self._stage(lambda state: execute(self._bundle(state), commands).commands)

    def commit(self, command, *, idempotency_key=None, dry_run=False, via="python"):
        """Capture and flush one native command, or retry its original flight."""
        return self.commit_many([command], idempotency_key=idempotency_key, dry_run=dry_run, via=via)

    def commit_many(self, commands, *, idempotency_key=None, dry_run=False, via="python", base=None):
        """Capture and flush a batch, or retry its exact flight before a suffix."""
        from astrid.sdk.timeline._command_state import equal
        from astrid.sdk.timeline.commands import execute

        commands = [_native_command(command) for command in commands]
        self._stage(lambda state: execute(self._bundle(state), commands).commands,
                    lambda pending: len(pending) == len(commands) and all(
                        all(equal(saved.get(key), value) for key, value in command.items() if key != "intent")
                        and all(equal(saved["intent"].get(key), value)
                                for key, value in command.get("intent", {}).items())
                        for saved, command in zip(pending, commands)), base=base)
        return self.flush(idempotency_key=idempotency_key, dry_run=dry_run, via=via)

    def _queue(self, capture, matches=None):
        return self._stage(lambda state: [capture(state)], matches, retry_capture=True)[0]

    def _stage(self, capture, matches=None, *, retry_capture=False, base=None):
        from astrid.sdk.timeline._command_state import equal

        while True:
            with self.outbox.locked():
                state = self._state()
                if base is not None and state["base"] != _pin(base):
                    raise TimelineEditError("outbox no longer has the original sheet basis")
                if any(call['op'] == 'producer.guard' for call in state['pending']):
                    raise TimelineEditError('flush the producer proposal before another edit')
                if matches is not None and state["pending"]:
                    prefix = state["pending"][:state["flight"]["count"]] if state["flight"] else state["pending"]
                    if not matches(prefix):
                        raise TimelineEditError("pending intent differs; flush the original request before another edit")
                    return copy.deepcopy(prefix)
            commands = capture(state)
            with self.outbox.locked():
                if not equal(self._state(), state):
                    if retry_capture:  # Preserve the existing move callback concurrency contract.
                        continue
                    raise TimelineEditError("outbox changed during capture; original intent was not queued")
                state["pending"].extend(copy.deepcopy(commands))
                self.outbox.write(state)
                return copy.deepcopy(commands)

    def move(self, select, on, *, idempotency_key=None, dry_run=False, via="python"):
        # A repeated one-shot CLI/SDK invocation retries original intent, never
        # recaptures guards from a possibly changed head after a lost ACK.
        from astrid.sdk.timeline.capture import capture_move

        self._queue(lambda state: capture_move(self._bundle(state), select, on),
                    lambda pending: len(pending) == 1 and pending[0]["op"] == "clip.move"
                    and pending[0]["select"] == select and pending[0]["args"] == {"on": on})
        return self.flush(idempotency_key=idempotency_key, dry_run=dry_run, via=via)

    def trim(self, select, *, in_s=None, out_s=None, idempotency_key=None, dry_run=False, via="python"):
        """Capture a literal source trim once, retrying its original flight."""
        from astrid.sdk.timeline._trim_commands import capture_clip_trim

        self._queue(lambda state: capture_clip_trim(self._bundle(state), select, in_s=in_s, out_s=out_s),
                    lambda pending: len(pending) == 1 and pending[0]["op"] == "clip.trim"
                    and pending[0]["select"] == select
                    and pending[0]["args"] == {"in_s": in_s, "out_s": out_s})
        return self.flush(idempotency_key=idempotency_key, dry_run=dry_run, via=via)

    def undo(self, publications, *, idempotency_key=None, dry_run=False, via="python"):
        publications = list(publications)
        if not publications or len(set(publications)) != len(publications) or not all(isinstance(p, str) and p for p in publications):
            raise TimelineEditError("undo requires a nonempty unique list of publication IDs, oldest first")
        command = {"schema_version": 1, "op": "timeline.inverse", "version": "1",
                   "select": None, "args": {"publications": publications}}
        with self.outbox.locked():
            state = self._state()
            if state["pending"] and state["pending"] != [command]:
                raise TimelineEditError("flush pending intent before undo")
            state["pending"] = [command]
            self.outbox.write(state)
        return self.flush(idempotency_key=idempotency_key, dry_run=dry_run, via=via)

    def restore(self, revision_id, content_digest, *, idempotency_key=None, dry_run=False, via="python"):
        """Restore one exact retained revision through the native commit path.

        The revision and digest are caller-supplied historical identity pins;
        neither is inferred from a legacy numeric version.  Staging and flush
        retain the normal outbox draft and exact-retry guarantees.
        """
        if not isinstance(revision_id, str) or not revision_id:
            raise TimelineEditError("restore requires an exact nonempty revision_id")
        if not isinstance(content_digest, str) or not content_digest:
            raise TimelineEditError("restore requires the exact nonempty content_digest")
        command = {
            "schema_version": 1,
            "op": "timeline.restore",
            "version": "1",
            "select": None,
            "args": {"revision_id": revision_id, "content_digest": content_digest},
        }
        with self.outbox.locked():
            state = self._state()
            if state["pending"] and state["pending"] != [command]:
                raise TimelineEditError("flush pending intent before restore")
            state["pending"] = [command]
            self.outbox.write(state)
        return self.flush(idempotency_key=idempotency_key, dry_run=dry_run, via=via)

    def flush(self, *, idempotency_key=None, dry_run=False, via="python"):
        """Send/retry exactly one prefix; leave newer local commands untouched."""
        return self._flush(idempotency_key=idempotency_key, dry_run=dry_run, via=via)

    def _flush(self, *, idempotency_key=None, dry_run=False, via="python", prepare=None):
        with self.outbox.locked():
            state = self._state()
            if prepare is not None:
                prepare(state)
            flight = state["flight"]
            if flight is None:
                if not state["pending"]:
                    raise TimelineEditError("no pending timeline commands")
                body = {"api_version": 1, "project_id": self.project_id, "timeline_id": self.timeline_id,
                        "base_revision_id": state["base"]["revision_id"],
                        "base_publication_id": state["base"]["publication_id"],
                        "commands": copy.deepcopy(state["pending"]), "source": {"via": via}, "dry_run": dry_run}
                if 'rationale' in state:
                    body['rationale'] = state['rationale']
                key = idempotency_key if idempotency_key is not None else f"timeline-edit-{uuid.uuid4().hex}"
                if key == state.get("preview_key"):
                    raise TimelineEditError("use a fresh key after a preview")
                flight = {"path": self.path, "body": request_bytes(body).decode(), "key": key,
                          "count": len(state["pending"]), "fence": uuid.uuid4().hex}
                state["flight"] = flight
                self.outbox.write(state)
            body = self._flight_body(state, flight, idempotency_key, dry_run)
            if "fence" not in flight:  # Preserve requests persisted before fencing was added.
                flight["fence"] = uuid.uuid4().hex
                self.outbox.write(state)
            flight = copy.deepcopy(flight)
        try:
            result = _response(self.client.timelines.commit(
                self.project_id, self.timeline_id, body, idempotency_key=flight["key"],
            ))
        except Exception as exc:
            details = getattr(exc, "details", {})
            if isinstance(details, dict) and details.get("status") in {"conflict", "refused"}:
                failure = {"code": getattr(exc, "code", "conflict"), "message": str(getattr(exc, "message", exc)), "details": details}
                with self.outbox.locked():
                    state = self._state()
                    if state["flight"] == flight:
                        self._flight_body(state, flight, idempotency_key, dry_run)
                        state["conflict"] = failure
                        self.outbox.write(state)
                raise CommitConflict(failure) from exc
            raise  # Ambiguous failure: never replace the durable flight.
        data, receipt = _ack(result, body, flight, self.identity)
        with self.outbox.locked():
            state = self._state()
            # A duplicate send may finish after another send acknowledged this
            # prefix and even started the next flight. Its response is read-only.
            if state["flight"] == flight:
                self._flight_body(state, flight, idempotency_key, dry_run)
                if dry_run:
                    state["preview_key"] = flight["key"]
                else:
                    state["base"] = _pin({"revision_id": data["accepted_revision_id"],
                                           "publication_id": receipt["receipt_id"]})
                    del state["pending"][:flight["count"]]
                    state.pop('rationale', None)
                state["flight"] = None
                state.pop("conflict", None)
                self.outbox.write(state)
        result = copy.deepcopy(result)
        result["data"] = copy.deepcopy(data)
        if not dry_run:
            result["data"]["accepted_publication_id"] = receipt["receipt_id"]
            result["data"]["show_command"] = shlex.join([
                "astrid", "timelines", "show", self.timeline_id, "--project", self.project_id,
                "--published", "--revision-id", data["accepted_revision_id"],
            ])
        return result

    def _flight_body(self, state, flight, key, dry_run):
        from astrid.sdk.timeline._command_state import equal

        try:
            body = json.loads(flight["body"])
            count = flight["count"]
            valid = (type(count) is int and 0 < count <= len(state["pending"])
                     and isinstance(flight["key"], str) and bool(flight["key"])
                     and flight["path"] == self.path
                     and equal(body["commands"], state["pending"][:count])
                     and request_bytes(body).decode() == flight["body"]
                     and body["project_id"] == self.project_id and body["timeline_id"] == self.timeline_id
                     and body["base_revision_id"] == state["base"]["revision_id"]
                     and body["base_publication_id"] == state["base"]["publication_id"]
                     and (key is None or key == flight["key"])
                     and body.get("dry_run", False) == dry_run)
        except (KeyError, TypeError, ValueError) as exc:
            raise TimelineEditError("invalid in-flight request; original intent retained") from exc
        if not valid:
            raise TimelineEditError("in-flight request is immutable; retry its original payload and key")
        return body
