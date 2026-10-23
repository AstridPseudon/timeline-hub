"""Thin native-command CLI adapters; schemas and capture stay in the SDK."""
from __future__ import annotations

import copy
from collections.abc import Mapping
from pathlib import Path

from astrid.core.cli.domain_output import DomainResult, print_result


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


def commit_edit(parsed, *, command=None, sheet=False, edit=None):
    from astrid.core.receipts.contract import CommandReceipt
    from astrid.sdk.contracts import ErrorObject
    from astrid.sdk.timeline._common import TimelineEditError
    from astrid.sdk.timeline.sync import CommitConflict, TimelineSession

    try:
        if sheet and parsed.draft:
            raise TimelineEditError("--native cannot be combined with a local draft")
        session = TimelineSession.open(parsed.project, parsed.ref, client=parsed.client)
        options = {"idempotency_key": parsed.idempotency_key, "dry_run": parsed.dry_run, "via": "cli"}
        if edit is not None:
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
        elif command is not None:
            result = session.commit(command, label=f"CLI {command}", **options)
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
        shown = DomainResult.failure(error)
    return print_result(shown, as_json=parsed.json,
                        human_renderer=lambda value: _render_commit_result(value, dry_run=parsed.dry_run))


def configure_edit_options(subparser):
    from astrid.packs.timeline.cli import _add_idempotency_key, _add_json_flag

    subparser.description = ("Literal clip moves and trims commit through the durable timeline session. "
                             "Ordinary --trim-in/--trim-out on literal parent media also commit directly "
                             "when no detached working copy exists. Other flags edit a legacy detached working copy.")
    subparser.add_argument("--dry-run", action="store_true", help="Preview a native trim without accepting a publication.")
    _add_idempotency_key(subparser)
    _add_json_flag(subparser, default=False)
    subparser.set_defaults(native_trim_defaults={action.dest: action.default for action in subparser._actions})


def configure_apply_options(subparser):
    from astrid.packs.timeline.cli import _add_idempotency_key, _add_json_flag

    subparser.add_argument("--dry-run", action="store_true", help="Preview the sheet commit without publishing.")
    _add_idempotency_key(subparser)
    _add_json_flag(subparser, default=False)
