# App P2/P3 farm handoff

## Scope and source

This is a read-only inventory for the original three-products gesture tour (P2) and PLAN-v1 §6 gate 5 (P3). No browser, live-socket, Runtime, Agent, or acceptance suite was run. App source is clean at commit `c85da5427944d26242c71e503516d8d203a5f7a7`, tree `8666399f23cd10adde62e36b3429aea4bf7375de`, branch `tl/ap2-P2-P3-farm-readiness-r2`. The required integrated Agent and Runtime SHAs are runtime inputs (`TIMELINE_BUNDLE_AGENT_HEAD` and `TIMELINE_BUNDLE_RUNTIME_HEAD`), not present in this App-only source inventory; do not make a farm claim until those exact full SHAs are recorded.

## Existing runner

The existing runner is `npm run test:e2e:three-products`, configured by `playwright.three-products.config.ts` (`testMatch: 'three-products*.spec.ts'`, one worker, 300 s timeout). The central named suites are:

- `e2e-m1-gesture`: `npm run test:e2e:three-products -- --grep 'M1 real'`
- whole three-products file: `npm run test:e2e:three-products` (central `full-e2e-three-products`; not run for this handoff)

There is no dedicated current P2 selector. `e2e-m1-gesture` selects the M1 gesture and dependency-conflict cases, and also selects the Gate-5 title because it contains `M1 real`; it is not a P2-only tour. Do not add a launcher or narrow the proof to a substitute selector.

## P2: three-products gesture mapping

Every row that becomes P2 farm proof must capture the real POST to `COMMITS` and verify, in order: the expected command, no old-route POST (`SAVES`, `/composition-revisions`), only the intended document fields changed, reload/reopen preserves the pending/accepted state, and Runtime Undo emits the guarded `timeline.inverse` for the accepted publication. The existing `faultFirstCommit`, `commandOutboxes`, `history`, `accepted`, `revisionState`, and `expectImmutableClosure` helpers in `tests/e2e/local/three-products.spec.ts` are the available evidence surface.

| P2 gesture / expected commit | Current source and title | Intended-field delta | Current status |
| --- | --- | --- | --- |
| App track label: `track.set`, `select: parent/track:V1`, label only | `tests/e2e/local/three-products.spec.ts:408`, `agent -> open App: an Astrid task and its publication appear in the open App without a reload`; body assertion at 469–471 | `config.tracks[id:V1].label` only | Existing mixed Agent/App case; it does not yet prove Runtime `/commits` old-route absence, reload, or Undo for this gesture. |
| Single move: `clip.move`, `select: parent/clip:<appClipId>`, `args.on` | `three-products.spec.ts:1002`, `M1 real gesture...`; capture/order helper `prepareDependentMoves` at 888–914 | The selected parent clip's authored `at` only | New-path retry/reload/Undo coverage exists; add the Runtime `/commits` check below before calling it P2 proof. |
| Ordinary extension batch: the exact ten-command batch asserted at 1278–1290: five `clip.move` plus five `clip.set` commands for the parent and occurrence clips | `three-products.spec.ts:1239`, `M2 ordinary extension batch...` | Only the listed clips' `at`/`hold` values; Agent track label is a separate dependent intent | Existing new-path retry/restart/guarded Undo and `wire.legacy=[]`; Runtime history classification is missing. |
| Native manual ADD: `clip.add-media`, `select: parent`, selected verified media, row at the requested placement | `three-products.spec.ts:1410`, `M2 real mounted manual video drop...`; exact assertions at 1562 onward; producer is `parentClipAddMediaPort` in `src/tools/video-editor/commands/commitSession.ts:433` | One new media asset/clip row with its authored track, placement, type, and asset identity; no existing row or opaque data mutation | Existing refusal, native recovery, retry/restart, and Undo; add Runtime `/commits` classification and explicit allowed-field comparison. |
| Occurrence duplicate: `occurrence.duplicate`, source occurrence select, reserved copied occurrence/shot IDs | `three-products.spec.ts:1888`, `M2 native occurrence duplicate...`; exact body at 1924 | New occurrence/shot and copied authored fields only; source occurrence remains unchanged | Existing new-path network check, retry/restart, and guarded Undo; Runtime `/commits` classification is missing. |
| Native transition clear: `None` single/bulk paths, the existing command body is inspected by `expectRecordedTransitionClears` / `expectTransitionClear` | `three-products.spec.ts:2253` and `2331`, `M2 native None single/bulk...` | Only the selected transition's raw mirrors (single) or the explicitly selected transition IDs (bulk) | Existing exact retry, reload, restart, conflict/refusal, and Undo; classify the `/commits` delta and keep the atomic command list exact. |
| Selected element/parameter: `clip.set-params` (or the already-supported element command), selected clip only | `tests/e2e/local/three-products.selected-param-dev.spec.ts:25`, `local DEV selected PARAM uses admitted P1 through P2 removal, refusal, retry, reload and undo`; capture implementation `src/tools/video-editor/commands/elementCapture.ts:215–270` | Only the selected clip's admitted parameter/element fields; refusal produces no new commit | Existing DEV selected-parameter coverage, not the seeded three-products farm proof; keep it as supporting coverage until A3 wires the same path into the farm case. |

Popup swap is not currently represented by an App three-products journey. The real implementation surface is `parentClipSwapMediaPort` in `commitSession.ts:509`, `captureParentClipSwapMedia` / `finishParentClipSwapMedia` in `src/tools/video-editor/commands/parentClipSwapCapture.ts`, and expected command `clip.swap-media`. A3 must supply the real popup gesture case; the Agent CLI swap in the 408 test is not App popup-swap evidence. Its delta must be the target clip's asset replacement plus the selected old/new media identities only, followed by the same reload/Undo checks.

The original three-products tests at 495 (`concurrent edit...`) and 665 (`Runtime restart...`) still intercept `SAVES` and assert snapshot-route behavior. They are migration coverage, not current P2 proof. Once A2 removes that route, retain their passing behavior expectations as strict expected-to-fail tests with the migration requirement named, per the project rule; do not rewrite them to expect refusal or delete them.

## P3: gate-5 journey

The current candidate is `tests/e2e/local/three-products.spec.ts:1115`, `M2 real gate 5 (M1 real mounted path): Agent edit, lost ACK, newer local gesture, exact retry, restart and undo preserve intent`. Its existing sequence is the required new path: App A accepted; independent Agent C; A durable response is lost; App B is authored after the lost ACK; reload; Runtime restart; exact A bytes/key/receipt retry; B rebases with a fresh key/base; C remains; guarded Undo inverses B. It already asserts `wire.legacy=[]`, outbox ordering, opaque preservation, history growth, immutable closure, and Agent revision visibility.

The one minimal missing farm assertion is authoritative Runtime history: snapshot `history(harness, seed3)` before A, after A/C/B recovery, and after Undo; inspect the new `/commits?limit=50` entries, not only the browser door log. Every gesture publication must have `intent: 'recorded'`, a non-null `records` payload, and a `receipt.command_kind` for the timeline commit; the post-bootstrap delta must contain no `intent: 'legacy_unknown'`, `records: null`, or `parent_composition.publish`. The final inverse entry must identify B in its undo record. The bootstrap test at 1642 intentionally has a baseline `parent_composition.publish`/`bootstrap` entry; exclude that pre-gesture baseline rather than treating it as a legacy leak.

## Minimal A2/new-path instrumentation

Add only inline assertions to the existing `three-products.spec.ts` cases/helpers after A2/A3 integration:

1. Before each gesture, call the existing `history()` helper; after acceptance/recovery and after Undo, call it again and compare the new entry IDs.
2. Keep the existing `wire.legacy`/`legacyPosts` network assertion. In the same interval, reject any new Runtime `/commits` entry classified as `legacy_unknown`, null `records`, or `parent_composition.publish` (with the bootstrap exception above). This is the required network **and** Runtime check; a door/audit log alone is insufficient.
3. Compare the accepted canonical document/records using the existing `revisionState` and command records. Assert the per-row allowlists above, including no source-row mutation for duplicate and no unrelated parent/opaque changes for ADD/swap/parameter gestures.
4. Reuse the current `faultFirstCommit` transport fault, persisted outbox, reload, `harness.restartRuntime()`, and visible `Undo` button. Do not change selectors, timeout, mocks, or retry behavior.

## Owners and dependencies

- A2/App: route all gesture writers through the existing commit session/provider and outbox; preserve dependent-intent chaining, exact retry, refusal/revalidation, and Runtime history semantics.
- A3/App: qualify popup ADD/SWAP, placement, element/parameter, and asset-registration consumers through A2. Popup SWAP remains the concrete missing farm case.
- R2/Agent: provide the integrated guarded whole/per-step Undo behavior consumed by P3; current App source alone cannot establish it.
- Runtime: keep `/commits` authoritative and retire/mark legacy snapshot writes; farm proof must use the integrated Runtime head and distinguish intentional bootstrap history.
- Integration: provide exact full Agent/Runtime SHA variables plus the required farm seed/project; this worktree does not contain those dependencies.

## Evidence from this inventory

Static commands run, with no acceptance claim:

- `git status --short --branch` — clean `tl/ap2-P2-P3-farm-readiness-r2`.
- `git show -s --format='commit=%H tree=%T' HEAD` — App commit/tree recorded above.
- `rg -n ...` over the current specs and command captures — confirmed operation names, source symbols, and current test titles.
- `npx playwright test --config playwright.three-products.config.ts --list tests/e2e/local/three-products.spec.ts tests/e2e/local/three-products.selected-param-dev.spec.ts` — listed 14 tests in 2 files; listing only, no test execution.

No P2/P3 test, browser, live socket, Runtime, Agent, or farm suite was run. Recommended next step is to apply the minimal `/commits` assertions on the integrated A2/A3/R2/Runtime heads, then run the existing central named suite(s); this handoff does not certify those future runs.
