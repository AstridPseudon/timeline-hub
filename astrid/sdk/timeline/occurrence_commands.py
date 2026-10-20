"""Whole canonical occurrence translation and atomic single-lane retrack."""
from __future__ import annotations

from ._command_state import CommandError, equal, root_identity
from ._recording import active
from .capture import (
    CLIP_FIELDS,
    MAP_FIELDS,
    MOVE_INTENT,
    RELATIONS,
    _duration,
    _provenance,
    number,
    occurrence_start,
    quantized_start,
    rate,
)

OCCURRENCE_MOVE_INTENT = dict(MOVE_INTENT, ownership='occurrence')
LANE_FIELDS = ('id', 'kind', 'role', 'enabled', 'active', 'disabled', 'hidden', 'deleted')


def lane(row):
    placement = row.get('placement') or {}
    if not isinstance(placement, dict):
        raise CommandError('occurrence placement must be an object', kind='unsupported_map')
    value = placement.get('track', row.get('track'))
    if ('track' in row and 'track' in placement and row['track'] != value
            or not isinstance(value, str) or not value.strip() or '/' in value or '::' in value):
        raise CommandError('ambiguous occurrence lane', kind='unsupported_ownership')
    return value


def geometry(ctx, ref, *, occurrence=False):
    row = ctx.state.entity(ref)
    for path in (MAP_FIELDS if occurrence else [(key,) for key in CLIP_FIELDS]):
        ctx.read(ref, path)
    if not active(row):
        raise CommandError('move requires active members', ref=ref)
    for key in ('time_map', 'timeMap', 'clips', 'children', 'from_ms', 'to_ms'):
        if ctx.read(ref, [key]) is not None:
            raise CommandError('unsupported move map: ' + key, kind='unsupported_map', ref=ref)
    if occurrence:
        for key in ('at', 'start', 'start_ms'):
            ctx.read(ref, [key])
        if (isinstance(row.get('source_offset'), bool) or isinstance(row.get('speed'), bool)
                or row.get('source_offset') not in (None, 0) or row.get('speed') not in (None, 1)
                or 'at' in row or 'start' in row or 'start_ms' in row):
            raise CommandError('occurrence requires an unambiguous translation', kind='unsupported_map')
        start, duration = occurrence_start(row), number(ctx.read(ref, ['duration_ms']), 'duration_ms', positive=True) / 1000
    else:
        start, duration = row.get('at', row.get('at_ms', 0) / 1000), _duration(row)
    if start < 0:
        raise CommandError('negative authored start', kind='unsupported_timing', ref=ref)
    return start, duration


def relations(ctx, ref, *, child=False):
    for prefix in ([], ['app'], ['app', 'astrid']):
        for key in RELATIONS:
            value = ctx.read(ref, prefix + [key])
            if key in ('fixed_start', 'for'):
                continue
            if value is not None and value != {}:
                # Parent fixed-start authoring replaces the supported relations.
                if not child and prefix and key in ('on', 'until', 'until_film_end'):
                    continue
                raise CommandError('unsupported timing relation: ' + key, kind='unsupported_timing', ref=ref)


def output_lane(ctx, ref):
    for key in LANE_FIELDS:
        ctx.read(ref, [key])
    row = ctx.state.entity(ref)
    if (row.get('kind') not in ('visual', 'audio') or row.get('role', 'output') != 'output'
            or not active(row)):
        raise CommandError('move requires an active output lane', ref=ref)
    return row


def occurrence_move(ctx, command):
    owner = command['select']
    if root_identity(owner) is None or not owner.startswith('occurrence:'):
        raise CommandError('occurrence.move requires an exact occurrence root')
    if ctx.read('parent', ['config', 'pinnedShotGroups']):
        raise CommandError('legacy groups require recorded migration', kind='unsupported_ownership')
    if ctx.select('placement.owners', owner) != [owner]:
        raise CommandError('shared authored content is unsupported', kind='unsupported_ownership')
    ctx.read(owner, ['occurrence_id'])
    ctx.read(owner + '/shot', ['shot_id'])
    _, duration = geometry(ctx, owner, occurrence=True)
    relations(ctx, owner)
    row = ctx.state.occurrence(owner)
    source_lane = lane(row)
    target = command['args'].get('track', 'parent/track:' + source_lane)
    source = output_lane(ctx, 'parent/track:' + source_lane)
    destination = output_lane(ctx, target)
    if source['kind'] != destination['kind']:
        raise CommandError('incompatible destination lane', kind='unsupported_ownership')
    fps = rate(ctx.read('parent', ['config', 'output', 'fps']))
    child_fps = ctx.read(owner + '/source', ['output', 'fps'])
    if child_fps is not None and rate(child_fps) != fps:
        raise CommandError('parent and child fps differ', kind='unsupported_timing')
    on = float(quantized_start(command['args']['on'], fps))
    ctx.dependency('move.quantization', 'time-map', {'numerator': fps.numerator,
        'denominator': fps.denominator, 'rounding': 'half-toward-positive-infinity'})
    members = ctx.select('occurrence.members', owner)
    if not members:
        raise CommandError('occurrence has no authored children', kind='unsupported_ownership')
    for index, ref in enumerate(members):
        start, length = geometry(ctx, ref)
        relations(ctx, ref, child=True)
        clip = ctx.state.entity(ref)
        if clip.get('track') != source_lane or start + length > duration + 1e-9:
            raise CommandError('move requires a complete single-lane group within its extent', ref=ref)
        output_lane(ctx, owner + '/track:' + source_lane)
        asset = clip.get('asset', clip.get('asset_id'))
        if asset is not None:
            pin = ctx.read(owner + '/source', ['registry', 'assets', str(asset)])
            if not isinstance(pin, dict) or not (pin.get('media_id') or pin.get('object_id')):
                raise CommandError('missing immutable member media pin', kind='dependency_changed', ref=ref)
            ctx.dependency('move.source:' + str(index), 'entity', pin)
        ctx.bind('move.member:' + str(index), ref)
    for ref in ctx.select('occurrence.move.blockers', owner, boundaries=[target]):
        start, length = geometry(ctx, ref, occurrence=ref.startswith('occurrence:'))
        relations(ctx, ref, child=True)
        if on < start + length and start < on + duration:
            raise CommandError('moved occurrence overlaps destination content', kind='occurrence_boundary', ref=ref)
    retrack = target != 'parent/track:' + source_lane
    if retrack:
        # The complete definition is copied or compared, including opaque data.
        destination = ctx.read(target)
        child_target = owner + '/track:' + destination['id']
        existing = ctx.read(child_target)
        if existing is None:
            ctx.create(owner, 'track', destination)
        elif not equal(existing, destination):
            raise CommandError('destination child track definition is incompatible', kind='identity_collision', ref=child_target)
    _provenance(ctx, owner)
    ctx.bind('move.owner', owner, dependencies=['move.images', 'move.quantization'])
    ctx.bind('move.track', target)
    ctx.object(owner, ['placement'])
    ctx.write(owner, ['placement', 'start_ms'], on * 1000)
    if 'at_ms' in row:
        ctx.write(owner, ['at_ms'], on * 1000)
    if retrack:
        ctx.write(owner, ['placement', 'track'], destination['id'])
        ctx.write(owner, ['track'], destination['id'])
        for ref in members:
            ctx.write(ref, ['track'], destination['id'])
    ctx.object(owner, ['app'])
    ctx.object(owner, ['app', 'astrid'])
    for prefix in (['app'], ['app', 'astrid']):
        for key in ('on', 'until', 'until_film_end'):
            ctx.clear(owner, prefix + [key])
    ctx.write(owner, ['app', 'astrid', 'fixed_start'], True)
    ctx.write(owner, ['app', 'astrid', 'for'], duration)


def capture_occurrence_move(bundle, select, on, *, track=None, ownership='occurrence'):
    """Capture GLOBAL seconds on the original canonical bundle, before preview.

    track is an exact parent/track:<raw ID>; omit to retain the current lane.
    A new parent lane is a preceding explicit track.create in the same gesture.
    """
    if ownership != 'occurrence':
        raise CommandError('shared occurrence editing is unsupported', kind='unsupported_ownership')
    from .commands import execute

    args = {'on': on}
    if track is not None:
        args['track'] = track
    return execute(bundle, [{'schema_version': 1, 'op': 'occurrence.move', 'version': '1',
        'select': select, 'args': args, 'intent': OCCURRENCE_MOVE_INTENT}]).commands[0]
