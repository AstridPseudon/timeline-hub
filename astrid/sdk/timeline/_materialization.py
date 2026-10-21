"""Derived allocations, bound to exact immutable inputs rather than row absence."""
from __future__ import annotations

import copy

from ._command_state import CommandError, State, equal, item_identity, root_identity

SOURCE_BOUND_OPERATIONS = frozenset({
    'clip.move', 'placement.move', 'track.create', 'clip.set',
    'clip.set-element', 'track.set',
    'shot.set', 'clip.set-params', 'occurrence.add-media', 'occurrence.swap-media',
    'placement.create', 'placement.unplace', 'shot.pool', 'clip.delete',
})


def capture_version(bundle, select):
    """Choose the source-bound format only while authoring a virtual shot slot."""
    if '_source_closure' in bundle['source_mapping'] and isinstance(select, str):
        owner = select.split('/', 1)[0]
        for row in bundle['placements']:
            if owner == 'occurrence:' + row['occurrence_id']:
                shot = row['shot_id']
                source = bundle['source_mapping']['shots'].get(shot)
                if source is not None and shot != source['shot_id']:
                    return '2'
    return '1'


def allocations(bundle):
    """Return only virtual aggregates whose authored content will materialize."""
    from astrid.core.timeline.authoring_bundle import _canonical_json

    result = []
    # The paired carrier requires a verified Runtime closure; frozen M1 bundles
    # without that input keep their legacy claims and identity maps.
    if '_source_closure' not in bundle['source_mapping']:
        return result
    for row in bundle['placements']:
        destination = row['shot_id']
        source = bundle['source_mapping']['shots'].get(destination)
        shot = bundle['shots'][destination]
        if (source is not None and destination != source['shot_id']
                and (_canonical_json(shot['payload']) != _canonical_json(shot['base_payload'])
                     or _canonical_json(shot['internal_timeline']) != _canonical_json(shot['base_internal_timeline']))):
            result.append((destination, 'occurrence:' + row['occurrence_id'], {
                'parent': bundle['base_parent'], 'source': source}))
    return result


def recorded_allocations(records):
    """Join complete allocation facts once, preserving their original source pins."""
    result = {}
    for record in records:
        for dep in record['dependencies']:
            if not dep['key'].startswith('materialization.source:'):
                continue
            shot = dep['key'].removeprefix('materialization.source:')
            root = root_identity(shot)
            pin = dep['pin']
            source = pin.get('source', {})
            if (root is None or root[0] != 'shot' or dep['kind'] != 'entity'
                    or dep['policy'] != 'exact' or set(pin) != {'parent', 'source'}
                    or not isinstance(source.get('shot_id'), str)
                    or root_identity('shot:' + source['shot_id']) is None
                    or not isinstance(source.get('item_id_map'), dict)):
                raise CommandError('invalid materialization dependency', kind='capture_mismatch')
            pairs = {shot: 'shot:' + source['shot_id']}
            for raw, target in source['item_id_map'].items():
                if (not isinstance(raw, str) or not isinstance(target, str)
                        or item_identity(shot + '/item:' + target) is None
                        or item_identity(pairs[shot] + '/item:' + raw) is None
                        or shot + '/item:' + target in pairs):
                    raise CommandError('invalid materialization item map', kind='capture_mismatch')
                pairs[shot + '/item:' + target] = pairs[shot] + '/item:' + raw
            owner_key = 'materialization.owner:' + shot
            owners = [b for b in record['bindings'] if b['key'] == owner_key]
            if (len(owners) != 1 or root_identity(owners[0]['ref']) is None
                    or root_identity(owners[0]['ref'])[0] != 'occurrence'):
                raise CommandError('invalid materialization owner', kind='capture_mismatch')
            pairs[owner_key] = owners[0]['ref']
            expected = [{'key': key, 'ref': ref, 'policy': 'fixed', 'dependencies': [dep['key']]}
                        for key, ref in pairs.items()]
            actual = [b for b in record['bindings'] if b['key'] in pairs or dep['key'] in b['dependencies']]
            if len(actual) != len(expected) or any(sum(equal(b, e) for b in actual) != 1 for e in expected):
                raise CommandError('incomplete materialization bindings', kind='capture_mismatch')
            facts = [root[1], owners[0]['ref'], pin]
            if shot in result and not equal(result[shot], facts):
                raise CommandError('conflicting materialization allocation', kind='capture_mismatch')
            result[shot] = facts
    return list(result.values())


def capture(ctx, originals=()):
    candidates = {row[0]: row for row in allocations(ctx.state.bundle)}
    candidates.update({row[0]: row for row in recorded_allocations(originals)})
    for destination, owner, pin in candidates.values():
        shot = 'shot:' + destination
        if not any(w['ref'] == shot or w['ref'].startswith(shot + '/item:')
                   or w['ref'].startswith(owner + '/') for w in ctx.record['writes']):
            continue
        key = 'materialization.source:' + shot
        ctx.dependency(key, 'entity', pin)
        ctx.bind(shot, 'shot:' + pin['source']['shot_id'], dependencies=[key])
        for raw, identity in pin['source']['item_id_map'].items():
            ctx.bind(shot + '/item:' + identity, 'shot:' + pin['source']['shot_id'] + '/item:' + raw,
                     dependencies=[key])
        ctx.bind('materialization.owner:' + shot, owner, dependencies=[key])


def accepted_context(records, commands, load):
    """Select original allocations from authenticated history, never from claims."""
    bindings = {key: value for command in commands for key, value in command.get('bindings', {}).items()
                if key.startswith('materialization.owner:')}
    selected, closures = [], {}
    for record in records:
        if not any(b['key'] in bindings and b['ref'] == bindings[b['key']] for b in record['bindings']):
            continue
        for _, _, pin in recorded_allocations([record]):
            revision = pin['parent']['revision_id']
            if revision not in closures:
                closures[revision] = load(revision)
        selected.append(record)
    return selected, closures


def id_map(records):
    """Return allocation-ref to raw identity pairs, separate from semantic births."""
    result = {}
    for destination, _, pin in recorded_allocations(records):
        shot = 'shot:' + destination
        result[shot] = destination
        result.update({shot + '/item:' + item: item for item in pin['source']['item_id_map'].values()})
    return result


def source_bundle(state, pin):
    """Find the original, verified input; never fall back to writable authored S."""
    from astrid.core.timeline.authoring_bundle import open_authoring_bundle

    from .commit import bundle_from_document

    for bundle in [state.bundle, *state.closures.values()]:
        document = bundle['source_mapping'].get('_runtime_document')
        source = bundle['source_mapping'].get('_source_closure')
        if not (document or source) or not equal(bundle['base_parent'], pin['parent']):
            continue
        verified = (bundle_from_document(document) if document else
                    open_authoring_bundle(**source, capture_sources=True))
        if ((verified['project_id'], verified['timeline_id']) == (
                state.bundle['project_id'], state.bundle['timeline_id'])
                and equal(verified['base_parent'], pin['parent'])
                and any(equal(pin['source'], source) for source in verified['source_mapping']['shots'].values())):
            return verified
    raise CommandError('materialization source closure unavailable', kind='history_unavailable')


def verify_sources(state, records):
    for destination, owner, pin in recorded_allocations(records):
        verified = source_bundle(state, pin)
        if (not equal(verified['source_mapping']['shots'].get(destination), pin['source'])
                or State(verified).occurrence(owner)['shot_id'] != destination):
            raise CommandError('materialization source/owner mismatch', kind='capture_mismatch')


def source_entity(state, ref, pin):
    """Resolve S/I read-only inside an authenticated original source closure."""
    from ._command_state import one

    verified = source_bundle(state, pin)
    document = verified['source_mapping'].get('_runtime_document',
                                              verified['source_mapping'].get('_source_closure'))
    shot = next(row for row in document['shot_revisions']
                if row['revision_id'] == pin['source']['revision_id'])
    member = item_identity(ref)
    source, item = member if member else (ref, None)
    if source != 'shot:' + shot['shot_id']:
        raise CommandError('materialization source reference mismatch', kind='capture_mismatch')
    return copy.deepcopy(one(shot['payload'].get('items', []), 'item_id', item, item=True)
                         if item else shot['payload'])


def consume(bundle, records, *, closures=None):
    """Restore captured editing slots when a sibling or undo made S unshared."""
    from astrid.core.timeline.authoring_bundle import _remap_known_item_references

    if any(not isinstance(record, dict) or not all(isinstance(record.get(key), list)
               for key in ('bindings', 'dependencies')) for record in records):
        raise CommandError('complete allocation history is required', kind='history_unavailable')
    verify_sources(State(bundle, closures=closures), records)
    bundle = copy.deepcopy(bundle)
    for destination, owner, pin in recorded_allocations(records):
        source = pin['source']
        row = State(bundle).occurrence(owner)
        if row['shot_id'] == destination:
            continue
        current = row['shot_id']
        if (current != source['shot_id'] or
                not equal(bundle['source_mapping']['shots'][current], {**source, 'item_id_map': {}})):
            raise CommandError('materialization source changed', kind='identity_conflict', ref=owner)
        shot = bundle['shots'][current]
        replacement = copy.deepcopy(shot)
        replacement['shot_id'] = destination
        for field in ('payload', 'base_payload'):
            items = {item.get('item_id', item.get('id')) for item in shot[field].get('items', [])}
            if items != source['item_id_map'].keys():
                raise CommandError('materialization source items changed', kind='identity_conflict')
            replacement[field] = _remap_known_item_references(shot[field], source['item_id_map'])
        row['shot_id'] = destination
        bundle['shots'][destination] = replacement
        bundle['source_mapping']['shots'][destination] = copy.deepcopy(source)
        if not any(other['shot_id'] == current for other in bundle['placements']):
            bundle['shots'].pop(current)
            bundle['source_mapping']['shots'].pop(current)
    return bundle
