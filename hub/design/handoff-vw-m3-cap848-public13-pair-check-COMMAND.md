# App cap8488 / public13 paired-gate commands

All commands were read-only against the App checkout, except for temporary
private overlay/config creation under `/tmp`; no shared dependency was written.

## Archive and overlay

```sh
ART=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/artifacts/banodoco-timeline-composition-0.0.13.tgz
MAN=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-release13-member-manifest.txt
sha256sum "$ART"
tar -tzf "$ART" | wc -l
diff -u <(tar -tzf "$ART" | sort) <(sort "$MAN")
```

Result: SHA-256 `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`,
`77`, exact manifest match. The extracted private leaf reported version
`0.0.13`; `/home/user/work/app/node_modules/@banodoco/timeline-composition`
reported `0.0.12`.

## Public root/evaluator probe

```sh
node --input-type=module -e "const root=await import('/tmp/vw-m3-cap848-public13.Ve1XoR/node_modules/@banodoco/timeline-composition/dist/index.js'); const evaluation=await import('/tmp/vw-m3-cap848-public13.Ve1XoR/node_modules/@banodoco/timeline-composition/dist/evaluation.js'); const theme=await import('/tmp/vw-m3-cap848-public13.Ve1XoR/node_modules/@banodoco/timeline-composition/dist/theme-api.js'); if(typeof root.prepareCompositionScene!=='function'||typeof evaluation.prepareScene!=='function'||typeof evaluation.querySceneFrame!=='function'||typeof evaluation.clipOpacity!=='function') throw new Error('public root/evaluator surface missing'); const track={id:'V',kind:'visual',label:'public13'}; const run=(ms)=>{const clips=Array.from({length:12},(_,i)=>({id:'leaf-'+i,at:i===0?0:i*0.01,hold:i===0?ms/1000:0.01,track:'V',...(i===0?{effects:{fade_out:1},app:{canonicalTiming:{occurrenceStartMs:0,occurrenceDurationMs:ms}}}:{})})); const scene=evaluation.prepareScene([{track,clips,transitions:Array(11).fill(null),incomingTransitions:Array(12).fill(null)}],{assets:{}},30,1280,720); const plan=scene.tracks[0].prepared.plans[0]; const composition=root.prepareCompositionScene([{track,clips}],{assets:{}},30,root.toRuntimeTheme(theme.DEFAULT_THEME),1280,720); return {ms,publicRootDrawDuration:composition.tracks[0].prepared.plans[0].drawDuration,opacity105:evaluation.clipOpacity(clips[0],105,30),active105:evaluation.querySceneFrame(scene,105).layers.some(x=>x.clipId==='leaf-0'),active119:evaluation.querySceneFrame(scene,119).layers.some(x=>x.clipId==='leaf-0'),active120:evaluation.querySceneFrame(scene,120).layers.some(x=>x.clipId==='leaf-0'),activeEnd:evaluation.querySceneFrame(scene,plan.drawDuration).layers.some(x=>x.clipId==='leaf-0')};}; const values=[run(4000),run(4500)]; const expected=[{ms:4000,publicRootDrawDuration:120,opacity105:0.5,active105:true,active119:true,active120:false,activeEnd:false},{ms:4500,publicRootDrawDuration:135,opacity105:1,active105:true,active119:true,active120:true,activeEnd:false}]; if(JSON.stringify(values)!==JSON.stringify(expected)) throw new Error(JSON.stringify(values)); console.log('PASS public13 root/evaluator frames 105/119/120',JSON.stringify(values));"
```

Result: `PASS public13 root/evaluator frames 105/119/120` with the expected
4000/4500 values.

## App targeted tests

```sh
./node_modules/.bin/vitest run --config .tmp-vw-m3-cap848-public13-vitest.config.ts --no-cache --maxWorkers=1 --no-file-parallelism --reporter=dot src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewSurface.storedCap.test.tsx src/tools/video-editor/components/PreviewPanel/TimelineFramePreview.test.tsx src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewSurface.lifecycle.test.tsx src/tools/video-editor/lib/canonicalRenderBounds.test.ts
```

Result: `4 passed`, `35 passed`.

```sh
./node_modules/.bin/vitest run --config .tmp-vw-m3-cap848-public13-vitest.config.ts --no-cache --maxWorkers=1 --no-file-parallelism --reporter=dot --testNamePattern='client renderer' src/tools/video-editor/hooks/useRenderState.test.tsx
```

Result: `5 passed | 62 skipped` by name filter; file passed.

## ES2020 project check

```sh
./node_modules/.bin/tsc -p .tmp-vw-m3-cap848-public13-tsconfig.json --noEmit --pretty false
```

Result: exit `0`, no diagnostics. The temporary config mapped all existing
Composition subpaths to the private 0.0.13 declarations and was removed after
the run.

## Integrity after the gate

```sh
git status --short
git diff --check HEAD^ HEAD
git diff --name-only HEAD^ HEAD
```

Result: worktree clean; diff check passed; only the 11 App consumer/test files
from `8488f9c1c` were listed. No package/root/pin file was listed.
