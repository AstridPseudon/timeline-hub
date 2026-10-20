"""Occurrence-only media recipes over raw children and detached Runtime inputs."""
from __future__ import annotations

import copy
import re

from ._command_state import ABSENT, CommandError, equal
from ._media_inputs import _verified
from ._recording import active
from .capture import MAP_FIELDS, RELATIONS, number, occurrence_start, rate

MEDIA_INTENT = {'ownership': 'occurrence'}


def _owner(ctx, ref, *, child=False):
    pattern = r'occurrence:(?!.*::)[^/]+' + (r'/clip:(?!.*::)[^/]+' if child else '')
    if not isinstance(ref, str) or not re.fullmatch(pattern, ref):
        raise CommandError('media edit requires explicit occurrence/raw child ownership')
    owner = ref.rsplit('/', 1)[0] if child else ref
    ctx.select('collection.occurrences', 'parent')
    ctx.read(owner, ['occurrence_id'])
    ctx.read(owner + '/shot', ['shot_id'])
    for path in MAP_FIELDS:
        ctx.read(owner, path)
    row = ctx.state.occurrence(owner)
    occurrence_start(row)
    if (not active(row) or isinstance(row.get('source_offset'), bool) or isinstance(row.get('speed'), bool)
            or row.get('source_offset') not in (None, 0)
            or row.get('speed') not in (None, 1)
            or any(row.get(key) is not None for key in ('time_map', 'timeMap'))):
        raise CommandError('media edit requires an active translation-only occurrence', kind='unsupported_map')
    number(row.get('duration_ms'), 'occurrence.duration_ms', positive=True)
    fps = rate(ctx.read('parent', ['config', 'output', 'fps']))
    if rate(ctx.read(owner + '/source', ['output', 'fps'])) != fps:
        raise CommandError('parent and child fps differ', kind='unsupported_timing')
    if ctx.read(owner + '/source', ['source_window']) is not None:
        raise CommandError('internal source_window is unsupported', kind='unsupported_map')
    ctx.bind('media.owner', owner)
    return owner, row['duration_ms'] / 1000


def _exclusive(ctx, owner):
    if ctx.select('placement.owners', owner) != [owner]:
        raise CommandError('shared authored placement is unsupported', kind='unsupported_ownership', ref=owner)


def _consume(ctx, owner, ids):
    """Record the clip rows an automatic builder read, so a later change conflicts at replay."""
    members = ctx.select('collection.clips', owner)
    for clip_id in ids:
        ref = owner + '/clip:' + clip_id
        if ref not in members:
            raise CommandError('consumed clip is not in the occurrence', kind='identity_conflict', ref=ref)
        ctx.read(ref)


def _binding(pin, kind):
    return {'media_id': pin['object_id'], 'type': kind,
            'generationId': pin['generation_id'], 'variantId': pin['variant_id']}


def _registry(ctx, owner, pin, kind, *, create=False, alias=None):
    identity = pin['asset'] if alias is None else alias
    if not isinstance(identity, str) or not re.fullmatch(r'(?!.*::)[^/]+', identity):
        raise CommandError('media requires a reserved raw asset alias')
    # Containers must already exist. Never replace null/opaque registry state.
    registry = ctx.state.config(owner).get('registry')
    if not isinstance(registry, dict) or not isinstance(registry.get('assets'), dict):
        raise CommandError('media edit requires an authored asset registry')
    ref = owner + '/asset:' + identity
    expected = _binding(pin, kind)
    entry = ctx.read(ref)
    if ctx.state.get(ref, []) == ABSENT and create:
        ctx.create_asset(owner, identity, expected)
    elif create:
        if not equal(entry, expected):
            raise CommandError('existing registry binding differs from exact selection', kind='dependency_changed')
    elif (not isinstance(entry, dict) or entry.get('media_id') != pin['object_id']
          or entry.get('type') != kind
          or any(key in entry and entry[key] != value for key, value in expected.items())):
        raise CommandError('old registry binding differs from selection', kind='dependency_changed')
    if not create and any(key in entry for key in ('object_id', 'digest', 'content_digest', 'content_sha256',
                                                  'file', 'path', 'local_path', 'src', 'source', 'format')):
        raise CommandError('unsupported old registry identity codec', kind='unsupported_media')
    ctx.dependency('media.new' if create else 'media.old', 'media', pin)
    return ref


def _clip(ctx, owner, row, limit, kind, verified):
    if row.get('clipType') not in ('media', kind) or not isinstance(row.get('asset'), str):
        raise CommandError('media edit requires one matching media clip')
    if any(key in row for key in ('asset_id', 'media_id', 'object_id', 'clip_type')):
        raise CommandError('media edit requires one asset selector')
    for key in ('time_map', 'timeMap', 'clips', 'children', 'from_ms', 'to_ms', 'at_ms',
                'duration', 'duration_ms', 'source', 'sourceURL', 'sourceUrl', 'source_url',
                'src', 'source_uuid', 'anchor', 'transition'):
        if row.get(key) is not None:
            raise CommandError(f'media edit does not support {key}', kind='unsupported_timing')
    app = row.get('app')
    nested = app.get('astrid') if isinstance(app, dict) else None
    for container in (row, app, nested):
        if container is not None and not isinstance(container, dict):
            raise CommandError('intent container must be object or null')
        if isinstance(container, dict) and any(container.get(key) is not None for key in (
                *RELATIONS, 'beats', 'word', 'words', 'transcript', 'source_id', 'standin', 'standin_intent')):
            raise CommandError('media edit requires literal child timing', kind='unsupported_timing')
    at = number(row.get('at'), 'clip.at')
    hold = number(row.get('hold'), 'clip.hold', positive=True)
    speed = number(row.get('speed', 1), 'clip.speed', positive=True)
    if at < 0 or at + hold / speed > limit:
        raise CommandError('child interval exceeds occurrence', kind='occurrence_boundary')
    if kind == 'image':
        if speed != 1 or any(row.get(key) is not None for key in ('from', 'to')):
            raise CommandError('image requires hold without a source window', kind='unsupported_timing')
    else:
        left, right = number(row.get('from'), 'clip.from'), number(row.get('to'), 'clip.to')
        if left < 0 or right <= left or not equal(right - left, hold) or any(
                right > value['duration_seconds'] for value in verified):
            raise CommandError('source window differs from hold or exceeds media', kind='unsupported_timing')
    track = owner + '/track:' + str(row.get('track'))
    ctx.select('collection.tracks', owner)
    value = ctx.read(track)
    if (not isinstance(value, dict) or value.get('kind') != 'visual'
            or value.get('role', 'output') != 'output' or not active(value)):
        raise CommandError('media edit requires an active raw visual child track')
    ctx.bind('media.track', track)


def add_media(ctx, command):
    owner, limit = _owner(ctx, command['select'])
    _exclusive(ctx, owner)
    # Automatic births also depend on promotion and legacy-group eligibility.
    # Keep absent fields guarded even when no pool removal follows the birth.
    ctx.read(owner + '/source', ['app', 'astrid', 'pool'])
    ctx.read('parent', ['config', 'pinnedShotGroups'])
    row, pin = command['args']['row'], command['args']['media']
    _consume(ctx, owner, command['args'].get('consumed', ()))
    value, kind = _verified(ctx, pin)
    if row.get('asset') != pin['asset']:
        raise CommandError('child asset must equal the reserved selection alias')
    _clip(ctx, owner, row, limit, kind, [value])
    _registry(ctx, owner, pin, kind, create=True)
    ctx.create(owner, 'clip', row)


def swap_media(ctx, command):
    ref = command['select']
    owner, limit = _owner(ctx, ref, child=True)
    ctx.select('collection.clips', owner)
    row = ctx.read(ref)
    if not isinstance(row, dict):
        raise CommandError('missing raw child identity', kind='identity_conflict')
    old, pin = command['args']['old_media'], command['args']['media']
    previous, old_kind = _verified(ctx, old)
    value, kind = _verified(ctx, pin)
    if old_kind != kind:
        raise CommandError('media swap preserves media kind', kind='unsupported_media')
    _clip(ctx, owner, row, limit, kind, [previous, value])
    _registry(ctx, owner, old, kind, alias=row['asset'])
    _registry(ctx, owner, pin, kind, create=True)
    ctx.bind('media.target', ref, dependencies=['media.old', 'media.new'])
    ctx.write(ref, ['asset'], pin['asset'])


def capture_occurrence_add_media(bundle, owner, row, media, *, verified_media, consumed=()):
    """Caller keeps the selected asset alias and allocates row.id before capture."""
    from .commands import execute
    args = {'row': copy.deepcopy(row), 'media': copy.deepcopy(media)}
    if consumed:
        args['consumed'] = list(consumed)
    return execute(bundle, [{'schema_version': 1, 'op': 'occurrence.add-media', 'version': '1',
                             'select': owner, 'args': args, 'intent': MEDIA_INTENT}], verified_media=verified_media).commands[0]


def capture_occurrence_swap_media(bundle, select, old_media, media, *, verified_media):
    """Select an unprojected child; display occurrence:clip IDs are not raw IDs."""
    from .commands import execute
    return execute(bundle, [{'schema_version': 1, 'op': 'occurrence.swap-media', 'version': '1',
                             'select': select, 'args': {'old_media': copy.deepcopy(old_media),
                                                       'media': copy.deepcopy(media)},
                             'intent': MEDIA_INTENT}], verified_media=verified_media).commands[0]
