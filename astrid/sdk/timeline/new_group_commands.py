"""Explicit, recorded consumption of legacy parent groups into canonical owners."""
from __future__ import annotations

import copy
from fractions import Fraction

from astrid.core.timeline.authoring_bundle import _clip_selected_media, _digest
from astrid.core.timeline.shot_composition_migration import (
    MigrationAmbiguityError,
    _require_legacy_group_contiguous,
)

from ._command_state import CommandError
from .capture import RELATIONS, _duration, number, rate


def _fraction(value, label, *, positive=False):
    number(value, label, positive=positive)
    return Fraction(str(value))


def _literal(value):
    result = float(value)
    if Fraction(str(result)) != value:
        raise CommandError('migration timing is not exactly representable')
    return result


def _geometry(row):
    for key in ('at_ms', 'duration', 'duration_ms', 'from_ms', 'to_ms', 'time_map',
                'timeMap', 'source_map', 'sourceMap', 'source_offset', 'clips', 'children',
                'anchor', 'clip_type'):
        if row.get(key) is not None:
            raise CommandError(f'migration does not support {key}', kind='unsupported_timing')
    if row.get('clipType') == 'shot':
        raise CommandError('nested legacy shots require a separate migration')
    app = row.get('app')
    nested = app.get('astrid') if isinstance(app, dict) else None
    for container in (row, app, nested):
        if container is not None and not isinstance(container, dict):
            raise CommandError('migration intent container must be object or null')
        for key in (*RELATIONS, 'anchor', 'standin', 'standin_intent'):
            value = container.get(key) if isinstance(container, dict) else None
            if value is not None and not (key == 'fixed_start' and value is True):
                raise CommandError(f'migration requires fixed timing; found {key}')
    start = _fraction(row.get('at'), 'clip.at')
    if start < 0:
        raise CommandError('migration requires nonnegative starts')
    speed = _fraction(row['speed'], 'clip.speed', positive=True) if row.get('speed') is not None else Fraction(1)
    duration = (_fraction(row['hold'], 'clip.hold', positive=True) if row.get('hold') is not None
                else _fraction(row.get('to'), 'clip.to') - _fraction(row.get('from'), 'clip.from')) / speed
    _duration(row)
    return start, start + duration


def migrate_groups(ctx, command):
    manifest = ctx.state.bundle['source_mapping'].get('_runtime_document', {}).get('dependency_manifest', {})
    for pin in manifest.get('documents', []):
        kind = 'transcript' if pin['document_id'].startswith('transcript:') else 'source'
        ctx.dependency('migration.document:' + _digest(pin), kind, pin)
    groups = ctx.read('parent', ['config', 'pinnedShotGroups'])
    proposed = command['args']['groups']
    if not isinstance(groups, list) or not groups or any(not isinstance(g, dict) for g in groups):
        raise CommandError('migration requires an authored nonempty group array')
    legacy_ids = [g.get('shotId') for g in groups]
    if (any(not isinstance(identity, str) or not identity for identity in legacy_ids)
            or len(set(legacy_ids)) != len(legacy_ids)
            or legacy_ids != [g['legacy_shot_id'] for g in proposed]):
        raise CommandError('migration must map every unique group in authored order')
    for key in ('shot_id', 'occurrence_id'):
        if len({g[key] for g in proposed}) != len(proposed):
            raise CommandError('migration destination identities must be unique')
    ctx.select('migration.groups', 'parent', ['occurrence:' + g['occurrence_id'] for g in proposed])
    clips = ctx.select('collection.clips', 'parent')
    ctx.select('collection.occurrences', 'parent')
    ctx.select('collection.shots', 'parent')
    tracks = [ctx.read(ref) for ref in ctx.select('collection.tracks', 'parent')]
    output = ctx.read('parent', ['config', 'output'])
    fps = rate((output or {}).get('fps'))
    # Guard both registry declarations; the shared authority rule rejects divergence.
    ctx.read('parent', ['registry'])
    ctx.read('parent', ['config', 'registry'])
    try:
        registry = ctx.read('parent/registry')
    except ValueError as exc:
        raise CommandError(str(exc)) from exc
    raw = [ctx.state.entity(ref) for ref in clips]
    consumed, prepared = set(), []
    for index, (group, destination) in enumerate(zip(groups, proposed)):
        ids = group.get('clipIds')
        if (not isinstance(ids, list) or any(not isinstance(i, str) for i in ids)
                or consumed.intersection(ids)):
            raise CommandError('migration requires disjoint ordered member identities')
        try:
            positions = _require_legacy_group_contiguous(
                project_id=ctx.state.bundle['project_id'], timeline_id=ctx.state.bundle['timeline_id'],
                group_id=group['shotId'], clip_ids=ids, clips=raw)
        except MigrationAmbiguityError as exc:
            raise CommandError(str(exc)) from exc
        # Physical shot-item IDs are global; v1 has no preallocated item mapping.
        if group.get('items') not in (None, []):
            raise CommandError('migration items require explicit preallocated identity mapping')
        members = [ctx.read(clips[pos]) for pos in positions]
        geometry = [_geometry(row) for row in members]
        start, end = min(g[0] for g in geometry), max(g[1] for g in geometry)
        span = (end - start) * 1000
        if span.denominator != 1:
            raise CommandError('migration duration is not exactly representable in milliseconds')
        lanes = {row.get('track') for row in members}
        if len(lanes) != 1 or not isinstance(next(iter(lanes)), str):
            raise CommandError('migration requires one lane')
        lane = next(iter(lanes))
        if group.get('trackId', lane) != lane or any(
                group.get(key) is not None for key in ('time_map', 'timeMap', 'source_offset', 'speed')):
            raise CommandError('migration group has ambiguous lane or unsupported source map')
        if lane not in {row['id'] for row in tracks}:
            raise CommandError('migration member track is missing')
        for j, row in enumerate(members):
            if row.get('output') is not None and rate(row['output'].get('fps')) != fps:
                raise CommandError('migration child fps differs')
            if any(key in row for key in ('asset', 'asset_id', 'media_id', 'object_id')):
                media = _clip_selected_media(row, {'registry': registry}, 'migration member')
                pin = next((p for p in manifest.get('media', []) if p['media_id'] == media), None)
                if pin is None:
                    raise CommandError('migration selected media has no immutable pin')
                ctx.dependency(f'migration.media:{index}:{j}', 'media', pin)
            ctx.bind(f'migration.member:{index}:{j}', 'parent/clip:' + row['id'])
            ctx.bind(f'migration.destination:{index}:{j}', 'occurrence:' + destination['occurrence_id'] + '/clip:' + row['id'])
            row['at'] = _literal(geometry[j][0] - start)
        shot_ref, occurrence_ref = 'shot:' + destination['shot_id'], 'occurrence:' + destination['occurrence_id']
        ctx.bind(f'migration.shot:{index}', shot_ref)
        ctx.bind(f'migration.group:{index}', occurrence_ref)
        internal = {'tracks': copy.deepcopy(tracks), 'clips': members,
                    'registry': copy.deepcopy(registry)}
        if output is not None:
            internal['output'] = copy.deepcopy(output)
        occurrence = {'occurrence_id': destination['occurrence_id'], 'shot_id': destination['shot_id'],
                      'track': lane, 'placement': {'start_ms': _literal(start * 1000), 'track': lane},
                      'duration_ms': int(span), 'source_offset': 0, 'speed': 1,
                      'provenance': {'group_migration': {
                          'legacy_group': copy.deepcopy(group),
                          'members': [{'legacy_clip_id': i, 'clip_id': i} for i in ids]}}}
        prepared.append((shot_ref, occurrence_ref, internal, occurrence, ids))
        consumed.update(ids)
    for shot_ref, occurrence_ref, internal, occurrence, ids in prepared:
        ctx.create_entity(shot_ref, kind='shot', owner=None,
                          value={'payload': {'items': []}, 'internal_timeline': internal})
        ctx.create_entity(occurrence_ref, kind='occurrence', owner='parent', value=occurrence)
        for identity in ids:
            ctx.clear('parent/clip:' + identity, [])
    ctx.clear('parent', ['config', 'pinnedShotGroups'])


def capture_migrate_groups(document, groups):
    """The explicit legacy-read entry: destinations are allocated by the caller."""
    from .commands import execute
    from .commit import bundle_from_document

    command = {'schema_version': 1, 'op': 'timeline.migrate-groups', 'version': '1',
               'select': 'parent', 'args': {'groups': copy.deepcopy(groups)}, 'intent': {}}
    return execute(bundle_from_document(document, migration_command=command), [command]).commands[0]
