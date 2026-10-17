"""Trusted closure binding over disposable package/receipt bytes only."""
import hashlib
import json
import sys
from pathlib import Path

import pytest

from astrid.core.execution import remotion_closure as closure
from astrid.core.execution import remotion_host_session as host


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def test_inventory_keeps_hidden_and_linked_files_without_traversing_directory_links(tmp_path):
    root = tmp_path / 'root'; root.mkdir()
    hidden = root / '.hidden'; hidden.mkdir()
    first = root / 'file'; first.write_text('one')
    second = hidden / 'file'; second.write_text('two')
    alias = root / 'file-alias'; alias.symlink_to(first)
    (root / 'broken').symlink_to(root / 'missing')
    (hidden / 'cycle').symlink_to(root, target_is_directory=True)
    outside = tmp_path / 'outside'; outside.mkdir()
    (outside / 'unselected').write_text('outside')
    (root / 'directory-alias').symlink_to(outside, target_is_directory=True)
    assert set(closure._tree_files(root)) == {first, second, alias}


@pytest.mark.parametrize('change', ['bytes','added','removed','escape'])
def test_root_config_import_helpers_are_in_the_selected_closure(roots,tmp_path,change):
    project,_,_,args=roots
    helper=project/'webpack-alias.mjs';helper.write_text('// selected helper')
    binding=closure.RemotionClosureBinding.admit(**args)
    assert dict(binding.files).get(helper)==sha(helper)
    if change=='bytes':helper.write_text('// changed helper')
    elif change=='added':(project/'new-helper.mjs').write_text('// unadmitted helper')
    elif change=='removed':helper.unlink()
    else:
        outside=tmp_path/'outside.mjs';outside.write_text('// selected helper')
        helper.unlink();helper.symlink_to(outside)
    with pytest.raises(ValueError,match='changed|escaping'):
        binding.validate(project)


@pytest.fixture
def roots(tmp_path,monkeypatch):
    (tmp_path/'artifact-scratch').mkdir()
    project=tmp_path/'selected';installed=tmp_path/'installed';project.mkdir();installed.mkdir()
    modules=installed/'node_modules';modules.mkdir()
    versions={f'node_modules/{name}':'4.0.509' for name in ('remotion','@remotion/renderer','@remotion/cli','@remotion/bundler')}
    lock={'packages':{name:{'version':v,'integrity':'fixture-sri'} for name,v in versions.items()}}
    for root in (project,installed):
        (root/'package.json').write_text('{"name":"fixture"}')
        (root/'package-lock.json').write_text(json.dumps(lock))
    for name,v in versions.items():
        path=installed/name/'package.json';path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps({'version':v}))
    patches={}
    for name in closure._PATCHES:
        path=modules/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_text('disposable patched '+name);patches[name]=sha(path)
    monkeypatch.setattr(closure,'_PATCHES',patches)
    cli=modules/'@remotion/cli/remotion-cli.js';cli.write_text('// disposable CLI')
    source=project/'vendor/timeline-composition';source.mkdir(parents=True);(source/'evaluation.ts').write_text('pure-source-fixture')
    packed=modules/'@banodoco/timeline-composition';packed.mkdir(parents=True);(packed/'evaluation.ts').write_text('pure-source-fixture')
    (project/'src').mkdir();(project/'src/astrid-frame-worker.mjs').write_text('// fixture helper')
    (project/'node_modules').symlink_to(modules,target_is_directory=True)
    report={'passed':True,'issues':[],'installed_sri_missing':[],'installed_sri_bad':[],
            'source':{'manifest_sha256':sha(project/'package.json'),'lock_sha256':sha(project/'package-lock.json')},
            'counts':{'lock_sri_records_bad':0,'lock_sri_records_missing_or_unverified':0},'versions':versions}
    receipt=tmp_path/'verified.json';receipt.write_text(json.dumps(report))
    args=dict(project=project,installed_project=installed,verification_receipt=receipt,receipt_sha256=sha(receipt),
              manifest_sha256=sha(project/'package.json'),lock_sha256=sha(project/'package-lock.json'))
    return project,installed,receipt,args


def test_exact_admitted_install_link_binds_lexical_cli_and_source(roots,monkeypatch,tmp_path):
    project,installed,receipt,args=roots
    binding=closure.RemotionClosureBinding.admit(**args)
    assert binding.validate(project)==installed/'node_modules/@remotion/cli/remotion-cli.js'
    monkeypatch.setattr(host,'_host_browser_executable',lambda:None)
    owner=host.HostRemotionSession(track=lambda p:None,untrack=lambda p:None,closure_binding=binding)
    lease=owner.lease({'ASTRID_REMOTION_PROJECT_DIR':str(project),'ASTRID_NODE_EXECUTABLE':str(Path(sys.executable).resolve())},attempt=tmp_path, scratch=tmp_path/'artifact-scratch')
    try:
        assert lease.cli==project/'node_modules/@remotion/cli/remotion-cli.js'
        assert lease.cli.resolve()==installed/'node_modules/@remotion/cli/remotion-cli.js'
    finally:
        lease.close();owner.close()


@pytest.mark.parametrize('sibling', ['modules', 'src', 'composition'])
def test_pinned_receipt_in_same_prefix_sibling_stays_out_of_source_inventory(roots,sibling):
    project,installed,receipt,args=roots
    parent = {'modules': installed/'node_modules-evidence',
              'src': project/'src-evidence',
              'composition': project/'vendor/timeline-composition-evidence'}[sibling]
    parent.mkdir(parents=True)
    selected = parent/'verified.json'
    selected.write_bytes(receipt.read_bytes())
    binding = closure.RemotionClosureBinding.admit(
        **{**args, 'verification_receipt': selected, 'receipt_sha256': sha(selected)})
    assert binding.validate(project)==installed/'node_modules/@remotion/cli/remotion-cli.js'
    # The receipt is still byte-pinned even though it is outside each inventory.
    selected.write_text('{}')
    with pytest.raises(ValueError,match='changed'):
        binding.validate(project)


def test_unbound_out_of_tree_link_remains_refused(roots,tmp_path):
    project,_,_,_=roots
    owner=host.HostRemotionSession(track=lambda p:None,untrack=lambda p:None)
    with pytest.raises(ValueError,match='without an admitted closure'):
        owner.lease({'ASTRID_REMOTION_PROJECT_DIR':str(project),'ASTRID_NODE_EXECUTABLE':str(Path(sys.executable).resolve())},attempt=tmp_path, scratch=tmp_path/'artifact-scratch')
    assert not owner._leases and owner.process is None
    owner.close()


@pytest.mark.parametrize('change',['receipt','lock','manifest','package','patch','composition','extra-file','link'])
def test_closure_rejects_changed_bytes_or_unrelated_dependency_link(roots,tmp_path,change):
    project,installed,receipt,args=roots
    binding=closure.RemotionClosureBinding.admit(**args)
    if change=='receipt':receipt.write_text('{}')
    elif change=='lock':(project/'package-lock.json').write_text('{}')
    elif change=='manifest':(project/'package.json').write_text('{}')
    elif change=='package':(installed/'node_modules/@remotion/cli/package.json').write_text('{"version":"4.0.508"}')
    elif change=='patch':(installed/'node_modules/remotion/dist/esm/index.mjs').write_text('unpatched')
    elif change=='composition':(project/'vendor/timeline-composition/evaluation.ts').write_text('different evaluator')
    elif change=='extra-file':(installed/'node_modules/injected.js').write_text('unadmitted')
    else:
        (project/'node_modules').unlink();other=tmp_path/'unrelated';other.mkdir();(project/'node_modules').symlink_to(other,target_is_directory=True)
    with pytest.raises(ValueError,match='changed'):
        binding.validate(project)


@pytest.mark.parametrize('change',['receipt-digest','sri','version','patch','composition','link'])
def test_new_binding_requires_verified_exact_installation(roots,tmp_path,change):
    project,installed,receipt,args=roots
    if change=='receipt-digest':args['receipt_sha256']='0'*64
    elif change=='sri':
        report=json.loads(receipt.read_text());report['installed_sri_bad']=['fixture'];receipt.write_text(json.dumps(report));args['receipt_sha256']=sha(receipt)
    elif change=='version':(installed/'node_modules/@remotion/renderer/package.json').write_text('{"version":"4.0.508"}')
    elif change=='patch':(installed/'node_modules/remotion/dist/esm/index.mjs').write_text('missing patch')
    elif change=='composition':(installed/'node_modules/@banodoco/timeline-composition/evaluation.ts').write_text('different evaluator')
    else:
        (project/'node_modules').unlink();other=tmp_path/'unrelated';other.mkdir();(project/'node_modules').symlink_to(other,target_is_directory=True)
    with pytest.raises(ValueError):closure.RemotionClosureBinding.admit(**args)


def test_trusted_closure_binding_follows_existing_host_claim_slot(roots):
    from types import SimpleNamespace

    from astrid.core.execution.generic_host import GenericPackHost
    binding=closure.RemotionClosureBinding.admit(**roots[3])
    parent=GenericPackHost(pack_roots=[],client=SimpleNamespace(fork_for_host_slot=lambda:None),remotion_closure_binding=binding)
    slot=parent._new_claim_slot()
    try:
        assert slot._remotion_closure_binding is binding
        assert slot._remotion_host_session is None
    finally:
        slot.shutdown();parent.shutdown()


@pytest.mark.parametrize('edge', ['cache-validation', 'during-evaluation'])
def test_original_owner_rechecks_admitted_closure_for_evaluation_and_cache(roots, tmp_path, monkeypatch, edge):
    project, installed, receipt, args = roots
    binding = closure.RemotionClosureBinding.admit(**args)
    monkeypatch.setattr(host, '_host_browser_executable', lambda: None)
    owner = host.HostRemotionSession(track=lambda p: None, untrack=lambda p: None, closure_binding=binding)
    lease = owner.lease({'ASTRID_REMOTION_PROJECT_DIR': str(project),
                         'ASTRID_NODE_EXECUTABLE': str(Path(sys.executable).resolve())}, attempt=tmp_path, scratch=tmp_path/'artifact-scratch')
    (tmp_path/'artifact-scratch/props.json').write_text('{}')
    request = {'type': 'evaluate', 'projectDir': str(project), 'compositionId': 'AstridTrackEvaluation',
        'nodeExecutable': str(lease.node), 'remotionCli': str(lease.cli),
        'propsPath': str(tmp_path/'artifact-scratch/props.json'), 'outputDir': str(tmp_path/'artifact-scratch/unused'),
        'frames': [0], 'resolution': None, 'port': 31500, 'environment': {}}
    exchanges = []
    monkeypatch.setattr(owner, '_start', lambda *args: None)
    def exchange(value):
        exchanges.append(value)
        if edge == 'during-evaluation':
            (project/'vendor/timeline-composition/evaluation.ts').write_text('changed')
        return {'ok': True, 'evaluation': [{'frame': 0, 'layers': []}]}
    monkeypatch.setattr(owner, '_exchange', exchange)
    try:
        if edge == 'cache-validation':
            assert owner.request(lease, {'identity': 'same', 'request': request})['ok'] is True
            (project/'vendor/timeline-composition/evaluation.ts').write_text('changed')
            request = {**request, 'type': 'validate'}
        with pytest.raises(ValueError, match='closure input changed'):
            owner.request(lease, {'identity': 'same', 'request': request})
        assert len(exchanges) == 1 and owner.process is None
    finally:
        lease.close()
        owner.close()
