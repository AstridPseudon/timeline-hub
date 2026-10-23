# tf-zip-app: F-zip-dry rehearsal, App (REPO=app, BASE=7c17cc9d9)

Rehearsal only. Nothing pushed, no edits to the repo, tests, pins or locks.

**Outcome: BLOCKED at step 3.** Steps 1, 2, 4 (read-only) and 5 were run. Step 3 (fresh clone checked out at BASE, then apply and tree compare) was refused by the permission system on `git checkout --detach`. I did not route around it (no `git archive`, `worktree add`, `reset`, or temp-index substitute). The tree-equality claim is therefore **unverified**; see "Step 3".

## Summary

| Step | Result |
|---|---|
| 1. Record integration, base, ancestry | PASS |
| 2. Squashed patch base..integration | PASS (517 files, 8.4 MB) |
| 3. Fresh clone at BASE, apply, tree equals integration | **BLOCKED** (checkout denied) |
| 4. Apply against live upstream tip | Conflicts: 7 files (below) |
| 5. Fast checks on integrated tree | PASS: tsc (app, node), full-repo eslint, guards, two targeted vitest sets |

## Step 1: SHAs and ancestry

| Item | Value |
|---|---|
| BASE (`origin/main` in /home/user/work/app, full) | `7c17cc9d9f9504b578862e2ffd27623fca08a04f` |
| Integration `tl/integration` | commit `411ff10bd7043d55b4d83f2dfbbbd841af7b4806`, tree `0b19a5a9e33165b5fabe7d0425ae755aa58adfa2` |
| Hub `hub/timeline/app/tl/integration` | `411ff10bd7043d55b4d83f2dfbbbd841af7b4806` (same as tl/integration) |
| BASE is ancestor of integration | yes (`git merge-base --is-ancestor`, exit 0) |
| Worker worktree HEAD | `411ff10bd`, tree `0b19a5a9e` (clean, `git status` empty) |

## Step 2: squashed patch

- Command: `git diff --binary 7c17cc9d9f9504b578862e2ffd27623fca08a04f 411ff10bd7043d55b4d83f2dfbbbd841af7b4806`
- Size: 8,434,743 bytes (about 8.0 MiB; includes one binary vendor tarball).
- Files: 517 changed, +85,947 / -3,816 lines; 15 deletions (`--diff-filter=D`).
- Test/e2e/fixture paths by heuristic (`.test.`, `.spec.`, `__tests__`, `/test(s)/`, `e2e`): 222. Remainder (about 295) product, config and docs. The split is approximate.
- Patch file (scratch, not in repo): `/tmp/w-2e9bf98228/claude-0/-home-user-work-wt-tf-zip-app/c75b6cbf-558d-4f8d-a7e2-f787359dbf83/scratchpad/app-base-to-integration.patch`

## Step 3: fresh clone at BASE (BLOCKED)

1. `git clone https://github.com/banodoco/reigh-app <scratch>/app-fresh`: succeeded. Clone HEAD is `efe83c77e1bbbb5eaae36f3a9f999f027f982e94`.
2. `git ls-remote https://github.com/banodoco/reigh-app refs/heads/main` = `efe83c77e1bbbb5eaae36f3a9f999f027f982e94`. Equals the fresh clone's origin/main. The **live tip is efe83c77e**, not 6e3445ee9.
3. `git -C <clone> checkout --detach 7c17cc9d9…`: **denied by the permission system** ("Permission to use Bash with command … has been denied"). Not retried. No substitute was used.

Consequence: no fresh base tree, so `apply` to BASE and the tree comparison with `0b19a5a9e` were not performed. The reverse check in step 5 (below) is only a proxy.

## Step 4: apply against live upstream tip (efe83c77e)

Method: per-file `git apply --check` (split of the patch, 517 chunks), read-only. Script and output are in the scratch dir (`tip-check.txt`). A whole-patch `git apply --reject` was attempted and aborted on the add/add file before writing anything; the clone's working tree is unchanged.

Result: **510 of 517 apply cleanly; 7 conflict:**

| File | Conflict |
|---|---|
| `config/testing/vitest.astrid-renderer.config.ts:26` | patch failed |
| `config/testing/vitest.boundary.config.ts:1` | patch failed |
| `config/testing/vitest.config.ts:1` | patch failed |
| `package.json:13` | patch failed |
| `tests/e2e/local/support/app.ts:105` | patch failed |
| `tests/e2e/local/support/harness.ts:45` | patch failed |
| `supabase/functions/_tests/mocks/groqSdk.ts` | add/add: already exists upstream |

Per-file results are independent; an interaction check would need the step 3 tree.

Upstream drift:
- Base to live tip: **27 commits** (`git log 7c17cc9d9..efe83c77e`). BASE is an ancestor of the tip.
- The deferred `6e3445ee9` is an ancestor of the tip, so it is included in the drift. The tip also carries 26 more commits. The board's record (12:46Z, "App upstream 6e3445ee9") is stale. The deferred set is larger than the brief states; the orchestrator should decide whether the tip is the one to defer.
- Commit subjects are mostly e2e, CI and test work, but include product-touching items: `7f0067d01` "drop the dead pictureTracks seam code", `2fbc6754c` "refuse cross-project gallery adds". Not reviewed in depth.

## Step 5: fast checks on the integrated tree

Run in my worktree, which is at `411ff10bd` (tree `0b19a5a9e`), i.e. the integration tree itself, not a fresh-applied tree. Dependencies are the shared, read-only `/home/user/work/app/node_modules` (symlink). Caches were kept out of shared paths (vitest with `--cache=false`; no eslint `--cache`).

| Check | Command | Result |
|---|---|---|
| Patch reverse-check on integration tree | `git apply --reverse --check --binary <patch>` | exit 0 (proxy only; see step 3) |
| Typecheck, app | `node node_modules/typescript/bin/tsc -p tsconfig.app.json --noEmit` | exit 0 |
| Typecheck, node | `node node_modules/typescript/bin/tsc -p tsconfig.node.json --noEmit` | exit 0 |
| Lint, full repo (repo's `lint` script args) | `node node_modules/eslint/bin/eslint.js . --ext ts,tsx --report-unused-disable-directives --max-warnings 0` | exit 0 |
| Guard | `node scripts/quality/check-no-smoke-tests.mjs` | exit 0 |
| Guard | `node scripts/quality/check-known-failures.mjs` | exit 0 |
| Smoke set 1 (3 files) | `node node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --cache=false src/sdk/index.test.ts src/sdk/manifest-schema-validation.test.ts src/shared/hooks/__tests__/usePromoteVariantToGeneration.test.ts` | 3 files, **444 tests passed** |
| Smoke set 2 (10 files) | same command, files: `src/integrations/runtime/{timelineCommit,dataProvider,resolveProjectSelector,vendorLock}.test.ts`, `src/sdk/examples-governance.test.ts`, `src/shared/lib/placement/__tests__/placementService.test.ts`, `src/shared/lib/media/mediaCrossOrigin.test.ts`, `src/shared/state/selectionClipData.test.ts`, `src/shared/hooks/shots/__tests__/useShotGenerationMutations.test.ts`, `src/integrations/paired/pairedRoutePolicy.test.ts` | 10 files, **2793 tests passed** |

Not run: `typecheck:strict-islands`, `lint:edge`, `test:edge*`, `check:contracts`, Playwright, the full suite (not requested by the brief), and any npm install.

Sandbox friction: direct `node_modules/.bin/tsc` and `.bin` invocations, and some piped or `$?` commands, were held for approval. Running the package entrypoints with `node` worked.

## Findings for the orchestrator (not fixed; dry run)

1. **Dependency declared against policy.** Integration `package.json` adds `"@supabase/supabase-js": "^2.49.4"` (dependencies, not in base). CLAUDE.md says do not add `@supabase/*`. No `@supabase` import under `src/` was found by `git grep`; supabase code remains under `supabase/functions/` (which the integration also modifies; not inspected in depth).
2. **Composition package switched to a tarball.** `@banodoco/timeline-composition` changes from `file:vendor/timeline-composition` to `file:vendor/artifacts/banodoco-timeline-composition-635f4de06fda22a85fc2e4cfc764d0153a4c9f40.tgz`. The tarball and its `.sha256` are in the integration tree. **Not verified** (reading the tarball needed approval). The shared `node_modules` has `@banodoco/timeline-composition` at **0.0.13**, so step 5 ran against a composition package that may not be the one this tree declares. Treat step 5 as a weak signal for composition-dependent tests.
3. `package.json` also adds `react-joyride ^2.9.3`; present in the shared node_modules.
4. The 7 tip conflicts are concentrated in vitest configs, `package.json` scripts, and e2e support. They are merge-forward work for the App lane, and the 27-commit drift is the reason.

## Recommended next steps

- Lead / orchestrator: approve or decline a `git checkout` (or equivalent materialization) in a scratch clone so step 3 can run; that is the only missing evidence for "fresh tree equals integration tree".
- Verify the composition tarball sha and version, and re-run step 5 with the declared composition package in a private overlay (not the shared node_modules).
- Decide whether the deferred upstream set is `6e3445ee9` or the live tip `efe83c77e`.
- Ask the App lane to explain the `@supabase/supabase-js` dependency against CLAUDE.md.
