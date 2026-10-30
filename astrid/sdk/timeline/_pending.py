"""Pure helpers for retaining refused timeline changes."""
from __future__ import annotations

import copy
import json
import uuid
from datetime import datetime, timezone


def make_record(flight, pending, failure, *, base, options=None, evaluation=None,
                rationale=None, media_input=None, imports=None):
    body = json.loads(flight['body'])
    now = datetime.now(timezone.utc).isoformat()
    logical_key = flight.get('logical_key') or (flight['key'] if flight.get('explicit_key') else None)
    part = {'base': {'revision_id': body['base_revision_id'], 'publication_id': body['base_publication_id']},
            'commands': copy.deepcopy(body['commands']),
            'commit_options': {k: copy.deepcopy(body[k]) for k in ('label', 'steps', 'merge', 'reads') if k in body},
            'rationale': copy.deepcopy(body.get('rationale')),
            'media_input': copy.deepcopy(flight.get('media_input')),
            'imports': copy.deepcopy(flight.get('imports', [])),
            'evaluation': copy.deepcopy(flight.get('evaluation', evaluation))}
    parts = [part]
    suffix = pending[flight['count']:]
    if suffix:
        parts.append({'base': copy.deepcopy(base), 'commands': copy.deepcopy(suffix),
                      'commit_options': copy.deepcopy(options), 'rationale': copy.deepcopy(rationale),
                      'media_input': copy.deepcopy(media_input), 'imports': copy.deepcopy(imports or []),
                      'evaluation': copy.deepcopy(evaluation)})
    return {'id': 'pc_' + uuid.uuid4().hex[:12], 'state': 'pending', 'rev': 1,
            'key': logical_key or 'clash-' + uuid.uuid4().hex[:12], 'key_generated': logical_key is None,
            'label': body.get('label') or 'Timeline edit',
            'origin': 'function' if (part['evaluation'] or {}).get('kind') == 'function' else 'list',
            'parts': parts, 'part': 0, 'failure': copy.deepcopy(failure),
            'head': copy.deepcopy(failure.get('details', {}).get('current')),
            'choices': {}, 'candidate': None, 'flight_fence': None, 'receipts': [], 'versions': [],
            'created_at': now, 'updated_at': now, 'dropped_reason': None}


def retain(state, flight, failure, *, pending=None, base=None, options=None, evaluation=None):
    record = make_record(flight, state['pending'] if pending is None else pending, failure,
                         base=base or state['base'], options=options if options is not None else state.get('commit_options'),
                         evaluation=evaluation if evaluation is not None else state.get('evaluation'),
                         rationale=state.get('rationale'), media_input=state.get('media_input'),
                         imports=state.get('media_imports'))
    state.setdefault('pending_changes', {})[record['id']] = record
    return record


def migrate(state):
    rejected = state.get('rejected')
    if not isinstance(rejected, dict) or rejected.get('failure', {}).get('details', {}).get('status') != 'conflict':
        return False
    retain(state, rejected['flight'], rejected['failure'], pending=rejected['commands'],
           base=rejected['base'], options=rejected.get('commit_options'), evaluation=rejected.get('evaluation'))
    del state['rejected']
    return True


def resolve(state, ref):
    if hasattr(ref, 'pending_id'):
        ref = ref.pending_id
    records = state.get('pending_changes', {})
    matches = [r for r in records.values() if r['id'] == ref or r['key'] == ref]
    if len(matches) != 1:
        from ._common import TimelineEditError
        raise TimelineEditError('pending change not found or key is ambiguous')
    return matches[0]
