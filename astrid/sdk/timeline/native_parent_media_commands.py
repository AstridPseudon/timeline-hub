"""Flat-parent media insertion and explicit observed assembly replacement."""
from __future__ import annotations

import copy

from ._command_state import CommandError, State
from ._media_inputs import _verified
from .capture import rate
from .native_occurrence_media_commands import _clip, _registry


def assembled_target(ctx, command):
    if ctx.select('collection.occurrences', 'parent'):
        raise CommandError('assembled replacement requires flat parent ownership')
    members = ctx.select('collection.clips', 'parent')
    if members != command['args']['replace_clips']:
        raise CommandError('explicit prior populated target required', kind='selection_changed')
    for ref in members:
        ctx.read(ref)


def add_media(ctx, command):
    row, pin = command['args']['row'], command['args']['media']
    value, kind = _verified(ctx, pin)
    rate(ctx.read('parent', ['config', 'output', 'fps']))
    if ctx.read('parent/source', ['source_window']) is not None:
        raise CommandError('parent source_window is unsupported', kind='unsupported_map')
    ctx.bind('media.owner', 'parent')
    _clip(ctx, 'parent', row, float('inf'), kind, [value])
    _registry(ctx, 'parent', pin, kind, create=True, alias=row['asset'])
    ctx.create('parent', 'clip', row)


def capture_assembled_media(bundle, assembled, media, *, replace_clips, verified_media):
    """Normalize ordered assembler rows before proposal capture and artifact hashing.

    Media selections must already come from the exact ordered managed outputs.
    Legacy registry labels confer no selection authority and are not copied.
    """
    from .commands import execute

    timeline, media = copy.deepcopy(assembled['timeline']), copy.deepcopy(media)
    replace_clips = list(replace_clips)
    if (not timeline['clips'] or len(timeline['clips']) != len(media)
            or len(assembled['children']) != len(media)):
        raise CommandError('assembly requires one exact selection per ordered clip')
    if any(child['ordinal'] != i or child['clip_id'] != row['id'] or child['object_id'] != pin['object_id']
           for i, (child, row, pin) in enumerate(zip(assembled['children'], timeline['clips'], media))):
        raise CommandError('assembly selection differs from ordered child output')

    def call(op, args, select='parent'):
        return {'schema_version': 1, 'op': op, 'version': '1', 'select': select, 'args': args}

    calls = [call('timeline.assembled-target', {'replace_clips': replace_clips})]
    calls.extend(call('clip.delete', {}, ref) for ref in replace_clips)
    tracks = State(bundle).collection('parent', 'track')
    calls.extend(call('track.create', {'row': row}) for row in timeline['tracks']
                 if not any(track['id'] == row['id'] for track in tracks))
    for row, pin in zip(timeline['clips'], media):
        if 'hold' not in row:
            row['hold'] = row['to'] - row['from']
        calls.append(call('clip.add-media', {'row': row, 'media': pin}))
    return execute(bundle, calls, verified_media=verified_media).commands
