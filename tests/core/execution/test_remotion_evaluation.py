"""Python cache/protocol checks only; injected replies are not renderer proof."""
import json
from pathlib import Path
import sys

import pytest

from astrid.core.execution import remotion_evaluation as evaluation
from astrid.core.execution.remotion_frame_owner import FrameOwnerError


def query_client(tmp_path, monkeypatch, *, response=None):
    calls = []
    current = ['closure-component-package-font-a']
    class Transport:
        def request(self, identity, request, parser):
            props = json.loads(Path(request['propsPath']).read_bytes())
            assert request['type'] == 'evaluate'
            assert request['compositionId'] == 'AstridTrackEvaluation'
            assert props['frames'] == request['frames']
            calls.append((identity, props))
            return response if response is not None else {'ok': True, 'evaluation': [
                {'frame': frame, 'layers': []} for frame in props['frames']]}
    monkeypatch.setattr(evaluation, 'host_remotion_client', lambda: Transport())
    client = evaluation.RemotionEvaluationClient(project_dir=tmp_path, attempt_root=tmp_path,
        node_executable=sys.executable, renderer_closure=lambda: current[0])
    return client, calls, current


def ask(client, **overrides):
    return client.query_track(**{'revision_digest': 'resolved-relevant-revision',
        'spans': [{'start': 0, 'duration': 4}], 'transitions': [], 'frames': [0, 3, 4], **overrides})


def test_repeat_returns_copied_answer_and_new_identity_or_inputs_recompute(tmp_path, monkeypatch):
    client, calls, current = query_client(tmp_path, monkeypatch)
    first = ask(client)
    first[0]['layers'].append({'caller-mutation': True})
    assert ask(client)[0]['layers'] == []
    assert len(calls) == 1
    for label in ('component-change', 'package-change', 'font-change'):
        current[0] = label
        ask(client)
    assert len(calls) == 4
    ask(client, revision_digest='changed-relevant-revision')
    ask(client, spans=[{'start': 0, 'duration': 5}])
    assert len(calls) == 6
    assert not list(tmp_path.glob('evaluation-*'))


def test_owner_unavailable_fails_and_never_creates_legacy_owner(tmp_path, monkeypatch):
    client, _, _ = query_client(tmp_path, monkeypatch)
    monkeypatch.setattr(evaluation, 'host_remotion_client', lambda: None)
    with pytest.raises(FrameOwnerError, match='frame_owner_unavailable'):
        ask(client)
    assert not list(tmp_path.glob('evaluation-*'))


@pytest.mark.parametrize('response', [
    {'ok': False, 'error': 'owned-renderer-failure'},
    {'ok': True, 'evaluation': []},
    {'ok': True, 'evaluation': [{'frame': True, 'layers': []}]},
])
def test_failure_or_wrong_frames_are_never_cached(tmp_path, monkeypatch, response):
    client, calls, _ = query_client(tmp_path, monkeypatch, response=response)
    for _ in range(2):
        with pytest.raises(FrameOwnerError): ask(client)
    assert len(calls) == 2 and not client._cache
    assert not list(tmp_path.glob('evaluation-*'))


def test_closure_change_during_delivery_refuses_result(tmp_path, monkeypatch):
    client, _, _ = query_client(tmp_path, monkeypatch)
    identities = iter(['before', 'after'])
    client.closure = lambda: next(identities)
    with pytest.raises(FrameOwnerError, match='renderer_closure_changed_during_query'):
        ask(client)
    assert not client._cache


def test_query_count_budget_fails_before_transport(tmp_path, monkeypatch):
    client, calls, _ = query_client(tmp_path, monkeypatch)
    for frames in ([], list(range(121)), [True], [2**53]):
        with pytest.raises(FrameOwnerError, match='evaluation_inputs_invalid'):
            ask(client, frames=frames)
    assert calls == []
