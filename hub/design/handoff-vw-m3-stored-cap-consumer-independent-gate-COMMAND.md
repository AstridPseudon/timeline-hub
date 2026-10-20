# Independent gate commands and results

All commands were read-only against the Composition worktree or read-only App
source. No shared dependency or cache was changed.

## Public Composition 12-leaf probe

```sh
node --import /home/user/work/app/node_modules/tsx/dist/loader.mjs \
  --input-type=module -e "import {prepareScene,querySceneFrame,clipOpacity} from './typescript/src/evaluation.ts'; const run=(ms)=>{const clips=Array.from({length:12},(_,i)=>({id:'leaf-'+i,at:i===0?0:i*0.01,hold:i===0?ms/1000:0.01,track:'V',...(i===0?{effects:{fade_out:1},app:{canonicalTiming:{occurrenceStartMs:0,occurrenceDurationMs:ms}}}:{})})); const track={id:'V',kind:'visual',label:'public12'}; const scene=prepareScene([{track,clips,transitions:Array(11).fill(null),incomingTransitions:Array(12).fill(null)}],{assets:{}},30,1280,720); const plan=scene.tracks[0].prepared.plans[0]; return {ms,drawDuration:plan.drawDuration,ownDuration:plan.ownDuration,opacity105:clipOpacity(clips[0],105,30),active119:querySceneFrame(scene,119).layers.some(x=>x.clipId==='leaf-0'),activeEnd:querySceneFrame(scene,plan.drawDuration).layers.some(x=>x.clipId==='leaf-0')};}; const values=[run(4000),run(4500)]; if(JSON.stringify(values)!==JSON.stringify([{ms:4000,drawDuration:120,ownDuration:120,opacity105:0.5,active119:true,activeEnd:false},{ms:4500,drawDuration:135,ownDuration:135,opacity105:1,active119:true,activeEnd:false}])) throw new Error(JSON.stringify(values)); console.log('PASS public Composition 12-leaf stored-cap boundary',JSON.stringify(values));"
```

Result: **exit 0**

```text
PASS public Composition 12-leaf stored-cap boundary [{"ms":4000,"drawDuration":120,"ownDuration":120,"opacity105":0.5,"active119":true,"activeEnd":false},{"ms":4500,"drawDuration":135,"ownDuration":135,"opacity105":1,"active119":true,"activeEnd":false}]
```

This directly exercises the current public `prepareScene`, `querySceneFrame`,
and `clipOpacity` helpers from the worker's own Composition source. The input
uses the effective occurrence field because Composition consumes the approved
derived value only after App's private consumer copy has selected it; this is
not a producer or App serialization claim.

## Read-only source checks

```sh
git -C /home/user/banodoco/reigh-app show b1ef4b9b910ba72375c34cf319692f90d22edc25:src/tools/video-editor/components/PreviewPanel/TimelineFramePreview.tsx
git -C /home/user/banodoco/reigh-app show b1ef4b9b910ba72375c34cf319692f90d22edc25:src/tools/video-editor/compositions/TimelineRenderer.tsx
```

Result: the still input props contain `config` and optional host only; the
renderer has a compiled-vector branch but receives no vector from that still
boundary in the submitted consumer patch.

No full, browser, render, network, socket, install, or shared App test was run.
