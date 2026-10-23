# P1 App provenance fixed independent review

Result: **PASS**.

No H3 GO claim; the corpus remains authored-not-go.

## Reviewed scope

- Reviewed commit: `b6baa5ce49138af4a2c326761c9d6760653b95e6` (`fix(app): restore P1 current fixture integrity`).
- `tl/ap2-P1-app-provenance-fix-r2` resolves to the same SHA; review worktree was clean.
- Commit diff from the first correction (`d2fcf3ff4d680b5086d924bdf398a41fd0ea87ca`): only `src/tools/video-editor/commands/p1FeasibilityCorpus.test.ts`, 21 insertions and 3 deletions.
- `tests/fixtures/p1-feasibility/cases.json` is unchanged (SHA-256 `9b1790e871e36099bb06b911bd0f5e03fb7fb49e907469e10a01affbc037dd6f`). The original behavior-test block is unchanged (SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`); Vitest still reports 12 tests.
- No product, harness, session, outbox, schema, generated, pin, lock, dependency, launcher, provider, executor, or test-expectation changes are present in the reviewed correction. No digest was rebaselined and no skip/xfail was added.

## Historical and current-byte verification

Every entry was independently checked with `git -C <repo> show <commit>:<path>` and SHA-256. Current SHA is from the exact current file path used by the test.

| Entry | Declared SHA | Historical SHA | Current SHA | Result |
|---|---|---|---|---|
| `app-native-trim-real-document` | `4d71a9d184db1b85c220de10842b2dc68e5eb9b48afee180b6c29cf0d5b06152` | `4d71a9d184db1b85c220de10842b2dc68e5eb9b48afee180b6c29cf0d5b06152` | `4d71a9d184db1b85c220de10842b2dc68e5eb9b48afee180b6c29cf0d5b06152` | current match |
| `app-track-label-real-document` | `5aa9aed23a9764e4a9fb0d56fd5efc47368711933adbfaa224f2f725a766ed00` | `5aa9aed23a9764e4a9fb0d56fd5efc47368711933adbfaa224f2f725a766ed00` | `5aa9aed23a9764e4a9fb0d56fd5efc47368711933adbfaa224f2f725a766ed00` | current match |
| `app-move-real-document` | `b2d3b5c43d495d3c53c741a1665b7c1afa7a95537938b54d35d3c498c2ad72a4` | `b2d3b5c43d495d3c53c741a1665b7c1afa7a95537938b54d35d3c498c2ad72a4` | `b2d3b5c43d495d3c53c741a1665b7c1afa7a95537938b54d35d3c498c2ad72a4` | current match |
| `app-ordinary-real-batch` | `3190d1e3bac13bb69941477d1672b0d97a1dcad4465660e3f4535f584701ba46` | `3190d1e3bac13bb69941477d1672b0d97a1dcad4465660e3f4535f584701ba46` | `3190d1e3bac13bb69941477d1672b0d97a1dcad4465660e3f4535f584701ba46` | current match |
| `agent-split-created-id` | `46bce505cbba3d72f7eb6c060ed9f1cf890e0c50c42a8f50a8edee7d6287e204` | `46bce505cbba3d72f7eb6c060ed9f1cf890e0c50c42a8f50a8edee7d6287e204` | `46bce505cbba3d72f7eb6c060ed9f1cf890e0c50c42a8f50a8edee7d6287e204` | current match |
| `agent-trim-real-document` | `60fcc84d769a2a68b5330288e842ca286f3907510a5dd18bc240c6e314ee612c` | `60fcc84d769a2a68b5330288e842ca286f3907510a5dd18bc240c6e314ee612c` | `60fcc84d769a2a68b5330288e842ca286f3907510a5dd18bc240c6e314ee612c` | current match |
| `agent-sample-project-tiny3` | `f9348626c43de93409e25244ea1f81f6e86563a2f8650614fe862d618bcab51f` | `f9348626c43de93409e25244ea1f81f6e86563a2f8650614fe862d618bcab51f` | `f9348626c43de93409e25244ea1f81f6e86563a2f8650614fe862d618bcab51f` | current match |
| `three-products-seed-and-recovery` | `2ba2164ba7fd2d76ccca94d0645e6b79236c85ab4e53e82e84ae1af250c7d815` | `2ba2164ba7fd2d76ccca94d0645e6b79236c85ab4e53e82e84ae1af250c7d815` | `b243b340177c2d905f841ec4c7307b03e7afd4f43f0096701c20bf132f202534` | historical-only named harness |

The historical-only branch is exactly `kind === e2e-seed-and-harness`, App ownership, exact path `tests/e2e/local/support/harness.ts`, and `journey_sources` presence. All other entries require current SHA equality. `git show` uses uncaught `execFileSync`; a missing history object/path exits nonzero and fails closed, with no fallback to current bytes.

## Corruption counterexamples

Using isolated in-memory mutations only (no repository bytes changed), each historical match remained true while the current-integrity check rejected the mutated bytes:

- App trim: current `4d71a9d184db1b85c220de10842b2dc68e5eb9b48afee180b6c29cf0d5b06152`; corrupted `f2a6a35ed71332695f335f30b6f6c94949e55b29b9e695bdf3f8c983fd17413b`.
- App move: current `b2d3b5c43d495d3c53c741a1665b7c1afa7a95537938b54d35d3c498c2ad72a4`; corrupted `c0f59ace5608105405066ab667b34b496c5a3f49ffd832d62f7000b296ecb04f`.
- Agent split: current `46bce505cbba3d72f7eb6c060ed9f1cf890e0c50c42a8f50a8edee7d6287e204`; corrupted `8aa1ff7990ef552122a96ee27151f41e16a554e317955668ae317e10338e4d5d`.

## Verification commands

- `node node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --no-cache src/tools/video-editor/commands/p1FeasibilityCorpus.test.ts` — PASS; 1 file, 12 tests.
- `node node_modules/typescript/bin/tsc --noEmit` — PASS; exit 0.
- `node node_modules/eslint/bin/eslint.js src/tools/video-editor/commands/p1FeasibilityCorpus.test.ts --max-warnings 0` — PASS; exit 0.
- `git diff --check` — PASS; exit 0.
- Inline read-only 8-entry historical/current SHA probe — PASS; all historical hashes match, seven current hashes match, harness is the sole current mismatch.
- Inline read-only trim/move/split corruption probe — PASS; all three current-integrity checks reject.
- Missing-history `git show` probe — PASS; nonzero exit confirms fail-closed behavior.

No full, browser, heavy, or central test-service run was requested.
