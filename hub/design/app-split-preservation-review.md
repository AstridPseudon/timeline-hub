# Split source preservation review

The source candidate is **not release-qualified for the split family**. Its literal native source-halving recipe is supported by the bounded cases below, including correction of a demonstrable legacy hold/speed bug. Its converted single-media routing also removes prior successful operations for transition, animation and relational inputs without a replacement. Batch retention does not close those single-ingress gaps. No product change or integration merge is made by this review.

## Exact sources and scope

| Source | Reviewed identity and entry points |
| --- | --- |
| Plan | `ORCH/PLAN.md`, decisions 8–9, §4.1, lossless-semantics gate: one compiler; authored source times; half-open intervals; preserved authored intent; one evaluator. |
| App candidate | `tl/app-m2-split-batch-ui-compose`, HEAD `d84d519ee62e52749172a695f855984e4e3cba6c`; assigned review worktree has that same HEAD. |
| Current-main App helper | `origin/main` = `580508eed1bf6ed95caaf476c9d69a4672472a2f`; `src/tools/video-editor/lib/editor-utils.ts:177,291,314`. Probe verifies **byte equality** of this helper and its timing dependencies `config-utils.ts`, `timeline-domain.ts`, `time-grid.ts` against main before importing the worktree implementations. No rewritten split arithmetic. |
| Candidate single routing | `hooks/clip-editing/useClipSplitting.ts:48–85`; public facade `hooks/useTimelineCommandsService.ts:785–846`; native gate `commands/commitSession.ts:602–624`; full-row preview `commands/clipSplitGesture.ts:69`. Paths relative to `src/tools/video-editor/`. |
| Candidate batch routing | `hooks/clip-editing/useClipSplitting.ts:10–29,87–122`; actual legacy batch helper `lib/clip-editing-utils.ts:25`; sequential native adapter `commands/clipSplitBatchCapture.ts`. |
| Agent native capture | `/home/user/work/wt/app-m2-bundle2-agent-source`, frozen **`027bd16d96010544331c953c0e1014e161786e71`**; `astrid/sdk/timeline/_split_commands.py:12–131`, `commands.py:123`; original conformance vectors `tests/editing_conformance/test_recipe_m2_clip_split.py:78,340`. |
| Agent compiler/readback | Same 027: `sdk/timeline/commit.py:222` → **actual** `core/timeline/authoring_bundle.py:753` (`compile_authoring_candidate`); readback through `core/timeline/shot_composition_projection.py:454` (`project_runtime_parent_composition`). `authoring_bundle.py:106–114` explicitly describes half-open intervals and media-source offsets. This is 027's `authoring-bundle-1`, not a claim that a later R4 timing compiler was present in this frozen native bundle. |
| Native duration contract | Same 027: `core/timeline/duration.py:129–190`: numeric hold is source duration, speed divides it once, independently rounded start plus minimum-one-frame rounded duration. |
| Public Composition 10 | Actual installed `@banodoco/timeline-composition` **0.0.10**, all **77 package files byte-identical** to `ORCH/artifacts/banodoco-timeline-composition-0.0.10.tgz`, SHA256 `cd83b77f72ce436e25eef697b289d33adae2087d92035aa37a27a308975ddea7`. Imported through its declared public package and `/evaluation` exports, not a private source copy. |
| Runtime | Frozen bundle mate `4c145dc62192f0e942e3ee3922a11488aefe9b41` on `PYTHONPATH`; no Runtime acceptance, server or sockets exercised. |

The candidate's manifest still declares its 0.0.8 artifact; shared `node_modules` already contains 0.0.10. These requested public-10 probes use the verified installed bytes. No dependency installation, manifest/pin change or root-adoption qualification is implied.

Read the complete predecessor `workers/app-m2-split-batch-ui-compose/notes/report.md`, especially its “Preservation gaps and release boundary” items 1–4. The available file has no numbered §§15–24; those section labels from the brief could not be located. Its actual stated gaps are preserved here. Root generic preservation and writer-closure design documents are untouched.

## Executable cases

Supporting files live under `ORCH/workers/app-m2-split-preservation-review/notes/`:

- `probe.py`: opens the unchanged original `recipe_m2_clip_split.json`, derives explicit copies, invokes the **real main App utility** through `probe.mts`, captures and executes with **Agent 027**, compiles before/legacy/native through the **actual native compiler**, and reads them back through the existing projector. No same-ID recreation or ownership inference.
- `probe.mts`: verifies successful App capture commands and full after-rows exactly equal Agent's results; retains both refusal messages; calls actual App duration/trim APIs and public Composition scene/key-clock APIs. Only the legacy ID allocator's `Date.now` is fixed at `123456`; authored/cut time is never rounded by the probe.
- `vectors.json`: exact full input documents, authored before/after rows, compiled rows, timeline-second intervals, half-open frame intervals, App trim props, and public scene/clock answers for **17 vectors**. Absent fields stay absent. Original fixture/input/test files are never rewritten. Right IDs are the preallocated `right` for native and the real old allocator's `<original>-123456` for legacy.

From `/home/user/work/wt/app-m2-split-preservation-review`:

```sh
REVIEW_ORCH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch
env PYTHONDONTWRITEBYTECODE=1 \
  PYTHONPATH=/home/user/work/wt/app-m2-bundle2-agent-source:/home/user/work/wt/app-m2-bundle2-runtime-source \
  ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/app-m2-bundle2-runtime-source \
  /home/user/work/venv-agent/bin/python \
  "$REVIEW_ORCH/workers/app-m2-split-preservation-review/notes/probe.py" \
  > "$REVIEW_ORCH/workers/app-m2-split-preservation-review/notes/vectors.json"
```

PASS. Seven native successes, ten native refusals; all seventeen legacy helper calls succeed. Frozen native command and compiled output equal the **unchanged original golden**, not a regenerated expectation. Every native capture leaves its input bundle unchanged. App native successes match exact Agent commands and after-rows. App and Agent refuse the same ten vectors; their nonliteral-`for` wording differs (`finite positive number` vs `finite number`), retained in the output. Compilation/projector readback leaves all tested authored source/timing rows intact. Compiling legacy output here establishes pure compiler/readback behavior, not acceptance by the old App persistence path.

## Hold geometry: proven legacy bug and supported native rule

For the untouched frozen input, target is media `clip-a`, `at=1`, `hold=8`, `from=2`, `to=10`, `speed=2`, `app.astrid.for=4`, split `on=3`, FPS `30000/1001`. Opaque app/params/row data and neighbor `clip-b` are retained exactly in the executable case.

| State/half | at | hold (source s) | from | to | speed | literal for (timeline s) | Timeline interval | Half-open frame interval |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| Before | 1 | 8 | 2 | 10 | 2 | 4 | [1,5) | [30,150) |
| Legacy left | 1 | 2 | 2 | 10 | 2 | 4 | [1,2) | [30,60) |
| Legacy right | 3 | 6 | 2 | 10 | 2 | 4 | [3,6) | [90,180) |
| Native left | 1 | 4 | 2 | 6 | 2 | 2 | [1,3) | [30,90) |
| Native right | 3 | 4 | 6 | 10 | 2 | 2 | [3,5) | [90,150) |

The old helper recognizes **any numeric hold**, then uses elapsed **timeline** seconds as the new hold. Main's own duration API and Agent/Composition duration contracts interpret that hold as **source** seconds divided by speed. Hence old [60,90) is an actual empty layer interval; [150,180) extends the split target and overlaps its unchanged neighbor. The public scene API returns `GAP` at frame 89 after legacy split, versus a media layer before/native. A film-wide max-end assertion would miss this bug: the unchanged neighbor still ends at frame 210 in all three states.

This unit mismatch is a **proven legacy bug**, not evidence for changing the native recipe to holds 2/6. Agent's original conformance test expressly requires holds 4/4, windows [2,6]/[6,10], literal durations 2/2 and exact inverse. Keep that native recipe and original golden. Native's rewrite of literal `for` is supported by its explicit matching-duration precondition and original test; legacy merely duplicates the old value. This does not authorize normalization of arbitrary/mismatching/nonliteral `for`.

Two further retained cases separate timing from source-window behavior:

| Vector | Before | Legacy after | Native after |
| --- | --- | --- | --- |
| `hold-speed1` (`at=1,hold=8,from=2,to=10,speed=1,on=3`, no for) | [1,9), [30,270), source [2,10] | holds 2/6; intervals [1,3)/[3,9), [30,90)/[90,270); **both source windows [2,10]** | holds 2/6; same visible intervals; source [2,4]/[4,10] |
| `image-hold-only-speed2` (`at=1,hold=8,speed=2,for=4,on=3`, no from/to) | [1,5), [30,150) | holds 2/6, for 4/4; [1,2)/[3,6), [30,60)/[90,180) | holds 4/4, for 2/2; [1,3)/[3,5), [30,90)/[90,150); from/to remain absent |

For moving media, numeric hold **does not mean freeze a frame**: actual `VisualClip` passes `computeMediaTrim(clip,fps)` and sanitized speed to Video. Legacy's repeated window on the speed-one hold restarts the source; native source-halving follows the declared source-time contract. Actual App trim props are [60,300] before, [60,300]/[60,300] legacy, and [60,120]/[120,300] native. This is evidence about source/clock inputs, **not decoded pixel/audio parity**. No new freeze/hold policy is proposed.

## Exact source, speed and off-grid vectors

All following FPS values are `30000/1001` except the explicit final row. Full floating-point values and all authored fields are retained in `vectors.json`; the table abbreviates only repeated windows/metadata. `for` means `app.astrid.for`, and `—` means absent.

| Vector | Before: at; hold; from→to; speed; for; cut | Legacy left / right | Native left / right | Half-open frames: before → legacy → native |
| --- | --- | --- | --- | --- |
| `window-speed2` | 1; —; 2→10; 2; —; 3 | at 1/3; hold —/—; windows 2→6 / 6→10; speed 2/2; for —/— | Same geometry/windows/speed/presence | [30,150) → [30,90)/[90,150) → same |
| `precise-window-speed1.3` | 1; —; 2.123456789→10.987654321; 1.3; 6.818613486153846; 3 | at 1/3; hold —/—; windows 2.123456789→**4.7235** / **4.7235**→10.987654321; for unchanged on both | at 1/3; hold —/—; windows 2.123456789→**4.723456789** / **4.723456789**→10.987654321; for 2/4.818613486153846 | [30,234) → [30,90)/[90,234) → same |
| `precise-hold-speed1.3` | 1; 8.864197532; same precise window; 1.3; 6.818613486153846; 3 | at 1/3; holds 2/**6.8642**; full original window on both; for unchanged | at 1/3; holds 2.6/**6.264197532000001**; windows split at 4.723456789; for 2/4.818613486153846 | [30,234) → **[30,76)/[90,248)** → [30,90)/[90,234) |
| `offgrid-window-speed1.3` | **1.003**; —; same precise window; 1.3; 6.818613486153846; **3.003000123** | at 1.003/**3.003**; hold —/—; windows split at **4.7235**; for unchanged | at 1.003/**3.003000123**; hold —/—; windows split at **4.723456948900001**; for **2.0000001230000004 / 4.818613363153846** | [30,234) → [30,90)/[90,234) → same |
| `offgrid-half-frame-refusal`, **30fps** | **0**; —; **0→1**; **1**; —; **0.05** | at 0/0.05; hold —/—; windows 0→0.05 / 0.05→1; for —/— | **No after-state**: `split must preserve half-open frame geometry` | [0,30) → **[0,2)/[2,31)** → refused |

Speed stays unchanged on both halves throughout. Precise-window legacy timeline intervals are [1,3.0000332392307687)/[3,7.818580246923077), versus native [1,3)/[3,7.818613486153847). Off-grid legacy intervals are [1.003,3.003033239230769)/[3.003,7.8215802469230775), versus native [1.003,3.0030001230000005)/[3.003000123,7.821613486153845). Native retains authored precision instead of adding a UI snap or a four-decimal source cut.

The 0.05 case is the smallest retained frame-geometry refusal: legacy returns success but extends a one-second film by one frame. Native refusal is explained by the **existing** half-open contract, not a new policy. Nevertheless it is another prior successful operation that the converted arbitrary-time single ingress now refuses. This review does not authorize rounding the requested cut, changing compiler defaults, fallback on refusal, or declaring all historical arbitrary-time splits preserved. Leave that qualification open for Agent/orchestrator disposition; do not rewrite an existing positive to expect refusal.

Public Composition 10 was called on **before and both successful outputs**, including exact endpoint-adjacent frame vectors. For all accepted native geometry cases its prepared own spans equal the existing App/Agent half-open intervals. Around rational-frame cut 90, before `contentFrame` is 59/60/61 at frames 89/90/91; native is left 59 then right 0/1. Its public `timelineKeyframeTime` yields 2.9696333333333333 / 3.003 / 3.036366666666667 seconds in all states; `spriteKeyframeFrame` resets to 0 on the new row. These clocks have different domains; neither is a proof that arbitrary animations survive cloning. No key origin is inferred or rewritten.

The public **0.0.10** export does not expose a media decoder/source-time clock or `computeMediaTrim`/`getSanitizedPlaybackRate`; those are additive **0.0.11** exports (`Composition 7d663330a996bbf2410660d167f658824e19c6ea`). This review does not silently adopt 11. We retain actual App trim props plus Composition 10 content/key clocks, not a newly invented source-sampling formula. For the three precise vectors, App trim frames are [64,329] before and [64,142]/[142,329] native; equal rounded trim values cannot establish equal sampled media. Media has no decoded alpha evidence in these fixtures, so Composition honestly returns `UNKNOWN` for active media, and `GAP` for empty spans. Pure scene/geometry evidence is **not pixel/audio parity**.

## Removed single positives and exact retained-domain boundary

These use the predecessor's **original batch-positive patches** on `{id:'a',track:'picture',clipType:'media',asset:'picture',at:1,hold:4,from:0,to:4}`, at 30fps and cut 3. The old helper succeeds and clones the entire patch onto both halves, holds 2/2, at 1/3, source windows still [0,4]/[0,4], intervals [30,90)/[90,150). The executable file retains all complete rows. “Positive” here proves the prior App operation returned a split and preserved fields; it does not prove correct transition/animation/anchor rendering.

| Exact original patch/input | Agent 027 and candidate App capture result | Candidate routing impact |
| --- | --- | --- |
| `transition:{type:'dissolve',duration:0.5}` | `does not support transition` | Every converted single ingress loses this old positive; batch retains its existing full-config ingress. Composition 10 reports `Unknown transition id 'dissolve'` on this exact input; no substitute registered transition was invented. |
| No target transition; unchanged sibling `b` at 5 with that transition | `does not support parent transitions` | Even an otherwise ordinary target loses single splitting because of a sibling. Batch checks **any current config clip transition** before capture and retains the whole batch. |
| `animation:{keep:[null,false]}` | `does not support animation` | Single refused; batch retained. This is the original opaque positive, not proof that this opaque shape is an evaluable animation. |
| `params:{fadeIn:0.5}` | `does not support animated media parameters` | Single refused; batch retained. |
| `app:{astrid:{on:'anchor'}}` | `does not support on` | Single refused; batch retained. No inferred anchor binding. |
| `app:{astrid:{for:'until next cut'}}` | Agent: `for must be a finite number`; App: `for must be a finite positive number` | Single refused; batch retained. No implicit duration resolution. |
| `app:{astrid:{fixed_start:false}}` | `does not support fixed_start` | Single refused; batch retained. |
| `time_map:{keep:[null,false]}` | `does not support time_map` | Single refused; batch retained. |
| Moving media with numeric hold but absent from/to | `moving media split requires an explicit source window` | Single refused; batch retained. No guessed window. |

The exact affected ingress is **both** branches already converted for media:

1. `useClipSplitting.handleSplitClipAtTime` (selected keyboard `s` and inspector call through `handleSplitSelectedClip`; pointer/context “Split Here” supplies its own frozen time). The sole old-path predicate is now `clip.clipType !== 'media'`; otherwise native capture throws and the hook toasts. There is no replacement for the above media positives.
2. Public `TimelineCommands.splitClip` in `useTimelineCommandsService.ts`: the same media/nonmedia partition, then native capture/submit; synchronous failure returns `mutation_failed`. It previously called the same old helper/validated mutation for these media.

**Recommended smallest retained boundary:** keep the already separate original single ingress for these recognized, unqualified field/source forms on a raw, unambiguous **literal parent** target, including a transition anywhere in the parent collection. Select this boundary from authored shape and established raw ownership **before capture**; preserve the current head/scope, group, editability and collision guards. Use the same native contract qualifications the retained batch path already names; do not make every media row native merely because it has `clipType:'media'`. An App change to do this is a follow-up, not included here. Arbitrary-time geometry remains the explicit open case above; no new snap policy is designed here.

This recommendation is **retention of a pre-existing ingress**, not a new publisher, optional-port fallback, native-error fallback, or reason to reopen the generic writer path. Missing port, native refusal, ambiguous ownership, stale head and identity collision must not select legacy. Do not infer parent/occurrence ownership from display ID text or `app.canonical`; the existing raw owner resolver remains authoritative. No same-ID row replacement/recreation is proposed.

Transitions, animation, relational intentions, nonliteral duration, time maps, unknown moving windows, projected/shared/occurrence ownership and unqualified nonmedia splits **must remain unconverted until their own native contracts are qualified**. No source/contract evidence here proves those historical successful operations are all legacy bugs or deliberate removals. The PLAN specifically keeps playback features existing films use. Native's explicit “unsupported” checks establish its current domain; they do not authorize deleting App behavior outside it.

The existing batch path must retain original valid-input order, invocation playhead, outside/interior filtering, one atomic config edit for mixed/nonmedia/unqualified selections, and whole-selection pinned-group exclusion. Existing nonmedia text/hold single success stays intact. Original grouped split exclusion and positive group behavior tests remain unchanged. The three original drag requirements remain open; no marker/name/assertion was edited and none was newly added.

## Qualification result and follow-up

No accepted native counterexample contradicting the source-halving/half-open recipe was established by these bounded **pure** probes. That statement is limited to these seven native-success vectors. Source-clock/pixel/audio continuity, valid transition rendering, animated/relational split semantics, browser gestures, actual Runtime acceptance, inverse/rebase and release integration are not proved by this review.

Before release, App must preserve the identified single positives through a preselected retained ingress or a qualified native replacement. Agent must qualify the exact retained source/speed/off-grid vectors against its real render/source clock; if that shows a changed film, fix the Agent recipe/compiler and retain the smallest failing before/native case, rather than patching App math or changing global defaults. Keep the original conformance golden. The half-frame refusal needs explicit contract disposition; it is not silently closed as a passing preservation case. Real Player/export pixel and audio parity remains a separate gate.

Verification on unchanged candidate product source: six targeted App files, **168 passed, 3 existing expected failures**; seventeen executable pure comparison cases PASS; known-marker check **3 authorized / 0 forbidden**; `git diff --check` clean and `git status --short` empty. Exact commands/results and probe-development limitations are in `workers/app-m2-split-preservation-review/notes/report.md`. No browser, full suite, central service request, tsc, build, install, socket, commit, checkout, merge or integration mutation.
