# Commands and results

Candidate identity:

```sh
git -C /home/user/banodoco/reigh-app show -s --format='%H %T %P %s' 6b7afe3ad28e6a899a09b15fbfaa5e79f4b05214
```

Result: `6b7afe3ad28e6a899a09b15fbfaa5e79f4b05214
32dc0de053ffb98d718077a111994181ae03ea15
48576cfa2783331f2c7c8309ff4069162a3afd11 fix(timeline): restore complete verified stored-cap delivery`.

Read-only candidate checks:

```sh
git -C /home/user/banodoco/reigh-app diff --check 48576cfa2783331f2c7c8309ff4069162a3afd11 6b7afe3ad28e6a899a09b15fbfaa5e79f4b05214
git -C /home/user/banodoco/reigh-app diff --quiet 48576cfa2783331f2c7c8309ff4069162a3afd11 6b7afe3ad28e6a899a09b15fbfaa5e79f4b05214 -- package.json package-lock.json bun.lockb pnpm-lock.yaml runtime.lock.json vendor
git -C /home/user/banodoco/reigh-app grep -n 'Object.hasOwn' 6b7afe3ad28e6a899a09b15fbfaa5e79f4b05214 -- src/tools/video-editor/lib/serialize.ts src/tools/travel-between-images/components/shotTimelineDataProvider.ts
```

Results: diff check PASS; package/lock/vendor check PASS (no changes); ES2020
guard PASS (no `Object.hasOwn` match).

Public13 artifact/import check:

```sh
realpath /home/user/work/app/node_modules/@banodoco/timeline-composition
cat /home/user/work/app/node_modules/@banodoco/timeline-composition/package.json | sed -n '1,4p'
sha256sum /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/artifacts/banodoco-timeline-composition-0.0.13.tgz
tar -tzf /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/artifacts/banodoco-timeline-composition-0.0.13.tgz | wc -l
```

Results: imported package resolves to the shared App graph read-only, version
`0.0.13`; archive SHA256
`9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`; 77
members.

Public root evaluator probe, using `/opt/node22/bin/node` with the App graph
first on `PATH`:

```sh
PATH=/opt/node22/bin:$PATH /opt/node22/bin/node --input-type=module -e "import {prepareScene,querySceneFrame,clipOpacity} from '@banodoco/timeline-composition/evaluation'; const run=(ms)=>{const clips=Array.from({length:12},(_,i)=>({id:'leaf-'+i,at:i===0?0:i*0.01,hold:i===0?ms/1000:0.01,track:'V',...(i===0?{effects:{fade_out:1},app:{canonicalTiming:{occurrenceStartMs:0,occurrenceDurationMs:ms}}}:{})})); const track={id:'V',kind:'visual',label:'public13'}; const scene=prepareScene([{track,clips,transitions:Array(11).fill(null),incomingTransitions:Array(12).fill(null)}],{assets:{}},30,1280,720); const plan=scene.tracks[0].prepared.plans[0]; const frame=(n)=>({frame:n,opacity:clipOpacity(clips[0],n,30),active:querySceneFrame(scene,n).layers.some((x)=>x.clipId==='leaf-0')}); return {ms,drawDuration:plan.drawDuration,ownDuration:plan.ownDuration,frames:[frame(105),frame(119),frame(120)]};}; const values=[run(4000),run(4500)]; const [a,b]=values; if(a.drawDuration!==120||a.ownDuration!==120||a.frames[0].opacity!==0.5||!a.frames[0].active||!a.frames[1].active||a.frames[2].active||b.drawDuration!==135||b.ownDuration!==135||b.frames[0].opacity!==1||!b.frames[0].active||!b.frames[1].active||!b.frames[2].active) throw new Error(JSON.stringify(values)); console.log('PASS public13 root 105/119/120',JSON.stringify(values));"
```

Result: PASS. 4000 ms: draw/own `120/120`, opacity at 105 `0.5`, active at
105/119 and inactive at 120. 4500 ms: draw/own `135/135`, opacity at 105 `1`,
active at 105/119/120.

Existing exact-candidate evidence was used for the App lanes per task scope:

- corrected consumer seam: 6 files / 115 tests passed;
- public13 paired gate: 4 files / 35 tests passed, client-route lane 5 passed,
  private public13 project check exit 0;
- complete candidate cap retest: 2 files / 13 tests passed;
- complete candidate broad lane: 24 files passed, 2 files failed; 575 passed,
  10 failed. The 8 lifecycle failures are the known MAIN574 label issue; the
  two cap comparison failures were rerun green after excluding provenance-only
  revision IDs.

Not run here: full suite, 304-case matrix, browser/e2e, actual Player capture,
actual render/export, network/live sockets, install, or whole-project tsc.
