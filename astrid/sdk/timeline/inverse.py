"""Guarded authored inverses over trusted accepted records, never snapshots."""
from __future__ import annotations

import copy

from ._command_state import ABSENT, CommandError, overlaps, present
from ._recording import guard, selection


def _patch(state, path, replacement):
    if not path:
        return copy.deepcopy(replacement)
    value = copy.deepcopy(state.get('value', {}))
    node = value
    for token in path[:-1]:
        node = node.setdefault(token, {})
    if replacement['state'] == 'absent':
        node.pop(path[-1], None)
    else:
        node[path[-1]] = copy.deepcopy(replacement['value'])
    return present(value)


def coalesce(records):
    """Retain first-before/last-after, folding descendants into authored roots."""
    result = []
    for record in records:
        for raw in record['writes']:
            write = copy.deepcopy(raw)
            address = write['ref'], tuple(write['path'])
            ancestor = next((old for old in result if old['ref'] == address[0]
                             and address[1][:len(old['path'])] == tuple(old['path'])), None)
            if ancestor is not None:
                ancestor['after'] = _patch(ancestor['after'], write['path'][len(ancestor['path']):],
                                           write['after'])
                continue
            descendants = [old for old in result if overlaps(
                (old['ref'], tuple(old['path'])), address)]
            for old in reversed(descendants):
                write['before'] = _patch(write['before'], old['path'][len(write['path']):], old['before'])
                result.remove(old)
            result.append(write)
    return result


def check_intervening(records, intervening_records, *, include_reads=True):
    if intervening_records is None:
        raise CommandError('complete intervening history is required', kind='history_unavailable')
    guarded = []
    for record in records:
        if not isinstance(record, dict) or any(key not in record for key in ('writes', 'reads', 'selections', 'created')):
            raise CommandError('complete accepted recorder history is required', kind='history_unavailable')
        guarded.extend((w['ref'], tuple(w['path'])) for w in record['writes'])
        if include_reads:
            guarded.extend((r['ref'], tuple(r['path'])) for r in record['reads'])
    for record in intervening_records:
        if not isinstance(record, dict) or 'writes' not in record:
            raise CommandError("complete intervening write history is required", kind='history_unavailable')
        for write in record['writes']:
            address = write['ref'], tuple(write['path'])
            if any(overlaps(address, prior) for prior in guarded):
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
            expected = copy.deepcopy(selected)
            if selected['key'] == 'track.create':
                members = list(selected['members'])
                for change in changes:
                    if change['path'] or not change['ref'].startswith(selected['owner'] + '/track:'):
                        continue
                    if change['before'] == ABSENT and change['ref'] not in members:
                        members.append(change['ref'])
                    elif change['after'] == ABSENT and change['ref'] in members:
                        members.remove(change['ref'])
                expected.update(members=members, order=list(members), boundaries=list(members))
            actual = selection(ctx.state, selected['key'], selected['owner'], selected['members'])
            if actual != expected:
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
            ctx.create(owner, entity.split(':', 1)[0], write['before']['value'])
        else:
            ctx.assign(write['ref'], write['path'], write['before'])
