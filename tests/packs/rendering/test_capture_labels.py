"""Source-bound labels from the SDK projector through host CAS materialization.

Runtime admission is doubled here; these tests do not qualify its certification.
"""
import hashlib
import json
import zipfile
from argparse import Namespace
from copy import deepcopy
from pathlib import Path
from types import SimpleNamespace

import pytest

from astrid.core.execution.generic_host import GenericPackHost, HostError
from astrid.core.rendering.verified_source import SOURCE_ENV, inherited_source
from astrid.packs.rendering.actions.render import managed_timeline
from astrid.packs.rendering.actions.timeline_visualize import composed_frame, filmstrip_execution
from astrid.packs.rendering.actions.timeline_visualize.inspection_contract import inspect_filmstrip
from astrid.packs.rendering.actions.timeline_visualize.provenance import snapshot_label
from tests.packs.rendering.test_timeline_offline_inspection import make_bundle
from tests.sdk.test_capture_closure_source import ClosureClient, candidate, prepare
from tests.timeline.test_authoring_bundle import AUDIO, OLD, _digest, _replace_values


@pytest.fixture
def capture(tmp_path, monkeypatch):
    monkeypatch.delenv(SOURCE_ENV, raising=False)
    monkeypatch.setattr(managed_timeline, '_runtime_snapshot_registry',
                        lambda registry, **_kwargs: deepcopy(registry))

    def build(*, working_copy=False, cas_only=False):
        client = ClosureClient()
        payloads = {OLD: b'exact picture', AUDIO: b'exact audio'}
        replacements = {old: 'sha256:' + hashlib.sha256(data).hexdigest() for old, data in payloads.items()}
        objects = {replacements[old]: data for old, data in payloads.items()}
        client.parent = _replace_values(client.parent, replacements)
        client.shots = _replace_values(client.shots, replacements)
        client.internals = _replace_values(client.internals, replacements)
        for row in [client.parent, *client.shots, *client.internals]:
            row['content_digest'] = _digest(row['payload'])
        preview = candidate(client) if working_copy else None
        authority = prepare(client, **({'authoring_preview': preview} if preview else {}))
        snapshot = authority['capture_snapshot']
        raw = json.dumps(snapshot, sort_keys=True, separators=(',', ':')).encode()
        digest = 'sha256:' + hashlib.sha256(raw).hexdigest()
        objects[digest] = raw
        canonical = snapshot['metadata']['capture_authority']
        ref = {'digest': digest, 'project_id': canonical['project_id'], 'timeline_id': canonical['timeline_id'],
               'revision_id': canonical['parent_revision_id'], 'revision_digest': canonical['parent_content_digest'],
               'source_kind': 'working_copy' if working_copy else 'revision'}
        if working_copy:
            marker = snapshot['metadata']['working_copy']
            ref['revision_digest'] = marker['candidate_digest']
            ref['working_copy'] = {
                'candidate_digest': marker['candidate_digest'], 'publication_digest': marker['publication_digest'],
                'base_revision_id': marker['base_parent']['revision_id'],
                'base_revision_digest': marker['base_parent']['content_digest'],
            }
        if cas_only:
            ref = {'digest': digest, 'source_kind': 'cas', 'project_id': canonical['project_id']}
        handed = {key: value for key, value in authority.items() if key != 'capture_snapshot'}
        handed['capture_snapshot_ref'] = ref
        spec = {'authority_context': handed, 'input_object_ids': list(objects),
                'spec': {'inputs': {'filmstrip_authority': json.dumps(handed)}}}
        host = GenericPackHost(pack_roots=[tmp_path], client=SimpleNamespace(
            get_object=lambda key: objects['sha256:' + key]))
        values = host._materialize_inputs(spec, tmp_path / 'attempt')
        hydrated = json.loads(values['filmstrip_authority'])
        assert hydrated['capture_snapshot'] == snapshot
        assert objects[digest] == raw
        return snapshot, ref, values, hydrated

    return build


@pytest.mark.parametrize('working_copy', [False, True])
def test_real_capture_producer_ref_and_host_source_label(capture, working_copy):
    snapshot, ref, values, _ = capture(working_copy=working_copy)
    assert snapshot_label(snapshot)['status'] == 'uncertified'
    source = values.timeline_source
    assert source.read()['ref'] == ref
    label = snapshot_label(snapshot, source=source)
    if working_copy:
        assert label == {'status': 'candidate', 'label': 'unsaved candidate based on committed revision parent-1',
                         'actual_revision_id': None, 'base_revision_id': 'parent-1'}
    else:
        assert label == {'status': 'committed', 'label': 'committed revision parent-1',
                         'actual_revision_id': 'parent-1', 'base_revision_id': None}


@pytest.mark.parametrize('working_copy', [False, True])
def test_cas_ref_never_promotes_leftover_capture_metadata(capture, working_copy):
    snapshot, _, values, _ = capture(working_copy=working_copy, cas_only=True)
    assert values.timeline_source is None
    label = snapshot_label(snapshot, source=values.timeline_source)
    assert label['status'] == 'uncertified'
    assert label['label'].startswith('UNCERTIFIED ')
    assert 'committed' not in label['label']
    assert label['actual_revision_id'] is None
    if working_copy:
        marker = snapshot['metadata']['working_copy']
        assert label['base_revision_id'] == marker['base_parent']['revision_id']
        assert marker['candidate_parent_revision_id'] in label['label']


@pytest.mark.parametrize('change', ['config', 'registry', 'metadata', 'numeric', 'revision', 'scope'])
def test_source_is_bound_to_exact_snapshot(capture, change):
    snapshot, _, values, _ = capture()
    replacement = deepcopy(snapshot)
    if change == 'metadata':
        replacement['metadata']['working_copy'] = {'base_parent': {'revision_id': 'forged'}}
    elif change == 'numeric':
        replacement['config']['clips'][0]['hold'] = float(replacement['config']['clips'][0]['hold'])
    elif change == 'revision':
        replacement['metadata']['capture_authority']['parent_revision_id'] = 'other-revision'
    elif change == 'scope':
        replacement['project_slug'] = 'other-project'
    else:
        replacement[change]['forged'] = True
    assert json.dumps(replacement, sort_keys=True) != json.dumps(snapshot, sort_keys=True)
    with pytest.raises(ValueError, match='differs from verified source snapshot'):
        snapshot_label(replacement, source=values.timeline_source)


def test_caller_json_cannot_supply_source_or_certify_metadata(capture):
    snapshot, ref, _, _ = capture()
    for source in (ref, {'status': 'committed', 'label': 'committed revision parent-1'}, True):
        with pytest.raises(ValueError, match='host-owned'):
            snapshot_label(snapshot, source=source)
    snapshot['metadata'].update(certified=True, source_kind='revision', snapshot_label='committed revision forged')
    label = snapshot_label(snapshot)
    assert label['status'] == 'uncertified'
    assert label['actual_revision_id'] is None


def test_prepared_pair_replacement_cannot_reuse_source(capture, monkeypatch):
    snapshot, _, values, _ = capture()
    monkeypatch.setenv(SOURCE_ENV, values.timeline_source._anchor)
    path = Path(values['timeline'])
    path.write_text('{}')
    with pytest.raises(ValueError, match='prepared timeline bytes differ'):
        inherited_source(path, values['assets_registry'])
    assert snapshot_label(snapshot)['status'] == 'uncertified'


def test_host_ref_mismatch_is_refused(tmp_path):
    from tests.packs.rendering.test_verified_source import admitted

    host, spec, _, ref = admitted(tmp_path, capture=True)
    spec['authority_context']['capture_snapshot_ref'] = {**ref, 'revision_id': 'different'}
    with pytest.raises(HostError, match='reference differs from admitted context'):
        host._materialize_inputs(spec, tmp_path / 'attempt')


@pytest.mark.parametrize('working_copy', [False, True])
@pytest.mark.parametrize('cas_only', [False, True])
@pytest.mark.parametrize('show_inputs', [False, True])
def test_source_bound_label_reaches_exported_pages_and_receipt(
    capture, monkeypatch, tmp_path, working_copy, cas_only, show_inputs,
):
    from PIL import Image

    snapshot, _, values, authority = capture(working_copy=working_copy, cas_only=cas_only)
    authority['snapshot_label'] = {'status': 'committed', 'label': 'committed revision forged'}
    authority['certified'] = True
    source = values.timeline_source
    if source:
        monkeypatch.setenv(SOURCE_ENV, source._anchor)
    label = snapshot_label(snapshot, source=source)

    class Frames:
        def __init__(self, *args, **kwargs):
            pass

        def capture(self, cards, out_root, resolution):
            for card in cards:
                path = Path(out_root) / card['image']
                path.parent.mkdir(parents=True, exist_ok=True)
                Image.new('RGB', (32, 18), 'red').save(path)
            return {'evidence_source': 'test_capture'}

        def close(self, **kwargs):
            pass

    monkeypatch.setattr(composed_frame, 'RemotionFrameProvider', Frames)
    args = Namespace(filmstrip_authority=json.dumps(authority), project_slug='demo', range_value=None,
                     timeline=Path(values['timeline']), assets_registry=Path(values['assets_registry']),
                     out=tmp_path / 'result', frame=0, show=['output', 'inputs'] if show_inputs else ['output'])
    result = filmstrip_execution.execute_filmstrip(args)
    assert result['snapshot_label'] == label
    assert result['outputs']['snapshot_label'] == label
    with zipfile.ZipFile(result['outputs']['filmstrip_bundle']) as bundle:
        index = json.loads(bundle.read('frame-index.json'))
        assert index['provenance']['revision'] == label
        if show_inputs:
            assert index['static_surface']['mode'] == 'paired_rows'
        assert label['label'] in bundle.read('filmstrip.md').decode()
    assert inspect_filmstrip(result['manifest_path'])['data']['records'][0]['revision']['status'] == 'uncertified'


@pytest.mark.parametrize('legacy', [False, True])
def test_offline_bundle_is_uncertified_without_rewriting_bytes(tmp_path, legacy):
    manifest, _ = make_bundle(tmp_path, legacy=legacy)
    before = {path: path.read_bytes() for path in tmp_path.rglob('*') if path.is_file()}
    result = inspect_filmstrip(manifest)
    assert result['ok']
    assert result['data']['records'][0]['revision']['label'].startswith('UNCERTIFIED ')
    assert inspect_filmstrip(manifest, section='placements')['ok']
    assert {path: path.read_bytes() for path in before} == before


def test_native_file_preview_without_source_is_usable():
    from astrid.packs.rendering.actions.timeline_visualize.filmstrip_cards import plan_filmstrip

    snapshot = {'project_slug': 'demo', 'timeline_id': 'cut', 'render_run_id': 'native',
                'video_digest': 'sha256:native', 'fps_rational': [30, 1], 'duration_frames': 30,
                'tracks': [], 'clips': [], 'scripts': [], 'metadata': {}}
    result = plan_filmstrip(snapshot, {'every': 1})
    assert result['cards']
    assert result['provenance']['revision']['status'] == 'uncertified'
