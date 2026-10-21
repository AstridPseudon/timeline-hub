# private392 dormant visual seam member proof

## Result

PASS. Added one focused behavior case to the existing private392 App Door
driver. The case uses the approved Agent 1303/e010 and Runtime f8da pair,
artifact52df/raw392 contract, and the existing custody guards. It builds the
dormant visual seam project-data patch, captures the exact existing
project-data.write command, sends it through the real RuntimeDataProvider Door,
reloads the raw seam values, and performs guarded native undo.

The existing 29-assertion private392 journey remains unchanged in the driver.
The runner selects only the new seam case so the prior retry, restart,
credential, cohort, rebase, stale-refusal, opaque-value, and zero-legacy-post
coverage from gate 6846 is carried forward without repeating that broad run.

## Source changes

- Carried the already-approved private392 driver, runner, integration config,
  and generated f8da contract counterpart onto this base because the requested
  base did not contain those existing reviewed files.
- Added the focused case to
  [runtimePrivate392Consumer.test.ts](/home/user/work/wt/ap2-m2-seam-private392-real-member-proof-0100/tests/integration/runtimePrivate392Consumer.test.ts).
- Updated the runner's source digest to the modified driver and selected the
  new case by name.
- No live UI, browser, activation, public pin, new authority, DTO, or
  useTimelineState/useTimelineOps change was made.

The case verifies that a stored opaque report and unknown sibling survive,
newly derived report data is excluded, the authored leaf is lowered as one
exact replace command, baseline key order is retained through save/reload,
an absent sibling remains absent, and guarded native undo restores the exact
raw seam object.

## Tests and checks

Local:

- `vitest run --config config/testing/vitest.config.ts --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/commands/visualSeamProjectDataMember.test.ts src/tools/video-editor/commands/projectDataMember.test.ts` — PASS, 2 files, 13 tests.
- ESLint on the touched App/integration/config TypeScript files — PASS.
- `sh -n scripts/testing/private392-http-runner.sh` — PASS.
- `node scripts/vendor-lock.mjs check runtime.lock.json --producer /home/user/work/wt/rt-pin-f8da4b6d` — PASS.
- `node_modules/.bin/tsc --noEmit --pretty false` — PASS.
- `git diff --check` — PASS.
- Vitest list with `--testNamePattern='accepts the dormant visual seam member'` — exactly one selected case.

Central named run:

- Suite: `ap2-m2-private392-approved-native-env-app-http-integration`
- Result: PASS, one test passed and the unchanged broad case was unselected.
- Result directory:
  `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/ap2-m2-seam-private392-real-member-proof-0100-ap2-m2-private392-approved-native-env-app-http-integration-1021010301-15399`
- The central run used the existing real capture/session/provider Door lane;
  no local browser, local socket, or full suite was run.

Two earlier central attempts reached the live case but failed on test-only
expectations (container guard shape and pre-persistence object order), then
passed after those assertions were corrected. A third corrected attempt
initially exposed the existing head-shape adapter requirement; the final run
constructed the provider's verified head shape and passed.

## Blockers and next steps

No blocker remains for this scoped dormant compatibility proof. The case does
not activate the seam in live UI or retire any writer. The orchestrator should
review and merge the worker commit through the normal integration queue.

