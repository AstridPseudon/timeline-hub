# AP2 M2 ordinary mounted journey gate

## Result

Source-only candidate prepared from current App HOME `480db7feb`; central gate intentionally not requested because source changed and the worker must stop at a committed candidate. No pins, API/schema/dependency changes, extra App copy, local browser/socket run, or full suite.

## Changes

- Ported the reviewed generic capture read-order fix: `source_offset`, `speed`, then track/time-map reads, preserving the existing `clipTrim0fa`, `selected5a`, and `owner7d` state.
- Admitted the reviewed App-owned Scene Phase Markers extension beside the generated catalog, and made `openCommandTimeline` establish authoring admission for standalone cases.
- Added the reviewed marker constants/seed data and focused authoring-admission/marker-reader regression checks.
- Ported the reviewed real ordinary five-member fixture, parity helper, and capture assertions; the ordinary disjoint Agent edit uses `S1`, while local App editing remains on `V1`.
- Repaired the ordinary undo oracle one-to-one from the independent pre-ordinary Runtime document plus the preserved Agent `S1` label. It compares the complete raw parent payload, pre-edit shot/internal closure arrays, and dependency manifest, retaining existing position, opaque, immutable-closure, zero-legacy, and credential checks. It does not derive expected state from the inverse response.

## Failure diagnosis

The prior central run was `ap2-m2-ordinary-disjoint-rebase-review-gate-e2e-m2-ordinary-committed-driver-gate-1020222651-25944` (exit 1). Ten commands, retry/rebase, and S1-versus-V1 assertions passed. The first failure was the old `tests/e2e/local/three-products.spec.ts:1273` whole-document equality against `agentEdit.data.canonical_document`. Undo correctly restored the independent pre-ordinary authored positions/holds, while `agentEdit` still represented the derived ordinary revision. The raw diff also showed materialized revision/content identifiers. The new oracle follows the approved duplicate-removal precedent without dropping raw or closure assertions.

## Verification

All commands ran in this worker with no browser, live socket, or full suite:

- `node_modules/.bin/vitest run --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/commands/genericPatchCapture.test.ts src/tools/video-editor/commands/ordinaryRealBatch.test.ts` — PASS, 2 files / 17 tests.
- `node_modules/.bin/vitest run --no-cache --maxWorkers=1 --no-file-parallelism src/test/threeProductsAuthoring.test.ts` — PASS, 1 file / 4 tests.
- `node_modules/.bin/eslint --max-warnings 0` on all changed TypeScript files — PASS.
- `git diff --check` and JSON parse of `ordinary_real_batch.json` — PASS.

The catalog test is excluded by the repository's default Vitest config; an isolated temporary-config attempt did not produce a result before its timeout and the temporary config was removed. No catalog test result is claimed.

## Next gate

After the harness commits this candidate and confirms a clean worktree, run exactly once through the central service:

```sh
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test ap2-m2-ordinary-mounted-journey-gate e2e-m2-ordinary-committed-driver-gate --no-cache) && /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"
```

Use the absolute driver `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-ordinary-committed-driver-gate/run-central-m2-ordinary.sh`; its source guards must continue selecting Agent `8130a401bf44a518d5a40ae274d398b8c560be55` / tree `236c3e57e0265c52b81ba8085de3193026176bff` and Runtime `2c4ac180c2220bdad966bc01e95ad230e99ce26a` / tree `7ab412cc4bcbe517efcfa806e092336390312e18`.

## Blockers

None for source completion. The central ordinary qualification remains unverified until the committed candidate is run by the central service.
