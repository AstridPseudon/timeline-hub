# App D01 duplicate HOME merge and ledger finish

Date: 2026-10-20 UTC  
Worker: `ap2-m2-duplicate-home-merge-ledger-finish`  
Repo: App

## Result

The HOME merge completed after the owner-review wait:

- Candidate: `d1191f4be175d37d4f677e1f7109e6f0d91fd6c7`
- Actual HOME merge SHA: `8c0e1f799b64e9b6f179018b7dff01479d43c85c`
- Merge result artifact: `MERGED 8c0e1f799`

The App D01 duplicate row is now `DELETED` in both `deletion-ledger.app.md` and the corresponding master `deletion-ledger.md`. No other ledger rows were changed. The row does not claim whole-App zero-writer completion.

## Exact-SHA verification

Read-only verification was run against `/home/user/work/app` at the full merged SHA:

```sh
git -C /home/user/work/app show --no-ext-diff --format=fuller --stat --summary 8c0e1f799b64e9b6f179018b7dff01479d43c85c
git -C /home/user/work/app diff-tree --no-commit-id --name-status -r 8c0e1f799b64e9b6f179018b7dff01479d43c85c^1 8c0e1f799b64e9b6f179018b7dff01479d43c85c
git -C /home/user/work/app merge-base --is-ancestor d1191f4be 8c0e1f799b64e9b6f179018b7dff01479d43c85c
git -C /home/user/work/app grep -n -I 'duplicateIndependentShot' 8c0e1f799b64e9b6f179018b7dff01479d43c85c -- .
git -C /home/user/work/app ls-tree -r --name-only 8c0e1f799b64e9b6f179018b7dff01479d43c85c
```

Results:

- The candidate is an ancestor of the actual merged SHA.
- `duplicateIndependentShot` has zero references at the merged SHA, including zero production references.
- Native consumers remain present: `src/tools/video-editor/commands/occurrenceDuplicateCapture.ts`, `occurrenceDuplicateGesture.ts`, `commitSession.occurrenceDuplicate.test.ts`, and `tests/e2e/local/three-products.spec.ts`.
- The merged integration branch subsequently resolved to the same full SHA.

## Central qualification evidence

The existing independent central command was:

```sh
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test ap2-m2-duplicate-final-state-review-gate e2e-m2-duplicate-effective-graph-three-products) && /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"
```

Recorded result: `ap2-m2-duplicate-final-state-review-gate-e2e-m2-duplicate-effective-graph-three-products-1020204512-19235`, exit 0, one test passed in 118 seconds (journey 40.8 seconds). This was the existing central qualification; it was not rerun by this ledger worker, per the task instructions.

The existing assertion-conversion map records:

- The tautological `undoDuplicate.data.canonical_document === agentEdit.data.canonical_document` expectation was replaced with the exact pre-A `parent_revision.payload` / `structuredClone(beforeDocument)` baseline plus literal independent C’s `S1` label.
- Duplicate absence remained asserted, with exactly one preserved original pre-A occurrence.
- Exact pre-A shot/internal closure identities, digests, payloads, dependency manifest, opaque fields, and array/order fidelity remained asserted.
- Local B undo, zero legacy traffic, credentials, and the dependency-conflict negative journey remained asserted.

## Tests and checks

No product tests were rerun here. The task explicitly prohibited a full/browser/socket rerun. The existing reports record these passing candidate checks:

```sh
./node_modules/.bin/eslint tests/e2e/local/three-products.spec.ts --max-warnings 0
./node_modules/.bin/vitest run --config config/testing/vitest.config.ts --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/commands/occurrenceDuplicateCapture.test.ts src/tools/video-editor/commands/occurrenceDuplicateGesture.test.ts src/tools/video-editor/commands/commitSession.occurrenceDuplicate.test.ts
npm run typecheck:strict-probe
./node_modules/.bin/playwright test --config playwright.three-products.config.ts --list --grep 'M2 native occurrence duplicate'
git diff --check
```

Recorded results: ESLint clean; 3 files/45 Vitest tests passed; strict probe passed; one Playwright test listed without browser/socket execution; diff check clean. Central qualification is the pass identified above. No full suite, local browser, localhost/live socket, or additional central run was performed by this worker.

## Decisions and blockers

The App and master D01 rows were updated together because the normal ledger workflow keeps the area ledger and master row synchronized. The actual HOME merge SHA is recorded separately from the candidate SHA. The duplicate deletion is complete, but the broader App writer-removal and Gate 6 work remain open. No blocker remains for this bounded ledger task.
