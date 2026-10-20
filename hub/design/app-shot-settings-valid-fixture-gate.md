# ShotSettings valid-fixture gate — BLOCKED, keep merge hold

2026-10-20. Worktree `/home/user/work/wt/app-m2-shot-settings-valid-fixture-gate`, base `c07be0d4d`. PLAN read first. Final tested App source tree `916b6705914788292df0f6f46e026c0317ed0e11`. No source edits after the central request.

## Changes and decisions

- Only two test/support files changed: `seedThreeProducts(referenceAt = THREE_PRODUCTS_REFERENCE_AT)` keeps the original 15s default and uses the argument for the successor in both parent clips/config clips. Only the new ShotEditor test calls it with 3s. The original M1 restore test is byte-identical to base, including its default seed call. The incoming crossfade and all opaque/root assertions are retained. Both production files containing c07's raw reader/writer and settings-root-presence fixes are byte-identical to base.
- The new case waits for either publication or a captured callback error before asserting publication/error success, so a local admission failure becomes visible promptly.
- Local probing found the new case's later tracked control would break the seam again by moving only its predecessor to 5s. Retained that actual Agent move and added a second actual Agent move of its successor to 8s, preserving the transition and every existing refusal/draft assertion. Executed both moves through the real pinned Agent capture/execute/compiler offline and proved their resulting graph passes the unchanged production App guard. The central test did not reach those commands, so their HTTP acceptance is unverified.
- No production code, admission guard, original fixture default, opaque assertion, transition assertion, or expected HTTP refusal was weakened. No tests skipped/deleted/xfail-ed. The failing malformed-input expectation remains unchanged.

## Actual central result: all settings roots pass, overall gate fails

Requested exactly once, after the final source edits:

```sh
ORCH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch
$ORCH/bin/request-test app-m2-shot-settings-valid-fixture-gate restore-opaque-m1-compat-integration
$ORCH/bin/wait-test app-m2-shot-settings-valid-fixture-gate-restore-opaque-m1-compat-integration-1020082604-16296 1
```

**FAIL, exit 1, 1 passed / 1 failed; 23s service time, 19.42s Vitest.** The unchanged original M1 restore test passed. The new test completed all five root iterations (`absent`, `null`, `scalar`, `array`, `object`) before failing at `runtimeRestore.test.ts:266`: malformed-input control expected HTTP 400, received HTTP 200. The unchanged-head assertion after that control and the subsequent tracked settings/name HTTP-refusal/draft checks were not reached.

The completed iterations are actual production callback -> App adapter/encoder -> normal Runtime-door HTTP publications -> normal raw immutable HTTP parent/shot/internal reads. They verify neutral-save no-publication, accepted name edits, accepted prompt edits for object/absent/null roots, scalar/array prompt refusal with no publication, exact full outgoing and raw immutable shot payloads, own prototype-named/nested opaque keys, explicit nulls/absent keys, unchanged internal payloads/parent config and opaque occurrence values, old immutable history, and fresh App raw reads after prompt saves. Null/scalar/array roots are qualified only for this real accepting codec and historical tuple. This is no longer App-reload-only evidence.

Executed centrally:

```sh
flock -w 600 /home/user/work/.app-m1-browser.lock env ASTRID_CHECKOUT=/home/user/work/wt/app-m1-full-agent-source ASTRID_PYTHON=/home/user/work/venv-agent/bin/python ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/app-m1-full-runtime-source ASTRID_RUNTIME_PYTHON=/home/user/work/venv-runtime/bin/python npx vitest run --config config/testing/vitest.runtime-restore.integration.config.ts --maxWorkers=1
```

Read-only historical leases were verified before and after: Agent `4a75f68f32049a69fd86135c645fa64c51175c14`, Runtime `4bb1d0f7efd2972d7b027fd9f458dbe8dabd0136`. This worktree's ignored node_modules symlink selects the physical standard `/tmp/app-m2-coherent-deps8/node_modules`; no shared dependency contents were changed. This is historical-compatible SAFETY evidence only, never current-tuple qualification. The service's generic external-head metadata is not the explicit source selection in the command above.

Result/log directory:
`ORCH/tests/app-m2-shot-settings-valid-fixture-gate-restore-opaque-m1-compat-integration-1020082604-16296/` (expand ORCH as above).

The earlier real-read-roundtrip failure remains recorded and its report is untouched: `app-m2-shot-settings-real-read-roundtrip-restore-opaque-m1-compat-integration-1020075825-497`, tree `aa09c8819f6e3d0c3fa0ac2372eeb445d94a521c`, original restore PASS/new callback FAIL before save. The new gate does not erase that failure.

## Precise new blocker and next step

The malformed-input control supplies a new shot revision with `metadata: []`, but reuses the current parent payload without changing its occurrence's `shot_revision_id`. Thus that malformed revision is not selected by any occurrence. Runtime 4bb's `service.py:3352` resolves shots from occurrence pins, and `service.py:3441-3444` runs `_validate_published_shot_payload` only on those resolved shots. The supplied extra malformed row is excluded from the published closure. HTTP 200 therefore is **not** evidence that a referenced malformed shot was stored or admitted; the negative fixture does not exercise its intended validator. This explains the observed status by source inspection, rather than inventing a backend validation regression.

Recommendation to the orchestrator: keep this candidate unmerged. Dispatch a narrow follow-up that binds the negative fixture's parent occurrence to its new malformed shot revision, preserves the expected 400 and unchanged-head assertions, then allows one fresh central gate to reach both that real negative control and the tracked 409/draft checks. Do not change Runtime admission or relax the test to expect 200. The positive raw read/save/readback gap now has actual HTTP evidence, but the requested complete gate remains red. Merge FIRST only after the actual complete gate passes. No rerun or source correction was made after using this task's single request allowance.

## Exact local validation

Run from the assigned worktree; all commands below exited 0:

```sh
./node_modules/.bin/vitest run --config config/testing/vitest.config.ts --maxWorkers=1 src/tools/travel-between-images/pages/ShotEditorView.test.tsx src/tools/video-editor/data/shotCompositionEditor.test.ts src/tools/video-editor/data/shotCompositionEditor.opaqueRemap.test.ts src/tools/travel-between-images/providers/VideoTravelSettingsProvider.test.tsx src/shared/state/createEntityStore.test.ts
# 5 files, 74 passed, 13.87s
./node_modules/.bin/vitest run --config config/testing/vitest.config.ts --maxWorkers=1 src/integrations/runtime/shotCompositionRuntime.test.ts src/integrations/runtime/opaqueRootWriters.test.tsx src/integrations/runtime/dataProvider.test.ts src/integrations/runtime/dataProvider.parity.test.ts src/integrations/runtime/timelineCommit.test.ts src/tools/video-editor/data/shotCompositionAdapter.test.ts src/tools/video-editor/data/shotCompositionProjection.test.ts src/tools/video-editor/data/visualSeamContract.test.ts
# 8 files, 222 passed, 18.75s
./node_modules/.bin/eslint tests/e2e/local/support/harness.ts tests/integration/runtimeRestore.test.ts
# exit 0, no output
./node_modules/.bin/vitest list --config config/testing/vitest.runtime-restore.integration.config.ts --maxWorkers=1
# exit 0, both real tests collected without sockets
git diff --check
# exit 0
```

Local production admission was GREEN **before** the central request. Reproduce the final executable probes using absolute notes paths:

```sh
NOTES=$ORCH/workers/app-m2-shot-settings-valid-fixture-gate/notes
node "$NOTES/admission-probe.mjs" --export
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/user/work/wt/app-m1-full-runtime-source /home/user/work/venv-runtime/bin/python "$NOTES/codec-probe.py"
node "$NOTES/admission-probe.mjs"
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/user/work/wt/app-m1-full-agent-source /home/user/work/venv-agent/bin/python "$NOTES/tracked-move-probe.py"
node "$NOTES/admission-probe.mjs" --tracked
```

All final probe commands exited 0. They execute the real seed method with its HTTP boundary intercepted solely to collect the payload without sockets; call the real Runtime `_complete_shot_payload`/`_validate_published_shot_payload`; and bundle the real private App converter, name helper, encoder, projection and admission guard in memory. Every root passes the 3s geometry; every root still produces the expected original 15s-gap refusal. The tracked probe uses real Agent capture/execute/compile and verifies final 5s/8s admission. These pure probes supplement, rather than replace, the actual HTTP result. An earlier diagnostic with only the predecessor moved to 5s exited 1 as expected; `admission-moved.log` retains the seam error without its generated data-URL stack.

Logs and executable probes are in the absolute NOTES directory above. No full suite, build, browser, tsc, install, git commit/merge/rebase/checkout/push, or other worktree mutation was performed. No build output/temp files remain in the assigned worktree. KEEP and commit-msg are supplied. BLOCKED is supplied instead of DONE because the full requested gate has not passed.
