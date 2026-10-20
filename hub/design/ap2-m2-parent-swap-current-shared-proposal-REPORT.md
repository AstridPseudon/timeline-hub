# AP2-M2 current parent swap proposal

## Result

Ported the reviewed row-local native `clip.swap-media` helper onto current App
root. The existing preparation-only parent swap carrier remains unchanged.
The helper emits private014's parent-owned command, preserves raw parent clip
ownership/timing/transitions/opaque fields, freezes the authored old selection
and replacement selection before verification, requires both exact verified
media inputs, preserves registry opaque fields, and records guarded inverse and
replay claims. Public013 remains inert; no UI activation, legacy retirement,
provider/dataProvider mutation, DTO, schema, endpoint, source-generation, pin,
or dependency change was made.

Added:

- `src/tools/video-editor/commands/parentClipSwapCapture.ts`
- `src/tools/video-editor/commands/parentClipSwapCapture.test.ts`
- `src/tools/video-editor/commands/fixtures/parent_clip_swap_parity.py`
- reviewed swap/selection/record changes in `parentClipAddCapture.ts`

The separate current-HOME shared session/Provider adapter proposal is:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/ap2-m2-parent-swap-current-shared-proposal.patch`

It is a real `git apply`-checkable patch and is not applied in this branch. It
adds only the swap port, legacy-clean fence, and Timeline state/Provider
mounting. It does not activate a producer or edit App-owned shared files here.

## Verification

All commands ran from `/home/user/work/wt/ap2-m2-parent-swap-current-shared-proposal`.

```text
node --import 'data:text/javascript,globalThis.__dirname=process.cwd()+"/config/testing"' node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/commands/parentClipSwapCapture.test.ts src/tools/video-editor/commands/parentClipAddCapture.test.ts
PASS: 2 files, 14 tests

PARENT_SWAP_PARITY_OUTPUT=<temporary file> node ... parentClipSwapCapture.test.ts
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=<private014 Agent worker source> /home/user/work/venv-app2-native/bin/python src/tools/video-editor/commands/fixtures/parent_clip_swap_parity.py <temporary file>
PASS: 4 exact App/native commands, records and authored bundles; exact inverse, deterministic replay, unrelated-peer replay, and stale/wrong-selection/occupied-alias/short-source refusal

npm run typecheck:strict-islands -- --pretty false
PASS

node node_modules/eslint/bin/eslint.js --no-cache src/tools/video-editor/commands/parentClipAddCapture.ts src/tools/video-editor/commands/parentClipSwapCapture.ts src/tools/video-editor/commands/parentClipSwapCapture.test.ts
PASS

git diff --check
PASS

git apply --check --whitespace=error /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/ap2-m2-parent-swap-current-shared-proposal.patch
PASS: static applicability against current HOME
```

Not run: request-test, full suites, browser/e2e, localhost/live sockets,
Runtime Door/provider qualification, or live App lost-ack/restart acceptance.
