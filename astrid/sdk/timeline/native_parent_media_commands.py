"""Parent media birth and explicit ordered replacement over complete authored rows."""
from __future__ import annotations

import copy
import math

from astrid.core.timeline.duration import clip_timeline_duration

from ._command_state import CommandError, State
from ._media_inputs import _verified
from .capture import number, rate
from .native_occurrence_media_commands import _clip, _registry


def _start(row):
    """Return the authored raw start without selecting a display projection."""
    if 'at' not in row:
        raise CommandError('parent after-clip anchor requires an authored at', kind='unsupported_timing')
    start = number(row['at'], 'clip.at')
    if start < 0:
        raise CommandError('clip.at must not be negative', kind='unsupported_timing')
    if ('at_ms' in row and row['at_ms'] is not None
            and not math.isclose(number(row['at_ms'], 'clip.at_ms') / 1000, start, abs_tol=1e-9)):
        raise CommandError('contradictory at/at_ms timing codecs', kind='unsupported_timing')
    return start


def _after_row(source, requested, media, *, start):
    """Clone the raw Main source row, changing only its reserved identities."""
    if not isinstance(requested, dict) or not isinstance(requested.get('id'), str):
        raise CommandError('after-clip birth requires a reserved destination id')
    if requested.get('track', source.get('track')) != source.get('track'):
        raise CommandError('after-clip birth cannot change the source track', kind='unsupported_ownership')
    if requested.get('asset', media.get('asset')) != media.get('asset'):
        raise CommandError('after-clip birth asset differs from the reserved selection', kind='dependency_changed')
    row = copy.deepcopy(source)
    row['id'] = requested['id']
    row['asset'] = media['asset']
    if 'at' in source:
        row['at'] = start
    if 'at_ms' in source:
        row['at_ms'] = start * 1000
    for key in ('effectId', 'effect_id'):
        if key in source or key in requested:
            row[key] = copy.deepcopy(requested.get(key, f'effect-{requested["id"]}'))
    return row


def _after_capture_row(bundle, after, row, media):
    source = State(bundle).entity(after, optional=True)
    if not isinstance(source, dict):
        raise CommandError('after-clip anchor is missing', kind='selection_changed', ref=after)
    start = _start(source)
    duration = max(0.05, clip_timeline_duration(source))
    return _after_row(source, row, media, start=start + duration)


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
    after = None if command['select'] == 'parent' else command['select']
    prior_records = getattr(ctx, 'prior_records', ())
    replacing = bool(prior_records and
                     prior_records[-1]['command']['op'] == 'timeline.assembled-target')
    ctx.bind('media.owner', 'parent')
    _clip(ctx, 'parent', row, float('inf'), kind, [value], raw_window=after is not None and not replacing)
    for occurrence in ctx.select('collection.occurrences', 'parent'):
        for path in (['placement', 'track'], ['track']):
            if ctx.read(occurrence, path) == row['track']:
                raise CommandError('track is the lane of an occurrence-owned shot',
                                   kind='unsupported_ownership')
    _registry(ctx, 'parent', pin, kind, create=True, alias=row['asset'])
    if after is not None and not replacing:
        if not after.startswith('parent/clip:'):
            raise CommandError('parent after-clip birth requires a raw parent clip',
                               kind='unsupported_ownership')
        ctx.select('collection.clips.after', 'parent', [after])
        source = ctx.read(after)
        if not isinstance(source, dict) or source.get('track') != row.get('track'):
            raise CommandError('after-clip anchor track changed', kind='dependency_changed', ref=after)
        source_asset = source.get('asset')
        if not isinstance(source_asset, str):
            raise CommandError('after-clip anchor has no raw media identity', kind='unsupported_media', ref=after)
        ctx.read('parent/asset:' + source_asset)
        ctx.bind('parent.after-clip', after)
        ctx.bind('parent.after-track', 'parent/track:' + str(source['track']))
        start = _start(source)
        duration = max(0.05, clip_timeline_duration(source))
        expected = _after_row(source, row, pin, start=start + duration)
        if expected != row:
            raise CommandError('after-clip birth row is not the captured source clone',
                               kind='capture_mismatch', ref=after)
        members = ctx.record['selections'][-1]['order']
        for ref in members[members.index(after) + 1:]:
            if ctx.read(ref, ['track']) != source['track']:
                continue
            later = ctx.read(ref)
            later_start = _start(later)
            shifted = later_start + duration
            ctx.write(ref, ['at'], shifted)
            if 'at_ms' in later:
                ctx.write(ref, ['at_ms'], shifted * 1000)
        # Parent clips have a lossless mirror. Keep it coherent before the
        # structural birth checks the collection shape again.
        ctx.compile_mirrors()
    ctx.create('parent', 'clip', row, after=after)
    # Automatic builders may add original-state read constraints to this literal
    # birth. Observe them ourselves; caller snapshots never become record facts.
    # Ordinary births retain their existing capture and disjoint-edit behavior.
    for read in command.get('reads', ()):
        if not any(item['ref'] == read['ref'] and item['path'] == read['path']
                   for item in ctx.record['reads']):
            if (not read['ref'].startswith('parent/clip:')
                    or read['path'] not in [[field] for field in
                        ('at', 'at_ms', 'track', 'hold', 'from', 'to', 'speed')]
                    or ctx.command_input.entity(read['ref'], optional=True) is None):
                raise CommandError('unsupported parent placement read')
            ctx.read(read['ref'], read['path'])


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

    if after is not None:
        row = _after_capture_row(bundle, after, row, media)

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
