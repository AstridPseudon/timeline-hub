# P1 App provenance correction

Disposition: PASS for the requested bounded correction. No H3 GO claim; the corpus remains authored-not-go.

## Changes

Only `src/tools/video-editor/commands/p1FeasibilityCorpus.test.ts` changed.

- Retained `git show <declared commit>:<declared path>` SHA-256 verification for all 8 corpus sources.
- Restored current-file SHA-256 equality for the 7 non-harness sources.
- Kept the mutable harness historical-only, bounded by the named `e2e-seed-and-harness` kind, the presence of `journey_sources` metadata, app ownership, and the exact `tests/e2e/local/support/harness.ts` path.
- No fixture declarations, behavior assertions, product code, harness code, session/outbox/schema/generated/pin/lock/dependency files, launcher, or root report changed.

## Historical/current SHA evidence

| Corpus source | Declared SHA | Historical `git show` SHA | Current SHA | Disposition |
|---|---|---|---|---|
| app-native-trim-real-document | `4d71a9d184db1b85c220de10842b2dc68e5eb9b48afee180b6c29cf0d5b06152` | `4d71a9d184db1b85c220de10842b2dc68e5eb9b48afee180b6c29cf0d5b06152` | `4d71a9d184db1b85c220de10842b2dc68e5eb9b48afee180b6c29cf0d5b06152` | current equality |
| app-track-label-real-document | `5aa9aed23a9764e4a9fb0d56fd5efc47368711933adbfaa224f2f725a766ed00` | `5aa9aed23a9764e4a9fb0d56fd5efc47368711933adbfaa224f2f725a766ed00` | `5aa9aed23a9764e4a9fb0d56fd5efc47368711933adbfaa224f2f725a766ed00` | current equality |
| app-move-real-document | `b2d3b5c43d495d3c53c741a1665b7c1afa7a95537938b54d35d3c498c2ad72a4` | `b2d3b5c43d495d3c53c741a1665b7c1afa7a95537938b54d35d3c498c2ad72a4` | `b2d3b5c43d495d3c53c741a1665b7c1afa7a95537938b54d35d3c498c2ad72a4` | current equality |
| app-ordinary-real-batch | `3190d1e3bac13bb69941477d1672b0d97a1dcad4465660e3f4535f584701ba46` | `3190d1e3bac13bb69941477d1672b0d97a1dcad4465660e3f4535f584701ba46` | `3190d1e3bac13bb69941477d1672b0d97a1dcad4465660e3f4535f584701ba46` | current equality |
| agent-split-created-id | `46bce505cbba3d72f7eb6c060ed9f1cf890e0c50c42a8f50a8edee7d6287e204` | `46bce505cbba3d72f7eb6c060ed9f1cf890e0c50c42a8f50a8edee7d6287e204` | `46bce505cbba3d72f7eb6c060ed9f1cf890e0c50c42a8f50a8edee7d6287e204` | current equality |
| agent-trim-real-document | `60fcc84d769a2a68b5330288e842ca286f3907510a5dd18bc240c6e314ee612c` | `60fcc84d769a2a68b5330288e842ca286f3907510a5dd18bc240c6e314ee612c` | `60fcc84d769a2a68b5330288e842ca286f3907510a5dd18bc240c6e314ee612c` | current equality |
| agent-sample-project-tiny3 | `f9348626c43de93409e25244ea1f81f6e86563a2f8650614fe862d618bcab51f` | `f9348626c43de93409e25244ea1f81f6e86563a2f8650614fe862d618bcab51f` | `f9348626c43de93409e25244ea1f81f6e86563a2f8650614fe862d618bcab51f` | current equality |
| three-products-seed-and-recovery | `2ba2164ba7fd2d76ccca94d0645e6b79236c85ab4e53e82e84ae1af250c7d815` | `2ba2164ba7fd2d76ccca94d0645e6b79236c85ab4e53e82e84ae1af250c7d815` | `b243b340177c2d905f841ec4c7307b03e7afd4f43f0096701c20bf132f202534` | historical-only named harness |

## Current-corruption counterexamples

Using in-memory mutations of the current App trim, App move, and Agent split JSON (no repository bytes changed):

- App trim: historical match `true`; corrupted current SHA `f2a6a35ed71332695f335f30b6f6c94949e55b29b9e695bdf3f8c983fd17413b`; current-integrity refusal `true`.
- App move: historical match `true`; corrupted current SHA `c0f59ace5608105405066ab667b34b496c5a3f49ffd832d62f7000b296ecb04f`; current-integrity refusal `true`.
- Agent split: historical match `true`; corrupted current SHA `4a6e54b0208c5e7ddce004d750e45a50545a99678124d89435bc775026fe33e7`; current-integrity refusal `true`.

## Exact verification

- `node node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --no-cache src/tools/video-editor/commands/p1FeasibilityCorpus.test.ts` — PASS; 1 file, 12 tests.
- `node node_modules/typescript/bin/tsc --noEmit` — PASS; exit 0.
- `node node_modules/eslint/bin/eslint.js src/tools/video-editor/commands/p1FeasibilityCorpus.test.ts --max-warnings 0` — PASS; exit 0.
- `git diff --check` — PASS; exit 0.
- Read-only 8-source historical/current SHA probe — PASS; all historical hashes match, seven current hashes match, harness is the sole historical-only mismatch.
- Read-only corruption probe — PASS; all three corrupted real fixtures would refuse on current-integrity comparison while historical bytes still match.
- No full, browser, heavy, or central test-service run requested.

