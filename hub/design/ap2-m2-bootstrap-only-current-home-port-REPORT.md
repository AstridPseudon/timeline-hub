# AP2-M2 bootstrap-only current-HOME port

## Result

Completed the code-only bounded port from donor range
`480db7febe624fe4658a75cbdb66ed5de84c2c61..35c5ed018c1983acb522a0e7333de18a271638ea`
onto current `hub/tl/integration`.

The worktree base was `e9d04f4bf0b9c06d184541655f20a4ca832d0370`, with
`hub/tl/integration` resolving to the same SHA. The donor base is an ancestor
of this current HOME. The patch was applied as the exact Git diff, without
copying old files or resetting unrelated paths.

The prior HOLD was handled as directed: current HOME settings authority and
ShotEditor/shotSet/e2e harness behavior remain intact. The HOLD was not caused
by a bootstrap-control test failure.

## Exact touch list

The donor range and this worktree have the same 16 touched paths:

- `src/integrations/runtime/bootstrapInitialization.test.ts`
- `src/integrations/runtime/bootstrapInitialization.ts`
- `src/integrations/runtime/client.ts`
- `src/integrations/runtime/createDefaultTimeline.test.ts`
- `src/integrations/runtime/createDefaultTimeline.ts`
- `src/integrations/runtime/dataProvider.ts`
- `src/tools/video-editor/commands/bootstrapCapture.test.ts`
- `src/tools/video-editor/commands/bootstrapCapture.ts`
- `src/tools/video-editor/commands/commitOutbox.test.ts`
- `src/tools/video-editor/commands/commitOutbox.ts`
- `src/tools/video-editor/commands/fixtures/bootstrap_parity.py`
- `src/tools/video-editor/commands/fixtures/recipe_m2_app_bootstrap.json`
- `tests/e2e/local/support/app.ts`
- `tests/e2e/local/support/timeline-scope.test.ts`
- `tests/e2e/local/support/timeline-scope.ts`
- `tests/e2e/local/three-products.spec.ts`

The exact sorted donor-path/current-path comparison passed. Therefore no
out-of-scope current files changed, including `src/tools/travel-between-images/components/ShotEditor/**`,
`src/tools/travel-between-images/pages/ShotEditorView.tsx`,
`src/tools/video-editor/commands/shotSetGesture.ts`,
`src/tools/video-editor/commands/shotSetSession.test.ts`,
`tests/e2e/local/shot-name-command.spec.ts`, and
`tests/e2e/local/support/harness.ts`. The retained7d/selected5a/trim behavior
and current settings authority were preserved. The final sentence above was
incorrect and is corrected here: `b69c85ea7` did make a live public call-path
change. It replaced the live `createDefaultTimeline` initializer's
`publishParentComposition` path with
`RuntimeDataProvider.initializeNativeBootstrapTimeline`, whose captured batch
starts with `timeline.init@1`. The checked-in public013 Runtime contract does
not accept that operation. HOME owns the call-path revert; this report does
not duplicate or modify it.

## Live-caller and contract correction

This is an activation-impacting source packet, not an inert helper port. The
following changed exports/surfaces have live product callers (the search
excluded tests, `tests/**`, `__tests__/**`, and vendor trees):

| Changed surface | Live product caller(s) | Effect in `b69c85ea7` |
| --- | --- | --- |
| `createCanonicalTimeline` | `src/tools/video-editor/pages/VideoEditorPage.tsx:551`; internally `createDefaultTimeline.ts:108` | Additional-timeline creation now runs native create/init/commit. |
| `ensureProjectHasTimeline` | `src/shared/hooks/projects/useProjectCRUD.ts:154`; `src/tools/video-editor/pages/VideoEditorPage.tsx:461`; internally `createDefaultTimeline.ts:108` | Project creation and first/headless-timeline repair now run native create/init/commit. |
| `RuntimeDataProvider.initializeNativeBootstrapTimeline` | `src/integrations/runtime/createDefaultTimeline.ts:64` | Routes the initializer through the configured Runtime client and native bootstrap owner. |
| `initializeBootstrapTimeline` | `src/integrations/runtime/dataProvider.ts:78,503` | Live durable create/init boundary, not test-only glue. |
| `reserveBootstrapInitialization` / `resumeBootstrapInitialization` | `src/integrations/runtime/bootstrapInitialization.ts:213,216-217` | Live recovery path; `reserveBootstrapInitialization` calls `outbox.reserveCreate` at `:34`. |
| `captureBootstrap` | `src/integrations/runtime/bootstrapInitialization.ts:170` | Live capture emits `timeline.init@1` followed by `track.create@1` records. |
| `AstridRuntimeClient.createTimeline` | `src/integrations/runtime/dataProvider.ts:508` | Live create request used before the native commit. |
| `createCommitOutbox` / `reserveCreate` surface | `src/tools/video-editor/commands/commitSession.ts:133`; `src/integrations/runtime/bootstrapInitialization.ts:209` | Shared live outbox; the initializer invokes it, so it is not inert. |

The required private bootstrap command cohort is:

```text
timeline.init@1 (select=parent; args=name, slug, output) + track.create@1...
```

The currently pinned public013 Runtime is exact, not a moving-main
assumption: App `runtime.lock.json` pins producer source
`2c4ac180c2220bdad966bc01e95ad230e99ce26a`, producer version
`sha256:6f000bc615a9cb24fb00cc69a97af75eae71006ebfe87e3caa272fcdbbb1af56`,
contract `0.2.13`, and schema digest
`sha256:8de823011a121359b9ad021e283b45afb6baeabc8a154a02bd086d1260a8b8f4`.
Its exact `contract/schemas/edit-command.json` contains `track.create` but no
`timeline.init`; its generated public types contain no `TimelineInitArgs`.
The public HTTP operations `createTimeline` and `commitTimeline` do not imply
that the command operation `timeline.init` is accepted.

The private202 overlay is a different cohort: Runtime
`202074110717146fc7f08af2306a8dd7f695b0b1` / producer
`a0dca16975dfe8f5e762703b99d9791a16cf7fd7`, contract `0.2.14`, schema digest
`sha256:ce3781c282564b650890456f6c257f3faabe2de3898a84363fecd47e48b30d59`.
Its exact edit-command schema adds `timeline.init@1` and `TimelineInitArgs`.
Any activation test using that overlay is private202 evidence only; it is
never public013 readiness evidence.

## Disposition

The source-only bootstrap packet may remain privately qualified against the
matched private202 Agent/Runtime pair, but public delivery is **HELD**. Do not
claim public activation, public writer retirement, or a public bootstrap gate
from this packet. Re-activation requires HOME's reverted public call path plus
one matched Main014 Agent/Runtime/App adoption and its real create/init/restart
proof. No pin, schema, product, call-path, or test change was made by this
correction.

## Verification

All commands ran from
`/home/user/work/wt/ap2-m2-bootstrap-only-current-home-port`.

- `./node_modules/.bin/vitest run --config config/testing/vitest.config.ts --no-cache src/integrations/runtime/bootstrapInitialization.test.ts src/integrations/runtime/createDefaultTimeline.test.ts src/tools/video-editor/commands/bootstrapCapture.test.ts src/tools/video-editor/commands/commitOutbox.test.ts` — **PASS**, 4 files, 128 tests.
- `node --import tsx --test tests/e2e/local/support/timeline-scope.test.ts` — **PASS**, 1 test.
- Focused ESLint over all 14 touched TypeScript files with `--report-unused-disable-directives --max-warnings 0` — **PASS**, exit 0.
- `npm run typecheck:strict-islands` — **PASS**, exit 0.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-bootstrap-fixed-pair-gate/sources/agent-4296:$PWD" /home/user/work/venv-app2-native/bin/python -m pytest -q -p no:cacheprovider src/tools/video-editor/commands/fixtures/bootstrap_parity.py` — **PASS**, 12 tests; one pre-existing `PytestUnknownMarkWarning` for `integration`.
- `./node_modules/.bin/playwright test --config playwright.three-products.config.ts tests/e2e/local/three-products.spec.ts --grep "M2 real gate 5 bootstrap actual consumer" --list` — **PASS**, exactly 1 test listed; no browser execution.
- `git diff --check` — **PASS**.
- Exact donor/current touch-list comparison including untracked files — **PASS**.

An initial Vitest attempt with `--configLoader=runner` stopped before test
collection because this repository config exposes `__dirname`, which is not
defined in runner mode. The successful rerun used the normal config loader
with `--no-cache`; no test was counted from the startup failure. An initial
parity-fixture attempt without the frozen Agent source also failed during
collection with a missing `astrid` import; the corrected read-only Agent
source path above passed. No shared install or venv was modified.

## Boundaries and next step

No `request-test`, local driver, browser execution, localhost/live socket,
full suite, pin/adoption, or product schema-generation run was performed. The
public013 mismatch is established by exact pinned source inspection above; the
actual public production create/init/retry/restart/undo journey remains
unverified here and is not claimed.

The original next-step instruction below is superseded by this correction.
Do not request a gate from this packet: HOME must first land its public call-
path revert, and a matched Main014 cohort must be adopted. Only then may the
orchestrator authorize a dedicated bootstrap-only central suite; the generic
Gate5 wrapper must not be used because it may select an ordinary journey:

```sh
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test ap2-m2-bootstrap-only-current-home-port ap2-m2-bootstrap-observed-request-match-fix) && /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"
```

That suite must retain its unique `bootstrap actual consumer` selector and
run once against the committed current-HOME candidate.
