"""Explain refused intent using authoritative Runtime previews, without an outbox.

Local execution supplies sites and values only. In particular, a successful local
replay is never evidence that a command applies to the current publication.
"""
from __future__ import annotations

import copy
import math
import uuid

from ._command_state import ABSENT, CommandError, present
from ._commit_patch import _prefix, canonical_site, record_sites
from ._doc_patch import Closure, identity_key, normalized_path, value_at
from .commands import execute
from .sync import _pin, _response


class _HeadMoved(Exception):
    pass


def _unsupported(command):
    op = command['op']
    return (op in {'timeline.inverse', 'timeline.restore', 'producer.guard', 'assembly-admission'}
            or op == 'occurrence.place-shared' and 'source_ref' in command.get('args', {}))


def _history(session, base):
    """Verify the public, ascending pages, retaining exactly B -> H."""
    cursor, cursors, publications = None, set(), set()
    head, previous, found, entries = None, None, False, []
    while True:
        page = _response(session.client.timelines.history(
            session.project_id, session.timeline_id, cursor=cursor, limit=100))['data']
        current = _pin(page['head'])
        if head is not None and current != head:
            raise _HeadMoved('history head changed')
        head = current
        for entry in page['items']:
            pin = _pin(entry)
            # Public history may omit the bootstrap publication. Its exact pin
            # still authenticates B when it is the first entry's predecessor.
            if previous is None and not publications:
                previous = entry['previous']
                found = previous == base
            if entry['previous'] != previous or pin['publication_id'] in publications:
                raise ValueError('incomplete publication ancestry')
            publications.add(pin['publication_id'])
            if found:
                entries.append(copy.deepcopy(entry))
            if pin == base:
                found = True
            previous = pin
        cursor = page['next_cursor']
        if cursor is None:
            if previous != head and not (not publications and head == base):
                raise ValueError('missing publication ancestry')
            if not found and head != base:
                raise ValueError('base is outside publication ancestry')
            return head, entries
        if cursor in cursors or previous == head:
            raise ValueError('invalid history cursor')
        cursors.add(cursor)


def _bundle(session, pin, commands=()):
    return session._capture_bundle({'base': pin, 'pending': []}, commands)


def _addresses(ref, path, closure):
    """Include stable occurrence aliases across physical revision transitions."""
    result = [(ref, list(path))]
    try:
        physical, normalized = canonical_site(closure, ref, path)
    except CommandError:
        return result
    result.append((physical, normalized))
    if physical in closure.images:
        try:
            result.extend(closure.native_sites(physical, normalized))
        except CommandError:
            pass  # A whole managed collection has no native authored alias.
    return result


def _touches(left, right):
    return any(a == b and _prefix(p, q) for a, p in left for b, q in right)


def _selection_refs(command, record=None):
    refs = [command.get('select'), *command.get('resolved', [])]
    for selection in (record or command).get('selections', []):
        refs.extend([*selection.get('members', []), *selection.get('boundaries', [])])
    return [ref for ref in refs if isinstance(ref, str)]


def _describe(command, record, closure, after):
    writes, reads = [], []
    for site in record_sites(record, closure):
        writes.extend(_addresses(site['ref'], site['path'], closure))
    for created in record['created']:
        writes.extend(_addresses(created['ref'], [], closure))
    for read in record['reads']:
        reads.extend(_addresses(read['ref'], read['path'], closure))
    for ref in _selection_refs(command, record):
        reads.extend(_addresses(ref, [], closure))
    return {'record': record, 'closure': closure, 'after': Closure(after), 'writes': writes, 'reads': reads,
            'unknown': False}


def _base_records(bundle, commands):
    # Prefer one execution so compiler, staged records and sequential bindings
    # have the same boundaries as the original request. Authority-only commands
    # may fail locally; retain unknown sites rather than guessing their effects.
    try:
        plan = execute(bundle, commands)
    except CommandError:
        plan = None
    result, running = [], bundle
    for ordinal, command in enumerate(commands):
        closure = Closure(running)
        try:
            if plan is None:
                one = execute(running, [command])
                record, running = one.records[0], one.bundle
            else:
                record = plan.records[ordinal]
                # Applying a prefix preserves the boundary for alias mapping.
                running = execute(bundle, commands[:ordinal + 1]).bundle
            result.append(_describe(command, record, closure, running))
        except CommandError:
            result.append({'record': None, 'closure': closure, 'writes': [], 'reads': [],
                           'unknown': True})
    return result


def _owners(commands, records, remaining, conflict, head):
    ref, path = conflict['ref'], conflict.get('path', [])
    target = _addresses(ref, path, head)
    owners = []
    for ordinal in remaining:
        info = records[ordinal]
        target_at_base = _addresses(ref, path, info['closure'])
        if (_touches(info['writes'] + info['reads'], target + target_at_base)
                or ref in _selection_refs(commands[ordinal], info['record'])):
            owners.append(ordinal)
    return owners or [next((i for i in remaining if records[i]['unknown']), remaining[0])]


def _dependents(records, remaining, removed):
    """Propagate unavailable writes through later read/selection dependencies."""
    unavailable, blocked = set(removed), {}
    for ordinal in remaining:
        if ordinal in unavailable:
            continue
        needs = [i for i in sorted(unavailable) if i < ordinal
                 and _touches(records[ordinal]['reads'], records[i]['writes'])]
        if needs:
            blocked[ordinal] = needs
            unavailable.add(ordinal)
    return blocked


def _state(closure, ref, path, source=None):
    try:
        physical, normalized = canonical_site(closure, ref, path)
    except CommandError:
        if source is not None:
            try:
                physical, normalized = canonical_site(source, ref, path)
            except CommandError:
                return ABSENT.copy()
            if physical in source.images:
                states = [_state(closure, alias, tail) for alias, tail
                          in source.native_sites(physical, normalized)
                          if alias != ref or tail != list(path)]
                if states:
                    if any(state != states[0] for state in states[1:]):
                        raise ValueError('ambiguous current value for shared physical ref')
                    return states[0]
        return ABSENT.copy()
    if physical == 'timeline':
        return ABSENT.copy()
    try:
        return copy.deepcopy(value_at(closure.payload(physical), physical, normalized))
    except (CommandError, KeyError):
        return ABSENT.copy()


def _value(state):
    # Keep absent distinct from a present JSON null.
    return copy.deepcopy(state['value']) if state.get('state') == 'present' else ABSENT.copy()


def _receipt_sites(entries, base):
    receipts, sites, before = [], [], base
    for entry in entries:
        recorder = entry.get('records')
        if (entry.get('intent') != 'recorded' or not isinstance(recorder, dict)
                or recorder.get('schema_version') != 1 or not recorder.get('commands')):
            raise ValueError('intervening write intent is unavailable')
        document = entry['receipt']['result'].get('canonical_document')
        if document is None:
            raise ValueError('intervening closure is unavailable')
        from .commit import bundle_from_document

        after = Closure(bundle_from_document(document))
        writes, addresses = [], []
        for record in recorder['commands']:
            for site in record_sites(record, before):
                write = site.get('write')
                if write is None:
                    write = {'before': _state(before, site['ref'], site['path']),
                             'after': _state(after, site['ref'], site['path'], before)}
                writes.append({'ref': site['ref'], 'path': copy.deepcopy(site['path']),
                               'before': copy.deepcopy(write['before']),
                               'after': copy.deepcopy(write['after'])})
                addresses.append(_addresses(site['ref'], site['path'], before)
                                 + _addresses(site['ref'], site['path'], after))
        data = entry['receipt']['result']
        receipts.append({'publication_id': entry['publication_id'],
                         'label': data.get('label', recorder.get('label')),
                         'publisher': entry['publisher'],
                         'idempotency_key': entry['receipt']['idempotency_key'],
                         'writes': writes, 'clashes_with': []})
        sites.append(addresses)
        before = after
    return receipts, sites


def _attribution(ref, path, base, head, receipts, sites, ordinal):
    target = _addresses(ref, path, base) + _addresses(ref, path, head)
    latest = None
    for receipt, groups in zip(receipts, sites):
        if any(_touches(group, target) for group in groups):
            latest = receipt['publication_id']
            if ordinal not in receipt['clashes_with']:
                receipt['clashes_with'].append(ordinal)
    return latest


def _overlap(conflict, info, base, head, receipts, sites, ordinal):
    ref, path = conflict['ref'], conflict.get('path', [])
    yours = (_state(info['after'], ref, path, head) if info['record'] is not None
             else conflict.get('ours', ABSENT))
    return {'ref': ref, 'path': copy.deepcopy(path), 'kind': conflict['kind'],
            'base': _value(_state(base, ref, path, head)), 'theirs': _value(_state(head, ref, path, base)),
            'yours': _value(yours),
            'receipt': _attribution(ref, path, base, head, receipts, sites, ordinal)}


def _number(value):
    return type(value) in (int, float) and math.isfinite(value)


def _clip_times(writes):
    """Project both native at writes and doc.patch collection/item writes."""
    result = {}

    def clip(ref, path):
        if '/clip:' in ref:
            return not path
        prefix = ['config', 'clips'] if ref == 'parent' and path[:1] == ['config'] else ['clips']
        return (ref == 'parent' or ref.startswith('internal')) and (
            path[:len(prefix)] == prefix and len(path) == len(prefix) + 1
            and path[-1].startswith('id:'))

    def remember(site, before, after):
        site = site[0], tuple(normalized_path(site[0], site[1]))
        result[site] = (result.get(site, (before, after))[0], after)

    def walk(ref, path, before, after):
        if path[-1:] == ['at'] and clip(ref, path[:-1]):
            remember((ref, tuple(path)), before.get('value'), after.get('value'))
        elif before.get('state') == after.get('state') == 'present':
            a, b = before['value'], after['value']
            if isinstance(a, dict) and isinstance(b, dict):
                for key in a.keys() | b.keys():
                    walk(ref, [*path, key], present(a[key]) if key in a else ABSENT,
                         present(b[key]) if key in b else ABSENT)
            elif (isinstance(a, list) and isinstance(b, list) and path[-1:] == ['clips']
                  and identity_key(ref, path) == 'id'):
                old, new = {row['id']: row for row in a}, {row['id']: row for row in b}
                for identity in old.keys() | new.keys():
                    walk(ref, [*path, 'id:' + identity],
                         present(old[identity]) if identity in old else ABSENT,
                         present(new[identity]) if identity in new else ABSENT)
        elif after.get('state') == 'present':
            value = after['value']
            if isinstance(value, dict):
                for key, item in value.items():
                    walk(ref, [*path, key], ABSENT, present(item))
            elif isinstance(value, list) and path[-1:] == ['clips'] and identity_key(ref, path) == 'id':
                for row in value:
                    walk(ref, [*path, 'id:' + row['id']], ABSENT, present(row))

    for write in writes:
        walk(write['ref'], write['path'], write['before'], write['after'])
    return result


def _ripples(times):
    groups = []
    for site, (before, after) in times.items():
        if not (_number(before) and _number(after)) or before == after:
            continue
        delta = after - before
        group = next((group for group in groups if math.isclose(group['by'], delta,
                      rel_tol=1e-9, abs_tol=1e-9)), None)
        if group is None:
            group = {'by': delta, 'after': before, 'sites': []}
            groups.append(group)
        group['after'] = min(group['after'], before)
        group['sites'].append(site)
    return [group for group in groups if len(group['sites']) >= 2]


def _literal_times(command):
    args, op = command.get('args', {}), command['op']
    if op == 'doc.patch':
        for change in args['changes']:
            if change['op'] not in ('set', 'list.insert'):
                continue
            path = [*change['path'], 'id:' + change['id']] if change['op'] == 'list.insert' else change['path']
            times = _clip_times([{'ref': change['ref'], 'path': path,
                                  'before': change['before'], 'after': present(change['value'])}])
            for (ref, path), (_, time) in times.items():
                if _number(time):
                    yield ref, list(path), time
    elif _number(args.get('on')):
        yield command['select'], ['at'], args['on']
    elif _number(args.get('values', {}).get('at')):
        yield command['select'], ['at'], args['values']['at']


def _has_moment(closure, ref, path, source):
    for suffix in (['app', 'astrid', 'on'], ['app', 'on']):
        state = _state(closure, ref, [*path[:-1], *suffix], source)
        if state.get('state') == 'present' and isinstance(state['value'], str):
            return True
    return False


def _ripple_flags(packet, records, base, head, receipts):
    theirs = [(receipt, _clip_times(receipt['writes'])) for receipt in receipts]
    moved = [site for _, times in theirs for site, (a, b) in times.items() if a != b]
    for row in packet['commands']:
        if row['verdict'] != 'applies':
            continue
        for ref, path, time in _literal_times(row['command']):
            info = records[row['ordinal']] if row['ordinal'] < len(records) else {}
            if _has_moment(info.get('after', head), ref, path, base):
                continue
            target = _addresses(ref, path, head)
            if any(_touches(target, _addresses(r, p, head)) for r, p in moved):
                continue
            for receipt, times in theirs:
                for ripple in _ripples(times):
                    if time >= ripple['after']:
                        row['time_shift'] = {key: ripple[key] for key in ('by', 'after')}
                        row['time_shift']['receipt'] = receipt['publication_id']
                        row['choices'] = ['keep', 'shift']
    ours = []
    for info in records:
        if info['record'] is not None:
            ours.extend({'ref': site['ref'], 'path': site['path'], **site['write']}
                        for site in record_sites(info['record'], info['closure']) if 'write' in site)
    after = next((info['after'] for info in reversed(records) if 'after' in info), base)
    times = {site: values for site, values in _clip_times(ours).items()
             if not _has_moment(after, site[0], list(site[1]), base)}
    for ripple in _ripples(times):
        covered = [_addresses(ref, path, base) for ref, path in ripple['sites']]
        clips = []
        for receipt, times in theirs:
            for (ref, path), (before, after) in times.items():
                if (before != after and _number(after) and after >= ripple['after']
                        and not any(_touches(group, _addresses(ref, path, head)) for group in covered)
                        and _state(head, ref, path) != ABSENT):
                    clips.append({'ref': ref, 'path': list(path), 'at': after,
                                  'receipt': receipt['publication_id']})
        if clips:
            packet['ripple_gap'] = {'by': ripple['by'], 'after': ripple['after'],
                                    'clips': clips, 'choices': ['keep', 'extend']}


def _probe(session, request, remaining):
    body = {key: copy.deepcopy(value) for key, value in request.items()
            if key not in {'base', 'steps', 'reads', 'merge', 'commands', 'key', 'origin'}}
    body.update(api_version=1, project_id=session.project_id, timeline_id=session.timeline_id,
                commands=[copy.deepcopy(request['commands'][i]) for i in remaining],
                merge='fields', reads=[], dry_run=True)
    body.setdefault('source', {'via': 'python'})
    try:
        return _response(session.client.timelines.commit(
            session.project_id, session.timeline_id, body,
            idempotency_key='clash-probe-' + uuid.uuid4().hex))['data']
    except Exception as exc:  # noqa: BLE001 - transport exceptions retain their wire details
        if isinstance(getattr(exc, 'details', None), dict):
            return exc.details
        raise


def classify(session, request, *, failure=None, key=None, origin='list', pending_id=None):
    """Build an ``astrid.clash/1`` packet for a captured commit request.

    ``session`` is a TimelineSession. ``request`` is the original wire body
    (a nested ``base`` pin is also accepted). No outbox state is read or written.
    Network/ancestry/probe failures are returned as an unclassified packet so
    callers can save the refused intent independently of this explanation.
    """
    request = copy.deepcopy(request)
    base = _pin(request.get('base') or {
        'revision_id': request['base_revision_id'], 'publication_id': request['base_publication_id']})
    request.update(base_revision_id=base['revision_id'], base_publication_id=base['publication_id'])
    details = (failure or {}).get('details', failure or {})
    packet = {'schema': 'astrid.clash/1', 'project_id': session.project_id,
              'timeline_id': session.timeline_id, 'label': request.get('label', 'Timeline edit'),
              'key': key, 'origin': origin, 'base': base, 'head': details.get('current'),
              'runtime': {'reason': details.get('reason'),
                          'conflicts': copy.deepcopy(details.get('conflicts', []))},
              'receipts': [], 'commands': [], 'ripple_gap': None, 'classified': False,
              'pending_id': pending_id, 'next': f'tl.rebase({pending_id!r})'}
    for restart in range(4):
        packet.update(classified=False, receipts=[], ripple_gap=None, commands=[
            {'ordinal': i, 'op': call['op'], 'command': copy.deepcopy(call),
             'verdict': 'unsupported' if _unsupported(call) else 'unknown'}
            for i, call in enumerate(request['commands'])])
        try:
            head, entries = _history(session, base)
            packet['head'] = head
            base_bundle = _bundle(session, base, request['commands'])
            base_closure = Closure(base_bundle)
            head_closure = Closure(_bundle(session, head))
            records = _base_records(base_bundle, request['commands'])
            receipts, sites = _receipt_sites(entries, base_closure)
            packet['receipts'] = receipts
            remaining = [row['ordinal'] for row in packet['commands'] if row['verdict'] != 'unsupported']
            blocked = _dependents(records, remaining, [row['ordinal'] for row in packet['commands']
                                                       if row['verdict'] == 'unsupported'])
            for ordinal, needs in blocked.items():
                packet['commands'][ordinal].update(verdict='blocked', needs=needs)
            remaining = [i for i in remaining if i not in blocked]
            for _ in range(len(remaining) + 1):
                if not remaining:
                    break
                probe = _probe(session, request, remaining)
                evaluated = _pin(probe.get('evaluated_head') or probe.get('current'))
                if evaluated != head:
                    raise _HeadMoved('probe head changed')
                if probe['status'] == 'preview':
                    for ordinal in remaining:
                        packet['commands'][ordinal]['verdict'] = 'applies'
                    break
                if probe['status'] != 'conflict' or not probe.get('conflicts'):
                    raise ValueError('clash probe ' + str(probe.get('reason', probe['status'])))
                conflict = probe['conflicts'][0]
                owners = _owners(request['commands'], records, remaining, conflict, head_closure)
                for ordinal in owners:
                    row = packet['commands'][ordinal]
                    overlap = _overlap(conflict, records[ordinal], base_closure, head_closure,
                                       receipts, sites, ordinal)
                    # Some provider conflicts use ABSENT for all three wire
                    # values. Resolve presence on H rather than interpreting
                    # that placeholder as a deleted target.
                    if (_state(head_closure, conflict['ref'], conflict.get('path', []), base_closure) == ABSENT
                            or _state(head_closure, conflict['ref'], [], base_closure) == ABSENT):
                        row.update(verdict='target_missing', ref=conflict['ref'],
                                   receipt=overlap['receipt'], choices=['theirs'])
                    else:
                        row.update(verdict='overlaps', overlaps=[overlap], choices=['ours', 'theirs'])
                        if overlap['path'][-1:] == ['at'] and all(_number(overlap[k]) for k in ('base', 'theirs', 'yours')):
                            row['choices'].append('shift')
                blocked = _dependents(records, remaining, owners)
                for ordinal, needs in blocked.items():
                    packet['commands'][ordinal].update(verdict='blocked', needs=needs)
                remaining = [i for i in remaining if i not in owners and i not in blocked]
            else:
                raise ValueError('clash probe did not converge')
            _ripple_flags(packet, records, base_closure, head_closure, receipts)
            packet['classified'] = True
            packet.pop('error', None)
            return packet
        except _HeadMoved as exc:
            packet['error'] = str(exc)
            if restart == 3:
                packet['head_moving'] = True
        except Exception as exc:  # noqa: BLE001 - explanation failure must preserve refused intent
            packet['error'] = str(exc)
            return packet
    return packet
