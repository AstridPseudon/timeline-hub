# Local history authority audit

**Finding: accepted data can still be rewound locally through undo and redo when an accepted remote publication has the same authored content as the displayed unsent edit.** The mounted assembly emits `scheduleSave` without sending `timeline.inverse`. This violates PLAN decision 6 and the App M2 mission. No product changes were made; the RED reproductions remain outside the committed suite as requested.

Audited worktree: `/home/user/work/wt/app-m2-local-history-authority-audit`, HEAD `066b651b9b9f76ec9bdaf053dc663eff6e7c08fa` (assigned opaque-current qualification base). Read PLAN, App manager BRIEF, history/state/command-session/save/persistence hooks, commitSession/outbox, keyboard, toolbar, browser facade and TimelineOps checkpoint/rollback. KEEP exists in the worker directory. Git status is clean.

## Executable counterexample

Artifacts, all outside the repo:

- `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-local-history-authority-audit/notes/useTimelineState.history-authority.test.tsx`
- `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-local-history-authority-audit/notes/run-repro.sh`
- `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-local-history-authority-audit/notes/repro.log`

The script temporarily copies the reproduction into this worktree for normal Vitest resolution, refuses to overwrite an existing file, and removes its copy on exit. It accepts an optional worktree path followed by Vitest flags. It does not change configuration or an existing test.

The reproduction mounts **real useTimelineState**, including its real store slices, useTimelineSave/useTimelineCommit/useTimelineHistory/useTimelineCommandSession, commitSession and IndexedDB outbox. It uses the existing `commitSessionEnvironment` raw canonical-closure fixture and actual RuntimeDataProvider/transport parsing. Only query delivery and the unrelated render-state hook are stubbed. No save status or accepted/local projection fact is assigned by the test. Ordinary snapshot writes use the existing explicit `TimelineSchemaIncompatibleError('timeline_commit_required', [])` refusal setup from `useTimelineCommandSession.test.tsx`; no retired endpoint succeeds.

Undo case:

1. Start at r0/p0 with clip x at 1 and no owned accepted publication in the editor's history. The fixture's raw document is normalized up front so both producers can author identical bytes; the parent digest is recomputed normally.
2. Use the actual command facade's ordinary `updateClip` to move x to 5. Its snapshot write is refused, the draft at 5 is retained, the displayed data has no accepted fact, and local undo is available.
3. A separate editor session using the same fixture identity accepts a semantic move to 5 through command capture, the provider and HTTP fixture. Deliver its actual raw closure/head through the query input.
4. Assert the authored stable signatures are equal and wait for the mounted command-session projection to produce **accepted r1/p1**. This is real acceptance, not a save-status inference.
5. Invoke assembled `chrome.undo`. Actual: x becomes **1**, accepted fact becomes **undefined**, `scheduleSave` count increases **1 -> 2**, and the Runtime commit count does not increase. A fresh immutable closure read still has x at **5**.

Redo case: first undo the refused local edit, creating a redo entry for x at 5. The separate editor accepts a same-value move at 1, producing **r0/p1** (same revision, new publication). The assembled accepted projection is at 1. Local redo changes it to **5**, drops the accepted fact, emits another `scheduleSave` (**2 -> 3**) and sends no Runtime inverse. The server closure remains at 1. This also proves revision identity alone is insufficient.

These are UI/config rewinds and legacy-save scheduling, **not evidence of a successful server overwrite**. The 410-equivalent refusal remains in force. With `schemaIncompatible` already set, persistence creates the scheduled draft before its schema guard, then refuses another network save (`useTimelinePersistence.ts:949`, `:1030`, `:1093`). The emitted event is measured directly; post-rewind draft replacement is source-traced, not separately asserted by the RED tests.

## Exact path and exclusions

| Ingress or state | Outcome and evidence |
|---|---|
| Toolbar undo/redo | Calls `chrome.undo/redo` (`TimelineEditorShellToolbar.tsx:99`, `:111`). Uses the same assembly callback as the reproduction. |
| Keyboard | Shell passes chrome callbacks (`TimelineEditorShellCore.tsx:346`); `useKeyboardShortcuts.ts:224`/`:230` dispatch them. Actual keyboard undo of an owned accepted edit passed the mounted control. |
| Browser command facade | `browser/hooks.tsx:248`/`:249` exposes chrome callbacks, so it inherits the same ownership decision. `createTimelineCommands` supplies the edit producers, not an independent undo API. |
| No command ownership + accepted identical-content replacement | **Defect.** `useTimelineHistory.ts:407` returns immediately on equal stable signatures. `useTimelineCommandSession.ts:47` only gains ownership from active work or `canUndo`; observing a remote accepted projection does not itself gain ownership. `useTimelineState.ts:1299` therefore leaves local undo/redo callbacks installed. |
| Snapshot restore | `useTimelineHistory.ts:303` calls `commitData(..., {save:true, skipHistory:true})`. Commit checks pending-command blocking, drops any inherited accepted fact, replaces local data and emits `scheduleSave` (`useTimelineCommit.ts:344`, `:349`, `:407`). No accepted-history guard exists there. Media command-history failure can also fall back to a snapshot (`useTimelineHistory.ts:282`), but that fallback was source-reviewed rather than independently reproduced. |
| Owned accepted move A | **Runtime inverse, no snapshot writer.** Assembly override (`useTimelineState.ts:1303`) calls the existing session undo; `commitSession.ts:324` enqueues `timeline.inverse` naming the accepted publication. Both direct chrome and real keyboard controls passed. Redo stays disabled/no-op. |
| Uncertain A + queued dependent B | **Retained local draft, not an accepted rewind.** A5/B7 stays local at original r0/p0. Reload rejects while command session is active (`useTimelineSave.ts:329`); undo rejects uncertain pending work (`commitSession.ts:310`). |
| A ACK after independent C | A is retried with identical body/key; B uses base r1/p1 and its original A5 value guard. C causes B's typed conflict; B remains displayed at 7 with its original local fact. Exact request/base/guard assertions pass in the assembled control. Outbox promotes only the dependent base on ACK and retains rejected work (`commitOutbox.ts:259`). |
| Recovery of conflicted B | Remount against a fresh actual C closure offers the persisted owner. Recovery restores B7 with original local r0/p0 display basis, retains the conflict, sends no new request and still blocks reload. Mounted control passes. |
| Ordinary refused edit after owned accepted A | Chrome undo still sends the Runtime inverse of A. It does not locally restore a legacy snapshot. The separate ordinary draft (label plus A5, base r1) remains byte-for-byte retained after the inverse projects accepted r2/p2; no extra scheduleSave occurs. Mounted control passes. This is distinct from the accepted-echo defect. |
| Different-content remote acceptance / conflict reload | Remote-commit event clears the local stacks when the signature differs. Existing original boundary tests pass. True same-head URL refreshes deliberately keep history; that behavior must remain. |
| Local checkpoint jump / TimelineOps.rollback | Generic history can restore a snapshot via the same `save:true` path (`useTimelineHistory.ts:488`, `useTimelineOps.ts:337`); jump is not replaced by the command ownership override. **No reachable Runtime checkpoint counterexample claimed:** RuntimeDataProvider implements neither saveCheckpoint nor loadCheckpoints, and the Runtime history menu selects canonical history instead. No checkpoint capability was invented for the fixture. |
| Canonical history menu restore | Routes through provider `shotComposition.restoreHistory`, not local snapshot jump (`useTimelineHistory.ts:580`, `dataProvider.ts:226`). Existing provider path uses current-head Runtime restore. Source-reviewed here; no live Runtime/menu journey claimed. |

## Tests

All commands run from `/home/user/work/wt/app-m2-local-history-authority-audit` unless otherwise stated.

```sh
./node_modules/.bin/vitest run --config config/testing/vitest.config.ts src/tools/video-editor/hooks/useTimelineCommandSession.test.tsx src/tools/video-editor/hooks/useTimelineCommandSession.projection.test.tsx src/tools/video-editor/hooks/useTimelineHistory.remote-boundary.test.tsx src/tools/video-editor/hooks/useTimelineHistory.test.ts
```

**PASS: 4 files, 43 tests.** All original raw-closure, opaque-root, accepted/local-fact, recovery and history assertions are unchanged. No tests were weakened, deleted, skipped or marked expected-to-fail.

```sh
./node_modules/.bin/vitest run --config config/testing/vitest.config.ts src/tools/video-editor/hooks/useTimelineOps.test.ts src/tools/video-editor/hooks/useKeyboardShortcuts.test.tsx src/tools/video-editor/browser/hooks.test.tsx src/tools/video-editor/components/TimelineEditorShellToolbar.test.tsx
```

**PASS: 4 files, 64 tests.** Log: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-local-history-authority-audit/notes/ingress-tests.log`.

```sh
bash /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-local-history-authority-audit/notes/run-repro.sh
```

**Expected RED: 1 file, 2 failing reproductions, 4 passing assembled controls; exit 1.** Each failing test has three soft assertions reporting the bad config value, removed accepted fact and extra scheduleSave. All setup/closure/signature assertions and the fresh server read pass. Final log is `notes/repro.log` at the absolute path above.

No full suite, browser, localhost service, install, build or tsc was run. Tests use jsdom and an in-process HTTP fixture; they prove App ingress/routing and closure handling, not live Runtime inverse semantics. No cohort/metadata gate claim is made.

## Small fix plan for the manager

1. Make the existing remote-history boundary recognize accepted publication/provenance changes even when authored signatures match. Cover both r0/p0 -> r1/p1 and same-revision r0/p0 -> r0/p1. Preserve original same-head URL-refresh history expectations and clean unsent local undo.
2. Ensure assembly/local-history eligibility cannot expose an old accepted snapshot as unsent work after that boundary. Continue using the existing Runtime inverse for owned accepted publications; do not add a second inverse implementation or substitute saveStatus for accepted/local facts. Preserve A/B pending/recovery guards and the separate refused draft.
3. Promote the two RED cases into permanent focused assembly tests when that fix is authorized, retain the four controls and all original assertions, and qualify through the manager's gates. No product fix or permanent test addition is included in this audit.

No settled plan decision needs changing. This is an implementation gap against decision 6. The audit is complete; the defect needs a separate authorized fix. No environmental blocker remains. The worktree is unchanged, and the runner leaves no build output or temporary test behind.
