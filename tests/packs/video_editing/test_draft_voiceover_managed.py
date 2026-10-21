"""Bounded combined source checks, with the generated client's wire transport.

No health response, live Runtime, child worker, or requester acceptance is faked.
The wire fixture supplies catalog responses and bytes; host context, speech
preparation, native capture, proposal validation and manifest harvest are real.
"""
from __future__ import annotations

import copy
import hashlib
import io
import json
import wave
from contextlib import nullcontext
from dataclasses import replace
from types import SimpleNamespace
from urllib.parse import parse_qsl, unquote, urlsplit

import pytest

from astrid.core.env_vars import ASTRID_INTERNAL_INVOCATION
from astrid.core.execution.executor import _action_context as action_context
from astrid.core.execution.executor._action_context import (
    _require_action_context,
)
from astrid.core.execution.executor.registry import ExecutorRegistry
from astrid.core.execution.executor.runner import run_executor
from astrid.packs.video_editing.shared import draft_voiceover as vo
from astrid.sdk import AstridClient
from astrid.sdk.remote import RemoteAstridClient
from astrid.sdk.timeline.commit import _digest
from astrid.sdk.timeline.producer import build_producer_batch
from astrid.sdk.workspace_client import WorkspaceClient, WorkspaceClientError
from tests.core.execution.test_python_action_context import managed_invocation as managed_invocation
from tests.editing_conformance.test_recipe_native_voiceover import _voiceover_bundle_and_outcome


def wav_bytes(sample):
    out = io.BytesIO()
    with wave.open(out, 'wb') as audio:
        audio.setnchannels(1)
        audio.setsampwidth(2)
        audio.setframerate(8000)
        audio.writeframes(sample * (8000 * 4))
    return out.getvalue()


@pytest.fixture
def media_wire():
    payload = wav_bytes(b'\x01\x00')
    object_id = 'sha256:' + hashlib.sha256(payload).hexdigest()
    selection = dict(asset='draft-voiceover-vo', generation_id='generation-new',
                     variant_id='variant-new', object_id=object_id,
                     catalog_digest='sha256:' + 'b' * 64)
    verified = dict(selection=selection, media_type='audio/wav', size=len(payload),
                    duration_seconds=4)
    output = dict(association_id='association', object_id=object_id, digest=object_id,
                  project_id='project', generation_id='generation-new',
                  version=2, lifecycle={'version': 2}, name='speech')
    f = SimpleNamespace(payload=payload, selection=selection, verified=verified,
                        output=output, objects={object_id: payload}, calls=[], status=200)

    def wire(method, path, headers, body):
        assert method == 'GET' and body is None
        assert headers['Authorization'] == 'Bearer conformance-token'
        parsed = urlsplit(path)
        query = dict(parse_qsl(parsed.query))
        f.calls.append((parsed.path, query))
        if parsed.path.startswith('/v1/objects/'):
            data = f.objects[unquote(parsed.path.removeprefix('/v1/objects/'))]
            return 200, {'Content-Type': 'application/octet-stream'}, data
        assert parsed.path.startswith('/v1/projects/project/media-selection')
        if f.status != 200:
            return f.status, {}, json.dumps({'code': 'forbidden', 'message': 'scope refused'}).encode()
        if parsed.path.endswith('/verified'):
            assert query == f.selection
            value = f.verified
        else:
            assert query == {'association_id': 'association', 'object_id': object_id, 'version': '2'}
            value = f.selection
        return 200, {'Content-Type': 'application/json'}, json.dumps(value).encode()

    workspace = WorkspaceClient('http://127.0.0.1:8765', 'conformance-token')
    # The generated client explicitly supports a conformance wire transport.
    workspace._generated._transport = wire
    f.workspace = workspace
    f.client = AstridClient(remote=RemoteAstridClient(workspace))
    return f


def test_fixed_normal_readers_bind_exact_selection_metadata_and_real_wav(media_wire):
    f = media_wire
    f.output['selection'] = copy.deepcopy(f.selection)
    selected, info = vo._read_authoritative_media_info(f.client, 'project', f.output)
    assert selected == f.selection and info == f.verified
    with wave.open(io.BytesIO(f.payload), 'rb') as audio:
        assert audio.getnframes() / audio.getframerate() == info['duration_seconds']
    assert [path for path, _ in f.calls] == [
        '/v1/projects/project/media-selection', '/v1/projects/project/media-selection/verified',
        '/v1/objects/' + f.selection['object_id'].replace(':', '%3A')]


def test_reader_does_not_use_mutable_client_methods_as_authority(media_wire):
    f = media_wire
    def forged(*args, **kwargs):
        pytest.fail('caller-installed reader used')
    f.client.get_project_media_selection = forged
    f.workspace.get_project_media_selection = forged
    f.workspace.get_project_verified_media = forged
    assert vo._read_authoritative_media_info(f.client, 'project', f.output)[0] == f.selection
    with pytest.raises(vo.VoiceoverSyncError, match='normal Runtime client'):
        vo._read_authoritative_media_info(SimpleNamespace(
            get_project_media_selection=forged, get_project_verified_media=forged), 'project', f.output)


@pytest.mark.parametrize('claim', [
    {'project_id': 'foreign'}, {'asset': 'other'}, {'generation_id': 'other'},
    {'variant_id': 'other'}, {'object_id': 'sha256:' + 'c' * 64},
    {'catalog_digest': 'sha256:' + 'c' * 64},
    {'selection': {'association_id': 'foreign'}},
    {'selection': {'project_id': 'foreign'}},
    {'source': {'generation_id': 'other'}},
    {'digest': 'sha256:' + 'd' * 64}, {'version': 3}, {'version': True},
    {'lifecycle': {'version': True}},
])
def test_conflicting_output_claims_refuse(media_wire, claim):
    f = media_wire
    with pytest.raises(vo.VoiceoverSyncError, match='media .*|media selector'):
        vo._read_authoritative_media_info(f.client, 'project', {**f.output, **claim})
    assert not any(path.endswith('/verified') for path, _ in f.calls)


@pytest.mark.parametrize('field', ['asset', 'generation_id', 'variant_id', 'object_id', 'catalog_digest'])
def test_runtime_selection_cannot_replace_any_known_output_identity(media_wire, field):
    f = media_wire
    f.output.update(selection=copy.deepcopy(f.selection))
    f.selection = {**f.selection, field: 'sha256:' + 'd' * 64 if 'digest' in field or field == 'object_id' else 'other'}
    with pytest.raises(vo.VoiceoverSyncError, match='differs from the bound output'):
        vo._read_authoritative_media_info(f.client, 'project', f.output)


@pytest.mark.parametrize('change', [
    {'duration_seconds': 0}, {'duration_seconds': True}, {'duration_seconds': float('inf')},
    {'size': True}, {'size': 0}, {'size': 1}, {'media_type': 'video/mp4'},
    {'selection': {}}, {'project_id': 'foreign'}, {'association_id': 'foreign'},
])
def test_invalid_verified_media_refuses(media_wire, change):
    f = media_wire
    f.verified = {**f.verified, **change}
    with pytest.raises(vo.VoiceoverSyncError):
        vo._read_authoritative_media_info(f.client, 'project', f.output)


def test_same_size_wrong_bytes_refuse(media_wire):
    f = media_wire
    f.objects[f.selection['object_id']] = f.payload[:-1] + b'\x01'
    with pytest.raises(vo.VoiceoverSyncError, match='byte hash or size'):
        vo._read_authoritative_media_info(f.client, 'project', f.output)


def test_runtime_authorization_failure_remains_visible(media_wire):
    f = media_wire
    f.status = 403
    with pytest.raises(WorkspaceClientError) as error:
        vo._read_authoritative_media_info(f.client, 'project', f.output)
    assert error.value.status == 403 and error.value.code == 'forbidden'


@pytest.fixture
def combined(request, media_wire, monkeypatch):
    f, media = request.getfixturevalue('managed_invocation'), media_wire
    authored, _ = _voiceover_bundle_and_outcome()
    authored['project_id'], authored['timeline_id'] = 'project', 'timeline'
    # Existing canonical lowering fixture: real source graph, with no imported
    # host module or replacement helper/capture implementation.
    shot = authored['shots'][authored['placements'][0]['shot_id']]
    old_bytes = wav_bytes(b'\x00\x00')
    old_id = 'sha256:' + hashlib.sha256(old_bytes).hexdigest()
    old = dict(asset='voice', generation_id='generation-old', variant_id='variant-old',
               object_id=old_id, catalog_digest='sha256:' + 'a' * 64)
    shot['internal_timeline']['registry']['assets']['voice'].update(media_id=old_id, selection=old)
    shot['payload']['metadata'][vo.KEY]['audio_media_id'] = old_id
    media.objects[old_id] = old_bytes
    scripts = {'revision_id': authored['base_parent']['revision_id'], 'occurrences': [
        {'occurrence_id': 'occ-1', 'status': 'present', 'text': 'Long new narration'}]}
    f.target['base_revision_id'] = authored['base_parent']['revision_id']
    f.bound['admitted_target'] = copy.deepcopy(f.target)
    f.heads = [dict(head_revision_id=f.target['base_revision_id'], head_publication_id='publication')] * 2
    f.published = []
    f.authored, f.scripts, f.media = authored, scripts, media
    remote = media.client._remote
    monkeypatch.setattr(remote.projects, 'show', lambda *a: {'project_id': 'project'})
    monkeypatch.setattr(remote.timelines, 'resolve_scope', lambda *a: {'timeline_id': 'timeline'})
    monkeypatch.setattr(remote.timelines, 'script', lambda *a, **k: scripts)
    monkeypatch.setattr(remote.timelines, 'open_composition', lambda *a: {'summary': f.heads.pop(0)})
    target = SimpleNamespace(open=lambda: copy.deepcopy(authored), validate=lambda work: {},
                             diff=lambda work: {'changes': ['voiceover']},
                             preview=lambda work: {'candidate_digest': _digest(work)},
                             publish=lambda *a, **k: f.published.append(True))
    monkeypatch.setattr(media.client, 'open_authoring_target', lambda *a: target)
    monkeypatch.setattr(action_context, '_managed_read_client',
                        lambda context: nullcontext(media.client))
    monkeypatch.setenv(ASTRID_INTERNAL_INVOCATION, '1')
    # Serve the old pin through the same generated readers, with original wire
    # transport still handling the new association and actual object bytes.
    wire = media.workspace._generated._transport

    def with_old(method, path, headers, body):
        parsed = urlsplit(path)
        query = dict(parse_qsl(parsed.query))
        if query.get('asset') == 'voice':
            media.calls.append((parsed.path, query))
            value = (dict(selection=old, media_type='audio/wav', size=len(old_bytes), duration_seconds=4)
                     if parsed.path.endswith('/verified') else old)
            return 200, {}, json.dumps(value).encode()
        return wire(method, path, headers, body)

    media.workspace._generated._transport = with_old
    f.speech_calls = []

    def speech(capability, **kwargs):
        assert capability == 'generation.generate_speech'
        assert _require_action_context().producer['task_id'] == 'outer-task'
        f.speech_calls.append(kwargs)
        manifest = {'text': kwargs['inputs']['text'], 'text_sha256': vo.digest(kwargs['inputs']['text'])[7:],
                    'settings': dict(vo.DEFAULT_SETTINGS), 'audio_sha256': media.selection['object_id'][7:],
                    'duration_seconds': 99}
        manifest_bytes = json.dumps(manifest).encode()
        manifest_id = 'sha256:' + hashlib.sha256(manifest_bytes).hexdigest()
        media.objects[manifest_id] = manifest_bytes
        return SimpleNamespace(ok=True, run_id='inner-run', kernel_task_id='inner-speech',
                               kernel_attempt_id='inner-attempt', outputs={'managed_outputs': [
                                   media.output, {'name': 'speech_manifest', 'object_id': manifest_id}]})

    monkeypatch.setattr('astrid.sdk.invoke', speech)
    return f


def invoke(f, **inputs):
    request = replace(f.request, inputs={**f.request.inputs, 'occurrence_ids': ['occ-1'], **inputs})
    return run_executor(request, ExecutorRegistry([f.definition]), _admission=f.bound)


def test_combined_action_prepares_nonempty_claim_bound_proposal_and_standard_manifest(combined):
    f = combined
    result = invoke(f, timing_policy='ripple')
    proposal = result.payload['action_result']['authoring_proposal']
    assert set(proposal) == {'schema_version', 'producer', 'admitted_target', 'commands',
                             'rationale', 'proposal_digest'}
    assert proposal['commands'] and proposal['producer']['task_id'] == 'outer-task'
    assert proposal['admitted_target'] == f.target and not f.published
    assert len(f.speech_calls) == 1
    assert proposal['producer']['task_id'] != 'inner-speech'
    assert build_producer_batch(proposal)['commands'][0]['op'] == 'producer.guard'
    assert result.outputs[0]['content_hash'] == _file_hash(f.request.out / 'authoring-proposal.json')
    manifest = json.loads((f.request.out / 'manifest.json').read_text())
    assert manifest['outputs'][0]['artifact_type'] == 'timeline/authoring-proposal'
    assert manifest['outputs'][0]['content_hash'] == result.outputs[0]['content_hash']
    assert any(command['op'] == 'occurrence.swap-media' for command in proposal['commands'])
    draft = next(command for command in proposal['commands'] if command['op'] == 'shot.set')
    assert draft['args']['values']['metadata']['draft_voiceover']['duration_seconds'] == 4


def _file_hash(path):
    return 'sha256:' + hashlib.sha256(path.read_bytes()).hexdigest()


@pytest.mark.parametrize('field', ['head_revision_id', 'head_publication_id'])
@pytest.mark.parametrize('when', [0, 1])
def test_combined_refuses_changed_admitted_revision_or_publication(combined, field, when):
    f = combined
    f.heads[when] = {**f.heads[when], field: 'foreign'}
    with pytest.raises(vo.VoiceoverSyncError, match='admitted target|changed during synthesis'):
        invoke(f, timing_policy='ripple')
    assert not f.published and not list(f.request.out.iterdir())
    if when == 0:
        assert not f.speech_calls


@pytest.mark.parametrize('planned', [True, False])
def test_combined_advisory_results_settle_only_reports(combined, planned):
    f = combined
    if not planned:
        f.scripts['occurrences'][0]['text'] = 'Hello'
    result = invoke(f, plan_only=planned)
    assert result.payload['action_result']['report']['status'] == ('planned' if planned else 'unchanged')
    assert len(result.outputs) == 1 and result.outputs[0]['name'] == 'report'
    assert not f.speech_calls and not f.published
    assert not (f.request.out / 'authoring-proposal.json').exists()


def test_combined_media_refusal_cannot_settle_a_proposal(combined):
    f = combined
    f.media.output['selection'] = {'variant_id': 'foreign'}
    with pytest.raises(vo.VoiceoverSyncError, match='variant_id differs'):
        invoke(f, timing_policy='ripple')
    assert not f.published and not list(f.request.out.iterdir())


def test_old_authored_media_conflict_is_not_discarded(combined):
    f = combined
    shot = f.authored['shots'][f.authored['placements'][0]['shot_id']]
    shot['internal_timeline']['clips'][1]['object_id'] = 'sha256:' + 'f' * 64
    with pytest.raises(vo.VoiceoverSyncError, match='object_id differs'):
        invoke(f, timing_policy='ripple')
    assert not f.published and not list(f.request.out.iterdir())
