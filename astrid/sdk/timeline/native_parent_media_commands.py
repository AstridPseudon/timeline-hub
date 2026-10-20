"""Parent media birth and explicit ordered replacement over complete authored rows."""
from __future__ import annotations

import copy

from ._command_state import CommandError, State
from ._media_inputs import _verified
from .capture import rate
from .native_occurrence_media_commands import _clip, _registry


def assembled_target(ctx, command):
    occurrences = ctx.select('collection.occurrences', 'parent')
    if command['select'] == 'parent' and occurrences:
        raise CommandError('assembled replacement requires flat parent ownership')
    members = ctx.select('collection.clips', 'parent')
    if (members != command['args']['replace_clips']
            or command['select'] != 'parent' and command['select'] not in members):
        raise CommandError('explicit prior populated target required', kind='selection_changed')
    # Whole assembly consumes every row; a scoped replacement consumes only its target.
    for ref in members if command['select'] == 'parent' else [command['select']]:
        ctx.read(ref)


def add_media(ctx, command):
    row, pin = command['args']['row'], command['args']['media']
    value, kind = _verified(ctx, pin)
    rate(ctx.read('parent', ['config', 'output', 'fps']))
    if ctx.read('parent/source', ['source_window']) is not None:
        raise CommandError('parent source_window is unsupported', kind='unsupported_map')
    ctx.bind('media.owner', 'parent')
    _clip(ctx, 'parent', row, float('inf'), kind, [value])
    for occurrence in ctx.select('collection.occurrences', 'parent'):
        for path in (['placement', 'track'], ['track']):
            if ctx.read(occurrence, path) == row['track']:
                raise CommandError('track is the lane of an occurrence-owned shot',
                                   kind='unsupported_ownership')
    _registry(ctx, 'parent', pin, kind, create=True, alias=row['asset'])
    after = None if command['select'] == 'parent' else command['select']
    ctx.create('parent', 'clip', row, after=after)


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


def capture_clip_add_media(bundle, row, media, *, verified_media, after=None):
    """Birth preserves the complete authored row and inserts after a stable boundary or appends."""
    from .commands import execute

    return execute(bundle, [{'schema_version': 1, 'op': 'clip.add-media', 'version': '1',
                             'select': 'parent' if after is None else after,
                             'args': {'row': copy.deepcopy(row), 'media': copy.deepcopy(media)}}],
                   verified_media=verified_media).commands[0]


def capture_clip_replace_media(bundle, target, row, media, *, verified_media):
    """Explicit parent clip replacement is guarded birth plus ordinary deletion."""
    from .commands import execute

    state = State(bundle)
    old = state.entity(target, optional=True)
    if (not isinstance(old, dict) or old.get('clipType') not in ('media', 'image', 'video')
            or not isinstance(old.get('asset'), str) or old.get('track') != row['track']):
        raise CommandError('replace requires a populated clip on the same track', kind='unsupported_media')
    refs = ['parent/clip:' + clip['id'] for clip in state.collection('parent', 'clip')]
    calls = [{'schema_version': 1, 'op': op, 'version': '1', 'select': select, 'args': args}
             for op, select, args in (
                 ('timeline.assembled-target', target, {'replace_clips': refs}),
                 ('clip.add-media', target, {'row': copy.deepcopy(row), 'media': copy.deepcopy(media)}),
                 ('clip.delete', target, {}))]
    return execute(bundle, calls, verified_media=verified_media).commands


def capture_parent_completion(bundle, args, *, verified_media):
    """Literal completion scalars build the same row/media birth; automatic timing is separate."""
    required = {'id', 'track', 'at', 'hold', 'media'}
    optional = {'from', 'to', 'speed'}
    if not required <= args.keys() or args.keys() - required - optional:
        raise CommandError('completion requires literal id/track/at/hold/media and optional from/to/speed')
    row = {key: copy.deepcopy(value) for key, value in args.items() if key != 'media'}
    row.update(clipType='media', asset=args['media']['asset'])
    return capture_clip_add_media(bundle, row, args['media'], verified_media=verified_media)
