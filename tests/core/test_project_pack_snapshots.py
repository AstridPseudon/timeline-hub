"""Portable admission bytes and pure decoding; Runtime custody is tested by Runtime."""
from __future__ import annotations

import base64
import copy
import hashlib
import json
import shutil
from pathlib import Path

import pytest
import yaml

from astrid.core.element import project_packs as packs
from tests.core import test_project_packs
from tests.core.test_project_pack_inputs import capture_input

configured = test_project_packs.configured


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=True,
                      allow_nan=False).encode('utf-8')


@pytest.fixture
def admitted(configured):
    root, directory, _ = test_project_packs.seed()
    result = packs.admit_project_pack('realm', 'project')
    record = result['elements'][0]
    source = capture_input(configured, record)
    admission = source[1]['document']['content']['admissions'][0]
    descriptor = admission['snapshot_object']
    data = configured.media.objects[('project', descriptor['object_id'])]
    snapshot = {**descriptor, 'bytes_base64': base64.b64encode(data).decode('ascii')}
    return result, record, source, snapshot, data, root, directory


def test_admission_uploads_original_resources_and_receipt_once(admitted, configured):
    result, record, source, snapshot, data, _, _ = admitted
    envelope = json.loads(data)
    assert canonical(envelope) == data
    assert [item['path'] for item in envelope['files']] == sorted(source[2])
    assert {item['path']: base64.b64decode(item['bytes_base64'])
            for item in envelope['files']} == source[2]
    assert base64.b64decode(envelope['build_receipt_base64']) == source[3]
    closure = [{'path': name, 'sha256': hashlib.sha256(raw).hexdigest()}
               for name, raw in sorted(source[2].items())]
    assert source[1]['document']['content']['admissions'][0]['snapshot_digest'] == hashlib.sha256(canonical(closure)).hexdigest()
    assert snapshot['digest'] == 'sha256:' + hashlib.sha256(data).hexdigest()
    assert snapshot['size'] == len(data)
    before = copy.deepcopy(configured.rows)
    writes, uploads = len(configured.writes), len(configured.media.imports)
    again = packs.admit_project_pack('realm', 'project')
    assert again['documentVersion'] == result['documentVersion']
    assert configured.rows == before
    assert (len(configured.writes), len(configured.media.imports)) == (writes, uploads)
    assert (Path(record['snapshot']['root']) / '.build-receipt.json').read_bytes() == source[3]


def test_portable_resolution_after_local_sources_and_cache_are_removed(admitted, monkeypatch):
    _, record, source, snapshot, _, root, _ = admitted
    shutil.rmtree(root)
    shutil.rmtree(Path(record['snapshot']['root']).parents[3])

    def forbidden(*args, **kwargs):
        raise AssertionError('portable resolver attempted external I/O')

    monkeypatch.setattr(packs, '_open_client', forbidden)
    for name in ('read_bytes', 'read_text', 'open', 'resolve', 'is_file', 'is_dir', 'rglob'):
        monkeypatch.setattr(Path, name, forbidden)
    assert packs.admitted_element_snapshot_descriptor('realm', 'project', *source[:2], snapshot) == record['descriptor']


def test_noop_readmission_after_cache_loss_reuses_original_cas_receipt(admitted, configured):
    result, record, source, _, _, _, _ = admitted
    shutil.rmtree(Path(record['snapshot']['root']))
    before = copy.deepcopy(configured.rows)
    uploads = len(configured.media.imports)
    again = packs.admit_project_pack('realm', 'project')
    assert again['documentVersion'] == result['documentVersion']
    assert configured.rows == before and len(configured.media.imports) == uploads
    assert (Path(record['snapshot']['root']) / '.build-receipt.json').read_bytes() == source[3]


def test_explicit_legacy_readmission_backfills_one_identity(admitted, configured):
    _, _, source, _, _, _, _ = admitted
    row = configured.rows[('project', source[1]['pin']['document_id'])]
    del row['content']['admissions'][0]['snapshot_object']
    packs.materialize_project_pack('realm', 'project')
    old_digest = row['content']['admissions'][0]['snapshot_digest']
    before = row['version']
    result = packs.admit_project_pack('realm', 'project')
    updated = configured.rows[('project', source[1]['pin']['document_id'])]
    assert result['documentVersion'] == before + 1
    assert len(updated['content']['admissions']) == 1
    assert updated['content']['admissions'][0]['snapshot_digest'] == old_digest
    assert updated['content']['admissions'][0]['snapshot_object'] == source[1]['document']['content']['admissions'][0]['snapshot_object']


def test_legacy_without_snapshot_fails_with_readmission_instruction(admitted):
    _, _, source, snapshot, _, _, _ = admitted
    verified = copy.deepcopy(source[1])
    del verified['document']['content']['admissions'][0]['snapshot_object']
    with pytest.raises(ValueError, match='pack snapshot unavailable; re-admit pack'):
        packs.admitted_element_snapshot_descriptor('realm', 'project', source[0], verified, snapshot)


@pytest.mark.parametrize('metadata', [
    {'media_type': 'application/octet-stream'}, {'size': True}, {'size': 1},
    {'digest': 'sha256:' + '0' * 64}, {'object_id': 'sha256:' + '0' * 64},
])
def test_dedup_metadata_mismatch_does_not_advance_selection(configured, metadata):
    test_project_packs.seed()
    before = copy.deepcopy(configured.rows)
    selection = Path(packs.inspect_project_pack('realm', 'project')['manifestPath'])
    index = selection.read_bytes()
    configured.media.metadata = metadata
    with pytest.raises(ValueError, match='descriptor|metadata mismatch'):
        packs.admit_project_pack('realm', 'project')
    assert configured.rows == before
    assert selection.read_bytes() == index


def test_failed_upload_then_retry_uses_original_bytes_and_key(configured):
    test_project_packs.seed()
    before = copy.deepcopy(configured.rows)
    configured.media.reject = True
    with pytest.raises(ValueError, match='ingest failed'):
        packs.admit_project_pack('realm', 'project')
    assert configured.rows == before
    configured.media.reject = False
    packs.admit_project_pack('realm', 'project')
    assert configured.media.imports[0] == configured.media.imports[1]


def test_document_cas_retry_reuses_original_bytes_and_upload_identity(configured):
    test_project_packs.seed()
    before = copy.deepcopy(configured.rows)
    configured.reject_update = True
    with pytest.raises(ValueError, match='CAS rejected'):
        packs.admit_project_pack('realm', 'project')
    assert configured.rows == before
    configured.reject_update = False
    packs.admit_project_pack('realm', 'project')
    assert configured.media.imports[0] == configured.media.imports[1]


def test_backfill_cannot_replace_original_closure(admitted, configured):
    _, _, source, _, _, root, _ = admitted
    row = configured.rows[('project', source[1]['pin']['document_id'])]
    del row['content']['admissions'][0]['snapshot_object']
    packs.materialize_project_pack('realm', 'project')
    # A pack-only description change leaves the selected element revision fixed.
    manifest = yaml.safe_load((root / 'pack.yaml').read_text())
    manifest['description'] += ' changed'
    (root / 'pack.yaml').write_text(yaml.safe_dump(manifest))
    before = copy.deepcopy(configured.rows)
    with pytest.raises(ValueError, match='closure changed'):
        packs.admit_project_pack('realm', 'project')
    assert configured.rows == before


@pytest.mark.parametrize('damage', ['missing', 'extra', 'digest', 'size', 'bool_size', 'mime', 'bytes', 'base64'])
def test_verified_object_must_match_exact_descriptor(admitted, damage):
    _, _, source, snapshot, _, _, _ = admitted
    snapshot = copy.deepcopy(snapshot)
    if damage == 'missing':
        del snapshot['size']
    elif damage == 'extra':
        snapshot['path'] = '/tmp/caller'
    elif damage == 'digest':
        snapshot['digest'] = snapshot['object_id'] = 'sha256:' + '0' * 64
    elif damage in ('size', 'bool_size'):
        snapshot['size'] = 1 if damage == 'size' else True
    elif damage == 'mime':
        snapshot['media_type'] = 'text/plain'
    elif damage == 'bytes':
        snapshot['bytes_base64'] = base64.b64encode(b'changed').decode('ascii')
    else:
        snapshot['bytes_base64'] += '\n'
    with pytest.raises(ValueError):
        packs.admitted_element_snapshot_descriptor('realm', 'project', *source[:2], snapshot)


@pytest.mark.parametrize('damage', [
    'duplicate_key', 'duplicate_path', 'order', 'hash', 'base64', 'noncanonical_base64',
    'extra', 'absolute', 'traversal', 'dot', 'backslash', 'nul', 'receipt', 'spaces',
])
def test_portable_envelope_rejects_malformed_resources(admitted, damage):
    _, _, _, _, data, _, _ = admitted
    envelope = json.loads(data)
    first = envelope['files'][0]
    if damage == 'duplicate_key':
        data = b'{"files":[],"files":[],"build_receipt_base64":"e30="}'
    elif damage == 'duplicate_path':
        envelope['files'].append(first)
    elif damage == 'order':
        envelope['files'].reverse()
    elif damage == 'hash':
        first['sha256'] = '0' * 64
    elif damage == 'base64':
        first['bytes_base64'] += '\n'
    elif damage == 'noncanonical_base64':
        first['bytes_base64'] = 'Zh=='  # Decodes as f; canonical spelling is Zg==.
    elif damage == 'extra':
        first['source'] = '/tmp/source'
    elif damage in ('absolute', 'traversal', 'dot', 'backslash', 'nul'):
        first['path'] = {'absolute': '/pack.yaml', 'traversal': '../pack.yaml',
                         'dot': './pack.yaml', 'backslash': 'a\\pack.yaml',
                         'nul': 'pack\x00.yaml'}[damage]
    elif damage == 'receipt':
        envelope['build_receipt_base64'] = base64.b64encode(b'{"x":1,"x":2}').decode('ascii')
    else:
        data = json.dumps(envelope, indent=2).encode()
    if damage not in ('duplicate_key', 'spaces'):
        data = canonical(envelope)
    with pytest.raises(ValueError):
        packs._snapshot_resources(data)


def test_nonascii_resource_paths_keep_original_admission_closure(configured):
    root, directory, manifest = test_project_packs.seed()
    (directory / 'café.png').write_bytes(b'asset')
    manifest['rendering']['effects/reveal']['resources'].append(
        {'kind': 'asset', 'path': 'rendering/elements/effects/reveal/café.png'})
    (root / 'pack.yaml').write_text(yaml.safe_dump(manifest))
    # Main's canonical resource grammar is ASCII-only; do not broaden admission.
    with pytest.raises(ValueError, match='does not match'):
        packs.admit_project_pack('realm', 'project')
    files = {'pack.yaml': b'manifest', 'café.png': b'asset'}
    closure = [{'path': name, 'sha256': hashlib.sha256(raw).hexdigest()}
               for name, raw in sorted(files.items())]
    assert packs._closure_digest(closure) == hashlib.sha256(canonical(closure)).hexdigest()
    assert packs._closure_digest(closure) != packs._json_digest(closure).removeprefix('sha256:')
    portable = packs._portable_snapshot(files, b'{"original":"receipt"}')
    assert b'caf\\u00e9.png' in portable
    assert packs._snapshot_resources(portable) == (files, b'{"original":"receipt"}')
