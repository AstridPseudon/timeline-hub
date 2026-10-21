"""Bounded raw clip fields; media assignment uses the scoped swap recipes."""
from __future__ import annotations

import copy
import math

from astrid.core.timeline.duration import clip_end_frame, clip_start_frame

from ._command_state import CommandError
from ._materialization import capture_version
from ._scalar_commands import _capture, _changes, _clip_basis, _selected_schema, _target
from .capture import CLIP_FIELDS, MAP_FIELDS, RELATIONS, _duration, number, occurrence_start, rate

_GENERATED_IDENTITY = ('extensionId', 'contributionId')
_GENERATED_FIXED_FIELDS = ('extensionId', 'contributionId', 'generatedAt', 'sourceMapEntryId')
_TEXT_LEAVES = frozenset(('content', 'fontSize', 'color', 'bold', 'align'))
_HOST_CONFLICT_POLICIES = frozenset(
    ('preserve-output', 'regenerate-output', 'propose-source-update'))


def _generated_context(metadata):
    """Return the accepted host carrier context, or refuse malformed provenance."""
    if not isinstance(metadata, dict):
        return None
    extension_id = metadata.get('extensionId')
    contribution_id = metadata.get('contributionId')
    provenance = metadata.get('provenance')
    if (not isinstance(extension_id, str) or not extension_id
            or (contribution_id is not None
                and (not isinstance(contribution_id, str) or not contribution_id))
            or not isinstance(provenance, dict)
            or provenance.get('contractVersion') != 1):
        return None
    for key in ('sourceSchemaRef', 'sourceItemId', 'sourceFingerprint',
                'generatorVersion', 'outputFingerprint'):
        if not isinstance(provenance.get(key), str) or not provenance[key]:
            return None
    source_revision = provenance.get('sourceRevision')
    if (source_revision is not None
            and (isinstance(source_revision, bool)
                 or not isinstance(source_revision, (str, int, float))
                 or (isinstance(source_revision, str) and not source_revision)
                 or (isinstance(source_revision, float) and not math.isfinite(source_revision)))):
        return None
    if provenance.get('conflictPolicy') not in _HOST_CONFLICT_POLICIES:
        return None
    generated_at = metadata.get('generatedAt')
    if (generated_at is not None
            and (isinstance(generated_at, bool) or not isinstance(generated_at, (int, float))
                 or isinstance(generated_at, float) and not math.isfinite(generated_at))):
        return None
    source_map_entry_id = metadata.get('sourceMapEntryId')
    if (source_map_entry_id is not None
            and (not isinstance(source_map_entry_id, str) or not source_map_entry_id)):
        return None
    return {'extensionId': extension_id, 'contributionId': contribution_id}


def _producer_app(ctx, ref, incoming):
    """Update an established generated carrier; never adopt a raw/user clip."""
    current = ctx.read(ref, ['app'])
    if not isinstance(current, dict):
        raise CommandError('clip.set app leaves require an existing generated clip',
                           kind='unsupported_ownership', ref=ref)
    managed_by = current.get('managedBy')
    has_managed_by = 'managedBy' in current
    if has_managed_by and (not isinstance(managed_by, str) or managed_by == ''):
        raise CommandError('clip.set app leaves require an existing managed clip',
                           kind='unsupported_ownership', ref=ref)
    ctx.read(ref, ['app', 'managedBy'])
    if '__generated__' not in incoming:
        if 'managedBy' in incoming and incoming['managedBy'] != managed_by:
            raise CommandError('clip.set cannot change clip ownership', kind='unsupported_ownership', ref=ref)
        return
    metadata = incoming['__generated__']
    previous = current.get('__generated__')
    declared = _generated_context(metadata)
    established = _generated_context(previous)
    if declared is None or established is None:
        raise CommandError('clip.set generated metadata has unknown or malformed provenance',
                           kind='unsupported_ownership', ref=ref)
    ctx.read(ref, ['app', '__generated__'])
    # Main's fresh birth carries the host-generated identity but no managedBy.
    # The exact persisted extension/contribution pair is the only private
    # source-only owner fallback; it is never materialized as managedBy.
    if not has_managed_by:
        managed_by = established['extensionId']
    if declared['extensionId'] != managed_by:
        raise CommandError('clip.set generated metadata owner does not match managedBy',
                           kind='unsupported_ownership', ref=ref)
    for key in _GENERATED_IDENTITY:
        if metadata.get(key) != previous.get(key):
            raise CommandError('clip.set cannot adopt or change generated metadata identity',
                               kind='unsupported_ownership', ref=ref)
    for key in _GENERATED_FIXED_FIELDS:
        if metadata.get(key) != previous.get(key):
            raise CommandError('clip.set generated metadata identity changed',
                               kind='unsupported_ownership', ref=ref)


def _producer_text(ctx, ref, incoming):
    if not _TEXT_LEAVES.issuperset(incoming):
        raise CommandError('clip.set text contains an unsupported leaf', ref=ref)
    current = ctx.read(ref, ['text'])
    if current is not None and not isinstance(current, dict):
        raise CommandError('clip.set text requires an object', ref=ref)
    if current is None:
        ctx.object(ref, ['text'])
    for key in sorted(incoming):
        ctx.write(ref, ['text', key], incoming[key])


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
    for key in sorted(values):
        if key == 'app':
            _producer_app(ctx, ref, values[key])
            for leaf in sorted(values[key]):
                ctx.write(ref, ['app', leaf], values[key][leaf])
        elif key == 'text':
            _producer_text(ctx, ref, values[key])
        else:
            ctx.write(ref, [key], values[key])
    for key in sorted(clear):
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
