# AP2 M2 ordinary actual journey gate

## Candidate prepared

App test source:

- `tests/e2e/local/three-products.spec.ts`: adds `M2 ordinary extension batch: move and hold, Agent label, lost ACK, restart, exact retry and guarded undo`.
- `tests/e2e/local/support/harness.ts`: the existing three-products seed now includes two production Scene Phase Markers (`ordinary-marker-a` at 1 and `ordinary-marker-b` at 6) in `config.app['haus.astrid.scene-phase-markers']`.

The journey opens the production-mounted Scene Phase Markers extension, invokes its public panel action, and observes one generic-port outbox intent containing two supported move+hold edits. It then applies a disjoint Agent label, creates a newer local App label, loses the ACK, reloads, restarts Runtime, performs exact persisted retry and guarded recovery, undoes the newer label and the grouped ordinary batch, and verifies the Agent edit, opaque fields, history, immutable closure, and zero legacy snapshot traffic. The journey's mutation path does not call Runtime POST directly or install a test-only provider/callback; the existing fixture seed remains the only direct setup mechanism.

The existing unsupported-mixed refusal coverage remains in the generic patch tests. No positive unsupported matrix was added and no passing behavior expectation was weakened.

## Candidate prerequisite before central execution

The production extension source in the current App tree still emits these public operations from `buildAlignShotsPatch`:

- `clip.move` payload `{ track, at }`
- `clip.update` payload `{ hold, mode: 'merge' }`

The generic ordinary port intentionally accepts the normalized native shapes used by the test assertions:

- move: payload `{ at }`, producing `clip.move` args `{ on }`
- scalar hold: payload `{ values: { hold }, clear: [] }`, producing `clip.set`

Therefore the exact candidate used by the central lane must include the production extension's minimal normalization to those supported shapes (while preserving the extension's public `timeline.apply`, source/meta, ordering, and existing extension tests). Do not bypass the extension or add a test-only production callback. The test is intentionally not marked as passing against today's builder because that would encode a false positive.

## Locked central prerequisites

Use the already locked normal tuple only:

- Composition public package `0.0.13`
- Agent `8130a401bf44a518d5a40ae274d398b8c560be55`
- Runtime `2c4ac180c2220bdad966bc01e95ad230e99ce26a`

The central lane should run only after this App candidate and the extension normalization are committed and registered. Register a named `e2e-m2-ordinary-three-products` suite in the central suites configuration with the existing locked Node graph and command:

```text
npm run test:e2e:three-products -- --grep "M2 ordinary extension batch"
```

Then the orchestrator can request it once using the normal central test service; this worker did not run browser, localhost, socket, or full-suite tests.

## Local evidence

Passed:

```text
git diff --check
node_modules/.bin/eslint tests/e2e/local/three-products.spec.ts tests/e2e/local/support/harness.ts --max-warnings 0
node_modules/.bin/vitest run --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/commands/genericPatchCapture.test.ts src/tools/video-editor/commands/ordinaryMoveMember.test.ts src/tools/video-editor/commands/ordinaryScalarMember.test.ts src/tools/video-editor/commands/commitSession.genericPatch.test.ts
```

Result: 4 test files passed, 21 tests passed.

Collection-only check passed:

```text
node_modules/.bin/playwright test tests/e2e/local/three-products.spec.ts --config playwright.three-products.config.ts --list
```

Result: 8 tests collected, including the new journey. No browser execution was performed.

The requested app project typecheck was run with `node_modules/.bin/tsc -p tsconfig.app.json --noEmit --pretty false` and exits 2 on existing diagnostics in `elementCapture.ts`, `elementGesture.ts`, `genericPatchCapture.ts`, `occurrenceDuplicateCapture.ts`, `ordinaryMoveMember.ts`, `ordinaryScalarMember.ts`, and Composition integration/export files. The edited E2E files are not among the diagnostics.
