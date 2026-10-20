"""Derived allocations, bound to exact immutable inputs rather than row absence."""
from __future__ import annotations

import copy

from ._command_state import CommandError, State, equal, root_identity


def allocations(bundle):
    """Return only virtual aggregates whose authored content will materialize."""
    result = []
    # The paired carrier requires a verified Runtime closure; frozen M1 bundles
    # without that input keep their legacy claims and identity maps.
    if not any(key in bundle['source_mapping'] for key in ('_runtime_document', '_source_closure')):
        return result
    for row in bundle['placements']:
        destination = row['shot_id']
        source = bundle['source_mapping']['shots'].get(destination)
        shot = bundle['shots'][destination]
        if (source is not None and destination != source['shot_id']
                and (not equal(shot['payload'], shot['base_payload'])
                     or not equal(shot['internal_timeline'], shot['base_internal_timeline']))):
            result.append((destination, 'occurrence:' + row['occurrence_id'], source))
    return result


def recorded_allocations(records):
    result = {}
    for record in records:
        for dep in record['dependencies']:
            if dep['key'].startswith('materialization.source:'):
                shot = dep['key'].removeprefix('materialization.source:')
                owner = next(b['ref'] for b in record['bindings']
                             if b['key'] == 'materialization.owner:' + shot)
                result[shot[5:]] = (shot[5:], owner, dep['pin']['source'])
    return list(result.values())


def capture(ctx, originals=()):
    candidates = {row[0]: row for row in allocations(ctx.state.bundle)}
    candidates.update({row[0]: row for row in recorded_allocations(originals)})
    for destination, owner, source in candidates.values():
        shot = 'shot:' + destination
        if not any(w['ref'] == shot or w['ref'].startswith(shot + '/item:')
                   or w['ref'].startswith(owner + '/') for w in ctx.record['writes']):
            continue
        key = 'materialization.source:' + shot
        prior = [dep for record in originals for dep in record['dependencies'] if dep['key'] == key]
        pin = prior[0]['pin'] if prior else {'parent': ctx.state.bundle['base_parent'], 'source': source}
        ctx.dependency(key, 'entity', pin)
        ctx.bind(shot, 'shot:' + pin['source']['shot_id'], dependencies=[key])
        for raw, identity in pin['source']['item_id_map'].items():
            ctx.bind(shot + '/item:' + identity, 'shot:' + pin['source']['shot_id'] + '/item:' + raw,
                     dependencies=[key])
        ctx.bind('materialization.owner:' + shot, owner, dependencies=[key])


def id_map(records):
    """Join recorder facts exactly; legacy identity pairs are checked separately."""
    result, seen = {}, {}
    for record in records:
        bindings = record['bindings']
        for dep in record['dependencies']:
            if not dep['key'].startswith('materialization.source:'):
                continue
            shot = dep['key'].removeprefix('materialization.source:')
            root = root_identity(shot)
            source = dep['pin'].get('source', {})
            if (root is None or root[0] != 'shot' or dep['kind'] != 'entity'
                    or dep['policy'] != 'exact' or set(dep['pin']) != {'parent', 'source'}):
                raise CommandError('invalid materialization dependency', kind='capture_mismatch')
            pairs = {shot: 'shot:' + source['shot_id'], **{
                shot + '/item:' + target: 'shot:' + source['shot_id'] + '/item:' + raw
                for raw, target in source['item_id_map'].items()}}
            owners = [b for b in bindings if b['key'] == 'materialization.owner:' + shot]
            expected = [{'key': key, 'ref': ref, 'policy': 'fixed', 'dependencies': [dep['key']]}
                        for key, ref in pairs.items()]
            if (len(owners) != 1 or root_identity(owners[0]['ref']) is None
                    or root_identity(owners[0]['ref'])[0] != 'occurrence'
                    or owners[0]['policy'] != 'fixed' or owners[0]['dependencies'] != [dep['key']]
                    or any(bindings.count(binding) != 1 for binding in expected)):
                raise CommandError('incomplete materialization bindings', kind='capture_mismatch')
            facts = (dep, expected, owners)
            if shot in seen and not equal(seen[shot], facts):
                raise CommandError('conflicting materialization allocation', kind='capture_mismatch')
            seen[shot] = facts
            for ref in pairs:
                result[ref] = ref.rsplit(':', 1)[1]
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
                and pin['source'] in verified['source_mapping']['shots'].values()):
            return verified
    raise CommandError('materialization source closure unavailable', kind='history_unavailable')


def verify_sources(state, records):
    id_map(records)
    for record in records:
        for dep in record['dependencies']:
            if not dep['key'].startswith('materialization.source:'):
                continue
            shot = dep['key'].removeprefix('materialization.source:')
            verified = source_bundle(state, dep['pin'])
            owner = next(b['ref'] for b in record['bindings']
                         if b['key'] == 'materialization.owner:' + shot)
            if (verified['source_mapping']['shots'].get(shot[5:]) != dep['pin']['source']
                    or State(verified).occurrence(owner)['shot_id'] != shot[5:]):
                raise CommandError('materialization source/owner mismatch', kind='capture_mismatch')


def source_entity(state, ref, pin):
    """Resolve S/I read-only inside an authenticated original source closure."""
    from ._command_state import one

    verified = source_bundle(state, pin)
    document = verified['source_mapping'].get('_runtime_document',
                                              verified['source_mapping'].get('_source_closure'))
    shot = next(row for row in document['shot_revisions']
                if row['revision_id'] == pin['source']['revision_id'])
    source, _, item = ref.partition('/item:')
    if source != 'shot:' + shot['shot_id']:
        raise CommandError('materialization source reference mismatch', kind='capture_mismatch')
    return copy.deepcopy(one(shot['payload'].get('items', []), 'item_id', item, item=True)
                         if item else shot['payload'])


def consume(bundle, records, *, closures=None):
    """Restore captured editing slots when a sibling or undo made S unshared."""
    from astrid.core.timeline.authoring_bundle import _remap_shot_items

    if any(not isinstance(record, dict) or not all(isinstance(record.get(key), list)
               for key in ('bindings', 'dependencies')) for record in records):
        raise CommandError('complete allocation history is required', kind='history_unavailable')
    verify_sources(State(bundle, closures=closures), records)
    bundle = copy.deepcopy(bundle)
    for destination, owner, source in recorded_allocations(records):
        row = State(bundle).occurrence(owner)
        if row['shot_id'] == destination:
            continue
        current = row['shot_id']
        if (current != source['shot_id'] or
                bundle['source_mapping']['shots'][current] != {**source, 'item_id_map': {}}):
            raise CommandError('materialization source changed', kind='identity_conflict', ref=owner)
        shot = bundle['shots'][current]
        replacement = copy.deepcopy(shot)
        replacement['shot_id'] = destination
        for field in ('payload', 'base_payload'):
            items = {item.get('item_id', item.get('id')) for item in shot[field].get('items', [])}
            if items != source['item_id_map'].keys():
                raise CommandError('materialization source items changed', kind='identity_conflict')
            replacement[field] = _remap_shot_items(shot[field], source['item_id_map'])
        row['shot_id'] = destination
        bundle['shots'][destination] = replacement
        bundle['source_mapping']['shots'][destination] = copy.deepcopy(source)
        if not any(other['shot_id'] == current for other in bundle['placements']):
            bundle['shots'].pop(current)
            bundle['source_mapping']['shots'].pop(current)
    return bundle
