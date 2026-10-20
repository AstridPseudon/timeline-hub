from pathlib import Path
import ast
import difflib
import hashlib
import importlib.util
import json
import subprocess

REPO=Path('/home/user/work/wt/vw-m3-current12-pcm-caller-preserve-main')
ORCH=Path('/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch')
PREFIX=str(ORCH/'design/handoff-vw-m3-current12-pcm-caller-preserve-main-')
TASK=ORCH/'workers/vw-m3-current12-pcm-caller-preserve-main'
base='c456b3281497653cecf44f61acd6fa30565d83c8'
run='astrid/packs/rendering/rendering/renderers/remotion/run.py'
helper='astrid/packs/rendering/rendering/renderers/remotion/normal_audio.py'
test='tests/packs/rendering/test_normal_audio_run.py'
owned=[run,helper,test]
prereqs=json.loads(Path(PREFIX+'prerequisites.json').read_text())
snapshot=TASK/'composed-prerequisites'
for name,facts in prereqs['files'].items():
    assert hashlib.sha256((snapshot/name).read_bytes()).hexdigest()==facts['sha256']
    if name not in owned:
        assert (REPO/name).read_bytes()==(snapshot/name).read_bytes(),name
patch=''
for name in owned:
    original=(snapshot/name).read_text() if (snapshot/name).exists() else ''
    patch+=''.join(difflib.unified_diff(original.splitlines(keepends=True),(REPO/name).read_text().splitlines(keepends=True),fromfile='a/'+name if original else '/dev/null',tofile='b/'+name))
Path(PREFIX+'caller-only.patch').write_text(patch)
expected=set(prereqs['files'])|{test}
changed=set(subprocess.check_output(['git','diff','--name-only',base],cwd=REPO,text=True).splitlines())
changed.update(subprocess.check_output(['git','ls-files','--others','--exclude-standard'],cwd=REPO,text=True).splitlines())
assert changed==expected,(changed-expected,expected-changed)
protected=['astrid/core/timeline/banodoco_composer.py','astrid/core/timeline/duration.py','astrid/core/timeline/authoring_bundle.py','astrid/core/timeline/shot_composition_projection.py','astrid/sdk/timeline/commit.py','astrid_runtime_client/generated.py','runtime.lock.json','astrid/packs/rendering/rendering/renderers/threejs/run.py','tests/packs/rendering/test_live_scene_composition.py','tests/packs/rendering/test_composition_package.py','tests/packs/rendering/test_scene_source_carry.py']
for name in protected:
    assert (REPO/name).read_bytes()==subprocess.check_output(['git','show',base+':'+name],cwd=REPO),name

def functions(source):
    return {node.name:ast.dump(node,include_attributes=False) for node in ast.parse(source).body if isinstance(node,(ast.FunctionDef,ast.AsyncFunctionDef))}
old=functions(subprocess.check_output(['git','show',base+':'+run],cwd=REPO,text=True))
new=functions((REPO/run).read_text())
assert old['capture_remotion_frames']==new['capture_remotion_frames']
assert 'on_scene_props(merged_props, frame_numbers)' in (REPO/run).read_text()
metadata={'base':base,'kernel':prereqs['kernel'],'extent':prereqs['extent'],'caller_only_files':owned,'caller_only_patch_sha256':hashlib.sha256(patch.encode()).hexdigest(),'changed':{name:{'bytes':(REPO/name).stat().st_size,'sha256':hashlib.sha256((REPO/name).read_bytes()).hexdigest()} for name in sorted(changed)},'protected':{name:hashlib.sha256((REPO/name).read_bytes()).hexdigest() for name in protected},'capture_remotion_frames_ast_unchanged':True}
Path(PREFIX+'source.json').write_text(json.dumps(metadata,indent=2,sort_keys=True)+'\n')
# Keep an applying, exact base diff for inspection without mutating any git state.
tracked=subprocess.check_output(['git','diff','--binary',base],cwd=REPO)
for name in sorted(changed):
    exists=subprocess.run(['git','cat-file','-e',base+':'+name],cwd=REPO,stderr=subprocess.DEVNULL).returncode==0
    if not exists:
        result=subprocess.run(['git','diff','--no-index','--binary','--','/dev/null',name],cwd=REPO,capture_output=True)
        assert result.returncode==1
        tracked+=result.stdout
Path(PREFIX+'composed-source.patch').write_bytes(tracked)
spec=importlib.util.spec_from_file_location('caller_setup',PREFIX+'setup.py')
# Load the helper definition without re-running its mutating setup body.
setup_ast=ast.parse(Path(PREFIX+'setup.py').read_text())
namespace={}
for node in setup_ast.body:
    if isinstance(node,(ast.Import,ast.ImportFrom,ast.FunctionDef)) or (isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SHARED' for t in node.targets)):
        exec(compile(ast.Module(body=[node],type_ignores=[]),PREFIX+'setup.py','exec'),namespace)
after=namespace['shared_manifest']()
assert after==json.loads(Path(PREFIX+'shared-before.json').read_text()),'shared Composition graph drift'
Path(PREFIX+'shared-after.json').write_text(json.dumps(after,sort_keys=True))
print('PASS: 19 exact composed prerequisite paths, only two caller source deltas plus new tests; current M2/provider/client/serializer/Three.js and callbacks preserved; shared graph identical (%d entries)'%len(after))
