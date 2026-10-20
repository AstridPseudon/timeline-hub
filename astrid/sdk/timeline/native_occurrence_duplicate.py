"""Independent copy of one canonical placement under explicit reserved identities."""
from __future__ import annotations

import copy

from ._command_state import CommandError, root_identity

OCCURRENCE_INTENT = {'ownership': 'occurrence'}


def occurrence_duplicate(ctx, command):
    owner = command['select']
    if root_identity(owner) is None or not owner.startswith('occurrence:'):
        raise CommandError('duplicate requires one explicit occurrence', kind='unsupported_ownership')
    if ctx.read('parent', ['config', 'pinnedShotGroups']) not in (None, []):
        raise CommandError('legacy groups require recorded migration', kind='migration_needed')
    row = ctx.read(owner)
    if not isinstance(row, dict):
        raise CommandError('duplicate source disappeared', kind='identity_conflict', ref=owner)
    source_shot = ctx.read(owner + '/shot', ['shot_id'])
    ctx.select('collection.clips', owner)
    ctx.select('collection.tracks', owner)
    internal = ctx.read(owner + '/source')
    payload = ctx.read(owner + '/shot', ['payload'])
    occurrence_id, shot_id = command['args']['occurrence_id'], command['args']['shot_id']
    if occurrence_id == row['occurrence_id'] or shot_id == source_shot:
        raise CommandError('duplicate requires reserved identities distinct from the source',
                           kind='identity_collision', ref=owner)
    from astrid.core.timeline.authoring_bundle import _copy_shot_for_placement
    bundle = ctx.state.bundle
    copied, remap = _copy_shot_for_placement(
        payload, project_id=bundle['project_id'], timeline_id=bundle['timeline_id'],
        occurrence_id=occurrence_id, authoring_shot_id=shot_id, source_shot_id=source_shot)
    occupied = {item.get('item_id', item.get('id')) for shot in bundle['shots'].values()
                for item in shot['payload'].get('items', [])}
    if occupied & set(remap.values()):
        raise CommandError('duplicate item identity is occupied', kind='identity_collision', ref=owner)
    ctx.bind('duplicate.owner', owner)
    ctx.create_entity('shot:' + shot_id, kind='shot', owner=None,
                      value={'payload': copied, 'internal_timeline': copy.deepcopy(internal)})
    created = copy.deepcopy(row)
    created.pop('shot_revision_id', None)
    created.pop('revision_id', None)
    created.update(occurrence_id=occurrence_id, shot_id=shot_id)
    ctx.create_entity('occurrence:' + occurrence_id, kind='occurrence', owner='parent', value=created)


def capture_occurrence_duplicate(bundle, owner, occurrence_id, shot_id):
    """Capture a copy of the raw canonical owner with caller-reserved target identities."""
    from .commands import execute

    return execute(bundle, [{'schema_version': 1, 'op': 'occurrence.duplicate', 'version': '1',
                             'select': owner, 'args': {'occurrence_id': occurrence_id, 'shot_id': shot_id},
                             'intent': OCCURRENCE_INTENT}]).commands[0]
