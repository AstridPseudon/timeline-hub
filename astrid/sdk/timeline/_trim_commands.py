"""Bounded source trim of literal parent media, without refreshing media."""
from __future__ import annotations

import copy
import re

from astrid.sdk import timeline_intent as intent

from ._command_state import CommandError, equal
from ._common import TimelineEditError
from .capture import CLIP_FIELDS, RELATIONS, number
from .units import trim_source_interval


def clip_trim(ctx, command):
    ref = command['select']
    if not isinstance(ref, str) or not re.fullmatch(r'parent/clip:[^/]+', ref) or '::' in ref:
        raise CommandError('clip.trim v1 requires a literal parent clip identity')
    if ctx.read(ref, ['id']) is None:
        raise CommandError('trim target disappeared', kind='identity_conflict', ref=ref)
    fields = (*CLIP_FIELDS, 'sourceURL', 'sourceUrl', 'source_url', 'src', 'source_uuid',
              'source', 'source_window', 'source_offset', 'anchor', 'animation', 'animations', 'keyframes', 'curves')
    clip = {key: ctx.read(ref, [key]) for key in fields}
    for key in ('at_ms', 'from_ms', 'to_ms', 'duration', 'duration_ms', 'time_map', 'timeMap',
                'clips', 'children', *fields[len(CLIP_FIELDS):]):
        if clip[key] is not None:
            raise CommandError(f'clip.trim v1 does not support {key}', kind='unsupported_timing', ref=ref)
    for key in ('animation', 'animations', 'keyframes', 'curves'):
        if ctx.read(ref, ['params', key]) is not None:
            raise CommandError(f'clip.trim v1 does not support params.{key}', kind='unsupported_timing', ref=ref)
    app = ctx.read(ref, ['app'])
    if app is not None and not isinstance(app, dict):
        raise CommandError('trim intent container must be object or null', ref=ref)
    nested = app.get('astrid') if isinstance(app, dict) else None
    if nested is not None and not isinstance(nested, dict):
        raise CommandError('trim intent container must be object or null', ref=ref)
    for prefix, container in (([], clip), (['app'], app), (['app', 'astrid'], nested)):
        for key in (*RELATIONS, 'anchor', 'standin', 'standin_intent', 'animation', 'animations'):
            value = ctx.read(ref, prefix + [key]) if not prefix else (container or {}).get(key)
            if key == 'fixed_start' and value in (None, True):
                continue
            if key == 'for' and prefix and value is not None:
                number(value, 'for', positive=True)
            elif value is not None:
                raise CommandError(f'clip.trim v1 does not support {key}', kind='unsupported_timing', ref=ref)
    if clip['clipType'] not in (None, 'media') or clip['clip_type'] not in (None, 'media'):
        raise CommandError('clip.trim applies to media clips', ref=ref)
    asset = clip['asset']
    if not isinstance(asset, str) or not asset or any(clip[key] is not None for key in
            ('asset_id', 'media_id', 'object_id')):
        raise CommandError('clip.trim requires the current registry asset identity', ref=ref)
    start = number(clip['at'], 'clip.at')
    if start < 0:
        raise CommandError('clip.trim requires a non-negative literal start', ref=ref)
    if clip['hold'] is not None:
        number(clip['hold'], 'clip.hold', positive=True)
    speed = 1 if clip['speed'] is None else clip['speed']
    number(speed, 'clip.speed', positive=True)
    source = {key: ctx.read('parent/registry', ['assets', asset, key]) for key in
              ('media_id', 'object_id', 'digest', 'content_digest', 'type', 'duration',
               'duration_ms', 'duration_seconds', 'source', 'source_window', 'time_map', 'timeMap')}
    if any(source[key] is not None for key in ('source', 'source_window', 'time_map', 'timeMap')):
        raise CommandError('clip.trim v1 does not support a mapped media source', kind='unsupported_map', ref=ref)
    limit = source['duration']
    number(limit, 'registry source duration', positive=True)
    endpoints = []
    for key, arg, default in (('from', 'in_s', 0), ('to', 'out_s', limit)):
        current = default if clip[key] is None else clip[key]
        number(current, 'clip.' + key)
        value = command['args'].get(arg)
        endpoints.append(current if value is None else value)
    source_in, source_out = endpoints
    if source_in < 0 or source_out > limit or source_out <= source_in:
        raise CommandError(f'source range must fit inside the file (0–{limit:g} s)', ref=ref)
    # ``hold`` is authored source time; playback duration applies ``speed``.
    try:
        source_in, source_out, hold = trim_source_interval(source_in, source_out, limit)
    except TimelineEditError as exc:
        raise CommandError(str(exc), ref=ref) from exc
    ctx.dependency('trim.source', 'entity', {'asset': asset, 'source': source})
    ctx.bind('trim.target', ref, dependencies=['trim.source'])
    for key, value in (('from', source_in), ('to', source_out), ('hold', hold)):
        ctx.write(ref, [key], value)
    # Main's clear helpers also tidy empty/null containers and handle legacy
    # flat intent precedence. Guard the app object they consume as one unit.
    cleared = {'app': copy.deepcopy(app)}
    intent.set_until(cleared, None)
    intent.set_for(cleared, None)
    if 'app' in cleared:
        ctx.write(ref, ['app'], cleared['app'])
    else:
        ctx.clear(ref, ['app'])


def capture_clip_trim(bundle, select, *, in_s=None, out_s=None):
    """Capture original claims. Null endpoints retain the current/default bound."""
    if isinstance(select, str) and select.startswith('occurrence:'):
        raise CommandError('clip.trim v1 select does not match the required parent/clip identity')
    from .commands import execute

    return execute(bundle, [{'schema_version': 1, 'op': 'clip.trim', 'version': '1',
                             'select': select, 'args': {'in_s': in_s, 'out_s': out_s},
                             'intent': {}}]).commands[0]


def _verified_occurrence_source(ctx, owner, asset, source):
    """Resolve the existing selected-media authority for a dormant source trim.

    Occurrence trim has no media argument from which to call ``_verified``.  The
    registry identity is therefore matched to exactly one already-verified
    selection.  The descriptor supplies the intrinsic duration; the authored
    registry remains a guarded identity/source carrier.
    """
    candidates = []
    source_id = source.get('media_id') or source.get('object_id')

    def same_id(left, right):
        if not isinstance(left, str) or not isinstance(right, str):
            return False
        return left.removeprefix('sha256:') == right.removeprefix('sha256:')

    for value in ctx.verified_media:
        selection = value.get('selection') if isinstance(value, dict) else None
        if not isinstance(selection, dict) or selection.get('asset') != asset:
            continue
        selected_id = selection.get('object_id', selection.get('media_id'))
        if not same_id(selected_id, source_id):
            continue
        for selected_key, source_keys in (
                ('catalog_digest', ('digest', 'content_digest', 'content_sha256')),
                ('generation_id', ('generationId', 'generation_id')),
                ('variant_id', ('variantId', 'variant_id'))):
            selected_value = selection.get(selected_key)
            authored_value = next((source.get(key) for key in source_keys
                                   if source.get(key) is not None), None)
            if (selected_value is not None and authored_value is not None
                    and (not same_id(selected_value, authored_value)
                         if selected_key == 'catalog_digest'
                         else selected_value != authored_value)):
                break
        else:
            candidates.append(value)
    if not candidates or any(not equal(value, candidates[0]) for value in candidates[1:]):
        raise CommandError('occurrence trim requires exact Runtime-verified media input',
                           kind='dependency_changed', ref=owner)
    value = candidates[0]
    media_type = value.get('media_type')
    if not isinstance(media_type, str) or not media_type.startswith('video/'):
        raise CommandError('occurrence trim requires verified video metadata',
                           kind='unsupported_media', ref=owner)
    duration = number(value.get('duration_seconds'), 'intrinsic duration', positive=True)
    return value, duration


def _occurrence_trim_intent(ctx, ref, row):
    """Validate v1's static intent allowance and return its cleaned copy."""
    app = ctx.read(ref, ['app'])
    if app is not None and not isinstance(app, dict):
        raise CommandError('trim intent container must be object or null', ref=ref)
    nested = app.get('astrid') if isinstance(app, dict) else None
    if nested is not None and not isinstance(nested, dict):
        raise CommandError('trim intent container must be object or null', ref=ref)
    for prefix, container in (([], row), (['app'], app), (['app', 'astrid'], nested)):
        for key in (*RELATIONS, 'anchor', 'standin', 'standin_intent', 'animation', 'animations'):
            value = ctx.read(ref, prefix + [key]) if not prefix else (container or {}).get(key)
            if key == 'fixed_start' and value in (None, True):
                continue
            if key == 'for' and prefix and value is not None:
                number(value, 'for', positive=True)
            elif value is not None:
                raise CommandError(f'clip.trim v2 does not support {key}',
                                   kind='unsupported_timing', ref=ref)
    if app is None:
        return None
    cleared = {'app': copy.deepcopy(app)}
    intent.set_until(cleared, None)
    intent.set_for(cleared, None)
    return cleared.get('app')


def _clip_trim_v2(ctx, command):
    """Dormant occurrence-owned source-window trim recipe.

    This handler is intentionally not installed in ``operations()``.  It is a
    source agreement artifact until the peer ACK and an explicit activation
    decision; parent ``clip.trim`` v1 remains the only live operation.
    """
    ref = command['select']
    if not isinstance(ref, str) or not re.fullmatch(r'occurrence:(?!.*::)[^/]+/clip:(?!.*::)[^/]+', ref):
        raise CommandError('clip.trim v2 requires a literal occurrence raw child identity')
    owner = ref.rsplit('/', 1)[0]
    from .native_occurrence_media_commands import _exclusive, _owner

    owner, limit = _owner(ctx, ref, child=True)
    _exclusive(ctx, owner)
    if ref not in ctx.select('collection.clips', owner):
        raise CommandError('trim target disappeared', kind='identity_conflict', ref=ref)
    fields = (*CLIP_FIELDS, 'sourceURL', 'sourceUrl', 'source_url', 'src', 'source_uuid',
              'source', 'source_window', 'anchor', 'animation', 'animations', 'keyframes', 'curves')
    row = copy.deepcopy(ctx.state.entity(ref))
    for key in fields:
        ctx.read(ref, [key])
    if row.get('id') is None:
        raise CommandError('trim target disappeared', kind='identity_conflict', ref=ref)
    for key in ('animation', 'animations', 'keyframes', 'curves'):
        if ctx.read(ref, ['params', key]) is not None:
            raise CommandError(f'clip.trim v2 does not support params.{key}',
                               kind='unsupported_timing', ref=ref)
    if row.get('clipType') not in ('media', 'video') or row.get('clip_type') is not None:
        raise CommandError('clip.trim v2 applies to video media clips', ref=ref)
    asset = row.get('asset')
    if not isinstance(asset, str) or not asset or any(row.get(key) is not None
                                                      for key in ('asset_id', 'media_id', 'object_id')):
        raise CommandError('clip.trim v2 requires the current registry asset identity', ref=ref)
    if row.get('from') is None or row.get('to') is None or row.get('hold') is None:
        raise CommandError('clip.trim v2 requires an existing source window',
                           kind='unsupported_timing', ref=ref)
    source = {key: ctx.read(owner + '/registry', ['assets', asset, key]) for key in
              ('media_id', 'object_id', 'digest', 'content_digest', 'content_sha256', 'type',
               'duration', 'duration_ms', 'duration_seconds', 'source', 'source_window',
               'time_map', 'timeMap')}
    if any(source[key] is not None for key in ('source', 'source_window', 'time_map', 'timeMap')):
        raise CommandError('clip.trim v2 does not support a mapped media source',
                           kind='unsupported_map', ref=ref)
    verified, duration = _verified_occurrence_source(ctx, owner, asset, source)
    source_type = source.get('type')
    if source_type is not None and not str(source_type).startswith('video/') and source_type != 'video':
        raise CommandError('occurrence trim requires a video registry source',
                           kind='unsupported_media', ref=owner)
    source['duration_seconds'] = duration

    current_in, current_out = number(row['from'], 'clip.from'), number(row['to'], 'clip.to')
    current_hold = number(row['hold'], 'clip.hold', positive=True)
    if current_in < 0 or current_out <= current_in or not equal(current_out - current_in, current_hold):
        raise CommandError('source window differs from hold', kind='unsupported_timing', ref=ref)
    endpoints = []
    for key, arg, default in (('from', 'in_s', current_in), ('to', 'out_s', current_out)):
        value = command['args'].get(arg)
        value = default if value is None else number(value, 'clip.' + key)
        endpoints.append(value)
    source_in, source_out = endpoints
    if source_in < 0 or source_out > duration or source_out <= source_in:
        raise CommandError(f'source range must fit inside the file (0–{duration:g} s)', ref=ref)
    try:
        source_in, source_out, hold = trim_source_interval(source_in, source_out, duration)
    except TimelineEditError as exc:
        raise CommandError(str(exc), ref=ref) from exc

    cleaned_app = _occurrence_trim_intent(ctx, ref, row)
    candidate = copy.deepcopy(row)
    candidate.update({'from': source_in, 'to': source_out, 'hold': hold})
    if cleaned_app is not None:
        candidate['app'] = cleaned_app
    from .native_occurrence_media_commands import _clip

    # ``_clip`` supplies the existing timing/track guards. Intent was checked
    # above because its static ``fixed_start`` marker is legal for trim but is
    # intentionally refused by media birth/swap.
    timing_candidate = copy.deepcopy(candidate)
    timing_candidate.pop('app', None)
    _clip(ctx, owner, timing_candidate, limit, 'video', [verified])
    ctx.dependency('trim.source', 'entity', {'owner': owner, 'asset': asset, 'source': source})
    ctx.bind('trim.target', ref, dependencies=['trim.source'])
    for key, value in (('from', source_in), ('to', source_out), ('hold', hold)):
        ctx.write(ref, [key], value)
    if row.get('app') is not None:
        ctx.write(ref, ['app'], cleaned_app)


def _capture_clip_trim_v2(bundle, select, *, in_s=None, out_s=None, verified_media=()):
    """Capture the dormant recipe without registering or accepting the command."""
    from ._recording import Recording

    command = {'schema_version': 1, 'op': 'clip.trim', 'version': '2', 'select': select,
               'args': {'in_s': in_s, 'out_s': out_s}, 'intent': {}}
    recorder = Recording(copy.deepcopy(bundle), command, 0, verified_media=verified_media)
    _clip_trim_v2(recorder, command)
    return recorder.finish(capture=True)['command']


def _record_clip_trim_v2(bundle, select, *, in_s=None, out_s=None, verified_media=()):
    """Return the dormant candidate and recorder facts for source-only tests."""
    from ._recording import Recording

    command = {'schema_version': 1, 'op': 'clip.trim', 'version': '2', 'select': select,
               'args': {'in_s': in_s, 'out_s': out_s}, 'intent': {}}
    recorder = Recording(copy.deepcopy(bundle), command, 0, verified_media=verified_media)
    _clip_trim_v2(recorder, command)
    record = recorder.finish(capture=True)
    return recorder.state.bundle, record
