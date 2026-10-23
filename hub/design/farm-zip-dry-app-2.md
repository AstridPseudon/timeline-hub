# tf-zip-app-2: F-zip-dry rehearsal, App (REPO=app, BASE=7c17cc9d9), resumed steps 3-4

Rehearsal only. Nothing pushed; no edits to the repo, tests, pins or locks; no commit, reset, merge or checkout in /home/user/work/app. Scratch lives in the worker tmpdir `/tmp/w-2b8bf3e808/` (the path in `workers/tf-zip2-app/tmpdir`), under the session scratchpad `.../ecd898e2-a1c9-4e75-89cc-73c99d6abde0/scratchpad/fz2/`.

**Outcome: all five steps ran. No refusals.** Step 2 needed one correction in my own staging method (see Step 2). Step 4 result: 7 strict-apply conflicts, reproducing the earlier report exactly.

## Summary

| Step | Result | Key numbers |
|---|---|---|
| 1. Record integration, base, ancestry | PASS | integration `6294895141`, tree `03714e15a`; base is ancestor |
| 2. Squashed patch; fresh clone at BASE; apply; tree equality | PASS (after a staging fix, below) | 8,435,056 bytes, 517 files; applied tree `03714e15a` = integration tree |
| 3. Fast checks on applied tree (private graph, 0.0.14 archive) | PASS | tsc app 0, tsc node 0, full-repo lint 0, two quality guards 0, smoke 444 + 2793 tests passed |
| 4. Apply against live upstream tip | 7 conflicts (strict per-file); 4 unmerged under 3-way | tip `efe83c77e`, 510/517 apply cleanly strict |
| Composition 0.0.14 archive check | PASS | sha256 `819acf6b…2040234`, package.json version 0.0.14 |

## Step 1: SHAs and ancestry

| Item | Value |
|---|---|
| BASE `7c17cc9d9f9504b578862e2ffd27623fca08a04f` | (full SHA, `git rev-parse`) |
| Integration `tl/integration` (`/home/user/work/app`) | commit `6294895141ffe0e92a83c61ba0541249a41243eb`, tree `03714e15af54da54865c1d732b2ea03900731fe1` |
| Hub `hub/timeline/app/tl/integration` | `6294895141ffe0e92a83c61ba0541249a41243eb` (same) |
| Worker worktree `tl/tf-zip2-app` | HEAD `6294895141`, tree `03714e15a` (clean) |
| BASE ancestor of integration | yes (`git merge-base --is-ancestor`, exit 0) |

Integration differs from the earlier report's head (`411ff10bd`, tree `0b19a5a9e`). The integration moved on since then; the earlier report is superseded.

## Step 2: squashed patch and fresh clone

1. Patch: `git -C /home/user/work/app diff --binary 7c17cc9d9f9504b578862e2ffd27623fca08a04f 6294895141ffe0e92a83c61ba0541249a41243eb > fz2/app-base-to-integration.patch`
   - **8,435,056 bytes; 517 files** (`grep -c '^diff --git'` = 517; `git diff --name-status` = 517).
2. Fresh clone: `git clone https://github.com/banodoco/reigh-app fz2/app-fresh` (exit 0), then `git checkout --detach 7c17cc9d9f9504b578862e2ffd27623fca08a04f` (exit 0). This is the step the earlier report was refused on; here it ran.
3. `git apply --check <patch>` → exit 0. `git apply <patch>` → exit 0. Only whitespace warnings (trailing whitespace in added lines; not failures).
4. Tree check: first `git add -A` then `git write-tree` gave `021d79762f5187e3ef1fc294b0fe363665f35986` ≠ `03714e15a`. `ls-tree -r` diff showed exactly one missing path: `docs/cutover-inventory.md`. Cause: the repo's `.gitignore:49` is `*.md`, so `git add -A` skipped the new file. The integration commit tracks it (force-added). The patch itself is correct; the defect was my staging command.
   - Fix: `git add -f docs/cutover-inventory.md`, then `git write-tree` → **`03714e15af54da54865c1d732b2ea03900731fe1`, equal to the integration tree.**
   - Harness note for the farm procedure: any "fresh tree" check must use `git add -f` for tracked-but-ignored paths, or compare `ls-tree` listings, or `git add -A` will undercount by the force-added `.md` files.

## Step 3: fast checks on the applied fresh tree

Private graph: `npm ci --no-audit --no-fund --prefix fz2/app-fresh` (exit 0; "added 576 packages"; postinstall applied the Remotion 4.0.509 audio-resume patch inside the private graph only). Shared `/home/user/work/app/node_modules` was not touched.

The Composition archive the package pins is `vendor/artifacts/banodoco-timeline-composition-635f4de06fda22a85fc2e4cfc764d0153a4c9f40.tgz`:
- `sha256sum` = `819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234` (matches the brief's SHA; its `.sha256` file agrees)
- `tar -xzOf … package/package.json` → `"version": "0.0.14"`
- installed as `node_modules/@banodoco/timeline-composition` (a real directory in the private graph), version 0.0.14.

| Check | Command | Exit / result |
|---|---|---|
| Typecheck app | `node …/typescript/bin/tsc -p …/tsconfig.app.json --noEmit` | 0 |
| Typecheck node | `node …/typescript/bin/tsc -p …/tsconfig.node.json --noEmit` | 0 |
| Lint (repo script, full repo) | `npm run --prefix …/app-fresh lint` (`eslint . --ext ts,tsx --report-unused-disable-directives --max-warnings 0`) | 0 |
| Guard | `node scripts/quality/check-no-smoke-tests.mjs` | 0, "No placeholder smoke tests found." |
| Guard | `node scripts/quality/check-known-failures.mjs` | 0, 0 authorized and 0 forbidden expected-failure markers |
| Smoke set 1 (3 files) | `node node_modules/vitest/vitest.mjs run --root <fresh> --config <fresh>/config/testing/vitest.config.ts --cache=false` + `src/sdk/index.test.ts src/sdk/manifest-schema-validation.test.ts src/shared/hooks/__tests__/usePromoteVariantToGeneration.test.ts` | 0; **3 files, 444 tests passed** |
| Smoke set 2 (10 files) | same, + `src/integrations/runtime/{timelineCommit,dataProvider,resolveProjectSelector,vendorLock}.test.ts`, `src/sdk/examples-governance.test.ts`, `src/shared/lib/placement/__tests__/placementService.test.ts`, `src/shared/lib/media/mediaCrossOrigin.test.ts`, `src/shared/state/selectionClipData.test.ts`, `src/shared/hooks/shots/__tests__/useShotGenerationMutations.test.ts`, `src/integrations/paired/pairedRoutePolicy.test.ts` | 0; **10 files, 2793 tests passed** |

Not run (not asked, or not fast): full suite; `typecheck:strict-islands`; `lint:edge`; `test:edge*`; Playwright; `check:*` governance scripts beyond the two guards. No full suite was requested and none was run.

## Step 4: live upstream tip

- Re-fetched: `git ls-remote https://github.com/banodoco/reigh-app refs/heads/main` = `efe83c77e1bbbb5eaae36f3a9f999f027f982e94`; the scratch clone's `fetch origin main` then `rev-parse origin/main` = the same. Tip **`efe83c77e`**.
- Drift: `git rev-list --count 7c17cc9d9..origin/main` = **25** (the earlier report said 27; this count is the measured one). `6e3445ee9` (the deferred SHA) is an ancestor of the tip, so it is inside the drift. The 25 commits include product-touching items the orchestrator should see: `7f0067d01` (drop the dead pictureTracks seam code), `2fbc6754c` (refuse cross-project gallery adds). Most of the rest is e2e/CI.

Method A — strict, per file (the earlier method; no 3-way). Each of the 517 patch chunks split out and checked with `git apply --check --binary` in a clean clone at the tip (`fz2/app-tip2`): **510 apply cleanly, 7 conflict**:

| File | Strict result |
|---|---|
| `config/testing/vitest.astrid-renderer.config.ts:26` | patch failed |
| `config/testing/vitest.boundary.config.ts:1` | patch failed |
| `config/testing/vitest.config.ts:1` | patch failed |
| `package.json:13` | patch failed |
| `tests/e2e/local/support/app.ts:105` | patch failed |
| `tests/e2e/local/support/harness.ts:45` | patch failed |
| `supabase/functions/_tests/mocks/groqSdk.ts` | already exists in working directory (add/add) |

These match the earlier report's 7 exactly.

Method B — 3-way: `git apply --3way <patch>` in a second clean tip clone (`fz2/app-tip`), exit 1 with 4 unmerged paths (`git diff --name-only --diff-filter=U`): `config/testing/vitest.astrid-renderer.config.ts`, `package.json`, `supabase/functions/_tests/mocks/groqSdk.ts`, `tests/e2e/local/support/harness.ts`. Three of the strict-7 (`vitest.boundary.config.ts`, `vitest.config.ts`, `tests/e2e/local/support/app.ts`) merge cleanly under 3-way. The 3-way log also has one "repository lacks the necessary blob" line that fell back to direct application; status afterward shows all 517 paths present, so no path was lost. Both methods are recorded; the strict count is the conservative number.

Classification: **product/merge-forward drift**, not harness or environment. The 25-commit upstream drift touches the same vitest configs, `package.json` scripts and e2e support files as the integration. Upstream also added `supabase/functions/_tests/mocks/groqSdk.ts` independently. Nothing here is a refusal.

## Dependency note: `@supabase/supabase-js` (CLAUDE.md forbids `@supabase/*`)

- Integration `package.json:135`: `"@supabase/supabase-js": "^2.49.4"` under `dependencies`. The base `package.json` has no `@supabase` entry, so the integration adds it.
- `src/` import: **none.** `Grep "@supabase/"` over the integration worktree's `src/` returns no matches. The only other references are `config/testing/vitest.edge.aliases.ts:30-32` (mock aliases for the Edge tests), `package.json:23` (`lint:edge` over `supabase/functions`), and `supabase/functions/**`, which the integration also edits and I did not review in depth.
- Lint passes with the declaration in place, because no `src/` file imports it. The declaration itself still contradicts CLAUDE.md ("do not add … `@supabase/*`"). Recommendation: the App lane removes the dependency line (and the matching lockfile entries) in the integration; I did not change it.

## Other findings

1. **Composition version label is ambiguous.** The brief's "0.0.14 archive" (SHA `819acf6b…`) is the vendored `635f4de…tgz`, which is what `package.json:125` pins. But `/home/user/work/agent/remotion/artifacts/banodoco-timeline-composition-0.0.14.tgz` (and the same file in `wt/tf-zip2-agent`) is also labelled 0.0.14 with a **different** SHA, `21fde4d2a5d6…`. Two different artifacts share the 0.0.14 label. The orchestrator should key Composition pins by SHA, not by version. The App pin (`635f4de`) is what this rehearsal verified.
2. Earlier report's composition concern is resolved: the private graph has the pinned 0.0.14, not the shared node_modules' 0.0.13. Step 3 results are therefore for the declared composition package.
3. The shared `/home/user/work/app/node_modules` still holds Composition 0.0.13 (unchanged; not my concern, not touched).

## Failure classification

| Item | Class | Notes |
|---|---|---|
| Step 2 tree mismatch on first attempt | harness (my staging method) | `git add -A` skips gitignored `*.md`; fixed with `git add -f`; patch was correct |
| Step 4 seven strict conflicts | product / merge-forward drift | 25 upstream commits since base; touches the same files |
| 3-way "lacks the necessary blob" line | environment-benign | fell back to direct apply; all 517 paths present afterward |
| `@supabase` declaration | product policy violation (CLAUDE.md) | declared, not imported |

No step was refused. No permission denial occurred during this run.

## Commands and environment

- Worker tmpdir: `/tmp/w-2b8bf3e808/` (from `workers/tf-zip2-app/tmpdir`). Scratch: `…/scratchpad/fz2/`. Clones: `app-fresh` (applied, base+patch, private `node_modules`), `app-tip` (3-way attempt, dirty by design), `app-tip2` (clean tip, strict check).
- Patch: `fz2/app-base-to-integration.patch`; per-file chunks `fz2/chunks/`; splitter `fz2/split_patch.py`; strict checker `fz2/check_tip.py`.
- Node/npm used from PATH; npm ci exit 0.

## Recommended next steps

1. Orchestrator: decide the upstream target. The brief's deferred set (`6e3445ee9`) is an ancestor of the live tip `efe83c77e`, and the drift is 25 commits, two of them product-touching (`7f0067d01`, `2fbc6754c`). Merge-forward (App lane) must cover all 25, not just `6e3445ee9`.
2. App lane: remove `@supabase/supabase-js` from the integration (CLAUDE.md), and resolve the 4 unmerged files under 3-way (or the 7 under strict) in the integration.
3. Pin Composition by SHA (`635f4de` / `819acf6b…`), not by version label; the agent repo's two 0.0.14 archives disagree.
4. Full-tree check procedure: use `git add -f` (or `ls-tree` comparison) for tracked-but-ignored `*.md` paths, so tree equality is not falsely reported.
5. Not verified here: the full suite; the `supabase/functions/` changes; the post-merge tree of the tip (only the per-file and 3-way apply were run, not a fresh tip tree with the patch resolved).
