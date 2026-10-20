"""Capture the existing native media-swap command through a TimelineSession."""
from __future__ import annotations

import copy
import re
from collections.abc import Mapping

from astrid.core.receipts.contract import CommandReceipt

from .contracts import DomainResult, ErrorObject

_OBJECT_ID = re.compile(r"sha256:[0-9a-f]{64}")
_SELECTION_KEYS = ("asset", "generation_id", "variant_id", "object_id", "catalog_digest")


class _SelectionHold(ValueError):
    """The public locator cannot be resolved to one immutable media selection."""


def _failure(message, *, key, details=None, code="validation_error"):
    return DomainResult.failure(
        ErrorObject(code, message, details or {}),
        idempotency_key=key if isinstance(key, str) else "",
    )


def _plain(value):
    if isinstance(value, Mapping):
        if set(value) >= {"data", "receipt"}:
            value = value["data"]
        return dict(value)
    if hasattr(value, "__dict__"):
        return dict(value.__dict__)
    return value


def _read(transport, operation, *args):
    """Use the typed transport when present, otherwise its generated read."""
    reader = getattr(transport, operation, None)
    if not callable(reader):
        generated = getattr(transport, "_generated", None)
        reader = getattr(generated, operation, None)
    if not callable(reader):
        raise _SelectionHold(f"Runtime does not expose exact {operation} media reads")
    try:
        return _plain(reader(*args))
    except Exception as exc:  # generated clients expose stable error attributes
        message = getattr(exc, "message", str(exc))
        raise _SelectionHold(f"exact {operation} media read failed: {message}") from exc


def _selection(transport, project_id, pin):
    if not isinstance(pin, Mapping) or set(pin) != {
            "asset", "generation_id", "variant_id", "object_id", "catalog_digest"}:
        raise _SelectionHold("native media replacement requires one complete immutable media selection")
    selector = {key: pin[key] for key in ("asset", "generation_id", "variant_id")}
    resolved = _read(transport, "get_project_media_selection", project_id, selector)
    if not isinstance(resolved, Mapping) or dict(resolved) != dict(pin):
        raise _SelectionHold("managed media selection changed while it was being resolved")
    verified = _read(transport, "get_project_verified_media", project_id, dict(pin))
    if not isinstance(verified, Mapping) or verified.get("selection") != dict(pin):
        raise _SelectionHold("managed media verification does not match the immutable selection")
    return dict(pin), dict(verified)


def _selection_for_selector(transport, project_id, selector):
    selected = _read(transport, "get_project_media_selection", project_id, dict(selector))
    if not isinstance(selected, Mapping):
        raise _SelectionHold("Runtime returned an invalid immutable media selection")
    return _selection(transport, project_id, selected)


def _paged_read(transport, operation, project_id):
    reader = getattr(transport, operation, None)
    if not callable(reader):
        generated = getattr(transport, "_generated", None)
        reader = getattr(generated, operation, None)
    if not callable(reader):
        raise _SelectionHold(f"Runtime does not expose exact {operation} media reads")
    cursor = None
    rows = []
    seen = set()
    while True:
        try:
            page = _plain(reader(project_id, cursor=cursor, limit=50))
        except Exception as exc:
            message = getattr(exc, "message", str(exc))
            raise _SelectionHold(f"exact {operation} media read failed: {message}") from exc
        if isinstance(page, Mapping):
            items, next_cursor = page.get("items"), page.get("next_cursor")
        elif isinstance(page, (list, tuple)) and len(page) == 2:
            items, next_cursor = page
        else:
            raise _SelectionHold(f"Runtime returned an invalid {operation} media page")
        if not isinstance(items, list) or (next_cursor is not None and not isinstance(next_cursor, str)):
            raise _SelectionHold(f"Runtime returned an invalid {operation} media page")
        rows.extend(_plain(item) for item in items)
        if next_cursor is None:
            return rows
        if not next_cursor or next_cursor in seen:
            raise _SelectionHold(f"Runtime returned a cyclic {operation} media page")
        seen.add(next_cursor)
        cursor = next_cursor


def _selection_for_object(transport, project_id, object_id):
    """Resolve an object identity exactly; never choose a current/gallery item."""
    if not isinstance(object_id, str) or not _OBJECT_ID.fullmatch(object_id):
        raise _SelectionHold("source_object_id must be a canonical sha256 object id")
    candidates = []
    for generation in _paged_read(transport, "list_generations", project_id):
        if not isinstance(generation, Mapping):
            continue
        generation_id = generation.get("generation_id")
        if not isinstance(generation_id, str) or not generation_id:
            continue
        for variant in _paged_read(transport, "list_variants", generation_id):
            if not isinstance(variant, Mapping) or variant.get("object_id") != object_id:
                continue
            variant_id = variant.get("variant_id")
            if isinstance(variant_id, str) and variant_id:
                candidates.append({
                    "asset": variant_id, "generation_id": generation_id,
                    "variant_id": variant_id, "object_id": object_id,
                })
    if len(candidates) != 1:
        raise _SelectionHold(
            "source_object_id does not identify exactly one immutable managed-media selection"
        )
    return _selection_for_selector(transport, project_id, {
        key: candidates[0][key] for key in ("asset", "generation_id", "variant_id")
    })


def _publication_for_head(timelines, project_id, timeline_id, revision_id):
    cursor = None
    seen = set()
    while True:
        result = timelines._typed(
            "list_timeline_commits", project_id, timeline_id, cursor=cursor, limit=50
        )
        if not result.ok or not isinstance(result.data, Mapping):
            raise _SelectionHold("the expected parent head has no readable publication identity")
        page = result.data
        for row in page.get("items", ()):
            if isinstance(row, Mapping) and row.get("revision_id") == revision_id:
                publication = row.get("publication_id")
                if isinstance(publication, str) and publication:
                    return publication
                receipt = row.get("receipt")
                if isinstance(receipt, Mapping) and isinstance(receipt.get("receipt_id"), str):
                    return receipt["receipt_id"]
        cursor = page.get("next_cursor")
        if cursor is None:
            break
        if not isinstance(cursor, str) or not cursor or cursor in seen:
            break
        seen.add(cursor)
    raise _SelectionHold("the expected parent head has no readable publication identity")


def _target_pin(bundle, owner, clip_id):
    from .timeline._command_state import State

    state = State(bundle)
    clip = state.entity(owner + "/clip:" + clip_id)
    if not isinstance(clip, Mapping) or not isinstance(clip.get("asset"), str):
        raise _SelectionHold("selected clip has no exact authored asset identity")
    binding = state.entity(owner + "/asset:" + clip["asset"])
    if not isinstance(binding, Mapping):
        raise _SelectionHold("selected clip has no exact authored managed-media binding")
    generation_id = binding.get("generationId", binding.get("generation_id"))
    variant_id = binding.get("variantId", binding.get("variant_id"))
    object_id = binding.get("media_id", binding.get("object_id"))
    if not all(isinstance(value, str) and value for value in (generation_id, variant_id, object_id)):
        raise _SelectionHold("selected clip's authored media binding is not immutable and complete")
    return {
        "asset": clip["asset"], "generation_id": generation_id,
        "variant_id": variant_id, "object_id": object_id,
    }


def _domain(result, key):
    data = result.get("data") if isinstance(result, Mapping) else None
    receipt = result.get("receipt") if isinstance(result, Mapping) else None
    if not isinstance(data, Mapping) or not isinstance(receipt, Mapping):
        return _failure("Runtime returned an invalid native timeline acknowledgement", key=key,
                        code="protocol_error")
    try:
        receipt = CommandReceipt.from_dict(receipt)
    except (TypeError, ValueError) as exc:
        return _failure("Runtime returned an invalid native timeline receipt", key=key,
                        details={"reason": str(exc)}, code="protocol_error")
    return DomainResult.success(
        dict(data), receipt=receipt,
        idempotency_key=key if key is not None else receipt.idempotency_key,
    )


def _pending_matches(command, *, owner, clip_id, source_object_id, old_media, media):
    """Prove that one persisted swap is this caller's logical request."""
    expected_select = owner + "/clip:" + clip_id
    expected_intent = {"ownership": "parent" if owner == "parent" else "occurrence"}
    if not isinstance(command, Mapping) or command.get("select") != expected_select:
        return False
    if command.get("op") != ("clip.swap-media" if owner == "parent" else "occurrence.swap-media"):
        return False
    if command.get("intent") != expected_intent:
        return False
    args = command.get("args")
    if not isinstance(args, Mapping) or set(args) != {"old_media", "media"}:
        return False
    original_old, original_new = args["old_media"], args["media"]
    for pin in (original_old, original_new):
        if not isinstance(pin, Mapping) or set(pin) != set(_SELECTION_KEYS):
            return False
    if original_new["object_id"] != source_object_id or original_old["object_id"] == source_object_id:
        return False
    if isinstance(old_media, Mapping) or isinstance(media, Mapping):
        if not isinstance(old_media, Mapping) or not isinstance(media, Mapping):
            return False
        if dict(old_media) != dict(original_old) or dict(media) != dict(original_new):
            return False
    return True


def replace_selected_media(timelines, project, ref, *, occurrence_id, clip_id, source_object_id,
                           expected_head, expected_publication=None, old_media=None, media=None,
                           idempotency_key):
    """Capture one exact native swap and flush it through a durable session."""
    key = idempotency_key
    if key is not None and (not isinstance(key, str) or not key):
        return _failure("native media replacement requires an idempotency key", key=key or "")
    if not all(isinstance(value, str) and value.strip()
               for value in (project, ref, clip_id, source_object_id, expected_head)):
        return _failure("native media replacement requires exact project, locator and head", key=key)
    if occurrence_id is not None and (not isinstance(occurrence_id, str) or not occurrence_id.strip()):
        return _failure("native media replacement requires an exact occurrence id", key=key)
    if not _OBJECT_ID.fullmatch(source_object_id):
        return _failure("source_object_id must be a canonical sha256 object id", key=key)

    try:
        from types import SimpleNamespace

        from .timeline.native_occurrence_media_commands import (
            capture_occurrence_swap_media,
            capture_parent_swap_media,
        )
        from .timeline.sync import TimelineSession

        session_client = SimpleNamespace(
            timelines=timelines.__class__(timelines._client),
            _remote=SimpleNamespace(_transport=timelines._client),
        )
        # Opening without a supplied base lets a persisted flight be retried
        # without reading a new head or recapturing media selections.
        session = TimelineSession.open(
            project,
            ref,
            client=session_client,
            **({
                "base_revision_id": expected_head,
                "base_publication_id": expected_publication,
            } if expected_publication else {}),
        )
        state = session._state()
        pending = state.get("pending") or []
        if pending or state.get("flight") is not None:
            if state["base"] != {
                "revision_id": expected_head,
                "publication_id": state["base"].get("publication_id")
                if expected_publication is None else expected_publication,
            }:
                raise _SelectionHold("pending native replacement belongs to a different expected head")
            if (len(pending) != 1 or not isinstance(pending[0], Mapping)
                    or pending[0].get("op") not in {"occurrence.swap-media", "clip.swap-media"}):
                raise _SelectionHold("another native edit is already pending in this timeline session")
            owner = "parent" if occurrence_id is None else "occurrence:" + occurrence_id
            if not _pending_matches(
                    pending[0], owner=owner, clip_id=clip_id,
                    source_object_id=source_object_id, old_media=old_media, media=media):
                raise _SelectionHold("pending native replacement does not match this exact request")
            return _domain(session.flush(idempotency_key=key), key)

        project_id, timeline_id = session.project_id, session.timeline_id
        publication_id = expected_publication or (
            state["base"]["publication_id"] if state["base"]["revision_id"] == expected_head else None
        )
        if publication_id is None:
            publication_id = _publication_for_head(timelines, project_id, timeline_id, expected_head)
        if state["base"] != {"revision_id": expected_head, "publication_id": publication_id}:
            session = TimelineSession.open(
                project, ref, client=session_client,
                base_revision_id=expected_head, base_publication_id=publication_id,
            )
            state = session._state()
        bundle = session._bundle(state)
        owner = "parent" if occurrence_id is None else "occurrence:" + occurrence_id
        target = _target_pin(bundle, owner, clip_id)
        transport = timelines._client
        old_pin, old_verified = _selection_for_selector(
            transport, project_id,
            {key: target[key] for key in ("asset", "generation_id", "variant_id")},
        )
        if old_pin["object_id"] != target["object_id"]:
            raise _SelectionHold("selected clip's managed-media binding changed")
        if isinstance(media, Mapping) or isinstance(old_media, Mapping):
            if not isinstance(old_media, Mapping) or not isinstance(media, Mapping):
                raise _SelectionHold("native media replacement requires both exact media selections")
            old_pin, old_verified = _selection(transport, project_id, old_media)
            new_pin, new_verified = _selection(transport, project_id, media)
        else:
            new_pin, new_verified = _selection_for_object(transport, project_id, source_object_id)
        if any(old_pin[key] != target[key] for key in target):
            raise _SelectionHold("provided old media selection does not match the authored clip")
        if new_pin["object_id"] != source_object_id:
            raise _SelectionHold("managed media selection does not match source_object_id")
        if old_pin["object_id"] == new_pin["object_id"]:
            raise _SelectionHold("native media replacement requires a changed managed-media object")
        select = owner + "/clip:" + clip_id
        verified = [old_verified, new_verified]
        if owner == "parent":
            command = capture_parent_swap_media(bundle, select, old_pin, new_pin, verified_media=verified)
        else:
            command = capture_occurrence_swap_media(bundle, select, old_pin, new_pin, verified_media=verified)

        with session.outbox.locked():
            current = session._state()
            if current != state:
                raise _SelectionHold("timeline session changed while native media intent was captured")
            current["pending"] = [copy.deepcopy(command)]
            session.outbox.write(current)
        return _domain(session.flush(idempotency_key=key), key)
    except _SelectionHold as exc:
        return _failure(str(exc), key=key)
    except Exception as exc:  # noqa: BLE001 - preserve the DomainResult boundary
        details = getattr(exc, "details", {})
        if not isinstance(details, Mapping):
            details = {}
        return _failure(str(getattr(exc, "message", exc)), key=key,
                        details=dict(details), code=getattr(exc, "code", "validation_error"))
