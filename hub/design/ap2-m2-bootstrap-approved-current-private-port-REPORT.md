# AP2-M2 bootstrap approved current private port

## Result

Forwarded the approved current-root bootstrap packet onto this App worktree as a private 014 candidate. The implementation is the reviewed source packet, not a fresh design:

- Replaced bootstrap-local `publishEmptyTimeline` use in `createDefaultTimeline.ts` with the existing durable create/init owner path and current `RuntimeDataProvider` basis loader.
- Added the narrow `AstridRuntimeClient.createTimeline` wrapper for the already-generated Runtime create operation.
- Extended the existing outbox owner with exact create reservation, project-scoped recovery, original create retention, and original initialization request/result retention.
- Added the fresh four-absence native capture (`config.output`, `name`, `slug`, `registry.assets`) and the approved bootstrap fixture/parity tests.
- Preserved exact normal `/v1` transport headers, handshake, full request bodies, idempotency keys, retry identity, H0 guards, history/immutable-closure verification, and legacy bootstrap-route rejection.
- Preserved the existing alias, canonical-ID precedence, reassignment/CAS, headed opaque-document, headless repair, additional timeline, and lost-response positive coverage. No test was deleted, skipped, weakened, or converted to refusal.

## Public floor vs missing App port

The single public floor remains current public013: no init pin, activation, or release, and no fallback/unknown-operation behavior. This branch is only a private 014 candidate; it does not change public pins, dependencies, generated contracts, DTOs, endpoints, or release decisions.

The missing App port at that floor was the real current-root consumer: create the timeline through the normal Runtime operation, retain the exact create/init flights in the existing outbox, perform native capture at verified H0, commit through `/v1`, and recover without recapture. This candidate supplies that App-side port. Matched Agent/Runtime qualification, central actual transport/browser evidence, owner activation, and the later ledger/deletion gate remain outside this task.

## Evidence

All commands were run from `/home/user/work/wt/ap2-m2-bootstrap-approved-current-private-port`:

Source packet fingerprints: fresh current-root parity patch `511ec8c038fdf5f5c6291e535ab64ae2a92ffe640bcb07d7e0f4486ed4c1f2d1`; strict transport repair source `f5ae641574b45b7e9733b2ef6ffd5955a27888c0b1c1d3467b4e0121cc8e0fd6`.

```text
git apply --check /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-ap2-m2-bootstrap-fresh-capture-parity-currentroot.patch
PASS

NODE_OPTIONS='--require=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-bootstrap-transport-assertion-repair/notes/vitest-runner.cjs' node node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism src/integrations/runtime/bootstrapInitialization.test.ts src/tools/video-editor/commands/bootstrapCapture.test.ts src/tools/video-editor/commands/commitOutbox.test.ts src/integrations/runtime/createDefaultTimeline.test.ts src/integrations/runtime/client.test.ts src/integrations/runtime/clientSharedSession.test.ts
PASS — 6 files, 158 tests

NODE_OPTIONS='--require=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-bootstrap-transport-assertion-repair/notes/vitest-runner.cjs' node node_modules/eslint/bin/eslint.js src/integrations/runtime/bootstrapInitialization.ts src/integrations/runtime/bootstrapInitialization.test.ts src/integrations/runtime/client.ts src/integrations/runtime/createDefaultTimeline.ts src/integrations/runtime/createDefaultTimeline.test.ts src/tools/video-editor/commands/bootstrapCapture.ts src/tools/video-editor/commands/bootstrapCapture.test.ts src/tools/video-editor/commands/commitOutbox.ts src/tools/video-editor/commands/commitOutbox.test.ts --max-warnings 0
PASS

node node_modules/typescript/bin/tsc -p tsconfig.strict-islands.json --noEmit
PASS

AGENT=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-bootstrap-fixed-pair-gate/sources/agent-4296 PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$AGENT:$PWD" /home/user/work/venv-app2-native/bin/python -m pytest -q -p no:cacheprovider src/tools/video-editor/commands/fixtures/bootstrap_parity.py
PASS — 12 tests; one pre-existing PytestUnknownMarkWarning for `integration`

git diff --check
PASS
```

Not run: full suite, central suite, browser, localhost/live sockets, real Runtime Door admission, public pin/release, or dependency installation. No App-owned old ports/lifetimes were edited.

## Files

Production changes are limited to the current runtime client/create seam, bootstrap initializer/capture, and existing outbox. Tests and the small parity fixture are included in the same candidate. No build output or temporary files remain in the worktree.

## Next step

Have the orchestrator review this private candidate against the matched Agent 3c4-init-fixed / Runtime 202 private source packet and run the separately authorized central actual gate. Do not promote or delete/merge the old publisher until the same-cohort actual gate and owner activation are complete.

