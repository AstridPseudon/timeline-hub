"""Fake/offline G1b vectors; no selected interpreter, host or kernel launch."""
import ast
import copy
import hashlib
import importlib.util
import json
import os
import re
from pathlib import Path
import pickle
import sys
import subprocess
import sysconfig
from types import ModuleType, SimpleNamespace

import pytest
from runtime_protocol import verified_host_launch as gate


@pytest.fixture(scope='module')
def selected_action_installation(tmp_path_factory):
    """Exact retained action artifacts plus receiver source in offline fixtures.

    No install/profile/service is produced. Product RECORDs describe only these
    test copies; dependency RECORDs retain their original exact identities.
    """
    import shutil
    from test_selected_python_inventory import write_host_records
    source = os.environ.get('HOST_LAUNCH_TEST_ASTRID_SOURCE')
    provenance_path = os.environ.get('ACTION_CLOSURE_TEST_PROVENANCE')
    if not source or not provenance_path:
        pytest.skip('select admitted SDK and retained action artifact binding')
    source = Path(source); provenance = json.loads(Path(provenance_path).read_text())
    root = tmp_path_factory.mktemp('selected-action')/'site'; root.mkdir()
    def product_ignore(directory, names):
        ignored = {n for n in names if n == '__pycache__' or n.endswith(('.pyc','.pyo'))}
        if Path(directory) == source/'astrid/packs':
            ignored.update(n for n in names if n not in {'generation','__init__.py'})
        return ignored
    for name in ('astrid','banodoco_workspace_client','schemas'):
        shutil.copytree(source/name, root/name, ignore=product_ignore)
    runtime = Path(__file__).parents[1]
    for name in ('runtime_protocol','banodoco_local'):
        shutil.copytree(runtime/name, root/name, ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
    artifact_root = Path(provenance['artifact_source']['root'])
    action_names = {re.sub(r'[-_.]+','-',d['distribution_name']).lower():d for d in provenance['artifact_source']['distributions']}
    dependency_names = set(gate.HOST_DISTRIBUTIONS)-{'astrid','banodoco-workspace-runtime'} | set(action_names)
    records = {}
    for name in sorted(dependency_names):
        distribution = importlib.metadata.distribution(name)
        origin = Path(distribution.locate_file(''))
        if name in action_names:
            expected = action_names[name]
            assert origin == artifact_root
            assert distribution.version == expected['version']
            record = origin/next(p for p in distribution.files if str(p).endswith('.dist-info/RECORD'))
            assert hashlib.sha256(record.read_bytes()).hexdigest() == expected['record_sha256']
        for relative in distribution.files:
            if '..' in relative.parts or '__pycache__' in relative.parts or relative.suffix in {'.pyc','.pyo'}:
                continue
            path = origin/relative
            assert path.is_file() and not path.is_symlink()
            target = root/relative; target.parent.mkdir(parents=True, exist_ok=True)
            if target.exists(): assert target.read_bytes() == path.read_bytes()
            else: shutil.copyfile(path,target)
        records[name] = {'version':distribution.version,'origin':str(origin)}
    # Retain exact third-party RECORDs; write wheel-shaped product records only.
    # The shared helper also preserves bytes of existing third-party RECORDs
    # by using a temporary narrowed product table for these two source copies.
    original = gate.HOST_DISTRIBUTIONS
    gate.HOST_DISTRIBUTIONS = {n:original[n] for n in ('astrid','banodoco-workspace-runtime')}
    try: write_host_records(root)
    finally: gate.HOST_DISTRIBUTIONS = original
    matrix = root.parent/'capabilities.json'
    matrix.write_bytes((source/'config/astrid-beta-capabilities.json').read_bytes())
    actions = gate.qualify_action_closures(root, ['generation.generate_speech'], matrix)
    closure = gate.installed_host_closure(root, action_closures=actions)
    layout = gate.selected_python_layout(root)
    # Only stdlib and extension inventories are needed by this cold child.
    inventories = {gate.raw_digest(v):v for role in ('python-stdlib','python-extensions')
                   for v in [gate.installed_inventory(layout['roots'][role],python_role=role,selected_source=root)]}
    host_inventory = {'root':str(root),'files':closure['files']}
    identity = gate.raw_digest(host_inventory); inventories[identity]=host_inventory
    entries = [{'path':str(root),'inventory_digest':identity}]
    entries += [{'path':v['root'],'inventory_digest':pin} for pin,v in inventories.items() if pin != identity]
    mapping = gate._mapping(entries,inventories,host_inventory,trusted_local=True)
    launcher = runtime/'runtime_protocol/verified_host_launch.py'
    retained = {'actions':actions,'profile_digest':'a'*64,'host_files':closure['files'],
        'source_root':str(root),'mapping':mapping,'distribution_metadata':gate._distribution_metadata(entries,inventories),
        'selected_python':layout,'launcher':{'path':str(launcher),'sha256':hashlib.sha256(launcher.read_bytes()).hexdigest()}}
    selection = actions['generation.generate_speech']
    context = {'profile_digest':retained['profile_digest'],'owner':{'pid':123,'uid':os.getuid(),'birth_id':'owner'},
        'owner_epoch':'epoch','generation':1,'operation_id':'prepare','channel_id':'channel','task_id':'task',
        'attempt_id':'attempt','lease_id':'lease','fence':1,'runtime_epoch':1,'operation':selection['action_id'],
        'executor_id':'host','capability_digest':selection['capability_digest'],'closure_digest':selection['digest']}
    (root.parent/'provenance.json').write_text(json.dumps({'artifacts':records,'selection':selection,'host_distributions':closure['distributions']},sort_keys=True,indent=2)+'\n')
    return SimpleNamespace(root=root,actions=actions,closure=closure,retained=retained,context=context,matrix=matrix)


def test_selected_action_exact_union_does_not_expand_host_mapping(selected_action_installation):
    f = selected_action_installation
    assert set(f.actions['generation.generate_speech']['distributions']) == {
        'edge-tts','aiohttp','aiohappyeyeballs','aiosignal','attrs','certifi','frozenlist',
        'multidict','propcache','tabulate','typing-extensions','yarl','idna'}
    assert set(f.closure['distributions']) == set(gate.HOST_DISTRIBUTIONS)
    assert 'edge_tts' not in f.retained['mapping']
    with pytest.raises(ModuleNotFoundError): gate.MappedImports(f.retained['mapping']).find_spec('edge_tts')
    before = dict(sys.modules)
    payload = gate.prepare_action_binding(f.retained,action_id='generation.generate_speech',context=f.context,network_environment={})
    assert payload['mapping']['edge_tts']['path'] == str(f.root/'edge_tts/__init__.py')
    assert 'astrid.packs.rendering' not in payload['mapping']
    assert all(sys.modules.get(name) is module for name,module in before.items())
    assert 'edge_tts' not in sys.modules
    assert 'certifi/cacert.pem' in f.actions['generation.generate_speech']['distributions']['certifi']['files']
    assert any(path.endswith(tuple(gate.importlib.machinery.EXTENSION_SUFFIXES)) for path in f.actions['generation.generate_speech']['distributions']['multidict']['files'])


@pytest.mark.parametrize('field', sorted(gate.ACTION_CONTEXT_FIELDS))
def test_selected_action_context_cannot_change(selected_action_installation,field):
    f = selected_action_installation; context = copy.deepcopy(f.context)
    context[field] = None
    with pytest.raises((gate.HostLaunchError,TypeError,KeyError)):
        gate.prepare_action_binding(f.retained,action_id='generation.generate_speech',context=context,network_environment={})


def test_selected_action_cannot_select_another_actions_closure(selected_action_installation):
    f = selected_action_installation
    with pytest.raises(gate.HostLaunchError,match='no selected'):
        gate.prepare_action_binding(f.retained,action_id='generation.generate_video',context=f.context,network_environment={})


@pytest.mark.parametrize('edge', ['record','resource','native','version','missing-transitive','undeclared','shared-conflict',
    'pack','entrypoint','declaration','capability-matrix','interpreter','origin','missing-record-coverage'])
def test_selected_action_install_union_refuses_drift(selected_action_installation,tmp_path,edge):
    import shutil
    f = selected_action_installation
    root = tmp_path/'site'
    # Independent writable copies; the immutable module fixture is never edited.
    shutil.copytree(f.root,root)
    matrix=tmp_path/'matrix.json';matrix.write_bytes(f.matrix.read_bytes())
    actions = gate.qualify_action_closures(root,['generation.generate_speech'],matrix)
    binding = actions['generation.generate_speech']
    if edge == 'record':
        identity=binding['distributions']['edge-tts']; (Path(identity['origin'])/'RECORD').write_text('changed')
    elif edge == 'resource': (root/'certifi/cacert.pem').write_text('changed')
    elif edge == 'native':
        native=next(p for p in binding['distributions']['multidict']['files'] if p.endswith(tuple(gate.importlib.machinery.EXTENSION_SUFFIXES)))
        (root/native).write_bytes(b'changed')
    elif edge == 'version':
        path=Path(binding['distributions']['edge-tts']['origin'])/'METADATA'; path.write_text(path.read_text().replace('7.2.8','7.2.9'))
    elif edge == 'missing-transitive': shutil.rmtree(root/'yarl')
    elif edge == 'undeclared': (root/'certifi/foreign-resource.bin').write_bytes(b'undeclared')
    elif edge == 'shared-conflict':
        binding['distributions']['attrs']['version']='0.0'
        binding['digest']=gate.raw_digest({k:v for k,v in binding.items() if k!='digest'})
    elif edge == 'pack':
        path=root/'astrid/packs/generation/pack.yaml';path.write_text(path.read_text()+'\n')
    elif edge == 'entrypoint':(root/'astrid/packs/generation/actions/generate_speech/run.py').write_text('raise AssertionError("substitution")')
    elif edge == 'capability-matrix':matrix.write_text(matrix.read_text()+'\n')
    elif edge == 'missing-record-coverage':
        path=Path(binding['distributions']['certifi']['origin'])/'RECORD'
        path.write_text('\n'.join(line for line in path.read_text().splitlines() if not line.startswith('certifi/cacert.pem,'))+'\n')
    else:
        if edge == 'declaration':binding['declaration']['python']=['edge-tts==0']
        elif edge == 'interpreter':binding['interpreter']['sha256']='0'*64
        elif edge == 'origin':binding['distributions']['attrs']['origin']=str(tmp_path/'ambient/attrs.dist-info')
        binding['digest']=gate.raw_digest({k:v for k,v in binding.items() if k!='digest'})
    with pytest.raises((gate.HostLaunchError,FileNotFoundError)):
        gate.installed_host_closure(root,action_closures=actions)


def test_selected_action_cold_real_module_imports_metadata_resources_and_native(selected_action_installation,tmp_path):
    f = selected_action_installation
    payload = gate.prepare_action_binding(f.retained,action_id='generation.generate_speech',context=f.context,network_environment={})
    path=tmp_path/'binding.json';path.write_bytes(gate.canonical(payload))
    (tmp_path/'edge_tts.py').write_text('raise AssertionError("ambient CWD imported")')
    (tmp_path/'sitecustomize.py').write_text('raise AssertionError("ambient site imported")')
    (tmp_path/'foreign.pth').write_text('import sitecustomize')
    program = r'''
import importlib.util,json,sys
spec=importlib.util.spec_from_file_location('cold_gate',sys.argv[1]);gate=importlib.util.module_from_spec(spec);spec.loader.exec_module(gate)
payload=json.load(open(sys.argv[2]))
assert not any(n in sys.modules for n in ('astrid','edge_tts','aiohttp','multidict'))
try:gate.launch_action_from_binding(payload,context_digest=payload['context_digest'],arguments=['--help'])
except SystemExit as exc:assert exc.code == 0
from pathlib import Path
from importlib.metadata import version
from importlib.resources import files
import edge_tts,aiohttp,multidict,frozenlist,propcache,yarl,certifi
from astrid.core.pack.canonical import validate_canonical_pack
from astrid.core.pack.discovery import discover_pack_metadata
from astrid.sdk.actions import validate_action_inputs_definition,action_executor_definition
from astrid.core.pack.discovery import DiscoveredPack
from astrid.core.pack.loader import load_pack_manifest
root=Path(payload['action']['pack_root']);pack=load_pack_manifest(root/'pack.yaml')
definition=action_executor_definition(DiscoveredPack(pack,'extra',0),'generate_speech',pack.actions['generate_speech'])
validate_action_inputs_definition(definition,dict(text='offline',provider='edge-tts',voice='en-US-ChristopherNeural',rate='+0%',volume='+0%',pitch='+0Hz'))
assert validate_canonical_pack(root).id == 'generation'
assert any(p.pack.id == 'generation' for p in discover_pack_metadata(project_root=root.parent,extra_pack_roots=(str(root),)))
assert version('edge-tts') == '7.2.8'
assert len(files('certifi').joinpath('cacert.pem').read_bytes()) > 1000
assert multidict.CIMultiDict({'A':'b'})['a']=='b'
assert frozenlist.FrozenList([1]) == [1]
for name in ('sitecustomize','pytest','astrid.packs.rendering','unselected_action'):
 try:__import__(name)
 except ModuleNotFoundError:pass
 else:raise AssertionError(name+' escaped child closure')
assert sys.path == []
print('SELECTED_ACTION_COLD_OK',edge_tts.__file__,version('aiohttp'))
'''
    child=subprocess.run([sys.executable,'-I','-S','-B','-c',program,gate.__file__,str(path)],cwd=tmp_path,
        env={'PATH':os.environ.get('PATH',''),'HOME':str(tmp_path),'PYTHONPATH':str(tmp_path)},capture_output=True,text=True)
    (tmp_path/'cold-output.json').write_text(json.dumps({'argv':child.args,'exit':child.returncode,'stdout':child.stdout,'stderr':child.stderr},indent=2)+'\n')
    assert child.returncode == 0, child.stderr
    assert 'SELECTED_ACTION_COLD_OK' in child.stdout


def test_selected_action_union_is_measurable_inside_unchanged_host_mapping(selected_action_installation,tmp_path):
    f=selected_action_installation
    path=tmp_path/'host-input.json';path.write_bytes(gate.canonical(f.retained))
    program=r'''
import importlib.util,json,sys
spec=importlib.util.spec_from_file_location('host_gate',sys.argv[1]);gate=importlib.util.module_from_spec(spec);spec.loader.exec_module(gate)
value=json.load(open(sys.argv[2]));finder=gate.MappedImports(value['mapping'],trusted_local=True)
sys.path[:]=[];sys.path_hooks[:]=[];sys.path_importer_cache.clear();sys.meta_path[:]=[finder]
finder._bind_distribution_metadata(value['distribution_metadata'])
from runtime_protocol.verified_host_launch import installed_host_closure,HOST_DISTRIBUTIONS
from importlib.metadata import version,PackageNotFoundError
closure=installed_host_closure(value['source_root'],action_closures=value['actions'])
assert set(closure['distributions'])==set(HOST_DISTRIBUTIONS)
try:version('edge-tts')
except PackageNotFoundError:pass
else:raise AssertionError('action metadata escaped Host mapping')
try:import edge_tts
except ModuleNotFoundError:pass
else:raise AssertionError('action code escaped Host mapping')
assert 'edge_tts' not in sys.modules
print('HOST_UNION_OBSERVATION_OK')
'''
    child=subprocess.run([sys.executable,'-I','-S','-B','-c',program,gate.__file__,str(path)],capture_output=True,text=True)
    assert child.returncode==0,child.stderr
    assert 'HOST_UNION_OBSERVATION_OK' in child.stdout


def test_selected_action_concurrent_children_cannot_import_each_others_dependencies(selected_action_installation,tmp_path):
    import base64,csv,io,shutil
    import yaml
    from test_selected_python_inventory import write_host_records
    f=selected_action_installation;root=tmp_path/'site';shutil.copytree(f.root,root)
    pack=root/'astrid/packs/isolated';(pack/'actions').mkdir(parents=True)
    for path in (pack/'__init__.py',pack/'actions/__init__.py'):path.write_text('')
    (pack/'actions/run.py').write_text("import other_action_dependency\ntry:\n import edge_tts\nexcept ModuleNotFoundError:pass\nelse:raise AssertionError('cross-child dependency')\nprint('ISOLATED_CHILD_OK')\n")
    declaration={'schema_version':3,'id':'isolated','name':'Offline isolated child','version':'1.0.0',
        'actions':{'probe':{'description':'Offline isolated child fixture','invocation':{'kind':'command','command':{'argv':['{python_exec}','-m','astrid.packs.isolated.actions.run']}},
        'inputs':[],'outputs':[],'metadata':{'execution_dependencies':{'python':['other-action-dependency==1.0']}},
        'resources':[{'kind':'implementation','path':'actions/run.py'}]}}}
    (pack/'pack.yaml').write_text(yaml.safe_dump(declaration))
    package=root/'other_action_dependency';package.mkdir();(package/'__init__.py').write_text('VALUE=42\n')
    info=root/'other_action_dependency-1.0.dist-info';info.mkdir();(info/'METADATA').write_text('Name: other-action-dependency\nVersion: 1.0\n')
    stream=io.StringIO(newline='');writer=csv.writer(stream)
    for path in [package/'__init__.py',info/'METADATA']:
        content=path.read_bytes();writer.writerow([str(path.relative_to(root)),
            'sha256='+base64.urlsafe_b64encode(hashlib.sha256(content).digest()).decode().rstrip('='),len(content)])
    writer.writerow([str(info.relative_to(root))+'/RECORD','','']);(info/'RECORD').write_bytes(stream.getvalue().encode())
    original=gate.HOST_DISTRIBUTIONS;gate.HOST_DISTRIBUTIONS={n:original[n] for n in ('astrid','banodoco-workspace-runtime')}
    try:write_host_records(root)
    finally:gate.HOST_DISTRIBUTIONS=original
    matrix=json.loads(f.matrix.read_text());matrix['capabilities'].append({'id':'isolated.probe','disposition':'optional',
        'evidence_reason':'Offline fixture only','adapter_family':'cpu','resource_keys':['cpu'],
        'required_env':[],'required_binaries':[],'required_packages':[]})
    path=tmp_path/'matrix.json';path.write_text(json.dumps(matrix))
    actions=gate.qualify_action_closures(root,['generation.generate_speech','isolated.probe'],path)
    host=gate.installed_host_closure(root,action_closures=actions)
    inventory={'root':str(root),'files':host['files']};pin=gate.raw_digest(inventory)
    mapping=gate._mapping([{'path':str(root),'inventory_digest':pin}],{pin:inventory},inventory,trusted_local=True)
    for name,item in f.retained['mapping'].items():
        if not Path(item['path']).is_relative_to(f.root):mapping[name]=item
    retained={**f.retained,'source_root':str(root),'host_files':host['files'],'actions':actions,'mapping':mapping,
        'distribution_metadata':gate._distribution_metadata([{'path':str(root),'inventory_digest':pin}],{pin:inventory})}
    payloads=[]
    for action_id in ('generation.generate_speech','isolated.probe'):
        selection=actions[action_id];context={**f.context,'operation':action_id,
            'capability_digest':selection['capability_digest'],'closure_digest':selection['digest']}
        payloads.append(gate.prepare_action_binding(retained,action_id=action_id,context=context,network_environment={}))
    assert 'other_action_dependency' not in payloads[0]['mapping']
    assert 'edge_tts' not in payloads[1]['mapping']
    children=[]
    for index,payload in enumerate(payloads):
        argv=[sys.executable,'-I','-S','-B',gate.__file__,'--action-binding-fd','0','--context-digest',payload['context_digest']]
        if index==0:argv.append('--help')
        children.append(subprocess.Popen(argv,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE))
    # Start both before observing either. Their stdio/mappings are independent.
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=2) as pool:
        jobs=[pool.submit(child.communicate,gate.canonical(payload)) for child,payload in zip(children,payloads)]
        results=[job.result() for job in jobs]
    assert [child.returncode for child in children]==[0,0],results
    assert b'ISOLATED_CHILD_OK' in results[1][0]
    assert 'edge_tts' not in sys.modules and 'other_action_dependency' not in sys.modules


def _metadata_binding(tmp_path):
    root=tmp_path/'installed';metadata=root/'astrid-7.2.dist-info'
    metadata.mkdir(parents=True)
    (metadata/'METADATA').write_text('Metadata-Version: 2.1\nName: astrid\nVersion: 7.2\n')
    (metadata/'top_level.txt').write_text('astrid\n')
    inventory=gate.installed_inventory(root);identity=gate.raw_digest(inventory)
    rows=gate._distribution_metadata([{'path':str(root),'inventory_digest':identity}],{identity:inventory})
    return root,metadata,rows


def test_mapped_distribution_metadata_real_version_with_empty_sys_path(tmp_path,monkeypatch):
    root,metadata,rows=_metadata_binding(tmp_path)
    finder=gate.MappedImports({},trusted_local=True,distribution_metadata=rows)
    monkeypatch.setattr(sys,'meta_path',[finder]);monkeypatch.setattr(sys,'path',[])
    assert gate.importlib.metadata.version('Astrid')=='7.2'
    source=Path(os.environ.get('HOST_LAUNCH_TEST_ASTRID_SOURCE', Path(__file__).parents[2]/'Astrid--integration-reconciled'))
    version_path=source/'astrid/version.py'
    item={'path':str(version_path),'sha256':hashlib.sha256(version_path.read_bytes()).hexdigest(),'package':False}
    selected_version=ModuleType('selected_version')
    gate._SourceLoader(item,trusted_local=True).exec_module(selected_version)
    assert selected_version.__version__=='7.2'
    assert gate.importlib.metadata.distribution('astrid').read_text('top_level.txt')=='astrid\n'
    with pytest.raises(gate.importlib.metadata.PackageNotFoundError):
        gate.importlib.metadata.version('unreviewed-distribution')
    candidates=list(finder.find_distributions(gate.importlib.metadata.DistributionFinder.Context(name='astrid',path=['/ambient'])))
    assert len(candidates)==1
    with pytest.raises(gate.HostLaunchError,match='outside'):
        candidates[0].locate_file('../outside')


@pytest.mark.parametrize('edge',['missing','changed','escape','duplicate','strict','null'])
def test_mapped_distribution_metadata_fails_closed(tmp_path,edge):
    root,metadata,rows=_metadata_binding(tmp_path)
    trusted=True
    if edge=='missing':(metadata/'METADATA').unlink()
    if edge=='changed':(metadata/'METADATA').write_text('Name: astrid\nVersion: forged\n')
    if edge=='escape':rows[0]['distributions'][0]['directory']='../astrid-7.2.dist-info'
    if edge=='duplicate':rows[0]['distributions']*=2
    if edge=='strict':trusted=False
    if edge=='null':rows={}
    with pytest.raises((gate.HostLaunchError,FileNotFoundError)):
        gate.MappedImports({},trusted_local=trusted,distribution_metadata=rows)


def test_mapped_distribution_metadata_cannot_fill_missing_selected_astrid_from_second_root(tmp_path):
    root,metadata,rows=_metadata_binding(tmp_path)
    selected=tmp_path/'selected';selected.mkdir();(selected/'selected.py').write_text('VALUE=1')
    inventories=[gate.installed_inventory(p) for p in [selected,root]]
    pins={gate.raw_digest(v):v for v in inventories}
    entries=[{'path':v['root'],'inventory_digest':gate.raw_digest(v)} for v in inventories]
    with pytest.raises(gate.HostLaunchError,match='outside the selected'):
        gate._distribution_metadata(entries,pins)


def test_mapped_distribution_metadata_is_emitted_from_reviewed_trusted_binding_only(tmp_path):
    f=local_fixture(tmp_path)
    metadata=f.source/'astrid-7.2.dist-info';metadata.mkdir()
    (metadata/'METADATA').write_text('Name: astrid\nVersion: 7.2\n')
    inventory=gate.installed_inventory(f.source);identity=gate.raw_digest(inventory)
    old=f.record['import_binding']['import_roots'][0]['inventory_digest']
    del f.record['inventories'][old]
    f.record['inventories'][identity]=inventory
    f.record['import_binding']['import_roots'][0]['inventory_digest']=identity
    verifier=gate.TrustedLocalHostLaunchVerifier(installed_release=f.record)
    proof=verifier.verify(**f.args);_,data=verifier.claim(proof,**f.args,binding_fd=3)
    body=json.loads(data)
    assert body['distribution_metadata'][0]['root']==str(f.source)
    assert body['distribution_metadata'][0]['files']['astrid-7.2.dist-info/METADATA']==inventory['files']['astrid-7.2.dist-info/METADATA']
    finder=gate.MappedImports(body['mapping'],trusted_local=True,distribution_metadata=body['distribution_metadata'])
    candidate=list(finder.find_distributions(gate.importlib.metadata.DistributionFinder.Context(name='astrid')))[0]
    assert candidate.version=='7.2'


@pytest.mark.parametrize("edge", ["valid", "unmapped-parser", "tampered-metadata"])
def test_cold_launch_binds_metadata_after_exact_importer_without_parser_preload(tmp_path, edge):
    # A fresh isolated interpreter exercises lazy stdlib imports; pytest's
    # already imported email modules cannot make this fixture pass.
    root, metadata, rows = _metadata_binding(tmp_path)
    files = {
        "astrid/__init__.py": "from importlib.metadata import version\n__version__=version('astrid')\n",
        "astrid/core/__init__.py": "",
        "astrid/core/execution/__init__.py": "",
        "astrid/core/execution/generic_host.py":
            "import sys\n"
            "from astrid.core.execution import generic_host as retained_host\n"
            "assert retained_host is sys.modules['__main__'], 'Host executed twice'\n"
            "assert retained_host._RETAINED_SELECTED_PYTHON is _RETAINED_SELECTED_PYTHON\n"
            "import astrid, email.parser, email.feedparser, email.policy\n"
            "from importlib.metadata import distribution\n"
            "assert distribution('astrid').read_text('top_level.txt')=='astrid\\n'\n"
            "print('COLD_MAPPED_METADATA:'+astrid.__version__)\n",
    }
    for relative, content in files.items():
        target = root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content)
    (root / 'unexecuted.pth').write_text('import sys; sys.exit("PTH EXECUTED")\n')
    ambient = tmp_path / 'ambient-cwd'
    ambient.mkdir()
    (ambient / 'email.py').write_text('raise RuntimeError("ambient shadow")\n')
    (ambient / 'sitecustomize.py').write_text('raise RuntimeError("ambient startup")\n')
    stdlib = Path(sysconfig.get_path("stdlib")).resolve()
    inventories = [gate.installed_inventory(root), gate.installed_inventory(stdlib, python_role='python-stdlib', selected_source=root)]
    pins = {gate.raw_digest(i): i for i in inventories}
    import_roots = [{"path": i["root"], "inventory_digest": gate.raw_digest(i)} for i in inventories]
    mapping = gate._mapping(import_roots, pins, inventories[1], trusted_local=True)
    if edge == "unmapped-parser":
        del mapping["email.parser"]
    if edge == "tampered-metadata":
        (metadata / "METADATA").write_text("Name: astrid\nVersion: forged\n")
    payload = {"schema_version": 1, "mode": gate.TRUSTED_LOCAL_MODE,
               "module": gate.HOST_MODULE, "mapping": mapping,
               "distribution_metadata": rows, "host_argv": [],
               "selected_python": gate.selected_python_layout(root)}
    manifest = tmp_path / "cold-binding.json"
    manifest.write_text(json.dumps(payload))
    program = """
import importlib.util,json,sys
spec=importlib.util.spec_from_file_location('cold_gate',sys.argv[1])
gate=importlib.util.module_from_spec(spec);spec.loader.exec_module(gate)
assert 'email.parser' not in sys.modules, 'parser unexpectedly preloaded'
with open(sys.argv[2]) as stream: payload=json.load(stream)
gate.launch_from_binding(payload)
"""
    result = subprocess.run([sys.executable, "-I", "-S", "-B", "-c", program, gate.__file__, str(manifest)],
                            cwd=ambient, env={**os.environ, 'PYTHONPATH':str(ambient),
                                'PYTHONUSERBASE':str(ambient), 'PYTHONSTARTUP':str(ambient/'sitecustomize.py')},
                            capture_output=True, text=True, timeout=30)
    if edge == "valid":
        assert result.returncode == 0, result.stderr
        assert result.stdout.strip() == "COLD_MAPPED_METADATA:7.2"
    else:
        assert result.returncode != 0
        assert "COLD_MAPPED_METADATA:" not in result.stdout
        if edge == "unmapped-parser":
            assert "outside the reviewed import mapping: email.parser" in result.stderr
        else:
            assert "HostLaunchError: import source differs from its reviewed pin" in result.stderr


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
    assert argv==[f.args['host_argv'][0],'-I','-S','-B',str(f.launcher),'--binding-fd','31']
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


@pytest.mark.parametrize('bytecode_flag', [True, False])
def test_claimed_cold_host_entry_disables_bytecode_before_schema_imports(tmp_path, bytecode_flag):
    """Execute the real descriptor entry, without a Host or native custody.

    The source-only fake authority selects this actual Runtime launcher. The
    fixture interpreter substitutes for its deliberately nonexecutable fake
    runtime; native interpreter/custody admission is not claimed by this test.
    """
    f = fixture_authority(tmp_path)
    host = f.source / 'astrid/core/execution/generic_host.py'
    host.write_text("import sys\n"
        "assert sys.flags.dont_write_bytecode == 1 and sys.dont_write_bytecode\n"
        "from banodoco_timeline_schema import generated, materialize, theme, validate\n"
        "print('COLD_SCHEMA_IMPORTS_WITH_EARLY_BYTECODE_SUPPRESSION')\n")
    schema = f.source / 'banodoco_timeline_schema'
    schema.mkdir()
    for name in ('__init__', 'generated', 'materialize', 'theme', 'validate'):
        (schema / (name + '.py')).write_text('VALUE = 1\n')
    runtime = next(value for value in f.record['inventories'].values()
                   if value['root'] == str(f.runtime))
    source = gate.installed_inventory(f.source)
    inventories = {gate.raw_digest(value): value for value in (source, runtime)}
    profile = f.args['preparation']['profile']
    protocol = {**profile['host_protocol'],
        'source_closure_digest': gate.source_checkout_closure(f.source)['digest']}
    profile.update(host_protocol=protocol)
    f.record.update(selected_profile_digest=gate.raw_digest(profile), host_protocol=protocol,
        source_components=gate.source_checkout_closure(f.source)['components'], inventories=inventories)
    launcher = Path(gate.__file__).resolve(strict=True)
    f.record['import_binding'].update(
        launcher={'path': str(launcher), 'sha256': hashlib.sha256(launcher.read_bytes()).hexdigest()},
        python_runtime_inventory_digest=gate.raw_digest(runtime),
        import_roots=[{'path': value['root'], 'inventory_digest': gate.raw_digest(value)}
                      for value in (source, runtime)])
    before = gate.installed_inventory(f.source)
    read_fd, write_fd = os.pipe()
    try:
        proof = f.verifier.verify(**f.args)
        argv, payload = f.verifier.claim(proof, **f.args, binding_fd=read_fd)
        assert argv[:4] == [f.args['host_argv'][0], '-I', '-S', '-B']
        if not bytecode_flag:
            argv.remove('-B')
        os.write(write_fd, payload)
        os.close(write_fd)
        write_fd = None
        result = subprocess.run([sys.executable, *argv[1:]], pass_fds=(read_fd,), cwd=tmp_path,
            env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'},
            capture_output=True, text=True, timeout=30)
    finally:
        os.close(read_fd)
        if write_fd is not None:
            os.close(write_fd)
    if bytecode_flag:
        assert result.returncode == 0, result.stderr
        assert result.stdout.strip() == 'COLD_SCHEMA_IMPORTS_WITH_EARLY_BYTECODE_SUPPRESSION'
    else:
        assert result.returncode != 0
        assert 'launcher requires the exact isolated binding descriptor mode' in result.stderr
        assert not result.stdout
    assert gate.installed_inventory(f.source) == before
    assert not list(schema.rglob('*.pyc'))


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
    source=Path(os.environ.get('HOST_LAUNCH_TEST_ASTRID_SOURCE', Path(__file__).resolve().parents[2]/'Astrid--integration'))
    host=source/'astrid/core/execution/generic_host.py'
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


@pytest.mark.parametrize('reader', [gate.read_source, gate._local_read])
def test_selected_import_file_keeps_64_mib_bound_before_read(tmp_path, monkeypatch, reader):
    oversized = tmp_path / 'selected.py'
    with oversized.open('wb') as stream:
        stream.truncate(64 * 1024 * 1024 + 1)
    assert gate.LIMIT == 67_108_864
    def unexpected_read(*args):
        pytest.fail('oversized selected file must be refused before reading bytes')
    monkeypatch.setattr(gate.os, 'read', unexpected_read)
    with pytest.raises(gate.HostLaunchError, match='bounded regular file'):
        reader(oversized, '0' * 64)


def test_trusted_local_selected_file_replacement_refuses_retained_pin(tmp_path):
    selected = tmp_path / 'selected.py'
    selected.write_bytes(b'VALUE=1\n')
    inventory = gate.installed_inventory(tmp_path)
    replacement = tmp_path / 'replacement'
    replacement.write_bytes(b'VALUE=2\n')
    replacement.replace(selected)
    with pytest.raises(gate.HostLaunchError, match='differs from its reviewed pin'):
        gate._local_inventory(inventory)


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


@pytest.mark.parametrize('namespace', ['astrid', 'banodoco_workspace_client', 'runtime_protocol', 'banodoco_local'])
def test_trusted_local_namespace_cannot_fall_back_to_stale_installed_astrid(tmp_path, namespace):
    f=fixture_authority(tmp_path);site=tmp_path/'site';(site/namespace/'core').mkdir(parents=True)
    (site/namespace/'__init__.py').write_text('STALE=1')
    (site/namespace/'core/extra.py').write_text('STALE=1')
    inv=gate.installed_inventory(site);pin=gate.raw_digest(inv)
    f.record['inventories'][pin]=inv;f.record['import_binding']['mode']=gate.TRUSTED_LOCAL_MODE
    f.record['import_binding']['import_roots'].append({'path':str(site),'inventory_digest':pin})
    local=gate.TrustedLocalHostLaunchVerifier(installed_release=f.record)
    proof=local.verify(**f.args);_,data=local.claim(proof,**f.args,binding_fd=3)
    mapping=json.loads(data)['mapping']
    assert mapping['astrid']['path']==str(f.source/'astrid/__init__.py')
    assert namespace+'.core.extra' not in mapping


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


def test_host_only_trusted_local_variant_still_requires_owner_record_and_original_child(tmp_path, monkeypatch):
    from test_selected_python_inventory import selected_case
    f=selected_case(tmp_path, monkeypatch)
    verifier=gate.TrustedLocalHostLaunchVerifier(installed_release=f.record)
    proof=verifier.verify(**f.args)
    argv,payload=verifier.claim(proof,**f.args,binding_fd=31)
    assert isinstance(payload,bytes) and gate.canonical(json.loads(payload))==payload
    child=SimpleNamespace(pid=42);identity={'pid':42,'uid':501,'birth_id':'original'}
    verifier.bind_child(proof,child=child,identity=identity)
    verifier.verify_child(proof,child=child,identity=identity)
    with pytest.raises(gate.HostLaunchError):
        verifier.verify_child(proof,child=SimpleNamespace(pid=42),identity=identity)


def host_only_environment_fixture(tmp_path):
    f=fixture_authority(tmp_path)
    profile=f.args['preparation']['profile']
    profile.update(execution_mode='host_only_cpu',support_root=f.args['config']['support_root'],realm_root=str(tmp_path/'realm'))
    f.args['environment'].update(ASTRID_OUTPUT_ROOT=str(tmp_path/'support/host-output'),BANODOCO_LOCAL_DATA_ROOT=str(tmp_path/'realm'))
    f.record['selected_profile_digest']=gate.raw_digest(profile)
    f.record['import_binding']['mode']=gate.TRUSTED_LOCAL_MODE
    f.verifier=gate.TrustedLocalHostLaunchVerifier(installed_release=f.record)
    return f


@pytest.mark.parametrize('edge',['output','realm','missing','config','PYTHONPATH','PYTHONDONTWRITEBYTECODE','BANODOCO_RUNTIME_OWNER_TOKEN'])
def test_host_only_environment_rejects_unadmitted_roots_and_ambient_before_inventory(tmp_path,monkeypatch,edge):
    f=host_only_environment_fixture(tmp_path)
    if edge=='output': f.args['environment']['ASTRID_OUTPUT_ROOT']=str(tmp_path/'other')
    elif edge=='realm': f.args['environment']['BANODOCO_LOCAL_DATA_ROOT']=str(tmp_path/'other')
    elif edge=='missing': del f.args['environment']['ASTRID_OUTPUT_ROOT']
    elif edge=='config': f.args['config']['support_root']=str(tmp_path/'other')
    else: f.args['environment'][edge]='/ambient'
    observed=[]
    monkeypatch.setattr(f.verifier,'_inventory',lambda value:observed.append(value))
    with pytest.raises(gate.HostLaunchError,match='environment'):
        f.verifier.verify(**f.args)
    assert observed==[]


def test_strict_provider_does_not_admit_host_only_product_roots(tmp_path,monkeypatch):
    f=host_only_environment_fixture(tmp_path)
    f.record['import_binding']['mode']=gate.MODE
    verifier=gate.HostLaunchVerifier(authority_resolver=lambda _:copy.deepcopy(f.record),protected_materialization=lambda _:f.lease)
    observed=[]
    monkeypatch.setattr(verifier,'_inventory',lambda value:observed.append(value))
    with pytest.raises(gate.HostLaunchError,match='environment'):
        verifier.verify(**f.args)
    assert observed==[]


def test_host_only_environment_validates_selected_release_before_accepting_roots(tmp_path,monkeypatch):
    f=host_only_environment_fixture(tmp_path)
    f.args['preparation']['profile']['release_digest']='sha256:'+'f'*64
    observed=[]
    monkeypatch.setattr(f.verifier,'_inventory',lambda value:observed.append(value))
    with pytest.raises(gate.HostLaunchError,match='release differs'):
        f.verifier.verify(**f.args)
    assert observed==[]
