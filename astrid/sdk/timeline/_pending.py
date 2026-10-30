"""Pure helpers for durable pending timeline changes."""
from __future__ import annotations

import copy
import json
import uuid
from collections.abc import Mapping
from datetime import datetime, timezone


def migrate(state) -> bool:
    """Move a legacy rejected conflict into ``pending_changes`` in-place."""
    if not isinstance(state, dict):
        return False
    rejected = state.get("rejected")
    if not isinstance(rejected, Mapping):
        return False
    failure = rejected.get("failure")
    details = failure.get("details") if isinstance(failure, Mapping) else None
    if not isinstance(details, Mapping) or details.get("status") != "conflict":
        return False
    commands = rejected.get("commands")
    if not isinstance(commands, list):
        return False

    flight = rejected.get("flight")
    body = None
    if isinstance(flight, Mapping) and isinstance(flight.get("body"), str):
        try:
            candidate = json.loads(flight["body"])
            body = candidate if isinstance(candidate, Mapping) else None
        except (TypeError, ValueError):
            body = None
    flight_commands = body.get("commands") if body else None
    if not isinstance(flight_commands, list):
        count = flight.get("count") if isinstance(flight, Mapping) else None
        count = count if isinstance(count, int) and not isinstance(count, bool) else len(commands)
        flight_commands = commands[:count]
    count = flight.get("count") if isinstance(flight, Mapping) else None
    if not isinstance(count, int) or isinstance(count, bool) or count < 0 or count > len(commands):
        count = len(flight_commands)

    evaluation = rejected.get("evaluation")
    origin = "function" if isinstance(evaluation, Mapping) and evaluation.get("kind") == "function" else "list"
    key = flight.get("logical_key", flight.get("key")) if isinstance(flight, Mapping) else None
    if not isinstance(key, str) or not key:
        key = f"clash-{uuid.uuid4().hex[:12]}"
    record_id = f"pc_{uuid.uuid4().hex[:12]}"
    now = datetime.now(timezone.utc).isoformat()
    base = copy.deepcopy(rejected.get("base"))
    first_body = body or {}
    parts = [{
        "base": {"revision_id": first_body.get("base_revision_id"),
                 "publication_id": first_body.get("base_publication_id")}
        if first_body else base,
        "commands": copy.deepcopy(flight_commands),
        "commit_options": copy.deepcopy(rejected.get("commit_options")),
        "rationale": copy.deepcopy(first_body.get("rationale")),
        "media_input": copy.deepcopy(rejected.get("media_input")),
        "imports": copy.deepcopy(flight.get("imports", [])) if isinstance(flight, Mapping) else [],
        "evaluation": copy.deepcopy(evaluation),
    }]
    suffix = commands[count:]
    if suffix:
        parts.append({
            "base": base,
            "commands": copy.deepcopy(suffix),
            "commit_options": copy.deepcopy(rejected.get("commit_options")),
            "rationale": copy.deepcopy(rejected.get("rationale")),
            "media_input": copy.deepcopy(rejected.get("media_input")),
            "imports": [],
            "evaluation": copy.deepcopy(evaluation),
        })

    records = state.setdefault("pending_changes", {})
    if not isinstance(records, dict):
        return False
    records[record_id] = {
        "id": record_id, "state": "pending", "rev": 1,
        "key": key, "key_generated": not bool(flight and flight.get("logical_key")),
        "label": first_body.get("label") or "Timeline edit", "origin": origin,
        "parts": parts, "part": 0,
        "failure": copy.deepcopy(failure),
        "head": copy.deepcopy(details.get("current")),
        "choices": {}, "candidate": None, "flight_fence": None,
        "receipts": [], "versions": [],
        "created_at": now, "updated_at": now, "dropped_reason": None,
    }
    state.pop("rejected", None)
    return True
