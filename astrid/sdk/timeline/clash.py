"""Explain a saved timeline edit conflict from verified Runtime history."""
from __future__ import annotations

import copy
import uuid

from ._command_state import CommandError
from ._commit_patch import _prefix, canonical_site, record_sites
from ._doc_patch import Closure
from .sync import _pin, _response


class _HeadMoved(Exception):
    pass


def _history(session, base):
    """Verify public history pages and return the entries after ``base``."""
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


def _addresses(ref, path, closure):
    """Include stable aliases for a write across physical revision changes."""
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
            pass
    return result


def _touches(left, right):
    return any(a == b and _prefix(p, q) for a, p in left for b, q in right)


def _receipt_sites(entries, base):
    """Summarize each intervening receipt by its touched refs and paths."""
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
        touched, addresses = [], []
        for record in recorder['commands']:
            for site in record_sites(record, before):
                ref, path = site['ref'], copy.deepcopy(site['path'])
                address = _addresses(ref, path, before) + _addresses(ref, path, after)
                addresses.extend(address)
            for write in [*record.get('writes', []), *record.get('derived_writes', [])]:
                ref, path = write['ref'], copy.deepcopy(write['path'])
                public = {'ref': ref, 'path': path}
                if public not in touched:
                    touched.append(public)
        data = entry['receipt']['result']
        receipts.append({'publication_id': entry['publication_id'],
                         'label': data.get('label', recorder.get('label')),
                         'publisher': entry['publisher'], 'touched': touched,
                         'touches_conflict': False})
        sites.append(addresses)
        before = after
    return receipts, sites


def _part(record):
    parts = record.get('parts')
    if isinstance(parts, list) and parts:
        index = record.get('part', 0)
        if type(index) is int and 0 <= index < len(parts):
            return parts[index]
    return record


def _summary(record, conflicts, receipts):
    label = record.get('label') or 'Timeline edit'
    pending_id = record.get('id') or 'unknown'
    match = next((receipt for receipt in receipts if receipt.get('touches_conflict')), None)
    if match:
        who = f" ({match['publisher']})" if match.get('publisher') else ''
        return (f'"{label}" was not committed: "{match.get("label") or "Another edit"}"{who} '
                f'changed a conflicting part after your edit was made. Your edit is saved as '
                f'{pending_id}; nothing is lost.')
    if conflicts and receipts:
        return (f'"{label}" was not committed: the timeline changed after your edit was made. '
                f'Your edit is saved as {pending_id}; nothing is lost.')
    return (f'"{label}" was not committed: the timeline changed after your edit was made. '
            f'Your edit is saved as {pending_id}; nothing is lost.')


def explain(session, record):
    """Build an ``astrid.clash/2`` summary for a durably saved pending record."""
    record = copy.deepcopy(record)
    part = _part(record)
    base = _pin(part.get('base') or record.get('base'))
    failure = record.get('failure') or {}
    details = failure.get('details', failure)
    conflicts = copy.deepcopy(details.get('conflicts', []))
    packet = {'schema': 'astrid.clash/2', 'pending_id': record.get('id'),
              'label': record.get('label', 'Timeline edit'), 'key': record.get('key'),
              'origin': record.get('origin', 'list'), 'base': base,
              'head': copy.deepcopy(details.get('current') or record.get('head')),
              'conflicts': conflicts, 'receipts': None}
    try:
        head, entries = _history(session, base)
        base_bundle = session._capture_bundle({'base': base, 'pending': []})
        receipts, sites = _receipt_sites(entries, Closure(base_bundle))
        for conflict in conflicts:
            try:
                target = _addresses(conflict['ref'], conflict.get('path', []), Closure(base_bundle))
            except (KeyError, CommandError):
                continue
            for receipt, touched in zip(receipts, sites):
                if _touches(touched, target) and not receipt.get('touches_conflict'):
                    receipt['touches_conflict'] = True
        packet['head'] = head
        packet['receipts'] = receipts
    except Exception:  # noqa: BLE001 - enrichment must not disturb the saved edit
        pass
    packet['summary'] = _summary(record, conflicts, packet['receipts'] or [])
    pending_id = record.get('id')
    packet['next'] = f'tl.retry({pending_id!r})' if pending_id else 'tl.pending_list()'
    return packet


def _probe(session, request, merge, reads):
    """Send a dry-run probe without changing the saved request's merge contract."""
    body = {key: copy.deepcopy(value) for key, value in request.items()
            if key not in {'base', 'reads', 'merge', 'commands', 'key', 'origin'}}
    body.update(api_version=1, project_id=session.project_id, timeline_id=session.timeline_id,
                commands=copy.deepcopy(request['commands']), merge=merge,
                reads=copy.deepcopy(reads), dry_run=True)
    body.setdefault('source', {'via': 'python'})
    try:
        return _response(session.client.timelines.commit(
            session.project_id, session.timeline_id, body,
            idempotency_key='clash-probe-' + uuid.uuid4().hex))['data']
    except Exception as exc:  # noqa: BLE001 - retain wire details for J2's probe case
        if isinstance(getattr(exc, 'details', None), dict):
            return exc.details
        raise
