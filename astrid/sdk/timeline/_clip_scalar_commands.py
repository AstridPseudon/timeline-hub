"""Bounded raw clip fields; media assignment remains occurrence.swap-media."""
from __future__ import annotations

import copy
import math

from astrid.core.timeline.duration import clip_end_frame, clip_start_frame, clip_timeline_duration

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

_MISSING = object()


def _same_field(left, right, key):
    """Compare a raw field's presence and value, not just its value."""
    left_present, right_present = key in left, key in right
    return (left_present == right_present
            and (not left_present or equal(left[key], right[key])))


def _existing_ref(row):
    """Return the canonical ref, legacy ref, or an explicit missing marker."""
    if 'elementRef' in row:
        return row['elementRef']
    if 'element_ref' in row:
        return row['element_ref']
    return _MISSING


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
    before = ctx.read(ref, ['transition'])
    row = ctx.state.entity(ref)
    selected = values['elementRef'] if 'elementRef' in values else _MISSING
    previous = _existing_ref(row)
    same_transition = (isinstance(before, dict) and 'type' in before
                       and equal(before['type'], transition['type'])
                       and _same_field(before, transition, 'revision'))
    if selected is _MISSING:
        if not same_transition or previous is not _MISSING:
            raise CommandError('transition SET without elementRef requires the existing raw identity',
                               ref=ref)
        same = True
    else:
        if not isinstance(selected, dict) or selected.get('kind') != 'transition':
            raise CommandError('transition SET requires its matching elementRef', ref=ref)
        if (selected.get('id') != transition['type']
                or selected.get('revision') != transition.get('revision')):
            raise CommandError('transition requires its matching selected reference', ref=ref)
        same = same_transition and previous is not _MISSING and equal(selected, previous)
    params = transition['params'] if 'params' in transition else _MISSING
    changed = {key: value for key, value in params.items()} if isinstance(params, dict) else {}
    if changed:
        changed = {key: value for key, value in changed.items()
                   if not same or not equal(present(value), ctx.state.get(ref, ['transition', 'params', key]))}
    if selected is _MISSING:
        if 'schema_source' in command['args']:
            raise CommandError('schema_source requires a selected project pack transition', ref=ref)
        schema = (read_transition_schema(transition['type'])
                  if transition['type'] in list_transition_ids() else {})
    else:
        builtin = next((item for item in list_element_descriptors('transitions')
                        if all(item.get(key) == selected.get(key)
                               for key in ('id', 'kind', 'revision', 'packId'))), None)
        if builtin is not None:
            if 'schema_source' in command['args']:
                raise CommandError('builtin transition does not use schema_source', ref=ref)
            schema = builtin['schema']
        elif selected.get('packId'):
            schema = (_selected_schema(ctx, command, ref, selected)
                      if changed or not same or 'schema_source' in command['args'] else {})
        else:
            if 'schema_source' in command['args']:
                raise CommandError('schema_source requires a selected project pack transition', ref=ref)
            if selected:
                raise CommandError('selected transition declaration is unavailable', ref=ref)
            schema = read_transition_schema(transition['type']) if transition['type'] in list_transition_ids() else {}
    _validate_param_values(ref, changed, schema)
    next_transition = copy.deepcopy(before) if isinstance(before, dict) else {}
    next_transition.update(copy.deepcopy(transition))
    existing_params = (before['params'] if isinstance(before, dict) and 'params' in before else _MISSING)
    if params is _MISSING:
        if existing_params is not _MISSING:
            next_transition['params'] = copy.deepcopy(existing_params)
    elif params is None:
        # Null is a raw value, not a duration-only instruction. Refuse a
        # non-empty object-to-null change rather than silently retaining data.
        if ((isinstance(existing_params, dict) and existing_params)
                or (existing_params is not _MISSING and existing_params is not None
                    and not isinstance(existing_params, dict))):
            raise CommandError('transition params null would remove existing parameters',
                               ref=ref, path=['transition', 'params'])
        next_transition['params'] = None
    elif isinstance(params, dict):
        base_params = existing_params if isinstance(existing_params, dict) else {}
        next_transition['params'] = {**copy.deepcopy(base_params), **copy.deepcopy(params)}
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
    predecessors = ctx.select('transition.predecessor', ref)
    if len(predecessors) != 1:
        raise CommandError('transition requires an adjacent predecessor on the same track', ref=ref)
    predecessor = predecessors[0]
    predecessor_row = ctx.state.entity(predecessor)
    target_row = ctx.state.entity(ref)

    def authored_start(row):
        if 'at' in row:
            return number(row['at'], 'clip.at')
        if 'at_ms' in row:
            return number(row['at_ms'], 'clip.at_ms') / 1000
        raise CommandError('transition requires explicit clip starts', ref=ref)

    try:
        predecessor_duration = clip_timeline_duration(predecessor_row)
        target_duration = clip_timeline_duration(target_row)
    except (TypeError, ValueError) as exc:
        raise CommandError('transition requires valid adjacent clip durations',
                           kind='unsupported_timing', ref=ref) from exc
    if abs(authored_start(predecessor_row) + predecessor_duration - authored_start(target_row)) >= .001:
        raise CommandError('transition requires adjacent clips on the same track', ref=ref)
    shortest_clip_frames = min(predecessor_duration, target_duration) * float(fps)
    if shortest_clip_frames <= 0 or frames > shortest_clip_frames + .0001:
        raise CommandError('transition duration exceeds the shorter adjacent clip', ref=ref)

    for neighbor in [ref, predecessor]:
        basis = _clip_basis(ctx, neighbor)
        asset = basis['asset'] or basis['asset_id']
        if isinstance(asset, str):
            ctx.read(owner + '/registry', ['assets', asset, 'content_sha256'])
        for key in CLIP_FIELDS:
            ctx.read(neighbor, [key])
        for prefix in ([], ['app'], ['app', 'astrid']):
            for key in RELATIONS:
                ctx.read(neighbor, prefix + [key])

    return next_transition


def _transition_clear_pair(ctx, ref):
    """Validate the explicit transition/elementRef removal pair.

    The historical transition-only clear is deliberately handled separately:
    it never infers or removes either element reference spelling.
    """
    references = []
    for key in ('elementRef', 'element_ref'):
        value = ctx.state.get(ref, [key])
        if value['state'] == 'present':
            references.append((key, value['value']))
    if not references:
        return
    transition = ctx.state.get(ref, ['transition'])
    value = transition.get('value') if transition['state'] == 'present' else None
    if not isinstance(value, dict) or not isinstance(value.get('type'), str):
        raise CommandError('transition remove requires a matching transition identity', ref=ref)
    for key, selected in references:
        if (not isinstance(selected, dict) or selected.get('kind') != 'transition'
                or selected.get('id') != value['type']
                or selected.get('revision') != value.get('revision')):
            raise CommandError('transition remove refuses a mismatched element reference', ref=ref,
                               path=[key])


def clip_set(ctx, command):
    ref = _target(ctx, command, 'clip')
    values, clear = _changes(command)
    identity = _clip_basis(ctx, ref)
    if 'elementRef' in clear:
        if 'transition' not in clear:
            raise CommandError('elementRef clear requires transition clear', ref=ref)
        _transition_clear_pair(ctx, ref)
    if 'elementRef' in values and 'transition' not in values:
        raise CommandError('elementRef requires transition SET', ref=ref)
    transition_write = None
    if 'transition' in values:
        transition_write = _transition_set(ctx, command, ref, values, identity)
    elif 'schema_source' in command['args']:
        raise CommandError('schema_source requires transition SET', ref=ref)
    row = ctx.state.entity(ref)
    existing_ref = _existing_ref(row)
    if 'hold' in values and isinstance(existing_ref, dict):
        ctx.select('element.targets', ref.rsplit('/', 1)[0])
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
    for key in sorted(values):
        if key == 'transition':
            ctx.write(ref, [key], transition_write)
            continue
        ctx.write(ref, [key], values[key])
    if 'elementRef' in values and 'element_ref' in row:
        ctx.clear(ref, ['element_ref'])
    for key in sorted(clear):
        ctx.clear(ref, [key])
        if key == 'elementRef' and 'element_ref' in row:
            ctx.clear(ref, ['element_ref'])
        if key == 'transition':
            # Transition-only clear is a frozen public operation.  Its
            # unrelated component/effect identity, including the legacy
            # spelling, remains byte-for-byte untouched.
            continue


def capture_clip_set(bundle, select, *, values=None, clear=(), schema_source=None,
                     schema_inputs=(), realm_id=None):
    """Capture source hold, incoming transition SET, or explicit raw field removal."""
    return _capture(bundle, 'clip.set', select, values, clear, schema_source=schema_source,
                    schema_inputs=schema_inputs, realm_id=realm_id)


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
    return execute(bundle, [{'schema_version': 1, 'op': 'clip.set-element', 'version': '1',
                             'select': select, 'args': args}], schema_inputs=schema_inputs,
                   realm_id=realm_id).commands[0]
