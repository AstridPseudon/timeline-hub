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
and current settings authority were preserved. No pin, adoption, schema, DTO,
dependency, or public activation change was made.

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
full suite, pin/adoption, or schema run was performed. The actual production
create/init/retry/restart/undo journey remains unverified here.

After the harness commits this candidate, use the dedicated bootstrap-only
central suite, not the generic Gate5 wrapper which may select an ordinary
journey:

```sh
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test ap2-m2-bootstrap-only-current-home-port ap2-m2-bootstrap-observed-request-match-fix) && /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"
```

That suite must retain its unique `bootstrap actual consumer` selector and
run once against the committed current-HOME candidate.
