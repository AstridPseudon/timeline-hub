"""CLI restore request producer; the existing semantic COMMIT owns all image edits.

The timeline journal retains the original envelope before dispatch so a repeated
key replays the same captured head, selection, session and receipt after a race
or lost response. No draft or public history is rewritten here.
"""
from __future__ import annotations

import copy
import hashlib
import uuid

from astrid.sdk.contracts import DomainResult, ErrorObject
from astrid.sdk.timeline import journal
from astrid.sdk.timeline._common import TimelineEditError
from astrid.sdk.timeline.commit import _digest
from astrid.sdk.timeline.revisions import RuntimeRevisions, resolve_revision_record
from astrid.sdk.timeline.saved_intent import _finite_json
from astrid.sdk.timeline.saved_publish import _authenticate, _key, _verify_result, _workspace
from astrid.sdk.workspace_client import WorkspaceClientError

# This is a sealed incident qualification, not a classifier for arbitrary 401s.
# The full 15-line snapshot binds the captured session, origin, base and target
# without copying them (or any credentials) into the resolution record.
_REFUSAL_CAPTURE = dict(
    qualification="d233-single-send-preacceptance-v1",
    request_id="d1ba6a87f3764b738a9680f56fde919e",
    request_hash="sha256:3a3d096b87ca8d0062e508fc1df23d45d3b9fe91494d5bde77c54aec30fa95d8",
    project_id="0e60c5b0db0c4905a8385a4ce8325970", timeline_id="d189-speech-200",
    journal_sha256="aaac20aa3a07b8990f169fa36c2033da72f2db61061fb5358c5d00c18f64aacb",
    response_sha256="79ded6e8b6796f2c3f58e229a25c3be3940690ecf6c805dab2c8a041bf8c9281",
    send_count=1,
)
# Source/protocol proof adopted in the retained ruling. Neither check location
# identifies which historical cancellation/relay disjunct failed. Both are
# before durable acceptance; exceptions at the final check roll back completely.
_REFUSAL_PROTOCOL_PROOF = dict(
    runtime_commit="9eaa2aafd40cedac80adcf9c738ea8f09a854eed",
    authoring_scene_sha256="13601c40e79fff2868b7aea13ea293be630e9149bf76be7a2d2fbb651ebf15e8",
    timeline_commit_sha256="33db3a288431678412e22df1addca517177dd365f4aff17edd1f85addf049f9a",
    ruling_sha256="d922e1b7da3c9b3e8fde3475954ae3890846a257fcf12c00b678218eb10141ac",
    checks=["before_publication", "inside_acceptance_transaction"],
    exceptions_rollback=True, post_acceptance_readback="distinct_ambiguous_path",
)
_RESOLUTION_KIND = "restore-commit-local-refusal-resolution-v1"
_REFUSAL_EVIDENCE_LIMIT = 16384


def resolve_restore_refusal(project, timeline, *, evidence, response):
    """Resolve only the qualified single D233 send, entirely locally.

    ``evidence`` is a finite JSON object with kind restore-refusal-evidence-v1,
    the exact _REFUSAL_CAPTURE fields, the original envelope's origin, and the
    exact _REFUSAL_PROTOCOL_PROOF as protocol_proof. ``response`` is the original
    response file's bytes, not a reserialized object. Only a byte-identical
    captured journal (or its already-resolved prefix) is admitted. Prior or
    additional sends are outside this qualification, even with the same body.

    No client, lookup, Runtime result, history row or acceptance is created.
    The historical cancellation/relay cause remains unknown.
    """
    try:
        if (not isinstance(evidence, dict) or not isinstance(response, bytes)
                or len(response) > _REFUSAL_EVIDENCE_LIMIT):
            raise ValueError
        # Bound metadata before use and reject nonfinite/duplicate JSON at the CLI.
        from astrid.sdk.timeline.journal import _canonical
        if len(_canonical(evidence).encode("utf-8")) > _REFUSAL_EVIDENCE_LIMIT:
            raise ValueError
        expected = dict(kind="restore-refusal-evidence-v1", **_REFUSAL_CAPTURE,
                        origin=evidence.get("origin"), protocol_proof=_REFUSAL_PROTOCOL_PROOF)
        if (not isinstance(evidence.get("origin"), dict) or _digest(evidence) != _digest(expected)
                or (project, timeline) != (_REFUSAL_CAPTURE["project_id"], _REFUSAL_CAPTURE["timeline_id"])
                or hashlib.sha256(response).hexdigest() != _REFUSAL_CAPTURE["response_sha256"]):
            raise ValueError
        received = _finite_json(response.decode("utf-8"))
        if (received.get("ok") is not False or received.get("idempotency_key") != evidence["request_id"]
                or received.get("error", {}).get("code") != "unauthorized"):
            raise ValueError
        path = journal.journal_path(project, timeline)
        with journal._locked(path):
            raw = path.read_bytes()
            text = raw.decode("utf-8")
            if journal.verify_text(text):
                raise ValueError
            lines = raw.splitlines(keepends=True)
            rows = [_finite_json(line.decode("utf-8")) for line in lines]
            intents, resolutions = [], []
            for index, row in enumerate(rows):
                for item in row.get("evidence", []):
                    if not isinstance(item, dict):
                        continue
                    kind = item.get("kind")
                    key = (item.get("body") or {}).get("request_id") if kind == "restore-commit-intent-v1" else item.get("request_id")
                    if key != evidence["request_id"]:
                        continue
                    if kind == "restore-commit-intent-v1":
                        intents.append((row, item))
                    elif kind == _RESOLUTION_KIND:
                        resolutions.append((index, row, item))
                    else:
                        # Includes results and any additional journaled dispatch.
                        raise ValueError
            if len(intents) != 1 or len(resolutions) > 1:
                raise ValueError
            row, intent = intents[0]
            body = intent["body"]
            if (row.get("kind") != "restore" or row.get("outcome") != "pending"
                    or (row.get("project"), row.get("timeline")) != (project, timeline)
                    or (body["project_id"], body["timeline_id"]) != (project, timeline)
                    or _digest(body) != evidence["request_hash"]
                    or intent.get("request_hash") != evidence["request_hash"]
                    or _digest(intent.get("origin")) != _digest(evidence["origin"])):
                raise ValueError
            resolution = dict(kind=_RESOLUTION_KIND, request_id=evidence["request_id"],
                              request_hash=evidence["request_hash"], qualification=evidence["qualification"],
                              evidence_hash=_digest(evidence), response_sha256=evidence["response_sha256"],
                              journal_sha256=evidence["journal_sha256"])
            prefix = b"".join(lines[:resolutions[0][0]]) if resolutions else raw
            if hashlib.sha256(prefix).hexdigest() != evidence["journal_sha256"]:
                raise ValueError
            if resolutions:
                _, row, previous = resolutions[0]
                if (previous != resolution or row.get("evidence") != [resolution]
                        or (row.get("project"), row.get("timeline")) != (project, timeline)
                        or row.get("kind") != "restore-refusal-resolution"
                        or row.get("outcome") != "locally-resolved-refusal"):
                    raise ValueError
                try:
                    journal.sync(path)
                except OSError as exc:
                    raise TimelineEditError("local refusal resolution exists but durability is unconfirmed; repeat resolution, never restore") from exc
                return resolution
            try:
                journal._append_locked(path, project=project, timeline=timeline,
                    draft="restore-commit", kind="restore-refusal-resolution", outcome="locally-resolved-refusal",
                    label="Resolve captured pre-acceptance restore refusal locally",
                    source=dict(via="local-refusal-resolution"), evidence=(resolution,))
            except OSError as exc:
                raise TimelineEditError("local refusal resolution durability is unconfirmed; inspect journal, never restore") from exc
            return resolution
    except TimelineEditError:
        raise
    except (OSError, ValueError, TypeError, KeyError, AttributeError) as exc:
        raise TimelineEditError("restore refusal evidence or pending journal is unqualified; left unresolved") from exc


def _intent(path, key, origin, selection, message):
    if not path.exists():
        return None
    if journal.verify(path):
        raise TimelineEditError("restore journal is damaged; run timelines log --verify")
    found = []
    for line in path.read_text(encoding="utf-8").splitlines():
        row = _finite_json(line)
        for item in row.get("evidence", []):
            if isinstance(item, dict) and item.get("kind") == _RESOLUTION_KIND and item.get("request_id") == key:
                raise TimelineEditError("restore key was locally resolved as refused; it cannot dispatch again")
            if isinstance(item, dict) and item.get("kind") == "restore-commit-intent-v1" and item["body"]["request_id"] == key:
                if (item.get("request_hash") != _digest(item["body"])
                        or item.get("origin") != origin or item.get("selection") != selection
                        or item.get("message") != message
                        or (row.get("project"), row.get("timeline")) != (
                            item["body"]["project_id"], item["body"]["timeline_id"])):
                    raise TimelineEditError("restore key has different scope, origin or intent")
                found.append(item)
    if len(found) > 1:
        raise TimelineEditError("restore journal has duplicate request envelopes")
    return found[0] if found else None


def restore_revision(client, project, timeline, source, *, idempotency_key=None, message=None):
    """Submit one named whole-image COMMIT, preserving exact-key recovery."""
    key = _key(idempotency_key) or uuid.uuid4().hex
    scope = client.timelines.resolve_scope(project, timeline)
    if not scope.ok:
        return DomainResult.failure(scope.error, idempotency_key=key)
    project, canonical_timeline = scope.data["project_id"], scope.data["timeline_id"]
    if "@" in source:
        name, _, source = source.rpartition("@")
        if name and name not in {timeline, canonical_timeline}:
            raise TimelineEditError("restore source must belong to the same timeline")
    selection = dict(project=project, timeline=canonical_timeline, ref=source)
    workspace = _workspace(client)
    origin, session = _authenticate(workspace)
    path = journal.journal_path(project, canonical_timeline)
    with journal._locked(path):
        intent = _intent(path, key, origin, selection, message)
    if intent is None:
        store = RuntimeRevisions(client.timelines)
        head = store.head_state(project, canonical_timeline)
        if not head["revision_id"]:
            raise TimelineEditError("restore requires a published head")
        selected = resolve_revision_record(project, canonical_timeline, source, store=store)
        if selected is None:
            # Select the captured head event, never a fresh mutable head.
            rows = store.list(project, canonical_timeline, limit=200) or []
            selected = next((row for row in rows if row.id == head["revision_id"]
                             and row.publication_id == head["publication_id"]), None)
            if selected is None:
                raise TimelineEditError("captured restore head publication is unavailable")
        command = store.restore_command(selected)
        body = dict(api_version=1, project_id=project, timeline_id=canonical_timeline,
                    request_id=key, session_id=session, session_sequence=1,
                    base_revision_id=head["revision_id"], base_publication_id=head["publication_id"],
                    scope=dict(target="parent", complete=["clips", "tracks"], projection_version=1),
                    change=dict(commands=[command]), source=dict(via="cli"),
                    label=message if message is not None else f"Restore {selected.id}", dry_run=False)
        prepared = dict(kind="restore-commit-intent-v1", body=body, request_hash=_digest(body),
                        origin=origin, selection=selection, message=message)
        with journal._locked(path):
            intent = _intent(path, key, origin, selection, message)
            if intent is None:
                journal._append_locked(path, project=project, timeline=canonical_timeline,
                                       draft="restore-commit", kind="restore", outcome="pending", label=body["label"],
                                       source=body["source"], evidence=(prepared,))
                intent = prepared  # append fsyncs before any mutation request
    body = intent["body"]
    # Serialize reconciliation against dispatch and its durable result. A local
    # resolution cannot be appended between this final check and the send.
    with journal._locked(path):
        _intent(path, key, origin, selection, message)
        if key == _REFUSAL_CAPTURE["request_id"]:
            raise TimelineEditError("captured refused restore key requires local resolution; do not retry it")
        try:
            result = workspace.commit_timeline(copy.deepcopy(body))
            _verify_result(workspace, intent, result)
        except (WorkspaceClientError, TimelineEditError) as exc:
            return DomainResult.failure(ErrorObject(getattr(exc, "code", "unverified_commit"), str(exc), {
                "details": getattr(exc, "details", None),
                "recovery": "preserve this pending key and envelope; reconcile captured evidence before any retry",
            }), idempotency_key=key)
        journal._append_locked(path, project=project, timeline=canonical_timeline,
                               draft="restore-commit", kind="restore", outcome=result["status"], label=body["label"],
                               source=body["source"], evidence=(dict(
                                   kind="restore-commit-result-v1", request_id=key,
                                   request_hash=intent["request_hash"], result=copy.deepcopy(result)),))
    if result["status"] != "accepted":
        error = result.get("error") or {}
        return DomainResult.failure(ErrorObject(error.get("code", result["status"]),
            error.get("message", "restore COMMIT requires correction"), {"receipt": result}),
            idempotency_key=key)
    return DomainResult.success(result, idempotency_key=key)
