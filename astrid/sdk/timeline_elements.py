"""Same-placement pack element edits through the native Runtime commit path."""
from __future__ import annotations

import copy
import json
import math
import uuid
from collections.abc import Mapping
from types import SimpleNamespace
from typing import Any

from astrid.core.element.project_packs import _json_digest, _read_document
from astrid.sdk.contracts import DomainResult, ErrorObject
from astrid.sdk.documents import Documents
from astrid.sdk.timeline.commands import validate_command


def update_parent_element(owner: Any, project: str, timeline: str, *, realm: str, clip_id: str,
                          element: dict[str, str], expected_head: str, duration: float | None = None,
                          params: dict[str, Any] | None = None, idempotency_key: str | None = None):
    key = idempotency_key or f"element-{uuid.uuid4().hex}"
    try:
        if not all(isinstance(v, str) and v for v in (project, timeline, realm, clip_id, expected_head)):
            raise ValueError('Explicit project/timeline/realm/clip/expected head are required')
        if duration is not None and (isinstance(duration, bool) or not isinstance(duration, (int, float))
                                     or not math.isfinite(duration) or duration <= 0):
            raise ValueError('Duration must be finite and positive')
        if params is not None and (not isinstance(params, dict)
                                   or len(json.dumps(params, allow_nan=False)) > 16384):
            raise ValueError('Params must be a bounded JSON object')
        opened = owner.open_bundle(project, timeline)
        if not opened.ok or not isinstance(opened.data, Mapping):
            return opened
        data = opened.data
        if data.get('head_revision_id') != expected_head or data.get('revision_id') != expected_head:
            return DomainResult.failure(ErrorObject(
                'conflict', 'Timeline head changed; inspect before making a fresh edit',
                {'expected_head': expected_head, 'actual_head': data.get('head_revision_id')}),
                idempotency_key=key)
        bundle = data['bundle']
        project_id, timeline_id = str(data['project_id']), str(data['timeline_id'])
        history = owner.history(project_id, timeline_id, limit=1)
        if not history.ok:
            return history
        head = history.data['head']
        if head['revision_id'] != expected_head:
            return DomainResult.failure(ErrorObject(
                'conflict', 'Timeline head changed; inspect before making a fresh edit',
                {'expected_head': expected_head, 'actual_head': head['revision_id']}), idempotency_key=key)
        clips = bundle['parent'].get('clips')
        if not isinstance(clips, list):
            raise ValueError('Canonical parent clips are unavailable')
        matches = [c for c in clips if isinstance(c, dict) and c.get('id') == clip_id]
        if len(matches) != 1:
            raise ValueError('Expected one existing parent effect clip')
        before = copy.deepcopy(matches[0])
        old_ref = before.get('elementRef') or before.get('element_ref')
        if (not isinstance(old_ref, dict) or old_ref.get('kind') != 'effect'
                or before.get('clipType') != old_ref.get('id')
                or isinstance(before.get('hold'), bool) or not isinstance(before.get('hold'), (int, float))
                or any(k in before for k in ('asset', 'file', 'src', 'source', 'from', 'to'))):
            raise ValueError('Update requires an existing generated hold effect without media source trimming')
        if (not isinstance(element, dict) or element.get('kind') != 'effect'
                or element.get('id') != old_ref.get('id')
                or old_ref.get('packId') is not None and old_ref['packId'] != element.get('packId')):
            raise ValueError('Update must preserve the existing effect identity')
        target = f'parent/clip:{clip_id}'
        # Runtime validates the selected declaration through its retained snapshot,
        # even when no params are authored in this edit.
        client = SimpleNamespace(documents=Documents(owner._client))
        document_id, document = _read_document(client, realm, project_id)
        if document is None or document['content']['pack_id'] != element.get('packId'):
            document_id, document = _read_document(client, realm, project_id, element.get('packId'))
        if document is None or document['content']['pack_id'] != element.get('packId'):
            raise ValueError('Element owner/revision is not admitted for this project')
        pin = {'document_id': document_id, 'version': document['version'],
               'content_digest': _json_digest(document['content'])}
        calls = [{'schema_version': 1, 'op': 'clip.set-element', 'version': '1', 'select': target,
                  'args': {'elementRef': copy.deepcopy(element), 'schema_source': pin}}]
        if duration is not None:
            calls.append({'schema_version': 1, 'op': 'clip.set', 'version': '1', 'select': target,
                          'args': {'values': {'hold': duration}, 'clear': []}})
        if params:
            calls.append({'schema_version': 1, 'op': 'clip.set-params', 'version': '1', 'select': target,
                          'args': {'values': copy.deepcopy(params), 'clear': [], 'schema_source': pin}})
        for call in calls:
            validate_command(call)
        committed = owner.commit(project_id, timeline_id, {
            'api_version': 1, 'project_id': project_id, 'timeline_id': timeline_id,
            'base_revision_id': expected_head, 'base_publication_id': head['publication_id'],
            'commands': calls, 'dry_run': False,
        }, idempotency_key=key)
        if not committed.ok:
            return committed
        new_head = committed.data.get('accepted_revision_id')
        if not isinstance(new_head, str) or not new_head:
            raise ValueError('Publication receipt omitted committed head')
        parent = committed.data['canonical_document']['parent_revision']['payload']
        clip = next(c for c in parent['clips'] if c.get('id') == clip_id)
        return DomainResult.success({
            'project_id': project_id, 'timeline_id': timeline_id, 'expected_head': expected_head,
            'new_head': new_head, 'clip_id': clip_id, 'element': element, 'duration': clip.get('hold'),
            'params': clip.get('params', {}), 'before': {
                'element': old_ref, 'duration': before.get('hold'), 'params': before.get('params', {})},
        }, receipt=committed.receipt, idempotency_key=key)
    except (ValueError, KeyError, TypeError) as exc:
        return DomainResult.failure(ErrorObject('validation_error', str(exc), {}), idempotency_key=key)
