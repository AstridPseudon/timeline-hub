"""Lossless bundle-to-``doc.patch`` translation.

The emitter is deliberately a small, structural adapter.  It does not execute
patches, resolve closure aliases, or guess semantic commands; those jobs belong
to the provider.  In particular, changes to closure membership and provenance
are refused instead of being represented as a root replacement.
"""
from __future__ import annotations

import copy
from collections.abc import Mapping
from typing import Any

from ._command_state import equal, present
from ._common import TimelineEditError


class DocumentPatchError(TimelineEditError):
    """A document change cannot be represented as a safe generic patch."""


# Kept as a discoverable name for callers migrating from the detached adapter.
DocumentEmitterError = DocumentPatchError
_MISSING = object()


def _state(value: Any) -> dict[str, Any]:
    if value is _MISSING:
        return {"state": "absent"}
    return present(value)


def _path(path: tuple[str, ...] | list[str]) -> list[str]:
    if not all(isinstance(token, str) for token in path):
        raise DocumentPatchError("doc.patch paths contain string tokens only")
    return list(path)


def _identity_key(rows: list[Any], path: tuple[str, ...]) -> str | None:
    """Return the schema-level identity convention available to this bundle.

    Authoring collections use ``id``; the closure's occurrence collection uses
    ``occurrence_id``.  Anything else is intentionally treated as an id-less
    array and is replaced as one guarded value.
    """
    if path and path[-1] == "occurrences":
        key = "occurrence_id"
    else:
        key = "id"
    if not rows or not all(isinstance(row, Mapping) and isinstance(row.get(key), str)
                           and bool(row[key]) for row in rows):
        return None
    identities = [row[key] for row in rows]
    return key if len(set(identities)) == len(identities) else None


def _ref_for_internal(bundle: Mapping[str, Any], shot_id: str, shot: Mapping[str, Any]) -> str:
    source = bundle.get("source_mapping")
    source_shots = source.get("shots", {}) if isinstance(source, Mapping) else {}
    source_row = source_shots.get(shot_id) if isinstance(source_shots, Mapping) else None
    for value in (
        shot.get("internal_timeline_id"),
        source_row.get("internal_timeline_id") if isinstance(source_row, Mapping) else None,
        bundle.get("timeline_id"),
        "main",
    ):
        if isinstance(value, str) and value:
            return "internal:" + value
    raise DocumentPatchError(f"shot {shot_id!r} has no verified internal timeline identity")


def _protected(ref: str, path: tuple[str, ...]) -> bool:
    """Reject fields whose meaning is a managed closure edge or immutable pin."""
    if not path:
        return False
    if ref == "parent" and path[0] == "occurrences":
        # Occurrence membership and shot pins are semantic closure operations.
        if len(path) == 1 or "occurrence_id:" in path:
            return True
    if ref.startswith("internal:") and path[:1] in (("internal_timeline_revision_id",),):
        return True
    if any(token in {"revision_id", "content_digest", "shot_revision_id", "internal_timeline_revision_id"}
           for token in path):
        return True
    return False


def _change(op: str, ref: str, path: tuple[str, ...], before: Any, value: Any = _MISSING) -> dict[str, Any]:
    if _protected(ref, path):
        raise DocumentPatchError(
            f"{ref}/{'.'.join(path) or '<root>'} is a managed closure edge; use its semantic command"
        )
    change: dict[str, Any] = {"op": op, "ref": ref, "path": _path(path), "before": _state(before)}
    if op == "set":
        if value is _MISSING:
            raise DocumentPatchError("doc.patch set requires a value")
        change["value"] = copy.deepcopy(value)
    return change


def _list_changes(before: list[Any], after: list[Any], ref: str, path: tuple[str, ...], out: list[dict[str, Any]]) -> None:
    if _protected(ref, path):
        raise DocumentPatchError(
            f"{ref}/{'.'.join(path) or '<root>'} membership/order is managed; use its semantic command"
        )
    key = _identity_key(before or after, path)
    if key is None:
        out.append(_change("set", ref, path, before, after))
        return

    old = {row[key]: row for row in before}
    new = {row[key]: row for row in after}
    current = list(before)
    current_ids = [row[key] for row in current]
    target_ids = [row[key] for row in after]

    # Remove from the end so every order_before is the exact sequential order.
    for identity in reversed(current_ids):
        if identity not in new:
            order = [row[key] for row in current]
            out.append({"op": "list.remove", "ref": ref, "path": _path(path), "id": identity,
                        "before": present(copy.deepcopy(old[identity])), "order_before": order})
            current.pop(current_ids.index(identity))
            current_ids.remove(identity)

    # Insert in target order.  The predecessor is already present because the
    # target prefix is built left-to-right.
    for index, identity in enumerate(target_ids):
        if identity in current_ids:
            continue
        order = [row[key] for row in current]
        after_id = target_ids[index - 1] if index else None
        out.append({"op": "list.insert", "ref": ref, "path": _path(path), "id": identity,
                    "before": {"state": "absent"}, "order_before": order,
                    "after_id": after_id, "value": copy.deepcopy(new[identity])})
        insert_at = current_ids.index(after_id) + 1 if after_id is not None else 0
        current.insert(insert_at, copy.deepcopy(new[identity]))
        current_ids.insert(insert_at, identity)

    # Then make order match.  Move operations compare the complete item at its
    # current position, not the target item after a later content edit.
    for index, identity in enumerate(target_ids):
        if current_ids[index] == identity:
            continue
        old_index = current_ids.index(identity)
        row = copy.deepcopy(current[old_index])
        order = list(current_ids)
        out.append({"op": "list.move", "ref": ref, "path": _path(path), "id": identity,
                    "before": present(row), "order_before": order,
                    "after_id": target_ids[index - 1] if index else None})
        moved = current.pop(old_index)
        current_ids.pop(old_index)
        insert_at = current_ids.index(target_ids[index - 1]) + 1 if index else 0
        current.insert(insert_at, moved)
        current_ids.insert(insert_at, identity)

    # Compare item contents after structural operations.  The identity token is
    # not writable, so it is deliberately omitted from the recursive path.
    for identity in target_ids:
        if identity not in old:
            continue
        _diff(old[identity], new[identity], ref,
              path + (f"{key}:{identity}",), out, identity_token=key)


def _diff(before: Any, after: Any, ref: str, path: tuple[str, ...], out: list[dict[str, Any]], *, identity_token: str | None = None) -> None:
    if equal(before, after):
        return
    if before is _MISSING or after is _MISSING:
        if after is _MISSING:
            out.append(_change("remove", ref, path, before))
        else:
            out.append(_change("set", ref, path, before, after))
        return
    if isinstance(before, Mapping) and isinstance(after, Mapping):
        for key in sorted(set(before) | set(after)):
            if not isinstance(key, str):
                raise DocumentPatchError("doc.patch object keys must be strings")
            _diff(before.get(key, _MISSING), after.get(key, _MISSING), ref,
                  path + (key,), out)
        return
    if isinstance(before, list) and isinstance(after, list):
        _list_changes(before, after, ref, path, out)
        return
    out.append(_change("set", ref, path, before, after))


def _roots(bundle: Mapping[str, Any]) -> list[tuple[str, Any, Any]]:
    parent = bundle.get("parent")
    shots = bundle.get("shots")
    if not isinstance(parent, Mapping) or not isinstance(shots, Mapping):
        raise DocumentPatchError("timeline bundle must contain a parent and shot map")
    roots: list[tuple[str, Any, Any]] = [("parent", parent, "parent")]
    for shot_id in sorted(shots):
        shot = shots[shot_id]
        if not isinstance(shot_id, str) or not isinstance(shot, Mapping):
            raise DocumentPatchError("timeline shot roots must be named objects")
        if not isinstance(shot.get("payload"), Mapping) or not isinstance(shot.get("internal_timeline"), Mapping):
            raise DocumentPatchError(f"shot {shot_id!r} has malformed closure payloads")
        roots.append((f"shot:{shot_id}", shot["payload"], shot_id))
        roots.append((_ref_for_internal(bundle, shot_id, shot), shot["internal_timeline"], shot_id))
    return roots


def _outside(bundle: Mapping[str, Any]) -> dict[str, Any]:
    value = copy.deepcopy(dict(bundle))
    value.pop("parent", None)
    shots = value.get("shots")
    if isinstance(shots, dict):
        for shot in shots.values():
            if isinstance(shot, dict):
                shot.pop("payload", None)
                shot.pop("internal_timeline", None)
    return value


def _payload_for_emit(ref: str, payload: Any) -> Any:
    """Hide the authored ``clips`` mirror when it is represented by ``clips``.

    Authoring bundles retain both spellings for compatibility, while the
    provider treats them as one logical collection and regenerates the mirror.
    Emitting both changes would be a duplicate membership operation.
    """
    if ref != "parent" or not isinstance(payload, Mapping):
        return payload
    config = payload.get("config")
    if not isinstance(config, Mapping) or not isinstance(payload.get("clips"), list):
        return payload
    if not equal(payload.get("clips"), config.get("clips", _MISSING)):
        return payload
    value = copy.deepcopy(dict(payload))
    value["config"] = copy.deepcopy(dict(config))
    value["config"].pop("clips", None)
    return value


def emit_document_commands(before_bundle: Mapping[str, Any], after_bundle: Mapping[str, Any]) -> list[dict[str, Any]]:
    """Emit the minimal ordered generic patch for two raw authoring bundles.

    The inputs are copied by the caller-facing G2 seam; this function also
    copies every value placed in a command so later local mutation cannot alter
    the durable request body.
    """
    if not isinstance(before_bundle, Mapping) or not isinstance(after_bundle, Mapping):
        raise DocumentPatchError("document emitter requires mapping bundles")
    if before_bundle.get("project_id") != after_bundle.get("project_id") or before_bundle.get("timeline_id") != after_bundle.get("timeline_id"):
        raise DocumentPatchError("document and Runtime bundle have different project/timeline scope")
    if not equal(_outside(before_bundle), _outside(after_bundle)):
        raise DocumentPatchError("closure membership or provenance changed; use a semantic command")

    def root_map(bundle: Mapping[str, Any]) -> dict[str, list[Any]]:
        result: dict[str, list[Any]] = {}
        for ref, payload, _ in _roots(bundle):
            result.setdefault(ref, []).append(payload)
        return result

    before_root_lists = root_map(before_bundle)
    after_root_lists = root_map(after_bundle)
    if set(before_root_lists) != set(after_root_lists):
        raise DocumentPatchError("closure root creation/removal requires a semantic command")
    before_roots: dict[str, Any] = {}
    after_roots: dict[str, Any] = {}
    for ref in before_root_lists:
        before_list = before_root_lists[ref]
        after_list = after_root_lists[ref]
        if len(before_list) != len(after_list):
            raise DocumentPatchError(f"closure root {ref!r} is ambiguous")
        if len(before_list) > 1:
            if all(equal(left, right) for left, right in zip(before_list, after_list)):
                continue
            raise DocumentPatchError(f"closure root {ref!r} is ambiguous")
        before_roots[ref] = _payload_for_emit(ref, before_list[0])
        after_roots[ref] = _payload_for_emit(ref, after_list[0])
    changes: list[dict[str, Any]] = []
    for ref in before_roots:
        _diff(before_roots[ref], after_roots[ref], ref, (), changes)
    if not changes:
        return []
    return [{"schema_version": 1, "op": "doc.patch", "version": "1", "select": None,
             "args": {"changes": copy.deepcopy(changes)}}]


__all__ = ["DocumentPatchError", "DocumentEmitterError", "emit_document_commands"]
