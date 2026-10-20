"""Literal parent clip creation; media and occurrence authoring follow separately.

The row is authored JSON, appended exactly as supplied. As in main's
authoring-bundle compiler, at/hold are seconds and are not quantized or
normalized at creation. Frame rounding belongs to timing evaluation.
"""
from __future__ import annotations

import copy

from ._command_state import CommandError
from ._recording import active
from .capture import RELATIONS, number


def clip_add(ctx, command):
    if command['select'] != 'parent':
        raise CommandError('clip.add v1 requires parent ownership; occurrence creation is unsupported')
    row = command['args']['row']
    number(row['at'], 'row.at')
    number(row['hold'], 'row.hold', positive=True)
    if row['at'] < 0:
        raise CommandError('row.at must not be negative')
    if row['clipType'].lower() in ('media', 'image', 'video', 'audio'):
        raise CommandError('clip.add v1 does not support media clips', kind='unsupported_media')
    # Main treats even a null media-selector key as a selection. Do not turn
    # it into absence or silently manufacture registry/media authority.
    for key in ('asset', 'asset_id', 'media_id', 'object_id'):
        if key in row:
            raise CommandError(f'clip.add v1 does not support {key}', kind='unsupported_media')
    for key in ('sourceURL', 'sourceUrl', 'source_url', 'src', 'source_uuid', 'source',
                'from', 'to', 'from_ms', 'to_ms', 'at_ms', 'duration', 'duration_ms',
                'time_map', 'timeMap', 'clips', 'children', 'clip_type', 'anchor'):
        if row.get(key) is not None:
            raise CommandError(f'clip.add v1 does not support {key}', kind='unsupported_timing')
    if row.get('speed') is not None and (isinstance(row['speed'], bool) or row['speed'] != 1):
        raise CommandError('clip.add v1 requires literal hold timing without speed changes',
                           kind='unsupported_timing')
    app = row.get('app')
    if app is not None and not isinstance(app, dict):
        raise CommandError('clip.add intent container must be object or null')
    nested = app.get('astrid') if isinstance(app, dict) else None
    if nested is not None and not isinstance(nested, dict):
        raise CommandError('clip.add intent container must be object or null')
    for container in (row, app, nested):
        if isinstance(container, dict):
            for key in (*RELATIONS, 'anchor', 'standin', 'standin_intent'):
                if container.get(key) is not None:
                    raise CommandError(f'clip.add v1 does not support {key}', kind='unsupported_timing')
    ref = 'parent/track:' + row['track']
    for key in ('id', 'kind', 'role', 'enabled', 'active', 'disabled', 'hidden', 'deleted'):
        ctx.read(ref, [key])
    track = ctx.state.entity(ref, optional=True)
    if track is None:
        raise CommandError('clip.add destination track is missing', kind='identity_conflict', ref=ref)
    if track.get('kind') not in ('visual', 'audio') or track.get('role', 'output') != 'output':
        raise CommandError('clip.add requires an output track', ref=ref)
    if not active(track):
        raise CommandError('clip.add requires an active track', ref=ref)
    if 'schema_source' in command['args']:
        from ._scalar_commands import _selected_schema, _validate_param_values

        selected = row.get('elementRef')
        if not isinstance(selected, dict) or not selected.get('packId'):
            raise CommandError('schema_source requires an owner-pinned elementRef',
                               ref='parent/clip:' + row['id'])
        if selected.get('kind') != 'effect' or selected.get('id') != row['clipType']:
            raise CommandError('owned overlay clip must match its effect elementRef',
                               ref='parent/clip:' + row['id'])
        if track.get('kind') != 'visual':
            raise CommandError('owned overlay clip requires a visual output track', ref=ref)
        schema = _selected_schema(ctx, command, 'parent/clip:' + row['id'], selected)
        params = row.get('params', {})
        if params is not None:
            if not isinstance(params, dict):
                raise CommandError('owned overlay params must be an object',
                                   ref='parent/clip:' + row['id'], path=['params'])
            _validate_param_values('parent/clip:' + row['id'], params, schema)
    ctx.bind('add.track', ref)
    ctx.create('parent', 'clip', row)


def capture_clip_add(bundle, owner, row, *, schema_source=None, schema_inputs=(), realm_id=None):
    """Capture through native execution; the caller allocates row.id beforehand."""
    from .commands import execute

    args = {'row': copy.deepcopy(row)}
    if schema_source is not None:
        args['schema_source'] = copy.deepcopy(schema_source)
    return execute(bundle, [{'schema_version': 1, 'op': 'clip.add', 'version': '1',
                             'select': owner, 'args': args, 'intent': {}}],
                   schema_inputs=schema_inputs, realm_id=realm_id).commands[0]
