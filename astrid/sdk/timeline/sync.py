"""Guarded timeline commands through the generated Runtime commit operation.

The Runtime owns acceptance/history. This module retains only pending intent and
one exact request until its acknowledgement is durably applied.
"""
from __future__ import annotations

import copy
import hashlib
import json
import shlex
import uuid
from urllib.parse import quote

from astrid.sdk.timeline._common import TimelineEditError
from astrid.sdk.timeline.outbox import Outbox, request_bytes


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
    return transport._generated, identity


def _pin(value):
    if not isinstance(value, dict) or not all(isinstance(value.get(key), str) and value[key]
                                             for key in ("revision_id", "publication_id")):
        raise TimelineEditError("timeline has no verified publication; editing is unavailable")
    return {key: value[key] for key in ("revision_id", "publication_id")}


class TimelineSession:
    def __init__(self, client, outbox, identity, project_id, timeline_id):
        self.client, self.outbox, self.identity = client, outbox, identity
        self.project_id, self.timeline_id = project_id, timeline_id
        self.path = f"/v1/projects/{quote(project_id, safe='')}/timelines/{quote(timeline_id, safe='')}/commit"

    @classmethod
    def open(cls, project, timeline, *, client, outbox_path=None):
        from astrid.sdk.storage_root import resolve_runtime_data_root
        from astrid.sdk.timeline.store import resolve_ids

        generated, identity = _connection(client)
        project_id, timeline_id, _ = resolve_ids(project, timeline, client=client)
        scope = {**identity, "project_id": project_id, "timeline_id": timeline_id}
        if outbox_path is None:
            name = hashlib.sha256(request_bytes(scope)).hexdigest() + ".json"
            outbox_path = resolve_runtime_data_root() / "timeline-outbox" / name
        session = cls(client, Outbox(outbox_path), identity, project_id, timeline_id)
        with session.outbox.locked():
            state = session.outbox.read()
            if state is None:
                head = generated.list_timeline_commits(project_id, timeline_id, limit=1)["head"]
                session.outbox.write({"scope": scope, "base": _pin(head), "pending": [], "flight": None})
            elif state["scope"] != scope:
                raise TimelineEditError("outbox belongs to a different realm, actor, project or timeline")
            elif not state["pending"] and state["flight"] is None:
                state["base"] = _pin(generated.list_timeline_commits(project_id, timeline_id, limit=1)["head"])
                session.outbox.write(state)
        return session

    def _state(self):
        _, identity = _connection(self.client)
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

        with self.outbox.locked():
            state = self._state()
            command = capture_move(self._bundle(state), select, on)
            state["pending"].append(copy.deepcopy(command))
            self.outbox.write(state)
            return copy.deepcopy(command)

    def move(self, select, on, *, idempotency_key=None, dry_run=False, via="python"):
        # A repeated one-shot CLI/SDK invocation retries original intent, never
        # recaptures guards from a possibly changed head after a lost ACK.
        with self.outbox.locked():
            state = self._state()
            pending = state["pending"]
            if pending:
                command = pending[0]
                if len(pending) != 1 or command["op"] != "clip.move" or command["select"] != select or command["args"] != {"on": on}:
                    raise TimelineEditError("pending intent differs; flush the original request before another move")
            else:
                from astrid.sdk.timeline.capture import capture_move

                pending.append(capture_move(self._bundle(state), select, on))
                self.outbox.write(state)
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

    def flush(self, *, idempotency_key=None, dry_run=False, via="python"):
        """Send/retry exactly one prefix; leave newer local commands untouched."""
        with self.outbox.locked():
            state = self._state()
            flight = state["flight"]
            if flight is None:
                if not state["pending"]:
                    raise TimelineEditError("no pending timeline commands")
                body = {"api_version": 1, "project_id": self.project_id, "timeline_id": self.timeline_id,
                        "base_revision_id": state["base"]["revision_id"],
                        "base_publication_id": state["base"]["publication_id"],
                        "commands": copy.deepcopy(state["pending"]), "source": {"via": via}, "dry_run": dry_run}
                key = idempotency_key if idempotency_key is not None else f"timeline-edit-{uuid.uuid4().hex}"
                if key == state.get("preview_key"):
                    raise TimelineEditError("use a fresh key after a preview")
                flight = {"path": self.path, "body": request_bytes(body).decode(), "key": key,
                          "count": len(state["pending"])}
                state["flight"] = flight
                self.outbox.write(state)
            body = json.loads(flight["body"])
            if (flight["path"] != self.path or body["commands"] != state["pending"][:flight["count"]]
                    or request_bytes(body).decode() != flight["body"]
                    or body["project_id"] != self.project_id or body["timeline_id"] != self.timeline_id
                    or body["base_revision_id"] != state["base"]["revision_id"]
                    or body["base_publication_id"] != state["base"]["publication_id"]
                    or (idempotency_key is not None and idempotency_key != flight["key"])
                    or body["dry_run"] != dry_run):
                raise TimelineEditError("in-flight request is immutable; retry its original payload and key")
            generated, _ = _connection(self.client)
            try:
                result = generated.commit_timeline(self.project_id, self.timeline_id, body,
                                                   idempotency_key=flight["key"])
            except Exception as exc:
                details = getattr(exc, "details", {})
                if isinstance(details, dict) and details.get("status") in {"conflict", "refused"}:
                    failure = {"code": getattr(exc, "code", "conflict"), "message": str(getattr(exc, "message", exc)), "details": details}
                    state["conflict"] = failure
                    self.outbox.write(state)
                    raise CommitConflict(failure) from exc
                raise  # Ambiguous transport failure: retain exact flight unchanged.
            data, receipt = result["data"], result["receipt"]
            if any(key != value for key, value in data.get("id_map", {}).items()):
                raise TimelineEditError("Runtime returned a nonidentity id_map; request remains in flight")
            if dry_run:
                if data.get("status") != "preview" or receipt is not None:
                    raise TimelineEditError("Runtime did not return an unaccepted preview")
                state["preview_key"] = flight["key"]
            else:
                if data.get("status") not in {"accepted", "rebased"} or not receipt:
                    raise TimelineEditError("Runtime did not acknowledge acceptance; request remains in flight")
                if receipt.get("idempotency_key") != flight["key"] or receipt.get("project_id") != self.project_id:
                    raise TimelineEditError("Runtime acknowledged another request; request remains in flight")
                state["base"] = _pin({"revision_id": data.get("accepted_revision_id"),
                                       "publication_id": receipt.get("receipt_id")})
                del state["pending"][:flight["count"]]
            state["flight"] = None
            state.pop("conflict", None)
            self.outbox.write(state)
            result = copy.deepcopy(result)
            if not dry_run:
                result["data"]["accepted_publication_id"] = receipt["receipt_id"]
                result["data"]["show_command"] = shlex.join([
                    "astrid", "timelines", "show", self.timeline_id, "--project", self.project_id,
                    "--published", "--revision-id", data["accepted_revision_id"],
                ])
            return result
