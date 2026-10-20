# App M2 duplicate final undo expectation repair

Date: 2026-10-20 UTC  
Worker: `ap2-m2-duplicate-final-undo-expectation-fix`  
Repo: App  
Base/candidate source: `846d2b018af63b63977ea399d33e3470989836e7` plus this uncommitted test-only change

## Result

Corrected the final duplicate-undo expected baseline in
`tests/e2e/local/three-products.spec.ts`. The test no longer compares the
post-duplicate undo document with `agentEdit`, whose response was captured
after A and therefore still legitimately contained A's copied occurrence.

The expected authored state now comes from the real pre-A Runtime parent
fixture, with only the independent C edit applied to track `S1`. It retains
exact parent payload ordering and opaque fields, checks the original
pre-A occurrence exactly once and the copied occurrence absent, and compares
the original pre-A shot/internal closure identities, digests, payloads, and
dependency manifest. Existing immutable-closure, opaque-child/parent,
zero-legacy, and credential assertions remain.

No product source, Runtime behavior, API, schema, dependency, pin, or
compiler behavior changed.

## Assertion conversion map

| Previous assertion | Corrected assertion | Reason |
|---|---|---|
| `undoDuplicate.data.canonical_document === agentEdit.data.canonical_document` | Exact `parent_revision.payload` against `structuredClone(beforeDocument)` plus C's explicit `S1` label; exact pre-A shot/internal closure and manifest comparisons | `agentEdit` was based on A and necessarily still contained A's duplicate |
| Duplicate occurrence `some(...) === false` | Retained verbatim, plus original pre-A occurrence filter has length 1 | Keeps the direct deletion and no-double-occurrence checks |
| Final opaque parent leaf check | Exact full pre-A-derived parent payload plus existing `expectOpaqueDataKept` and `expectImmutableClosure` | Preserves unrelated own fields, opaque data, persisted closure, and generated revision/digest validation without normalizing or dropping fields |
| Implicit closure coverage from whole-document equality | Exact pre-A shot/internal IDs, digests, payloads and dependency manifest, followed by existing `expectImmutableClosure` | Accounts for deterministic compiler revision identities through the existing Runtime readback/closure helper |

The separate real dependency-conflict journey remains unchanged and continues to
assert the negative causal guard (`409`, non-stale-head conflict, retained B
guards/intent).

## Validation

Passed directly in this worktree:

```
./node_modules/.bin/eslint tests/e2e/local/three-products.spec.ts --max-warnings 0
./node_modules/.bin/vitest run --config config/testing/vitest.config.ts --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/commands/occurrenceDuplicateCapture.test.ts src/tools/video-editor/commands/occurrenceDuplicateGesture.test.ts src/tools/video-editor/commands/commitSession.occurrenceDuplicate.test.ts
  3 files, 45 tests passed
npm run typecheck:strict-probe
  tsc -p tsconfig.strict-islands.json --noEmit passed
./node_modules/.bin/playwright test --config playwright.three-products.config.ts --list --grep 'M2 native occurrence duplicate'
  1 test listed; no browser/socket run
git diff --check
```

Not run: local browser, localhost/live socket, full suite, central effective
graph, or dirty-source request. The central gate remains unverified after this
change.

## Post-commit effective-graph gate

After the harness commits the worktree, run exactly:

```sh
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test ap2-m2-duplicate-final-undo-expectation-fix e2e-m2-duplicate-effective-graph-three-products) && /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"
```

This uses the existing private effective-graph runner and must be the next
independent browser qualification; do not claim the duplicate gate qualified
until it passes.
