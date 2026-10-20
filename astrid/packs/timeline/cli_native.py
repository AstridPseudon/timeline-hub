"""Thin native-command CLI adapters; schemas and capture stay in the SDK."""
from __future__ import annotations

import argparse


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
