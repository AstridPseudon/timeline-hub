"""Append a placement of an exact, authenticated same-timeline source."""
from __future__ import annotations

import copy

from ._command_state import CommandError, State, equal, root_identity
from .capture import number
from .native_occurrence_duplicate import OCCURRENCE_INTENT

PARAMETERS = {
    'type': 'object', 'required': ['occurrence_id', 'on'],
    'properties': {'occurrence_id': {'type': 'string', 'pattern': r'^(?!.*::)[^/]+$'},
                   'on': {'type': 'number', 'minimum': 0}},
    'additionalProperties': False,
}


def reopen_shared_source(bundle, owner):
    """Recover an unchanged physical compiler input from this exact closure."""
    state = State(bundle)
    row = state.entity(owner)
    identity = state.entity(owner + '/shot')['shot_id']
    shot = bundle['shots'][row['shot_id']]
    if (not equal(shot['payload'], shot.get('base_payload'))
            or not equal(shot['internal_timeline'], shot.get('base_internal_timeline'))):
        raise CommandError('shared placement requires an unchanged published source',
                           kind='identity_conflict', ref=owner)
    if row['shot_id'] != identity:
        origin = bundle['source_mapping']['shots'][row['shot_id']]
        document = bundle['source_mapping']['_runtime_document']
        image = next(image for image in document['shot_revisions']
                     if (image['shot_id'], image['revision_id']) == (identity, origin['revision_id']))
        internal = next(image for image in document['internal_timeline_revisions']
                        if image['revision_id'] == origin['internal_timeline_revision_id'])
        physical = {'shot_id': identity, 'payload': copy.deepcopy(image['payload']),
                    'base_payload': copy.deepcopy(image['payload']),
                    'internal_timeline': copy.deepcopy(internal['payload']),
                    'base_internal_timeline': copy.deepcopy(internal['payload'])}
        if identity in bundle['shots'] and not equal(bundle['shots'][identity], physical):
            raise CommandError('shared physical source changed', kind='identity_conflict', ref=owner)
        bundle['shots'][identity] = physical
        bundle['source_mapping']['shots'][identity] = {**copy.deepcopy(origin), 'item_id_map': {}}
    return identity


def normalize_shared_roots(bundle, records):
    """Keep native inverse occurrence roots in their authenticated physical spelling."""
    roots = {write['ref'] for record in records for write in record['writes']
             if not write['path'] and write['ref'].startswith('occurrence:')}
    state = State(bundle)
    for owner in roots:
        row = state.entity(owner, optional=True)
        if row is not None:
            row['shot_id'] = reopen_shared_source(bundle, owner)


def prepare_shared_inverse(ctx, records):
    """Normalize only accepted shared-occurrence stages, including their redo input."""
    from ._collections import AcceptedRecords

    if not isinstance(records, AcceptedRecords):
        return
    load_boundary = records.load_boundary
    sources = {binding['ref'] for record in records for binding in record['bindings']
               if binding['key'] == 'shared.source'}
    if not sources:
        return
    for source in sorted(sources):
        ctx.bind('shared.source', source)
    normalize_shared_roots(ctx.state.bundle, records)

    def normalized_boundary(entry):
        before, after = load_boundary(entry)
        for bundle in (before, after):
            normalize_shared_roots(bundle, records)
        return before, after

    records.load_boundary = normalized_boundary


def occurrence_place_shared(ctx, command):
    owner = command['select']
    root = root_identity(owner)
    if root is None or root[0] != 'occurrence':
        raise CommandError('shared placement requires one explicit occurrence', kind='unsupported_ownership')
    if ctx.read('parent', ['config', 'pinnedShotGroups']) not in (None, []):
        raise CommandError('legacy groups require recorded migration', kind='migration_needed')
    ctx.select('collection.occurrences', 'parent')
    row = ctx.read(owner)
    if not isinstance(row, dict):
        raise CommandError('shared source disappeared', kind='identity_conflict', ref=owner)
    ctx.read(owner + '/shot', ['shot_id'])
    ctx.read(owner + '/shot', ['payload'])
    ctx.read(owner + '/source')
    on = number(command['args']['on'], 'on')
    created = copy.deepcopy(row)
    created.pop('shot_revision_id', None)
    created.pop('revision_id', None)
    created['occurrence_id'] = command['args']['occurrence_id']
    created['shot_id'] = reopen_shared_source(ctx.state.bundle, owner)
    created.setdefault('placement', {})['start_ms'] = number(on * 1000, 'start_ms')
    from astrid.core.timeline.authoring_bundle import _rederive_root_identity

    origin = ctx.state.bundle['source_mapping']['shots'][created['shot_id']]
    _rederive_root_identity(created, ctx.state.bundle['project_id'], ctx.state.bundle['timeline_id'],
                            origin['revision_id'])
    ctx.bind('shared.source', owner)
    ctx.create_entity('occurrence:' + created['occurrence_id'], kind='occurrence',
                      owner='parent', value=created)


def capture_occurrence_place_shared(bundle, owner, occurrence_id, *, on):
    """Capture against the source closure; on is seconds and the ID is reserved once."""
    from .commands import execute

    return execute(bundle, [{'schema_version': 1, 'op': 'occurrence.place-shared', 'version': '1',
                             'select': owner, 'args': {'occurrence_id': occurrence_id, 'on': on},
                             'intent': OCCURRENCE_INTENT}]).commands[0]
