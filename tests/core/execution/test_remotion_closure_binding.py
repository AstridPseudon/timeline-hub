"""Trusted closure binding over disposable package/receipt bytes only."""
import hashlib
import json
from pathlib import Path
import sys

import pytest
from astrid.core.execution import remotion_closure as closure
from astrid.core.execution import remotion_host_session as host


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


@pytest.fixture
def roots(tmp_path,monkeypatch):
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
    lease=owner.lease({'ASTRID_REMOTION_PROJECT_DIR':str(project),'ASTRID_NODE_EXECUTABLE':str(Path(sys.executable).resolve())},attempt=tmp_path)
    try:
        assert lease.cli==project/'node_modules/@remotion/cli/remotion-cli.js'
        assert lease.cli.resolve()==installed/'node_modules/@remotion/cli/remotion-cli.js'
    finally:
        lease.close();owner.close()


def test_unbound_out_of_tree_link_remains_refused(roots,tmp_path):
    project,_,_,_=roots
    owner=host.HostRemotionSession(track=lambda p:None,untrack=lambda p:None)
    with pytest.raises(ValueError,match='without an admitted closure'):
        owner.lease({'ASTRID_REMOTION_PROJECT_DIR':str(project),'ASTRID_NODE_EXECUTABLE':str(Path(sys.executable).resolve())},attempt=tmp_path)
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
