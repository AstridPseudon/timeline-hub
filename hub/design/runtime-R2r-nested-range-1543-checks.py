import ast,copy,hashlib,json,pathlib,subprocess,types
from runtime_protocol.timeline_commit import CommitRejected
from runtime_protocol.timeline_commit_auth import validate
root=pathlib.Path.cwd();w=pathlib.Path('/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-R2r-nested-range-1543/evidence')
old=subprocess.check_output(['git','show','HEAD:runtime_protocol/timeline_commit_auth.py'],text=True)
module=types.ModuleType('runtime_protocol._nested_baseline');module.__package__='runtime_protocol';exec(compile(old,'baseline-timeline_commit_auth.py','exec'),module.__dict__)
inputs=json.loads((root/'tests/fixtures/timeline_nested_inverse_1543.json').read_text())
try:module.validate(**copy.deepcopy(inputs))
except CommitRejected as exc:print('OLD RED:',exc);assert str(exc)=='inverse stage provenance does not match authenticated history'
else:raise AssertionError('old Runtime unexpectedly accepted nested ranges')
validate(**copy.deepcopy(inputs));print('NEW GREEN: complete validate on same retained-fact auth projection')
old_tree=ast.parse(old);new_tree=ast.parse((root/'runtime_protocol/timeline_commit_auth.py').read_text());before={node.name:ast.dump(node,include_attributes=False) for node in old_tree.body if isinstance(node,(ast.FunctionDef,ast.ClassDef))};after={node.name:ast.dump(node,include_attributes=False) for node in new_tree.body if isinstance(node,(ast.FunctionDef,ast.ClassDef))};changed=[name for name in before if before[name]!=after.get(name)];print('Changed original functions:',changed);assert set(changed)=={'_inverse_stage_history','_inverse_stage_ranges','_inverse_stage_boundaries'}
p='tests/test_timeline_inverse_stage_authentication.py';a=ast.parse(subprocess.check_output(['git','show','HEAD:'+p],text=True));b=ast.parse((root/p).read_text());assert [ast.dump(n,include_attributes=False) for n in a.body]==[ast.dump(n,include_attributes=False) for n in b.body[:len(a.body)]];print('Original tests AST: unchanged')
paths=json.loads(pathlib.Path('/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-R2r-inverse-stage-sol-0922/evidence/frozen77.json').read_text());print('Frozen paths:',len(paths));baseline={};old_manifest_diffs=[]
for p,h in paths.items():
 data=(root/p).read_bytes();base=subprocess.check_output(['git','show','HEAD:'+p]);assert data==base,p;baseline[p]=hashlib.sha256(data).hexdigest()
 if baseline[p]!=h:old_manifest_diffs.append(p)
assert len(paths)==77
(w/'frozen77.json').write_text(json.dumps(baseline,sort_keys=True,indent=2)+'\n');print('Frozen77 current HEAD equality: 77/77; differences from 0922 manifest:',old_manifest_diffs)
print('Source qualification only; no provider compilation or public redo invoked')
