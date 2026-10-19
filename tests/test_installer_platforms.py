"""Service contracts and native command boundaries, exercised without OS services."""
import io
import plistlib
import subprocess
import tarfile
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path, PureWindowsPath
from unittest.mock import Mock

import pytest

from astrid.installer import service, tools
from astrid.installer.backend import Backend
from astrid.installer.core import Version, read_json, write_json

FIXTURES = Path(__file__).parent / 'fixtures/installer'


def sample(system='linux'):
    root = PureWindowsPath('C:/Astrid/versions/v1') if system == 'win32' else Path('/astrid/versions/v1')
    python = root / ('py/Scripts/python.exe' if system == 'win32' else 'py/bin/python')
    version = Version(root, python, root / 'profile.json', {'PATH': 'C:\\Astrid\\tools;C:\\Windows\\System32' if system == 'win32' else '/astrid/tools:/usr/bin:/bin', 'PYTHONUTF8': '1'})
    data = PureWindowsPath('C:/Astrid Data') if system == 'win32' else Path('/astrid data')
    log = PureWindowsPath('C:/Astrid/logs/install.log') if system == 'win32' else Path('/logs/install.log')
    return version, data, log


@pytest.mark.parametrize('system,fixture', [('darwin','launchd.plist'), ('linux','systemd.service'), ('win32','task.xml')])
def test_service_definitions_match_reviewed_snapshots(system, fixture):
    version, data, log = sample(system)
    rendered = service.render(system, version, data, log, user='S-1-5-21-1234')
    assert rendered == (FIXTURES / fixture).read_text(encoding='utf-8')
    assert 'npm' not in rendered and 'pack_host' not in rendered and 'chat' not in rendered


def test_launchd_is_foreground_keepalive_with_explicit_environment():
    version, data, log = sample('darwin')
    value = plistlib.loads(service.render('darwin', version, data, log).encode())
    assert value['KeepAlive'] is True and value['RunAtLoad'] is True
    assert value['ProgramArguments'] == [str(version.python), '-I', '-m', 'astrid_runtime', 'run', '--profile', 'astrid', '--data-root', str(data), '--source-manifest', str(version.profile)]
    assert value['EnvironmentVariables']['PATH'] == version.env['PATH']


def test_windows_task_settings_and_no_console_executable():
    version, data, log = sample('win32')
    root = ET.fromstring(service.render('win32', version, data, log, user='S-1-5-21-1234'))
    ns = {'t': 'http://schemas.microsoft.com/windows/2004/02/mit/task'}
    def field(path):
        return root.find(path, ns).text
    assert field('t:Settings/t:ExecutionTimeLimit') == 'PT0S'
    assert field('t:Settings/t:DisallowStartIfOnBatteries') == 'false'
    assert field('t:Settings/t:StopIfGoingOnBatteries') == 'false'
    assert field('t:Settings/t:MultipleInstancesPolicy') == 'IgnoreNew'
    assert field('t:Principals/t:Principal/t:LogonType') == 'InteractiveToken'
    assert field('t:Principals/t:Principal/t:RunLevel') == 'LeastPrivilege'
    assert field('t:Triggers/t:LogonTrigger/t:UserId') == 'S-1-5-21-1234'
    assert field('t:Actions/t:Exec/t:Command').endswith('pythonw.exe')
    arguments = field('t:Actions/t:Exec/t:Arguments')
    assert 'os.environ.update' in arguments and 'astrid_runtime.cli' in arguments
    assert 'open(' in arguments and 'encoding=' in arguments
    assert 'Hidden' not in service.render('win32', version, data, log)


def test_systemd_quotes_spaces_percent_dollar_and_supply_tool_path():
    version, data, log = sample()
    version = Version(version.root, Path('/astrid %v $x/py/bin/python'), version.profile, version.env)
    unit = service.render('linux', version, data, log)
    assert 'ExecStart="/astrid %%v $$x/py/bin/python"' in unit
    assert '"/astrid data"' in unit
    assert 'Environment="PATH=/astrid/tools:/usr/bin:/bin"' in unit
    assert 'Restart=on-failure' in unit
    assert 'WantedBy=default.target' in unit


def test_non_systemd_fallback_is_explicit_and_requests_runtime_start(tmp_path):
    runner = Mock(side_effect=FileNotFoundError('systemctl'))
    lines = []
    manager = service.Service(tmp_path / 'program', tmp_path / 'log', runner, home=tmp_path, system='linux', say=lines.append)
    version = Version(tmp_path / 'program/versions/v1', tmp_path / 'python', tmp_path / 'profile', {'PATH': '/tools:/bin'})
    manager.register(version, tmp_path / 'data')
    assert manager.start() is False
    assert lines == ['There is no systemd user service; run the install line to restart Astrid.']
    assert read_json(manager.registry)['data_root'] == str(tmp_path / 'data')


def test_task_registration_is_no_profile_and_failure_is_not_hidden(tmp_path):
    runner = Mock(side_effect=subprocess.CalledProcessError(1, 'powershell'))
    manager = service.Service(tmp_path / 'program', tmp_path / 'log', runner, home=tmp_path, system='win32')
    with pytest.raises(subprocess.CalledProcessError):
        manager.powershell('Register-ScheduledTask')
    argv = runner.call_args.args[0]
    assert '-NoProfile' in argv and '-ExecutionPolicy' in argv
    assert "$ErrorActionPreference='Stop'" in argv[-1]


def test_service_record_preserves_an_unavailable_workspace_instead_of_falling_back(tmp_path):
    manager = service.Service(tmp_path / 'program', tmp_path / 'log', Mock(), home=tmp_path, system='linux')
    write_json(manager.registry, {'owner': service.LABEL, 'data_root': str(tmp_path / 'offline-drive')})
    assert manager.recorded()['data_root'] == str(tmp_path / 'offline-drive')


def test_ffmpeg_probe_checks_every_required_encoder_and_analysis_filter():
    encoders = '\n'.join(' V..... ' + name + ' description' for name in tools.ENCODERS)
    filters = '\n'.join(' ... ' + name + ' description' for name in tools.FILTERS)
    tools.probe_ffmpeg(encoders, filters)
    for name in tools.ENCODERS | tools.FILTERS:
        with pytest.raises(ValueError, match=name):
            tools.probe_ffmpeg(encoders.replace(name, 'absent'), filters.replace(name, 'absent'))
    with pytest.raises(ValueError, match='libx264'):
        tools.probe_ffmpeg('ffmpeg version 7.0.2', 'ffmpeg version 7.0.2')


@pytest.mark.parametrize('name', ['../escape', '/absolute', 'C:/windows', 'safe\\..\\escape'])
def test_downloaded_archives_cannot_escape_owned_staging_directory(tmp_path, name):
    archive = tmp_path / 'payload.zip'
    with zipfile.ZipFile(archive, 'w') as bundle:
        bundle.writestr(name, 'payload')
    with pytest.raises(ValueError, match='Unsafe archive'):
        tools.extract(archive, tmp_path / 'extract')
    assert not (tmp_path / 'escape').exists()


def test_tar_never_materializes_links_and_keeps_official_node_npm_entrypoint(tmp_path):
    archive = tmp_path / 'node.tar.gz'
    with tarfile.open(archive, 'w:gz') as bundle:
        entry = tarfile.TarInfo('node/bin/npm')
        entry.type = tarfile.SYMTYPE
        entry.linkname = '../lib/node_modules/npm/bin/npm-cli.js'
        bundle.addfile(entry)
        entry = tarfile.TarInfo('node/lib/node_modules/npm/bin/npm-cli.js')
        entry.size = 4
        bundle.addfile(entry, io.BytesIO(b'npm!'))
    tools.extract(archive, tmp_path / 'extract')
    assert not (tmp_path / 'extract/node/bin/npm').exists()
    assert tools.binary(tmp_path / 'extract', 'npm-cli.js').read_bytes() == b'npm!'


def test_uninstall_only_removes_owned_files_and_reports_windows_lock_residue(tmp_path, monkeypatch):
    program, data = tmp_path / 'program', tmp_path / 'data'
    program.mkdir()
    data.mkdir()
    sentinel = data / 'film'
    sentinel.write_text('keep')
    backend = Backend(program, tmp_path / 'log', tmp_path / 'uv')
    with pytest.raises(ValueError, match='unowned'):
        backend.remove(program, data, delete_data=False)
    write_json(program / 'install.json', {'owner': service.LABEL})
    (program / 'versions').mkdir()
    monkeypatch.setattr('shutil.rmtree', Mock(side_effect=PermissionError('locked DLL')))
    assert backend.remove(program, data, delete_data=False) == [program / 'versions']
    assert read_json(program / 'install.json')['owner'] == service.LABEL
    assert sentinel.read_text() == 'keep'


def test_backend_native_failures_reach_transaction_and_log_details(tmp_path, monkeypatch):
    backend = Backend(tmp_path / 'program', tmp_path / 'install.log', tmp_path / 'uv')
    monkeypatch.setattr(subprocess, 'run', Mock(return_value=subprocess.CompletedProcess(['tool'], 19, 'failure details')))
    with pytest.raises(subprocess.CalledProcessError) as error:
        backend.run(['tool'])
    assert error.value.returncode == 19
    assert 'failure details' in (tmp_path / 'install.log').read_text()


def test_old_service_wrapper_data_root_is_read_without_executing_profile(tmp_path):
    program = tmp_path / 'old program'
    (program / 'bin').mkdir(parents=True)
    data = tmp_path / 'existing film'
    (program / 'env').write_text(f"export ASTRID_RUNTIME_DATA_ROOT='{data}'\nexport UNRELATED='$(do-not-execute)'\n")
    manager = service.Service(tmp_path / 'new program', tmp_path / 'log', Mock(), home=tmp_path, system='darwin')
    manager.path.parent.mkdir(parents=True)
    manager.path.write_bytes(plistlib.dumps({'ProgramArguments': [str(program / 'bin/astrid-service')]}))
    assert manager.recorded() == {'data_root': str(data)}


def test_linux_backup_temporarily_starts_only_neutral_daemon_and_snapshots_stopped_support(tmp_path, monkeypatch):
    program, data, realm = tmp_path / 'program', tmp_path / 'data', tmp_path / 'data/runtime/realms/one'
    realm.mkdir(parents=True)
    (realm / 'film').write_text('large media')
    write_json(data / 'runtime/catalog.json', {'selected': 'one'})
    backend = Backend(program, tmp_path / 'log', tmp_path / 'uv')
    backend.service.system = 'linux'
    calls = []
    def runtime(version, root, *args, **kwargs):
        calls.append(args)
        if args[0] == 'backup':
            destination = Path(args[2])
            destination.mkdir(parents=True)
            (destination / 'authenticated-backup').write_text('verified')
        return {}
    backend.runtime = runtime
    backend.stop = lambda version, root: calls.append(('stop',))
    version = Version(program / 'versions/old', tmp_path / 'python', tmp_path / 'profile', {})
    result = backend.backup(version, data, {'realm_root': str(realm)})
    assert [call[0] for call in calls] == ['up', 'backup', 'stop']
    assert calls[0] == ('up', '--hosted-origin', 'off')
    snapshot = Path(result['root']) / 'support'
    assert read_json(snapshot / 'runtime/catalog.json') == {'selected': 'one'}
    assert not (snapshot / 'runtime/realms').exists()
    assert (realm / 'film').read_text() == 'large media'


def test_mac_backup_uses_runtime_fsclone_only_after_stop_and_never_starts_daemon(tmp_path, monkeypatch):
    import shutil
    program, data, realm = tmp_path / 'program', tmp_path / 'data', tmp_path / 'realm'
    realm.mkdir()
    (realm / 'realm.sqlite3').write_text('stopped db')
    write_json(data / 'runtime/catalog.json', {'selected': 'one'})
    copies = []
    def clone(src, dst):
        copies.append((src, dst))
        shutil.copy2(src, dst)
    monkeypatch.setattr('runtime_protocol.fsclone.clone_or_copy_file', clone)
    backend = Backend(program, tmp_path / 'log', tmp_path / 'uv')
    backend.service.system = 'darwin'
    backend.runtime = Mock(side_effect=AssertionError('must remain stopped'))
    version = Version(program / 'versions/old', tmp_path / 'python', tmp_path / 'profile', {})
    result = backend.backup(version, data, {'realm_root': str(realm)})
    assert result['kind'] == 'clone'
    assert {src.name for src, dst in copies} == {'realm.sqlite3', 'catalog.json'}
    assert (Path(result['root']) / 'realm/realm.sqlite3').read_text() == 'stopped db'


def test_clone_rollback_restores_workspace_and_support_without_deleting_other_realms(tmp_path, monkeypatch):
    import shutil
    program, data = tmp_path / 'program', tmp_path / 'data'
    realm = data / 'runtime/realms/one'
    other = data / 'runtime/realms/two'
    realm.mkdir(parents=True)
    other.mkdir()
    (realm / 'realm.sqlite3').write_text('original')
    (other / 'unselected').write_text('keep')
    write_json(data / 'runtime/catalog.json', {'selected': 'one'})
    write_json(data / 'runtime/source-profiles/astrid.json', {'version': 'old'})
    monkeypatch.setattr('runtime_protocol.fsclone.clone_or_copy_file', lambda src, dst: shutil.copy2(src, dst))
    backend = Backend(program, tmp_path / 'log', tmp_path / 'uv')
    backend.service.system = 'darwin'
    version = Version(program / 'versions/old', tmp_path / 'python', tmp_path / 'profile', {})
    identity = {'realm_root': str(realm)}
    backup = backend.backup(version, data, identity)
    (realm / 'realm.sqlite3').write_text('migrated')
    write_json(data / 'runtime/source-profiles/astrid.json', {'version': 'new'})
    backend.restore(version, data, identity, backup)
    assert (realm / 'realm.sqlite3').read_text() == 'original'
    assert read_json(data / 'runtime/source-profiles/astrid.json') == {'version': 'old'}
    assert (other / 'unselected').read_text() == 'keep'
    assert any((p / 'realm.sqlite3').read_text() == 'migrated' for p in realm.parent.glob('one.failed-*'))


@pytest.mark.parametrize('mismatch', [None, 'realm', 'instance', 'port', 'owner'])
def test_door_verification_requires_selected_realm_recorded_instance_and_live_owner(tmp_path, monkeypatch, mismatch):
    import json

    from astrid.installer import backend as module
    program, data = tmp_path / 'program', tmp_path / 'data'
    version = Version(program / 'versions/old', tmp_path / 'python', tmp_path / 'profile', {})
    discovery = {'active_realm': 'selected', 'runtime_instance_id': 'owned-instance',
                 'door_endpoint': 'http://127.0.0.1:17340'}
    if mismatch == 'port':
        discovery['door_endpoint'] = 'http://127.0.0.1:9999'
    write_json(data / 'runtime/discovery.json', discovery)
    health = {'status': 'ok', 'runtime_instance_id': 'foreign' if mismatch == 'instance' else 'owned-instance'}
    realm = {'realm_id': 'other' if mismatch == 'realm' else 'selected'}
    def opening(request, timeout):
        return io.BytesIO(json.dumps(health if request.full_url.endswith('/health') else realm).encode())
    opener = Mock()
    opener.open.side_effect = opening
    monkeypatch.setattr(module.urllib.request, 'build_opener', Mock(return_value=opener))
    ticks = iter([0, 0, 91])
    monkeypatch.setattr(module.time, 'monotonic', lambda: next(ticks))
    monkeypatch.setattr(module.time, 'sleep', lambda value: None)
    backend = Backend(program, tmp_path / 'log', tmp_path / 'uv')
    backend.runtime = Mock(return_value={'discovery': discovery, 'support': {'pid_alive': mismatch != 'owner'}})
    if mismatch:
        with pytest.raises(RuntimeError, match='door did not become ready'):
            backend.verify(version, data, 'selected')
    else:
        backend.verify(version, data, 'selected')
        assert all(call.args[0].headers['Origin'] == 'https://astrid.haus' for call in opener.open.call_args_list)


def test_source_archives_are_flattened_to_shallow_managed_paths(tmp_path, monkeypatch):
    def unpack(url, destination):
        child = destination / ('astrid-agent-' + 'a' * 40)
        child.mkdir(parents=True)
        (child / 'pyproject.toml').write_text('source')
    monkeypatch.setattr(tools, 'fetch_archive', unpack)
    root = tools.source('agent', 'a' * 40, tmp_path / 'a')
    assert root == tmp_path / 'a'
    assert (root / 'pyproject.toml').read_text() == 'source'
    assert not (tmp_path / 'a.unpack').exists()


def test_python311_windows_reparse_points_are_rejected_using_mocked_file_attributes(monkeypatch):
    import stat
    from types import SimpleNamespace

    from astrid.installer.core import absolute, linked
    monkeypatch.setattr(Path, 'is_symlink', lambda path: False)
    monkeypatch.setattr(Path, 'lstat', lambda path: SimpleNamespace(st_file_attributes=stat.FILE_ATTRIBUTE_REPARSE_POINT))
    assert linked(Path('/junction'))
    with pytest.raises(ValueError, match='cannot contain links'):
        absolute('/junction/workspace')


def test_delete_data_includes_identity_checked_external_attached_workspace(tmp_path, monkeypatch):
    program, data, external = tmp_path / 'program', tmp_path / 'support', tmp_path / 'film'
    data.mkdir()
    external.mkdir()
    (external / 'film.mov').write_text('media')
    write_json(program / 'install.json', {'owner': service.LABEL, 'data_root': str(data)})
    backend = Backend(program, tmp_path / 'log', tmp_path / 'uv')
    version = Version(program / 'versions/old', tmp_path / 'python', tmp_path / 'profile', {})
    monkeypatch.setattr(backend, 'existing', lambda path: version)
    monkeypatch.setattr(backend, 'workspace', lambda version, root: {'realm_root': str(external)})
    assert backend.remove(program, data, delete_data=True) == []
    assert not program.exists() and not data.exists() and not external.exists()


def test_no_systemd_starts_foreground_runtime_supervisor_with_recorded_birth_identity(tmp_path, monkeypatch):
    from runtime_protocol import platform
    run = Mock(side_effect=FileNotFoundError('no systemd'))
    manager = service.Service(tmp_path / 'program', tmp_path / 'log', run, home=tmp_path, system='linux')
    version = Version(tmp_path / 'program/versions/v1', tmp_path / 'python', tmp_path / 'profile', {'PATH': '/tools:/bin'})
    manager.register(version, tmp_path / 'data')
    spawn = Mock(return_value=Mock(pid=123))
    monkeypatch.setattr(platform, 'spawn_tree', spawn)
    monkeypatch.setattr(platform, 'process_identity', lambda pid: {'birth_id': 'birth-123'})
    manager.start_foreground(version, tmp_path / 'data')
    assert spawn.call_args.args[0][3:5] == ['astrid_runtime', 'run']
    assert spawn.call_args.kwargs['detached'] is True
    assert spawn.call_args.kwargs['env']['PATH'] == '/tools:/bin'
    assert read_json(manager.registry)['foreground'] == {'pid': 123, 'birth_id': 'birth-123'}
    # PID reuse cannot make uninstall wait for an unrelated process.
    monkeypatch.setattr(platform, 'process_identity', lambda pid: {'birth_id': 'new-owner'})
    manager.stop()
