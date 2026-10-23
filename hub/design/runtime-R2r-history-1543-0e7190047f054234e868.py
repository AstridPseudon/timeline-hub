from pathlib import Path
import ast
import collections
import hashlib
import json
import shutil
import subprocess

root = Path.cwd()
orch = Path('/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch')
worker = orch / 'workers/rt-R2r-history-sequential-1543'
ev = worker / 'evidence'
design = orch / 'design'
changed = subprocess.check_output(['git', 'diff', '--name-only'], text=True).splitlines()
assert set(changed) == {'runtime_protocol/timeline_commit_port.py', 'runtime_protocol/timeline_commit_store.py', 'tests/test_timeline_commit_sequential_verifier.py'}
assert not subprocess.check_output(['git', 'ls-files', '--others', '--exclude-standard'], text=True).strip()
subprocess.run(['git', 'diff', '--check'], check=True)
head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip()
assert head == '85b2feeb58bc54174ac7b89fda4805883865d3b2'
entries = {}
for row in subprocess.check_output(['git', 'ls-tree', '-rz', 'HEAD']).split(b'\0'):
    if row:
        prefix, path = row.split(b'\t', 1)
        mode, kind, oid = prefix.split()
        entries[path] = mode, oid.decode()
def tree(values):
    grouped = {}
    for path, value in values.items():
        first, sep, rest = path.partition(b'/')
        grouped.setdefault(first, []).append((rest if sep else None, value))
    rows = []
    for name, children in grouped.items():
        if children[0][0] is None:
            mode, oid = children[0][1]
            key = name
        else:
            mode = b'40000'
            oid = tree({child: value for child, value in children})
            key = name + b'/'
        rows.append((key, mode + b' ' + name + b'\0' + bytes.fromhex(oid)))
    raw = b''.join(data for _, data in sorted(rows))
    return hashlib.sha1(b'tree ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
assert tree(entries) == subprocess.check_output(['git', 'rev-parse', 'HEAD^{tree}'], text=True).strip()
for path in changed:
    raw = (root / path).read_bytes()
    entries[path.encode()] = b'100644', hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
    shutil.copyfile(root / path, ev / ('source-' + Path(path).name))
    shutil.copyfile(root / path, design / ('runtime-R2r-history-1543-source-' + Path(path).name))
manifest = {'base_head': head, 'source_tree_computed_without_git_write': tree(entries),
            'changed': {p: hashlib.sha256((root / p).read_bytes()).hexdigest() for p in changed}}
agent = Path('/home/user/work/wt/agt-pin-67ba416b')
agent_head = subprocess.check_output(['git', '-C', str(agent), 'rev-parse', 'HEAD'], text=True).strip()
assert agent_head == '67ba416bca813f4931b557f6f2ca2abf935d7d35'
assert not subprocess.check_output(['git', '-C', str(agent), 'status', '--porcelain'], text=True).strip()
original_test = 'tests/editing_conformance/test_doc_patch_sequential_rebase.py'
raw = (agent / original_test).read_bytes()
assert raw == subprocess.check_output(['git', '-C', str(agent), 'show', 'HEAD:' + original_test])
manifest['original_agent_test'] = {'head': agent_head, 'file_sha256': hashlib.sha256(raw).hexdigest(),
    'ast_sha256': hashlib.sha256(ast.dump(ast.parse(raw), include_attributes=False).encode()).hexdigest()}
shutil.copyfile(agent / original_test, ev / 'original-agent-test.py')
assert (root / 'runtime_protocol/timeline_commit_auth.py').read_bytes() == subprocess.check_output(['git','show','HEAD:runtime_protocol/timeline_commit_auth.py'])
artifacts = json.loads((root / 'contract/artifacts.json').read_text())['artifacts']
for p, expected in artifacts.items():
    assert 'sha256:' + hashlib.sha256((root / p).read_bytes()).hexdigest() == expected
    assert (root / p).read_bytes() == subprocess.check_output(['git','show','HEAD:' + p])
manifest['preservation'] = {'all_auth_including_atomic_and_inverse_helpers_byte_identical': True,
    'all_78_manifest_artifacts_match_and_unchanged': True, 'schemas_contracts_clients_locks_pins_unchanged': True,
    'submitted_agent_tests_ast_and_bytes_unchanged': True}
reports = [json.loads(p.read_text()) for p in (ev / 'original9').glob('pytest-report-*.json')]
assert len(reports) == 27
calls = [p for p in reports if p['when'] == 'call']
assert len(calls) == 9 and all(p['outcome'] == 'passed' for p in reports)
assert sum('refusal' in p['nodeid'] for p in calls) == 5
assert '366 passed' in (ev / 'runtime-final.log').read_text()
for tool, expected in [('ruff',22),('pyright',80)]:
    d = json.loads((ev / (tool+'-comparison.json')).read_text())
    assert d == {'baseline':expected,'candidate':expected,'added':[],'removed':[]}
manifest['tests'] = {'runtime_nine_files': {'passed':366,'exit':0}, 'original_agent_nine': {'passed':9,'strict_negatives':5,'reports':27,'exit':0},
    'moved_history_old_source': {'failed':1,'exit':1,'reason':'provider alias is outside its authenticated boundary -> accepted commit record is corrupt'},
    'sequential_final': {'passed':57,'exit':0},'ruff':{'exit':1,'baseline':22,'added':0,'removed':0},
    'pyright':{'exit':1,'baseline':80,'added':0,'removed':0}}
(ev / 'source-manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
patch = subprocess.check_output(['git','diff','HEAD'])
(ev / 'candidate.patch').write_bytes(patch)
(design / 'runtime-R2r-history-1543-current-only.patch').write_bytes(patch)
def credential_keys(value, path=()):
    out=[]
    if isinstance(value,dict):
        for key,child in value.items():
            if key not in {'credential_keys', 'credential_clean'} and any(token in key.lower() for token in ('password','secret','credential','api_key','authorization')):
                out.append('.'.join((*path,key)))
            out.extend(credential_keys(child,(*path,key)))
    elif isinstance(value,list):
        for i,child in enumerate(value): out.extend(credential_keys(child,(*path,str(i))))
    return out
capture_files = sorted((ev / 'original9').glob('original9-capture-*.json'))
credentials = {p.name: credential_keys(json.loads(p.read_text())) for p in capture_files}
assert not any(credentials.values())
(ev/'credential-scan.json').write_text(json.dumps({'files':len(capture_files),'credential_keys':credentials,'clean':True},indent=2)+'\n')
# Every source, report, capture and log is durable and flat in design.
exported={}
for p in sorted(ev.rglob('*')):
    if p.is_file():
        raw=p.read_bytes()
        h=hashlib.sha256(raw).hexdigest()
        name='runtime-R2r-history-1543-'+h[:20]+p.suffix
        dest=design/name
        if not dest.exists(): dest.write_bytes(raw)
        exported[str(p.relative_to(ev))]={'sha256':h,'bytes':len(raw),'design':str(dest)}
exports={'source':manifest,'files':exported,'capture_count':len(capture_files),'reports':27}
(ev/'export-manifest.json').write_text(json.dumps(exports,indent=2)+'\n')
(design/'runtime-R2r-history-1543-manifest.json').write_text(json.dumps(exports,indent=2)+'\n')
print(json.dumps(manifest,indent=2))
print('Exported',len(exported),'files;',len(capture_files),'captures; 27 reports; credential scan clean')
