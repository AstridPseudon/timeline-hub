"""Guarded authored inverses over trusted accepted records, never snapshots."""
from __future__ import annotations

import copy

from ._collections import KINDS, arrange, restoration_orders, selection_overlap
from ._command_state import ABSENT, CommandError, logical_address, overlaps, present
from ._recording import guard, selection


def _patch(state, path, replacement):
    if not path:
        return copy.deepcopy(replacement)
    value = copy.deepcopy(state.get('value', {}))
    node = value
    for token in path[:-1]:
        if isinstance(token, tuple):
            matches = [row for row in node if row.get('id') == token[1]]
            if len(matches) != 1:
                raise CommandError('ambiguous collection alias', kind='identity_conflict')
            node = matches[0]
        elif isinstance(node, list):
            node = node[int(token)]
        else:
            node = node.setdefault(token, {})
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
    found = []
    owners = ['parent'] + ['occurrence:' + row['occurrence_id'] for row in state.bundle['placements']]
    for other in owners:
        for clip in state.collection(other, 'clip'):
            if (other == owner and clip.get('track') == identity) or ref in (
                    clip.get('track_ref'), clip.get('owner_ref')):
                found.append(other + '/clip:' + clip['id'])
        config = state.config(other)
        for key in ('audio', 'effects'):
            for row in config.get(key, []):
                if isinstance(row, dict) and ((other == owner and row.get('track_id') == identity)
                                             or row.get('track_ref') == ref):
                    found.append(other + '/' + key)
        if other != 'parent':
            shot = state.bundle['shots'][state.occurrence(other)['shot_id']]['payload']
            for row in shot.get('audio_bindings', []):
                if ((other == owner and row.get('track_id') == identity)
                        or row.get('track_ref') == ref):
                    found.append(other + '/shot')
    if owner == 'parent':
        for row in state.bundle['placements']:
            if row.get('placement', {}).get('track', row.get('track')) == identity:
                found.append('occurrence:' + row['occurrence_id'])
    return found


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
    # Selection and identity guards remain relevant; value reads changed by the
    # target itself are verified by the coalesced final authored-state guard.
    for record in records:
        for read in record['reads']:
            addr = read['ref'], tuple(read['path'])
            if not any(overlaps(addr, (w['ref'], tuple(w['path']))) for w in changes):
                guard(ctx.state, read['ref'], read['path'], read['state'], kind='inverse_dependency_changed')
                ctx.read(read['ref'], read['path'])
        for selected in record['selections']:
            if (selected['owner'], KINDS.get(selected['key'])) in orders:
                continue
            actual = selection(ctx.state, selected['key'], selected['owner'], selected['members'])
            if actual != selected:
                raise CommandError("inverse selection changed", kind='selection_changed', ref=selected['owner'])
            ctx.select(selected['key'], selected['owner'], selected['members'])
        for created in record['created']:
            if created['kind'] == 'track' and _dependents(ctx.state, created['ref']):
                raise CommandError("created track has surviving dependents", kind='surviving_dependents',
                                   ref=created['ref'])
    for write in reversed(changes):
        ctx.read(write['ref'], write['path'])
        if not write['path'] and write['after'] == ABSENT:
            owner, entity = write['ref'].rsplit('/', 1)
            ctx.create(owner, entity.split(':', 1)[0], write['before']['value'], restoring=True)
        else:
            ctx.assign(write['ref'], write['path'], write['before'])
    for (owner, kind), (original, _) in orders.items():
        arrange(ctx.state, owner, kind, original)
