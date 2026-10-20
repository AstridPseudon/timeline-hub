"""Bounded whole-occurrence translation onto an existing parent lane."""
from __future__ import annotations

import copy
from fractions import Fraction

from astrid.core.timeline.duration import clip_start_frame

from ._command_state import CommandError, equal, root_identity
from ._recording import active
from .capture import MOVE_INTENT, RELATIONS, _provenance, number, occurrence_start, rate
from .new_group_commands import _geometry

OCCURRENCE_MOVE_INTENT = dict(MOVE_INTENT, ownership='occurrence')


def lane(row):
    placement = row.get('placement')
    if placement is None:
        placement = {}
    if not isinstance(placement, dict):
        raise CommandError('occurrence placement must be an object')
    value = placement.get('track', row.get('track'))
    if not isinstance(value, str) or row.get('track', value) != value:
        raise CommandError('ambiguous occurrence lane', kind='unsupported_ownership')
    return value


def output_lane(ctx, ref):
    row = ctx.read(ref)
    if (not isinstance(row, dict) or row.get('kind') not in ('visual', 'audio')
            or row.get('role', 'output') != 'output' or not active(row)):
        raise CommandError('move requires an active output lane', ref=ref)
    return row


def occurrence_move(ctx, command):
    owner, args = command['select'], command['args']
    if root_identity(owner) is None or not owner.startswith('occurrence:'):
        raise CommandError('move requires an exact occurrence root')
    if 'start_ms' in args:
        _move_start(ctx, owner, args['start_ms'])
        return
    if ctx.select('placement.owners', owner) != [owner]:
        raise CommandError('shared occurrence isolation needs a materialization carrier', kind='unsupported_ownership')
    row = ctx.read(owner)
    source = ctx.read(owner + '/shot', ['shot_id'])
    if source != row['shot_id']:
        raise CommandError('derived owner needs a materialization carrier', kind='unsupported_ownership')
    if (isinstance(row.get('source_offset'), bool) or not active(row) or row.get('source_offset') not in (None, 0)
            or row.get('speed') not in (None, 1) or isinstance(row.get('speed'), bool)
            or any(row.get(k) is not None for k in ('time_map', 'timeMap', 'source_map', 'sourceMap', 'clips', 'children',
                                                        'from_ms', 'to_ms', 'at', 'start', 'start_ms'))):
        raise CommandError('move requires a translation-only occurrence', kind='unsupported_map')
    app = row.get('app')
    for container in (row, app, app.get('astrid') if isinstance(app, dict) else None):
        if container is not None and (not isinstance(container, dict) or any(
                container.get(k) is not None and not (k == 'fixed_start' and container[k] is True)
                for k in (*RELATIONS, 'anchor'))):
            raise CommandError('move requires fixed occurrence timing')
    source = output_lane(ctx, 'parent/track:' + lane(row))
    destination = output_lane(ctx, args['track'])
    child_target = args['child_track']
    if child_target != owner + '/track:' + child_target.rsplit('/track:', 1)[-1]:
        raise CommandError('destination child track must belong to the occurrence')
    child = output_lane(ctx, child_target)
    if len({source['kind'], destination['kind'], child['kind']}) != 1:
        raise CommandError('incompatible destination lane')
    fps = rate(ctx.read('parent', ['config', 'output', 'fps']))
    child_fps = ctx.read(owner + '/source', ['output', 'fps'])
    if child_fps is not None and rate(child_fps) != fps:
        raise CommandError('parent and child fps differ')
    on = float(Fraction(clip_start_frame({'at': args['on'], 'hold': 1}, float(fps))) / fps)
    duration = number(row.get('duration_ms'), 'duration_ms', positive=True) / 1000
    members = ctx.select('collection.clips', owner)
    if not members:
        raise CommandError('move requires authored children')
    ctx.read(owner + '/source', ['registry'])
    raw_lanes = set()
    for index, ref in enumerate(members):
        clip = ctx.read(ref)
        _, end = _geometry(clip)
        raw_lanes.add(clip['track'])
        raw_lane = output_lane(ctx, owner + '/track:' + clip['track'])
        if len(raw_lanes) != 1 or end > Fraction(str(duration)) or not active(clip):
            raise CommandError('move requires a complete active single-lane group within its extent')
        if raw_lane['kind'] != child['kind']:
            raise CommandError('incompatible child lane')
        ctx.bind('move.member:' + str(index), ref)
        ctx.bind('move.raw-track:' + str(index), owner + '/track:' + clip['track'])
    for ref in ctx.select('lane.members', args['track']):
        if ref == owner:
            continue
        blocker = ctx.read(ref)
        if not active(blocker):
            continue
        if ref.startswith('occurrence:'):
            start = occurrence_start(blocker)
            end = start + number(blocker.get('duration_ms'), 'duration_ms', positive=True) / 1000
        else:
            start, end = _geometry(blocker)
        if on < end and start < on + duration:
            raise CommandError('moved occurrence overlaps destination content', kind='occurrence_boundary')
    _provenance(ctx, owner)
    for key, ref in (('owner', owner), ('track', args['track']), ('child-track', child_target)):
        ctx.bind('move.' + key, ref)
    ctx.object(owner, ['placement'])
    ctx.write(owner, ['placement', 'start_ms'], on * 1000)
    if 'at_ms' in row:
        ctx.write(owner, ['at_ms'], on * 1000)
    ctx.write(owner, ['placement', 'track'], destination['id'])
    ctx.write(owner, ['track'], destination['id'])
    for ref in members:
        ctx.write(ref, ['track'], child['id'])


def _move_start(ctx, owner, start_ms):
    """Translate the canonical root clock without quantizing or retracking children."""
    if type(start_ms) is not int or start_ms < 0:
        raise CommandError('start_ms must be a nonnegative integer', kind='unsupported_timing')
    owners = ctx.select('collection.occurrences', 'parent')
    row = ctx.read(owner)
    # Record ownership as canonical identity reads. A sibling's materialization
    # can make this unchanged source unshared; State.matches proves that exact
    # source/slot alias without weakening membership or shared-owner guards.
    for other in owners:
        shot_id = ctx.read(other, ['shot_id'])
        if other != owner and shot_id == row['shot_id']:
            raise CommandError('shared occurrence isolation needs a materialization carrier',
                               kind='unsupported_ownership')
    if row.get('occurrence_id') != root_identity(owner)[1]:
        raise CommandError('move requires a stable occurrence identity', kind='identity_conflict')
    # State validates the raw source or its canonical occurrence-owned alias.
    # A display/group ID never supplies authority for a materialized root.
    ctx.read(owner + '/shot', ['shot_id'])
    occurrence_start(row)
    if (not active(row)
            or not any(equal(row.get('source_offset'), value) for value in
                       (None, 0, {'start': 0, 'end': 0}))
            or not any(equal(row.get('speed'), value) for value in
                       (None, 1, {'numerator': 1, 'denominator': 1}))
            or any(row.get(k) is not None for k in ('time_map', 'timeMap', 'source_map', 'sourceMap',
                                                    'clips', 'children', 'from_ms', 'to_ms',
                                                    'at', 'start', 'start_ms'))):
        raise CommandError('move requires a translation-only occurrence', kind='unsupported_map')
    app = row.get('app')
    for container in (row, app, app.get('astrid') if isinstance(app, dict) else None):
        if container is not None and (not isinstance(container, dict) or any(
                container.get(k) is not None and not (k == 'fixed_start' and container[k] is True)
                for k in (*RELATIONS, 'anchor'))):
            raise CommandError('move requires fixed occurrence timing')
    output_lane(ctx, 'parent/track:' + lane(row))
    number(row.get('duration_ms'), 'duration_ms', positive=True)
    duration = Fraction(str(row['duration_ms']))
    for other in ctx.select('move.blockers', owner):
        if other == owner:
            continue
        blocker = ctx.read(other)
        occurrence_start(blocker)
        start = (blocker.get('placement') or {}).get('start_ms')
        start = Fraction(str(blocker.get('at_ms', 0) if start is None else start))
        number(blocker.get('duration_ms'), 'duration_ms', positive=True)
        end = start + Fraction(str(blocker['duration_ms']))
        if start_ms < end and start < start_ms + duration:
            raise CommandError('moved occurrence overlaps destination content', kind='occurrence_boundary')
    for ref in ctx.select('collection.clips', owner):
        ctx.read(ref)
    ctx.read(owner + '/source', ['registry'])
    _provenance(ctx, owner)
    ctx.bind('move.owner', owner)
    ctx.object(owner, ['placement'])
    ctx.write(owner, ['placement', 'start_ms'], start_ms)
    if 'at_ms' in row:
        ctx.write(owner, ['at_ms'], start_ms)


def capture_occurrence_start(bundle, select, start_ms):
    """Capture an exact root start; child ownership and source state stay intact."""
    from .commands import execute

    return execute(bundle, [{'schema_version': 1, 'op': 'occurrence.move', 'version': '1',
                             'select': select, 'args': {'start_ms': start_ms},
                             'intent': OCCURRENCE_MOVE_INTENT}]).commands[0]


def capture_occurrence_move(bundle, select, on, *, track, child_track, new_child_track=None):
    """Capture once before preview; an optional caller-owned track birth is in this batch."""
    from .commands import execute

    commands = []
    if new_child_track is not None:
        if child_track != select + '/track:' + new_child_track['id']:
            raise CommandError('new child track identity differs from explicit binding')
        commands.append({'schema_version': 1, 'op': 'track.create', 'version': '1',
                         'select': select, 'args': {'row': copy.deepcopy(new_child_track)}})
    commands.append({'schema_version': 1, 'op': 'occurrence.move', 'version': '1', 'select': select,
                     'args': {'on': on, 'track': track, 'child_track': child_track},
                     'intent': OCCURRENCE_MOVE_INTENT})
    return execute(bundle, commands).commands
