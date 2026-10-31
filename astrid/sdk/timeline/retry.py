"""Retry durable timeline edits saved after a conflict."""
from __future__ import annotations

import copy
import hashlib
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote

from . import clash
from .sync import _response
from .outbox import Outbox


def _pin(value):
    return {"revision_id": value["revision_id"], "publication_id": value["publication_id"]}


def _record_digest(record):
    encoded = json.dumps(record, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    return hashlib.sha256(encoded).hexdigest()


def _record(timeline, ref):
    if not isinstance(ref, str):
        ref = getattr(ref, "pending_id", None)
    if not isinstance(ref, str) or not ref:
        raise ValueError("retry requires a pending id or key")
    actors = "self" if getattr(timeline.session, "_explicit_outbox", False) else "all"
    found = [(path, record) for path, record in timeline._pending_records_with_paths(actors)
             if record.get("id") == ref or record.get("key") == ref]
    if not found:
        raise ValueError(f"no pending change with id or key {ref!r}")
    if len(found) > 1:
        raise ValueError(f"pending key {ref!r} is ambiguous; use a pending id")
    return found[0]


def _close(path, record, session, entry, how):
    publication = entry.get("publication_id")
    receipt = entry.get("receipt", {}).get("receipt_id") or publication
    actor = entry.get("publisher")
    base = _pin(entry)
    outbox = session.outbox if Path(path) == Path(session.outbox.path) else Outbox(Path(path))
    with outbox.locked():
        state = outbox.read()
        saved = state.get("pending_changes", {}).get(record["id"]) if isinstance(state, dict) else None
        if saved is None:
            return record
        if (saved.get("state") == "pending"
                and saved.get("part", 0) == record.get("part", 0)
                and receipt not in saved.get("receipts", [])):
            index = saved.get("part", 0)
            parts = saved.get("parts") or []
            saved.setdefault("receipts", []).append(receipt)
            if index + 1 < len(parts):
                saved["part"] = index + 1
                parts[index + 1]["base"] = copy.deepcopy(base)
                saved["attempts"] = int(saved.get("attempts", 1))
            else:
                saved["state"] = "landed"
                saved["closed_by"] = {"actor_id": actor,
                                       "publication_id": publication, "how": how}
            saved["rev"] = int(saved.get("rev", 0)) + 1
            saved["updated_at"] = datetime.now(timezone.utc).isoformat()
            outbox.write(state)
        return copy.deepcopy(saved)


def _landed(timeline, path, record):
    if record.get("state") == "landed":
        closed = record.get("closed_by") or {}
        publication = closed.get("publication_id")
        actor = closed.get("actor_id")
        label = record.get("label") or "Timeline edit"
        suffix = f" (by {actor})" if actor else ""
        return {"status": "landed", "pending_id": record["id"],
                "summary": f'"{label}" already landed as {publication}{suffix}; '
                           f'{record["id"]} is closed. Nothing was sent.', "next": None}
    base = _pin(record["parts"][0]["base"])
    try:
        _, entries = clash._history(timeline.session, base)
    except Exception:  # noqa: BLE001 - history is only a recovery confirmation path
        return None
    matches = [item for item in entries if item.get("group_id") == record["id"]]
    index = record.get("part", 0)
    if type(index) is not int or index < 0 or len(matches) <= index:
        return None
    entry = matches[index]
    publication = entry.get("publication_id")
    if publication is None:
        publication = entry.get("receipt", {}).get("receipt_id")
    closed = _close(path, record, timeline.session, entry, "retry")
    actor = entry.get("publisher")
    label = record.get("label") or "Timeline edit"
    suffix = f" (by {actor})" if actor else ""
    if closed.get("state") != "landed":
        return {"status": "part_landed", "pending_id": record["id"],
                "data": {"publication_id": publication, "part": closed.get("part")},
                "summary": f'Part {index + 1} of "{label}" landed as {publication}{suffix}; '
                           f'{record["id"]} still has saved work.',
                "next": f'tl.retry({record["id"]!r})', "record": closed}
    data = {"publication_id": publication}
    receipt = entry.get("receipt")
    if isinstance(receipt, dict):
        data["receipt"] = copy.deepcopy(receipt)
    return {"status": "landed", "pending_id": record["id"], "data": data,
            "summary": f'"{label}" already landed as {publication}{suffix}; '
                       f'{record["id"]} is closed. Nothing was sent.', "next": None,
            "record": closed}


def _part(record):
    parts = record.get("parts") or []
    index = record.get("part", 0)
    if type(index) is not int or index < 0 or index >= len(parts):
        raise ValueError("pending change has no retryable part")
    return parts[index]


def _refresh_function_base(timeline, record):
    """Move an exhausted function retry's empty outbox to a verified head."""
    session = timeline.session
    with session.outbox.locked():
        state = session._state()
        # A flight may have an unknown outcome. Let commit() reconcile it; never
        # replace it with a fresh evaluation. Likewise, don't move a queued tail.
        if state.get("flight") is not None or state.get("pending"):
            return False
        base = _pin(_part(record)["base"])
        head, _ = clash._history(session, base)
        state["base"] = _pin(head)
        state.pop("conflict", None)
        state.pop("evaluation", None)
        session.outbox.write(state)
    return True


def _request(record, part):
    options = copy.deepcopy(part.get("commit_options") or {})
    evaluation = part.get("evaluation") or {}
    steps = options.get("steps") or []
    scope = {"kind": "scope", "ref": "timeline", "path": []}
    if (evaluation.get("kind") == "function" and evaluation.get("synthetic_function_scope") is True
            and options.get("merge") == "atomic" and "reads" not in options
            and all(step.get("reads") and step["reads"][-1] == scope for step in steps)):
        for step in steps:
            step["reads"].pop()
            if not step["reads"]:
                del step["reads"]
        options["merge"] = "fields"
    base = _pin(part["base"])
    request = {"base_revision_id": base["revision_id"],
               "base_publication_id": base["publication_id"],
               "commands": copy.deepcopy(part["commands"]),
               "label": options.pop("label", record.get("label") or "Timeline edit"),
               **options}
    request.setdefault("merge", "fields")
    if "reads" not in request and request.get("merge") != "atomic":
        request["reads"] = []
    if part.get("rationale") is not None:
        request["rationale"] = copy.deepcopy(part["rationale"])
    if part.get("group_id") is not None:
        request["group_id"] = copy.deepcopy(part["group_id"])
    request["imports"] = copy.deepcopy(part.get("imports", []))
    request["source"] = {"via": "python"}
    return request


def _probe(session, request):
    """Probe the saved request, preserving an intentionally omitted read set."""
    body = {key: copy.deepcopy(value) for key, value in request.items()
            if key not in {"base", "reads", "merge", "commands", "key", "origin", "imports"}}
    body.update(api_version=1, project_id=session.project_id, timeline_id=session.timeline_id,
                commands=copy.deepcopy(request["commands"]), merge=request["merge"], dry_run=True)
    if "reads" in request:
        body["reads"] = copy.deepcopy(request["reads"])
    body.setdefault("source", {"via": "python"})
    try:
        remote = getattr(session.client, "_remote", None)
        transport = getattr(remote, "_transport", None)
        generated = getattr(transport, "_generated", None)
        raw_request = getattr(generated, "_request", None)
        if callable(raw_request):
            # The generated CommitPreview DTO only admits accepted/merged
            # previews. A conflict preview is valid for retry and must reach
            # the re-derive branch instead of becoming invalid_response.
            path = (f"/v1/projects/{quote(session.project_id, safe='')}"
                    f"/timelines/{quote(session.timeline_id, safe='')}/commit")
            _, _, payload = raw_request(
                "POST", path,
                body=json.dumps(body, separators=(",", ":"), allow_nan=False).encode(),
                headers={"Content-Type": "application/json",
                         "Idempotency-Key": "clash-probe-" + uuid.uuid4().hex})
            return generated._json(payload)["data"]
        return _response(session.client.timelines.commit(
            session.project_id, session.timeline_id, body,
            idempotency_key="clash-probe-" + uuid.uuid4().hex))["data"]
    except Exception as exc:  # noqa: BLE001 - retain Runtime refusal details
        details = getattr(exc, "details", None)
        if isinstance(details, dict) and details:
            return exc.details
        raise


def _preview_diff(timeline, data, evaluated_head):
    """Diff the canonical preview document against its evaluated head."""
    document = data.get("canonical_document")
    if not isinstance(document, dict):
        raise ValueError("retry preview did not include canonical_document")
    from .commit import bundle_from_document
    from .emitter import _diff, _payload_for_emit, _root_pairs
    from .store import fetch_bundle

    before = fetch_bundle(timeline.session.project_id, timeline.session.timeline_id,
                          revision_id=evaluated_head["revision_id"],
                          publication_id=evaluated_head["publication_id"],
                          client=timeline.session.client)
    after = bundle_from_document(document)
    changes = []
    for ref, old, new in _root_pairs(before, after):
        _diff(_payload_for_emit(ref, old), _payload_for_emit(ref, new), ref, (), changes)
    if not changes:
        changes = [{"op": command["op"], "ref": command.get("select"),
                    "args": copy.deepcopy(command["args"])}
                   for command in data.get("commands", [])]
    return {"changes": changes}


def _summary_rederive(record, packet):
    label = record.get("label") or "Timeline edit"
    receipts = packet.get("receipts") or []
    receipt = next((item for item in receipts if item.get("touches_conflict")), None)
    conflicts = ((record.get("failure") or {}).get("details") or {}).get("conflicts", [])
    conflict = conflicts[0] if conflicts else {}
    path = "/".join(map(str, conflict.get("path", [])))
    ref = str(conflict.get("ref", "the changed part")).rsplit("/", 1)[-1]
    if ":" in ref:
        kind, identity = ref.split(":", 1)
        ref = f"{kind} {identity}"
    site = ref + (f' ({path})' if path else "")
    cause = "the timeline changed"
    if receipt:
        cause = f'"{receipt.get("label") or "Another edit"}"'
        if receipt.get("publisher"):
            cause += f' ({receipt["publisher"]})'
        cause += f' changed {site}'
    return (f'"{label}" can no longer apply as reviewed: {cause}. '
            f'Run what produced the list again on the newest timeline, preview it, then commit it '
            f'with pending="{record["id"]}".')


def retry(timeline, ref, fn=None, *, overwrite=False):
    """Retry a saved record, returning a reviewable preview or terminal state."""
    if fn is None and callable(getattr(ref, "retry_fn", None)):
        fn = ref.retry_fn
    path, record = _record(timeline, ref)
    if record.get("state") not in {"pending", "landed"}:
        return {"status": "refused", "pending_id": record.get("id"),
                "summary": f'Cannot retry a pending change in state {record.get("state")!r}.',
                "next": None}
    landed = _landed(timeline, path, record)
    if landed is not None:
        return landed
    if record.get("state") == "landed":
        return _landed(timeline, path, record)
    if fn is not None:
        refreshed = _refresh_function_base(timeline, record)
        part = _part(record)
        original_base = None if overwrite else _pin(part["base"])
        options = part.get("commit_options") or {}
        result = timeline.commit(fn, label=record.get("label"), key=record.get("key"),
                                 pending=record["id"], reads=options.get("reads"),
                                 _function_base=original_base)
        receipt = result.get("receipt") if isinstance(result, dict) else None
        receipt_id = receipt.get("receipt_id") if isinstance(receipt, dict) else None
        if refreshed and receipt_id and result.get("status") in {"accepted", "merged", "rebased"}:
            label = record.get("label") or "Timeline edit"
            result["summary"] = (f'Committed "{label}" as {receipt_id} after re-running it on the '
                                 f'newest timeline; {record["id"]} is closed.')
            if isinstance(result.get("data"), dict):
                result["data"]["summary"] = result["summary"]
        if overwrite and receipt_id:
            result["rebased"] = True
            result["summary"] = result.get("summary", "").rstrip(".") + "; rebased onto the newest timeline."
            if isinstance(result.get("data"), dict):
                result["data"]["rebased"] = True
                result["data"]["summary"] = result["summary"]
        return result

    if overwrite:
        raise ValueError("overwrite requires the original edit function")

    part = _part(record)
    request = _request(record, part)
    data = _probe(timeline.session, request)
    details = data.get("details", data) if isinstance(data, dict) else {}
    status = data.get("would_status", data.get("status", details.get("status")))
    if status in {"accepted", "merged"}:
        head = data.get("evaluated_head")
        if not isinstance(head, dict) or not head.get("revision_id") or not head.get("publication_id"):
            raise ValueError("retry preview did not include an evaluated_head")
        head = _pin(head)
        token_data = json.dumps([record["id"], record.get("attempts", 1), head],
                                sort_keys=True, separators=(",", ":")).encode()
        token = hashlib.sha256(token_data).hexdigest()
        label = record.get("label") or "Timeline edit"
        result = {"status": "preview", "pending_id": record["id"],
                  "data": {"commands": copy.deepcopy(part["commands"]),
                           "diff": _preview_diff(timeline, data, head), "head": head,
                           "retry": {"pending_id": record["id"], "token": token}},
                  "summary": f'"{label}" still applies to the newest timeline. Show this diff to '
                             "whoever approves it, then commit.",
                  "next": "tl.commit(r)",
                  "_retry_request": request, "_retry_path": str(path), "_retry_token": token,
                  "_retry_record_rev": record.get("rev"), "_retry_attempts": record.get("attempts", 1),
                  "_retry_record_digest": _record_digest(record)}
        return result
    if status == "conflict":
        packet = clash.explain(timeline.session, record)
        return {"status": "re_derive", "pending_id": record["id"],
                "data": {"conflicts": copy.deepcopy(details.get("conflicts", [])),
                         "receipts": copy.deepcopy(packet.get("receipts"))},
                "summary": _summary_rederive(record, packet),
                "next": (f'preview = tl.commit(make_edit, label={record.get("label")!r}, dry_run=True); '
                         f'tl.commit(preview["data"]["commands"], label={record.get("label")!r}, '
                         f'key={record.get("key")!r}, pending={record["id"]!r})')}
    message = data.get("message") or details.get("message") or details.get("reason") or "The Runtime refused this edit."
    return {"status": "refused", "pending_id": record["id"], "data": copy.deepcopy(data),
            "summary": str(message), "next": f'tl.retry({record["id"]!r})'}


def commit_preview(timeline, result):
    """Durably send the exact base-B request represented by a retry preview."""
    if not isinstance(result, dict) or result.get("status") != "preview" or "_retry_request" not in result:
        raise ValueError("commit_preview requires a retry preview returned by retry()")
    request = copy.deepcopy(result["_retry_request"])
    pending_id = result["pending_id"]
    path = result["_retry_path"]
    token = result.get("data", {}).get("retry", {}).get("token")
    if token != result.get("_retry_token"):
        raise ValueError("retry preview token is stale or invalid")
    current = next((record for record_path, record in timeline._pending_records_with_paths("all")
                    if record.get("id") == pending_id and str(record_path) == path), None)
    if current is not None:
        landed = _landed(timeline, Path(path), current)
        if landed is not None:
            return landed
    if (current is None or current.get("state") != "pending"
            or current.get("rev") != result.get("_retry_record_rev")
            or current.get("attempts", 1) != result.get("_retry_attempts")
            or _record_digest(current) != result.get("_retry_record_digest")):
        raise ValueError("pending change changed after this retry preview; preview it again")
    check = json.dumps([pending_id, result["_retry_attempts"], result["data"]["head"]],
                       sort_keys=True, separators=(",", ":")).encode()
    if hashlib.sha256(check).hexdigest() != token:
        raise ValueError("retry preview token is stale or invalid")
    with timeline.session.outbox.locked():
        expected = timeline.session._state()
    part = _part(current)
    expected_request = _request(current, part)
    if request != expected_request:
        raise ValueError("retry preview request no longer matches its saved part; preview it again")
    options = {key: copy.deepcopy(request[key]) for key in ("merge", "reads") if key in request}
    group_id = request.get("group_id", current["id"])
    try:
        submitted = timeline.session.submit(
            request["commands"], label=request["label"], steps=request.get("steps", []),
            merge=options.get("merge", "fields"), reads=options.get("reads"),
            idempotency_key=str(uuid.uuid4()),
            logical_key=current["key"], group_id=group_id,
            rationale=copy.deepcopy(request.get("rationale")),
            imports=copy.deepcopy(part.get("imports", [])),
            expected_state=expected, base={"revision_id": request["base_revision_id"],
                                            "publication_id": request["base_publication_id"]},
            pending_id=pending_id, pending_path=path, pending_how="retry")
        return timeline._accepted(submitted)
    except Exception as exc:
        # Timeline.commit() reconciles durable unknown outcomes on the next call.
        if getattr(exc, "failure", {}).get("details", {}).get("status") != "conflict":
            raise
        landed = _landed(timeline, Path(path), current)
        if landed is not None:
            return landed
        raise
