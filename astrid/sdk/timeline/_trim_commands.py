"""Bounded source trim of literal parent media, without refreshing media."""
from __future__ import annotations

import copy
import re

from astrid.sdk import timeline_intent as intent

from ._command_state import CommandError
from ._common import TimelineEditError
from ._recording import active
from .capture import CLIP_FIELDS, RELATIONS, number
from .units import trim_source_interval


def _media_kind(value):
    media_type = (value.get('type') if 'type' in value else value.get('media_type')) \
        if isinstance(value, dict) else None
    if isinstance(media_type, str):
        return media_type.split('/', 1)[0]
    return None


def _verified_source_duration(ctx, source, expected_kind):
    """Use request-scoped Runtime metadata when authored duration is absent."""
    limit = source['duration']
    if limit is not None:
        number(limit, 'registry source duration', positive=True)
        return limit, None
    object_id = next((source.get(key) for key in
                      ('object_id', 'media_id', 'digest', 'content_digest')
                      if source.get(key) is not None), None)
    if object_id is None:
        raise CommandError('registry source duration requires an exact media identity',
                           kind='dependency_changed')
    matches = [value for value in ctx.verified_media
               if isinstance(value, dict) and 'selection' not in value
               and value.get('object_id') == object_id]
    if not matches or any(value != matches[0] for value in matches):
        raise CommandError('registry source duration requires exact Runtime-verified media metadata',
                           kind='dependency_changed')
    value = matches[0]
    if value.get('object_id') != object_id or _media_kind(value) != expected_kind \
            or type(value.get('size')) is not int or value['size'] <= 0:
        raise CommandError('trim source media metadata is not exact audio media',
                           kind='unsupported_media')
    media_id = source.get('media_id') or object_id
    content_digest = source.get('content_digest') or source.get('digest') or media_id
    pin = {'media_id': media_id, 'content_digest': content_digest}
    limit = ctx.read_media(pin, ['duration_seconds'])
    number(limit, 'intrinsic duration', positive=True)
    return limit, value


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
    if clip['clipType'] not in (None, 'media', 'audio') or clip['clip_type'] not in (None, 'media', 'audio'):
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
    source_kind = _media_kind(source)
    clip_kind = 'audio' if 'audio' in (clip['clipType'], clip['clip_type'], source_kind) else source_kind
    if clip_kind == 'audio':
        track = ctx.read('parent/track:' + str(clip['track']))
        if not isinstance(track, dict) or track.get('kind') != 'audio' or not active(track):
            raise CommandError('clip.trim requires an active raw audio track', ref=ref)
        if source_kind != 'audio':
            raise CommandError('clip.trim audio track requires an audio registry asset', ref=ref)
    limit, _ = _verified_source_duration(ctx, source, clip_kind)
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


def capture_clip_trim(bundle, select, *, in_s=None, out_s=None, verified_media=()):
    """Capture original claims. Null endpoints retain the current/default bound."""
    from .commands import execute

    return execute(bundle, [{'schema_version': 1, 'op': 'clip.trim', 'version': '1',
                             'select': select, 'args': {'in_s': in_s, 'out_s': out_s},
                             'intent': {}}], verified_media=verified_media).commands[0]
