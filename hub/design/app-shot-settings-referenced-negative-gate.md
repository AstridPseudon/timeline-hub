# Referenced malformed ShotSettings gate — BLOCKED before central execution

2026-10-20. Worker `app-m2-shot-settings-referenced-negative-gate`; base `b7153c590c88c2947fcbac2119912e7730d8720c`. PLAN and `design/app-shot-settings-valid-fixture-gate.md` read first. FIRST merge candidate remains on hold pending a complete green historical safety gate and independent review.

## Change

Only `tests/integration/runtimeRestore.test.ts` changed: 9 insertions / 2 deletions, within the new settings case's negative fixture. Read the current raw closure, allocate the malformed shot revision once, and repin the actual selected occurrence by occurrence_id to that revision. Spread the entire current parent and shot payloads, changing only that occurrence's shot revision pin and the shot's `metadata` to `[]`. Reuse the current immutable internal timeline revision; unrelated occurrences remain unchanged.

The original M1 case, seed helper/default 15s, new contiguous 3s fixture, all five positive-root assertions, expected 400 and unchanged-head assertions, actual Agent predecessor 5s/successor 8s moves, and tracked settings/name 409/draft/readback assertions are byte-identical to base. No production code, Runtime guard, skipped/disabled/weakened test, or positive behavior changes. No source edits after the central request.

## Local evidence: GREEN

Run from `/home/user/work/wt/app-m2-shot-settings-referenced-negative-gate`:

```sh
ASTRID_CHECKOUT=/home/user/work/wt/app-m1-full-agent-source ./node_modules/.bin/vitest run --config config/testing/vitest.config.ts --cache=false --maxWorkers=1 src/tools/travel-between-images/pages/ShotEditorView.test.tsx src/tools/video-editor/data/shotCompositionEditor.test.ts src/integrations/runtime/shotCompositionRuntime.test.ts src/tools/video-editor/data/visualSeamContract.test.ts
# exit 0; 4 files / 73 passed; 7.93s
./node_modules/.bin/eslint tests/integration/runtimeRestore.test.ts
# exit 0; no output
ASTRID_CHECKOUT=/home/user/work/wt/app-m1-full-agent-source ./node_modules/.bin/vitest list --config config/testing/vitest.runtime-restore.integration.config.ts --cache=false --maxWorkers=1
# exit 0; both real integration tests collected without sockets
git diff --check
# exit 0
```

Executable source/codec probes, with NOTES expanded to the absolute worker notes path below:

```sh
NOTES=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-shot-settings-referenced-negative-gate/notes
node "$NOTES/negative-probe.mjs"
# exit 0; edited source selects malformed revision, preserves parent/shot opaque fields and child identity,
# leaves unrelated occurrence unchanged, allocates shot revision once, mutates no input;
# all source outside negative block and entire harness unchanged
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/user/work/wt/app-m1-full-runtime-source /home/user/work/venv-runtime/bin/python "$NOTES/negative-codec-probe.py"
# exit 0; real historical Runtime codec accepts current full shot payload,
# then refuses selected malformed metadata: [] with "shot revision payload cannot be projected losslessly"
```

The JS probe executes the exact edited negative block with an intercepted HTTP boundary and a raw fixture derived from the prior worker's real seed/codec probe outputs. It includes opaque prototype-named keys and an unrelated occurrence. The Python probe selects the shot by the same occurrence key used by Runtime service.py:3352, then executes the actual `_complete_shot_payload` / `_validate_published_shot_payload`. These are local executable checks, not HTTP acceptance evidence. Initial probe setup hit sandbox `spawnSync git EPERM`; exporting the base through the shell instead resolved that setup issue before the passing probes and central request.

## Single central request: rejected, no tests executed

```sh
ORCH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch
$ORCH/bin/request-test app-m2-shot-settings-referenced-negative-gate restore-opaque-m1-compat-integration --files '--cache=false'
$ORCH/bin/wait-test app-m2-shot-settings-referenced-negative-gate-restore-opaque-m1-compat-integration-1020083144-13713 1
```

Request creation exited 0. The service and wait-test exited **1**, status **error**, with exact summary:

```text
bad file arg --cache=false (relative path/glob/node-id, no ..)
```

This was my request-format error: I attempted to disable Vitest cache writes to protect the shared dependency folder, but the service allows paths through `--files`, not CLI options. It rejected the request before snapshotting or executing the suite. There is no tested source-tree ID, no log.txt, and no HTTP result for this candidate. I did not resubmit or modify source because the brief allows one request and requires reporting a new problem without relaxing the gate.

Result directory:
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/app-m2-shot-settings-referenced-negative-gate-restore-opaque-m1-compat-integration-1020083144-13713/`

Consequently original restore + all five roots + invalid 400/no head change + tracked settings/name 409/draft kept + whole raw HTTP closure readback are **UNVERIFIED on this candidate**. The prior valid-fixture report's original restore and five-root passes remain historical evidence for its own tree only; its malformed setup failure is not erased.

## Explicit historical inputs and scope

The named suite explicitly selects read-only Agent `/home/user/work/wt/app-m1-full-agent-source` at `4a75f68f32049a69fd86135c645fa64c51175c14` and Runtime `/home/user/work/wt/app-m1-full-runtime-source` at `4bb1d0f7efd2972d7b027fd9f458dbe8dabd0136`. Both heads and clean status were checked before and after. This worker's own ignored node_modules symlink was repointed to `/tmp/app-m2-coherent-deps8/node_modules`, the physical standard deps8 with Composition package 0.0.8. Shared dependencies were read-only; no files or links inside shared node_modules/runtimes/venvs were created, replaced or deleted. Local Vitest runs used cache=false. Intended qualification is historical M1 compatibility safety only, never current-pair qualification.

No full suite, build, browser, tsc, install, git commit/merge/rebase/checkout/push, other worker mutation, or product-source change was performed. No build output/temp files remain in the worktree. Probes/logs live in this worker's notes folder. KEEP and commit-msg supplied; BLOCKED supplied instead of DONE.

## Decision and next step

The sole implementation choice was preserving the latest complete raw closure, including its actual child pin, instead of reconstructing a partial malformed shot from the initial seed. This isolates the intended metadata failure and preserves opaque data.

Orchestrator: keep merge hold. Authorize a corrected central request using a cache-safe runner command (cache disabling belongs in the suite command, not --files), then require the unchanged complete assertions to pass on the explicit historical pair/deps8 and obtain independent review before FIRST merges. The source is frozen and ready for that check; no actual integration failure or success can be inferred from the request rejection.
