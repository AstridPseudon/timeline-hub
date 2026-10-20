# Independent review: placement, duplicate, and ACK-loss scheduling

Reviewed 2026-10-20 against PLAN.md. Product tree unchanged. Recommendations concern each exact unit independently; they do not authorize merging a staged feature cohort or activating an unqualified caller.

| Unit | Exact comparison | Recommendation |
| --- | --- | --- |
| Explicit placement | `55e7e217b..615a23a20` (`tl/app-m2-placement-move-session-stage`) | **HOLD** as a standalone integration/use candidate. The additive capture/port delta is sound on inspected inputs, but its unchanged session still automatically retries uncertain A when post-retry B is appended. Reconcile narrowly with the approved scheduling fix and current safety corpus before qualification. |
| Independent duplicate | `55e7e217b..4969238c5` (`tl/app-m2-duplicate-native-binding-stage`) | **HOLD**. The native capture and RAW compiled golden resolve the old root-identity concern, but the same inherited scheduling defect remains, and the observed Runtime official union does not admit duplicate. No UI activation. |
| ACK-loss scheduling | `1be0efdde..5fe884946` (`tl/app-m2-ackloss-new-intent-unit`) | **APPROVE** the bounded core fix and retained positive tests. Browser/Gate 5 qualification remains pending; approval is not a complete Gate 5 pass. |

No newly demonstrated need for a DTO, client history guard, second queue, replacement writer, or policy change. A HOLD here is a review result, not an unfinished review task.

## 1. Placement: native capture is preserved; standalone scheduling remains wrong

Source references below are relative to App commit `615a23a20`, unless explicitly qualified.

`commands/placementCapture.ts:29–59,88–133` adds the exact retained asset reads and exclusive occurrence-owner selection around the existing native clip-move recorder. `:142–175` snapshots/freezes capture and requires every original claim at finish, including rejecting extra original args. `commands/commitSession.ts:421–450` is the existing owner resolver, reused at `:464`: parent ownership uses a real parent row; occurrence binding checks explicit raw owner/clip, projected ID, project/document, source shot/revision/internal pin and output identity. It never derives ownership by splitting a display suffix. Capture at `:453–473` also requires matching project/timeline/displayed revision/publication, one display clip, no matching legacy group, and a retained nonempty media_id binding. Finish/submission at `:475–503` replay original claims on current authored bytes, use the prepared-command map/local generation, and admit only the matching same-clip move preview. The hook adds legacy-save fences at capture, finish and submit; it introduces no caller migration.

The imported placement fixture is byte-identical to Agent `2431ae1f`'s `tests/editing_conformance/fixtures/recipe_m2_placement.json`: SHA-256 **7404b665b2918ebf095abc68bd3a20176afb0589b79cf785887c1da50b68d271** (both git-object streams hashed during this review). App parity tests compare complete command/record and authored state, not a replacement guard table. Agent normal sources are `astrid/sdk/timeline/native_placement_commands.py:27–78` and `tests/editing_conformance/test_recipe_m2_placement.py:37–71,119–169,216–232` at `2431ae1f`: same move writes, full registry binding reads, original replay, reload/inverse/redo, shared-owner refusal, and final-value rebase versus history-sensitive inverse. These were inspected, not executed here.

The port is correctly limited to **existing unchanged-media re-placement**. It preserves raw clip ID, media/source window and sibling closure; it does not substitute unplace/recreate, allocate new IDs, pool, choose latest/gallery media, implement automatic completion, or imply create/unplace admission. Distinct legacy automatic policy and continuation work remains separate.

**Counterexample preventing standalone approval:** in this exact branch `commitSession.ts:137–154,233–248`, append always calls `pump()` and the pump dispatches an existing pending request. Let placement A reach status retry after a lost ACK; then capture/submit placement B. B durably appends, but its append also retransmits A without Retry/recovery/flush. This follows directly from the unchanged shared scheduling code; it was not executed afresh with placement in this review. The ACK-loss worker's retained RED proves that scheduling path with native clip moves. Placement's suffix test does not catch it: it calls `first.retry()` after B and only asserts all prefix requests have identical bytes/key, without asserting there was no extra prefix request before that explicit call. Exact retry identity is preserved; retry authority is not.

The placement session tests cover native parent/occurrence captures, persisted original basis, same request/key through explicit recovery at a newer head, original H0 plus A/B preview recovery, B's original guards at accepted HA, accepted projection and an ordinary inverse request targeting accepted publication. Their inverse response is fabricated from restored input; they do **not** execute real Runtime inverse/rebase/admission. Reported 451 plus final 58 passing tests are source evidence only, not 509 distinct tests or actual Runtime proof.

Required next gates: preserve the port's bounded delta while restoring its prerequisites on current integration; apply the scheduling semantics from unit 3; run targeted retained capture/session/hook and current corpus/history regressions on the resulting tree; then qualify official paired Runtime acceptance/reload/lost-ACK retry/suffix and real inverse (including binding/ownership conflict refusal). Activate any explicit caller only in its separately gated migration. Automatic completion and shared placementService remain unqualified.

## 2. Duplicate: exact RAW roots are fixed in Agent; official admission is still absent

App references in this section use `4969238c5`. `commands/occurrenceDuplicateCapture.ts:14–107` accepts only raw occurrence owner, closed independent intent and exactly the two caller-reserved IDs. It records whole source row, source shot identity, collection membership/order, raw internal source, source payload and absence of the two destinations, then creates exactly shot/occurrence roots. Item IDs use Agent's existing deterministic recipe and collision check; source/sibling rows are copied unchanged. `:117–130` preserves a frozen portable original capture. The gesture adapter freezes the caller's reserved args once and checks the returned command still uses them. Session `commitSession.ts:453–487` replays those original claims against its authored bundle, stores a null preview in the existing outbox, and remains unbound to hook/UI. No new Runtime or graph publication path was added.

`clipMovePrimitives.ts:169–222` adds optional root lookup, created-shot support, collection-shape reads and the existing known-item remap for raw source payload reads. The diff does not replace the shared opaque remapper or recursively reinterpret identity-looking metadata. Parity and neighboring authoring-bundle tests cover its effect. Unknown nested metadata, output history, task IDs and associations remain literal JSON; no historical field is relabelled as a new copied output.

The enriched fixture is tied to normal Agent source `hub/tl/agt-m2-stack-sync-2` = **2431ae1fcdb6c9baf568043d3c0dad7c602b0e49**, incorporating `27037f0b` root rederivation. I verified native duplicate source SHA-256 **551302c17ba42326a3ccfdbf516126bdf35f4a423e5871f7598523978afbae3a**. Normal Agent `native_occurrence_duplicate.py:11–45` agrees with the TS recipe. Crucially, `astrid/core/timeline/authoring_bundle.py:231–253,1039–1048` rederives exactly present root stable_deep_link/output_identity, using the actual compiled destination shot revision and row parent_document_id (fallback timeline ID). It does not rewrite nested strings/history. `tests/editing_conformance/test_recipe_occurrence_duplicate.py:174–193` asserts those roots and the destination closure.

App `occurrenceDuplicateCapture.test.ts`'s RAW-root test checks the fixture's parent occurrence bytes **before** reopening/projection: encoded parent document `doc /é`, new shot/occurrence, the copied row's actual shot_revision_id, exact factories, and a corresponding shot/internal closure. Its complete golden test compares command, record and after_bundle. The after_bundle legitimately still holds source root strings; only Agent compilation knows final revision IDs. This is not App read-side repair. However, consuming a precomputed correct closure in a fake transport cannot prove the deployed provider rederives it. That remains an actual-pair gate.

**Counterexamples/limits:** (a) the branch has the same `commitSession.ts:137–154,233–248` automatic-prefix-retry defect as placement; its suffix test queues B before awaiting retry and does not assert the post-retry/no-transmission schedule; (b) submitting duplicate against observed Runtime official schema fails closed, irrespective of App's generic string op type; (c) a retired destination that is absent at today's head is not proven reusable merely because local capture sees absence. Strict reservation/history/ABA enforcement belongs to accepted server history and atomic admission.

Keep the ABA distinctions exact. Agent `test_recipe_occurrence_duplicate.py:105–139` refuses intervening whole-row/source-clips publications on ordinary replay and all four tested scopes on inverse, but deliberately permits equal-value shot-ID/shot-payload subpath ordinary replay. PLAN's final-value dependent-edit rule permits that; it is not proof of globally strict replay ABA. Root identity reuse is separately strict: Agent `commit.py:503–621` and `tests/sdk/test_timeline_commit_graph_roots.py:97–148` retain retired root reservations and exempt only authenticated inverse restoration. App adds no historical guard and does not establish project-wide collision protection. Agent itself notes at `commit.py:552–555` that Runtime atomic admission must additionally check project-wide shot occupancy/reservations. Require real duplicate create→undo/delete→ordinary reuse refusal, restart, and competing/cross-timeline destination coverage; do not weaken existing inverse or reservation expectations to admit it.

Required next gates: integrate the final Agent recipe/compiler via its owner; publish the matching Runtime official union/generated resources/provider release and App pin; narrowly reconcile the staged primitive/session delta and unit 3 scheduling semantics while retaining current safety tests. Then prove real RAW readback at the actual destination, shared-source isolation, dependent original guards, conflict retention, retired-ID reservations/ABA, reload/undo/redo and lost-ACK exact retry. Only afterward migrate the original duplicate UI caller and remove its graph-publish writer in the same gated change. The original 135-test positive behavior set must remain intact.

## 3. ACK-loss scheduling: approve the minimal fix

References use `5fe884946`. Product diff is only 8 added/2 deleted lines in `commands/commitSession.ts`. `pump(retryPending = true)` at `:88` retains existing explicit transmission entry points. The append callback uses `pump(false)` at `:201`; `:103–108` sees an existing flight, publishes retry, and returns before dispatch. The append is already durable. No frozen request, identity guard, dependency suffix, outbox format, acceptance path or inverse authority changes. A currently running pump remains serialized by sending; ACK processing still waits for append chain before reading the suffix. Rejected prefixes still hit publishRefusal first. I found no new counterexample in those paths.

`commitSession.test.ts:231–341` adds the exact missing chronology: A is accepted by the fixture, ACK is lost, session reaches retry, **then** a fresh B is captured. It asserts one POST before recovery, unchanged pending flight/body/key, B's entire original command/read/selection and after-A basis, no ready base, original H0 display, owner/scope exclusion, restart and explicit recovery, identical A wire bytes, fresh B key at HA with exact original command, projection and publication-targeted inverse request. Disk failure retains B's visible preview and durable A without ephemeral send. The refusal branch deliberately injects a conflict on exact A retry; it checks retention, not a claim that a real idempotency store may reject an already accepted same-key/same-body replay.

The helper changes record transmitted body text and apply actual compileTimelinePatch previews/recovery, rather than replacing recorder logic. All original session assertions and the 78 capture tests/28 Agent capture goldens remain unchanged; the test diff adds 113 lines, removes zero. The initial RED (115 pass/2 fail, expected retry but saved) and final 118-pass run are visible in retained logs. The intermediate correction changes only the new spy assertion to include its own deliberate stale-finish throw. No behavior is removed, skipped, weakened or marked passing through refusal.

Recovery, Retry and flush still authorize pumping (`:293–310`); undo refuses an uncertain flight (`:312–316`). This patch does not invent a phase-authority bypass. Actual UI callers must still prove they do not automatically flush after B, and the hook must permit the fresh gesture through its ordinary legacyClean fence. Native browser IndexedDB/locks, process restart, intervening Agent edit, real Runtime rebase/conflict and inverse are unverified here. Required next gate is the separate mounted after-ACK-loss Gate 5 journey on a pinned actual release tuple. The existing readiness handoff is `design/app-gate5-after-ackloss-readiness.md`; its source report records only lint/listing, not browser execution.

## Exact observed release gaps and current-tree protection

Read-only observations: App integration **1be0efdde5b9ec14f6ef85e0cbcd6bf6b27c80ff**; Agent integration **481e600ba0bc06a68362afb9c4f5e3c8f728606d**; Runtime integration **1f3e64d0c5f681d056dc0154748dbef5714cd6fa**.

- Runtime official `contract/schemas/edit-command.json:941` already declares **placement.move**; its SHA-256 is **472622c45fa6b5c7a425c949516a64a52d83192d3749e78a0f000decd088aee9**. Missing placement registration in Agent integration is **not** missing Runtime DTO support. Agent integration operations/validation currently admit clip.move, track.create/set and inverse/restore, not placement or duplicate. The reviewed Agent candidate has the additional recipes.
- Runtime's observed official schema does **not** dispatch occurrence.duplicate (nor placement.create/unplace); provider compatibility requires exact schema digest at `runtime_protocol/timeline_commit_provider.py:55–66`. Generated string types or test-only provider/schema registration are insufficient. I also inspected `hub/tl/rt-m2-duplicate-add-native-fixture`'s schema: it still shows placement.move, without duplicate. No official paired duplicate admission pass was established.
- Both staged App units pin Runtime **0.2.8**, digest **sha256:a4e1eebd0c86423db187a92198e9c47fa52063834101ee18af1ee10726afea4a**, matching the observed Runtime metadata. Current integration App still pins **0.2.1**, digest **sha256:4e52f7df017db99483ffcd0c593ce414b6443d5d0214ada943bb26fdfcc1714d**. Copying an old generated file or accepting both digests is not a coordinated pair.
- The staged package guard is Composition **0.0.10**; current App source pins **0.0.8**. Public **0.0.12** adoption and matching Agent Runtime/public12 release remain their own pending coordinated step. The read-only adoption report identifies artifact SHA-256 **0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3** and intended DEFAULT_THEME change. This review did not independently execute that package or qualify its deployment. Neither staged pass qualifies public12.
- `55e7e217b` is a broader staged feature tree, not current integration. Exact unit diffs add only 8 files/deltas apiece. Do not overwrite current commitSession/hooks/primitives with those whole branch files. Preserve integration's `commands/authoringBundle.sharedOpaqueRemap.test.ts`, `commands/fixtures/corpus/opaque_remap.json`, `hooks/useTimelineState.history-authority.test.tsx`, newer `useTimelineHistory.ts` boundary, accepted-projection helper fixes, opaque writer/runner tests and transition preservation. Those newer files are absent/different in the staged base; that absence is not authorized deletion. Current integration also lacks several stage prerequisites, so a raw patch is not itself a validated reconciliation.

## Evidence and commands

This worker ran **no tests**, installs, builds, tsc, browsers, live sockets or central requests, as required. There was sufficient retained source/RED evidence; no additional focused counterexample test was needed. Read-only review commands completed successfully: `git diff --stat/--numstat/--name-status`, exact `git diff BASE..UNIT -- PATH`, `git show REF:PATH`, `git grep`, source/log `rg`, and git-object `sha256sum` comparisons above. Searches with no matching registration are recorded as absence, not runtime execution.

Existing test inputs/expectations are retained by the exact deltas: placement only appends one hook test; duplicate edits no existing test; ACK-loss only appends session cases and improves its shared helper. Their new fixtures carry complete native inputs/records/closures. No guard table substitutes for capture execution, and the new RAW test does not relabel history.

The following are **prior worker executions**, checked against their reports and retained log summaries, not new runs by this reviewer. Commands are reproduced exactly below. Full original context lives under `workers/app-m2-placement-move-session-stage/notes/report.md`, `workers/app-m2-duplicate-native-binding-stage/notes.md`, and `workers/app-m2-ackloss-new-intent-unit/notes/report.md` (plus adjacent log.txt).

### Placement commands/results

Reported exit 0: 31 tests; broader 15 files/451 tests; final 3 files/58 tests. Final focused result is after the last tidy, not another disjoint cohort. Lint/diff/hash checks passed. Initial imported negative case was RED (23 pass/1 fail) and fixed in product without changing its expectation.

```sh
./node_modules/.bin/vitest run --config config/testing/vitest.config.ts src/tools/video-editor/commands/placementCapture.test.ts src/tools/video-editor/commands/commitSession.placement.test.ts --maxWorkers=2
```

```sh
./node_modules/.bin/vitest run --config config/testing/vitest.config.ts src/tools/video-editor/commands/placementCapture.test.ts src/tools/video-editor/commands/commitSession.placement.test.ts src/tools/video-editor/commands/commitSession.test.ts src/tools/video-editor/commands/commitSession.mixed.test.ts src/tools/video-editor/commands/commitSession.clipScalar.test.ts src/tools/video-editor/commands/commitSession.clipDelete.test.ts src/tools/video-editor/commands/commitSession.parentClipAdd.test.ts src/tools/video-editor/commands/commitSession.trackCreate.test.ts src/tools/video-editor/commands/commitSession.params.test.ts src/tools/video-editor/commands/commitSession.upgrade.test.ts src/tools/video-editor/commands/commitOutbox.test.ts src/tools/video-editor/commands/clipMoveCapture.test.ts src/tools/video-editor/commands/semanticGestures.test.ts src/tools/video-editor/hooks/useTimelineCommandSession.test.tsx src/tools/video-editor/hooks/useTimelineCommandSession.projection.test.tsx --maxWorkers=2
```

```sh
./node_modules/.bin/vitest run --config config/testing/vitest.config.ts src/tools/video-editor/commands/placementCapture.test.ts src/tools/video-editor/commands/commitSession.placement.test.ts src/tools/video-editor/hooks/useTimelineCommandSession.test.tsx --maxWorkers=2
```


### Duplicate commands/results

Reported exit 0: 13 files/352 tests plus 7 files/88 tests = **440 unique tests**, including the original nine-file 135 set; final new-only 3 files/44 tests after test annotations. Lint/diff passed.

```sh
node_modules/.bin/vitest run --config config/testing/vitest.config.ts src/tools/video-editor/commands/occurrenceDuplicateCapture.test.ts src/tools/video-editor/commands/occurrenceDuplicateGesture.test.ts src/tools/video-editor/commands/commitSession.occurrenceDuplicate.test.ts src/tools/video-editor/commands/clipMovePrimitives.test.ts src/tools/video-editor/commands/authoringBundle.test.ts src/tools/video-editor/commands/authoringBundle.moveOpaque.test.ts src/tools/video-editor/commands/clipMoveCapture.test.ts src/tools/video-editor/commands/commitSession.test.ts src/tools/video-editor/commands/commitSession.mixed.test.ts src/tools/video-editor/commands/commitSession.upgrade.test.ts src/tools/video-editor/commands/commitSession.trackCreate.test.ts src/tools/video-editor/hooks/useTimelineCommandSession.test.tsx src/tools/video-editor/hooks/useTimelineCommandSession.projection.test.tsx --maxWorkers=1
```

```sh
node_modules/.bin/vitest run --config config/testing/vitest.config.ts src/tools/video-editor/data/shotComposition.test.ts src/tools/video-editor/data/shotCompositionEditor.test.ts src/tools/video-editor/data/shotCompositionProjection.test.ts src/tools/video-editor/hooks/useFinalVideoAvailable.test.ts src/tools/video-editor/components/AstridTimelineEditor.document-shots.test.tsx src/tools/travel-between-images/pages/LocalTimelineShotBrowser.test.tsx src/tools/video-editor/lib/shot-group-pack-commands.test.ts --maxWorkers=1
```

```sh
node_modules/.bin/vitest run --config config/testing/vitest.config.ts src/tools/video-editor/commands/occurrenceDuplicateCapture.test.ts src/tools/video-editor/commands/occurrenceDuplicateGesture.test.ts src/tools/video-editor/commands/commitSession.occurrenceDuplicate.test.ts --maxWorkers=1
```


### ACK-loss commands/results

Same command: initial RED **115 pass/2 fail**, final **118 pass, exit 0**. Existing 37 session cases plus 3 new, and 78 capture cases. Lint/diff passed.

```sh
node_modules/.bin/vitest run --config config/testing/vitest.config.ts --maxWorkers=1 src/tools/video-editor/commands/commitSession.test.ts src/tools/video-editor/commands/clipMoveCapture.test.ts
```

No actual Runtime acceptance, server inverse execution, browser/native durability, full suite or public12 qualification is claimed by any of these unit counts. Recommendation: land the current-base scheduling fix through the normal queue; reconcile and qualify placement and duplicate as two separate later units after their explicit prerequisites/gates. Do not merge a large staged cohort.
