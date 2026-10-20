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


def _patch(state, path, replacement):
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


def coalesce(records):
    """Retain first-before/last-after, folding descendants into authored roots."""
    def value_address(write):
        ref, path = logical_address(write['ref'], write['path'])
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
                ancestor['after'] = _patch(ancestor['after'], address[1][len(value_address(ancestor)[1]):],
                                           write['after'])
                continue
            descendants = [old for old in result
                           if value_address(old)[0] == address[0]
                           and value_address(old)[1][:len(address[1])] == address[1]]
            for old in reversed(descendants):
                write['before'] = _patch(write['before'], value_address(old)[1][len(address[1]):], old['before'])
                result.remove(old)
            result.append(write)
    return result


def check_intervening(records, intervening_records, *, include_reads=True):
    if intervening_records is None:
        raise CommandError('complete intervening history is required', kind='history_unavailable')
    guarded = []
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
                        guarded.append(('shot:' + read['state']['value'], ()))
            for binding in record.get('bindings', []):
                ref = binding['ref']
                if member(ref) is not None:
                    guarded.append((ref, ('id',)))
                elif ref.startswith('occurrence:') and '/' not in ref:
                    guarded.append((ref, ('occurrence_id',)))
    for record in intervening_records:
        if not isinstance(record, dict) or 'writes' not in record:
            raise CommandError("complete intervening write history is required", kind='history_unavailable')
        for write in record['writes']:
            address = write['ref'], tuple(write['path'])
            if (any(overlaps(address, prior) for prior in guarded)
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


def _legacy_inverse_sites(records, record):
    """Recover only known v1 inverse read/create sites from its verified input."""
    if record['command']['op'] != 'timeline.inverse' or not isinstance(records, AcceptedRecords):
        raise CommandError('original read stage is unavailable', kind='history_unavailable')
    state, _ = records.boundary(record)
    reads, selections = [], []
    for write in record['writes']:
        guard(state, write['ref'], write['path'], write['before'], kind='history_unavailable')
        # The old inverse read immediately before each authored reversal.
        reads.append({'ref': write['ref'], 'path': write['path'], 'state': write['before']})
        entity = member(write['ref'])
        if entity is not None and not write['path'] and write['before'] == ABSENT:
            owner, kind, _ = entity
            if kind == 'track':
                selections.append(selection(state, 'track.create', owner))
        state.set(write['ref'], write['path'], write['after'])
    return reads, selections


def _validate_inputs(state, record, records):
    legacy = None
    for read in record['reads']:
        if state.matches(read['ref'], read['path'], read['state']):
            continue
        if legacy is None:
            legacy = _legacy_inverse_sites(records, record)
        if read not in legacy[0]:
            raise CommandError('original inverse read changed', kind='inverse_dependency_changed',
                               ref=read['ref'], path=read['path'])
    for selected in record['selections']:
        actual = selection(state, selected['key'], selected['owner'], selected['members'])
        if equal(actual, selected):
            continue
        if legacy is None:
            legacy = _legacy_inverse_sites(records, record)
        if selected not in legacy[1]:
            raise CommandError('inverse selection changed', kind='selection_changed', ref=selected['owner'])
    created = {item['ref'] for item in record['created']}
    for binding in record.get('bindings', []):
        ref = binding['ref']
        if ref not in created and state.entity(ref, optional=True) is None:
            raise CommandError('bound identity disappeared', kind='inverse_dependency_changed', ref=ref)


def apply_inverse(ctx, records, intervening_records):
    if not records:
        raise CommandError("inverse requires trusted accepted records", kind='history_unavailable')
    if any(not isinstance(record, dict) or 'writes' not in record for record in records):
        raise CommandError("inverse history lacks authored writes", kind='history_unavailable')
    check_intervening(records, intervening_records)
    changes = coalesce(records)
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
                entity = member(write['ref'])
                if entity is not None and entity[1] == 'track' and _dependents(scratch, write['ref']):
                    raise CommandError('created track has surviving dependents', kind='surviving_dependents',
                                       ref=write['ref'])
            root = root_identity(write['ref'])
            if root is not None and not write['path'] and write['after'] == ABSENT:
                staged.create_entity(write['ref'], kind=root[0],
                                     owner=None if root[0] == 'shot' else 'parent',
                                     value=write['before']['value'], restoring=True)
            else:
                scratch.set(write['ref'], write['path'], write['before'])
        for (owner, kind), (original, _) in staged_orders.items():
            arrange(scratch, owner, kind, original)
        staged.compile_mirrors()
        _validate_inputs(scratch, record, records)

    # Historical checks above are internal. Public claims describe H even when
    # the same address is read after another reversal during installation.
    ctx.capture_input()
    for record in records:
        for read in record['reads']:
            ctx.read(read['ref'], read['path'])
        for selected in record['selections']:
            ctx.select(selected['key'], selected['owner'], selected['members'])
    for write in reversed(changes):
        ctx.read(write['ref'], write['path'])
        if not write['path'] and write['after'] == ABSENT:
            root = root_identity(write['ref'])
            if root is not None:
                ctx.create_entity(write['ref'], kind=root[0],
                                  owner=None if root[0] == 'shot' else 'parent',
                                  value=write['before']['value'], restoring=True)
            else:
                owner, entity = write['ref'].rsplit('/', 1)
                ctx.create(owner, entity.split(':', 1)[0], write['before']['value'], restoring=True)
        else:
            ctx.assign(write['ref'], write['path'], write['before'])
    for (owner, kind), (original, _) in orders.items():
        arrange(ctx.state, owner, kind, original)
