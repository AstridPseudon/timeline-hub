# Manual native ADD submit final review — HOLD

Reviewed App `2d6f236f2b95f2f89ebbed7ba95a4f2d00032a83` against `ace8a84e075c5967605d0c27d61f19df5afef454`. Read PLAN.md, app-manual-native-add-independent-review.md and app-manual-native-add-submit-boundary-fix.md. No product or test edits; no settled decision changed.

**The bounded enqueue correction is supported: 407/407 pass together, and both original success probes fail on ace8. HOLD is solely on closing the previously reported popup failure: its cause remains unclassified.** No new product defect was demonstrated. This review does not label the prior failure a proven DOM/test-order issue or claim all historical evidence is clean.

## Enqueue boundary: verified

The complete candidate delta is three paths, +74/-4, net +70. Product is exactly two paths, +5/-2, **net +3**; test delta is +69/-2, net +67. The only existing-test helper adjustment exposes the fake IndexedDB factory. Original positive assertions remain intact; the two required-success probes are copied verbatim as ordinary `it` tests, with no fails/skip/refusal substitution.

- `runtimeRecoveryPlacement.ts:93–96` passes the required local `onEnqueued` callback; it no longer marks attempted handoff as submission. Its `finally` still clears only `pending`. No catch-reset exists.
- `commitSession.ts:295–311` converts the original document, checks cancellation/current binding and readiness, verifies the unchanged idle owner/head/document/bundle, and performs native capture **before** enqueue. Thus cancellation and atomic capture refusal leave the reservation reusable. The unchanged-choice regression checks the original reserved child ID; the corrected-window regression proceeds to one send.
- `enqueue` at `commitSession.ts:182–197` advances the local authored bundle, allocates the owner's local intent ID, pushes the capture into `pendingAppends`, and schedules persistence on a Promise chain. It returns synchronously. The callback executes immediately after that successful return, before `await chain`/`pump`; scheduled persistence cannot execute between these synchronous statements. There is no ACK-dependent latch, new coordinator, queue, storage contract or wire change.
- After transfer, unchanged and changed chooser requests remain refused. Append-storage failure leaves the exact capture in the existing owner's in-memory pending append, with no send/durable intent yet. Owner Retry persists and sends it. ACK-storage failure retains the durable pending request; Retry sends the identical body/key. Normal uncertainty, conflict, restart/outbox and suffix-preservation expectations remain unchanged. Append failure is **not crash-safe until storage recovers**; this patch does not pretend otherwise.

All 34 normal adapter tests and all 34 original private adapter controls pass within the combined run, including the two required successes, actual closed/busy owner, uncertainty, both new storage stages, no recapture, original identity and exact owner Retry.

## Prior closed-popup case: explicit classification and remaining uncertainty

The fix worker's preserved `controls.log` reported **41/42**, failing `private authority review controls > retains raw control-like identities as data and renders names as text` at authority-controls.test.tsx:138. After `fireEvent.click(combobox)`, the expected literal raw-name option was absent and the captured DOM had `aria-expanded="false"`, no listbox. Its subsequent isolated 8/8 does not explain that failure.

This review's single combined candidate run passes **407/407**, including that exact unchanged test and all 42 unchanged private controls. One controlled ace8 comparison of the original 42 gives **40 pass / 2 fail**: precisely the two pre-enqueue retry bugs. All eight authority controls, including the closed-popup case, also pass on ace8. Therefore the earlier popup symptom was **not reproduced on either tree**. This baseline demonstrates the correction's causal effect on the two retry probes; it does **not** demonstrate that the popup failure is a baseline harness defect.

The failed assertion concerns pre-submit popup interaction/rendering. That test calls `render(element())` with no placement callback, does not request placement, and does not call either changed product function. The chooser, ShotSelector, Popover, destination reads and test setup are byte-unchanged in the candidate diff. This localizes the symptom outside the modified enqueue boundary, but does not establish why the popup stayed closed.

Teardown inspection: `src/test/setup.ts:6–8` already calls RTL `cleanup()` after each test; the authority file restores its `scrollIntoView` shim in `afterAll`. The failed case is the first rendered UI case in that file (the preceding three only exercise provider reads). Chooser teardown clears its interval and aborts its request; ShotSelector cancels its focus animation frame. No concrete missing teardown or test-order mechanism was established. Calling this a proven harness flake would overstate the evidence. No arbitrary reruns, retries-until-green, timing delays or weakened expectations were used.

**Remaining review action:** a bounded diagnostic tracing popup open/close reasons, click readiness and cleanup on the original authority case, or an actual baseline reproduction of the closed-popup failure. Preserve the original expectation. The orchestrator can assess this residual UI-test uncertainty separately from the supported three-line enqueue fix; this report keeps HOLD rather than silently closing the specifically requested classification.

## Exact tests and results

Working directory: `/home/user/work/wt/app-m2-manual-native-add-submit-final-review`.

```sh
REVIEW=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-manual-native-add-submit-final-review
node /tmp/app-coherent-deps12/node_modules/vitest/vitest.mjs run \
  --config "$REVIEW/vitest.config.mts" --configLoader runner \
  --no-file-parallelism --maxWorkers=1 --no-cache \
  src/features/tasks/components/TasksPane/utils/runtimeRecoveryPlacement.test.ts \
  src/features/tasks/components/TasksPane/RuntimeRecoveryChooser.test.tsx \
  src/tools/video-editor/commands/occurrenceMediaCapture.test.ts \
  src/tools/video-editor/commands/occurrenceMediaPrimitives.test.ts \
  src/tools/video-editor/commands/occurrenceMediaOwnKeysCapture.test.ts \
  src/tools/video-editor/commands/commitSession.test.ts \
  src/tools/video-editor/commands/commitOutbox.test.ts \
  src/tools/video-editor/hooks/useTimelineCommandSession.test.tsx \
  "$REVIEW/adapter-controls.test.ts" "$REVIEW/authority-controls.test.tsx"
```

**10 files / 407 passed, exit 0, 28.92s.** This is one invocation combining the normal 365 tests and original 42 review controls. [Combined log](../workers/app-m2-manual-native-add-submit-final-review/combined.log).

Baseline was extracted using read-only `git archive ace8a84e0 src config vendor package.json runtime.lock.json` into `$REVIEW/baseline-ace8` (no checkout). Its own dependency symlink points read-only to private12. `vitest.baseline.config.mts` changes only source root/aliases/plugin/setup paths and private cacheDir to the baseline; it uses the same unchanged control files and dependency tree.

```sh
node /tmp/app-coherent-deps12/node_modules/vitest/vitest.mjs run \
  --config "$REVIEW/vitest.baseline.config.mts" --configLoader runner \
  --no-file-parallelism --maxWorkers=1 --no-cache \
  "$REVIEW/adapter-controls.test.ts" "$REVIEW/authority-controls.test.tsx"
```

**2 files / 40 passed, 2 failed, exit 1, 6.07s**; only the two original expected-success retry probes fail with the original already-submitted latch error. No tests were altered to hide them. [Baseline log](../workers/app-m2-manual-native-add-submit-final-review/baseline-controls.log).

```sh
git diff --numstat ace8a84e0 2d6f236f2
git diff --check ace8a84e0 2d6f236f2
git diff --check
git status --porcelain=v1
```

All exit 0; worktree clean. Python byte comparisons confirm the two controls exactly equal the original independent review files (SHA256 adapter `ebf55ee9570250ccebe0e2c8803dc58ba9a9265d07a518e6dd1206d015cc844a`, authority `b580cceb255559ff0ca382c51d6c9d7f366bd1f353bd7f4fbb1da841549c670a`) and the required-success block is verbatim in the normal suite. [Checks](../workers/app-m2-manual-native-add-submit-final-review/review-checks.log).

## Qualification limits and handoff

S2 `26ef2bbb31b4892fdd7c15ee5b20700bd40cb933` / candidate905 `905a4f0f1dcadf92a226b1da0baba50b8a37178d` native parity remains exactly the prior independent review's evidence. Recipes, primitives, fixtures, commands, ownership claims and transport contracts are unchanged in this fix; no native execution was rerun or new parity claimed.

Production host binding remains **OPEN**: TasksPane still supplies no placement callback, the owner hook retains its session privately, and the App's normal published client/pin adoption and authenticated same-client/session wiring remain pending. Mocked transports/fake IndexedDB and detached acceptance fixtures do not qualify real Runtime acceptance, raw reload, inverse/redo, restart/retry, mixed edits or zero-legacy traffic.

Runner/config/test imports all use `/tmp/app-coherent-deps12/node_modules`; only this assigned worktree's ignored dependency link and worker scratch links were configured. Private cacheDir plus runner loader/no-cache/maxWorkers=1 throughout. No shared dependencies, runtimes, venvs or cache contents changed. No full suite, build, tsc, browser, socket/localhost or install. No git mutation. Temporary baseline archive and private cache output removed after verification; logs/configs/unchanged controls retained in this worker's scratch. No build/temp files or product/test changes in the worktree.

The read-only review is complete, with no execution blocker. DONE indicates review completion, not source approval or production activation. No KEEP requested. Next step is the bounded popup diagnostic above, then the separately authorized host-binding/real-pair qualification.
