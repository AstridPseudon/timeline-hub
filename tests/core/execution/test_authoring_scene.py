"""Real private socket/session boundaries, synthetic native renderer I/O only.

No test result here is an actual Remotion frame or production COMMIT witness.
"""
import copy
import dataclasses
import json
import os
from pathlib import Path
import socket
import sys
import tempfile
import threading
from types import SimpleNamespace

import pytest

from astrid.core.execution import authoring_scene_protocol as wire
from astrid.core.execution import authoring_scene_transport as transport
from astrid.core.execution import authoring_scene_startup as startup
from astrid.core.execution.custody_broker import AuthenticatedCleanupActor
from astrid.core.execution.generic_host import GenericPackHost
from astrid.core.execution.remotion_frame_owner import FrameOwnerError
from astrid.core.execution.storage_preparation_transport import ProcessIdentity, read_frame
from test_remotion_host_session import environment, owner, fake_native, disposable_browser  # noqa: F401


def scene():
    return dict(timeline=dict(theme='banodoco-default', clips=[], tracks=[], theme_overrides={}),
                assets={'assets': {}}, fps=24, width=320, height=180, roles={})


def context():
    return {k: (1 if k == 'owner_generation' else 'astrid-v1' if k == 'provider_id'
                else 'sha256:' + 'a' * 64 if k.endswith('digest') or k == 'renderer_closure' else k)
            for k in wire.CONTEXT_FIELDS}


def request():
    projection = scene()
    invocation = {k: ('sha256:' + 'b' * 64 if k in {'request_hash', 'actor_session', 'candidate_digest'} else k)
                  for k in wire.INVOCATION_FIELDS}
    return dict(protocol=wire.PROTOCOL, operation=wire.OPERATION, purpose=wire.PURPOSE,
                context=context(), invocation=invocation, scene_digest=wire.digest(projection),
                scene=projection, dependencies={}, frames=[0, 1])


def answers(batch):
    return [dict(frame=f, layers=[], coverage='GAP', content=None, findings=[]) for f in batch]


def test_literal_closed_contract_roundtrip():
    value = request()
    assert wire.validate_request(value, context()) == {}
    response = wire.reply(value, answers(value['frames']))
    assert set(value) == wire.REQUEST_FIELDS and set(response) == wire.REPLY_FIELDS
    assert wire.validate_reply(response, value) == answers(value['frames'])


@pytest.mark.parametrize('key', sorted(wire.REPLY_FIELDS - {'evaluation'}))
def test_every_reply_binding_is_checked(key):
    value = request()
    response = wire.reply(value, answers(value['frames']))
    response[key] = None
    with pytest.raises(FrameOwnerError):
        wire.validate_reply(response, value)


@pytest.mark.parametrize('key', wire.CONTEXT_FIELDS)
def test_every_context_field_matches_trusted_startup(key):
    value = request()
    value['context'][key] = 2 if key == 'owner_generation' else 'foreign'
    with pytest.raises(FrameOwnerError):
        wire.validate_request(value, context())


@pytest.mark.parametrize('change', ['purpose', 'operation', 'unknown', 'candidate', 'frames', 'bool', 'oversize', 'path', 'url', 'dependencies'])
def test_bad_requests_refuse(change):
    value = request()
    if change in {'purpose', 'operation'}:
        value[change] = 'foreign'
    elif change == 'unknown': value['unknown'] = True
    elif change == 'candidate': value['scene']['fps'] = 30
    elif change == 'frames': value['frames'] = list(range(121))
    elif change == 'bool': value['frames'] = [True]
    elif change == 'oversize': value['scene']['oversize'] = 'a' * wire.LIMIT
    elif change in {'path', 'url'}:
        value['scene']['assets']['assets']['x'] = {change: '/escape' if change == 'path' else 'https://escape'}
        value['scene_digest'] = wire.digest(value['scene'])
    elif change == 'dependencies': value['dependencies'] = {'sha256:' + '0' * 64: {}}
    with pytest.raises(FrameOwnerError):
        wire.validate_request(value, context())


@pytest.mark.parametrize('change', ['unknown', 'incomplete', 'extra', 'nonfinite', 'frame'])
def test_bad_evaluation_refuses(change):
    value = answers([0])
    if change == 'unknown': value[0]['coverage'] = 'UNKNOWN'
    elif change == 'incomplete': value = []
    elif change == 'extra': value[0]['unexpected'] = 1
    elif change == 'nonfinite': value[0]['frame'] = float('nan')
    elif change == 'frame': value[0]['frame'] = True
    with pytest.raises(FrameOwnerError): wire.validate_evaluation(value, [0])


@pytest.fixture
def private_host(tmp_path, monkeypatch, disposable_browser, request):
    # Short canonical owner-only scratch avoids Darwin's Unix path bound.
    with tempfile.TemporaryDirectory(prefix='as106-', dir='/private/tmp') as temporary:
        support = Path(temporary)
        if getattr(request, 'param', False):
            support = support / ('long-selected-support-' + 'a' * 100)
            support.mkdir(mode=0o700)
        manager, _ = owner(tmp_path)
        env = environment(tmp_path)
        processes = fake_native(monkeypatch, manager)
        exchanges = []
        def exchange(req, **kwargs):
            if req['type'] == 'shutdown': return dict(ok=True, shutdown=True, exit=True)
            kwargs['guard']()
            assert req['type'] == 'evaluate'
            assert req['compositionId'] == 'AstridTrackEvaluation'
            props = json.loads(Path(req['propsPath']).read_bytes())
            assert Path(req['propsPath']).is_relative_to(support)
            exchanges.append(props)
            return dict(ok=True, evaluation=answers(req['frames']))
        monkeypatch.setattr(manager, '_exchange', exchange)
        identity = ProcessIdentity(**AuthenticatedCleanupActor.current().verify())
        config = transport.AuthoringSceneConfig(support, identity, identity, context(), 'a' * 64)
        host = SimpleNamespace(_shutdown=threading.Event(), _authoring_scene_lock=threading.Lock(),
            _authoring_scene_listener=None, _authoring_scene_session=lambda environment: manager)
        # Native peer/socket verification and HostRemotionSession/FrameOwner are
        # real. Admitted-source discovery is separately tested below.
        monkeypatch.setattr(startup, 'validate_host', lambda *args: None)
        listener = GenericPackHost.start_authoring_scene(host, config, env)
        config = listener.config
        relay = transport.AuthoringSceneRelay(config)
        try:
            yield SimpleNamespace(host=host, listener=listener, relay=relay, config=config,
                                  manager=manager, exchanges=exchanges, processes=processes)
        finally:
            listener.close()
            manager.close()


def test_native_private_transport_reuses_real_host_owner_boundary(private_host):
    w = private_host
    for _ in range(2):
        value = request()
        assert w.relay.exchange(value, guard=lambda: None, cancelled=threading.Event()) == answers([0, 1])
    assert len(w.exchanges) == 2 and len(w.processes) == 1
    assert not w.manager._leases
    assert not list(w.config.socket_path.parent.glob('scene-*'))


def test_private_host_refusal_diagnostic_does_not_reflect_exception_text(private_host, monkeypatch, capsys):
    w = private_host
    def failed(channel): raise ValueError('secret-credential /private/untrusted-path')
    monkeypatch.setattr(w.listener, '_handle', failed)
    with pytest.raises((EOFError, OSError, ValueError, FrameOwnerError)):
        w.relay.exchange(request(), guard=lambda: None, cancelled=threading.Event())
    captured = capsys.readouterr().err
    assert 'ValueError' in captured and 'test_authoring_scene.py' in captured
    assert 'secret-credential' not in captured and '/private/untrusted-path' not in captured


@pytest.mark.parametrize('alias', [False, True])
def test_scene_before_first_task_prepares_only_the_trusted_renderer_parent(tmp_path, monkeypatch, alias):
    from astrid.core.execution import remotion_host_session
    from astrid.core.execution.generic_host import HostError
    parent = tmp_path/'host-output/attempts'
    if alias:
        parent.parent.mkdir(); target = tmp_path/'outside'; target.mkdir(); parent.symlink_to(target)
    made = []
    def construct(**kwargs):
        assert parent.is_dir()
        made.append(kwargs)
        return SimpleNamespace()
    monkeypatch.setattr(remotion_host_session, 'HostRemotionSession', construct)
    host = SimpleNamespace(_renderer_setup_lock=threading.Lock(), _shutdown=threading.Event(),
        _cleanup_uncertain=False, _remotion_host_session=None, attempt_base=parent,
        pack_roots=(tmp_path/'admitted-packs',),
        _track_host_lifetime_process=lambda process: None, _untrack_host_lifetime_process=lambda process: None,
        _renderer_scratch_account=lambda root: None, _remotion_closure_binding=None,
        execution_policy=SimpleNamespace(evidence_budget=SimpleNamespace(release=lambda root: None)))
    if alias:
        with pytest.raises(HostError, match='attempt base changed'):
            GenericPackHost._authoring_scene_session(host, {})
        assert not made and list(target.iterdir()) == []
    else:
        owner = GenericPackHost._authoring_scene_session(host, {})
        assert owner is host._remotion_host_session
        assert made[0]['root_parent'] == str(parent)
        assert made[0]['pack_roots'] == host.pack_roots
        assert (parent.stat().st_mode & 0o777) == 0o700



@pytest.mark.parametrize('private_host', [True], indirect=True)
def test_long_selected_support_keeps_same_authenticated_scene_and_owned_cleanup(private_host):
    w = private_host
    assert len(os.fsencode(w.config.support_root / 'authoring-scene/s')) > 103
    assert len(os.fsencode(w.config.socket_path)) <= 103
    assert w.config.readiness_path.is_relative_to(w.config.support_root)
    assert json.loads(w.config.readiness_path.read_bytes()) == w.config.record
    assert w.relay.exchange(request(), guard=lambda: None, cancelled=threading.Event()) == answers([0, 1])
    compact = w.config.socket_root
    assert compact is not None
    changed = dict(w.config.record, socket_root=str(w.config.support_root))
    w.config.readiness_path.write_bytes(wire.encoded(changed) + b'\n')
    with pytest.raises(FrameOwnerError, match='endpoint_changed'):
        w.relay.check_live()
    assert len(w.exchanges) == 1
    w.listener.close()
    assert not compact.exists() and not w.config.readiness_path.exists()


@pytest.mark.parametrize('field', ['pid', 'uid', 'birth_id', 'audit_token_sha256', 'audit_token_pidversion'])
def test_wrong_native_peer_cannot_reach_owner(private_host, field):
    w = private_host
    old = w.config.runtime_peer
    foreign = dataclasses.replace(old, **{field: (getattr(old, field) + 1 if isinstance(getattr(old, field), int)
        else 'sha256:' + '0' * 64 if field == 'audit_token_sha256' else 'foreign')})
    w.listener.config = dataclasses.replace(w.config, runtime_peer=foreign)
    with pytest.raises((EOFError, OSError, ValueError, FrameOwnerError)):
        w.relay.exchange(request(), guard=lambda: None, cancelled=threading.Event())
    assert w.exchanges == []


@pytest.mark.parametrize('case', ['cancel', 'source', 'owner', 'shutdown', 'eof'])
def test_lifecycle_refuses_without_answers(private_host, monkeypatch, case):
    w = private_host
    cancelled = threading.Event()
    if case == 'cancel': cancelled.set()
    elif case == 'source':
        def changed(*args): raise FrameOwnerError('source_changed')
        monkeypatch.setattr(startup, 'validate_host', changed)
    elif case == 'owner': w.manager.frame_owner.generation += 1
    elif case == 'shutdown': w.host._shutdown.set()
    elif case == 'eof': w.listener.close()
    with pytest.raises((EOFError, OSError, ValueError, FrameOwnerError)):
        w.relay.exchange(request(), guard=lambda: None, cancelled=cancelled, timeout=1)
    assert not w.exchanges


def test_timeout_and_cancellation_are_polled_while_waiting(private_host, monkeypatch):
    w = private_host
    cancelled = threading.Event()
    original = w.listener._handle
    def held(channel):
        # Deliberately stalled transport fixture, no owner/frame claim.
        read_frame(channel, __import__('time').monotonic() + 1)
        cancelled.wait(.5)
    monkeypatch.setattr(w.listener, '_handle', held)
    with pytest.raises(FrameOwnerError, match='timeout'):
        w.relay.exchange(request(), guard=lambda: None, cancelled=cancelled, timeout=.05)
    monkeypatch.setattr(w.listener, '_handle', original)
    assert not w.exchanges


def test_framing_rejects_duplicates_nonfinite_extra_and_eof():
    for data in (b'{"x":1,"x":2}\n', b'{"x":NaN}\n', b'{}\n{}\n', b'{'):
        a, b = socket.socketpair()
        try:
            a.sendall(data); a.shutdown(socket.SHUT_WR)
            with pytest.raises((ValueError, EOFError)):
                read_frame(b, __import__('time').monotonic() + 1)
        finally:
            a.close(); b.close()


def test_only_verified_cas_dependencies_are_staged_in_host_scratch(private_host, monkeypatch):
    import base64
    import hashlib
    w = private_host
    data = b'explicit synthetic media, not an image frame'
    oid = 'sha256:' + hashlib.sha256(data).hexdigest()
    value = request()
    value['scene']['assets']['assets']['x'] = {'media_id': oid}
    value['dependencies'][oid] = dict(media_type='image/png', bytes=base64.b64encode(data).decode())
    value['scene_digest'] = wire.digest(value['scene'])
    w.relay.exchange(value, guard=lambda: None, cancelled=threading.Event())
    staged = w.exchanges[0]['scene']['assets']['assets']['x']['local_path']
    assert w.exchanges[0]['scene']['assets']['assets']['x']['file'] == staged
    assert w.exchanges[0]['scene']['assets']['assets']['x']['type'] == 'image'
    assert Path(staged).is_relative_to(w.config.socket_path.parent)
    assert not Path(staged).exists()  # request scratch released
    value['dependencies'][oid]['bytes'] = base64.b64encode(b'changed').decode()
    with pytest.raises(FrameOwnerError):
        w.relay.exchange(value, guard=lambda: None, cancelled=threading.Event())
    assert len(w.exchanges) == 1


@pytest.mark.parametrize('change', [None, 'provider', 'source', 'dependency', 'capability', 'epoch', 'boot', 'closure', 'generation', 'direct-boot', 'outside-boot'])
@pytest.mark.parametrize('mode', ['renderer', 'empty'])
def test_host_source_validation_at_real_method_boundary(tmp_path, monkeypatch, change, mode):
    from astrid.core.execution import generic_host as hosts
    c = context()
    c['provider_digest'] = startup.provider_digest()
    c['executor_source_digest'] = 'sha256:' + hosts._canonical_digest({'rendering.timeline_visualize': 'a' * 64})
    c['executor_dependency_digest'] = c['executor_source_digest']
    identity = ProcessIdentity(**AuthenticatedCleanupActor.current().verify())
    if mode == 'empty':
        c = {**{k: v for k, v in c.items() if k not in {'renderer_closure', 'owner_generation'}},
             'mode': wire.EMPTY_MODE}
    config = transport.AuthoringSceneConfig(tmp_path, identity, identity, c, 'a' * 64)
    record = SimpleNamespace(approval_reason=None, ready=True, matrix={}, source_digest='a' * 64,
        dependency_digest='a' * 64, capability_digest=c['capability_digest'], source_root=tmp_path,
        definition=SimpleNamespace(to_dict=lambda: {}))
    host = SimpleNamespace(_shutdown=threading.Event(), _cleanup_uncertain=False, executor_id=c['executor_id'],
        source_epoch=c['source_epoch'], boot_manifest_path=tmp_path / 'boot' / 'manifest.json',
        boot_manifest_hash=config.boot_manifest_hash,
        boot_manifest_provenance=lambda: dict(kind='astrid.boot_manifest', sha256=config.boot_manifest_hash),
        _registered_runtime_state={k: c[k] for k in ('runtime_instance_id', 'runtime_session_id', 'source_epoch')},
        capabilities={'rendering.timeline_visualize': record}, _remotion_host_session=SimpleNamespace(
            _closed=False, execution_invalidated=None, uncertain=None, frame_owner=SimpleNamespace(generation=1)))
    # Only the source inventory/renderer file observations are narrow fixtures.
    # The complete production source comparison and owner fence remain intact.
    monkeypatch.setattr(hosts, '_dependency_digest', lambda *a: 'a' * 64)
    monkeypatch.setattr(hosts, '_capability_digest', lambda *a: c['capability_digest'])
    monkeypatch.setattr(hosts, '_admitted_source_roots', lambda *a: [tmp_path])
    monkeypatch.setattr(hosts, '_verify_admitted_source', lambda *a: None)
    monkeypatch.setattr(startup, 'renderer_closure', lambda *a: 'sha256:' + 'a' * 64)
    if mode == 'empty':
        record.preflight = {}
        host._remotion_host_session = None
        host._remotion_closure_binding = None
    if change == 'direct-boot': host.boot_manifest_path=tmp_path/'boot-manifest.json'
    elif change == 'outside-boot': host.boot_manifest_path=tmp_path.parent/'foreign-manifest.json'
    if change == 'provider': c['provider_digest'] = 'sha256:' + '0' * 64
    elif change == 'source': record.source_digest = '0' * 64
    elif change == 'dependency': record.dependency_digest = '0' * 64
    elif change == 'capability': record.capability_digest = 'sha256:' + '0' * 64
    elif change == 'epoch': host.source_epoch = 'foreign'
    elif change == 'boot': host.boot_manifest_hash = '0' * 64
    elif change == 'closure':
        if mode == 'empty': host._remotion_closure_binding = object()
        else: monkeypatch.setattr(startup, 'renderer_closure', lambda *a: 'sha256:' + '0' * 64)
    elif change == 'generation':
        if mode == 'empty': host._remotion_host_session = object()
        else: host._remotion_host_session.frame_owner.generation += 1
    # Config snapshots mutable construction input.
    if change == 'provider': config = dataclasses.replace(config, binding=c)
    if change in (None, "direct-boot"): startup.validate_host(host, config, {})
    else:
        with pytest.raises(FrameOwnerError): startup.validate_host(host, config, {})


def test_owner_queue_honors_request_cancellation_before_admission(private_host):
    w = private_host
    held = w.manager.frame_owner._exchange
    held.acquire()
    try:
        with pytest.raises((FrameOwnerError, EOFError, OSError, ValueError)):
            w.relay.exchange(request(), guard=lambda: None, cancelled=threading.Event(), timeout=.05)
    finally:
        held.release()
    assert not w.exchanges


@pytest.mark.parametrize('key', wire.INVOCATION_FIELDS)
def test_reply_cannot_change_any_authenticated_invocation_field(key):
    value = request()
    response = wire.reply(value, answers(value['frames']))
    response['invocation'] = dict(response['invocation'], **{key: 'foreign'})
    with pytest.raises(FrameOwnerError): wire.validate_reply(response, value)


def test_oversized_reply_refuses_before_semantic_consumption():
    value = request()
    response = wire.reply(value, answers(value['frames']))
    response['evaluation'][0]['findings'] = ['x' * wire.LIMIT]
    with pytest.raises(FrameOwnerError, match='oversized'): wire.validate_reply(response, value)


@pytest.fixture
def selected_activation(tmp_path, monkeypatch):
    from astrid.core.execution import generic_host as hosts, hosted_contract, custody_broker
    identity = AuthenticatedCleanupActor.current().verify()
    c = context()
    support = tmp_path
    record = SimpleNamespace(source_digest='a' * 64, dependency_digest='a' * 64,
        capability_digest='sha256:' + 'a' * 64,
        preflight={'remotion': {'ok': True, 'project_dir': str(tmp_path), 'node_executable': '/fixture/node'}})
    state = dict(runtime_instance_id='runtime', runtime_session_id='session', coordinator_epoch='runtime', source_epoch='epoch')
    host = SimpleNamespace(_registered_runtime_state=state, boot_manifest_path=support / 'boot' / 'manifest.json',
        boot_manifest_hash='a' * 64, pack_roots=(tmp_path / 'packs',), source_epoch='epoch', executor_id='executor',
        capabilities={'rendering.timeline_visualize': record}, _renderer_setup_lock=threading.RLock(),
        _shutdown=threading.Event(), _cleanup_uncertain=False, _remotion_host_session=None,
        _track_host_lifetime_process=lambda p: None, _untrack_host_lifetime_process=lambda p: None,
        attempt_base=None, _renderer_scratch_account=lambda root: None,
        execution_policy=SimpleNamespace(evidence_budget=SimpleNamespace(release=lambda root: None)),
        _remotion_closure_binding=None)
    host._authoring_scene_session = lambda environment: GenericPackHost._authoring_scene_session(host, environment)
    launch = dict(pack_root=str(host.pack_roots[0]), boot_manifest_path=str(host.boot_manifest_path),
                  boot_manifest_hash=host.boot_manifest_hash, environment={})
    request = dict(operation_id='operation', channel_id='channel', owner_epoch='runtime', custody_scope=str(support),
        profile=dict(execution_mode='host_only_cpu', workspace_uuid='realm', support_root=str(support), host_launch=launch, host_executable=sys.executable),
        runtime_owner={**{k: identity[k] for k in ('pid', 'uid', 'birth_id')}, 'runtime_instance_id': 'runtime', 'coordinator_epoch': 'runtime'})
    broker = SimpleNamespace(role='host', owner_epoch='runtime', run_id='run', custody_generation=1,
                             authority_scope_root=support)
    hosted = hosted_contract.HostedLaunch(broker, request)
    hosted.environment([sys.executable, '-m', 'astrid.core.execution.generic_host', 'run',
        '--host-control-fd', str(hosted.children['control'].fileno()),
        '--activation-fd', str(hosted.children['activation'].fileno()),
        '--activation-operation-id', 'operation', '--activation-channel-id', 'channel'])
    class Authority:
        def __init__(self, scope, role): assert scope == support and role == 'host'
        def reference(self): return dict(generation=1, target={'pid': os.getpid()})
        def verify_reference(self, reference, *, expected_actor, owner_epoch):
            assert expected_actor == identity and owner_epoch == 'runtime'
    monkeypatch.setattr(custody_broker, 'RoleCustodyAuthority', Authority)
    monkeypatch.setattr(startup, 'validate_host', lambda *a: None)
    monkeypatch.setattr(startup, 'renderer_closure', lambda *a: 'sha256:' + 'a' * 64)
    preparation = SimpleNamespace(_claim_host=host, _request=request, _hosted_binding=hosted.value,
        _retained_relay_actor=AuthenticatedCleanupActor.current(), result={'status': 'prepared'}, _aborted=False,
        control_error=None, operation_id='operation', channel_id='channel',
        _activation_grant=dict(host={k: identity[k] for k in ('pid', 'birth_id')}, operation_id='operation',
            channel_id='channel', acceptance_mode=hosts._ACTIVATION_RECEIPT_MODE, executor_incarnation='incarnation'))
    try: yield preparation, host
    finally:
        hosted.close()
        if host._remotion_host_session is not None: host._remotion_host_session.close()


def test_trusted_activation_derives_identity_and_reuses_same_session(selected_activation, monkeypatch):
    preparation, host = selected_activation
    monkeypatch.setenv('ASTRID_AUTHORING_SCENE_SOCKET', '/foreign')
    config, environment = startup.configuration_from_activation(preparation)
    assert dataclasses.asdict(config.runtime_peer) == AuthenticatedCleanupActor.current().verify()
    assert config.binding['provider_digest'] == startup.provider_digest()
    first = host._remotion_host_session
    assert GenericPackHost._authoring_scene_session(host, environment) is first
    assert first.process is None  # configuration cannot manufacture a frame or spawn a renderer


@pytest.mark.parametrize('change', ['grant', 'owner', 'source', 'missing'])
@pytest.mark.parametrize('empty', [False, True])
def test_activation_refuses_unbound_startup(selected_activation, change, empty):
    preparation, host = selected_activation
    if empty: host.capabilities['rendering.timeline_visualize'].preflight = {}
    if change == 'grant': preparation._activation_grant['operation_id'] = 'foreign'
    elif change == 'owner': preparation._request['runtime_owner']['birth_id'] = 'foreign'
    elif change == 'source': host.pack_roots = (Path('/foreign'),)
    elif change == 'missing': preparation._activation_grant = None
    with pytest.raises((ValueError, FrameOwnerError)): startup.configuration_from_activation(preparation)


def layer():
    bounds = dict(status='known', rect=dict(x=0, y=0, width=320, height=180))
    return dict(clipId='clip', track='video', clipIndex=0, z=0, drawLocalFrame=0, ownFrame=0,
        transitionOpacity=1, opacity=1, visible=True, targetBounds=copy.deepcopy(bounds), bounds=bounds,
        role='picture', fullFrame=True, opaqueSupport='rect', coverage='covered', findings=[], dip=False)


def absent_layer():
    item = layer()
    unknown = dict(status='unknown', reason='Absent hold has no media geometry')
    item.update(visible=False, opacity=0, fullFrame=False, opaqueSupport='none', coverage='unknown',
                bounds=copy.deepcopy(unknown), targetBounds=copy.deepcopy(unknown))
    return item


@pytest.mark.parametrize('change', [None, 'visible', 'opacity', 'null-opacity', 'bool-opacity',
                                  'full-frame', 'dip', 'findings', 'coverage', 'reason',
                                  'extra-bounds', 'unknown-frame', 'opaque-rect', 'opaque-unknown'])
def test_only_zero_contributing_absent_layers_keep_unknown_geometry(change):
    value = answers([0])
    item = absent_layer()
    value[0]['layers'] = [item]
    if change == 'visible':
        item['visible'] = True
    elif change == 'opacity':
        item['opacity'] = .01
    elif change == 'null-opacity':
        item['opacity'] = None
    elif change == 'bool-opacity':
        item['opacity'] = False
    elif change == 'full-frame':
        item['fullFrame'] = True
    elif change == 'dip':
        item['dip'] = True
    elif change == 'findings':
        item['findings'] = [{'code': 'unknown-component-internals'}]
    elif change == 'coverage':
        item['coverage'] = 'partial'
    elif change == 'reason':
        item['bounds']['reason'] = None
    elif change == 'extra-bounds':
        item['bounds']['callback'] = 'untrusted'
    elif change == 'unknown-frame':
        value[0]['coverage'] = 'UNKNOWN'
    elif change == 'opaque-rect':
        item['opaqueSupport'] = 'rect'
    elif change == 'opaque-unknown':
        item['opaqueSupport'] = 'unknown'
    if change is None:
        assert wire.validate_evaluation(value, [0]) == value
        assert item['bounds']['status'] == 'unknown' and item['visible'] is False
    else:
        with pytest.raises(FrameOwnerError):
            wire.validate_evaluation(value, [0])


def test_absent_hold_roundtrip_preserves_unknown_bounds_without_claiming_pixels(private_host, monkeypatch):
    w = private_host
    original = w.manager._exchange
    expected = answers([0, 1])
    for value in expected:
        item = absent_layer()
        item.update(ownFrame=value['frame'], drawLocalFrame=value['frame'])
        value['layers'] = [item]
    def exchange(req, **kwargs):
        response = original(req, **kwargs)
        if req['type'] == 'evaluate':
            response['evaluation'] = copy.deepcopy(expected)
        return response
    monkeypatch.setattr(w.manager, '_exchange', exchange)
    assert w.relay.exchange(request(), guard=lambda: None, cancelled=threading.Event()) == expected
    assert len(w.processes) == 1 and not w.manager._leases


@pytest.mark.parametrize('support', ['none', 'unknown', True, None, {}, []])
def test_nonopaque_bounds_do_not_claim_opaque_picture_coverage(support):
    value = answers([0])
    item = layer()
    item['opaqueSupport'] = support
    value[0]['layers'] = [item]
    with pytest.raises(FrameOwnerError):
        wire.validate_evaluation(value, [0])
    if support == 'none':
        item['coverage'] = 'partial'
        assert wire.validate_evaluation(value, [0]) == value


@pytest.mark.parametrize('field', ['mediaEvidence', 'rendererIdentity', 'fontDigests'])
def test_caller_cannot_select_host_scene_capability_facts(field):
    value = request()
    value['scene'][field] = {'claimed': 'trusted'}
    value['scene_digest'] = wire.digest(value['scene'])
    with pytest.raises(FrameOwnerError):
        wire.validate_request(value, context())


def test_caller_registry_cannot_mint_media_evidence():
    value = request()
    value['scene']['assets']['assets']['media'] = {
        'media_id': 'sha256:' + 'a' * 64,
        'mediaEvidence': {'version': 1, 'opaqueSupport': 'rect'},
    }
    value['scene_digest'] = wire.digest(value['scene'])
    with pytest.raises(FrameOwnerError, match='asset_location_forbidden'):
        wire.validate_request(value, context())


def test_missing_opaque_support_does_not_receive_a_legacy_opaque_default():
    value = answers([0])
    item = layer()
    del item['opaqueSupport']
    value[0]['layers'] = [item]
    with pytest.raises(FrameOwnerError):
        wire.validate_evaluation(value, [0])


@pytest.mark.parametrize('change', [None, 'unknown', 'bounds', 'opacity', 'z', 'extra', 'visible', 'width'])
def test_strict_renderer_layer_shape(change):
    value = answers([0])
    item = layer()
    value[0]['layers'] = [item]
    if change == 'unknown': item['coverage'] = 'unknown'
    elif change == 'bounds': item['bounds'] = dict(status='unknown', reason='unavailable')
    elif change == 'opacity': item['opacity'] = True
    elif change == 'z': item['z'] = 'bad'
    elif change == 'extra': item['callback'] = 'bad'
    elif change == 'visible': item['visible'] = 'unknown'
    elif change == 'width': item['bounds']['rect']['width'] = -1
    if change is None: assert wire.validate_evaluation(value, [0]) == value
    else:
        with pytest.raises(FrameOwnerError): wire.validate_evaluation(value, [0])


@pytest.mark.parametrize('change', ['generation', 'source', 'cancel', 'late'])
def test_inflight_change_discards_delivered_result(private_host, monkeypatch, change):
    import time
    w = private_host
    cancelled = threading.Event()
    original = w.manager._exchange
    def delivered(request, **kwargs):
        result = original(request, **kwargs)
        if request['type'] == 'shutdown': return result
        if change == 'generation': w.manager.frame_owner.generation += 1
        elif change == 'source':
            def changed(*args): raise FrameOwnerError('source changed in flight')
            monkeypatch.setattr(startup, 'validate_host', changed)
        elif change == 'cancel': cancelled.set()
        elif change == 'late': time.sleep(.1)
        return result
    monkeypatch.setattr(w.manager, '_exchange', delivered)
    with pytest.raises((FrameOwnerError, EOFError, OSError, ValueError)):
        w.relay.exchange(request(), guard=lambda: None, cancelled=cancelled,
                         timeout=.05 if change == 'late' else 1)


@pytest.mark.parametrize("available", [True,False])
def test_static_visualization_requires_real_launch_readiness_for_authoring_scene(selected_activation,monkeypatch,available):
    from astrid.core.rendering import remotion_runtime
    preparation,host=selected_activation
    host.capabilities["rendering.timeline_visualize"].preflight={}
    host._remotion_closure_binding=object()  # Explicit fixture authority; no renderer executes.
    host._authoring_scene_session=lambda environment:SimpleNamespace(frame_owner=SimpleNamespace(generation=1))
    calls=[]
    def status(**kwargs):
        calls.append(kwargs)
        return SimpleNamespace(available=available,project_dir=Path("/qualified/project"),node_executable=Path("/qualified/node"))
    monkeypatch.setattr(remotion_runtime,"remotion_runtime_status",status)
    if available:
        _,environment=startup.configuration_from_activation(preparation)
        assert environment["ASTRID_REMOTION_PROJECT_DIR"]=="/qualified/project"
        assert environment["ASTRID_NODE_EXECUTABLE"]=="/qualified/node"
    else:
        with pytest.raises(FrameOwnerError,match="renderer_unavailable"):
            startup.configuration_from_activation(preparation)
    assert calls==[{"require_explicit_project":True}]


# Empty-only admission keeps the real private socket/peer transport. Source
# inventory is a narrow fixture; no native renderer process/session is created.
def empty_context():
    return {**{k: v for k, v in context().items()
               if k not in {"renderer_closure", "owner_generation"}}, "mode": wire.EMPTY_MODE}


def empty_candidate():
    from astrid.core.timeline.authoring_bundle import open_authoring_bundle
    from astrid.sdk.timeline.checkout import Checkout
    payload = dict(config={"tracks": [{"id": "V1", "kind": "visual", "opacity": .625}]},
                   clips=[], occurrences=[])
    return Checkout(open_authoring_bundle(
        dict(project_id="project_id", timeline_id="timeline_id", revision_id="empty-base",
             payload=payload, content_digest=wire.digest(payload)),
        shot_revisions=[], internal_timeline_revisions=[])).document()


def empty_request():
    value = request()
    candidate = empty_candidate()
    return dict(protocol=wire.PROTOCOL, operation=wire.EMPTY_OPERATION, purpose=wire.PURPOSE,
                context=empty_context(), invocation={**value["invocation"], "candidate_digest": wire.digest(candidate)},
                candidate=candidate)


@pytest.fixture
def private_empty_host(monkeypatch):
    with tempfile.TemporaryDirectory(prefix="as171-", dir="/private/tmp") as temporary:
        identity = ProcessIdentity(**AuthenticatedCleanupActor.current().verify())
        config = transport.AuthoringSceneConfig(Path(temporary), identity, identity, empty_context(), "a" * 64)
        def no_session(*args):
            pytest.fail("empty-only receiver acquired a renderer session")
        host = SimpleNamespace(_shutdown=threading.Event(), _authoring_scene_lock=threading.Lock(),
            _authoring_scene_listener=None, _authoring_scene_session=no_session)
        monkeypatch.setattr(startup, "validate_host", lambda *args: None)
        listener = GenericPackHost.start_authoring_scene(host, config, {})
        relay = transport.AuthoringSceneRelay(listener.config)
        try:
            yield SimpleNamespace(host=host, listener=listener, relay=relay)
        finally:
            relay.close()
            listener.close()


def test_empty_only_typed_completion_uses_real_transport_without_session(private_empty_host):
    value = empty_request()
    result = private_empty_host.relay.exchange(value, guard=lambda: None, cancelled=threading.Event())
    assert result == wire.empty_reply(value)
    assert wire.validate_empty_reply(result, value) == result
    assert "renderer_closure" not in result["context"] and "owner_generation" not in result["context"]


@pytest.mark.parametrize("field", sorted(wire.EMPTY_REPLY_FIELDS) + list(wire.INVOCATION_FIELDS))
def test_empty_completion_rejects_every_forged_reply_binding(field):
    value = empty_request()
    result = copy.deepcopy(wire.empty_reply(value))
    if field in wire.INVOCATION_FIELDS:
        result["invocation"][field] = "foreign"
    else:
        result[field] = None
    with pytest.raises(FrameOwnerError):
        wire.validate_empty_reply(result, value)


@pytest.mark.parametrize("change", ["frame", "mode", "renderer-mode", "candidate", "identity", "assert-empty"])
def test_empty_only_closed_request_refuses_wrong_mode_frame_and_candidate(change):
    value = empty_request()
    if change == "frame": value["frames"] = [0]
    elif change == "mode": value["context"]["mode"] = "anything"
    elif change == "renderer-mode": value["context"] = context()
    elif change == "candidate": value["candidate"]["parent"]["config"]["opacity"] = .75
    elif change == "identity":
        value["candidate"]["project_id"] = "foreign"
        value["invocation"]["candidate_digest"] = wire.digest(value["candidate"])
    elif change == "assert-empty": value["empty"] = True
    with pytest.raises(FrameOwnerError):
        wire.validate_request(value, empty_context())
    frame = request()
    frame["context"] = empty_context()
    with pytest.raises(FrameOwnerError): wire.validate_request(frame, empty_context())


@pytest.mark.parametrize("change", ["nonempty", "missing-shots", "malformed", "unsupported"])
def test_empty_host_verifies_complete_hydrated_candidate(private_empty_host, change):
    value = empty_request()
    if change == "nonempty":
        # Parent clips alone are empty, but the hydrated placements are not.
        from astrid.sdk.timeline.checkout import Checkout
        value["candidate"] = Checkout(json.loads((Path(__file__).parents[2] /
            "fixtures/timeline_editing/tiny_publishable.json").read_text())).document()
        value["candidate"].update(project_id="project_id", timeline_id="timeline_id")
    elif change == "missing-shots": del value["candidate"]["shots"]
    elif change == "malformed": value["candidate"]["placements"] = {"not": "a list"}
    elif change == "unsupported":
        value["candidate"]["parent"].setdefault("config", {}).setdefault("app", {})["astrid"] = {"v": 999}
    value["invocation"]["candidate_digest"] = wire.digest(value["candidate"])
    with pytest.raises((FrameOwnerError, EOFError, ValueError, OSError)):
        private_empty_host.relay.exchange(value, guard=lambda: None, cancelled=threading.Event())


def test_cpu_activation_derives_empty_mode_without_renderer_owner(selected_activation, monkeypatch):
    preparation, host = selected_activation
    host.capabilities["rendering.timeline_visualize"].preflight = {}
    host._authoring_scene_session = lambda *a: pytest.fail("empty activation acquired renderer")
    config, environment = startup.configuration_from_activation(preparation)
    assert wire.empty_only(config.binding)
    assert "owner_generation" not in config.binding and "renderer_closure" not in config.binding
    assert host._remotion_host_session is None
    assert not any(k.startswith("ASTRID_REMOTION") for k in environment)


@pytest.mark.parametrize("change", ["shutdown", "source", "endpoint", "relay", "cancel", "peer"])
def test_empty_completion_preserves_live_channel_guards(private_empty_host, monkeypatch, change):
    w = private_empty_host
    cancelled = threading.Event()
    if change == "shutdown": w.host._shutdown.set()
    elif change == "source":
        def invalid(*args): raise FrameOwnerError("source_changed")
        monkeypatch.setattr(startup, "validate_host", invalid)
    elif change == "endpoint": w.listener.config.readiness_path.unlink()
    elif change == "relay": w.relay.close()
    elif change == "cancel": cancelled.set()
    elif change == "peer":
        monkeypatch.setattr(transport, "_actor", lambda peer: SimpleNamespace(verify=lambda: {}))
    with pytest.raises((FrameOwnerError, EOFError, ValueError, OSError, KeyError)):
        w.relay.exchange(empty_request(), guard=lambda: None, cancelled=cancelled)


@pytest.mark.parametrize("change", ["profile", "selected", "preflight", "session"])
def test_empty_mode_cannot_upgrade_an_unready_or_selected_renderer(selected_activation, change):
    preparation, host = selected_activation
    host.capabilities["rendering.timeline_visualize"].preflight = {}
    if change == "profile": preparation._request["profile"]["execution_mode"] = "foreign"
    elif change == "selected": preparation._request["profile"]["host_launch"]["renderer_selection"] = {}
    elif change == "preflight": host.capabilities["rendering.timeline_visualize"].preflight = {"remotion": {"ok": False}}
    elif change == "session": host._remotion_host_session = SimpleNamespace(close=lambda: None)
    from astrid.core.execution.hosted_contract import HostedContractError
    expected = HostedContractError if change in {"profile", "selected"} else FrameOwnerError
    reason = "hosted preparation differs from authenticated launch" if change in {"profile", "selected"} else "renderer_unavailable"
    with pytest.raises(expected, match=reason):
        startup.configuration_from_activation(preparation)


@pytest.mark.parametrize("field", sorted(wire.EMPTY_CONTEXT_FIELDS))
def test_empty_request_preserves_every_trusted_context_field(field):
    value = empty_request()
    value["context"][field] = "foreign"
    with pytest.raises(FrameOwnerError): wire.validate_request(value, empty_context())
