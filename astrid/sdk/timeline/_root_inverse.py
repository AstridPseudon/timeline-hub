"""Restore removed placement order and immutable inputs from accepted boundaries."""
from __future__ import annotations

import copy

from ._collections import AcceptedRecords
from ._command_state import ABSENT, CommandError, equal, root_identity


def recover_source(state, value, source):
    """Reopen a missing compiler input, without creating or editing shot content."""
    identity, occurrence = value['shot_id'], value['occurrence_id']
    if identity in state.bundle['shots'] and (
            occurrence in state.bundle['base_placements'] or identity not in state.bundle['source_mapping']['shots']):
        return
    if (identity not in source['shots'] or identity not in source['source_mapping']['shots']
            or not any(row['occurrence_id'] == value['occurrence_id'] and row['shot_id'] == identity
                       for row in source['placements'])):
        raise CommandError('removed occurrence source is unavailable', kind='history_unavailable')
    if identity not in state.bundle['shots']:
        state.bundle['shots'][identity] = copy.deepcopy(source['shots'][identity])
        state.bundle['source_mapping']['shots'][identity] = copy.deepcopy(source['source_mapping']['shots'][identity])
    for target, original in ((state.bundle['base_placements'], source['base_placements']),
                             (state.bundle['source_mapping']['placements'], source['source_mapping']['placements'])):
        if occurrence not in target and occurrence in original:
            target[occurrence] = copy.deepcopy(original[occurrence])


def occurrence_orders(state, records, changes):
    """Only absent-to-present reversals need an authenticated insertion position."""
    removed = {w['ref'] for w in changes if not w['path'] and w['before'] != ABSENT
               and w['after'] == ABSENT and root_identity(w['ref']) is not None
               and w['ref'].startswith('occurrence:')
               and not any(other['ref'] == 'shot:' + w['before']['value']['shot_id']
                           and not other['path'] for other in changes)}
    needed = {id(record) for record in records if any(
        w['ref'] in removed and not w['path'] and w['before'] != ABSENT and w['after'] == ABSENT
        for w in record['writes'])}
    if not needed:
        return {}
    if not isinstance(records, AcceptedRecords):
        raise CommandError('removed occurrence needs accepted order/source boundaries', kind='history_unavailable')
    result = {}
    offset = 0
    for entry in records.entries:
        count = len(entry['records']['commands'])
        commands = records[offset:offset + count]
        offset += count
        if not equal(commands, entry['records']['commands']):
            raise CommandError('root inverse records differ from accepted history', kind='history_unavailable')
        if not any(id(record) in needed for record in commands):
            continue
        before, after = records.load_boundary(entry)
        ordered = [row['occurrence_id'] for row in before['placements']]
        for record in commands:
            original = list(ordered)
            for write in record['writes']:
                if root_identity(write['ref']) is None or not write['ref'].startswith('occurrence:') or write['path']:
                    continue
                identity = write['ref'].removeprefix('occurrence:')
                if write['before'] != ABSENT and write['after'] == ABSENT:
                    if id(record) in needed:
                        source = next((image for image in (before, after)
                                       if any(equal(row, write['before']['value']) for row in image['placements'])), None)
                        if source is None:
                            raise CommandError('removed occurrence boundary changed', kind='history_unavailable')
                        recover_source(state, write['before']['value'], source)
                    ordered.remove(identity)
                elif write['before'] == ABSENT and write['after'] != ABSENT:
                    ordered.append(identity)
            if id(record) in needed:
                result[id(record)] = original
    if set(result) != needed:
        raise CommandError('removed occurrence order is unavailable', kind='history_unavailable')
    return result


def arrange_restored(state, record, original):
    """Insert restored rows relative to surviving history; leave other rows alone."""
    if original is None:
        return
    rows = state.bundle['placements']
    restored = {w['before']['value']['occurrence_id'] for w in record['writes']
                if w['ref'].startswith('occurrence:') and '/' not in w['ref']
                and not w['path'] and w['before'] != ABSENT and w['after'] == ABSENT}
    for identity in reversed(original):
        if identity not in restored:
            continue
        row = next(row for row in rows if row['occurrence_id'] == identity)
        rows.remove(row)
        following = set(original[original.index(identity) + 1:])
        index = next((i for i, other in enumerate(rows) if other['occurrence_id'] in following), len(rows))
        rows.insert(index, row)
