# App M2 duplicate final-state review gate

Date: 2026-10-20 UTC  
Worker: `ap2-m2-duplicate-final-state-review-gate`  
Repo: App  
Candidate commit: `d1191f4be175d37d4f677e1f7109e6f0d91fd6c7`  
Candidate tree: `c7c022ecc83a37d87280e5dd8d45792f050d5369`

## Result

APPROVED and centrally qualified. The candidate fixes the final duplicate-undo
oracle without changing product source, schema, API, dependencies, pins, or
Runtime/Agent/Composition sources.

The prior `1717` central run failed at the old whole-document assertion because
`agentEdit` was captured after duplicate A and therefore still contained A's
copied occurrence. Its earlier causal phases passed. The candidate removes
that tautological expected value and derives the expected final authored state
from the independent pre-A Runtime parent fixture, then applies the literal C
edit to track `S1` (`F2 Agent duplicate sibling`).

The independent review verified that the conversion retains:

- exact raw parent payload, including opaque fields and array/order fidelity;
- duplicate A removal and exactly one preserved original occurrence;
- literal independent C survival and local B undo restoration;
- exact pre-A source shot and internal-timeline closure identities, digests,
  payloads, and dependency manifest;
- Runtime-backed immutable-closure validation;
- zero legacy save traffic and credential leak checks;
- the existing dependency-conflict negative journey and retained B guards.

No expected value is copied from the final undo response or from the
post-duplicate `agentEdit` response. The changed test is the only candidate
file change.

## Central qualification

Exactly one central request was submitted through the named app integration
suite:

```sh
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test ap2-m2-duplicate-final-state-review-gate e2e-m2-duplicate-effective-graph-three-products) && /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"
```

Result: `ap2-m2-duplicate-final-state-review-gate-e2e-m2-duplicate-effective-graph-three-products-1020204512-19235`, exit 0, one test passed in 118 seconds (journey 40.8 seconds). The run included private effective Composition 0.0.13 setup, hosted build, Chromium launch, and the single `M2 native occurrence duplicate` journey through final guarded undo.

Central source tree: `c7c022ecc83a37d87280e5dd8d45792f050d5369`. The fixed
cohort remained Agent `8130a401bf44a518d5a40ae274d398b8c560be55`, Runtime
`2c4ac180c2220bdad966bc01e95ad230e99ce26a`, and Composition 0.0.13. No source
guard or external tuple update was needed.

## Other validation

Recorded candidate checks passed:

```sh
./node_modules/.bin/eslint tests/e2e/local/three-products.spec.ts --max-warnings 0
./node_modules/.bin/vitest run --config config/testing/vitest.config.ts --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/commands/occurrenceDuplicateCapture.test.ts src/tools/video-editor/commands/occurrenceDuplicateGesture.test.ts src/tools/video-editor/commands/commitSession.occurrenceDuplicate.test.ts
npm run typecheck:strict-probe
./node_modules/.bin/playwright test --config playwright.three-products.config.ts --list --grep 'M2 native occurrence duplicate'
git diff --check
```

Results were ESLint clean, 3 files/45 Vitest tests passed, strict probe passed,
one Playwright test listed without browser/socket execution, and diff check
clean. No local browser, localhost/live-socket, full, or dirty-source run was
performed by this review worker.

## Handoff

The duplicate qualification is ready for HOME deletion merge. The central pass
does not claim the ledger's post-merge deleted SHA; that remains for the merge
and subsequent ledger update.

