"""Selected installation excludes ambient descendants even under stdlib allows."""
from dataclasses import replace
import errno
import json
import os
from pathlib import Path
import subprocess
import sys

import pytest

from astrid.core.execution import generic_host as host
from tests.core.execution.test_confinement_launch_integration import launch


PROBE = r'''
import importlib.util,json,mmap,sys
from pathlib import Path
ambient,selected,native=sys.argv[1:]
def load(path):
    spec=importlib.util.spec_from_file_location("planted",path)
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.VALUE
def observe(call):
    try: return {"value":call()}
    except OSError as exc: return {"errno":exc.errno}
def mapping():
    with open(native,"rb") as stream:
        with mmap.mmap(stream.fileno(),4096,flags=mmap.MAP_PRIVATE,prot=mmap.PROT_READ|mmap.PROT_EXEC):
            return "mapped"
print(json.dumps({"selected":load(selected),
    "ambient_read":observe(lambda:Path(ambient).read_text()),
    "ambient_import":observe(lambda:load(ambient)),
    "ambient_mapping":observe(mapping)}))
'''


def test_real_ambient_explicit_read_import_and_executable_mapping_denied(launch, tmp_path):
    policy, _, _, _ = launch
    ancestor = tmp_path/'synthetic-stdlib'
    ambient = ancestor/'site-packages'
    installed = tmp_path/'selected-packages'
    ambient.mkdir(parents=True); installed.mkdir()
    bad = ambient/'planted.py'; bad.write_text('VALUE="ambient"\n')
    good = installed/'selected.py'; good.write_text('VALUE="selected"\n')
    # Preserve a genuine signed Mach-O page so macOS code-signing refusal
    # cannot masquerade as the sandbox's executable-map denial.
    native = ambient/'native-page'; native.write_bytes(Path(sys.executable).resolve().read_bytes())
    native.chmod(0o700)
    # Exec registers the copied image's existing signature with the kernel.
    # Raw mmap alone does not register a new vnode's code signature on macOS.
    subprocess.run([str(native), '-I', '-S', '-B', '-c', 'pass'], check=True, capture_output=True)
    policy = replace(policy, bootstrap_roots=(*policy.bootstrap_roots, ancestor, installed))
    argv = [str(Path(sys.executable).resolve()), '-I', '-S', '-B', '-c', PROBE,
            str(bad), str(good), str(native)]
    def run(current, *, mapping_only=False):
        plan = host._confined_launch_plan(argv, policy=current)
        args = list(plan.argv)
        if mapping_only:
            # Isolate the map deny from the earlier open deny, so failure to
            # open a file cannot masquerade as executable-mapping coverage.
            args[2] = args[2].replace(f'(deny file-read* (subpath "{ambient}"))\n', '')
        result = subprocess.run(args, **plan.subprocess_options(), text=True, timeout=15)
        assert result.returncode == 0, result.stderr
        return json.loads(result.stdout), plan
    control, _ = run(policy)
    assert control['selected'] == 'selected' and control['ambient_import'] == {'value':'ambient'}
    assert control['ambient_mapping'] == {'value':'mapped'}
    denied = replace(policy, excluded_python_roots=(ambient,))
    observed, plan = run(denied)
    assert observed['selected'] == 'selected'
    for name in ('ambient_read','ambient_import','ambient_mapping'):
        assert observed[name]['errno'] in (errno.EACCES, errno.EPERM)
    assert f'(deny file-map-executable (subpath "{ambient}"))' in plan.argv[2]
    mapped, _ = run(denied, mapping_only=True)
    assert mapped['ambient_read']['value'].startswith('VALUE=')
    assert mapped['ambient_mapping']['errno'] in (errno.EACCES, errno.EPERM)


@pytest.mark.parametrize('edge', ['bootstrap', 'alias', 'search', 'project'])
def test_policy_cannot_readd_excluded_python_code(launch, tmp_path, edge):
    policy, _, _, _ = launch
    excluded = tmp_path/'ambient'; excluded.mkdir()
    selected = excluded/'selected'; selected.mkdir()
    changes = {'excluded_python_roots':(excluded,)}
    if edge == 'bootstrap': changes['bootstrap_roots'] = (*policy.bootstrap_roots, selected)
    if edge == 'search': changes['bootstrap_search_roots'] = (selected,)
    if edge == 'alias':
        alias = tmp_path/'alias'; alias.symlink_to(selected)
        changes['bootstrap_roots'] = (*policy.bootstrap_roots, alias)
    if edge == 'project': changes['excluded_python_roots'] = (policy.project.project_root,)
    with pytest.raises(host.HostError, match='re-admit excluded'):
        host._confined_launch_plan([str(Path(sys.executable).resolve())], policy=replace(policy, **changes))


def test_retained_package_root_overrides_minus_s_sysconfig_and_rejects_caller_boundary(monkeypatch, tmp_path):
    base = Path(sys.base_prefix).resolve()
    scheme = host.sysconfig.get_paths(vars={'base':str(base), 'platbase':str(base),
        'installed_base':str(base), 'installed_platbase':str(base)})
    rows=[]
    for raw in sorted({scheme[n] for n in ('purelib','platlib')}):
        path=Path(raw)
        kind='symlink' if path.is_symlink() else 'directory' if path.is_dir() else 'absent' if not path.exists() else 'file'
        rows.append(dict(path=raw,kind=kind,target=os.readlink(path) if kind=='symlink' else None,resolved=str(path.resolve())))
    selected=Path(host.__file__).resolve().parents[3]
    value={'version':1,'roots':{'installed-packages':str(selected),'python-runtime':str(base),
        'python-stdlib':host.sysconfig.get_path('stdlib'),'python-extensions':host.sysconfig.get_config_var('DESTSHARED')},
        'excluded_roots':rows,'startup_files':{},'interpreter':host._python_path_binding(Path(os.path.abspath(sys.executable)))}
    value['root_bindings']={role:host._python_path_binding(Path(raw)) for role,raw in value['roots'].items()}
    monkeypatch.setattr(host, '_RETAINED_SELECTED_PYTHON', value, raising=False)
    assert host._selected_python_package_paths() == (str(selected),)
    from tests.test_generic_host import _write_manifest
    pack=tmp_path/'pack'; _write_manifest(pack)
    owner=host.GenericPackHost(pack_roots=[pack]); owner.discover()
    attempt=tmp_path/'attempt'; attempt.mkdir()
    policy=host._AttemptPolicyFactory(owner._executable_admission).build(
        host._AuthenticatedAttempt((('project_id','synthetic'),)), attempt=attempt,
        record=owner.capabilities['test.echo'])
    assert selected in policy.bootstrap_roots
    assert {Path(row['path']) for row in rows} <= set(policy.excluded_python_roots)
    assert not any(Path(row['path']) in policy.bootstrap_roots for row in rows)
    plan=host._confined_launch_plan([str(Path(sys.executable).resolve())], policy=policy)
    for row in rows:
        assert f'(deny file-read* (subpath "{row["path"]}"))' in plan.argv[2]
        assert f'(deny file-map-executable (subpath "{row["path"]}"))' in plan.argv[2]
    value['excluded_roots']=[]
    with pytest.raises(host.HostError, match='exclusion boundary'):
        host._selected_python_package_paths()
