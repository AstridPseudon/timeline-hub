# Selected PARAM recovery follow-up

Completed on App base `1c7345b702ee84cc627ed0bc03c82ae77364a50b`, branch `tl/app-m2-selected-server-recovery-followup`, worktree `/home/user/work/wt/app-m2-selected-server-recovery-followup`. No blocker or disagreement with PLAN.md. D01 and native paired qualification remain OPEN.

## Change and decisions

Only `src/tools/video-editor/commands/commitSession.ts` and its existing `commitSession.selectedParams.test.ts` changed.

Recovery now compares the accepted closure's selected pack parameter states with the original display closure. An ordinary last ACK no longer hides earlier selected/inverse effects: both reported sequences recover seed 8 and seed 4 respectively. The comparison reads literal accepted data, including absent/present distinctions; it does not evaluate schemas, infer selected after-state, or authorize an edit. It covers parent and occurrence-owned clips and both existing element-reference spellings.

The accepted closure is eligible only when the retained first intent explicitly names that accepted intent as its predecessor. This also prevents an older local selected/inverse acceptance from replacing a newer original display closure, including the accepted bundle used for later cancellation. Ordinary-only recovery retains the original display control. Existing ordinary preview reconstruction supplies the working bundle in original suffix order; its writes still come from each immutable original capture.

No new persistence field, API, wire field, validator, writer, queue/store, browser export, UI activation, schema/pin refresh, optimistic selected execution, or guard refresh. Selected pending payloads remain `after: null`; retained original basis, literal bytes, exact inputs/pin, payload, request/key and false accepted-basis flag remain unchanged. The native provider remains the sole schema authority. Native semantics did not change, so no native-provider rerun was requested or claimed.

Both exact external repro bodies were appended permanently to the existing selected session suite. The original test file remains a byte-exact prefix. Two additional ancestor controls preserve a newer original closure after an older selected or inverse acceptance. All original four lifecycle controls and cancellation/new-capture behavior remain passing without weakened expectations, skips, or expected failures.

## Exact validation

CWD for all commands: `/home/user/work/wt/app-m2-selected-server-recovery-followup`.

Private runner configs mirror the existing repo config, use `--configLoader=runner`, private cacheDir, disabled caches, one worker and no file parallelism. Composition 0.0.12 came from a private extraction of this worktree's existing tarball. Shared node_modules and all shared dependency/cache paths were read-only. Observed Vitest version: 4.1.5. Recreate the removed private extraction before reproducing:

```bash
python /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-selected-server-recovery-followup/notes/prepare-test-env.py
```

Before the product fix, with the two repros promoted:

```bash
node node_modules/vitest/vitest.mjs run --config /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-selected-server-recovery-followup/notes/vitest.config.mjs --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/commands/commitSession.selectedParams.test.ts
```

Exit 1: **2 failed / 15 passed**, 4.58s (`notes/red.log`). Exactly the review's failures: recovered selected seed 4 instead of 8; recovered inverse seed 8 instead of 4.

Intermediate session check after the correction, before adding the two ancestor controls:

```bash
node node_modules/vitest/vitest.mjs run --config /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-selected-server-recovery-followup/notes/vitest.config.mjs --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/commands/commitSession.selectedParams.test.ts src/tools/video-editor/commands/commitSession.test.ts
```

Exit 0: **2 files / 86 PASS**, 9.90s (`notes/session.log`).

Final focused inherited eight-file cohort, with the two repros and two ancestor controls:

```bash
node node_modules/vitest/vitest.mjs run --config /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-selected-server-recovery-followup/notes/vitest.config.mjs --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/commands/commitSession.selectedParams.test.ts src/tools/video-editor/commands/commitSession.test.ts src/tools/video-editor/commands/commitOutbox.test.ts src/tools/video-editor/commands/semanticGestures.test.ts src/tools/video-editor/commands/trackLabelGesture.test.ts src/tools/video-editor/hooks/useTimelineCommandSession.test.tsx src/tools/video-editor/hooks/useTimelineCommandSession.projection.test.tsx src/integrations/runtime/retainedParamInputs.test.ts
```

Exit 0: **8 files / 241 PASS** = original 237 + two repros + two ancestor controls, 25.79s (`notes/targeted-final.log`).

Unchanged external original-four controls and exact external repro file, copied byte-for-byte from the independent review:

```bash
node node_modules/vitest/vitest.mjs run --config /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-selected-server-recovery-followup/notes/vitest.counterexamples.config.mjs --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism
node node_modules/vitest/vitest.mjs run --config /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-selected-server-recovery-followup/notes/vitest.probes.config.mjs --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism
```

Both exit 0: **4 original controls PASS**, 3.84s (`notes/counterexamples.log`); **2 repros + 1 cancellation/new-capture positive control PASS**, 3.31s (`notes/probes.log`). The positive control retains the original false basis/inputs through inverse ACK and reopen, cancels successive tails, then accepts fresh selected and ordinary work at their actual accepted heads with original guards.

```bash
node node_modules/eslint/bin/eslint.js src/tools/video-editor/commands/commitSession.ts src/tools/video-editor/commands/commitSession.selectedParams.test.ts --max-warnings 0
git diff --check
```

Both exit 0: lint has zero warnings (`notes/lint.log`); whitespace clean. `notes/source-check.txt` records original test-prefix and exact external-file equality checks.

## Scope, conflicts and next steps

No full suite, broad fullcohort, build, project tsc, install, browser, localhost/live socket, native process-restart/custody proof, shared dependency/cache write, upstream merge, integration-worktree edit, git commit/merge/rebase/checkout, push or ref deletion. No queued test or KEEP marker. Private extraction/cache removed; reproduction scripts/configs and logs retained under this worker only. Worktree contains only the two intended source/test changes.

Upstream refresh is deliberately separate. Read-only comparison used local `origin/main` `44f0b9ca9` and `tl/integration` `18becfbede00038830b97e63345445eeef54fa42`; no commits in `HEAD..origin/main` touched these two files. Integration still lacks the inherited selected/session work, so that parent stack must accompany this follow-up. Future conflict-sensitive areas are `commitSession.ts`'s `claim()` recovery basis selection and ordinary preview/inverse/cancel state reconstruction, plus the appended selected-session regression block. Preserve original captures and accepted predecessor protection when refreshing; no actual merge was attempted and merge cleanliness is not claimed.

Next: independent re-review of this bounded correction, then the orchestrator's separate matching-pair/native qualification. Actual public property ingress, retained V1 validation after V2/removal and real Runtime restart, durable lost-ACK exact retry, native inverse/reload and zero-legacy browser journey remain unverified here. These synthetic normal-port transports and fake IndexedDB tests demonstrate App recovery behavior, not accepted-server data loss or Runtime/browser custody.
