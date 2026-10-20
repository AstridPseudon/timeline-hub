from pathlib import Path
import ast, hashlib, io, json, os, subprocess, tarfile
O=Path('/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch')
W=O/'workers/vw-m3-current-native-extent-review'
R=Path('/home/user/work/wt/vw-m3-current-native-extent-review')
D=O/'workers/vw-m3-current-native-extent-unit'
P=O/'design/handoff-vw-m3-current-native-extent-review'
BASE='c456b3281497653cecf44f61acd6fa30565d83c8'
def git(*a):return subprocess.check_output(['git',*a],cwd=R)
assert (D/'DONE').exists() or (D/'BLOCKED').exists()
assert (D/'exit').read_text().strip()=='0'
TIP=git('rev-parse','tl/vw-m3-current-native-extent-unit').decode().strip()
assert TIP!=BASE
assert git('rev-parse',TIP+'^').decode().strip()==BASE
assert git('merge-base',TIP,BASE).decode().strip()==BASE
copy=W/'candidate';copy.mkdir(exist_ok=True)
with tarfile.open(fileobj=io.BytesIO(git('archive',TIP))) as t:t.extractall(copy,filter='data')
manifest={}
for item in git('ls-tree','-rz',TIP).split(b'\0'):
 if not item:continue
 header,filename=item.split(b'\t');mode,kind,oid=header.split();name=filename.decode()
 if kind!=b'blob':continue
 actual=os.readlink(copy/name).encode() if mode==b'120000' else (copy/name).read_bytes()
 actual_oid=hashlib.sha1(b'blob '+str(len(actual)).encode()+b'\0'+actual).hexdigest()
 assert actual_oid==oid.decode(),name
 manifest[name]={'git_blob':oid.decode(),'sha256':hashlib.sha256(actual).hexdigest(),'bytes':len(actual)}
root=git('show','20d4ab1aa9:remotion/tests/root-metadata.test.cjs')
assert (copy/'remotion/tests/root-metadata.test.cjs').read_bytes()==root
changed=git('diff','--name-only',BASE,TIP).decode().splitlines()
assert set(changed)=={'astrid/core/rendering/service.py','astrid/packs/rendering/rendering/renderers/remotion/run.py','remotion/src/Root.tsx','tests/packs/rendering/test_native_layer_extent.py','remotion/tests/root-metadata.test.cjs'}
assert (copy/'remotion/src/Root.tsx').read_bytes()==git('show','61f1a420f:remotion/src/Root.tsx')
unchanged={}
for name in ['astrid/core/timeline/banodoco_composer.py','astrid/core/timeline/duration.py','astrid/packs/rendering/rendering/renderers/remotion/normal_audio.py','astrid/packs/rendering/rendering/renderers/threejs/run.py','tests/packs/rendering/test_remotion_capture_scene_props.py','tests/packs/rendering/test_live_scene_composition.py','remotion/package.json','remotion/package-lock.json','remotion/normal-audio-sources.mjs','remotion/attempt-envelope-pcm.mjs']:
 p=copy/name
 old=subprocess.run(['git','show',BASE+':'+name],cwd=R,capture_output=True)
 if old.returncode:assert not p.exists();unchanged[name]='absent at both'
 else:
  assert old.stdout==p.read_bytes(),name
  unchanged[name]=manifest[name]
methods={}
for name in changed[:]:
 if name.endswith('.py') and name.startswith('astrid/'):
  def defs(data):return {n.name:ast.dump(n,include_attributes=False) for n in ast.walk(ast.parse(data)) if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))}
  old=defs(git('show',BASE+':'+name));new=defs((copy/name).read_bytes())
  methods[name]=sorted(k for k,v in new.items() if old.get(k)!=v)
state={'base':BASE,'candidate':TIP,'candidate_tree':git('rev-parse',TIP+'^{tree}').decode().strip(),'parent':BASE,'producer_exit':0,'archive_all_blob_bytes_equal':True,'archive_blob_count':len(manifest),'changed_files':{n:manifest[n] for n in changed},'unchanged_critical_files':unchanged,'ast_changed_methods':methods,'root_exact_test_sha256':hashlib.sha256(root).hexdigest(),'root_matches_approved_extent':True,'private_graph':{'typescript_leaf':str((W/'root-modules/node_modules/typescript').resolve()),'typescript_version':json.loads((W/'root-modules/node_modules/typescript/package.json').read_text())['version'],'node':'/tmp/vw-m3-agent-gate-node20.19.4/bin/node','composition_pin':json.loads((copy/'remotion/package.json').read_text())['dependencies']['@banodoco/timeline-composition']}}
Path(str(P)+'-sourcebytes.json').write_text(json.dumps(state,indent=2)+'\n')
Path(str(P)+'-all-blobs.json').write_text(json.dumps(manifest,indent=2)+'\n')
Path(str(P)+'-scope.patch').write_bytes(git('diff','--binary',BASE,TIP))
subprocess.run(['git','diff','--check',BASE,TIP],cwd=R,check=True)
print(json.dumps(state,indent=2))
