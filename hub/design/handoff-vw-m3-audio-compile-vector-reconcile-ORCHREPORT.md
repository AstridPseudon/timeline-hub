# Audio compiler corpus reconciliation — review complete

**138 PASS / 5 RED, four targeted files, exit 1, 6.57s.** No product policy repair, producer qualification or parity claim. App base `5912bfc3284da03112ef6c235447cfbeffb678bd` unchanged; six new test/fixture files only. The historical `vw-m3-audio-projection-goldens2/ORCHREPORT.md` and its five-RED report remain untouched.

## Deliverables and review findings

- `audio-corpus-map.json` here: side-by-side original Viewing `1bfa51d5a` and Agent draft `fd82c36c7cd66d1d58aa0250a008245a43e6fbaa`, with original vectors, actual authored children/occurrences, full output clips from both existing Agent entrypoints and complete Runtime closure/output artifacts. **11 Viewing rows, eight related Agent rows, three Agent-only rows; zero identical complete authored input pairs.** Relations mean coverage, never replacement/identity.
- `audio-compile-contract.proposal.md` here: proposed corrections for Agent domain review. No Agent contract was edited. Correct `source_from` to public11 `computeMediaTrim(clip,fps).trimBefore / fps`, and rate to public `getSanitizedPlaybackRate`. Remove the stale open curve question: PLAN now requires honouring curves. No parser edit is granted.
- App worktree: byte-identical original Viewing vectors, Agent draft vectors and Agent base graph; literal complete Agent output clips; two direct test files. Existing Viewing base graph is byte-identical to the original branch.
- `viewing-1.json` through `viewing-11.json`, `agent-12.json` through `agent-22.json` here retain each original graph, vector, exact Runtime closure and full actual projector output. These are pure function results, not accepted/certified Runtime publications.

| Original Viewing coverage | Related Agent coverage | Concrete difference |
| --- | --- | --- |
| child .8, unity occurrence | none | Agent absent-volume/unity is distinct |
| absent volume / gain .5 | gain-child-absent-is-unity | Viewing trim .125..1.125 at .25s; Agent 0..2 at 0 |
| mute, child .8 / gain .5 | muted-occurrence-silences-child-gain | same scalar rule, different trim/placement |
| child .8 / gain .5 | gain-child-x-occurrence | same multiplication, different trim/placement |
| child 1.5 / gain 2 | gain-boost-x-occurrence | same multiplication, different trim/placement |
| source_offset **350**, volume .8 | source-offset-is-metadata-only, **.35**, volume absent | preserve literal metadata values; do not silently change units |
| occurrence speed 1.5, child speed absent | occurrence-speed-not-inherited | same metadata rule, different child trim/placement/volume |
| hold 10, child speed 2, at .25, occurrence 4s | none | actual output hold **7.5** |
| trim .125..10.125, child speed 2, at .25, occurrence 4s | none | actual output to **7.625** |
| combined .1s in/out on .05..55, at .25, volume .8 | separate .5s in/out on 0..2, at 0, volume absent | three distinct fade inputs |
| effects=[{fade_in:.1,fade_out:.1}] | none | opaque preserved shape, not a public envelope |

Agent-only: absent volume/unity gain; absent volume/zero gain; child speed 2 alongside occurrence speed 1.5. JSON preserves all fields; the table is a reading guide.

**Clock counterexamples for Agent review:** original `from=.125` gives trimBefore=4 at both fps values, so origin is `4/30` or `4/(30000/1001)`, not .125. Original fade `from=.05` gives trimBefore **2 at 30** and **1 at 30000/1001**. Tests assert those literal boundaries and use only public helpers. Gain multiplication and metadata-only occurrence offset/speed remain settled.

## Exact passing and failing requirements

| File | PASS | FAIL |
| --- | ---: | ---: |
| shotCompositionProjection.audio.reconcile.test.ts | 35 | 4 |
| shotCompositionAudio.public-clock.test.tsx | 46 | 1 |
| existing shotCompositionProjection.test.ts | 28 | 0 |
| existing AudioTrack.test.tsx | 29 | 0 |
| **Total** | **138** | **5** |

All 22 clips from `project_runtime_parent_composition` and all 22 from the original `project_shot_composition` match literal full-field snapshots using `toStrictEqual`. Closure adaptation reshapes transport/pins only, retaining actual authored occurrence values. No second compiler computes timing/gain. Python checks input immutability and equality of the returned full closure. Supplemental Agent preservation checks retain opaque/unknown child data, native parent audio and its exact registry. This does not claim arbitrary App unknown-field preservation.

App sound comparisons preserve exact key presence/value for at/from/to/hold/speed/volume/params/effects. Four ordinary requirements remain RED:

1. Child .8, occurrence gain .5: App **.8**, Agent **.4**.
2. Child 1.5, occurrence gain 2: App **1.5**, Agent **3**.
3. Offset 350, child .125..1.125: App **.475..1.475**, Agent **.125..1.125**.
4. Occurrence speed 1.5, child absent: App **speed=1.5**, Agent **speed absent**.

Four passing planted negatives use these recorded wrong values against correct Agent sound. They do not require App to keep producing wrong output.

Fifth RED: the public non-Player boundary throws the unchanged `ENVELOPE_UNRENDERED: external encoder requires matching attempt-local envelope PCM` for all three original params-fade inputs. **One ordinary failing test, three diagnostics.** No actual normal producer is invoked; this is not preparation qualification. No absence/refusal was recast as passing product behavior.

Public controls exercise actual built public11 TimelineComposition/AudioTrack on all 22 literal compiler results at 30 and 30000/1001 fps. Media/frame primitives alone are mocked. Synthetic attempt metadata checks admission/trim/rate/scalar plumbing; no HTTP endpoint is fetched and no PCM is supplied. Combined fade samples pass; opaque effects remain opaque. A separate compiled-input exponential-slow control proves curve honouring without changing either corpus. These checks do not prove decoding, mixing, priming, browser playback, actual preparation or physical parity.

## Exact commands and results

Working directory `/home/user/work/wt/vw-m3-audio-compile-vector-reconcile`. Below:

```sh
P=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-audio-compile-vector-reconcile
```

Every CPU batch used `sh "$P/cpu-guard.sh"`: checks absolute ORCH/QUIET.md and ORCH/managers/viewing/QUIET.md; a live marker writes own fresh PAUSED_ACK and exits 75. Actual markers absent throughout; no release inferred.

```sh
sh "$P/cpu-guard.sh" env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/user/work/agent /home/user/work/venv-agent/bin/python "$P/reference.py"
sh "$P/cpu-guard.sh" /home/user/work/venv-agent/bin/python "$P/map.py"
```

Final **exit 0** each: 22 exact graph/closure projections and map produced. Initial generator failed because Agent's graph has no parent config; corrected transport scaffolding to config={} without altering authored inputs, then passed. Projector/duration/graph-validator source bytes match the specified Agent ref before/after.

```sh
sh "$P/cpu-guard.sh" env ASTRID_CHECKOUT=/home/user/work/agent AUDIO_CONTRACT_PYTHON=/home/user/work/venv-agent/bin/python node_modules/.bin/vitest run --config "$P/vitest.config.mjs" src/tools/video-editor/data/shotCompositionProjection.audio.reconcile.test.ts src/tools/video-editor/data/shotCompositionAudio.public-clock.test.tsx src/tools/video-editor/data/shotCompositionProjection.test.ts src/tools/video-editor/compositions/AudioTrack.test.tsx --reporter=verbose
```

**Exit 1: 138 PASS / 5 FAIL / 0 SKIP, 6.57s**, `tests.log`. Config extends current App setup and aliases advertised public11 exports to the existing read-only peer extraction; one worker thread. No private Composition source aliases/install/extraction/pin changes. Earlier successful new-tests-only invocation gave **81 PASS / 5 FAIL**, `tests-argv.log`; final run adds 57 existing neighbors and an explicit .05 rational-fps assertion.

```sh
sh "$P/cpu-guard.sh" node_modules/.bin/tsc -p "$P/tsconfig.json" --noEmit
sh "$P/cpu-guard.sh" node_modules/.bin/eslint src/tools/video-editor/data/shotCompositionProjection.audio.reconcile.test.ts src/tools/video-editor/data/shotCompositionAudio.public-clock.test.tsx --max-warnings 0
sh "$P/cpu-guard.sh" env PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python "$P/postflight.py"
git diff --check
sh "$P/cpu-guard.sh" node "$P/../vw-m3-envelope-public-clock-join/artifact/public-import-smoke.mjs"
```

All final **exit 0**: `types.log`, `lint.log`, `postflight.log`; fresh native ESM root/evaluation import smoke passes. Initial test-only type/declaration issues were corrected; final typecheck clean. Postflight verifies original corpora/base graphs byte-for-byte, unchanged tracked App files, Agent reference source, new-file whitespace, and exact public11 archive/extraction: **SHA256 dfa824a475737598477d98a2be2c2ad6ab9c3e6c8b0f967fad22e154afd74601, 58,344 bytes, 77 files**. Peer worker files were read-only.

Harness diagnostics are not evidence passes: three initial starts interrupted (130), two 45s timeouts (124); a traced run and fixed probe hit reference-hook timeouts (exit 1, 39 tests not reached); one temporary probe had a Python string SyntaxError (exit 1, 39 not reached). Logs: tests-initial/node/split/threads/minimal/trace/single-input/single-input-fixed.log here. No skip markers were added. The stall was Python stdin transfer; final bridge passes one bounded unchanged input per invocation via argv, with a subprocess timeout. Temporary probes removed. Central service inspected, never requested; no full/named suite queued.

## Handoff and unrun scope

Bounded task complete; no task blocker. Adoption remains held for **Agent domain review**, separate authorization of the four App repairs, real trusted normal-source preparation and coordinated public11 adoption. This is a review branch, not integration-green evidence.

No Agent compiler/provider/source, Runtime, integration, pins/locks, Root or product edits; no new canonical clock/math/copied DSP; no xfail/skip/weakened tests. No browser, capture, actual render, socket service, install, full suite, physical WAV/MP4, decode/codec/priming, Player/export parity or normal producer qualification was run or claimed. Real MP4/DIP remains ahead of further audio instrumentation.

Own external Vite cache cleaned; no temporary/build output in worktree. Commit message supplied; no git mutation/commit/merge/checkout/push/ref change.

Next: Agent domain owner reviews the exact JSON map and proposed clock/curve prose, retains both original corpora, then authorizes bounded App repair and trusted producer join. Re-run unchanged RED requirements through the actual producer before physical qualification.
