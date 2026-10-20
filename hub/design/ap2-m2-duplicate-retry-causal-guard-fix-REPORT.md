# App M2 duplicate retry causal-guard fixture repair

Date: 2026-10-20 UTC  
Worker: `ap2-m2-duplicate-retry-causal-guard-fix`  
Repo: App  
Base: `tl/ap2-m2-duplicate-current-joined-deletion-gate`  
Base commit: `9caf57adb`

## Result

Classified the first failure from effective-graph gate
`ap2-m2-duplicate-effective-graph-actual-gate-e2e-m2-duplicate-effective-graph-three-products-1020201231-672`.
It was a fixture conflict, not an over-broad production guard.

The gate's A/B/C sequence was:

1. A: App occurrence duplicate, accepted but acknowledgement lost.
2. C: real Agent `track.set` on `parent/track:V1`, changing its label from
   absent in the duplicate's captured dependency view to
   `F2 Agent duplicate sibling`.
3. B: local App `track.set` on the same `parent/track:V1`, captured over A and
   retained until A recovery.

The exact retry correctly returned `409 conflict` with
`dependency_changed`, path `label`, ref `parent/track:V1`, because C changed
B's original dependency. This is the intended causal guard behavior and must
remain a real negative case elsewhere; no production guard was weakened,
dropped, or recaptured.

## Change

Changed only `tests/e2e/local/three-products.spec.ts`:

- C remains the same real Agent `track.set` producer, but targets the seeded
  independent parent row `S1` instead of B's `V1` row.
- The retry success assertion now requires both independent Agent `S1` and
  local B `V1` labels.
- The first guarded undo assertion requires the Agent `S1` label to survive.

The seeded canonical parent has both `V1` and `S1` tracks. This keeps the
Agent intervention, local B, retry/rebase, guarded undo, opaque-data, and
zero-legacy assertions while making C genuinely disjoint from B. The existing
same-field conflict negative is preserved by the separate dependency-conflict
journey; this repair does not turn a conflict assertion into success.

No production source, command schema, wire/API, dependency guard, pin,
provider, or Runtime behavior changed.

## Validation

Passed:

```text
./node_modules/.bin/eslint tests/e2e/local/three-products.spec.ts --max-warnings 0
./node_modules/.bin/vitest run --config config/testing/vitest.config.ts --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/commands/occurrenceDuplicateCapture.test.ts src/tools/video-editor/commands/occurrenceDuplicateGesture.test.ts src/tools/video-editor/commands/commitSession.occurrenceDuplicate.test.ts
  3 files, 45 tests passed
npm run typecheck:strict-probe
./node_modules/.bin/playwright test --config playwright.three-products.config.ts --list --grep 'M2 native occurrence duplicate'
  1 test listed; no browser/socket run
git diff --check
```

No local browser, localhost/socket, full suite, or central service rerun was
run. The effective-graph gate therefore remains unverified after this change.

## Post-commit central handoff

After the harness commits this candidate, request exactly one effective-graph
targeted service run (the existing runner verifies the private Composition13
graph and exact Agent/Runtime tuple):

```sh
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test ap2-m2-duplicate-retry-causal-guard-fix e2e-m2-duplicate-effective-graph-three-products) && /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"
```

Do not mark D01-app-duplicate qualified/deleted until that committed
effective-graph run passes all existing duplicate journey assertions.
