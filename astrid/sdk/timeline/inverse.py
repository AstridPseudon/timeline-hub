"""Guarded authored inverses over trusted accepted records, never snapshots."""
from __future__ import annotations

import copy

from ._collections import AcceptedRecords, arrange, member, restoration_orders, selection_overlap
from ._command_state import (
    ABSENT,
    CommandError,
    State,
    equal,
    logical_address,
    overlaps,
    present,
    root_identity,
)
from ._recording import Recording, guard, selection
from ._root_inverse import arrange_restored, occurrence_orders, recover_source


def _patch(state, path, replacement, *, insertion_order=None):
    if not path:
        return copy.deepcopy(replacement)
    if state == ABSENT or state.get('value') is None:
        if replacement == ABSENT:
            return copy.deepcopy(state)
        raise CommandError('patch requires historical container structure', kind='history_unavailable')
    value = copy.deepcopy(state['value'])
    node = value
    for token in path[:-1]:
        if isinstance(token, tuple):
            matches = [row for row in node if row.get('id') == token[1]]
            if len(matches) != 1:
                raise CommandError('ambiguous collection alias', kind='identity_conflict')
            node = matches[0]
        elif isinstance(node, list):
            node = node[int(token)]
        elif isinstance(node, dict):
            if token not in node:
                if replacement == ABSENT:
                    return copy.deepcopy(state)
                raise CommandError('patch requires historical container structure', kind='history_unavailable')
            node = node[token]
        else:
            raise CommandError('patch parent must be an object or array', kind='history_unavailable')
        if node is None:
            if replacement == ABSENT:
                return copy.deepcopy(state)
            raise CommandError('patch requires historical container structure', kind='history_unavailable')
    if isinstance(path[-1], tuple):
        identity = path[-1][1]
        indices = [i for i, row in enumerate(node) if row.get('id') == identity]
        if len(indices) > 1:
            raise CommandError('ambiguous collection alias', kind='identity_conflict')
        if replacement['state'] == 'absent':
            if indices:
                node.pop(indices[0])
        elif indices:
            node[indices[0]] = copy.deepcopy(replacement['value'])
        elif insertion_order is not None and identity in insertion_order:
            identities = [row.get('id') for row in node]
            if (len(identities) != len(set(identities))
                    or any(item not in insertion_order for item in identities)
                    or identities != [item for item in insertion_order if item in identities]):
                raise CommandError('collection alias order differs from history', kind='history_unavailable')
            following = set(insertion_order[insertion_order.index(identity) + 1:])
            index = next((i for i, row in enumerate(node) if row.get('id') in following), len(node))
            node.insert(index, copy.deepcopy(replacement['value']))
        else:
            raise CommandError('collection alias insertion needs historical order', kind='history_unavailable')
        return present(value)
    if isinstance(node, list):
        index = int(path[-1])
        if replacement['state'] == 'absent':
            node.pop(index)
        else:
            node[index] = copy.deepcopy(replacement['value'])
        return present(value)
    if not isinstance(node, dict):
        raise CommandError('patch parent must be an object or array', kind='history_unavailable')
    if replacement['state'] == 'absent':
        node.pop(path[-1], None)
    else:
        node[path[-1]] = copy.deepcopy(replacement['value'])
    return present(value)


def _root_addresses(records, state=None):
    """Resolve aliases by authored owner, never a shared source shot identity."""
    owners = {}
    if state is not None:
        for row in state.bundle['placements']:
            ref = 'occurrence:' + row['occurrence_id']
            if ref in owners:
                raise CommandError('ambiguous root context', kind='history_unavailable', ref=ref)
            owners[ref] = row['shot_id']
    for record in records:
        for write in record['writes']:
            if root_identity(write['ref']) is None or not write['ref'].startswith('occurrence:') or write['path']:
                continue
            for value in (write['before'], write['after']):
                if value['state'] == 'present':
                    shot = value['value'].get('shot_id')
                    if not isinstance(shot, str) or root_identity('shot:' + shot) is None:
                        raise CommandError('root context is unavailable', kind='history_unavailable', ref=write['ref'])
                    if write['ref'] in owners and owners[write['ref']] != shot:
                        if state is None or not state.matches(write['ref'], ['shot_id'], present(shot)):
                            raise CommandError('root context changed', kind='history_unavailable', ref=write['ref'])
                    else:
                        owners[write['ref']] = shot

    def address(ref, path):
        if ref.startswith('occurrence:') and ref.endswith('/registry'):
            ref, path = ref.removesuffix('/registry'), ('source', 'registry', *path)
        if ref.endswith('/shot') and tuple(path[:1]) == ('payload',):
            owner = ref.removesuffix('/shot')
            if owner in owners:
                return 'shot:' + owners[owner], tuple(path)
        root, path = logical_address(ref, path)
        if root.startswith('occurrence:') and path[:1] == ('source',) and root in owners:
            return 'shot:' + owners[root], ('internal_timeline', *path[1:])
        return root, path

    return address


def coalesce(records, state=None):
    """Retain first-before/last-after, folding descendants into authored roots."""
    root_address = _root_addresses(records, state)

    def value_address(write):
        ref, path = root_address(write['ref'], write['path'])
        # Source rows are owned by an occurrence, but aren't JSON children of
        # its placement row. Ownership overlap must not fold them into that row.
        if ref.startswith('occurrence:') and path[:1] == ('source',):
            return ref + '/source', path[1:]
        return ref, path

    result = []
    for record in records:
        for raw in record['writes']:
            write = copy.deepcopy(raw)
            address = value_address(write)
            ancestor = next((old for old in result if value_address(old)[0] == address[0]
                             and address[1][:len(value_address(old)[1])] == value_address(old)[1]), None)
            if ancestor is not None:
                insertion_order = None
                entity = member(write['ref'])
                if entity is not None and not write['path'] and write['before'] == ABSENT:
                    # A root born earlier in the batch can gain child rows. Use
                    # the same recorded append/boundary proof as staged inverse.
                    orders = restoration_orders(records, only=record)
                    insertion_order = [member(ref)[2] for ref in orders[entity[:2]][1]]
                ancestor['after'] = _patch(ancestor['after'], address[1][len(value_address(ancestor)[1]):],
                                           write['after'], insertion_order=insertion_order)
                continue
            descendants = [old for old in result
                           if value_address(old)[0] == address[0]
                           and value_address(old)[1][:len(address[1])] == address[1]]
            for old in reversed(descendants):
                write['before'] = _patch(write['before'], value_address(old)[1][len(address[1]):], old['before'])
                result.remove(old)
            result.append(write)
    return result


def check_intervening(records, intervening_records, *, include_reads=True, state=None, identities_only=False):
    if intervening_records is None:
        raise CommandError('complete intervening history is required', kind='history_unavailable')
    guarded, source_roots = [], []
    selections = []
    for record in records:
        if not isinstance(record, dict) or any(key not in record for key in ('writes', 'reads', 'selections', 'created')):
            raise CommandError('complete accepted recorder history is required', kind='history_unavailable')
        guarded.extend((w['ref'], tuple(w['path'])) for w in record['writes'])
        selections.extend(record['selections'])
        if include_reads:
            for read in record['reads']:
                guarded.append((read['ref'], tuple(read['path'])))
                if read['ref'].endswith('/shot'):
                    guarded.append((read['ref'].removesuffix('/shot'), ('shot_id',)))
                    if read['path'] == ['shot_id'] and isinstance(read['state'].get('value'), str):
                        source_roots.append(('shot:' + read['state']['value'], ()))
            for binding in record.get('bindings', []):
                ref = binding['ref']
                if member(ref) is not None:
                    guarded.append((ref, ('id',)))
                elif ref.startswith('occurrence:') and '/' not in ref:
                    guarded.append((ref, ('occurrence_id',)))
    if identities_only:
        # Ordinary replay checks values and membership on the final head. Only
        # identity replacement must remain sensitive to intervening history.
        refs = [ref for ref, _ in guarded]
        refs.extend(ref for selected in selections
                    for ref in [selected['owner'], *selected['members'], *selected['boundaries']])
        refs.extend(ref for ref, _ in source_roots)
        source_roots = []
        guarded = []
        for ref in refs:
            if member(ref) is not None:
                guarded.append((ref, ('id',)))
            owner = ref.split('/', 1)[0]
            root = root_identity(owner)
            guarded.append((owner, (root[0] + '_id',) if root else ('id',)))
        selections = []
    root_address = _root_addresses(records, state)
    for record in intervening_records:
        if not isinstance(record, dict) or 'writes' not in record:
            raise CommandError("complete intervening write history is required", kind='history_unavailable')
        for write in record['writes']:
            address = write['ref'], tuple(write['path'])
            if (any(overlaps(address, prior) for prior in [*guarded, *source_roots])
                    or any(overlaps(root_address(*address), root_address(*prior)) for prior in guarded)
                    or any(selection_overlap(s, write) for s in selections)):
                raise CommandError("an intervening publication wrote a guarded address",
                                   kind='intervening_write', ref=address[0], path=address[1])
            if not write['path']:
                if write['ref'] == 'parent' and guarded:
                    raise CommandError('an intervening publication replaced the timeline',
                                       kind='intervening_write', ref='parent')
                # Removing an owner also invalidates every scoped descendant.
                if any(ref.startswith(write['ref'] + '/') for ref, _ in guarded):
                    raise CommandError("an intervening publication replaced an owner",
                                       kind='intervening_write', ref=address[0])


def _dependents(state, ref):
    owner, identity = ref.rsplit('/track:', 1)

    def references(row, other):
        if not isinstance(row, dict):
            raise CommandError('unsupported declared reference row', kind='surviving_dependents', ref=ref)
        for key in ('track_ref', 'owner_ref', 'track', 'track_id'):
            value = row.get(key)
            if value is not None and not isinstance(value, str):
                raise CommandError('unsupported declared reference edge', kind='surviving_dependents', ref=ref)
            if key in ('track_ref', 'owner_ref') and value == ref:
                return True
        return other == owner and (row.get('track') == identity or row.get('track_id') == identity)

    found = []
    owners = ['parent'] + ['occurrence:' + row['occurrence_id'] for row in state.bundle['placements']]
    for other in owners:
        for clip in state.collection(other, 'clip'):
            if references(clip, other):
                found.append(other + '/clip:' + clip['id'])
        config = state.config(other)
        for key in ('audio', 'effects'):
            for row in config.get(key, []):
                if references(row, other):
                    found.append(other + '/' + key)
        if other != 'parent':
            shot = state.bundle['shots'][state.occurrence(other)['shot_id']]['payload']
            for row in shot.get('audio_bindings', []):
                if references(row, other):
                    found.append(other + '/shot')
    for row in state.bundle['placements']:
        if references(row, 'parent') or references(row.get('placement') or {}, 'parent'):
            found.append('occurrence:' + row['occurrence_id'])
    for shot in state.bundle['shots'].values():
        for row in shot['payload'].get('audio_bindings', []):
            if references(row, None):
                found.append('shot:' + shot['shot_id'])
    return found


def _asset_dependents(state, ref):
    owner, identity = ref.rsplit('/asset:', 1)

    def references(value, local):
        if isinstance(value, dict):
            return ((local and any(value.get(key) == identity for key in ('asset', 'asset_id')))
                    or any(value.get(key) == ref for key in ('asset_ref', 'owner_ref'))
                    or any(references(child, local) for child in value.values()))
        return isinstance(value, list) and any(references(child, local) for child in value)

    owners = ['parent', *('occurrence:' + row['occurrence_id'] for row in state.bundle['placements'])]
    return (any(references(state.config(other), other == owner) for other in owners)
            or any(references(shot['payload'], False) for shot in state.bundle['shots'].values()))


def _legacy_inverse_sites(records, record):
    """Recover only known v1 inverse read/create sites from its verified input."""
    if record['command']['op'] != 'timeline.inverse' or not isinstance(records, AcceptedRecords):
        raise CommandError('original read stage is unavailable', kind='history_unavailable')
    state, after = records.boundary(record)
    reads = [read for read in record['reads'] if state.matches(read['ref'], read['path'], read['state'])]
    selections = [selected for selected in record['selections']
                  if equal(selection(state, selected['key'], selected['owner'], selected['members']), selected)]
    for write in record['writes']:
        guard(state, write['ref'], write['path'], write['before'], kind='history_unavailable')
        # The old inverse read immediately before each authored reversal.
        reads.append({'ref': write['ref'], 'path': write['path'], 'state': write['before']})
        entity = member(write['ref'])
        if entity is not None and not write['path'] and write['before'] == ABSENT:
            owner, kind, _ = entity
            if kind == 'track':
                selections.append(selection(state, 'track.create', owner))
        if (root_identity(write['ref']) is not None and write['ref'].startswith('occurrence:')
                and not write['path'] and write['after'] != ABSENT):
            recover_source(state, write['after']['value'], after.bundle)
        state.set(write['ref'], write['path'], write['after'])
    return reads, selections


def _validate_inputs(state, record, records):
    sites = None

    def proven_sites():
        if record['command']['op'] == 'timeline.inverse':
            return (*_legacy_inverse_sites(records, record), set())
        # Recorder writes are ordered even though reads and selections are not.
        # Reconstruct only those stages, retaining unrelated current authored data.
        staged = Recording(copy.deepcopy(state.bundle), record['command'], record['ordinal'],
                           closures=state.closures)
        stage = staged.state
        reads, selections, bindings = [], [], set()
        for write in [None, *record['writes']]:
            if write is not None:
                guard(stage, write['ref'], write['path'], write['before'], kind='history_unavailable')
                root = root_identity(write['ref'])
                if root is not None and not write['path'] and write['before'] == ABSENT and write['after'] != ABSENT:
                    created = {'ref': write['ref'], 'kind': root[0],
                               'owner': None if root[0] == 'shot' else 'parent'}
                    if record['created'].count(created) != 1:
                        raise CommandError('root creation context is unavailable', kind='history_unavailable',
                                           ref=write['ref'])
                    staged.create_entity(**created, value=write['after']['value'], restoring=True)
                else:
                    stage.set(write['ref'], write['path'], write['after'])
            reads.extend(read for read in record['reads']
                         if stage.matches(read['ref'], read['path'], read['state']))
            selections.extend(selected for selected in record['selections']
                              if equal(selection(stage, selected['key'], selected['owner'],
                                                 selected['members']), selected))
            bindings.update(binding['ref'] for binding in record.get('bindings', [])
                            if stage.entity(binding['ref'], optional=True) is not None)
        return reads, selections, bindings

    for read in record['reads']:
        if state.matches(read['ref'], read['path'], read['state']):
            continue
        if sites is None:
            sites = proven_sites()
        if not any(equal(read, site) for site in sites[0]):
            raise CommandError('original inverse read changed', kind='inverse_dependency_changed',
                               ref=read['ref'], path=read['path'])
    for selected in record['selections']:
        actual = selection(state, selected['key'], selected['owner'], selected['members'])
        if equal(actual, selected):
            continue
        if sites is None:
            sites = proven_sites()
        if not any(equal(selected, site) for site in sites[1]):
            raise CommandError('inverse selection changed', kind='selection_changed', ref=selected['owner'])
    created = {item['ref'] for item in record['created']}
    for binding in record.get('bindings', []):
        ref = binding['ref']
        if ref not in created and state.entity(ref, optional=True) is None:
            if sites is None:
                sites = proven_sites()
            if ref not in sites[2]:
                raise CommandError('bound identity disappeared', kind='inverse_dependency_changed', ref=ref)


def apply_inverse(ctx, records, intervening_records):
    if not records:
        raise CommandError("inverse requires trusted accepted records", kind='history_unavailable')
    if any(not isinstance(record, dict) or 'writes' not in record for record in records):
        raise CommandError("inverse history lacks authored writes", kind='history_unavailable')
    check_intervening(records, intervening_records, state=ctx.state)
    changes = coalesce(records, ctx.state)
    ctx.capture_input()
    root_orders = occurrence_orders(ctx.state, records, changes)
    orders = restoration_orders(records)
    for (owner, kind), (_, expected) in orders.items():
        actual = ctx.select('collection.' + kind + 's', owner)
        if actual != expected:
            raise CommandError('inverse collection membership/order changed',
                               kind='selection_changed', ref=owner)
    for write in changes:
        guard(ctx.state, write['ref'], write['path'], write['after'], kind='inverse_conflict')
    scratch = State(copy.deepcopy(ctx.state.bundle), closures=ctx.state.closures)
    for record in reversed(records):
        staged = Recording(scratch.bundle, record['command'], record['ordinal'], closures=scratch.closures)
        scratch = staged.state
        staged_orders = restoration_orders(records, only=record)
        for write in reversed(record['writes']):
            guard(scratch, write['ref'], write['path'], write['after'], kind='inverse_conflict')
            if not write['path'] and write['before'] == ABSENT:
                if '/asset:' in write['ref'] and _asset_dependents(scratch, write['ref']):
                    raise CommandError('created asset has surviving dependents', kind='surviving_dependents',
                                       ref=write['ref'])
                entity = member(write['ref'])
                if entity is not None and entity[1] == 'track' and _dependents(scratch, write['ref']):
                    raise CommandError('created track has surviving dependents', kind='surviving_dependents',
                                       ref=write['ref'])
            root = root_identity(write['ref'])
            if (root is not None and not write['path'] and write['after'] == ABSENT
                    and write['before']['state'] == 'present'):
                staged.create_entity(write['ref'], kind=root[0],
                                     owner=None if root[0] == 'shot' else 'parent',
                                     value=write['before']['value'], restoring=True)
            else:
                scratch.set(write['ref'], write['path'], write['before'])
        for (owner, kind), (original, _) in staged_orders.items():
            arrange(scratch, owner, kind, original)
        arrange_restored(scratch, record, root_orders.get(id(record)))
        staged.compile_mirrors()
        _validate_inputs(scratch, record, records)

    # Historical checks above are internal. Public claims describe H even when
    # the same address is read after another reversal during installation.
    for record in records:
        for read in record['reads']:
            ctx.read(read['ref'], read['path'])
        for selected in record['selections']:
            ctx.select(selected['key'], selected['owner'], selected['members'])
    for write in reversed(changes):
        ctx.read(write['ref'], write['path'])
        # An absent-to-absent edge still records authored intent, but restores
        # no entity and must not allocate an identity or dereference a value.
        if not write['path'] and write['after'] == ABSENT and write['before']['state'] == 'present':
            root = root_identity(write['ref'])
            if root is not None:
                ctx.create_entity(write['ref'], kind=root[0],
                                  owner=None if root[0] == 'shot' else 'parent',
                                  value=write['before']['value'], restoring=True)
            elif '/asset:' in write['ref']:
                owner, identity = write['ref'].rsplit('/asset:', 1)
                ctx.create_asset(owner, identity, write['before']['value'])
            else:
                owner, entity = write['ref'].rsplit('/', 1)
                ctx.create(owner, entity.split(':', 1)[0], write['before']['value'], restoring=True)
        else:
            ctx.assign(write['ref'], write['path'], write['before'])
    for (owner, kind), (original, _) in orders.items():
        if ctx.state.entity(owner, optional=True) is None and any(
                write['ref'] == owner and not write['path'] and write['before'] == ABSENT
                for write in changes):
            continue  # Reversing the owner's birth also removes its collections.
        arrange(ctx.state, owner, kind, original)

    for record in reversed(records):
        arrange_restored(ctx.state, record, root_orders.get(id(record)))
