"""WP1 contract checks on disposable paths; no product launch or network proof."""

from dataclasses import FrozenInstanceError, replace
import os
from pathlib import Path
import subprocess

import pytest

from astrid.core.execution import generic_host as host


@pytest.fixture
def config(tmp_path, monkeypatch):
    attempt = tmp_path / "attempt"
    private = attempt / "private"
    project = attempt / "selected-project"
    for path in (private, project / "read-only", project / "editable"):
        path.mkdir(parents=True, mode=0o700)
    boot = tmp_path / "bootstrap"
    boot.mkdir()
    executable = boot / "interpreter"
    executable.write_text("synthetic executable fixture\n")
    os.chmod(executable, 0o700)
    library = tmp_path / "library"
    library.mkdir()
    monkeypatch.setattr(host.sys, "platform", "darwin")
    monkeypatch.setattr(host.shutil, "which", lambda _: "/usr/bin/sandbox-exec")
    return host._ConfinementPolicy(
        attempt, private,
        host._SandboxProjectScope(project, (project,), (project / "editable",)),
        (executable,), (library,), host._SandboxEnvironmentPolicy(),
    )


def plan(config, **kwargs):
    return host._confined_launch_plan([str(config.bootstrap_files[0]), "fixture"], policy=config, **kwargs)


@pytest.mark.parametrize('changed',['executable','library','alias'])
def test_selected_action_media_executable_and_library_pins_refuse_replacement(config,tmp_path,changed):
    from astrid.core.execution.declared_executables import FilePin,ExecutableBinding
    executable=tmp_path/'ffmpeg';executable.write_bytes(b'offline executable fixture');executable.chmod(0o700)
    library=tmp_path/'codec.dylib';library.write_bytes(b'offline library fixture')
    binding=ExecutableBinding('ffmpeg',FilePin.measure(executable),(FilePin.measure(library),),(),tuple(os.uname()))
    directory=config.attempt_root/'.astrid-executables';directory.mkdir(mode=0o700)
    (directory/'ffmpeg').symlink_to(executable)
    policy=replace(config,executable_bindings=(binding,),executable_directory=directory)
    assert plan(policy)
    if changed=='executable':executable.write_bytes(b'substitute executable')
    elif changed=='library':library.write_bytes(b'substitute library')
    else:
        (directory/'ffmpeg').unlink();(directory/'ffmpeg').symlink_to(library)
    with pytest.raises(host.HostError):plan(policy)


@pytest.mark.parametrize('argument',['https://host.invalid/audio','http://host.invalid/audio',
    'tcp:127.0.0.1:443','udp:127.0.0.1:443','rtsp://host.invalid/audio','concat:https://host.invalid/a'])
def test_selected_action_local_media_cannot_carry_urls(argument):
    from astrid.core.execution.network_policy import _local_media_tool
    for tool in ('ffmpeg','ffprobe'):
        assert _local_media_tool([tool,'-i',argument,'local.wav']) is False
        assert _local_media_tool([tool,'-i','input.mp3','output.wav']) is True
    assert _local_media_tool(['edge-tts','--text','offline']) is False


def test_selected_action_broker_policy_has_no_direct_upstream_egress(monkeypatch):
    from astrid.core.execution import network_policy
    monkeypatch.setattr(network_policy,'_POLICY',{'allowed_destinations':['http://127.0.0.1:43210']})
    assert network_policy._allowed_destination('127.0.0.1',43210)
    assert not network_policy._allowed_destination('127.0.0.1',43211)
    assert not network_policy._allowed_destination('api.msedgeservices.com',443)
    assert not network_policy._allowed_destination('speech.platform.bing.com',443)


def test_selected_action_retained_profile_is_small_argv_and_rechecks_bytes(config):
    retained=plan(replace(config,retained_profile=True))
    assert retained.argv[:2]==('/usr/bin/sandbox-exec','-f')
    path=Path(retained.argv[2])
    assert not path.is_relative_to(config.private_write_root)
    assert all(not path.is_relative_to(root) for root in config.project.write_roots)
    assert '(deny default)' in path.read_text()
    retained.subprocess_options()
    path.chmod(0o600);path.write_text('(allow default)\n');path.chmod(0o400)
    with pytest.raises(ValueError):retained.subprocess_options()
    (config.attempt_root.parent.parent/'retained-profile-file-refusal.json').write_text(
        '{"changed_profile_refused":true,"native_execution":false}\n')


def test_valid_plan_separates_project_bootstrap_private_and_subprocess_authority(config):
    result = plan(config)
    profile = result.argv[2]
    assert result.argv[:2] == ("/usr/bin/sandbox-exec", "-p")
    assert result.argv[3:] == (str(config.bootstrap_files[0]), "fixture")
    assert '(deny default)' in profile
    assert f'(allow file-read* (subpath "{config.project.project_root}"))' in profile
    assert f'(allow file-write* (subpath "{config.project.write_roots[0]}"))' in profile
    assert f'(allow file-write* (subpath "{config.private_write_root}"))' in profile
    assert f'(allow file-map-executable (literal "{config.bootstrap_files[0]}"))' in profile
    assert f'(allow file-map-executable (subpath "{config.bootstrap_roots[0]}"))' in profile
    assert f'(allow file-write* (subpath "{config.project.project_root}"))' not in profile
    assert '(allow file-read*)' not in profile
    assert 'network' not in profile
    assert '(allow file-write* (literal "/dev/null"))' not in profile
    for ambient in (config.attempt_root, config.attempt_root.parent, Path('/tmp'), Path('/private/tmp')):
        assert f'(subpath "{ambient}")' not in profile
    options = result.subprocess_options()
    assert options == {
        'cwd': str(config.private_write_root), 'env': dict(result.environment),
        'close_fds': True, 'pass_fds': (), 'stdin': subprocess.PIPE,
        'stdout': subprocess.PIPE, 'stderr': subprocess.PIPE,
    }
    options['env']['HOME'] = 'request-change'
    assert dict(result.environment)['HOME'] == str(config.private_write_root)
    with pytest.raises(FrozenInstanceError):
        result.pass_fds = (12,)
    with pytest.raises(FrozenInstanceError):
        config.private_write_root = Path('/')


@pytest.mark.parametrize('policy', [None, {}, 'caller claims confinement', False])
def test_absent_or_untyped_policy_is_denied_without_broker(policy):
    with pytest.raises(host.HostError, match='policy is missing or invalid'):
        host._confined_launch_plan(['/fixture'], policy=policy)


def test_omitted_policy_is_denied():
    with pytest.raises(host.HostError, match='policy is missing or invalid'):
        host._confined_launch_plan(['/fixture'])


@pytest.mark.parametrize('change', [
    {'project': {}}, {'environment': {}}, {'network': {}}, {'pass_fds': [9]},
    {'bootstrap_files': []}, {'bootstrap_roots': []},
    {'attempt_root': Path('relative')}, {'private_write_root': Path('/')},
])
def test_malformed_policy_denied(config, change):
    with pytest.raises(host.HostError):
        host._confined_launch_plan([str(config.bootstrap_files[0])], policy=replace(config, **change))


@pytest.mark.parametrize('platform,backend', [
    ('linux', '/usr/bin/sandbox-exec'), ('win32', '/usr/bin/sandbox-exec'),
    ('darwin', None), ('darwin', '/caller/sandbox-exec'),
])
def test_no_missing_or_alternate_backend_fallback(config, monkeypatch, platform, backend):
    monkeypatch.setattr(host.sys, 'platform', platform)
    monkeypatch.setattr(host.shutil, 'which', lambda _: backend)
    with pytest.raises(host.HostError, match='sandbox'):
        plan(config)


def test_project_scope_cannot_expand_to_sibling_or_parent(config, tmp_path):
    outside = tmp_path / 'other-project'
    outside.mkdir()
    for root in (outside, config.attempt_root, Path('/')):
        with pytest.raises(host.HostError):
            plan(replace(config, project=replace(config.project, read_roots=(root,))))
    for root in (outside, config.attempt_root):
        with pytest.raises(host.HostError):
            plan(replace(config, project=replace(config.project, write_roots=(root,))))
    with pytest.raises(host.HostError):
        plan(replace(config, project=replace(config.project, read_roots=())))


def test_external_selected_project_can_be_read_but_not_written(config, tmp_path):
    external = tmp_path / 'external-project'
    external.mkdir()
    scope = host._SandboxProjectScope(external, (external,))
    assert f'(allow file-read* (subpath "{external}"))' in plan(replace(config, project=scope)).argv[2]
    with pytest.raises(host.HostError, match='writes must stay inside'):
        plan(replace(config, project=replace(scope, write_roots=(external,))))


def test_project_write_must_have_project_read_authority(config):
    scope = replace(config.project, read_roots=(config.project.project_root / 'read-only',))
    with pytest.raises(host.HostError, match='project read scope'):
        plan(replace(config, project=scope))


def test_private_write_cannot_escape_or_subsume_project(config):
    for private in (config.attempt_root.parent, config.attempt_root, config.project.project_root):
        with pytest.raises(host.HostError, match='private'):
            plan(replace(config, private_write_root=private))


def test_resolved_symlink_scope_is_validated(config, tmp_path):
    outside = tmp_path / 'outside'
    outside.mkdir()
    alias = config.project.project_root / 'escape'
    alias.symlink_to(outside, target_is_directory=True)
    with pytest.raises(host.HostError, match='selected project scope'):
        plan(replace(config, project=replace(config.project, read_roots=(alias,))))
    with pytest.raises(host.HostError, match='private writes'):
        plan(replace(config, private_write_root=alias))


@pytest.mark.parametrize('resource', [Path('/'), Path('relative'), Path('/fixture\ncontrol')])
def test_bootstrap_scope_is_explicit_and_validated(config, resource):
    with pytest.raises(host.HostError):
        plan(replace(config, bootstrap_roots=(resource,)))


def test_bootstrap_missing_wrong_type_and_authority_overlap_denied(config):
    for files in ((config.attempt_root / 'missing',), (config.attempt_root,)):
        with pytest.raises(host.HostError):
            plan(replace(config, bootstrap_files=files))
    for root in (config.attempt_root, config.project.project_root, config.private_write_root):
        with pytest.raises(host.HostError, match='bootstrap roots'):
            plan(replace(config, bootstrap_roots=(root,)))
    with pytest.raises(host.HostError, match='enumerated bootstrap'):
        host._confined_launch_plan([str(config.bootstrap_files[0])], policy=replace(config, bootstrap_files=()))


def test_bootstrap_alias_and_canonical_executable_are_explicit(config, tmp_path):
    alias = tmp_path / 'interpreter-alias'
    alias.symlink_to(config.bootstrap_files[0])
    result = plan(replace(config, bootstrap_files=(alias,)))
    assert result.argv[3] == str(config.bootstrap_files[0])
    for resource in (alias, config.bootstrap_files[0]):
        assert f'(allow file-read* (literal "{resource}"))' in result.argv[2]


def test_unexecutable_bootstrap_command_is_denied(config):
    os.chmod(config.bootstrap_files[0], 0o600)
    with pytest.raises(host.HostError, match='not executable'):
        plan(config)


def test_profile_escapes_literal_path_punctuation(config):
    executable = config.bootstrap_files[0].with_name('interpreter-"quoted\\name')
    executable.write_text('synthetic executable\n')
    os.chmod(executable, 0o700)
    profile = plan(replace(config, bootstrap_files=(executable,))).argv[2]
    escaped = str(executable).replace('\\', '\\\\').replace('"', '\\"')
    assert f'(literal "{escaped}")' in profile


@pytest.mark.parametrize('argv', [[], 'fixture', ['relative'], [12], ['/fixture\x00invalid']])
def test_invalid_command_denied(config, argv):
    with pytest.raises(host.HostError):
        host._confined_launch_plan(argv, policy=config)


def test_request_cwd_and_claims_cannot_grant_access(config, tmp_path):
    with pytest.raises(host.HostError, match='cwd exceeds'):
        plan(config, cwd=tmp_path)
    assert plan(config, cwd=config.project.project_root).cwd == config.project.project_root
    baseline = plan(config)
    hostile = {
        'HOME': str(tmp_path), 'TMPDIR': str(tmp_path), 'PATH': '/caller/bin',
        'PYTHONPATH': '/caller/imports', 'PYTHONSTARTUP': '/caller/hook',
        'DYLD_INSERT_LIBRARIES': '/caller/lib', 'LD_PRELOAD': '/caller/lib',
        'PROVIDER_TOKEN': 'synthetic-sentinel', 'ASTRID_DISABLE_SANDBOX': '1',
        'MCP_CONFIG': '{"filesystem":"/"}', 'TOOL_TITLE': 'approved admin',
        'PROJECT_ROOT': '/', 'BROKER_ENDPOINT': 'http://127.0.0.1:65432',
    }
    assert plan(config, parent_environment=hostile) == baseline
    # There is deliberately no caller policy/MCP/title-to-authority conversion.
    with pytest.raises(TypeError):
        plan(config, mcp_config={'paths': ['/']})


def test_environment_only_selects_host_enumerated_safe_keys(config):
    env = host._SandboxEnvironmentPolicy(('LANG',), (('TERM', 'dumb'),))
    result = plan(replace(config, environment=env), parent_environment={
        'LANG': 'C', 'TERM': 'caller-ignored', 'SECRET': 'synthetic-sentinel',
    })
    selected = dict(result.environment)
    assert selected['LANG'] == 'C' and selected['TERM'] == 'dumb'
    assert 'SECRET' not in selected
    assert selected['HOME'] == selected['TMPDIR'] == str(config.private_write_root)


@pytest.mark.parametrize('environment', [
    host._SandboxEnvironmentPolicy(('PYTHONPATH',)),
    host._SandboxEnvironmentPolicy(values=(('DYLD_INSERT_LIBRARIES', '/fixture'),)),
    host._SandboxEnvironmentPolicy(values=(('HOME', '/fixture'),)),
    host._SandboxEnvironmentPolicy(('LANG',), (('LANG', 'C'),)),
    host._SandboxEnvironmentPolicy(values=(('LANG', 'C\x00bad'),)),
    host._SandboxEnvironmentPolicy(values=(('LANG', 12),)),
    host._SandboxEnvironmentPolicy(values=(['LANG', 'C'],)),
    host._SandboxEnvironmentPolicy(inherit_names=['LANG']),
])
def test_unsafe_or_malformed_environment_policy_denied(config, environment):
    with pytest.raises(host.HostError, match='environment'):
        plan(replace(config, environment=environment))


def test_selected_parent_environment_value_is_validated(config):
    config = replace(config, environment=host._SandboxEnvironmentPolicy(('LANG',)))
    with pytest.raises(host.HostError, match='environment'):
        plan(config, parent_environment={'LANG': 'C\nforged'})


def test_default_network_denies_caller_loopback_without_host_broker(config):
    with pytest.raises(host.HostError, match='not authorized'):
        plan(config, broker_endpoint='http://127.0.0.1:65432')
    outbound = host._SandboxTcpEndpoint('127.0.0.1', 65432)
    config = replace(config, network=host._SandboxNetworkPolicy((outbound,)))
    with pytest.raises(host.HostError, match='not authorized'):
        plan(config, broker_endpoint='http://127.0.0.1:65432')


def test_explicit_broker_and_outbound_permissions_are_exact(config):
    broker = host._SandboxTcpEndpoint('127.0.0.1', 65432)
    outbound = host._SandboxTcpEndpoint('192.0.2.7', 443)
    config = replace(config, network=host._SandboxNetworkPolicy((outbound,), broker))
    profile = plan(config, broker_endpoint='http://127.0.0.1:65432').argv[2]
    assert '(allow network-outbound (remote tcp "127.0.0.1:65432"))' in profile
    assert '(allow network-outbound (remote tcp "192.0.2.7:443"))' in profile
    assert 'localhost' not in profile and 'network-inbound' not in profile
    assert profile.count('network-outbound') == 2
    for requested in ('http://localhost:65432', 'http://127.0.0.1:65433',
                      'http://127.0.0.1:65432/other', 'https://127.0.0.1:65432'):
        with pytest.raises(host.HostError, match='not authorized'):
            plan(config, broker_endpoint=requested)


@pytest.mark.parametrize('address,port', [
    ('localhost', 80), ('*', 80), ('0.0.0.0', 80), ('::1', 80),
    ('224.0.0.1', 80), ('255.255.255.255', 80), ('127.0.0.1', 0),
    ('127.0.0.1', 65536), ('127.0.0.1', True), ('127.0.0.1', '80'),
])
def test_invalid_network_authority_denied(config, address, port):
    network = host._SandboxNetworkPolicy(broker=host._SandboxTcpEndpoint(address, port))
    with pytest.raises(host.HostError, match='endpoint'):
        plan(replace(config, network=network))


def test_malformed_network_authority_denied(config):
    for network in (host._SandboxNetworkPolicy(outbound_tcp=[]),
                    host._SandboxNetworkPolicy(broker='http://127.0.0.1:65432')):
        with pytest.raises(host.HostError):
            plan(replace(config, network=network))


def test_descriptor_allowlist_is_explicit_pipe_only_and_closes_others(config):
    read_fd, write_fd = os.pipe()
    try:
        assert plan(config).subprocess_options()['pass_fds'] == ()
        result = plan(replace(config, pass_fds=(write_fd,)))
        assert result.pass_fds == (write_fd,)
        assert result.subprocess_options()['close_fds'] is True
        assert read_fd not in result.pass_fds
        with config.bootstrap_files[0].open('rb') as file:
            with pytest.raises(host.HostError, match='pipe channels'):
                plan(replace(config, pass_fds=(file.fileno(),)))
    finally:
        os.close(read_fd)
        os.close(write_fd)
    with pytest.raises(host.HostError, match='unavailable'):
        plan(replace(config, pass_fds=(write_fd,)))


@pytest.mark.parametrize('descriptors', [(0,), (1,), (2,), (-1,), (True,), ('12',), (12, 12)])
def test_invalid_descriptor_allowlist_denied(config, descriptors):
    with pytest.raises(host.HostError, match='descriptor allowlist'):
        plan(replace(config, pass_fds=descriptors))
