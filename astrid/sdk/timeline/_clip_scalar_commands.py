"""Bounded raw clip fields; media assignment remains occurrence.swap-media."""
from __future__ import annotations

import copy
import math

from astrid.core.timeline.duration import clip_end_frame, clip_start_frame

from ._command_state import CommandError, equal, present
from ._scalar_commands import (
    _capture,
    _changes,
    _clip_basis,
    _selected_schema,
    _target,
    _validate_param_values,
)
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


def _transition_set(ctx, command, ref, values, identity):
    from astrid.core.element.catalog import (
        list_element_descriptors,
        list_transition_ids,
        read_transition_schema,
    )

    transition = values['transition']
    number(transition['duration'], 'transition.duration', positive=True)
    selected = values.get('elementRef', identity['elementRef'] or identity['element_ref'])
    if selected is not None:
        if (not isinstance(selected, dict) or selected.get('kind') != 'transition'
                or selected.get('id') != transition['type']
                or ('revision' in transition and transition['revision'] != selected.get('revision'))):
            raise CommandError('transition requires its matching selected reference', ref=ref)
    before = ctx.read(ref, ['transition'])
    same = isinstance(before, dict) and before.get('type') == transition['type']
    same = same and equal(selected, identity['elementRef'] or identity['element_ref'])
    changed = {key: value for key, value in transition.get('params', {}).items()
               if not same or not equal(present(value), ctx.state.get(ref, ['transition', 'params', key]))}
    builtin = next((item for item in list_element_descriptors('transitions')
                    if selected and all(item[key] == selected.get(key)
                                        for key in ('id', 'kind', 'revision', 'packId'))), None)
    if builtin is not None:
        if 'schema_source' in command['args']:
            raise CommandError('builtin transition does not use schema_source', ref=ref)
        schema = builtin['schema']
    elif isinstance(selected, dict) and selected.get('packId'):
        schema = (_selected_schema(ctx, command, ref, selected)
                  if changed or not same or 'schema_source' in command['args'] else {})
    else:
        if 'schema_source' in command['args']:
            raise CommandError('schema_source requires a selected project pack transition', ref=ref)
        if selected:
            raise CommandError('selected transition declaration is unavailable', ref=ref)
        schema = read_transition_schema(transition['type']) if transition['type'] in list_transition_ids() else {}
    _validate_param_values(ref, changed, schema)
    owner = ref.rsplit('/', 1)[0]
    if identity['clipType'] == 'effect-layer':
        raise CommandError('effect layers cannot own incoming transitions', ref=ref)
    lane = ctx.read(ref, ['track'])
    if not isinstance(lane, str) or not lane:
        raise CommandError('transition requires an owning track', ref=ref)
    ctx.read(owner + '/track:' + lane, ['id'])
    fps = rate(ctx.read('parent', ['config', 'output', 'fps']))
    frames = transition['duration'] * float(fps)
    if not math.isfinite(frames) or frames < .5 or frames >= 2**53 - .5:
        raise CommandError('transition requires positive safe whole frames', ref=ref)
    if owner != 'parent':
        for path in MAP_FIELDS:
            ctx.read(owner, path)
    for neighbor in [ref, *ctx.select('transition.predecessor', ref)]:
        basis = _clip_basis(ctx, neighbor)
        asset = basis['asset'] or basis['asset_id']
        if isinstance(asset, str):
            ctx.read(owner + '/registry', ['assets', asset, 'content_sha256'])
        for key in CLIP_FIELDS:
            ctx.read(neighbor, [key])
        for prefix in ([], ['app'], ['app', 'astrid']):
            for key in RELATIONS:
                ctx.read(neighbor, prefix + [key])


def _effect_values(ctx, ref, values):
    for slot in ('entrance', 'exit', 'continuous', 'effects'):
        if slot not in values:
            continue
        patch = values[slot]
        if slot != 'effects':
            selected = ctx.read(ref, [slot, 'type'])
            if selected != patch['type']:
                previous = ctx.read(ref, [slot])
                if previous is not None and not isinstance(previous, dict):
                    raise CommandError('unsupported named effect shape', ref=ref, path=[slot])
            if 'params' in patch and (selected != patch['type'] or not equal(
                    ctx.state.get(ref, [slot, 'params']), present(patch['params']))):
                raise CommandError('named effect params require a durable exact descriptor binding',
                                   kind='unsupported_effect_schema', ref=ref, path=[slot, 'params'])
            if 'params' in patch:
                ctx.read(ref, [slot, 'params'])
            if selected != patch['type']:
                ctx.write(ref, [slot], patch)
                continue
        ctx.object(ref, [slot])
        for key in sorted(patch):
            if key == 'params':
                for name in sorted(patch[key]):
                    ctx.write(ref, [slot, key, name], patch[key][name])
            elif slot != 'effects' and key == 'type' and selected == patch[key]:
                continue
            else:
                ctx.write(ref, [slot, key], patch[key])


def clip_set(ctx, command):
    ref = _target(ctx, command, 'clip')
    values, clear = _changes(command)
    identity = _clip_basis(ctx, ref)
    if 'elementRef' in values and 'transition' not in values:
        raise CommandError('elementRef requires transition SET', ref=ref)
    if 'transition' in values:
        _transition_set(ctx, command, ref, values, identity)
    elif 'schema_source' in command['args']:
        raise CommandError('schema_source requires transition SET', ref=ref)
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
    _effect_values(ctx, ref, values)
    for key in sorted(values):
        if key not in ('entrance', 'exit', 'continuous', 'effects'):
            ctx.write(ref, [key], values[key])
    for key in sorted(clear):
        ctx.clear(ref, [key])


def capture_clip_set(bundle, select, *, values=None, clear=(), schema_source=None,
                     schema_inputs=(), realm_id=None):
    """Capture raw clip leaves, incoming transition SET, named effects, or field removal."""
    return _capture(bundle, 'clip.set', select, values, clear, schema_source=schema_source,
                    schema_inputs=schema_inputs, realm_id=realm_id)
