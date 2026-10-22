# P1 App provenance-fix handoff

Result: **PASS for the collection drift fix.** The corpus keeps strict
historical provenance while the behavioral checks continue to use the current
App/Agent fixture files. The H3 mixed App + Runtime + Agent chain remains
authored-not-go and unqualified, as required by the plan.

## Decision and implementation

`p1FeasibilityCorpus.test.ts` now verifies each declared `source.commit` and
`source.path` by hashing the immutable bytes returned by:

```text
git -C <source repository> show <source.commit>:<source.path>
```

This follows the existing repository convention used by the frozen-source
tests. `readSource()` and the imported App fixtures remain current working-tree
reads, so behavioral assertions do not silently execute historical code. The
fixture metadata and exact SHA equality assertion are unchanged; no digest was
refreshed and no provenance assertion was removed.

The repaired case is:

- declared source: App commit
  `3a10199e78e5a41ee6f6d7f4573ce2f11b33a87b`,
  `tests/e2e/local/support/harness.ts`
- declared/immutable source bytes SHA-256:
  `2ba2164ba7fd2d76ccca94d0645e6b79236c85ab4e53e82e84ae1af250c7d815`
- current App integration HEAD:
  `f9d5d0cdd666d4d68e5dfe6a2c29d513da92f8d9`
- current harness last-change commit:
  `15d9df3ce299e9e672dffbbb5a300e3d59fbdbf2`
- current mutable harness bytes SHA-256:
  `b243b340177c2d905f841ec4c7307b03e7afd4f43f0096701c20bf132f202534`

The declared commit is available in the local App git object database. A test
environment must retain the corpus-declared source commits; otherwise the
provenance check fails explicitly when `git show` cannot resolve the commit or
path.

For completeness, the immutable/current byte comparison is:

| corpus source | declared commit | immutable SHA | current SHA |
|---|---|---|---|
| `recipe_m2_clip_trim.json` | `afb774c875d9344132c697b1357a259e8f32f010` | `4d71a9d184db1b85c220de10842b2dc68e5eb9b48afee180b6c29cf0d5b06152` | `4d71a9d184db1b85c220de10842b2dc68e5eb9b48afee180b6c29cf0d5b06152` |
| `recipe_m2_app_track_label.json` | `927545cf52fdfbb273afbe7f190e00e11e5e2d70` | `5aa9aed23a9764e4a9fb0d56fd5efc47368711933adbfaa224f2f725a766ed00` | `5aa9aed23a9764e4a9fb0d56fd5efc47368711933adbfaa224f2f725a766ed00` |
| `recipe_m1_move.json` | `2048d8ddf04f23648aa86ca061f20e265350409c` | `b2d3b5c43d495d3c53c741a1665b7c1afa7a95537938b54d35d3c498c2ad72a4` | `b2d3b5c43d495d3c53c741a1665b7c1afa7a95537938b54d35d3c498c2ad72a4` |
| `ordinary_real_batch.json` | `b1887f206f454cfa0f998d93c0327e23dfbe6270` | `3190d1e3bac13bb69941477d1672b0d97a1dcad4465660e3f4535f584701ba46` | `3190d1e3bac13bb69941477d1672b0d97a1dcad4465660e3f4535f584701ba46` |
| `recipe_m2_clip_split.json` | `cda4d18ca1e0369ee2e1398f5d594ffda75647dc` | `46bce505cbba3d72f7eb6c060ed9f1cf890e0c50c42a8f50a8edee7d6287e204` | `46bce505cbba3d72f7eb6c060ed9f1cf890e0c50c42a8f50a8edee7d6287e204` |
| Agent `recipe_m2_clip_trim.json` | `cda4d18ca1e0369ee2e1398f5d594ffda75647dc` | `60fcc84d769a2a68b5330288e842ca286f3907510a5dd18bc240c6e314ee612c` | `60fcc84d769a2a68b5330288e842ca286f3907510a5dd18bc240c6e314ee612c` |
| Agent `tiny3.json` | `ded79f6dc2da14eb756064ad1ef1a8ffc0229e67` | `f9348626c43de93409e25244ea1f81f6e86563a2f8650614fe862d618bcab51f` | `f9348626c43de93409e25244ea1f81f6e86563a2f8650614fe862d618bcab51f` |
| `harness.ts` | `3a10199e78e5a41ee6f6d7f4573ce2f11b33a87b` | `2ba2164ba7fd2d76ccca94d0645e6b79236c85ab4e53e82e84ae1af250c7d815` | `b243b340177c2d905f841ec4c7307b03e7afd4f43f0096701c20bf132f202534` |

## Preserved assertions

The existing exact source SHA and 40-character commit assertions remain intact,
as do the real-fixture and behavioral checks for:

- App trim `from`/`to`/`hold`, speed and opaque data preservation, intent
  clearing, and recorded writes;
- Agent split command and created `right_id` binding;
- App move position/effects and disjoint authored-field preservation;
- H3 accepted/merged/refused metadata, Runtime wire dispositions, and all
  unavailable seam declarations;
- outbox Agent-head mutation, lost acknowledgement, owner disposal, restart
  recovery, exact first-request replay/key, dependent replay from the accepted
  head, and preserved Agent label data.

## Verification

- `node node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --no-cache src/tools/video-editor/commands/p1FeasibilityCorpus.test.ts` — PASS, 1 file, 12 tests.
- `node node_modules/typescript/bin/tsc --noEmit` — PASS, exit 0.
- `node node_modules/eslint/bin/eslint.js src/tools/video-editor/commands/p1FeasibilityCorpus.test.ts --max-warnings 0` — PASS, exit 0.
- `git diff --check` — PASS.

No browser, full, or heavy suite was run. No cases fixture, product/harness
source, runtime wire inventory, dependency install, or cache was changed.
