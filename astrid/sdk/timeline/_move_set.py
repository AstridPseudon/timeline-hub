"""One parent-owned free selection translation, captured before any writes."""
from __future__ import annotations

from fractions import Fraction

from ._command_state import CommandError
from ._recording import active
from .capture import (
    CLIP_FIELDS,
    RELATIONS,
    _provenance,
    clip_inputs,
    move_duration,
    number,
    quantized_on,
    rate,
    write_move,
)


def _free_clip(ctx, ref, key):
    clip, dependencies = clip_inputs(ctx, ref, 'parent', key)
    for prefix in ([], ['app'], ['app', 'astrid']):
        for field in (*RELATIONS, 'anchor', 'standin', 'standin_intent'):
            value = ctx.read(ref, prefix + [field])
            if field not in ('fixed_start', 'for') and value is not None:
                raise CommandError('move-set requires fixed free clips', ref=ref)
            if field == 'for' and value is not None:
                number(value, 'for', positive=True)
            if field == 'fixed_start' and value is not None and value is not True:
                raise CommandError('move-set requires fixed start intent', ref=ref)
    if clip.get('clipType', clip.get('clip_type')) == 'shot':
        raise CommandError('move-set requires active free clips', ref=ref)
    ctx.bind(key, ref, dependencies=dependencies)
    return clip, move_duration(clip, ref)


def move_set(ctx, command):
    args = command['args']
    refs = [member['clip'] for member in args['members']]
    if len(set(refs)) != len(refs) or args['anchor'] not in refs:
        raise CommandError('move-set needs unique members and a member anchor')
    if ctx.read('parent', ['config', 'pinnedShotGroups']) not in (None, []):
        raise CommandError('move-set requires migrated legacy groups')
    if set(ctx.select('selection.clips', 'parent', refs)) != set(refs):
        raise CommandError('move-set member disappeared', kind='identity_conflict')
    clips = [_free_clip(ctx, ref, f'move.member:{i}') for i, ref in enumerate(refs)]
    fps = rate(ctx.read('parent', ['config', 'output', 'fps']))
    ctx.dependency('move.quantization', 'time-map', {'numerator': fps.numerator,
                   'denominator': fps.denominator, 'rounding': 'half-toward-positive-infinity'})
    anchor = clips[refs.index(args['anchor'])][0]
    def start(row):
        return number(row.get('at', number(row.get('at_ms', 0), 'at_ms') / 1000), 'at')
    delta = quantized_on(args['on'], fps) - Fraction(str(start(anchor)))
    candidates = []
    for i, (member, (clip, duration)) in enumerate(zip(args['members'], clips)):
        target = member['track']
        for field in ('id', 'kind', 'role', 'enabled', 'active', 'disabled', 'hidden', 'deleted'):
            ctx.read(target, [field])
        source = ctx.state.entity('parent/track:' + clip['track'])
        lane = ctx.state.entity(target)
        if (not active(clip) or not active(source) or not active(lane) or source.get('kind') != lane.get('kind')
                or lane.get('kind') not in ('visual', 'audio')
                or source.get('role', 'output') != 'output' or lane.get('role', 'output') != 'output'):
            raise CommandError('move-set requires compatible active output tracks')
        ctx.bind(f'move.destination:{i}', target)
        at = float(Fraction(str(start(clip))) + delta)
        if at < 0:
            raise CommandError('move-set would precede timeline zero')
        candidates.append((target, at, at + duration))
    for target in dict.fromkeys(member['track'] for member in args['members']):
        for ref in ctx.select('lane.members', target):
            if ref in refs:
                continue
            if not ref.startswith('parent/clip:'):
                raise CommandError('move-set destination contains an unsupported occurrence', ref=ref)
            for field in CLIP_FIELDS:
                ctx.read(ref, [field])
            if not active(ctx.state.entity(ref)):
                continue
            clip, duration = _free_clip(ctx, ref, 'move.blocker:' + ref)
            at = start(clip)
            if any(lane == target and left < at + duration and at < right
                   for lane, left, right in candidates):
                raise CommandError('move-set overlaps a destination blocker', kind='lane_conflict', ref=ref)
    for i, (lane, left, right) in enumerate(candidates):
        for other, (other_lane, other_left, other_right) in enumerate(candidates[:i]):
            if lane == other_lane and left < other_right and other_left < right:
                old, previous = clips[i][0], clips[other][0]
                if old['track'] != previous['track']:
                    raise CommandError('move-set introduces member overlap', kind='lane_conflict')
    _provenance(ctx, 'parent')
    for ref, (clip, duration), (lane, at, _) in zip(refs, clips, candidates):
        write_move(ctx, ref, clip, at, duration)
        ctx.write(ref, ['track'], lane.removeprefix('parent/track:'))


def capture_move_set(bundle, members, anchor, on):
    """Capture ordered explicit members on the original (optionally staged) basis."""
    from .commands import execute

    return execute(bundle, [{'schema_version': 1, 'op': 'clip.move-set', 'version': '1',
                             'select': 'parent', 'args': {'members': members, 'anchor': anchor,
                                                         'on': on}}]).commands[0]
