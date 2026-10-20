# AP2-M2 bootstrap fresh-capture parity report

## Result

Prepared a new applicable current-root packet from App integration head
`ea38656fe62950440b36cafee780698cff2c3f9c`.

The production initializer stays on the existing `AstridRuntimeClient` /
`RuntimeDataProvider` path. The strict native transport test and all existing
identity, refusal, and retry assertions are retained. The durable outbox keeps
the exact create/init request bytes and idempotency key for recovery; no
recapture or request upgrade was added.

The fresh `captureBootstrap` path performs the exact raw pristine check without
recording a whole-parent read. Its recorded `timeline.init` reads are exactly
the four authored absence paths used by Agent 4296:
`config.output`, `name`, `slug`, and `registry.assets`.

## Artifacts

- `handoff-ap2-m2-bootstrap-fresh-capture-parity-currentroot.patch`
  SHA256 `511ec8c038fdf5f5c6291e535ab64ae2a92ffe640bcb07d7e0f4486ed4c1f2d1`
- `ap2-m2-bootstrap-fresh-capture-parity-currentroot-packet.json`
- `ap2-m2-bootstrap-fresh-capture-parity-sequence.md`

The packet uses Agent source
`4296a7091d30543d3839fe703c0f0626f9882ebe`; command and record hashes are
listed in the sequence document.

## Evidence

```text
NODE_OPTIONS='--require=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-bootstrap-transport-assertion-repair/notes/vitest-runner.cjs' node node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism src/integrations/runtime/bootstrapInitialization.test.ts src/tools/video-editor/commands/bootstrapCapture.test.ts src/tools/video-editor/commands/commitOutbox.test.ts src/integrations/runtime/createDefaultTimeline.test.ts src/integrations/runtime/client.test.ts src/integrations/runtime/clientSharedSession.test.ts
6 files, 158 tests passed

AGENT=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-bootstrap-fixed-pair-gate/sources/agent-4296; PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$AGENT:$PWD" /home/user/work/venv-app2-native/bin/python -m pytest -q -p no:cacheprovider src/tools/video-editor/commands/fixtures/bootstrap_parity.py
12 passed; one pre-existing PytestUnknownMarkWarning for an integration mark

node node_modules/eslint/bin/eslint.js src/integrations/runtime/bootstrapInitialization.ts src/integrations/runtime/bootstrapInitialization.test.ts src/integrations/runtime/client.ts src/integrations/runtime/createDefaultTimeline.ts src/integrations/runtime/createDefaultTimeline.test.ts src/tools/video-editor/commands/bootstrapCapture.ts src/tools/video-editor/commands/bootstrapCapture.test.ts src/tools/video-editor/commands/commitOutbox.ts src/tools/video-editor/commands/commitOutbox.test.ts --max-warnings 0
passed

node node_modules/typescript/bin/tsc -p tsconfig.strict-islands.json --noEmit
passed

git diff --check
passed

private clean-root: git apply --check handoff-ap2-m2-bootstrap-fresh-capture-parity-currentroot.patch
passed
```

The broader `tsconfig.app.json` no-emit check was also run and fails on
pre-existing unrelated Composition export mismatches and existing command/
environment type errors; it reported no diagnostic in the changed bootstrap
source beyond the existing `client.ts` `import.meta.env` environment typing.

## Limits

No full suite, browser, localhost/live socket, Runtime Door, actual App
activation, or native pair qualification was run. Those remain the separate
qualification boundary.
