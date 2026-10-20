from pathlib import Path
import hashlib, io, json, subprocess, tarfile
O=Path('/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch')
W=O/'workers/vw-m3-current-native-extent-review'
R=Path('/home/user/work/wt/vw-m3-current-native-extent-review')
P=O/'design/handoff-vw-m3-current-native-extent-review'
BASE='c456b3281497653cecf44f61acd6fa30565d83c8'
def git(*args): return subprocess.check_output(['git',*args],cwd=R)
base=W/'baseline'
base.mkdir(exist_ok=True)
with tarfile.open(fileobj=io.BytesIO(git('archive',BASE))) as t:t.extractall(base,filter='data')
root=git('show','20d4ab1aa9:remotion/tests/root-metadata.test.cjs')
(base/'remotion/tests/root-metadata.test.cjs').write_bytes(root)
mods=W/'root-modules/node_modules'
mods.mkdir(parents=True,exist_ok=True)
(mods/'typescript').symlink_to('/home/user/work/app/node_modules/typescript',target_is_directory=True)
Path(str(P)+'-probe.py').write_bytes((O/'design/handoff-vw-m3-native-extent-final-review-probe.py').read_bytes())
helpers=root.decode().split("test('Root registers",1)[0]
extra="""
test('both callbacks retain 300/600 frames for identical empty/sparse layers at rational FPS', async () => {
 for (const local of [1,31]) for (const total of [300,600]) {
  const fps=30000/1001;
  const timeline=timelineWithDuration(local,{clips:local===1?[]:[{id:'early'}],theme_overrides:{visual:{canvas:{width:320,height:180,fps}}}});
  assertSameMetadata(await metadataFor(propsFor(timeline,{astridCompositionDurationInFrames:total})),{width:320,height:180,fps,durationInFrames:total});
 }
});
test('boolean retained extents refuse', async () => {
 for(const value of [true,false]) await assert.rejects(()=>metadataFor(propsFor(timelineWithDuration(1),{astridCompositionDurationInFrames:value})));
});
"""
Path(str(P)+'-root-supplement.test.cjs').write_text(helpers+extra)
print(json.dumps({'baseline':BASE,'root_test_sha256':hashlib.sha256(root).hexdigest(),'typescript':json.loads(Path('/home/user/work/app/node_modules/typescript/package.json').read_text())['version'],'node':subprocess.check_output(['/tmp/vw-m3-agent-gate-node20.19.4/bin/node','--version'],text=True).strip()}))
