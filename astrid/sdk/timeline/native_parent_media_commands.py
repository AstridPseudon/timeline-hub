"""Parent-owned media birth: one image/video clip on a parent track, optionally replacing a clip.

The registry binding follows the occurrence rule: absent -> created as a recorded
write, present -> must equal the exact selection. Inverse removal of a created
alias is guarded by the generic dependent check; there is no standalone upsert.
"""
from __future__ import annotations

import copy
from fractions import Fraction

from astrid.core.timeline.duration import clip_start_frame

from ._command_state import CommandError, equal
from ._delete_commands import removable
from ._media_inputs import _verified
from ._recording import active
from .capture import number, rate
from .native_occurrence_media_commands import _registry


def _row(ctx, args, kind, value):
    fps = rate(ctx.read('parent', ['config', 'output', 'fps']))
    frame = clip_start_frame({'at': number(args['at'], 'at'), 'hold': 1}, float(fps))
    hold = number(args['hold'], 'hold', positive=True)
    speed = number(args.get('speed', 1), 'speed', positive=True)
    row = {'id': args['id'], 'clipType': kind, 'asset': args['media']['asset'], 'track': args['track'],
           'at': float(Fraction(frame, 1) / fps), 'hold': hold}
    if kind == 'image':
        if speed != 1 or 'speed' in args or 'from' in args or 'to' in args:
            raise CommandError('image requires hold without a source window or speed', kind='unsupported_timing')
        return row
    left, right = number(args.get('from'), 'from'), number(args.get('to'), 'to')
    if right <= left or not equal(right - left, hold) or right > value['duration_seconds']:
        raise CommandError('source window differs from hold or exceeds media', kind='unsupported_timing')
    row.update({'from': args['from'], 'to': args['to']})
    if 'speed' in args:
        row['speed'] = args['speed']
    return row


def _lane(ctx, args):
    track = 'parent/track:' + args['track']
    for key in ('id', 'kind', 'role', 'enabled', 'active', 'disabled', 'hidden', 'deleted'):
        ctx.read(track, [key])
    value = ctx.state.entity(track, optional=True)
    if value is None:
        raise CommandError('clip.add-media destination track is missing', kind='identity_conflict', ref=track)
    if value.get('kind') != 'visual' or value.get('role', 'output') != 'output' or not active(value):
        raise CommandError('clip.add-media requires an active visual output track', ref=track)
    # A lane an occurrence places its shot on belongs to that shot, not to the parent.
    for occurrence in ctx.select('collection.occurrences', 'parent'):
        for path in (['placement', 'track'], ['track']):
            if ctx.read(occurrence, path) == args['track']:
                raise CommandError('track is the lane of an occurrence-owned shot',
                                   kind='unsupported_ownership', ref=track)
    ctx.bind('add.track', track)


def add_media(ctx, command):
    args = command['args']
    value, kind = _verified(ctx, args['media'])
    # Two registry declarations would diverge under a one-sided write.
    if ctx.read('parent', ['registry']) is not None and ctx.read('parent', ['config', 'registry']) is not None:
        raise CommandError('parent declares two registries', kind='unsupported_media')
    row = _row(ctx, args, kind, value)
    _lane(ctx, args)
    target = None
    if 'replace' in args:
        target = 'parent/clip:' + args['replace']
        old = removable(ctx, target)
        if (old.get('clipType') not in ('media', 'image', 'video') or not isinstance(old.get('asset'), str)
                or old.get('track') != args['track']):
            raise CommandError('replace requires a populated clip on the same track',
                               kind='unsupported_media', ref=target)
    _registry(ctx, 'parent', args['media'], kind, create=True)
    ctx.create('parent', 'clip', row)
    if target is not None:
        ctx.clear(target, [])


def capture_clip_add_media(bundle, args, *, verified_media):
    """Caller reserves args['id'] and supplies the exact five-field selection and its verification."""
    from .commands import execute

    return execute(bundle, [{'schema_version': 1, 'op': 'clip.add-media', 'version': '1',
                             'select': 'parent', 'args': copy.deepcopy(args),
                             'intent': {}}], verified_media=verified_media).commands[0]
