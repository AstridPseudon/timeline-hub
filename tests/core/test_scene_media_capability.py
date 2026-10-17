"""Producer/provenance unit proof. Mocked ffprobe output is not decoded-media proof."""
import copy
import hashlib
import json
import subprocess

import pytest

from astrid.core import media
from astrid.core.timeline.scene_answers import _payload
from tests.core.util.test_util_media import HAPPY_FFPROBE_JSON


@pytest.fixture
def selected(tmp_path, monkeypatch):
    path = tmp_path / 'content-with-no-extension'
    path.write_bytes(b'unit-owned-media-object')
    oid = 'sha256:' + hashlib.sha256(path.read_bytes()).hexdigest()
    payload = json.loads(HAPPY_FFPROBE_JSON)
    payload['streams'][0]['index'] = 0
    payload['streams'][0]['sample_aspect_ratio'] = '1:1'
    calls = []
    def runner(cmd, **kwargs):
        calls.append(cmd)
        return subprocess.CompletedProcess(cmd, 0, stdout=json.dumps(payload), stderr='')
    monkeypatch.setattr(media.subprocess, 'run', runner)
    monkeypatch.setattr(media.shutil, 'which', lambda tool: '/qualified/ffprobe')
    return path, oid, payload, calls


def test_digest_and_actual_selected_stream_are_projected(selected):
    path, oid, payload, calls = selected
    proof = media.scene_media_evidence(path, oid)
    assert proof == {
        'version': 1, 'objectId': oid, 'contentSha256': oid[7:], 'file': str(path),
        'interpretation': media.SCENE_VIDEO_INTERPRETATION,
        'stream': {'index': 0, 'codec': 'h264', 'pixelFormat': 'yuv420p', 'profile':'High', 'level':'41', 'sampleAspectRatio':'1:1', 'width': 1920, 'height': 1080}}
    assert '-show_streams' in calls[0]
    assert '-show_format' in calls[0]


@pytest.mark.parametrize('change', ['digest','stale','alpha','alpha-tag','multi','attached','codec','index','dimensions','interpretation','sar','rotation','profile','level'])
def test_uncertain_or_changed_bindings_never_produce_opaque_fact(selected, change):
    path, oid, payload, calls = selected
    stream = payload['streams'][0]
    interpretation = media.SCENE_VIDEO_INTERPRETATION
    if change == 'digest': oid = 'sha256:' + '0' * 64
    if change == 'stale': path.write_bytes(b'changed')
    if change == 'alpha': stream['pix_fmt'] = 'yuva420p'
    if change == 'alpha-tag': stream['tags'] = {'alpha_mode': '1'}
    if change == 'multi': payload['streams'].append(copy.deepcopy(stream))
    if change == 'attached': stream['disposition']['attached_pic'] = 1
    if change == 'codec': stream['codec_name'] = 'vp9'
    if change == 'index': del stream['index']
    if change == 'dimensions': del stream['width']
    if change == 'sar': stream['sample_aspect_ratio'] = '4:3'
    if change == 'rotation': stream['tags'] = {'rotate':'90'}
    if change == 'profile': stream['profile'] = 'High 4:4:4 Predictive'
    if change == 'level': stream['level'] = 99
    if change == 'interpretation': interpretation = 'different-decoder'
    assert media.scene_media_evidence(path, oid, interpretation=interpretation) is None


def test_change_during_probe_is_unknown(selected, monkeypatch):
    path, oid, payload, calls = selected
    probe = media.ffprobe_metadata_strict(path)
    def changing(file):
        path.write_bytes(b'changed-during-probe')
        return probe
    monkeypatch.setattr(media, 'ffprobe_metadata_strict', changing)
    assert media.scene_media_evidence(path, oid) is None


def test_authored_evidence_is_not_promoted_to_host_inputs():
    config = {'clips': [{'id':'v','track':'v','asset':'a','clipType':'media','at':0,'hold':1,
                         'elementRef':{'id':'am-type','kind':'effect','packId':'astrid_motion'},
                         'sceneCapability': {'opaqueSupport':'rect'}}],
              'mediaEvidence': {'a': {'alpha':False}},
              'assets': {'assets': {'a': {'file':'forged.mp4','type':'video/mp4',
                         'sceneCapability': {'alpha':False}}}}}
    payload = _payload(config, 30, {'width':1920,'height':1080}, {})
    assert 'mediaEvidence' not in payload
    assert 'sceneCapability' not in payload['timeline']['clips'][0]
    # Registry-authored values may survive for display, but the evaluator only
    # reads the separately Host-admitted media map, never these fields.

def test_selected_component_owner_is_a_cache_relevant_projection():
    config = {'clips':[{'id':'caption','track':'label','clipType':'am-type','at':0,'hold':1,
                       'params':{'text':'Caption'},'elementRef':{'id':'am-type','kind':'effect','packId':'astrid_motion'}}]}
    projected = _payload(config,30,{'width':1920,'height':1080},{})
    assert projected['timeline']['clips'][0]['elementRef'] == config['clips'][0]['elementRef']
