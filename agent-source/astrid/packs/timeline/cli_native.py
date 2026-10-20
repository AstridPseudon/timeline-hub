"""Thin native-command CLI adapters; schemas and capture stay in the SDK."""
from __future__ import annotations

import argparse
import copy


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
    view.bundle.update(shots={}, placements=[])
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

def configure_track_label(parser):
    from astrid.packs.timeline.cli import (
        _add_idempotency_key,
        _add_json_flag,
        _add_project_arg,
        _cmd_commit_edit,
    )
    from astrid.sdk.timeline.commands import operations

    parameters = operations()['track.set'].parameters
    field, schema = next(iter(parameters['properties']['values']['properties'].items()))
    parser.description = 'Commit a guarded parent-track label through the native command registry.'
    _add_project_arg(parser, required=False)
    parser.add_argument('ref', help='Timeline id or slug.')
    parser.add_argument('--track', required=True, help='Stable parent/track:ID selector.')
    choice = parser.add_mutually_exclusive_group(required=True)
    choice.add_argument('--set', dest='label', metavar=schema['type'].upper(),
                        help=f'Set {field}; an empty string is a real value.')
    choice.add_argument('--clear', action='store_true', help=f'Remove {field}.')
    parser.add_argument('--dry-run', action='store_true', help='Validate without accepting a publication.')
    _add_idempotency_key(parser)
    _add_json_flag(parser, default=False)

    def run(parsed):
        command = {'schema_version': 1, 'op': 'track.set', 'version': '1',
                   'select': parsed.track,
                   'args': {'values': {} if parsed.clear else {field: parsed.label},
                            'clear': [field] if parsed.clear else []}}
        return _cmd_commit_edit(parsed, command=command)

    parser.set_defaults(command='track-label', handler=run)


def configure_commands_file(parser):
    from astrid.packs.timeline.cli import (
        _add_idempotency_key,
        _add_json_flag,
        _add_project_arg,
        _cmd_commit_edit,
    )
    from astrid.sdk.timeline.commands import operations

    parser.description = ('Commit a JSON array of registered EditCommands atomically on an explicit '
                          'original revision/publication. Supplied capture claims are verified, never '
                          'refreshed. Missing capture inputs refuse the batch; the file is kept.')
    parser.formatter_class = argparse.RawDescriptionHelpFormatter
    parser.epilog = 'Installed operations:\n  ' + '\n  '.join(operations())
    _add_project_arg(parser, required=False)
    parser.add_argument('ref', help='Timeline id or slug.')
    parser.add_argument('commands_file', metavar='FILE', help='JSON array of existing EditCommands.')
    parser.add_argument('--base-revision-id', required=True, help='Original immutable revision id.')
    parser.add_argument('--base-publication-id', required=True, help='Original publication id.')
    parser.add_argument('--dry-run', action='store_true', help='Validate without accepting a publication.')
    _add_idempotency_key(parser)
    _add_json_flag(parser, default=False)
    parser.set_defaults(command='commands-file', handler=_cmd_commit_edit)
