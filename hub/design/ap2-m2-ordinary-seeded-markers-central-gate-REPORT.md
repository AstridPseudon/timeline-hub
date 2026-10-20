# App M2 ordinary seeded-markers central gate

Result: **FAIL (first result only; no rerun)**

## Source and fixture

- App target: `ap2-m2-ordinary-marker-state-fixture-fix` exactly; `HEAD` and
  target both `30ebb0ec15c571556b90ef3ecb3defcda9fa0e17`.
- App tree: `61c898d8b2310184b8c20ecdb5b721cd5dc8fbf5`.
- Owner ancestors verified: `7d42fcd3a` and `8c0e1f799`.
- The committed ordinary fixture has
  `config.app['haus.astrid.scene-phase-markers'].sceneMarkers` with
  `ordinary-marker-a` at `1` and `ordinary-marker-b` at `6`.
- The ordinary journey retains the exact ten-command assertion: two parent
  clips plus three occurrence-owned clips, each with move and hold commands.

## Checks

Passed:

- `./node_modules/.bin/vitest run --no-cache --config config/testing/vitest.config.ts src/test/threeProductsAuthoring.test.ts`
  — 1 file, 4 tests passed.
- `./node_modules/.bin/eslint tests/e2e/local/support/harness.ts src/test/threeProductsAuthoring.test.ts --ext ts --report-unused-disable-directives --max-warnings 0`
  — passed.
- Playwright collection for `M2 ordinary extension batch` — exactly 1 test.
- Driver shell/JS syntax checks and `git diff --check` — passed.
- Worktree remained clean.

The initial Vitest attempt used unsupported `--cacheDir` and was rejected by
the installed Vitest CLI before running tests; the corrected `--no-cache`
command above is the valid result. No shared dependency was changed.

## Central gate

Command submitted once through the central service:

```text
request-test ap2-m2-ordinary-seeded-markers-central-gate e2e-m2-ordinary-committed-driver-gate
```

Driver: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-ordinary-committed-driver-gate/run-central-m2-ordinary.sh "$PWD"`

Run: `ap2-m2-ordinary-seeded-markers-central-gate-e2e-m2-ordinary-committed-driver-gate-1020215400-17002`

The driver’s pre-build collection selected one ordinary test, and its exact
source/lock/graph/bin guards passed. The central log reports:

- Agent `8130a401bf44a518d5a40ae274d398b8c560be55`.
- Runtime `2c4ac180c2220bdad966bc01e95ad230e99ce26a`.
- Composition/graph and lock guards passed; source tuple was emitted by the
  journey.
- Marker summary was `2 markers`.
- The ten-command membership assertion passed before the acceptance helper.
- First product failure: Runtime returned HTTP `409` with
  `reason: capture_mismatch`, `code: conflict`, and message
  `submitted reads does not match authoritative capture` at
  `three-products.spec.ts:1181`.

The retained textual evidence is outside the disposable run root:

- Central result log/summary:
  `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/ap2-m2-ordinary-seeded-markers-central-gate-e2e-m2-ordinary-committed-driver-gate-1020215400-17002/`
- First-failure trace:
  `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-ordinary-seeded-markers-central-gate/central-first-failure.md`

The driver cleaned the binary Playwright trace during its required EXIT
cleanup; the textual failure and source tuple remain in the central result
directory and first-failure record.

## Not claimed

The failure prevented Agent/local/lost-ACK/restart/retry/undo/zero-legacy
assertions from running. Broad type diagnostics were not run or called passed;
the separate wrapper `tsc` issue is not treated as a dependency failure or a
reason to rerun the gate. No source fix, loop, dependency change, pin/schema
change, or adoption was made.

Recommended next step: investigate the authoritative-capture mismatch in the
ordinary ten-command submission, then run a new central gate only after a
committed source fix is available.
