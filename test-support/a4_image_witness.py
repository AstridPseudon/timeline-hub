from __future__ import annotations

import copy
import hashlib
import json
import os
import sys
import time
from pathlib import Path
from typing import Any

AGENT = Path('/home/user/work/wt/agt-A4-image-valid-2348')
RUNTIME = Path('/home/user/work/runtime')
WORKER = Path('/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-A4-image-valid-2348')
EVIDENCE = WORKER / 'evidence'
REALM_ROOT = Path('/tmp/w-6879f4d043/agt-A4-image-valid-2348') / f'realm-{os.getpid()}'
OUTPUT = Path('/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/app-A4-image-valid-2348-output.json')
OLD_INPUT = Path('/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-A4-image-live-2315/evidence/producer-input.json')

os.environ['ASTRID_RUNTIME_CHECKOUT'] = str(RUNTIME)
sys.path[:0] = [str(AGENT), str(RUNTIME), str(RUNTIME / 'tests')]

from _pytest.monkeypatch import MonkeyPatch  # noqa: E402
from runtime_protocol.errors import RuntimeErrorBase  # noqa: E402
from runtime_protocol.timeline_commit_port import route_path, validate_request  # noqa: E402

from astrid.sdk.timeline._command_state import ABSENT  # noqa: E402
from tests.editing_conformance import test_commit_runtime_parent_media as parent  # noqa: E402


def compact_json(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, separators=(',', ':')).encode('utf-8')


def write_json(path: Path, value: Any) -> bytes:
    data = compact_json(value) + b'\n'
    temporary = path.with_name(path.name + '.tmp')
    temporary.write_bytes(data)
    os.replace(temporary, path)
    return data


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def current_head(service: Any, project: str) -> dict[str, str]:
    value = service.get_project_timeline(project, 'film')
    return {'revision_id': value['head_revision_id'], 'publication_id': value['head_publication_id']}


def current_document(editing: Any) -> dict[str, Any]:
    return parent.current(editing)


def db_snapshot(service: Any) -> list[str]:
    return list(service.store.conn.iterdump())


def commit(service: Any, editing: Any, request: dict[str, Any], key: str) -> Any:
    return service.commit_timeline(
        editing.project, 'film', request, idempotency_key=key,
        publisher='app-image-witness', invocation_path=route_path(editing.project, 'film'),
        authorize=editing.authorize,
    )


def track_read(order: list[str]) -> dict[str, Any]:
    return {
        'kind': 'collection', 'ref': 'parent', 'path': ['config', 'tracks'],
        'members': sorted(order), 'order': list(order),
    }


def repair_request(editing: Any, base: dict[str, str], order: list[str]) -> dict[str, Any]:
    row = {'id': 'visual', 'kind': 'visual', 'app': {'opaque': [None, False]}, 'role': 'output'}
    change = {
        'op': 'list.insert', 'ref': 'parent', 'path': ['config', 'tracks'],
        'before': copy.deepcopy(ABSENT), 'value': copy.deepcopy(row), 'id': 'visual',
        'order_before': list(order), 'after_id': order[-1] if order else None,
    }
    command = {
        'schema_version': 1, 'op': 'doc.patch', 'version': '1', 'select': None,
        'args': {'changes': [change]}, 'created': ['parent/track:visual'],
    }
    read = track_read(order)
    return {
        'api_version': 1, 'project_id': editing.project, 'timeline_id': 'film',
        'base_revision_id': base['revision_id'], 'base_publication_id': base['publication_id'],
        'commands': [command], 'label': 'Repair synthetic visual track extension',
        'steps': [{
            'id': 'repair-visual-track', 'label': 'Repair synthetic visual track extension',
            'intent': '', 'tags': ['fixture'], 'command_ordinals': [0],
            'patch': [copy.deepcopy(change)], 'reads': [copy.deepcopy(read)],
        }],
        'merge': 'atomic', 'reads': [read], 'dry_run': False, 'source': {'via': 'python'},
    }


def inverse_request(editing: Any, head: dict[str, str], receipt_id: str) -> dict[str, Any]:
    command = {
        'schema_version': 1, 'op': 'timeline.inverse', 'version': '1', 'select': None,
        'args': {'publications': [receipt_id]},
    }
    return {
        'api_version': 1, 'project_id': editing.project, 'timeline_id': 'film',
        'base_revision_id': head['revision_id'], 'base_publication_id': head['publication_id'],
        'commands': [command], 'label': 'Undo Add media',
        'steps': [{
            'id': 'undo-add-media', 'label': 'Undo Add media', 'intent': '', 'tags': [],
            'command_ordinals': [0], 'patch': [], 'reads': [],
        }],
        'merge': 'fields', 'reads': [], 'dry_run': False, 'source': {'via': 'app'},
    }


def refusal(service: Any, editing: Any, request: dict[str, Any], key: str, name: str) -> dict[str, Any]:
    before = {'head': current_head(service, editing.project), 'db': db_snapshot(service)}
    try:
        commit(service, editing, request, key)
    except RuntimeErrorBase as exc:
        result = {
            'name': name, 'status': 'refused', 'exception_type': type(exc).__name__,
            'message': str(exc), 'code': getattr(exc, 'code', None),
            'details': copy.deepcopy(getattr(exc, 'details', None)),
            'head_unchanged': current_head(service, editing.project) == before['head'],
            'database_unchanged': db_snapshot(service) == before['db'],
        }
        write_json(EVIDENCE / f'refusal-{name}.json', result)
        return result
    raise AssertionError(f'{name}: malformed control was accepted')


def main() -> None:
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    REALM_ROOT.mkdir(parents=True, exist_ok=True)
    monkeypatch = MonkeyPatch()
    realm = parent.media_realm(REALM_ROOT, monkeypatch, 'image', historical=True, pristine=True)
    editing = next(realm)
    service = editing.service
    try:
        original_document = copy.deepcopy(current_document(editing))
        original_head = current_head(service, editing.project)
        payload = original_document['parent_revision']['payload']
        original_tracks = copy.deepcopy(payload['config']['tracks'])
        original_order = [row['id'] for row in original_tracks]
        assert 'visual' not in original_order
        allowed = {'id', 'kind', 'label', 'role', 'scale', 'fit', 'opacity', 'volume', 'muted', 'blendMode', 'app'}
        unsupported = {
            row['id']: sorted(set(row) - allowed) for row in original_tracks if set(row) - allowed
        }
        write_json(EVIDENCE / 'closed-track-preflight.json', {
            'allowed_keys': sorted(allowed), 'unsupported_fixture_fields': unsupported,
            'status': 'valid' if not unsupported else 'invalid',
        })
        assert not unsupported

        repair = repair_request(editing, original_head, original_order)
        validate_request(repair)
        repair_result = commit(service, editing, repair, 'a4-image-fixture-repair')
        assert repair_result['data']['status'] in {'accepted', 'merged', 'rebased'}
        repaired_document = copy.deepcopy(current_document(editing))
        repaired_head = current_head(service, editing.project)
        repaired_tracks = repaired_document['parent_revision']['payload']['config']['tracks']
        repaired = next(row for row in repaired_tracks if row['id'] == 'visual')
        assert repaired == {'id': 'visual', 'kind': 'visual', 'app': {'opaque': [None, False]}, 'role': 'output'}
        assert [row['id'] for row in repaired_tracks] == original_order + ['visual']
        assert repaired_document['parent_revision']['payload']['clips'] == original_document['parent_revision']['payload']['clips']
        assert repaired_document['shot_revisions'] == original_document['shot_revisions']
        assert repaired_document['internal_timeline_revisions'] == original_document['internal_timeline_revisions']
        write_json(EVIDENCE / 'fixture-repair-response.json', repair_result)

        old_hash = sha256(OLD_INPUT.read_bytes()) if OLD_INPUT.is_file() else 'e61c49fe584c416aa6df63156950b2158b4f72ae626460491ca9cdbce863b01d'
        write_json(EVIDENCE / 'fixture-correction.json', {
            'original_input_sha256': old_hash, 'original_input_immutable': True,
            'repair_authority': 'RuntimeService.commit_timeline + Agent astrid provider',
            'repair_request': repair, 'accepted_head_before': original_head, 'accepted_head_after': repaired_head,
            'exact_payload_difference': {
                'path': 'parent_revision.payload.config.tracks[id:visual]',
                'before': {'id': 'visual', 'kind': 'visual', 'opaque': [None, False], 'role': 'output'},
                'after': repaired,
            },
            'other_original_track_rows_unchanged': True,
            'clips_shared_sources_opaque_null_order_registry_media_revisions_unchanged': True,
        })

        pin = copy.deepcopy(editing.pins['new'])
        verified = copy.deepcopy(service.get_project_verified_media(editing.project, pin, authorize=editing.authorize))
        association = next(item for item in editing.associations if item['variant_key'] == 'new')
        entry = {
            'file': association.get('filename') or pin['object_id'], 'type': verified['media_type'],
            'media_id': pin['object_id'], 'generationId': pin['generation_id'], 'variantId': pin['variant_id'],
        }
        if 'duration_seconds' in verified:
            entry['duration'] = verified['duration_seconds']
        assert entry['type'] == 'image/png'
        assert verified['selection'] == pin
        assert set(pin) == {'asset', 'catalog_digest', 'generation_id', 'object_id', 'variant_id'}
        producer_input = {
            'projectId': editing.project, 'timelineId': 'film',
            'head': {'revisionId': repaired_head['revision_id'], 'publicationId': repaired_head['publication_id']},
            'canonicalDocument': repaired_document,
            'preparedAsset': {
                'assetKey': pin['asset'], 'mediaType': 'image', 'durationSeconds': verified.get('duration_seconds'),
                'entry': entry, 'source': 'registered', 'mediaSelection': pin,
            },
            'placement': {'trackId': 'visual', 'at': 2},
        }
        input_bytes = write_json(EVIDENCE / 'producer-input.json', producer_input)
        input_hash = sha256(input_bytes)
        write_json(EVIDENCE / 'runtime-source-facts.json', {
            'runtime_checkout': str(RUNTIME), 'runtime_commit': 'abd47e68de6d7a36bec8ac4f0f6e0bc01d98d14e',
            'agent_commit': 'f88cc5242d4b6c87b97a83878b86ec3168daa3db', 'project_id': editing.project,
            'timeline_id': 'film', 'head': repaired_head,
            'canonical_parent_revision': repaired_document['parent_revision']['revision_id'],
            'canonical_parent_content_digest': repaired_document['parent_revision']['content_digest'],
            'selection': pin, 'verified_media': verified, 'registry_entry': entry,
            'managed_output_binding': {
                key: copy.deepcopy(association.get(key)) for key in (
                    'association_id', 'task_id', 'attempt_id', 'generation_id', 'object_id', 'output_port',
                    'group_key', 'variant_key', 'ordinal', 'role', 'size', 'media_type', 'filename',
                    'durability', 'lifecycle', 'provenance') if key in association
            },
            'input_sha256': input_hash,
        })
        (EVIDENCE / 'READY').write_text('\n'.join([
            'A4 corrected authentic IMAGE producer input READY', f'input_sha256={input_hash}',
            f'original_input_sha256={old_hash}', f'project_id={editing.project}', 'timeline_id=film',
            f'head_revision_id={repaired_head["revision_id"]}', f'head_publication_id={repaired_head["publication_id"]}',
            f'canonical_parent_content_digest={repaired_document["parent_revision"]["content_digest"]}',
            f'selection_asset={pin["asset"]}', f'selection_object_id={pin["object_id"]}',
            f'selection_catalog_digest={pin["catalog_digest"]}',
            'fixture_correction=visual-track.opaque moved verbatim to visual-track.app.opaque by public doc.patch',
            'runtime_realm=live-under-task-TMPDIR', '',
        ]), encoding='utf-8')

        deadline = time.monotonic() + 25 * 60
        while not OUTPUT.is_file():
            if time.monotonic() >= deadline:
                raise TimeoutError(f'App output did not arrive within 25 minutes: {OUTPUT}')
            if current_head(service, editing.project) != repaired_head or current_document(editing) != repaired_document:
                raise RuntimeError('live Runtime fixture/head changed before App output arrived')
            time.sleep(30)

        output_bytes = OUTPUT.read_bytes()
        write_json(EVIDENCE / 'app-output.json', json.loads(output_bytes))
        output = json.loads(output_bytes)
        assert set(output) == {'request', 'idempotency_key', 'request_body_sha256'}
        request = output['request']
        body_bytes = compact_json(request)
        assert output['request_body_sha256'] == 'sha256:' + sha256(body_bytes)
        assert request['project_id'] == editing.project and request['timeline_id'] == 'film'
        assert request['base_revision_id'] == repaired_head['revision_id']
        assert request['base_publication_id'] == repaired_head['publication_id']
        assert request.get('source') == {'via': 'app'}
        validate_request(request)
        command = request['commands'][0]
        assert command['op'] == 'clip.add-media' and command.get('intent', {}) == {}
        assert command['args']['media'] == pin and command['args']['row']['track'] == 'visual'
        write_json(EVIDENCE / 'app-request-verification.json', {
            'request_body_sha256_reported': output['request_body_sha256'],
            'request_body_sha256_recomputed': 'sha256:' + sha256(body_bytes),
            'idempotency_key': output['idempotency_key'], 'base_head_match': True,
            'selection_match': True, 'command_op': command['op'], 'clip_id': command['args']['row']['id'],
        })

        accepted = commit(service, editing, request, output['idempotency_key'])
        write_json(EVIDENCE / 'accepted-response.json', accepted)
        accepted_document = current_document(editing)
        accepted_head = current_head(service, editing.project)
        parent_payload = accepted_document['parent_revision']['payload']
        added = next(clip for clip in parent_payload['clips'] if clip['id'] == command['args']['row']['id'])
        assert added == command['args']['row']
        assert parent_payload['registry']['assets'][pin['asset']] == {
            'media_id': pin['object_id'], 'type': 'image',
            'generationId': pin['generation_id'], 'variantId': pin['variant_id']}
        assert next(row for row in parent_payload['config']['tracks'] if row['id'] == 'visual') == repaired
        assert accepted_document['shot_revisions'] == repaired_document['shot_revisions']
        assert accepted_document['internal_timeline_revisions'] == repaired_document['internal_timeline_revisions']
        assert accepted['data']['status'] in {'accepted', 'merged', 'rebased'} and accepted['receipt']
        exact_retry = commit(service, editing, request, output['idempotency_key'])
        assert exact_retry == accepted
        write_json(EVIDENCE / 'accepted-exact-retry.json', exact_retry)

        foreign = parent.foreign_pin(editing)
        malformed = copy.deepcopy(request)
        malformed['commands'][0]['args']['media']['object_id'] = 'not-a-digest'
        foreign_request = copy.deepcopy(request)
        foreign_request['commands'][0]['args']['media'] = foreign
        changed_body = copy.deepcopy(request)
        changed_body['label'] = 'changed body guard'
        changed_head = copy.deepcopy(request)
        changed_head['base_revision_id'] = repaired_head['revision_id']
        changed_head['base_publication_id'] = repaired_head['publication_id']
        refusals = [
            refusal(service, editing, malformed, 'image-malformed-selection', 'malformed-selection'),
            refusal(service, editing, foreign_request, 'image-foreign-selection', 'foreign-selection'),
            refusal(service, editing, changed_body, output['idempotency_key'], 'changed-body'),
            refusal(service, editing, changed_head, 'image-changed-head', 'changed-head'),
        ]
        current = current_head(service, editing.project)
        undo = inverse_request(editing, current, accepted['receipt']['receipt_id'])
        validate_request(undo)
        preview = commit(service, editing, {**undo, 'dry_run': True}, 'image-undo-preview')
        assert preview['receipt'] is None and preview['data']['would_status'] in {'accepted', 'merged'}
        write_json(EVIDENCE / 'undo-preview.json', preview)
        undone = commit(service, editing, undo, 'image-undo')
        write_json(EVIDENCE / 'undo-response.json', undone)
        assert current_document(editing) == repaired_document
        undo_retry = commit(service, editing, undo, 'image-undo')
        assert undo_retry == undone
        write_json(EVIDENCE / 'undo-exact-retry.json', undo_retry)
        history = service.list_timeline_commits(editing.project, 'film', authorize=editing.authorize)
        write_json(EVIDENCE / 'history.json', history)
        write_json(EVIDENCE / 'results.json', {
            'status': 'PASS', 'authority': 'RuntimeService.commit_timeline + Agent astrid provider',
            'source': {'agent_commit': 'f88cc5242d4b6c87b97a83878b86ec3168daa3db',
                       'runtime_commit': 'abd47e68de6d7a36bec8ac4f0f6e0bc01d98d14e'},
            'original_input_sha256': old_hash, 'input_sha256': input_hash,
            'output_sha256': sha256(output_bytes), 'request_body_sha256': output['request_body_sha256'],
            'fixture_repair_head': repaired_head, 'accepted_head': accepted_head,
            'accepted_receipt_id': accepted['receipt']['receipt_id'], 'added_clip_id': command['args']['row']['id'],
            'undo_receipt_id': undone['receipt']['receipt_id'],
            'canonical_restored': current_document(editing) == repaired_document,
            'refusals': refusals, 'no_product_source_edits': True,
        })
    finally:
        try:
            editing.service.close()
        finally:
            realm.close()
            monkeypatch.undo()


if __name__ == '__main__':
    main()
