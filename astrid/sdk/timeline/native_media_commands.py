"""Bounded parent media swap between existing, explicitly pinned registry slots.

Runtime supplies VerifiedMedia through selected_media, outside deterministic
execution. No registry allocation, media lookup, timing rewrite or acquisition
lives here. Occurrence, clear, audio-follow and new-slot authoring are future work.
"""
from __future__ import annotations

import copy
import re

from ._command_state import CommandError, equal
from .capture import RELATIONS, number


def _verified(ctx, pin):
    matches = [row for row in ctx.verified_media if equal(row.get('selection'), pin)]
    if not matches or any(not equal(row, matches[0]) for row in matches):
        raise CommandError('swap requires exact Runtime-verified media input', kind='dependency_changed')
    value = matches[0]
    media_type = value.get('media_type')
    kind = media_type.split('/')[0] if isinstance(media_type, str) and '/' in media_type else None
    if kind not in ('image', 'video') or type(value.get('size')) is not int or value['size'] <= 0:
        raise CommandError('swap v1 requires verified image/video metadata', kind='unsupported_media')
    if kind == 'video':
        number(value.get('duration_seconds'), 'intrinsic duration', positive=True)
    return value, kind


def _registry(ctx, pin, value, kind):
    # Read both supported parent codecs, including absence. Never resolve a
    # display ID or search some other owner for a conveniently matching object.
    entries = [ctx.read('parent', [*prefix, 'registry', 'assets', pin['asset']])
               for prefix in ([], ['config'])]
    entries = [entry for entry in entries if entry is not None]
    if not entries or any(not isinstance(entry, dict) for entry in entries):
        raise CommandError('swap requires an existing explicit registry binding', kind='identity_conflict')
    for entry in entries:
        if entry.get('media_id') != pin['object_id'] or entry.get('type') not in (kind, value['media_type']):
            raise CommandError('registry binding differs from verified media', kind='dependency_changed')
        for key in ('object_id', 'digest', 'content_digest', 'content_sha256'):
            if key in entry and entry[key] != (pin['object_id'][7:] if key == 'content_sha256' else pin['object_id']):
                raise CommandError('contradictory registry media identity', kind='dependency_changed')
        for key, field in (('generationId', 'generation_id'), ('variantId', 'variant_id')):
            if key in entry and entry[key] != pin[field]:
                raise CommandError('registry generation/variant differs from selection', kind='dependency_changed')
        if any(entry.get(key) is not None for key in ('file', 'path', 'local_path', 'src', 'source', 'format')):
            raise CommandError('swap v1 does not support registry source locators', kind='unsupported_media')


def swap_media(ctx, command):
    ref = command['select']
    if not isinstance(ref, str) or not re.fullmatch(r'parent/clip:(?!.*::)[^/]+', ref):
        raise CommandError('clip.swap-media v1 requires an existing parent clip identity')
    if ctx.select('media.target', 'parent', [ref]) != [ref]:
        raise CommandError('swap target disappeared', kind='identity_conflict', ref=ref)
    clip = ctx.read(ref)
    old, new = command['args']['old_media'], command['args']['media']
    if clip.get('clipType') not in ('media', 'image', 'video') or clip.get('asset') != old['asset']:
        raise CommandError('swap requires the exact old media selection', kind='dependency_changed', ref=ref)
    if any(key in clip for key in ('asset_id', 'media_id', 'object_id', 'clip_type')):
        raise CommandError('swap v1 requires one asset selector', kind='unsupported_media', ref=ref)
    for key in ('time_map', 'timeMap', 'clips', 'children', 'from_ms', 'to_ms', 'source',
                'sourceURL', 'sourceUrl', 'source_url', 'src', 'source_uuid', 'anchor'):
        if clip.get(key) is not None:
            raise CommandError(f'swap v1 does not support {key}', kind='unsupported_timing', ref=ref)
    app = clip.get('app')
    nested = app.get('astrid') if isinstance(app, dict) else None
    for container in (clip, app, nested):
        if container is not None and not isinstance(container, dict):
            raise CommandError('swap intent containers must be objects or null', ref=ref)
        if isinstance(container, dict):
            unsupported = set(RELATIONS) - {'on', 'fixed_start', 'for'}
            if any(container.get(key) is not None for key in (
                    *unsupported, 'beats', 'word', 'words', 'transcript', 'source_id', 'standin', 'standin_intent')):
                raise CommandError('swap v1 requires literal timing without source anchors', kind='unsupported_timing', ref=ref)
            for field, timing in (('on', 'at'), ('for', 'hold')):
                if container.get(field) is not None:
                    number(container[field], field)
                    if not equal(container[field], clip.get(timing)):
                        raise CommandError('swap literal intent contradicts timing', kind='unsupported_timing', ref=ref)
            if container.get('fixed_start') is not None and container['fixed_start'] is not True:
                raise CommandError('swap requires fixed literal timing', kind='unsupported_timing', ref=ref)
    number(clip.get('at'), 'clip.at')
    number(clip.get('hold'), 'clip.hold', positive=True)
    if clip['at'] < 0 or clip.get('at_ms') is not None or any(
            clip.get(key) is not None for key in ('duration', 'duration_ms')):
        raise CommandError('swap v1 requires literal at/hold seconds', kind='unsupported_timing', ref=ref)
    previous, old_kind = _verified(ctx, old)
    replacement, kind = _verified(ctx, new)
    if old_kind != kind:
        raise CommandError('swap v1 preserves media kind', kind='unsupported_media', ref=ref)
    if clip['clipType'] != 'media' and clip['clipType'] != kind:
        raise CommandError('clip type contradicts verified media', kind='unsupported_media', ref=ref)
    track = 'parent/track:' + str(clip.get('track'))
    if ctx.read(track, ['kind']) != 'visual':
        raise CommandError('swap v1 requires a visual track', ref=ref)
    for pin, value in ((old, previous), (new, replacement)):
        _registry(ctx, pin, value, kind)
        ctx.dependency('media.old' if pin is old else 'media.new', 'media', pin)
    speed = clip.get('speed', 1)
    number(speed, 'clip.speed', positive=True)
    if kind == 'image':
        if any(clip.get(key) is not None for key in ('from', 'to')) or speed != 1:
            raise CommandError('still swap requires hold timing without source windows', kind='unsupported_timing', ref=ref)
    else:
        left, right = clip.get('from'), clip.get('to')
        number(left, 'clip.from')
        number(right, 'clip.to', positive=True)
        if left < 0 or right <= left or any(right > row['duration_seconds'] for row in (previous, replacement)):
            raise CommandError('swap source window exceeds verified media', kind='unsupported_timing', ref=ref)
        if not equal((right - left) / speed, clip['hold']):
            raise CommandError('swap source window contradicts hold', kind='unsupported_timing', ref=ref)
    ctx.bind('media.target', ref, dependencies=['media.old', 'media.new'])
    ctx.write(ref, ['asset'], new['asset'])


def capture_swap_media(bundle, select, old_media, media, *, verified_media):
    """Capture once against the authored base and detached selected_media reads."""
    from .commands import execute

    return execute(bundle, [{'schema_version': 1, 'op': 'clip.swap-media', 'version': '1',
                             'select': select, 'args': {'old_media': copy.deepcopy(old_media),
                                                       'media': copy.deepcopy(media)}}],
                   verified_media=verified_media).commands[0]
