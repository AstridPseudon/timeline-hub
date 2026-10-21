"""Bounded raw clip fields; media assignment uses the scoped swap recipes."""
from __future__ import annotations

import copy
import math

from astrid.core.timeline.duration import clip_end_frame, clip_start_frame

from ._command_state import CommandError
from ._materialization import capture_version
from ._scalar_commands import _capture, _changes, _clip_basis, _selected_schema, _target
from .capture import CLIP_FIELDS, MAP_FIELDS, RELATIONS, _duration, number, occurrence_start, rate


def _hold_extent(ctx, ref, values, clear):
    owner = ref.rsplit('/', 1)[0]
    for key in CLIP_FIELDS:
        ctx.read(ref, [key])
    row = copy.deepcopy(ctx.state.entity(ref))
    for key in ('time_map', 'timeMap', 'clips', 'children', 'from_ms', 'to_ms'):
        if row.get(key) is not None:
            raise CommandError(f'clip.set does not support {key}', kind='unsupported_timing', ref=ref)
    duration_paths = []
    for prefix in ([], ['app'], ['app', 'astrid']):
        for key in RELATIONS:
            value = ctx.read(ref, prefix + [key])
            if value is None or (key == 'fixed_start' and isinstance(value, bool)):
                continue
            if key == 'cut':
                # A cut names the owning authored group; changing the source
                # hold must preserve that identity without treating it as a
                # timing relation.
                continue
            if key == 'for':
                # Preserve independent intent; only an agreeing static extent
                # follows this explicit source-hold edit.
                if not math.isclose(number(value, 'for', positive=True), _duration(row), abs_tol=1e-9):
                    raise CommandError('clip.set hold conflicts with static for', kind='unsupported_timing', ref=ref)
                duration_paths.append(prefix + [key])
                continue
            raise CommandError(f'clip.set hold does not support {key}', kind='unsupported_timing', ref=ref)
    if 'hold' in values:
        number(values['hold'], 'hold', positive=True)
        row['hold'] = values['hold']
    if 'hold' in clear:
        row.pop('hold', None)
        if row.get('from') is None or row.get('to') is None:
            raise CommandError('hold clear requires a surviving source window', kind='unsupported_timing', ref=ref)
    duration = _duration(row)
    row['at'] = row.get('at', row.get('at_ms', 0) / 1000)
    fps = rate(ctx.read('parent', ['config', 'output', 'fps']))
    # Preserve source seconds exactly; only the consumed extent is quantized.
    end = clip_end_frame(row, float(fps))
    ctx.dependency('clip.set.quantization', 'time-map', {
        'numerator': fps.numerator, 'denominator': fps.denominator,
        'rounding': 'half-toward-positive-infinity'})
    if owner == 'parent':
        return duration_paths, duration
    child_fps = ctx.read(owner + '/source', ['output', 'fps'])
    if child_fps is not None and rate(child_fps) != fps:
        raise CommandError('parent and child fps differ', kind='unsupported_timing')
    for path in MAP_FIELDS:
        ctx.read(owner, path)
    occurrence = ctx.state.occurrence(owner)
    if (occurrence.get('time_map') is not None or occurrence.get('timeMap') is not None
            or isinstance(occurrence.get('speed'), bool)
            or isinstance(occurrence.get('source_offset'), bool)
            or occurrence.get('speed') not in (None, 1)
            or occurrence.get('source_offset') not in (None, 0)):
        raise CommandError('clip.set requires a translation-only occurrence', kind='unsupported_map')
    origin = occurrence_start(occurrence)
    extent = occurrence.get('duration_ms')
    if extent is None:
        raise CommandError('clip.set requires an explicit occurrence extent', kind='unsupported_timing')
    limit = origin + number(extent, 'occurrence.duration_ms', positive=True) / 1000
    for other in ctx.select('move.blockers', owner):
        for path in (('placement', 'start_ms'), ('at_ms',), ('track',), ('placement', 'track'),
                     ('enabled',), ('active',), ('disabled',), ('hidden',), ('deleted',)):
            ctx.read(other, path)
        start = occurrence_start(ctx.state.occurrence(other))
        if other != owner and start > origin:
            limit = min(limit, start)
    # Both the authored half-open interval and its compiled frames must fit.
    boundary = clip_start_frame({'at': limit - origin, 'hold': 1}, float(fps))
    if row['at'] < 0 or row['at'] + duration > limit - origin + 1e-9 or end > boundary:
        raise CommandError('clip.set interval crosses occurrence boundary', kind='occurrence_boundary', ref=owner)
    return duration_paths, duration


_FADE_PAIRS = {
    'fade_in': ('entrance', 'fade'),
    'fade_out': ('exit', 'fade-out'),
}


def _fade_duration(value, label):
    if value is None:
        return None
    result = number(value, label)
    if result < 0:
        raise CommandError(f'{label} must be non-negative', kind='unsupported_timing')
    return result


def _effect_values(ctx, ref, values, clear):
    """Apply numeric effect leaves and Main's exact coupled fade slots."""
    patch = values.get('effects')
    cleared = {key.removeprefix('effects.') for key in clear
               if key.startswith('effects.')}
    coupled = {}
    for fade, (slot, slot_type) in _FADE_PAIRS.items():
        effect_set = isinstance(patch, dict) and fade in patch
        slot_set = slot in values
        effect_clear = fade in cleared
        slot_clear = slot in clear
        if slot_set and not effect_set:
            raise CommandError(f'{slot} must be paired with effects.{fade}', ref=ref,
                               path=[slot])
        if slot_clear and not effect_clear:
            raise CommandError(f'{slot} clear must be paired with effects.{fade}', ref=ref,
                               path=[slot])
        if (effect_set or slot_set) and (effect_clear or slot_clear):
            raise CommandError(f'cannot set and clear the {fade} pair', ref=ref,
                               path=['effects', fade])
        if slot_set:
            effect = patch[fade]
            slot_value = values[slot]
            if effect is None:
                if slot_value is not None:
                    raise CommandError(f'{fade} and {slot} must both be null or numeric',
                                       ref=ref, path=['effects', fade])
            else:
                duration = _fade_duration(effect, 'effects.' + fade)
                if (not isinstance(slot_value, dict)
                        or set(slot_value) != {'type', 'duration'}
                        or slot_value.get('type') != slot_type
                        or _fade_duration(slot_value.get('duration'), slot + '.duration') != duration):
                    raise CommandError(f'{fade} and {slot} must be the same Main fade',
                                       ref=ref, path=['effects', fade])
            coupled[fade] = (slot, slot_value)
        elif slot_clear:
            coupled[fade] = (slot, None)

    if coupled:
        # Coupled commands guard the original slots and complete effects
        # container, including opaque members and insertion order.
        ctx.read(ref, ['entrance'])
        ctx.read(ref, ['effects'])
        ctx.read(ref, ['exit'])

    if patch is None and not cleared:
        return
    if patch is not None:
        current = ctx.state.get(ref, ['effects'])
        if (current['state'] == 'present' and current['value'] is not None
                and not isinstance(current['value'], dict)):
            raise CommandError('clip.set effects requires an object effects map', ref=ref,
                               path=['effects'])
        ctx.object(ref, ['effects'])
        for key in sorted(patch):
            if key in coupled:
                if patch[key] is not None:
                    _fade_duration(patch[key], 'effects.' + key)
            else:
                number(patch[key], 'effects.' + key)
            ctx.write(ref, ['effects', key], patch[key])

    for key in sorted(cleared):
        current = ctx.state.get(ref, ['effects'])
        if (current['state'] == 'present' and current['value'] is not None
                and not isinstance(current['value'], dict)):
            raise CommandError('clip.set effects requires an object effects map', ref=ref,
                               path=['effects'])
        # State.clear records an absent/null parent as an exact no-op leaf
        # write, preserving the raw distinction in the command guard.
        ctx.clear(ref, ['effects', key])

    for fade, (slot, slot_value) in coupled.items():
        if isinstance(patch, dict) and fade in patch:
            ctx.write(ref, [slot], slot_value)
        else:
            ctx.clear(ref, [slot])


def clip_set(ctx, command):
    ref = _target(ctx, command, 'clip')
    values, clear = _changes(command)
    identity = _clip_basis(ctx, ref)
    if 'hold' in values and isinstance(identity['elementRef'] or identity['element_ref'], dict):
        ctx.select('element.targets', ref.rsplit('/', 1)[0])
    row = ctx.state.entity(ref)
    if 'asset' in clear:
        for key in ('asset_id', 'media_id', 'object_id'):
            if key in row:
                raise CommandError('asset clear cannot expose another media selector', ref=ref)
    asset = row.get('asset', row.get('asset_id'))
    if isinstance(asset, str):
        ctx.read(ref.rsplit('/', 1)[0] + '/registry', ['assets', asset, 'content_sha256'])
    if 'hold' in values or 'hold' in clear:
        duration_paths, duration = _hold_extent(ctx, ref, values, clear)
        for path in duration_paths:
            ctx.write(ref, path, duration)
    _effect_values(ctx, ref, values, clear)
    for key in sorted(values):
        if key not in {'effects', 'entrance', 'exit'}:
            ctx.write(ref, [key], values[key])
    for key in sorted(clear):
        if not key.startswith('effects.') and key not in {'entrance', 'exit'}:
            ctx.clear(ref, [key])


def capture_clip_set(bundle, select, *, values=None, clear=()):
    """Capture bounded raw clip leaves and explicit field removal."""
    return _capture(bundle, 'clip.set', select, values, clear)


def clip_set_element(ctx, command):
    ref = _target(ctx, command, 'clip')
    ctx.select('element.targets', ref.rsplit('/', 1)[0])
    for key in ('clipType', 'hold', 'asset', 'file', 'src', 'source', 'from', 'to'):
        ctx.read(ref, [key])
    element = command['args']['elementRef']
    selected, alias = ctx.read(ref, ['elementRef']), ctx.read(ref, ['element_ref'])
    before = selected if selected is not None else alias
    if not isinstance(before, dict):
        raise CommandError('clip.set-element requires an existing element ref', ref=ref)
    if (any(before.get(key) != element[key] for key in ('id', 'kind'))
            or before.get('packId') is not None and before['packId'] != element.get('packId')):
        raise CommandError('clip.set-element must keep the element id and kind and pack owner', ref=ref)
    if element.get('packId'):
        _selected_schema(ctx, command, ref, element)
    elif 'schema_source' in command['args']:
        raise CommandError('schema_source requires a selected project pack element', ref=ref)
    ctx.write(ref, ['elementRef'], element)
    if 'element_ref' in ctx.state.entity(ref):
        ctx.clear(ref, ['element_ref'])


def capture_clip_set_element(bundle, select, *, element, schema_source=None,
                             schema_inputs=(), realm_id=None):
    """Capture a revision change of the clip's own element; the ref is never cleared."""
    from .commands import execute

    args = {'elementRef': copy.deepcopy(element)}
    if schema_source is not None:
        args['schema_source'] = copy.deepcopy(schema_source)
    return execute(bundle, [{'schema_version': 1, 'op': 'clip.set-element', 'version': capture_version(bundle, select),
                             'select': select, 'args': args}], schema_inputs=schema_inputs,
                   realm_id=realm_id).commands[0]
