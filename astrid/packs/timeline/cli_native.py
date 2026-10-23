"""Thin native-command CLI adapters; schemas and capture stay in the SDK."""
from __future__ import annotations

import copy
import json
import sys
from collections.abc import Mapping
from pathlib import Path

from astrid.core.cli.domain_output import DomainResult, print_result


def _document_error(parsed, exc: Exception, *, code: str | None = None) -> DomainResult:
    """Turn a detached-document refusal into the normal structured CLI error."""
    from astrid.sdk.contracts import ErrorObject

    details = dict(getattr(exc, "details", {}) or {})
    failure = getattr(exc, "failure", None)
    if isinstance(failure, Mapping):
        details = dict(failure.get("details") or details)
        code = code or str(failure.get("code") or "timeline_commit_error")
    details.setdefault("path", "/file")
    details.setdefault("hint", "re-check out the detached document and retry with its exact base pair")
    details.setdefault(
        "suggested_command",
        f"astrid timelines checkout {parsed.ref} --project {parsed.project}",
    )
    return DomainResult.failure(
        ErrorObject(code or str(getattr(exc, "code", "timeline_commit_error")), str(exc), details),
        idempotency_key=parsed.idempotency_key or "",
    )


def _commit_envelope(raw: Mapping[str, object], key: str) -> DomainResult:
    """Preserve the complete Runtime v2 result returned by TimelineSession."""
    from astrid.core.receipts.contract import CommandReceipt

    receipt = raw.get("receipt")
    data = raw.get("data")
    if isinstance(receipt, Mapping):
        committed = CommandReceipt.from_dict(dict(receipt))
        if isinstance(committed.result, Mapping):
            data = dict(committed.result)
        return DomainResult.success(data, receipt=committed, idempotency_key=key)
    return DomainResult.success(data, idempotency_key=key)


def _detached_document(parsed):
    """Load the existing editable bundle format and verify its exact public scope."""
    from astrid.sdk.timeline._common import TimelineEditError
    from astrid.sdk.timeline.store import resolve_ids
    from astrid.sdk.timeline_checkout import Checkout

    checkout = Checkout.load(parsed.file)
    bundle = checkout.stored_document()
    project = bundle.get("project_id")
    timeline = bundle.get("timeline_id")
    base = bundle.get("base_parent")
    if not isinstance(project, str) or not project or not isinstance(timeline, str) or not timeline:
        raise TimelineEditError("unsupported detached document: project_id and timeline_id are required")
    if not isinstance(base, Mapping) or not all(
        isinstance(base.get(key), str) and base[key] for key in ("revision_id", "publication_id")
    ):
        raise TimelineEditError("detached document has no exact base revision/publication pair")
    if not isinstance(bundle.get("parent"), Mapping) or not isinstance(bundle.get("placements"), list):
        raise TimelineEditError("unsupported detached document: expected parent and placements")
    if not isinstance(bundle.get("shots"), Mapping):
        raise TimelineEditError("unsupported detached document: expected a shot map")

    resolved_project, resolved_timeline, _head = resolve_ids(
        parsed.project, parsed.ref, client=parsed.client
    )
    if (resolved_project, resolved_timeline) != (project, timeline):
        raise TimelineEditError(
            "commit scope does not match the detached document "
            f"(file {project}/{timeline}, command {resolved_project}/{resolved_timeline})"
        )
    return checkout, bundle, {key: base[key] for key in ("revision_id", "publication_id")}


def _preview_detached_document(checkout, bundle, base, parsed, *, dry_run: bool):
    """Use the public G2 session commit with the G3 emitter."""
    import copy

    from astrid.sdk.timeline.commit_session import Timeline
    from astrid.sdk.timeline.sync import TimelineSession

    session = TimelineSession.open(
        bundle["project_id"], bundle["timeline_id"], client=parsed.client,
        outbox_path=parsed.file.with_suffix(".outbox.json"),
        base_revision_id=base["revision_id"], base_publication_id=base["publication_id"],
    )
    with session.outbox.locked():
        state = session._state()
    authenticated_base = session._bundle(state)
    if checkout.bundle == authenticated_base:
        return {"data": {"status": "preview" if dry_run else "unchanged",
                          **({"would_status": "unchanged"} if dry_run else {}),
                          "project_id": bundle["project_id"], "timeline_id": bundle["timeline_id"],
                          "label": parsed.message, "commands": [], "steps": [],
                          "merge_mode": "atomic"}, "receipt": None}
    working = Timeline(session, authenticated_base, base)
    working.bundle = copy.deepcopy(checkout.bundle)
    working._refresh()
    return working.commit(
        parsed.message, merge="atomic", dry_run=dry_run,
        idempotency_key=parsed.idempotency_key,
    )


def _replay_document_commit(bundle, base, parsed):
    """Return an exact accepted receipt for a retry, without recapturing or writing."""
    import copy

    from astrid.sdk.timeline.commit import _json
    from astrid.sdk.timeline.emitter import emit_document_commands
    from astrid.sdk.timeline.store import fetch_bundle

    history = parsed.client.timelines.history(bundle["project_id"], bundle["timeline_id"], limit=200)
    if not history.ok or not isinstance(history.data, Mapping):
        return None
    entry = next(
        (row for row in history.data.get("items", [])
         if isinstance(row, Mapping)
         and isinstance(row.get("receipt"), Mapping)
         and row["receipt"].get("idempotency_key") == parsed.idempotency_key),
        None,
    )
    if entry is None:
        return None
    receipt = entry["receipt"]
    result = receipt.get("result")
    records = entry.get("records") if isinstance(entry.get("records"), Mapping) else {}
    label = records.get("label") or (result or {}).get("label") if isinstance(result, Mapping) else None
    canonical = result.get("canonical_document") if isinstance(result, Mapping) else None
    if (not isinstance(result, Mapping) or label != parsed.message
            or not isinstance(canonical, Mapping)
            or canonical.get("project_id") != bundle["project_id"]
            or canonical.get("timeline_id") != bundle["timeline_id"]
            or {"revision_id": result.get("previous_revision_id"),
                "publication_id": result.get("previous_publication_id")} != base):
        raise ValueError("the idempotency key belongs to a different timeline commit")
    authenticated_base = fetch_bundle(
        bundle["project_id"], bundle["timeline_id"],
        revision_id=base["revision_id"], publication_id=base["publication_id"], client=parsed.client,
    )
    candidate = copy.deepcopy(bundle)
    source = authenticated_base.get("source_mapping", {}).get("_runtime_document")
    if source is not None:
        candidate.setdefault("source_mapping", {})["_runtime_document"] = copy.deepcopy(source)
    commands = emit_document_commands(authenticated_base, candidate)
    recorded = records.get("commands") if isinstance(records.get("commands"), list) else result.get("commands")
    if isinstance(recorded, list):
        recorded = [row.get("command", row) if isinstance(row, Mapping) else row for row in recorded]

    def signature(command):
        return {key: copy.deepcopy(command.get(key)) for key in ("op", "args")}

    if not isinstance(recorded, list) or [_json(signature(row)) for row in recorded] != [_json(signature(row)) for row in commands]:
        raise ValueError("the idempotency key belongs to a different timeline commit")
    return {"data": dict(result), "receipt": dict(receipt)}


def commit_document(parsed) -> int:
    """Commit a detached document without making local sidecar or cache writes."""
    from astrid.sdk.timeline._common import TimelineEditError
    from astrid.sdk.workspace_client import WorkspaceClientError

    if not isinstance(parsed.message, str) or not parsed.message.strip():
        result = _document_error(parsed, TimelineEditError("commit message must be nonempty"), code="validation_error")
        return print_result(result, as_json=parsed.json)
    try:
        checkout, bundle, base = _detached_document(parsed)
        replay = _replay_document_commit(bundle, base, parsed)
        if replay is not None and not parsed.dry_run:
            result = _commit_envelope(replay, parsed.idempotency_key)
        elif parsed.dry_run:
            raw = _preview_detached_document(checkout, bundle, base, parsed, dry_run=parsed.dry_run)
            result = _commit_envelope(raw, parsed.idempotency_key)
        else:
            raw = _preview_detached_document(checkout, bundle, base, parsed, dry_run=parsed.dry_run)
            result = _commit_envelope(raw, parsed.idempotency_key)
    except (TimelineEditError, WorkspaceClientError, OSError, ValueError, TypeError, KeyError) as exc:
        result = _document_error(parsed, exc)
    return print_result(result, as_json=parsed.json)


def _render_commit_result(value: object, *, dry_run: bool) -> str:
    if dry_run:
        return "preview only; no publication accepted"
    if not isinstance(value, DomainResult) or not isinstance(value.data, Mapping):
        raise TypeError("native commit renderer received an invalid result envelope")
    data = value.data
    return (f"accepted revision {data['accepted_revision_id']} · publication {data['accepted_publication_id']}\n"
            f"{data['show_command']}")


def ordinary_trim_requested(parsed):
    from astrid.sdk.timeline import store

    if (parsed.client is None or parsed.file or parsed.draft
            or (parsed.trim_in is None and parsed.trim_out is None)):
        return False
    # Route only this family. Compare parser defaults so a new flag cannot
    # silently disappear when an older native adapter sees it.
    accepted = {'project', 'ref', 'clip', 'cut', 'near', 'trim_in', 'trim_out',
                'dry_run', 'idempotency_key', 'json', 'no_sweep'}
    if not all(name in accepted or getattr(parsed, name) == default
               for name, default in parsed.native_trim_defaults.items() if name != 'help'):
        return False
    # Detached work remains authoritative until that ingress is migrated.
    return store.find_draft(parsed.project, parsed.ref, client=parsed.client) is None


def ordinary_move_requested(parsed):
    from astrid.sdk.timeline import store

    if (parsed.client is None or parsed.file or parsed.draft
            or parsed.on is None):
        return False
    try:
        float(parsed.on)
    except (TypeError, ValueError):
        # Symbolic moments (for example, ``after \"Astrid\"``) still need
        # the detached checkout's authored-word resolution.
        return False
    accepted = {'project', 'ref', 'clip', 'cut', 'near', 'on', 'dry_run',
                'idempotency_key', 'json', 'no_sweep'}
    if not all(name in accepted or getattr(parsed, name) == default
               for name, default in parsed.native_trim_defaults.items() if name != 'help'):
        return False
    return store.find_draft(parsed.project, parsed.ref, client=parsed.client) is None


def dispatch_ordinary_edit(parsed):
    """Dispatch the supported ordinary native edit, or leave legacy edits alone."""
    if ordinary_move_requested(parsed):
        result = commit_edit(parsed, edit=commit_move)
        if result is not NotImplemented:
            return result

    if ordinary_trim_requested(parsed):
        result = commit_edit(parsed, edit=commit_trim)
        if result is not NotImplemented:
            return result
    return NotImplemented


def show_native(parsed):
    """Handle the retained native sheet projection, or leave ordinary show alone."""
    if not getattr(parsed, "native", False):
        return NotImplemented
    if getattr(parsed, "presentation", None) != "sheet":
        from astrid.sdk.contracts import ErrorObject

        return print_result(DomainResult.failure(ErrorObject(
            "validation_error", "--native requires --as sheet", {})), as_json=parsed.json)
    from astrid.packs.timeline.cli_show import print_native_sheet

    return print_native_sheet(parsed)


def _trim_selector(bundle, parsed):
    from astrid.core.timeline.cuts import bundle_fps
    from astrid.core.timeline.duration import clip_timeline_duration
    from astrid.sdk.timeline._command_state import State
    from astrid.sdk.timeline_checkout import Checkout

    state = State(bundle)
    if isinstance(parsed.clip, str) and '/clip:' in parsed.clip:
        state.entity(parsed.clip)
        return parsed.clip
    # Reuse the ordinary lookup grammar on a read-only view. Bind each view
    # row to its raw owner explicitly; display IDs never encode ownership.
    view = Checkout({})
    view.bundle = copy.deepcopy(bundle)
    # The lookup mixin also exposes parent-native clips. The synthetic views
    # below represent every owner as a shot, so retain no second parent source.
    view.bundle.update(parent={}, shots={}, placements=[])
    owners = ['parent', *('occurrence:' + row['occurrence_id'] for row in bundle.get('placements', []))]
    bindings = {}
    for owner in owners:
        config = copy.deepcopy(state.config(owner))
        config['clips'] = copy.deepcopy(state.collection(owner, 'clip'))
        for row in config['clips']:
            bindings[id(row)] = owner + '/clip:' + row['id']
        placement = {'start_ms': 0} if owner == 'parent' else copy.deepcopy(state.occurrence(owner).get('placement', {}))
        duration = max((row.get('at', 0) + clip_timeline_duration(row) for row in config['clips']), default=0)
        view.bundle['placements'].append({'shot_id': owner, 'occurrence_id': owner,
                                           'placement': placement, 'duration_ms': duration * 1000})
        view.bundle['shots'][owner] = {'payload': {}, 'internal_timeline': config}
    view.fps = bundle_fps(bundle) or 30
    if parsed.clip is not None:
        clip = view.clip(parsed.clip, near=parsed.near, cut=parsed.cut)
    else:
        cut = int(parsed.cut) if str(parsed.cut).isdigit() else parsed.cut
        clip = view.cut_picture(cut) if isinstance(cut, str) else view.cut(cut).picture
    return bindings[id(clip.data)] if clip is not None else None


def commit_trim(session, parsed, options):
    from astrid.sdk.timeline._command_state import CommandError
    from astrid.sdk.timeline._trim_commands import capture_clip_trim

    with session.outbox.locked():
        state = session._state()
    # Resolve aliases at the original base on retry, never at the newer head
    # or on the already-trimmed local prefix.
    bundle = session._bundle({**state, 'pending': []})
    select = _trim_selector(bundle, parsed)
    if select is None or not select.startswith('parent/clip:'):
        return NotImplemented
    if not state['pending']:
        try:
            command = capture_clip_trim(bundle, select, in_s=parsed.trim_in, out_s=parsed.trim_out)
        except CommandError:
            if parsed.clip == select:  # Explicit native identities report native errors.
                raise
            return NotImplemented
        return session.commit(command, **options)
    return session.trim(select, in_s=parsed.trim_in, out_s=parsed.trim_out, **options)


def commit_move(session, parsed, options):
    from astrid.sdk.timeline._command_state import CommandError

    with session.outbox.locked():
        state = session._state()
    # Resolve aliases against the pinned original head. The native command
    # stores the parent owner in its selection; it never infers ownership from
    # a display id or recaptures it after a lost acknowledgement.
    bundle = session._bundle({**state, 'pending': []})
    select = _trim_selector(bundle, parsed)
    if select is None:
        return NotImplemented
    try:
        return session.move(select, float(parsed.on), **options)
    except CommandError as exc:
        # Legacy occurrence timelines can carry source maps that the native
        # clip.move recipe deliberately does not support.  Let the detached
        # editor retain its owner-resolution path for those maps only; native
        # guard, identity, timing, and authority failures must remain visible.
        if select.startswith('occurrence:') and exc.kind == 'unsupported_map':
            return NotImplemented
        raise


def _verify_commit_selection(session, parsed):
    from types import SimpleNamespace

    from astrid.core.receipts.contract import CommandReceipt
    from astrid.sdk.timeline.revisions import RuntimeRevisions
    from astrid.sdk.workspace_client import WorkspaceClientError

    entries = {}

    def read(project, timeline, **options):
        result = session.client.timelines.history(project, timeline, **options)
        if result.ok and isinstance(result.data, dict):
            entries.update((row["publication_id"], row) for row in result.data["items"])
        return result

    # Reuse the public reader's pinned pagination and complete ancestry checks.
    history = RuntimeRevisions(SimpleNamespace(history=read)).list(
        session.project_id, session.timeline_id, limit=sys.maxsize)
    head = ({"revision_id": history[0].id, "publication_id": history[0].publication_id}
            if history else None)

    def require(condition, message):
        if not condition:
            raise WorkspaceClientError(0, "history_unavailable", message, {
                "path": "/commands/0/args/publications", "head": head,
            })

    ordered = [revision.publication_id for revision in reversed(history or [])
               if revision.publication_id in parsed.commit]
    require(ordered == parsed.commit, "select exact accepted commit receipts, oldest first")
    for publication in parsed.commit:
        entry = entries[publication]
        receipt = CommandReceipt.from_dict(entry["receipt"])
        data, records = receipt.result, entry["records"]
        require(entry["intent"] == "recorded" and isinstance(records, dict)
                and isinstance(data, dict), "selected commit has no guarded accepted history")
        require(receipt.receipt_id == publication and receipt.project_id == session.project_id
                and receipt.command_kind == "timeline.commit"
                and data.get("accepted_revision_id") == entry["revision_id"]
                and data.get("publisher") == entry["publisher"]
                and all(data.get(key) == entry[key] for key in ("provider_version", "compiler_version"))
                and {"revision_id": data.get("previous_revision_id"),
                     "publication_id": data.get("previous_publication_id")} == entry["previous"],
                "selected history does not match its exact accepted receipt")
        document = data.get("canonical_document", {})
        require(document.get("project_id") == session.project_id
                and document.get("timeline_id") == session.timeline_id
                and document.get("parent_revision", {}).get("revision_id") == entry["revision_id"],
                "selected receipt belongs to a different canonical timeline closure")
        require(all(key in data and data[key] == records.get(key) == entry.get(key)
                    for key in ("label", "steps", "merge_mode")),
                "selected label and steps do not match accepted receipt history")
        if parsed.command == "redo":
            require(bool(records.get("undo_of")), "redo requires an accepted undo commit receipt")


def commit_edit(parsed, *, sheet=False, edit=None, inverse=False):
    from astrid.core.receipts.contract import CommandReceipt
    from astrid.sdk.contracts import ErrorObject
    from astrid.sdk.timeline._common import TimelineEditError
    from astrid.sdk.timeline.sync import CommitConflict, TimelineSession

    try:
        if inverse:
            if not parsed.commit:
                raise TimelineEditError("commit options require --commit RECEIPT_ID")
            if parsed.draft or parsed.steps is not None or isinstance(parsed.steps_option, int):
                raise TimelineEditError("--commit cannot be combined with a local draft or edit count")
            if (any(not value.strip() for value in parsed.commit)
                    or len(set(parsed.commit)) != len(parsed.commit)):
                raise TimelineEditError("--commit requires unique exact receipt IDs, oldest first")
            if parsed.steps_option is not None and set(parsed.steps_option) != set(parsed.commit):
                raise TimelineEditError("--steps must map every selected commit to its step IDs")
        if sheet and parsed.draft:
            raise TimelineEditError("a sheet commit cannot be combined with a local draft")
        session = TimelineSession.open(parsed.project, parsed.ref, client=parsed.client)
        options = {"idempotency_key": parsed.idempotency_key, "dry_run": parsed.dry_run, "via": "cli"}
        if inverse:
            _verify_commit_selection(session, parsed)
            result = session.undo(parsed.commit, steps=parsed.steps_option, **options)
        elif edit is not None:
            result = edit(session, parsed, options)
            if result is NotImplemented:
                return NotImplemented
        elif sheet:
            from astrid.sdk.timeline_sheet import NativeSheet

            result = NativeSheet.load(session).apply(
                Path(parsed.sheet_file).read_text(encoding="utf-8"), session=session,
                dry_run=parsed.dry_run, idempotency_key=parsed.idempotency_key)
            if parsed.dry_run or not isinstance(result, dict):
                return print_result(DomainResult.success({
                    "status": "preview" if parsed.dry_run else "unchanged", "commands": result.commands,
                }), as_json=parsed.json, human_renderer=lambda _: (
                    "preview only; no publication accepted" if parsed.dry_run else "no change (the sheet matches its original export)"))
        else:
            result = session.move(parsed.clip, parsed.on, **options)
        receipt = CommandReceipt.from_dict(result["receipt"]) if result["receipt"] else None
        shown = DomainResult.success(result["data"], receipt=receipt,
                                     idempotency_key=result["idempotency_key"])
    except Exception as exc:  # noqa: BLE001 - preserve pending work and render transport/semantic failures
        message = str(exc) + (f"; edited sheet kept at {parsed.sheet_file}" if sheet else "")
        if isinstance(exc, CommitConflict):
            error = ErrorObject(exc.failure["code"], message, exc.failure["details"])
        else:
            error = ErrorObject(getattr(exc, "code", "timeline_edit_error"), message, getattr(exc, "details", {}))
        if inverse:
            import shlex

            details = dict(error.details)
            details.setdefault("path", "/commands/0/args/publications")
            details.setdefault("head", details.get("current"))
            details.setdefault("hint", "Read accepted history and select exact receipt IDs, oldest first; retry ambiguous outcomes with the original key.")
            details.setdefault("suggested_command", shlex.join([
                "astrid", "timelines", "history", parsed.ref, "--project", parsed.project, "--json",
            ]))
            error = ErrorObject(error.code, error.message, details)
        shown = DomainResult.failure(error, idempotency_key=(parsed.idempotency_key or "") if inverse else "")
    return print_result(shown, as_json=parsed.json,
                        human_renderer=lambda value: _render_commit_result(value, dry_run=parsed.dry_run))
def configure_edit_options(subparser):
    from astrid.packs.timeline.cli import _add_idempotency_key, _add_json_flag

    subparser.description = ("Literal clip moves and trims commit through the durable timeline session. "
                             "Other flags edit a legacy detached working copy.")
    subparser.add_argument("--dry-run", action="store_true", help="Preview a native trim without accepting a publication.")
    _add_idempotency_key(subparser)
    _add_json_flag(subparser, default=False)
    subparser.set_defaults(native_trim_defaults={action.dest: action.default for action in subparser._actions})


def configure_apply_options(subparser):
    from astrid.packs.timeline.cli import _add_idempotency_key, _add_json_flag

    subparser.add_argument("--dry-run", action="store_true", help="Preview the sheet commit without publishing.")
    _add_idempotency_key(subparser)
    _add_json_flag(subparser, default=False)


def history_steps(value):
    import argparse

    from astrid.packs.timeline.cli import _positive_int

    if not value.lstrip().startswith("{"):
        return _positive_int(value)
    try:
        steps = json.loads(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("steps must be a JSON map of receipt IDs to step-ID lists") from exc
    if (not steps or not all(isinstance(key, str) and key.strip()
                             and isinstance(ids, list) and ids
                             and all(isinstance(step, str) and step.strip() for step in ids)
                             and len(set(ids)) == len(ids) for key, ids in steps.items())):
        raise argparse.ArgumentTypeError("steps must map each receipt ID to nonempty unique step IDs")
    return steps


def configure_history_options(subparser):
    from astrid.packs.timeline.cli import _add_idempotency_key, _add_json_flag

    subparser.add_argument("--commit", action="append", metavar="RECEIPT_ID",
                           help="Reverse an accepted Runtime commit; for redo select the accepted undo. Repeat oldest first.")
    subparser.add_argument("--dry-run", action="store_true", help="Preview the inverse without accepting a commit.")
    _add_idempotency_key(subparser)
    _add_json_flag(subparser, default=False)
