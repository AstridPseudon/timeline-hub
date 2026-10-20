# Selected-server lifecycle independent re-review

**HOLD** on App `1c7345b702ee84cc627ed0bc03c82ae77364a50b` (`tl/app-m2-selected-server-lifecycle-fix`), compared with `b9c03ef5ba705312dc36f37f4b7b5fa7fd0a784c`. Recorded the exact branch SHA at start and verified it again at completion. All four original counterexamples are repaired, but a neighboring recovery sequence still loses the accepted selected value from the displayed/working closure. No product edits; review worktree stayed clean. This HOLD concerns reproducible local behavior, independently of outstanding paired qualification.

## Remaining blocker: ordinary acceptance hides earlier selected/inverse effects during recovery

`src/tools/video-editor/commands/commitSession.ts:566–568` decides whether to recover from accepted state solely from **the last accepted command's op**. The outbox retains only the last accepted prefix. An accepted ordinary command replaces that record even when its canonical closure still contains an earlier selected edit or inverse.

Two ordinary failing cases in this worker's `notes/probes.test.ts:74` prove the consequence:

| Sequence, followed by dispose/reopen at the actual current head and explicit owner recovery | Accepted seed before/after reopen | Projected seed after recovery |
|---|---|---|
| Pause selected 4→8; capture moves 5 and 7; ACK selected; ACK move 5; refuse move 7 | 8 | **4** (expected 8) |
| Accept selected 4→8; pause its inverse; capture moves 5 and 7; ACK inverse; ACK move 5; refuse move 7 | 4 | **8** (expected 4) |

Both probes first verify that all three intents were persisted before releasing the gate, that the accepted record's last command is `clip.move`, that its actual canonical closure has the correct seed, that the pre-reload projection is correct, and that the remaining refused move's original payload survives unchanged. After recovery they verify conflict status and exact retained-intent equality before failing only the final seed assertion. The projection spy rebuilds timeline data from the supplied basis; its omitted ordinary preview applies only a move, so it cannot account for a seed mismatch. These are synthetic normal-port session counterexamples, not native Runtime/browser proof or demonstrated accepted-server data loss.

The underlying issue is an incomplete recovery correction, not evidence that the settled server-authority decision is wrong. Recommended next step: make recovery preserve selected/inverse effects carried through later ordinary acceptances, while preserving the original ordinary-only B display controls and every original suffix capture/guard/pin. Promote these two red requirements into the existing main suite without weakening expectations. No speculative product correction was made here.

## Repairs independently confirmed

- Reran the requested eight-file cohort: **237 PASS**, including all original 232 cases, the four promoted requirements and the added successive-suffix cancellation control. The old selected test file is a byte-exact prefix of the new file; the other seven cohort files are unchanged by this repair.
- Copied the previous review's external `counterexamples.test.ts` byte-for-byte and ran it against this exact fixed source: **4 PASS**. Inverse ACK projects accepted seed 4 rather than stale 8; direct selected-ACK recovery retains seed 8; canceling an ordinary tail leaves the selected draft visibly pending with its unsent explanation; canceling the inverse suffix permits a fresh accepted capture at seed 4.
- One additional independent positive control passes: inverse ACK plus selected/ordinary suffix → reopen → original false accepted-basis flag, exact original retained inputs/pin/intent preserved → explicit successive cancellation → new capture at actual P2 with seed 4/true → new selected seed 6 submitted at P2 → newer ordinary move submitted at P3 with its original guard → final accepted seed 6/position 5. Selected `after` remains null and the display remains seed 4 before the new selected ACK.
- The original raw16 typed validation/refusal/conflict tests retain the selected draft and ordinary suffix; original body/key replay, V1-input/pin retention, unacknowledged-basis gating through ACK/reopen, inverse requests, later new selected capture and ordinary suffix controls all pass unchanged. V2/removal and refusal in those App tests are synthetic transport scenarios.
- Source review: the repair reconstructs only ordinary move/label preview writes from original captures and applies them to accepted state. It does not rewrite persisted original commands, guards, bases or pins, introduce a browser validator, or fabricate selected/inverse after-state before ACK. Unsent pending work now exposes the existing cancellation affordance. The remaining last-op recovery classification is the blocker above.

## Exact commands and results

CWD: `/home/user/work/wt/app-m2-selected-server-fix-independent-review`.

Private configs mirror the repository configuration with absolute imports, runner-compatible dirname, private cacheDir, cache disabled and one worker. A private extraction of this worktree's existing Composition 0.0.12 tarball supplies the package alias; shared dependencies were only read. To recreate the removed private extraction:

```bash
python /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-selected-server-fix-independent-review/notes/prepare-test-env.py
```

```bash
node node_modules/vitest/vitest.mjs run --config /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-selected-server-fix-independent-review/notes/vitest.config.mjs --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/commands/commitSession.selectedParams.test.ts src/tools/video-editor/commands/commitSession.test.ts src/tools/video-editor/commands/commitOutbox.test.ts src/tools/video-editor/commands/semanticGestures.test.ts src/tools/video-editor/commands/trackLabelGesture.test.ts src/tools/video-editor/hooks/useTimelineCommandSession.test.tsx src/tools/video-editor/hooks/useTimelineCommandSession.projection.test.tsx src/integrations/runtime/retainedParamInputs.test.ts
```

Exit 0: **8 files / 237 PASS**, 23.96s; `notes/targeted.log`.

```bash
node node_modules/vitest/vitest.mjs run --config /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-selected-server-fix-independent-review/notes/vitest.counterexamples.config.mjs --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism
```

Exit 0: **1 file / 4 original counterexamples PASS**, 3.01s; `notes/counterexamples.log`. Byte equality and source identity recorded in `notes/source-check.txt`.

```bash
node node_modules/vitest/vitest.mjs run --config /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-selected-server-fix-independent-review/notes/vitest.probes.config.mjs --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism
```

Exit 1: **2 ordinary failures / 1 positive control PASS**, 3.32s; `notes/probes.log`. Both failures are the remaining recovery defect. No skips, expected failures, altered repository tests or weakened expectations.

```bash
git diff --check b9c03ef5 HEAD
git status --short
git rev-parse HEAD
git rev-parse tl/app-m2-selected-server-lifecycle-fix
```

All exit 0; whitespace clean; status empty; both SHAs equal the reviewed SHA above.

## Scope and handoff

Read PLAN.md, the previous authority review, correction report and relevant source/tests. No decision deviation. No worker blocker: HOLD is the completed review verdict. No full/central suite, build, browser, project tsc, install, localhost/socket, native-provider rerun, git mutation or shared dependency/cache write. Private package extraction/cache and debug temp log removed; reproduction configs, scripts and final logs retained only under this worker's notes. No KEEP marker.

**D01 remains OPEN.** Actual matching-pair/property ingress, retained V1 validation after V2/removal and real Runtime process restart, durable lost-ACK exact retry, native inverse/reload and zero-legacy browser journey remain unqualified by this work. Synthetic provider transports and fake IndexedDB are not Runtime custody, process-restart durability or browser proof. After the bounded recovery follow-up and independent re-review, the orchestrator should run that separate qualification.
