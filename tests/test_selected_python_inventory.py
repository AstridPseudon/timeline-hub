"""Offline selected-interpreter authority vectors; no Host/Worker starts."""
import copy
import json
import os
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

from runtime_protocol import local_worker_composition as composition
from runtime_protocol import verified_host_launch as gate
from test_verified_host_launch import fixture_authority

QUALIFIED_PYTHON = sys.executable


def selected_case(tmp_path, monkeypatch):
    f = fixture_authority(tmp_path)
    stdlib = f.runtime / 'lib/python3.11'
    extensions = stdlib / 'lib-dynload'
    ambient = stdlib / 'site-packages'
    for root in (extensions, ambient): root.mkdir(parents=True)
    (stdlib / 'selected_stdlib.py').write_text('VALUE=42\n')
    (extensions / ('selected_native' + gate.importlib.machinery.EXTENSION_SUFFIXES[0])).write_bytes(b'FAKE NOT LOADED')
    (ambient / 'ambient_only.py').write_text('raise RuntimeError("ambient")\n')
    (ambient / 'ambient-1.dist-info').mkdir()
    (ambient / 'ambient-1.dist-info/METADATA').write_text('Name: ambient\nVersion: 1\n')
    selected_data = f.source/'resources/site-packages'
    selected_data.mkdir(parents=True)
    (selected_data/'keep.data').write_bytes(b'selected resource, not an ambient package root')
    huge = ambient / 'oversized.dylib'
    with huge.open('wb') as stream: stream.truncate(gate.LIMIT + 1)
    venv = tmp_path / 'venv'
    (venv / 'bin').mkdir(parents=True)
    executable = venv / 'bin/python'
    executable.symlink_to(f.runtime / 'bin/python')
    (venv / 'pyvenv.cfg').write_text('include-system-site-packages = false\n')
    monkeypatch.setattr(gate.sys, 'prefix', str(venv))
    monkeypatch.setattr(gate.sys, 'base_prefix', str(f.runtime))
    monkeypatch.setattr(gate.sys, 'executable', str(executable))
    monkeypatch.setattr(gate.sysconfig, 'get_paths', lambda **kw: {'purelib':str(ambient), 'platlib':str(ambient)})
    monkeypatch.setattr(gate.sysconfig, 'get_path', lambda name: str(stdlib) if name == 'stdlib' else str(f.source))
    monkeypatch.setattr(gate.sysconfig, 'get_config_var', lambda name: str(extensions) if name == 'DESTSHARED' else None)
    profile = f.args['preparation']['profile']
    profile.update(host_executable=str(executable), execution_mode='host_only_cpu',
                   support_root=f.args['config']['support_root'], realm_root=str(tmp_path/'realm'))
    f.args['host_argv'][0] = str(executable)
    f.args['environment'].update(ASTRID_OUTPUT_ROOT=str(tmp_path/'support/host-output'),
                                BANODOCO_LOCAL_DATA_ROOT=str(tmp_path/'realm'))
    monkeypatch.setattr(composition, '_verify_installed_host_records', lambda *args: None)
    monkeypatch.setattr(composition, '_selected_profile_payload', lambda _: profile)
    f.record = composition._installed_host_release(SimpleNamespace(**profile), f.args['config'])
    f.verifier = gate.TrustedLocalHostLaunchVerifier(installed_release=f.record)
    f.stdlib, f.extensions, f.ambient, f.venv = stdlib, extensions, ambient, venv
    return f


@pytest.fixture
def selected(tmp_path, monkeypatch):
    return selected_case(tmp_path, monkeypatch)


def test_selected_roles_keep_runtime_provenance_separate_and_exclude_before_walk(selected, monkeypatch):
    f = selected
    read, walk = gate._bounded_source, Path.iterdir
    def bounded(path, *args):
        assert not Path(path).is_relative_to(f.ambient)
        return read(path, *args)
    def children(path):
        assert not path.is_relative_to(f.ambient)
        return walk(path)
    monkeypatch.setattr(gate, '_bounded_source', bounded)
    monkeypatch.setattr(Path, 'iterdir', children)
    profile = SimpleNamespace(**f.args['preparation']['profile'])
    record = composition._installed_host_release(profile, f.args['config'])
    verifier = gate.TrustedLocalHostLaunchVerifier(installed_release=record)
    proof = verifier.verify(**f.args)
    _, data = verifier.claim(proof, **f.args, binding_fd=3)
    payload = json.loads(data)
    assert payload['mapping']['selected_stdlib']['path'] == str(f.stdlib/'selected_stdlib.py')
    assert payload['mapping']['selected_native']['kind'] == 'extension'
    assert 'ambient_only' not in payload['mapping']
    assert payload['selected_python']['roots']['installed-packages'] == str(f.source)
    entries = record['import_binding']['import_roots']
    assert [e['path'] for e in entries] == [str(f.source), str(f.stdlib), str(f.extensions)]
    runtime = record['inventories'][record['import_binding']['python_runtime_inventory_digest']]
    assert runtime['root'] == str(f.runtime) and 'bin/python' in runtime['files']
    assert all('site-packages' not in name for inv in record['inventories'].values()
               if inv['selection']['role'] != 'installed-packages' for name in inv['files'])
    selected_inventory = next(inv for inv in record['inventories'].values() if inv['root'] == str(f.source))
    assert 'resources/site-packages/keep.data' in selected_inventory['files']
    finder = gate.MappedImports(payload['mapping'], trusted_local=True, distribution_metadata=payload['distribution_metadata'])
    with pytest.raises(ModuleNotFoundError): finder.find_spec('ambient_only')
    assert not list(finder.find_distributions(gate.importlib.metadata.DistributionFinder.Context(name='ambient', path=[str(f.ambient)])))


def test_ambient_internal_changes_do_not_invalidate_selected_installation(selected):
    f = selected
    (f.ambient/'ambient_only.py').write_text('CHANGED=1\n')
    (f.ambient/'new.py').write_text('NEW=1\n')
    proof = f.verifier.verify(**f.args)
    f.verifier.claim(proof, **f.args, binding_fd=3)


def test_distinct_base_purelib_and_platlib_are_both_fixed_exclusions(selected, monkeypatch):
    f = selected
    platlib = f.runtime/'lib64/python3.11/site-packages'
    platlib.mkdir(parents=True)
    with (platlib/'oversized.dylib').open('wb') as stream: stream.truncate(gate.LIMIT + 1)
    monkeypatch.setattr(gate.sysconfig, 'get_paths', lambda **kw: {'purelib':str(f.ambient), 'platlib':str(platlib)})
    with pytest.raises(gate.HostLaunchError): f.verifier.verify(**f.args)
    record = composition._installed_host_release(SimpleNamespace(**f.args['preparation']['profile']), f.args['config'])
    verifier = gate.TrustedLocalHostLaunchVerifier(installed_release=record)
    proof = verifier.verify(**f.args)
    _, data = verifier.claim(proof, **f.args, binding_fd=3)
    assert {row['path'] for row in json.loads(data)['selected_python']['excluded_roots']} == {str(f.ambient), str(platlib)}


@pytest.mark.parametrize('edge', ['zip', 'broken-zip-alias', 'config', 'boundary-alias', 'root-alias', 'interpreter-alias', 'new-source', 'replaced', 'alias-excluded', 'alias-outside'])
def test_selected_drift_refuses_before_issue(selected, edge):
    f = selected
    if edge == 'zip': (f.stdlib.parent/f'python{gate.sys.version_info.major}{gate.sys.version_info.minor}.zip').write_bytes(b'new archive')
    if edge == 'broken-zip-alias': (f.stdlib.parent/f'python{gate.sys.version_info.major}{gate.sys.version_info.minor}.zip').symlink_to('missing.zip')
    if edge == 'config': (f.venv/'pyvenv.cfg').write_text('include-system-site-packages = true\n')
    if edge == 'boundary-alias':
        moved = f.ambient.with_name('moved-ambient'); f.ambient.rename(moved); f.ambient.symlink_to(moved)
    if edge == 'root-alias':
        moved = f.source.with_name('moved-source'); f.source.rename(moved); f.source.symlink_to(moved)
    if edge == 'interpreter-alias':
        executable = Path(f.args['host_argv'][0]); executable.unlink(); executable.symlink_to(str(f.runtime/'bin')+'/./python')
    if edge == 'new-source': (f.source/'new.py').write_text('NEW=1\n')
    if edge == 'replaced':
        replacement = f.source/'replacement'; replacement.write_text('REPLACED=1'); replacement.replace(f.source/'astrid/version.py')
    if edge in ('alias-excluded', 'alias-outside'):
        path = f.source/'astrid/version.py'; path.unlink()
        target = f.ambient/'ambient_only.py'
        if edge == 'alias-outside': target=f.source.parent/'outside.py'; target.write_text('OUTSIDE=1')
        path.symlink_to(target)
    with pytest.raises(gate.HostLaunchError): f.verifier.verify(**f.args)
    assert not f.verifier._issued


@pytest.mark.parametrize('edge', ['role', 'exclusion', 'root', 'file-escape', 'runtime-as-import', 'profile', 'release'])
def test_caller_cannot_forge_inventory_selection(selected, edge):
    f = selected
    record = copy.deepcopy(f.record)
    inventory = next(iter(record['inventories'].values()))
    if edge == 'role': inventory['selection']['role'] = 'caller-selected'
    if edge == 'exclusion': inventory['selection']['layout']['excluded_roots'] = []
    if edge == 'root': inventory['root'] = str(f.ambient)
    if edge == 'file-escape': inventory['files']['../outside.py'] = '0'*64
    if edge == 'runtime-as-import': record['import_binding']['import_roots'].append({'path':str(f.runtime), 'inventory_digest':record['import_binding']['python_runtime_inventory_digest']})
    if edge == 'profile': f.args['preparation']['profile']['profile_digest'] = 'sha256:'+'0'*64
    if edge == 'release': f.args['preparation']['profile']['release_digest'] = 'sha256:'+'0'*64
    verifier = gate.TrustedLocalHostLaunchVerifier(installed_release=record)
    with pytest.raises(gate.HostLaunchError): verifier.verify(**f.args)
    assert not verifier._issued


def test_selected_huge_file_refuses_producer_without_byte_read(selected, monkeypatch):
    f = selected
    huge = f.source/'selected-oversized.data'
    with huge.open('wb') as stream: stream.truncate(gate.LIMIT + 1)
    real = gate.os.read
    def read(fd, count):
        assert os.fstat(fd).st_size <= gate.LIMIT
        return real(fd, count)
    monkeypatch.setattr(gate.os, 'read', read)
    with pytest.raises(gate.HostLaunchError, match='bounded regular file'):
        gate.installed_inventory(f.source, python_role='installed-packages', selected_source=f.source)


def test_startup_drift_after_verify_refuses_claim(selected):
    f = selected
    proof = f.verifier.verify(**f.args)
    (f.venv/'pyvenv.cfg').write_text('changed\n')
    with pytest.raises(gate.HostLaunchError, match='boundary changed'):
        f.verifier.claim(proof, **f.args, binding_fd=3)


def test_private_selected_boundary_crosses_existing_cold_launcher(selected, tmp_path):
    f = selected
    (f.source/'astrid/core/execution/generic_host.py').write_text(
        'import json\nprint(json.dumps(_RETAINED_SELECTED_PYTHON["roots"],sort_keys=True))\n')
    profile = f.args['preparation']['profile']
    profile['host_protocol']['source_closure_digest'] = gate.source_checkout_closure(f.source)['digest']
    record = composition._installed_host_release(SimpleNamespace(**profile), f.args['config'])
    verifier = gate.TrustedLocalHostLaunchVerifier(installed_release=record)
    proof = verifier.verify(**f.args)
    _, data = verifier.claim(proof, **f.args, binding_fd=3)
    payload = tmp_path/'retained.json'; payload.write_bytes(data)
    program = (
        'import importlib.util,json,sys; '
        's=importlib.util.spec_from_file_location("gate",sys.argv[1]); '
        'g=importlib.util.module_from_spec(s);s.loader.exec_module(g); '
        'g.launch_from_binding(json.load(open(sys.argv[2])))')
    child = subprocess.run([QUALIFIED_PYTHON, '-I', '-S', '-B', '-c', program, gate.__file__, str(payload)],
                           capture_output=True, text=True, timeout=10)
    assert child.returncode == 0, child.stderr
    assert json.loads(child.stdout) == gate.selected_python_layout(f.source)['roots']
