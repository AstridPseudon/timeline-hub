**A2 / P1 actual17985: retained case-2 stage diagnosis; no new run**

The actual second case reaches the intended right-clip Timing input, changes its visible Source In from 0 to 3, completes Enter and Tab, and shows the App's conflict dialog before a second page-observed commit POST. At failure, the durable owner is idle at the split head, generation 1, with no intents or pending request. The trace also shows the later write-ack watchdog. This localizes the visible failure to the App save/conflict path before trim transmission. **The precise originating rejection, guard, mounted capture operands and owner/basis transition remain unobserved. A specific product repair is not justified.**

App evidence recommendation for Proof: custody and unchanged-body checks PASS; actual-stage localization is stronger than D25's previous packet; causal completeness remains INSUFFICIENT EVIDENCE and whole P1 remains NO-GO. Proof owns the final verdict. The first case's PASS cannot establish any second-case capture, ownership or recovery fact.

This report follows PLAN §3 A2/P1 and contract items 1–5: retain the full request/reply contract, mixed-command chaining, merged adoption, refusal rollback, exact replay and guarded undo requirements. No product, oracle, guard, body, fixture, settings, dependency or Git mutation was made. No new browser, HTTP, seed, preflight, build, benchmark, control loop, test service request or unit experiment was run.

**Source and custody**

Actual run: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/app-P1-D26-exact-target-sol-2007-ap2-P1-chain-h6-1023200755-17985` (below, `RUN`). Private case folder: `RUN/playwright-output/three-products.p1-chain-P1-c924b-p-rolls-back-with-a-message` (below, `CASE`). `CASE` remains retained; the test source snapshot was removed by the service. No run file was rewritten.

Actual App commit `be890a1fa5d6db02e4964522aa356f88f115a22a`, tree `f794d795dbefc2ead9a3f770a7566826da2b1f4e`; collector `b221388d30`, popup fix `17324ed4b7`; Agent `78738040d72ce74c42ddf7731221aecb06f9246d`, Runtime `2a9e347ff0e1df1dedff5ab7b59ddb27dfe3129d`. This worker's unchanged App HEAD/tree equal the actual App tuple. Later App integration `ba8583b829` contains producer `201044ee60`; neither that producer nor Proof adapter1953 was in actual17985. Their source descriptions below are coverage analysis, never historical event observations.

| Retained original | Bytes | SHA-256 | Result |
| --- | ---: | --- | --- |
| `CASE/p1-diagnostic.json` | 12296 | `06ebd3980bb71c95fa634b371f2cf1c73735f6ba1b4c86ac6a815f37f1ed0676` | Parseable JSON, schema 1, `afterEach_failure_continuation` |
| `CASE/trace.zip` | 3646437 | `e2f1181d6ffa307d1e185b43339666a06264296db1e895b0706f85ac8a585965` | Read privately with stdlib `zipfile`/`json`; remains private |
| `CASE/error-context.md` | 15452 | `a528c3a901e134a9d967e172ab4231ee33210b6bc288327ac07055fad57a40ae` | Read privately as text; remains private |
| `RUN/log.txt` | 28475 | `6e0936261a410073514ca5c27f4d97f8540f8b5b978d9f32869d4086ec2990dc` | Retained; artifact custody hash checked |

Safe diagnostic counterpart: [byte-exact JSON](./app-A2-P1-17985-actual-cause-sol-2017.json). Its 12296 bytes and SHA-256 equal the original above; `cmp` exit 0. Export happened only after the audit succeeded: formatter bytes exactly equal merged b221's `tests/e2e/local/p1-diagnostic-safety.ts` (SHA-256 `92e780dc73165857ab8090a8cfebd6220fa4044689493c8cf9fa4c0cf8b4c6a0`); recursively all keys belong to its container/primitive allowlists; no duplicate keys; all 165 strings individually classified as fixed case/phase/UI/error literals, finite numeric text, fixture display text, bounded non-auth identifiers, masked route, or timestamp; credential assignments/Bearer/JWT/URL scan clean. No raw body, credential, authenticated identity, session, headers, cookies, full network URL or asset structure was exported. Outbox `ownerId` is the permitted durable non-auth save-owner identifier. No trace resource/source/network body was exported or copied. Only existing artifact file hashes were calculated.

Actual service result, previously run by App's central test service: exit 1 / 460s, 1 PASS + 1 FAIL. First original case at spec1339 PASS 30.5s, covering its automatic accepted/merged/lost-ack/reload/restart/exact-retry chain. Second original case at spec1507 times out after 300000ms; spec1539 expected 2 page-observed POSTs, received 1. Agent move, trim HTTP409, refusal and rollback assertions are UNREACHED. These are retained results, not fresh tests by this worker.

**Case-2 evidence table**

Trace citations are `member:line @ byte-offset`, with zero-based offsets into that member's uncompressed UTF-8 bytes, not ZIP-file offsets. Times are recorded trace monotonic milliseconds; they are not UTC and are not assumed identical to `performance.now()` in a later emitter. All trace rows below belong exclusively to the failed second case archive. The JSON's observation time is `2026-10-23T20:15:34.390Z`, `durationMs=300001`; it is a failure-continuation snapshot, not a capture-time heap snapshot.

| Field / stage | Actual observation | Field source / member citation | Case / recorded time |
| --- | --- | --- | --- |
| Navigation | Browser navigation completes without action error; destination contents withheld | `0-trace.trace:8 @1957` before, `:11 @3010` after (`call@131`) | 2 / 49083.919→49183.583ms |
| Split reply | Sole page-observed commit gets HTTP200 and split head | JSON `available.wireHeads[0]`; request projection index0, body present/3669B, key present/36B | 2 / retained at continuation |
| Right clip selection | `.clip-action` click targets the JSON rightId; selected DOM node carries that ID and `data-selected=true` | `0-trace.trace:378 @351635` before, `:393 @378947` after; serialized DOM `:388 @368844` | 2 / 63059.213→63140.514ms; DOM 63108.740ms |
| Timing tab | Click completes without action error | `0-trace.trace:395 @379598`, `:415 @392870` (`call@230`) | 2 / 63146.584→63432.590ms |
| Pre-input timing DOM | Start2, Duration8, Source In0, Source Out8, Speed1 (visible input values) | `0-trace.trace:417 @393219`, labeled direct serialized input groups | 2 / 63493.334ms |
| Source In before | Visible value `0`, numericValue0; same selected right clip visible | JSON `available.sourceWindow.before.sourceIn` and `.selectedClip.identity.clipId` | 2 / collected before fill, retained at continuation |
| Fill | Intended Source In locator receives `3`, completes without action error | `0-trace.trace:443 @453820`, `:454 @466350` (`call@242`) | 2 / 63847.069→64007.472ms |
| Intermediate DOM | Visible numeric text includes `03`; this is not a mounted source value or proof of a malformed numeric callback | Direct serialized input in `0-trace.trace:456 @466670` | 2 / 64229.679ms |
| Enter | Source In `press('Enter')` completes without action error | `0-trace.trace:457 @484686`, `:465 @502614` (`call@244`) | 2 / 64233.344→64333.886ms |
| Tab / focus traversal | Source In `press('Tab')` completes without action error; direct visible input subsequently has `3`. Execution/arguments of the React blur callback are not recorded | `0-trace.trace:467 @512989`, `:475 @525097`; direct input `:476 @525187` | 2 / 64341.354→64448.936ms; DOM 64457.763ms |
| Source In after | Visible value `3`, numericValue3; same right clip visible | JSON `available.sourceWindow.after.sourceIn` and `.selectedClip.identity.clipId` | 2 / collected after Enter/Tab, retained at continuation |
| Conflict UI | Static conflict-dialog heading is present in serialized DOM after input sequence | `0-trace.trace:483 @537532` | 2 / 64582.027ms |
| Failed second-POST wait | Poll reaches its 90000ms ceiling; final assertion retains expected2/received1 and spec1539 | `test.trace:607 @312050` poll failure; final assertion `:1131 @473525`; JSON `case` | 2 / after input, before failure continuation |
| Diagnostic collection stall | Failure collector waits for `video-editor-provider` `data-timeline-id`, timeout0; no completion for this call in archive | `0-trace.trace:729 @648212` (`call@454`), source spec869 | 2 / start154540.389ms; global test deadline later |
| Watchdog | Static unacknowledged-save warning appears | `0-trace.trace:726 @606356`; error context line89 @3167 | 2 / 153864.949ms; final context untimed |
| Final timing DOM | Start2, Duration5, Source In3, Source Out8, Speed1 | `error-context.md` lines164/174/184/194/204, byte offsets6720/7272/7815/8359/8898 | 2 / final context, no own timestamp |
| Final conflict UI | Alertdialog and its static conflict heading retained | `error-context.md` line373 @15055, heading line375 @15148 | 2 / final context, no own timestamp |
| Durable owner | One owner; generation1; intentCount0; pending null; rejected false; accepted head equals split wire head; readFailed false | JSON `available.outbox.summary` and `.owners[0]` | 2 / continuation timestamp above |
| Wire head pair | Split revision `authoring-parent-revision-7fb9c6800da6dcfc0c48f57990c29b65e94eb77706bfef376c0ac1697ed8cb93`, publication `txn-f1d4434840ab48a08b9564158d872e02` | JSON `available.wireHeads[0].head` and `.outbox.owners[0].acceptedHead` | 2 / reply and later durable snapshot |
| Mounted provider attrs | No serialized DOM node in archive supplies the requested provider testid or project/timeline/head attributes. Collector lookup waits rather than returning a mounted value; source provider testid exists in mocks, not actual product provider | All 76 frame-snapshot records inspected for named attrs; stalled call above; product source search | 2 / whole retained archive; no mounted head pair established |
| Errors / UI snapshot | page errors[]; request failures[]; retained console sample40 identical503 messages, each signal `unknown`; connected, alertCount1, recoveryVisible false, timelineErrorVisible false | JSON `available.errors` / `.recovery` | 2 / continuation; capped/disposable observations |
| Actual capture / basis / owner lifecycle | UNKNOWN, explicitly recorded rather than inferred from successful split or outbox generation | JSON `mountedObservations`, `captureData`, `unknowns.{mountedDataRef,callbackPatch,captureResolution}`, `losses` | 2 / no mounted producer in this source |

The trace network member contains two HTTP200 POST entries at `0-trace.network:118 @215625` (57860.198ms) and `:119 @217711` (57852.935ms), both before right-clip input. A private equality comparison finds the same destination and postData; no values, headers, contents or hashes were published. The spec's route handler forwards the first browser POST via `route.fetch()` (spec1513–1519), so these network entries do not establish two authored browser commits or a trim transmission. The page observer and artifact retain one POST. Later missing trim cannot be supplied by counting the forwarded split twice. Trace network also has 101 HTTP503 records; their presence does not identify the save error or prove a capture failure.

**Mechanism supported by source, and its limit**

The direct trace establishes input delivery and the subsequent conflict UI; the final timing DOM also changes Duration8→5. These are DOM observations, not proof of the complete `dataRef`, callback patch, raw `hold`, source/gesture config identity or canonical document. In particular Duration5 must not be relabeled as a raw hold value. The accepted outbox head is a durable/wire fact, not a mounted provider head.

At actual source, `ClipPanelBody.tsx:153–163,378–384` forwards finite timing changes and conditionally reapplies committed values; `useClipEditing.ts:235–291` selects the current clip and can construct trim read operands. `useTimelinePersistence.ts:1009` captures before debounce; `:675` awaits that capture before mutation. `useTimelineSave.ts:87–93` can reject an unavailable/replaced owner; its owner/basis effect is at `:131–244`. `timelineLocalSaveHandoff.ts:57,321` uses/wraps local failures as `TimelineVersionConflictError`. Persistence's typed conflict branch at `:849–874` sets the exhausted flag through `:370–383`; `useTimelineRealtime.ts:24–28` opens the dialog for that flag, rendered by `TimelineEditorShellCore.tsx:1174–1185`. This source path explains how the observed conflict UI can occur without a trim HTTP409. It does not reveal which guard actually fired. A mapped effect-dependency cancellation or raw/rendered-source mismatch is a possibility, not the actual17985 cause.

The later 300s test deadline must also be separated from the original missing-POST wait: after the poll fails, the existing detailed diagnostic reader stalls on the absent provider selector. The bounded afterEach continuation eventually retains a parseable file. That collection stall explains lost fields and extra elapsed time; it does not explain the missing second POST. No collector change is proposed here.

**Exact remaining fields and existing-diagnostic coverage**

Producer coverage was read from `201044ee60`'s typed projection and actual call sites. Adapter coverage is limited to Proof's [1953 handoff](./handoff-ap2-P1-mounted-event-adapter-1953.md): pre-navigation opt-in, bounded allowlisted listener and early/continuation file integration are described, but final literal scope/type/nested-key matching to this exact producer remains explicitly unqualified there. No adapter source or independent final compatibility result was available in this task's retained handoff. Thus producer support below is source-observed; integrated adapter support is not a claimed PASS.

| Missing actual17985 field | Does 201044 cover the field at a future observed boundary? | Adapter1953 / remaining limit |
| --- | --- | --- |
| Delivered trim operands and selected clip at save schedule; mounted `from/to/at/hold/speed` versus callback source/gesture numerics | Yes: `schedule` projects `patch`, `mountedClip`, `sourceClip`, `gestureClip`, `clipId` and actual mounted head. It observes schedule, not the NumberField callback itself | Listener intended; exact final mapping unqualified. DOM text alone remains insufficient |
| Actual capture entered, resolved or rejected; joined owner/generation | Yes: `capture-called/resolved/rejected`, `ownerAlias`, generation, closed/sessionPresent | Listener intended. Capture's mounted/original head fields can still be UNKNOWN; correlate with schedule/basis events, do not fill them from wire |
| Original verified head pair, readiness and ordering relative to adoption | Yes: `basis-read/ready/unavailable/error`, `handoff-ready`, `adoption-start/complete`, `adopted-read`; selected original numerics only when a clip ID is available | Listener intended; originalClip can remain UNKNOWN. No entire config/bundle dependency data is projected |
| Owner lifecycle and actual dependency-trigger sequence | Partly: owner init/closed/retired, lifecycle-cancel, alias/generation/current, identity-presence and session-created/recovered/changed | No React dependency identities/equality results, exact editSeq/savedSeq comparison, ready-promise identity or cancellation reason is emitted; numeric/head equality cannot prove them |
| Exact original error class/code and rejecting guard/reason | **No.** Emitter reports `errorStage` capture/basis-read/owner-init and fixed `errorCode=operation-rejected`; `errorClass` remains UNKNOWN | Adapter cannot recover a reason producer never emits. A captured `operation-rejected` would narrow stage, not identify the guard or provider code |
| Durable pending intent count/status at the failing instant | Partly: session status/owner-presence/recoverableOwnerCount; emitter `intentsPendingCount` remains UNKNOWN | Existing artifact outbox owners/counts cover only later successful reads, not a synchronized history of the failing instant |

There is no historical evidence that the emitter was enabled, no production emitter in this tuple, and no basis for inventing its events. No claim is made that the later source fixes actual17985 or that matching its head/numeric projections would establish full input identity.

**Smallest justified recommendation**

Return this one retained result and exact JSON to Proof for the D25 verdict. Keep the second-POST requirement and every downstream refusal/rollback assertion. The current evidence justifies **no semantic/product/oracle repair**: it establishes an App-local save/conflict boundary but leaves several original rejection paths possible. In particular, do not remove owner cancellation, clear an owner, refresh the original basis, rewrite reads, force a save, accept one POST, or blame Runtime409 from this packet.

The next bounded source task, if dispatched by the manager, is to qualify the existing201044 producer against Proof1953's exact interface. That would cover most listed temporal fields prospectively. It still cannot supply the exact rejection reason because its error code is deliberately fixed; Proof should state whether that narrower stage evidence is sufficient before any additional diagnostic scope or product repair is chosen. This worker requested no run and makes no speculative repair patch. Actual17985 cannot become causally complete retroactively.

**Verification and unchanged scope**

Tests, typecheck and lint: N/A, read-only diagnosis; none run, no fresh green suite claimed. Exact verification commands executed from the assigned App worktree:

```sh
python "$TMPDIR/audit17985.py"
git diff --check
git status --short
git rev-parse HEAD HEAD^{tree}
```

Audit script in this task's harness-cleaned `/tmp/w-e2237cc921` used only stdlib for retained inputs, read-only `git show b221388d30:tests/e2e/local/p1-diagnostic-safety.ts`, and `cmp ORIGINAL EXPORTED_JSON`. Result: custody checks for all four files PASS, strict recursive export audit PASS, byte comparison PASS, protected bodies PASS. Private archive inspection used inline `python - <<'PY'` scripts with `zipfile.ZipFile(...).read()` and `json.loads()`; only the finite table projections, fixed source-matched UI markers, numeric values, times/offsets and presence/equality booleans were emitted. No private source resources or complete trace records were printed or retained outside the run.

Protected hashes verified from unchanged bytes: first case1339–1506 SHA-256 `4b04ad7ef74b8106244d87c23d12c7a18da251dd8f5a746f42d3221a72ea8b7f`; second1507–EOF `2f7501184477c8aec38d3cd289dd13c0d011fa8f69ecd43378f24f6c3100a2f7`; entire P1 spec `be63db711ea6857c45bfcb3b41909ae083d4147cd0f608760701f5044f12e497`; Gate5 blob `37caf28577d42fbe98afd2320dffa3c72e6e74b1`. `git diff --check` exit0; assigned worktree `git status --short` empty. No tracked report or other tracked file was added. Reports/JSON are small external task artifacts; scripts remain in TMPDIR. No operational blocker; the precise causal evidence gap above is a finding, not a reason to manufacture a result.
