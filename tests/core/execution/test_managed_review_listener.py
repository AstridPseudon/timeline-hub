"""Real review listener ownership and deny-bind confinement controls."""
import errno
import json
import os
import socket
import urllib.error
import urllib.request
from dataclasses import replace
from pathlib import Path

import pytest
import yaml

from astrid.core.execution import generic_host as host
from astrid.core.execution._review_listener import _InheritedReviewListener, _RetainedReviewListener
from tests.core.execution.test_generic_host_actions_v3 import FakeRuntime, _host_child_bridge


def world(tmp_path, *, code=None):
    if code is None:
        root = Path(__file__).resolve().parents[3] / 'astrid/packs/editorial'
    else:
        root = tmp_path / 'editorial'
        root.mkdir()
        (root / 'source.py').write_text(code)
        declaration = {
            'description': 'Synthetic review transport negative probe.',
            'inputs': [{'name': 'port', 'type': 'integer', 'default': 0, 'required': False}],
            'outputs': [{'name': 'probe', 'type': 'file', 'path_template': '{out}/probe.json'}],
            'isolation': {'mode': 'subprocess', 'network': False},
            'invocation': {'kind': 'command', 'command': {'argv': ['{python_exec}', str(root / 'source.py'), '{probe}']}},
        }
        (root / 'pack.yaml').write_text(yaml.safe_dump({'schema_version': 3, 'id': 'editorial',
            'name': 'Synthetic', 'version': '1.0.0', 'actions': {'human_review': declaration}}))
    h = host.GenericPackHost(pack_roots=[root], client=FakeRuntime())
    h.discover()
    _, admission = h.admit(capability_kind='executor', capability_id='editorial.human_review')
    record = h.capabilities['editorial.human_review']
    attempt = tmp_path.resolve() / 'attempt'
    (attempt / 'outputs').mkdir(parents=True)
    (attempt / 'inputs').mkdir()
    bridge = _host_child_bridge(h, h.client, attempt, record, task_id='review-listener')
    return h, record, admission, attempt, bridge


def resource(tmp_path):
    h, record, admission, attempt, bridge = world(tmp_path, code="print('synthetic')")
    launch = bridge.launch_binding()
    listener = _RetainedReviewListener(launch, h._confinement_policy, record, 0)
    launch.review_listener = listener
    policy = replace(h._confinement_policy, review_listener=listener, pass_fds=launch.descriptors)
    return h, record, attempt, bridge, launch, listener, policy


@pytest.mark.parametrize('fault', ['closed', 'rebound', 'foreign', 'claim', 'source', 'capability',
                                   'source_bytes', 'attempt', 'replay', 'fork'])
def test_retained_listener_rejects_resource_or_owner_drift(tmp_path, fault):
    h, record, attempt, bridge, launch, listener, policy = resource(tmp_path)
    other = None
    try:
        listener.validate(policy)
        if fault == 'closed':
            listener.socket.close()
        elif fault in ('rebound', 'foreign'):
            if fault == 'rebound':
                listener.socket.close()
            other = socket.socket()
            other.bind(('127.0.0.1', 0))
            other.listen(1)
            if fault == 'foreign':
                launch.review_listener = object()
            else:
                listener.socket = other
        elif fault == 'claim':
            h._attempt_claim_authority = host._AuthenticatedAttempt(tuple(sorted({**launch.claim, 'fence': 2}.items())))
        elif fault == 'source':
            h.capabilities[record.id] = replace(record, source_digest='changed')
        elif fault == 'capability':
            h.capabilities[record.id] = replace(record, capability_digest='changed')
        elif fault == 'source_bytes':
            (record.source_root / 'source.py').write_text('changed source')
        elif fault == 'attempt':
            policy = replace(policy, attempt_root=attempt.parent)
        elif fault == 'replay':
            listener.consume()
            with pytest.raises(ValueError, match='replayed'):
                listener.consume()
            return
        else:
            child = os.fork()
            if child == 0:
                result = 2
                try:
                    listener.validate(policy)
                    result = 1
                except ValueError:
                    result = 0
                finally:
                    os._exit(result)
            _, status = os.waitpid(child, 0)
            assert os.waitstatus_to_exitcode(status) == 0
            listener.validate(policy)
            return
        with pytest.raises((ValueError, OSError, host.HostError)):
            listener.validate(policy)
        assert not h._active_processes
        assert not (attempt / 'outputs' / host._REVIEW_SESSION_NAME).exists()
    finally:
        listener.close()
        if other is not None:
            other.close()
        bridge.revoke()


def test_inherited_listener_cannot_use_foreign_socket_or_replay(tmp_path):
    _, _, attempt, bridge, _, listener, _ = resource(tmp_path)
    try:
        metadata = listener.metadata()
        channel = listener.socket.dup()
        inherited = _InheritedReviewListener(channel, metadata)
        assert inherited.consume(attempt / 'outputs' / 'result.json') is channel
        with pytest.raises(ValueError, match='consumer'):
            inherited.consume(attempt / 'outputs' / 'result.json')
        inherited.close()
        other = socket.socket()
        try:
            other.bind(('127.0.0.1', 0))
            other.listen(1)
            with pytest.raises(ValueError, match='authenticated launch'):
                _InheritedReviewListener(other, metadata)
        finally:
            other.close()
    finally:
        listener.close()
        bridge.revoke()


PROBE = r'''
import errno,json,os,socket,stat,sys
from pathlib import Path
from astrid.sdk import _child_bridge
bridge=_child_bridge._bridge
listener=bridge._take_review_listener(Path(sys.argv[1]))
port=listener.getsockname()[1]
result={'stdin_is_null':stat.S_ISCHR(os.fstat(0).st_mode) and os.read(0,1)==b''}
for name,address in [('wildcard',('0.0.0.0',port)),('other_port',('127.0.0.1',0)),('external',('192.0.2.1',0))]:
    s=socket.socket()
    try:
        s.bind(address)
        result[name]=0
    except OSError as exc:
        result[name]=exc.errno
    finally:s.close()
s=socket.socket();s.settimeout(.2)
try:result['outbound']=s.connect_ex(('127.0.0.1',port))
finally:s.close()
try:
    bridge._take_review_listener(Path(sys.argv[1]))
    result['replay']=False
except ValueError:result['replay']=True
Path(sys.argv[1]).write_text(json.dumps(result))
'''


def test_actual_review_sandbox_denies_bind_and_outbound(tmp_path):
    h, record, admission, attempt, bridge = world(tmp_path, code=PROBE)
    try:
        h._run_command_definition(record, {}, attempt / 'outputs', attempt,
                                  cancelled=lambda: False, admission=admission, child_bridge=bridge)
        result = json.loads((attempt / 'outputs/probe.json').read_text())
        assert result == {**{name: errno.EPERM for name in ('wildcard', 'other_port', 'external', 'outbound')}, 'replay': True, 'stdin_is_null': True}
        listener = bridge._launch_binding.review_listener
        assert listener.closed and listener.socket.fileno() == -1
        assert not h._active_processes and not h._cleanup_uncertain
    finally:
        bridge.revoke()


@pytest.mark.parametrize('explicit_port', [False, True])
def test_actual_review_submit_validates_token_schema_and_closes_original_owner(tmp_path, explicit_port):
    h, record, admission, attempt, bridge = world(tmp_path)
    inputs = attempt / 'inputs'
    (inputs / 'page.html').write_text('<html>review</html>')
    (inputs / 'data.json').write_text('{}')
    (inputs / 'schema.json').write_text(json.dumps({'type': 'object', 'required': ['decision'],
        'properties': {'decision': {'const': 'approve'}}, 'additionalProperties': False}))
    port = 0
    if explicit_port:
        requested = socket.socket()
        requested.bind(('127.0.0.1', 0))
        port = requested.getsockname()[1]
        requested.close()
    observed = []
    descriptor = attempt / 'outputs' / host._REVIEW_SESSION_NAME

    def submit():
        if not descriptor.exists() or observed:
            return False
        url = json.loads(descriptor.read_text())['receiver_url']
        observed.append(url)
        base, token = url.split('?token=')
        with urllib.request.urlopen(url, timeout=2) as response:
            assert response.status == 200
        for suffix, data, status in [('/submit?token=wrong', {'decision': 'approve'}, 403),
                                      ('/submit?token=' + token, {}, 400)]:
            request = urllib.request.Request(base.rstrip('/') + suffix, data=json.dumps(data).encode(),
                                             headers={'Content-Type': 'application/json'})
            with pytest.raises(urllib.error.HTTPError) as error:
                urllib.request.urlopen(request, timeout=2)
            assert error.value.code == status
            assert not (attempt / 'outputs/human_review.final.json').exists()
        request = urllib.request.Request(base.rstrip('/') + '/submit?token=' + token,
            data=b'{"decision":"approve"}', headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(request, timeout=2) as response:
            assert response.status == 204
        return False

    try:
        result = h._run_command_definition(record, {'html': str(inputs / 'page.html'),
            'data': str(inputs / 'data.json'), 'response_schema': str(inputs / 'schema.json'),
            'no_open': True, 'timeout': 10, 'port': port}, attempt / 'outputs', attempt,
            cancelled=submit, admission=admission, child_bridge=bridge)
        assert result.returncode == 0 and len(observed) == 1
        assert json.loads((attempt / 'outputs/human_review.final.json').read_text()) == {'decision': 'approve'}
        listener = bridge._launch_binding.review_listener
        assert listener.closed and listener.socket.fileno() == -1
        if explicit_port:
            assert listener.identity['port'] == port
        assert not descriptor.exists() and not h._active_processes and not h._cleanup_uncertain
        with pytest.raises((urllib.error.URLError, ConnectionError, TimeoutError)):
            urllib.request.urlopen(observed[0], timeout=1)
    finally:
        bridge.revoke()


@pytest.mark.parametrize('port', [-1, 65536, True, '1234'])
def test_invalid_listener_request_refuses_without_spawn(tmp_path, port):
    h, record, _, _, bridge = world(tmp_path, code="print('synthetic')")
    launch = bridge.launch_binding()
    try:
        with pytest.raises(ValueError):
            _RetainedReviewListener(launch, h._confinement_policy, record, port)
        assert not h._active_processes and launch.custody is None
    finally:
        bridge.revoke()


def test_occupied_listener_request_preserves_original_service_without_fallback(tmp_path):
    h, record, _, _, bridge = world(tmp_path, code="print('synthetic')")
    launch = bridge.launch_binding()
    occupied = socket.socket()
    occupied.bind(('127.0.0.1', 0))
    occupied.listen(1)
    address = occupied.getsockname()
    try:
        with pytest.raises(OSError):
            _RetainedReviewListener(launch, h._confinement_policy, record, address[1])
        assert occupied.getsockname() == address
        assert not h._active_processes and launch.custody is None
    finally:
        occupied.close()
        bridge.revoke()


def test_untyped_listener_cannot_replace_strict_child_stdin(tmp_path):
    _, _, _, bridge, launch, listener, _ = resource(tmp_path)
    try:
        launch.review_listener = object()
        with pytest.raises(ValueError, match='typed review listener'):
            launch.verify()
    finally:
        listener.close()
        bridge.revoke()


def test_review_listener_cannot_add_outbound_authority(tmp_path):
    _, _, _, bridge, _, listener, policy = resource(tmp_path)
    try:
        widened = replace(policy, network=host._SandboxNetworkPolicy((host._SandboxTcpEndpoint('127.0.0.1', 12345),)))
        with pytest.raises(ValueError, match='changed'):
            listener.validate(widened)
    finally:
        listener.close()
        bridge.revoke()


def test_managed_review_missing_listener_never_falls_back_to_bind(tmp_path, monkeypatch):
    from tests.test_human_review_server import _receiver_bridge
    review, bridge, parent, attempt = _receiver_bridge(monkeypatch, tmp_path, transport='pipe')
    bridge._review_listener.close()
    bridge._review_listener = None
    (attempt / 'page.html').write_text('<html>review</html>')
    (attempt / 'data.json').write_text('{}')
    monkeypatch.setattr(review, '_pick_free_port', lambda: pytest.fail('managed fallback bind'))
    try:
        with pytest.raises(ValueError, match='inherited listener'):
            review.main(['--html', str(attempt / 'page.html'), '--data', str(attempt / 'data.json'),
                         '--out', str(attempt / 'outputs/result.json'), '--no-open'])
        assert not (attempt / 'outputs' / review._RECEIVER_SESSION_NAME).exists()
    finally:
        bridge.close()
        parent.close()


def test_foreign_duplicate_fd_cannot_replace_exact_retained_stdin(tmp_path):
    import subprocess
    _, _, attempt, bridge, launch, listener, _ = resource(tmp_path)
    duplicate = listener.socket.dup()
    try:
        listener.consume()
        launch.select(('/synthetic',), str(attempt / 'outputs'), (), launch.descriptors)
        options = {'cwd': str(attempt / 'outputs'), 'env': {}, 'close_fds': True,
                   'stdin': duplicate, 'stdout': subprocess.PIPE, 'stderr': subprocess.PIPE}
        with pytest.raises(ValueError, match='differs from admitted'):
            launch.verify_launch(['/synthetic'], options, new_session=True)
        assert duplicate.fileno() >= 0 and launch.custody is None
    finally:
        duplicate.close()
        listener.close()
        bridge.revoke()


def test_review_observation_cannot_redirect_to_another_loopback_port(tmp_path):
    from types import SimpleNamespace
    h, _, attempt, bridge, _, listener, _ = resource(tmp_path)
    path = attempt / 'outputs' / host._REVIEW_SESSION_NAME
    port = listener.identity['port'] % 65535 + 1
    row = {'schema': 'astrid.human-review-session/v1', 'process_pid': os.getpid(),
           'process_birth_id': host.process_birth_identity(),
           'receiver_url': f'http://127.0.0.1:{port}/?token=' + 'a' * 32}
    path.write_text(json.dumps(row))
    path.chmod(0o600)
    before = path.read_bytes()
    original = SimpleNamespace(pid=os.getpid(), _astrid_process_birth=row['process_birth_id'])
    try:
        with pytest.raises(host.HostError, match='original child'):
            host._observe_owned_review_session(original, attempt, expected_listener=listener)
        assert path.read_bytes() == before and not h._active_processes
    finally:
        listener.close()
        bridge.revoke()
