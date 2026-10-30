"""Retry durable timeline edits saved after a conflict."""
from __future__ import annotations

import copy
import hashlib
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path

from . import clash
from .outbox import Outbox


def _pin(value):
    return {"revision_id": value["revision_id"], "publication_id": value["publication_id"]}


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


def _close(path, record, session, publication, how):
    outbox = session.outbox if Path(path) == Path(session.outbox.path) else Outbox(Path(path))
    with outbox.locked():
        state = outbox.read()
        saved = state.get("pending_changes", {}).get(record["id"]) if isinstance(state, dict) else None
        if saved is None:
            return record
        if saved.get("state") == "pending":
            saved["state"] = "landed"
            saved["rev"] = int(saved.get("rev", 0)) + 1
            saved["updated_at"] = datetime.now(timezone.utc).isoformat()
            saved["closed_by"] = {"actor_id": session.identity["actor_id"],
                                   "publication_id": publication, "how": how}
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
    entry = next((item for item in entries if item.get("group_id") == record["id"]), None)
    if entry is None:
        return None
    publication = entry.get("publication_id")
    if publication is None:
        publication = entry.get("receipt", {}).get("receipt_id")
    closed = _close(path, record, timeline.session, publication, "retry")
    actor = entry.get("publisher")
    label = record.get("label") or "Timeline edit"
    suffix = f" (by {actor})" if actor else ""
    return {"status": "landed", "pending_id": record["id"], "data": {"publication_id": publication},
            "summary": f'"{label}" already landed as {publication}{suffix}; '
                       f'{record["id"]} is closed. Nothing was sent.', "next": None,
            "record": closed}


def _part(record):
    parts = record.get("parts") or []
    index = record.get("part", 0)
    if type(index) is not int or index < 0 or index >= len(parts):
        raise ValueError("pending change has no retryable part")
    return parts[index]


def _request(record, part):
    options = copy.deepcopy(part.get("commit_options") or {})
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
    request["source"] = {"via": "python"}
    return request


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


def retry(timeline, ref, fn=None):
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
        result = timeline.commit(fn, label=record.get("label"), key=record.get("key"), pending=record["id"])
        publication = result.get("receipt", {}).get("receipt_id")
        return {"status": "landed", "pending_id": record["id"], "data": result.get("data", {}),
                "summary": f'Committed "{record.get("label") or "Timeline edit"}" as {publication} '
                           f'after re-running it on the newest timeline; {record["id"]} is closed.',
                "next": None, "result": result}

    part = _part(record)
    request = _request(record, part)
    data = clash._probe(timeline.session, request, request["merge"], request.get("reads"))
    details = data.get("details", data) if isinstance(data, dict) else {}
    status = data.get("would_status", data.get("status", details.get("status")))
    if status in {"accepted", "merged"}:
        head = data.get("head") or details.get("current") or record.get("head") or part["base"]
        token_data = json.dumps([record["id"], record.get("attempts", 1), _pin(head)],
                                sort_keys=True, separators=(",", ":")).encode()
        token = hashlib.sha256(token_data).hexdigest()
        label = record.get("label") or "Timeline edit"
        result = {"status": "preview", "pending_id": record["id"],
                  "data": {"commands": copy.deepcopy(part["commands"]),
                           "diff": copy.deepcopy(data.get("diff", [])), "head": _pin(head),
                           "retry": {"pending_id": record["id"], "token": token}},
                  "summary": f'"{label}" still applies to the newest timeline. Show this diff to '
                             "whoever approves it, then commit.",
                  "next": "tl.commit(r)",
                  "_retry_request": request, "_retry_path": str(path), "_retry_token": token}
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
    with timeline.session.outbox.locked():
        expected = timeline.session._state()
    options = {key: copy.deepcopy(request[key]) for key in ("steps", "merge", "reads") if key in request}
    options["steps"] = options.get("steps", [])
    try:
        return timeline.session.submit(
            request["commands"], label=request["label"], steps=options["steps"],
            merge=options.get("merge", "fields"), reads=options.get("reads"),
            idempotency_key="timeline-retry-" + uuid.uuid4().hex,
            expected_state=expected, base={"revision_id": request["base_revision_id"],
                                            "publication_id": request["base_publication_id"]},
            pending_id=pending_id, pending_path=path, pending_how="retry")
    except Exception:
        # Timeline.commit() reconciles durable unknown outcomes on the next call.
        raise
