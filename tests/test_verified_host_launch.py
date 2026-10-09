"""Fake/offline G1b vectors; no selected interpreter, host or kernel launch."""
import ast
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import pickle
from types import ModuleType, SimpleNamespace

import pytest
from runtime_protocol import verified_host_launch as gate


def fixture_authority(tmp_path):
    source = tmp_path / 'source'; runtime = tmp_path / 'runtime'
    source_files = {
        'astrid/__init__.py': '', 'astrid/version.py': '__version__="fake"\n',
        'astrid/__main__.py': '', 'astrid/runtime_cli.py': '', 'astrid/omp_agent.py': '',
        'astrid/core/__init__.py': '', 'astrid/core/execution/__init__.py': '',
        'astrid/core/execution/generic_host.py': 'ANSWER=7\n',
        'astrid/sdk/__init__.py': '', 'banodoco_workspace_client/__init__.py': '',
    }
    for relative, content in source_files.items():
        path=source/relative;path.parent.mkdir(parents=True,exist_ok=True);path.write_text(content)
    python=runtime/'bin/python';python.parent.mkdir(parents=True);python.write_bytes(b'FAKE NOT EXECUTABLE PYTHON')
    launcher=tmp_path/'fake-loader.py';launcher.write_text('# Fake standalone artifact; never launched\n')
    def inventory(root):
        return {'root':str(root),'files':{str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in root.rglob('*') if p.is_file()}}
    invs=[inventory(source),inventory(runtime)];pins={gate.raw_digest(i):i for i in invs}
    closure=gate.source_checkout_closure(source)
    protocol={'version':gate.CURRENT_ROLES_VERSION,'module':gate.HOST_MODULE,'source_closure_digest':closure['digest']}
    profile={'profile_id':'fake-profile','profile_digest':'sha256:'+'1'*64,'release_digest':'sha256:'+'2'*64,'host_executable':str(python),'host_artifact_digest':'sha256:'+hashlib.sha256(python.read_bytes()).hexdigest(),'host_protocol':protocol}
    preparation={'profile':profile,'operation_id':'op','channel_id':'channel','owner_epoch':'epoch','custody_scope':str(tmp_path/'custody')}
    config={'source_checkout':str(source),'support_root':str(tmp_path/'support')}
    argv=[str(python),'-m',gate.HOST_MODULE,'run'];env={'PATH':'/fake/bin'}
    record={'selected_profile_digest':gate.raw_digest(profile),'profile_digest':profile['profile_digest'],'release_digest':profile['release_digest'],'host_protocol':protocol,'source_checkout':str(source),'source_components':closure['components'],'inventories':pins,
        'import_binding':{'schema_version':1,'mode':gate.MODE,'launcher':{'path':str(launcher),'sha256':hashlib.sha256(launcher.read_bytes()).hexdigest()},'python_runtime_inventory_digest':gate.raw_digest(invs[1]),'import_roots':[{'path':i['root'],'inventory_digest':gate.raw_digest(i)} for i in invs]}}
    # Explicit fake protection: it observes files only, not an installed immutable
    # boundary. Nothing in these tests qualifies production materialization.
    class FakeProtection:
        broken=False
        def verify(self):
            if self.broken: raise gate.HostLaunchError('fake protection lost')
    lease=FakeProtection()
    verifier=gate.HostLaunchVerifier(authority_resolver=lambda selected:copy.deepcopy(record),protected_materialization=lambda reviewed:lease)
    args={'preparation':preparation,'config':config,'host_argv':argv,'environment':env}
    return SimpleNamespace(source=source,runtime=runtime,launcher=launcher,record=record,args=args,verifier=verifier,lease=lease)


def test_private_retained_result_selects_exact_isolated_launch_once(tmp_path):
    f=fixture_authority(tmp_path);proof=f.verifier.verify(**f.args)
    argv,payload=f.verifier.claim(proof,**f.args,binding_fd=31)
    assert argv==[f.args['host_argv'][0],'-I','-S',str(f.launcher),'--binding-fd','31']
    body=json.loads(payload);assert body['host_argv'][-2:]==['--source-closure-digest',f.record['host_protocol']['source_closure_digest']]
    assert body['mapping'][gate.HOST_MODULE]['path']==str(f.source/'astrid/core/execution/generic_host.py')
    assert body['mapping']['astrid.core.execution']['package']
    with pytest.raises(TypeError):pickle.dumps(proof)
    with pytest.raises(gate.HostLaunchError): f.verifier.claim(proof,**f.args,binding_fd=31)
    child=SimpleNamespace(pid=41);identity={'pid':41,'uid':501,'birth_id':'fake-birth'}
    assert f.verifier.bind_child(proof,child=child,identity=identity)==gate.CURRENT_ROLES_VERSION
    f.verifier.verify_child(proof,child=child,identity=identity)
    with pytest.raises(gate.HostLaunchError):f.verifier.verify_child(proof,child=SimpleNamespace(pid=41),identity=identity)
    with pytest.raises(gate.HostLaunchError):f.verifier.bind_child(proof,child=child,identity=identity)


def test_no_default_authority_or_manifest_self_authentication(tmp_path):
    f=fixture_authority(tmp_path)
    with pytest.raises(gate.HostLaunchError,match='no independently reviewed'):gate.HostLaunchVerifier().verify(**f.args)
    with pytest.raises(gate.HostLaunchError,match='protection'):gate.HostLaunchVerifier(authority_resolver=lambda _:f.record,protected_materialization=lambda _:True).verify(**f.args)
    with pytest.raises(gate.HostLaunchError):f.verifier.claim(json.loads(gate.canonical(f.record)),**f.args,binding_fd=1)
    proof=f.verifier.verify(**f.args)
    other=gate.HostLaunchVerifier(authority_resolver=lambda _:f.record,protected_materialization=lambda _:f.lease)
    with pytest.raises(gate.HostLaunchError):other.claim(proof,**f.args,binding_fd=1)


@pytest.mark.parametrize('key,value',[('version',2),('version','v1'),('module','shadow.host'),('source_closure_digest','sha256:'+'a'*64),('source_closure_digest','A'*64),('source_closure_digest',None)])
def test_exact_protocol_fields(tmp_path,key,value):
    f=fixture_authority(tmp_path);p=copy.deepcopy(f.record['host_protocol']);p[key]=value
    with pytest.raises(gate.HostLaunchError):gate.validate_host_protocol(p)


@pytest.mark.parametrize('value',[None,{}, {'version':gate.CURRENT_ROLES_VERSION}, {'version':gate.CURRENT_ROLES_VERSION,'module':gate.HOST_MODULE,'source_closure_digest':'a'*64,'approved':True}])
def test_protocol_partial_unknown_or_null(value):
    with pytest.raises(gate.HostLaunchError):gate.validate_host_protocol(value)


@pytest.mark.parametrize('edge',['profile','release','component','closure','inventory','interpreter','module','protection','launcher'])
def test_failed_authority_materialization_edges_never_issue(tmp_path,edge):
    f=fixture_authority(tmp_path)
    if edge=='profile':f.record['selected_profile_digest']='a'*64
    if edge=='release':f.record['release_digest']='sha256:'+'3'*64
    if edge=='component':f.record['source_components'][0]['sha256']='a'*64
    if edge=='closure':f.args['preparation']['profile']['host_protocol']['source_closure_digest']='a'*64
    if edge=='inventory':next(iter(f.record['inventories'].values()))['files']['astrid/version.py']='a'*64
    if edge=='interpreter':f.args['preparation']['profile']['host_artifact_digest']='sha256:'+'a'*64
    if edge=='module':f.args['host_argv'][2]='shadow.host'
    if edge=='protection':f.lease.broken=True
    if edge=='launcher':f.launcher.write_text('changed')
    with pytest.raises(gate.HostLaunchError):f.verifier.verify(**f.args)
    assert f.verifier._issued=={}


@pytest.mark.parametrize('override',['PYTHONPATH','PYTHONHOME','PYTHONSTARTUP','LD_PRELOAD','DYLD_INSERT_LIBRARIES'])
def test_ambient_environment_cannot_enable_or_shadow(tmp_path,override):
    f=fixture_authority(tmp_path);f.args['environment'][override]='/shadow'
    with pytest.raises(gate.HostLaunchError,match='environment'):f.verifier.verify(**f.args)


@pytest.mark.parametrize('edge',['owner_epoch','channel','operation','argv','cwd','environment'])
def test_changed_launch_or_session_permanently_consumes_proof(tmp_path,edge):
    f=fixture_authority(tmp_path);proof=f.verifier.verify(**f.args);bad=copy.deepcopy(f.args)
    if edge=='owner_epoch':bad['preparation']['owner_epoch']='other'
    if edge=='channel':bad['preparation']['channel_id']='other'
    if edge=='operation':bad['preparation']['operation_id']='other'
    if edge=='argv':bad['host_argv'].append('--other')
    if edge=='cwd':bad['config']['support_root']='/other'
    if edge=='environment':bad['environment']['PATH']='/other'
    with pytest.raises(gate.HostLaunchError):f.verifier.claim(proof,**bad,binding_fd=4)
    with pytest.raises(gate.HostLaunchError):f.verifier.claim(proof,**f.args,binding_fd=4)
    with pytest.raises(gate.HostLaunchError):f.verifier.bind_child(proof,child=SimpleNamespace(pid=3),identity={'pid':3,'birth_id':'fake'})


def test_failed_child_binding_and_lost_protection_are_fenced(tmp_path):
    f=fixture_authority(tmp_path);proof=f.verifier.verify(**f.args);f.verifier.claim(proof,**f.args,binding_fd=4)
    child=SimpleNamespace(pid=41)
    with pytest.raises(gate.HostLaunchError):f.verifier.bind_child(proof,child=child,identity={'pid':42,'birth_id':'fake'})
    with pytest.raises(gate.HostLaunchError):f.verifier.bind_child(proof,child=child,identity={'pid':41,'birth_id':'fake'})
    f=fixture_authority(tmp_path/'second');proof=f.verifier.verify(**f.args);f.verifier.claim(proof,**f.args,binding_fd=4)
    identity={'pid':41,'birth_id':'fake'};f.verifier.bind_child(proof,child=child,identity=identity)
    f.lease.broken=True
    with pytest.raises(gate.HostLaunchError):f.verifier.verify_child(proof,child=child,identity=identity)
    f.lease.broken=False
    with pytest.raises(gate.HostLaunchError):f.verifier.verify_child(proof,child=child,identity=identity)


@pytest.mark.parametrize('relative',['astrid/core/execution/__init__.py','astrid/version.py'])
def test_package_initializer_or_source_substitution_fails(tmp_path,relative):
    f=fixture_authority(tmp_path);(f.source/relative).write_text('changed')
    with pytest.raises(gate.HostLaunchError):f.verifier.verify(**f.args)


@pytest.mark.parametrize('extra',['shadow.py','cache.pyc','unreviewed.pth'])
def test_unexpected_importable_or_bytecode_rejected(tmp_path,extra):
    f=fixture_authority(tmp_path);(f.source/extra).write_text('unexpected')
    with pytest.raises(gate.HostLaunchError):f.verifier.verify(**f.args)


def test_symlink_and_missing_component_fail_closed(tmp_path):
    f=fixture_authority(tmp_path);p=f.source/'astrid/version.py';p.unlink();p.symlink_to(f.source/'astrid/runtime_cli.py')
    with pytest.raises(gate.HostLaunchError):f.verifier.verify(**f.args)
    p.unlink()
    with pytest.raises(gate.HostLaunchError):gate.source_checkout_closure(f.source)


def test_source_loader_executes_verified_bytes_without_reopening_or_pyc(tmp_path,monkeypatch):
    f=fixture_authority(tmp_path);proof=f.verifier.verify(**f.args);_,payload=f.verifier.claim(proof,**f.args,binding_fd=4)
    item=json.loads(payload)['mapping'][gate.HOST_MODULE];path=Path(item['path'])
    original=gate.read_source
    def replace_after_read(path,pin):
        data=original(path,pin);path.write_text('ANSWER=99\n');return data
    monkeypatch.setattr(gate,'read_source',replace_after_read)
    module=ModuleType('fake_host');gate._SourceLoader(item).exec_module(module)
    assert module.ANSWER==7 and module.__cached__ is None
    assert not list(path.parent.glob('__pycache__/*'))
    with pytest.raises(gate.HostLaunchError):gate._SourceLoader(item).exec_module(ModuleType('changed'))


def test_mapping_ignores_cwd_site_editable_and_alternate_loaders(tmp_path):
    f=fixture_authority(tmp_path);proof=f.verifier.verify(**f.args);_,payload=f.verifier.claim(proof,**f.args,binding_fd=4)
    finder=gate.MappedImports(json.loads(payload)['mapping'])
    spec=finder.find_spec('astrid.core.execution.generic_host',path=['/cwd/shadow','/site-packages'])
    assert spec.origin==str(f.source/'astrid/core/execution/generic_host.py')
    with pytest.raises(ModuleNotFoundError):finder.find_spec('editable_fake')
    with pytest.raises(ModuleNotFoundError):finder.find_spec('namespace_fake')
    assert finder.find_spec('sys').origin=='built-in'


def test_native_extensions_require_protected_runtime_inventory(tmp_path):
    f=fixture_authority(tmp_path);source_inv=next(i for i in f.record['inventories'].values() if i['root']==str(f.source))
    suffix=gate.importlib.machinery.EXTENSION_SUFFIXES[0];p=f.source/('fake'+suffix);p.write_bytes(b'NOT EXECUTABLE')
    source_inv['files'][p.name]=hashlib.sha256(p.read_bytes()).hexdigest()
    old=next(k for k,v in f.record['inventories'].items() if v is source_inv);new=gate.raw_digest(source_inv)
    f.record['inventories'][new]=f.record['inventories'].pop(old);f.record['import_binding']['import_roots'][0]['inventory_digest']=new
    with pytest.raises(gate.HostLaunchError,match='native dependency'):f.verifier.verify(**f.args)


def test_nine_component_measurement_parity_without_importing_astrid(tmp_path):
    f=fixture_authority(tmp_path)
    host=Path(__file__).resolve().parents[2]/'Astrid--integration/astrid/core/execution/generic_host.py'
    tree=ast.parse(host.read_bytes());names={'_canonical_digest','_source_digest','source_checkout_closure'}
    nodes=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names]
    # Only measurement functions, not any host package/module import or startup.
    module=ast.Module(body=[ast.ImportFrom(module='__future__',names=[ast.alias(name='annotations')],level=0),*nodes],type_ignores=[])
    ns={'Path':Path,'hashlib':hashlib,'json':json};exec(compile(ast.fix_missing_locations(module),str(host),'exec'),ns)
    assert gate.source_checkout_closure(f.source)==ns['source_checkout_closure'](f.source)


def test_wrong_kernel_interpreter_pin_and_namespace_mapping_fail(tmp_path):
    f=fixture_authority(tmp_path)
    f.args['preparation']['profile'].update(host_os_executable=str(f.runtime/'bin/python'),host_os_artifact_digest='sha256:'+'0'*64)
    f.record['selected_profile_digest']=gate.raw_digest(f.args['preparation']['profile'])
    with pytest.raises(gate.HostLaunchError,match='kernel interpreter pin'):f.verifier.verify(**f.args)
    f=fixture_authority(tmp_path/'second')
    source=next(v for v in f.record['inventories'].values() if v['root']==str(f.source))
    (f.source/'namespace').mkdir();(f.source/'namespace/child.py').write_text('')
    source['files']['namespace/child.py']=hashlib.sha256(b'').hexdigest()
    old=next(k for k,v in f.record['inventories'].items() if v is source);new=gate.raw_digest(source)
    f.record['inventories'][new]=f.record['inventories'].pop(old);f.record['import_binding']['import_roots'][0]['inventory_digest']=new
    with pytest.raises(gate.HostLaunchError,match='namespace'):f.verifier.verify(**f.args)


def test_duplicate_import_roots_and_declared_bytecode_are_unsupported(tmp_path):
    f=fixture_authority(tmp_path);f.record['import_binding']['import_roots'].append(dict(f.record['import_binding']['import_roots'][0]))
    with pytest.raises(gate.HostLaunchError,match='duplicate'):f.verifier.verify(**f.args)
    f=fixture_authority(tmp_path/'second');inv=next(v for v in f.record['inventories'].values() if v['root']==str(f.source))
    path=f.source/'module.pyc';path.write_bytes(b'fake');inv['files']['module.pyc']=hashlib.sha256(b'fake').hexdigest()
    old=next(k for k,v in f.record['inventories'].items() if v is inv);new=gate.raw_digest(inv)
    f.record['inventories'][new]=f.record['inventories'].pop(old);f.record['import_binding']['import_roots'][0]['inventory_digest']=new
    with pytest.raises(gate.HostLaunchError,match='representation'):f.verifier.verify(**f.args)


def local_fixture(tmp_path):
    f = fixture_authority(tmp_path)
    f.record['import_binding']['mode'] = gate.TRUSTED_LOCAL_MODE
    f.verifier = gate.TrustedLocalHostLaunchVerifier(installed_release=f.record)
    return f


def test_trusted_local_explicit_constructor_keeps_default_closed_and_record_private(tmp_path):
    f = local_fixture(tmp_path)
    # Mutating the caller's record cannot replace the retained selected release.
    f.record['source_components'][0]['sha256'] = '0' * 64
    proof = f.verifier.verify(**f.args)
    argv, data = f.verifier.claim(proof, **f.args, binding_fd=9)
    assert argv[1:3] == ['-I', '-S']
    assert json.loads(data)['mode'] == gate.TRUSTED_LOCAL_MODE
    with pytest.raises(gate.HostLaunchError): gate.HostLaunchVerifier().verify(**f.args)
    with pytest.raises(TypeError): pickle.dumps(proof)
    with pytest.raises(gate.HostLaunchError): f.verifier.claim(proof, **f.args, binding_fd=9)
    child = SimpleNamespace(pid=41); identity = {'pid':41, 'birth_id':'observed-local-child'}
    assert f.verifier.bind_child(proof, child=child, identity=identity) == gate.CURRENT_ROLES_VERSION
    f.verifier.verify_child(proof, child=child, identity=identity)
    with pytest.raises(gate.HostLaunchError):
        f.verifier.verify_child(proof, child=SimpleNamespace(pid=41), identity=identity)


@pytest.mark.parametrize('edge', ['profile', 'release', 'component', 'inventory', 'launcher', 'source', 'interpreter', 'environment'])
def test_trusted_local_mismatch_before_claim_and_spawn(tmp_path, edge):
    f = local_fixture(tmp_path)
    if edge == 'profile': f.args['preparation']['profile']['profile_id'] = 'foreign'
    if edge == 'release': f.args['preparation']['profile']['release_digest'] = 'sha256:' + '0'*64
    if edge == 'component': (f.source/'astrid/version.py').write_text('changed')
    if edge == 'inventory': (f.source/'unexpected.py').write_text('changed')
    if edge == 'launcher': f.launcher.write_text('changed')
    if edge == 'source': (f.source/'astrid/core/execution/generic_host.py').write_text('changed')
    if edge == 'interpreter': (f.runtime/'bin/python').write_bytes(b'changed')
    if edge == 'environment': f.args['environment']['PYTHONPATH'] = '/task-override'
    with pytest.raises(gate.HostLaunchError): f.verifier.verify(**f.args)
    assert not f.verifier._issued


def test_trusted_local_measures_installed_bytecode_ignores_it_and_maps_native_dependency(tmp_path):
    f = fixture_authority(tmp_path)
    site = tmp_path/'site'; site.mkdir()
    suffix = gate.importlib.machinery.EXTENSION_SUFFIXES[0]
    (site/('fake_native'+suffix)).write_bytes(b'FAKE NOT LOADED')
    (site/'namespace').mkdir(); (site/'namespace/child.py').write_text('ANSWER=1')
    (site/'__pycache__').mkdir(); (site/'__pycache__/ignored.pyc').write_bytes(b'NOT LOADED')
    inv = gate.installed_inventory(site); pin = gate.raw_digest(inv)
    assert list(inv['files']) == ['fake_native'+suffix, 'namespace/child.py']
    f.record['inventories'][pin] = inv
    f.record['import_binding']['import_roots'].append({'path':str(site), 'inventory_digest':pin})
    f.record['import_binding']['mode'] = gate.TRUSTED_LOCAL_MODE
    local = gate.TrustedLocalHostLaunchVerifier(installed_release=f.record)
    proof = local.verify(**f.args); _, data = local.claim(proof, **f.args, binding_fd=8)
    mapping = json.loads(data)['mapping']
    assert mapping['fake_native']['kind'] == 'extension'
    assert mapping['namespace']['kind'] == 'namespace'
    finder = gate.MappedImports(mapping, trusted_local=True)
    assert finder.find_spec('namespace').submodule_search_locations == [str(site/'namespace')]
    with pytest.raises(ModuleNotFoundError): finder.find_spec('unrecorded_module')
    f.record['import_binding']['mode'] = gate.MODE
    strong = gate.HostLaunchVerifier(authority_resolver=lambda _:f.record, protected_materialization=lambda _:f.lease)
    with pytest.raises(gate.HostLaunchError): strong.verify(**f.args)


def test_trusted_local_recorded_python_alias_does_not_claim_tamper_protection(tmp_path):
    f = fixture_authority(tmp_path)
    alias = tmp_path/'venv-python'; alias.symlink_to(f.runtime/'bin/python')
    f.args['preparation']['profile']['host_executable'] = str(alias)
    f.args['host_argv'][0] = str(alias)
    f.record['selected_profile_digest'] = gate.raw_digest(f.args['preparation']['profile'])
    f.record['import_binding']['mode'] = gate.TRUSTED_LOCAL_MODE
    local = gate.TrustedLocalHostLaunchVerifier(installed_release=f.record)
    proof = local.verify(**f.args); local.claim(proof, **f.args, binding_fd=8)
    # Observed changes fail; this does not assert that an attacker cannot race
    # an observation, startup or native extension loader between these checks.
    alias.unlink(); alias.write_bytes(b'other interpreter')
    with pytest.raises(gate.HostLaunchError):
        local.bind_child(proof, child=SimpleNamespace(pid=4), identity={'pid':4,'birth_id':'real-retained-fake'})
    with pytest.raises(gate.HostLaunchError):
        local.bind_child(proof, child=SimpleNamespace(pid=4), identity={'pid':4,'birth_id':'real-retained-fake'})


def test_trusted_local_verified_source_bytes_and_recorded_namespace_only(tmp_path, monkeypatch):
    f=local_fixture(tmp_path); proof=f.verifier.verify(**f.args)
    _, data=f.verifier.claim(proof, **f.args, binding_fd=3)
    item=json.loads(data)['mapping'][gate.HOST_MODULE]
    original=gate._local_read
    def replace_after_read(path, pin):
        data=original(path, pin); Path(path).write_text('ANSWER=99'); return data
    monkeypatch.setattr(gate, '_local_read', replace_after_read)
    module=ModuleType('fake_host'); gate._SourceLoader(item, trusted_local=True).exec_module(module)
    assert module.ANSWER == 7 and module.__cached__ is None


def test_trusted_local_alias_targets_are_retained_without_directory_import_discovery(tmp_path):
    root=tmp_path/'installed';root.mkdir();target=tmp_path/'ambient';target.mkdir()
    (target/'shadow.py').write_text('NOT_SELECTED=1')
    (root/'selected.py').write_text('SELECTED=1')
    (root/'site-packages').symlink_to(target,target_is_directory=True)
    inv=gate.installed_inventory(root)
    assert inv['aliases']['site-packages']=={'target':str(target),'kind':'directory'}
    assert 'site-packages/shadow.py' not in inv['files']
    assert gate._local_inventory(inv)==inv
    other=tmp_path/'other';other.mkdir();(root/'site-packages').unlink();(root/'site-packages').symlink_to(other,target_is_directory=True)
    with pytest.raises(gate.HostLaunchError,match='unexpected'):
        gate._local_inventory(inv)


def test_trusted_local_namespace_cannot_fall_back_to_stale_installed_astrid(tmp_path):
    f=fixture_authority(tmp_path);site=tmp_path/'site';(site/'astrid/core').mkdir(parents=True)
    (site/'astrid/__init__.py').write_text('STALE=1')
    (site/'astrid/core/extra.py').write_text('STALE=1')
    inv=gate.installed_inventory(site);pin=gate.raw_digest(inv)
    f.record['inventories'][pin]=inv;f.record['import_binding']['mode']=gate.TRUSTED_LOCAL_MODE
    f.record['import_binding']['import_roots'].append({'path':str(site),'inventory_digest':pin})
    local=gate.TrustedLocalHostLaunchVerifier(installed_release=f.record)
    proof=local.verify(**f.args);_,data=local.claim(proof,**f.args,binding_fd=3)
    mapping=json.loads(data)['mapping']
    assert mapping['astrid']['path']==str(f.source/'astrid/__init__.py')
    assert 'astrid.core.extra' not in mapping


def test_trusted_local_standard_resources_use_selected_package_only(tmp_path):
    import importlib.resources
    f=fixture_authority(tmp_path)
    data=f.source/'astrid/selected.json'; data.write_text('{"selected":true}')
    root=f.record['import_binding']['import_roots'][0]
    inv=gate.installed_inventory(f.source); pin=gate.raw_digest(inv)
    f.record['inventories'].pop(root['inventory_digest']); f.record['inventories'][pin]=inv
    root['inventory_digest']=pin; f.record['import_binding']['mode']=gate.TRUSTED_LOCAL_MODE
    local=gate.TrustedLocalHostLaunchVerifier(installed_release=f.record)
    proof=local.verify(**f.args); _,payload=local.claim(proof,**f.args,binding_fd=8)
    mapping=json.loads(payload)['mapping']; spec=gate.MappedImports(mapping,trusted_local=True).find_spec('astrid')
    package=ModuleType('astrid'); package.__spec__=spec
    resources=importlib.resources.files(package)
    assert resources==f.source/'astrid'
    assert json.loads(resources.joinpath('selected.json').read_text())=={'selected':True}
    # Exact installed data remains part of the existing before-issue check.
    data.write_text('{"changed":true}')
    with pytest.raises(gate.HostLaunchError):local.verify(**f.args)


def test_resource_reader_keeps_strict_and_nonpackage_behavior_closed(tmp_path):
    p=tmp_path/'module.py'; p.write_text('')
    item={'path':str(p),'sha256':hashlib.sha256(b'').hexdigest(),'package':True,'kind':'source'}
    assert gate._SourceLoader(item).get_resource_reader('fake') is None
    assert gate._SourceLoader({**item,'package':False},trusted_local=True).get_resource_reader('fake') is None
