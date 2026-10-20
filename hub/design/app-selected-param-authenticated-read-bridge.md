# Selected PARAM authenticated read bridge

Implemented on App base `64d7e19b3c0e9db217381c955b8e50944879d49f`, branch `tl/app-m2-selected-param-authenticated-read-bridge`. Read PLAN and `design/app-selected-param013-production-binding-source.md`. This completes only the authorized authenticated read bridge; **production browser activation remains gated**.

The existing DataProvider has an optional readonly `paramReadClient` containing only the two generated verified-read signatures. RuntimeDataProvider forwards them through its own existing AstridRuntimeClient and refuses another project before traffic. The facade copies the supplied exact pin before awaiting, uses its existing authenticated session and WorkspaceClient, and rejects changed base/client/session or observed actor/realm/instance before returning an input. useTimelineSave passes that capability into the existing command session; that session's existing disposal/capture guards refuse late inputs after provider/project replacement or unmount. No new client, cache, endpoint, DTO, hash, semantic validator, latest fallback, or pin inference was introduced.

Changes: **6 source/test paths, +302/-1 (net +301)**; product **4 paths / +45**. Existing test assertions and helper bodies remain intact. The source audit proves **5833 other tracked files byte-identical** to the assigned base, including generated normal0.2.13, root/public Composition12 pins, MAIN parity harness, approved PARAM helper bodies and preview/render. New test file: `src/tools/video-editor/hooks/useTimelineSave.selectedParams.test.tsx`.

The actual provider → useTimelineSave → existing command session → generated authenticated read tests supply an explicit test-owned V1 pin. They prove one negotiated session, the existing bearer credential and provider project scope, exact document/object query pins, pending accepted4 until ACK8, opaque/clear preservation, and no latest document traffic. Literal16 reaches the synthetic server unchanged; its maximum10 refusal keeps accepted4 displayed and the original literal16/clear/pin/verified inputs in the durable outbox. Unavailable document/object reads and late disposal/client/project changes produce zero commits. Direct facade tests cover pin mutation before session negotiation, observed realm/actor/instance changes, reconnect during an object read, and authentication refusal without fallback.

These are synthetic HTTP/read specimens, **not native Runtime semantic-validator or browser qualification**. The tests do not manufacture a selected target's original authority from the dependency manifest.

Validation (Node22.22.0, Vitest4.1.5, read-only Composition0.0.12 dependency view, private TMPDIR/cacheDir, runner loader, cache disabled, one worker, no file parallelism):

- **14 files / 315 tests PASS**, exit0, 34.93s (`notes/targeted.log`). Product code is identical to this run.
- Final bridge rerun after test-only typing/handshake guard cleanup: **1 file / 8 tests PASS**, exit0, 5.16s (`notes/bridge-corrected.log`). An intermediate run failed8 because the test transport inspected command fields on the handshake body; corrected with optional access to `commands`. Original behavior expectations were retained. Initial bridge run also passed8 (`notes/bridge.log`).
- Scoped ESLint on all6 changed paths: exit0 (`notes/lint-final.log`); corrected bridge file rerun exit0 (`notes/lint-corrected.log`).
- `git diff --check`: exit0. Source audit exit0 (`notes/source-audit.json`). Read-only dependency/cache audit matched before/after the315 and subsequent8-test runs: all77 Composition file hashes, peer package metadata and observed shared cache trees (`notes/deps-before-neighbors.json`, `notes/deps-after.json`).

Exact commands (CWD `/home/user/work/wt/app-m2-selected-param-authenticated-read-bridge`; `$N` below expands to the worker notes path):

```bash
N=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-selected-param-authenticated-read-bridge/notes
python3 -B "$N/prepare-test-env.py"
env TMPDIR="$N/tmp" node --require "$N/vitest-runner.cjs" node_modules/vitest/vitest.mjs run --config "$N/vitest.config.ts" --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/hooks/useTimelineSave.selectedParams.test.tsx src/integrations/runtime/client.test.ts src/integrations/runtime/clientSharedSession.test.ts src/integrations/runtime/client.runtimeOrigin.test.ts src/integrations/runtime/dataProvider.test.ts src/integrations/runtime/dataProvider.parity.test.ts src/tools/video-editor/data/DataProvider.test.ts src/tools/video-editor/hooks/useTimelineSave.test.tsx src/tools/video-editor/hooks/useTimelineSave.recovery.test.tsx src/tools/video-editor/hooks/useTimelineSave.recovery.persistence.test.tsx src/tools/video-editor/hooks/useTimelineCommandSession.test.tsx src/tools/video-editor/hooks/useTimelineCommandSession.projection.test.tsx src/integrations/runtime/retainedParamInputs.test.ts src/tools/video-editor/commands/commitSession.selectedParams.test.ts
env TMPDIR="$N/tmp" node --require "$N/vitest-runner.cjs" node_modules/vitest/vitest.mjs run --config "$N/vitest.config.ts" --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/hooks/useTimelineSave.selectedParams.test.tsx
node node_modules/eslint/bin/eslint.js src/integrations/runtime/client.ts src/integrations/runtime/dataProvider.ts src/tools/video-editor/data/DataProvider.ts src/tools/video-editor/hooks/useTimelineSave.ts src/integrations/runtime/client.test.ts src/tools/video-editor/hooks/useTimelineSave.selectedParams.test.tsx
node node_modules/eslint/bin/eslint.js src/tools/video-editor/hooks/useTimelineSave.selectedParams.test.tsx
python3 -B "$N/audit-source.py"
python3 -B /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-selected-param013-production-binding-source/notes/audit-deps.py > "$N/deps-after.json"
cmp "$N/deps-before-neighbors.json" "$N/deps-after.json"
git diff --check
```

Decisions: used the smallest optional existing-provider capability and the existing command-session lifetime guard. No original-pin accessor or PropertiesPanel binding was invented. Cross-project reads fail before I/O; exact input reads remain uncached. No settled design decision was changed.

**Not run:** full suites, build, tsc, browser, localhost/live sockets, install, native server schema validation, end-to-end Props ingress or production activation. No git commit/merge/rebase/checkout/push/ref operations. No tests weakened, skipped or removed.

No blocker for this bounded bridge. Next: review/land it; finish the separate original-target-pin authority audit and UI binding, then qualify native maximum10 accept8/refuse16, retained V1 after V2/removal/restart, and production browser activation. The remaining original-pin authority and native/browser gates are not closed by this work.

Shared dependencies/runtimes/venvs were never written. Only the worker-local node_modules symlink was temporarily redirected to `/tmp/app-coherent-deps12/node_modules`, then restored to `/home/user/work/app/node_modules`. Private notes cache/tmp/dependency links were removed; the preparation script recreates them. No build output or temporary files remain in the worktree. Wrote report, commit-msg, DONE and KEEP.
