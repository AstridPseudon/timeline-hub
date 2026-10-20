# Independent parent-delete029 and parent-split029 source review

Review base: `c866da88e6acb92e6f7194324e0a29bfacab3b4b`. Read PLAN first. Reviewed the two refs independently using `git show/diff` and separate `git archive` snapshots; no merge, checkout, commit, push or product edit. These are source-unit verdicts only.

| Unit | Exact reviewed SHA | Verdict |
| --- | --- | --- |
| `tl/app-m2-parent-delete029-source-slice` | `a84f1c0c890113bf93f9a5213f9f340a877fa288` | **HOLD — one reproduced eligibility regression** |
| `tl/app-m2-parent-split029-source-slice` | `d1111fd3b05acac5c72f656cd62faae5e60466be` | **APPROVE — staged single-parent source unit only** |

Neither verdict approves an entire branch/cohort, writer retirement, M2 completion, group/occurrence coverage, zero legacy traffic, or actual Runtime/Agent paired acceptance. Missing paired acceptance is an activation limit, not the reason for the delete HOLD.

Source-unit author reports (reviewed separately): [delete](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-parent-delete029-source-slice/notes/report.md), [split](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-parent-split029-source-slice/notes/report.md). Exact independent allowlists: [delete](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-parent-delete-split029-review/notes/delete-allowlist.txt), [split](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-parent-delete-split029-review/notes/split-allowlist.txt).

## Delete finding D1 — P2: authored opaque metadata disables a supported parent delete

**Location:** delete SHA `src/tools/video-editor/commands/commitSession.ts:333–336`; routed by `hooks/clip-editing/useClipDeletion.ts:34–42` and `hooks/useTimelineCommandsService.ts:853–860`.

A real raw parent row `x`, under the matching project/timeline/head, may contain authored `app.canonical` data. The native recipe reads and guards that complete row without assigning ownership to that namespace. The new session instead demands that any non-null `app.canonical` contain exactly the parent identity fields. For example, `{canonical: {ownerRef: 'opaque-owner', clipRef: 'literal', rawClipId: 'literal'}}` makes `handleDeleteClip('x')` emit **“Delete requires one raw parent clip identity”**, with no preview/delete, once the supplied native port is present. The unchanged existing UI writer succeeds for exactly the same input. This is a supported single-parent operation being intercepted into a false unsupported failure, not an occurrence or native dependency refusal.

Reproduction: [/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-parent-delete-split029-review/parent-delete029.counterexample.test.tsx](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-parent-delete-split029-review/parent-delete029.counterexample.test.tsx:1), an ordinary test **outside notes**, with normal positive expectations and no skip/xfail/fails marker. Result: **2 passed / 1 failed**, exit 1. The passing controls prove portable native capture/finish and the original UI writer accept the opaque row; the failing case is the real new session port through the UI hook. Independent current-native Python case `delete: opaque canonical metadata` also accepts the row and restores it by inverse. Log: [/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-parent-delete-split029-review/notes/counterexample.log](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-parent-delete-split029-review/notes/counterexample.log).

Recommended correction: prove parent eligibility from the authenticated raw authoring closure and known display binding; keep authored `app.canonical` opaque. Do not simply broaden occurrence support, parse display-ID suffixes, or add a catch-and-snapshot fallback. Retain this positive regression and requalify the bounded delta. No product fix was made in this review.

The rest of the bounded delete implementation checks out: exact native command/whole-row guard/record/after state, original collection order/membership reads, final-row mirror removal, immutable original claims, current-closure replay without recapture, mixed `TimelineOps` atomic refusal, visible refusal with retained drafts, and one durable session/outbox. **17 files / 492 passed** independently reproduced; **+361 net product lines** verified. The entire original `useClipEditing.test.ts`, including the successful grouped assertion at **line 261**, is byte-identical to base and passed. Group/multi UI and shot-menu service positives with a native port supplied also passed. Keyboard/group expansion, prepared-media removal and unavailable-port consumers retain their existing paths. General occurrence routing and native group deletion remain unqualified; no full deletion claim is made.

## Split source assessment — no blocking finding

- `commands/commitSession.ts:324–342` requires the matching display head, one actual raw parent row, a literal stable ID and unoccupied caller-reserved right ID. It does not derive a parent ID from a projected/display suffix. Its parent-only context is explicit; it does not qualify arbitrary occurrence aliases or ambiguous displays. Authored `app.canonical` stays opaque.
- `commands/clipSplitCapture.ts:189–328` follows the native recipe: source registry read; unsupported native shapes refused; exact source-window/speed and literal `for` updates; rational-FPS/half-open checks; create-after membership/order/boundaries; one caller-reserved right ID; complete recorded writes/reads/bindings/created IDs. No App-side inverse semantics were added.
- `commands/commitSession.ts:344–371` replays the original full capture on current raw bytes, uses the existing prepared map and durable enqueue, validates the exact native preview, and fences duplicate completion/submission with generation and basis checks.
- `commands/clipSplitGesture.ts:50–89` installs complete native left/right rows using the existing `assembleTimelineData`, preserving the existing resolved media entry. The mounted hook uses `commitData(save:false, skipHistory:true)` exactly once, including the same recovery adapter; it does not schedule a snapshot save.
- All existing context-menu, keyboard, generic operations, split hooks and SDK facade producers are unchanged. Original group/multi/occurrence producers are not switched to the staged native split port. No existing positive expectation or failure marker was changed.

Independent focused rerun: **12 files / 296 passed** (includes all four new split suites, existing session/outbox, grouped editing, mounted projection and opaque-remap neighbors). Original worker report records 18 files / 564 passed plus final 4 files / 76 passed; those larger counts are prior evidence, not this review's rerun. **+516 net product lines** verified. The exact native golden and all six native split cases below agree; inverse and redo restore exact authored bundles.

## Native parity and lifecycle evidence

Native reference: read-only `/home/user/work/agent` at `c456b3281497653cecf44f61acd6fa30565d83c8`, existing dependencies-only venv, `PYTHONDONTWRITEBYTECODE=1`. Public Composition dependency is 0.0.12; shared dependencies were not modified.

The independent native script generated **11 cases (5 delete / 6 split)**. Both App primitives matched the current native **command, complete record and complete after bundle** for every case; JSON persistence/replay and input immutability also matched. Cases include the exact frozen goldens, final-row deletion/colon IDs, config-only collections, opaque `__proto__`/`constructor`/`prototype` own data, opaque canonical data, original collection order, raw fractional source windows, null speed/hold/params, and rational FPS. Existing focused tests additionally exercise membership/order/source/opaque claim changes and split frame boundaries. Native guarded inverse restores all 11 original bundles. See [/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-parent-delete-split029-review/notes/native-parity.py](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-parent-delete-split029-review/notes/native-parity.py), [/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-parent-delete-split029-review/notes/native-parity.log](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-parent-delete-split029-review/notes/native-parity.log), [/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-parent-delete-split029-review/notes/app-native-parity.log](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-parent-delete-split029-review/notes/app-native-parity.log).

**Separate native qualification limitation:** split redo verified for all six split cases. Calling the standalone conformance `inverse()` helper again on each delete inverse raises `history_unavailable: inverse insertion order needs an accepted boundary`, including on the unchanged original delete golden. The initial failed probe is retained as `native-parity-initial.log`; the final script records that native limitation explicitly. This is not an App implementation mismatch, a changed semantic expectation, or proof of actual accepted-history redo. Agent/history qualification should determine the required accepted boundary; no native behavior was rewritten here.

Original focused session tests verify exact pending bytes/key across ACK loss/reload, original guarded dependent suffixes, refusal retaining the draft and publication-based inverse requests. Split tests also verify unchanged reserved created IDs, abandoned capture and duplicate finish/submit. Two supplemental delete lifecycle tests independently prove that abandoned prepared work produces no preview/request/outbox intent, and duplicate finish is identical while only one submission is retained. **2 passed**, exit 0. This is cancellation by abandoning an unsubmitted capture, not a new cancel protocol or proof of server cancellation.

## Shared-session interaction review, without merging

Both units add operation ports to the **existing** `createTimelineCommandSession`; neither adds another engine, session, outbox, persistence owner, commit pump, compiler, provider or wire schema. Prepared-map keys contain complete commands (including operation/created IDs); both units share `localGeneration`, original `localBasis`, synchronous authored-state advancement and durable dependency ordering. A later submitted unit invalidates an earlier prepared basis. Ordinary move/label paths remain intact.

The **entire original pump/after-ACK body is byte-identical** to base in both refs, including the queued-append generation check that prevents an ACK from erasing a newer edit. Outbox, recovery, authoring conversion, move primitives, SDK/settings/generated clients, public12/current029 pins, new-M2 journey and render/runtime closure were not imported or replaced. Split's preview adapter is operation-specific and must coexist with the ordinary clip-remove/label/move preview compiler when these deltas are eventually combined. No combined split→delete/move journey or merged source tree was tested or approved. The delete opaque-metadata finding must be resolved before relying on their future shared flow.

`authoringBundle.ts` is unchanged: item/source ID remapping is confined to known item identity and `metadata.source_item_id` / `source_item` sites. Opaque namespaces and arbitrary strings are not remapped. Existing opaque/remap tests passed on split. Future `authoringRefs`/source-ID binding work must use verified context/identity maps; this review supplies no global binding authority or display-ID guessing.

## Exact verification commands and results

All Vitest executions used public12 dependencies through **new private snapshot/worker symlinks**, `--maxWorkers=1 --configLoader=runner --no-cache`. No symlink/file inside a shared dependency directory was changed. The runner only supplies the existing config's `__dirname`. Source snapshots were under the assigned worker directory and were removed after testing; the assigned product worktree remains clean. Recreate the exact snapshots and private dependency links before replaying commands with `python /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-parent-delete-split029-review/notes/prepare-snapshots.py`. Evidence/configs/scripts and the ordinary counterexample are retained.

Delete focused command, exit **0**, 17 files / **492 passed**:

```sh
cd /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-parent-delete-split029-review/notes/delete
node --require /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-parent-delete-split029-review/notes/runner.cjs node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 src/tools/video-editor/commands/clipDeleteCapture.test.ts src/tools/video-editor/commands/clipDeleteGesture.test.ts src/tools/video-editor/commands/commitSession.clipDelete.test.ts src/tools/video-editor/hooks/useTimelineOps.clipDelete.test.ts src/tools/video-editor/hooks/useClipEditing.test.ts src/tools/video-editor/hooks/useTimelineCommandSession.test.tsx src/tools/video-editor/commands/clipMoveCapture.test.ts src/tools/video-editor/commands/trackLabelCapture.test.ts src/tools/video-editor/commands/trackLabelGesture.test.ts src/tools/video-editor/commands/semanticGestures.test.ts src/tools/video-editor/commands/commitSession.test.ts src/tools/video-editor/commands/commitOutbox.test.ts src/tools/video-editor/hooks/useTimelineOps.test.ts src/tools/video-editor/hooks/useTimelineOps.trackLabel.test.ts src/tools/video-editor/lib/keyboard-delete.test.ts src/tools/video-editor/hooks/useTimelineState.history-authority.test.tsx src/tools/video-editor/hooks/useTimelineCommandSession.projection.test.tsx
```

Split focused command, exit **0**, 12 files / **296 passed**:

```sh
cd /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-parent-delete-split029-review/notes/split
node --require /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-parent-delete-split029-review/notes/runner.cjs node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 src/tools/video-editor/commands/clipSplitCapture.test.ts src/tools/video-editor/commands/clipSplitGesture.test.ts src/tools/video-editor/commands/commitSession.split.test.ts src/tools/video-editor/hooks/useTimelineCommandSession.split.test.tsx src/tools/video-editor/commands/commitSession.test.ts src/tools/video-editor/commands/commitOutbox.test.ts src/tools/video-editor/hooks/useClipEditing.test.ts src/tools/video-editor/commands/authoringBundle.test.ts src/tools/video-editor/commands/authoringBundle.moveOpaque.test.ts src/tools/video-editor/commands/authoringBundle.sharedOpaqueRemap.test.ts src/tools/video-editor/hooks/useTimelineCommandSession.test.tsx src/tools/video-editor/hooks/useTimelineCommandSession.projection.test.tsx
```

Independent native parity, exit **0**, 11 command/record/after/inverse matches; six split redos verified and five native delete redo limits explicitly recorded:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/user/work/agent /home/user/work/venv-agent/bin/python /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-parent-delete-split029-review/notes/native-parity.py > /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-parent-delete-split029-review/notes/native-parity.log 2>&1
```

Supplemental App parity, exit **0**, **11 passed**; delete lifecycle, exit **0**, **2 passed**; ordinary finding counterexample, exit **1**, **2 passed / 1 failed**:

```sh
cd /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-parent-delete-split029-review/notes/delete
node --require ../runner.cjs node_modules/vitest/vitest.mjs run --config ../parity.config.ts --configLoader=runner --no-cache --maxWorkers=1 > ../app-native-parity.log 2>&1
node --require ../runner.cjs node_modules/vitest/vitest.mjs run --config ../lifecycle.config.ts --configLoader=runner --no-cache --maxWorkers=1 > ../delete-lifecycle.log 2>&1
node --require ../runner.cjs node_modules/vitest/vitest.mjs run --config ../counterexample.config.ts --configLoader=runner --no-cache --maxWorkers=1 > ../counterexample.log 2>&1
```

Source preservation/allowlists/line census/primitive lineage/no-new-markers audit, exit **0**:

```sh
python /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-parent-delete-split029-review/notes/audit-source.py > /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-parent-delete-split029-review/notes/source-audit.log 2>&1
```

`git diff --check c866da88e6acb92e6f7194324e0a29bfacab3b4b <each exact unit SHA>` passed (invoked by that audit). Assigned-worktree `git diff --check` and `git status --short` are clean. Full per-file counts and SHA-256 values: [/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-parent-delete-split029-review/notes/source-audit.json](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-parent-delete-split029-review/notes/source-audit.json). Public12 package/peer hashes match the source worker's recorded hashes. During the supplemental checks, dependency/package/cache metadata snapshots `deps-current.json` and `deps-final.json` are identical. No pre-focused-run cache snapshot was taken by this reviewer, so no whole-run before/after cache claim is made. The initial counterexample run was a dependency-resolution setup error (0 tests), retained in `counterexample-initial-environment.log`; the corrected ordinary run is the 2-pass/1-fail result above.

No full suite, central test request, build, browser, project typecheck, install, live socket, Runtime pair, actual history restart, zero-legacy HTTP observation, or Player/export parity was run. Worker lint passes are prior evidence; lint was not rerun during this read-only review.

## Exact independent path allowlists

Delete (17 changed paths, +1,194/-4 total, **+361 product**):

```text
src/tools/video-editor/commands/clipDeleteCapture.test.ts
src/tools/video-editor/commands/clipDeleteCapture.ts
src/tools/video-editor/commands/clipDeleteGesture.test.ts
src/tools/video-editor/commands/clipDeleteGesture.ts
src/tools/video-editor/commands/commitSession.clipDelete.test.ts
src/tools/video-editor/commands/commitSession.ts
src/tools/video-editor/commands/fixtures/recipe_m2_app_clip_delete.json
src/tools/video-editor/hooks/clip-editing/types.ts
src/tools/video-editor/hooks/clip-editing/useClipDeletion.ts
src/tools/video-editor/hooks/useClipEditing.ts
src/tools/video-editor/hooks/useTimelineCommandSession.test.tsx
src/tools/video-editor/hooks/useTimelineCommandSession.ts
src/tools/video-editor/hooks/useTimelineCommandsService.ts
src/tools/video-editor/hooks/useTimelineOps.clipDelete.test.ts
src/tools/video-editor/hooks/useTimelineOps.ts
src/tools/video-editor/hooks/useTimelineState.ts
src/tools/video-editor/hooks/useTimelineState.types.ts
```

Split (12 changed paths, +3,936/-4 total, **+516 product**):

```text
src/tools/video-editor/commands/clipSplitCapture.test.ts
src/tools/video-editor/commands/clipSplitCapture.ts
src/tools/video-editor/commands/clipSplitGesture.test.ts
src/tools/video-editor/commands/clipSplitGesture.ts
src/tools/video-editor/commands/commitSession.split.test.ts
src/tools/video-editor/commands/commitSession.ts
src/tools/video-editor/commands/fixtures/clip_split_parity.py
src/tools/video-editor/commands/fixtures/recipe_m2_clip_split.json
src/tools/video-editor/hooks/useTimelineCommandSession.split.test.tsx
src/tools/video-editor/hooks/useTimelineCommandSession.ts
src/tools/video-editor/hooks/useTimelineState.ts
src/tools/video-editor/hooks/useTimelineState.types.ts
```

No whole old cohort was imported. Delete capture/gesture/golden match the reviewed `8361afef1` source; split capture matches `92cec8da6` apart from a trailing blank line, and its golden is byte-identical. The shared dependencies listed above are unchanged current-base modules, not copied older implementations.

## Handoff

No review-work blocker and no PLAN decision was changed. **Hold delete for D1**, request a narrow correction preserving the positive test and raw-parent-only scope. **Approve split as staged source only**. Before activating either unit, separately qualify its real current029/public12 Runtime/Agent UI journey, exact retry/restart and history behavior; retain existing unsupported group/multi/occurrence/media-removal writers until their own qualified replacements. Investigate the standalone native delete redo boundary with the Agent owner without rewriting App/native semantics. No whole-branch approval, retirement request, new failure marker or KEEP was created.
