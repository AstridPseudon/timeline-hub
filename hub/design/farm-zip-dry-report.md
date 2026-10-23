# F-zip-dry report: final-ZIP rehearsal, 2026-10-23T14:50Z. Verdict: PARTIAL (no repo was fully rehearsed; nothing pushed)
Per-repo detail: design/farm-zip-dry-{agent,app,runtime,composition}.md. Escalation: escalations/farm-20261023T1442-zip-dry-permission-denials.md.

| Repo | Integration (tree) | Base | Patch | Fresh apply at base | Live upstream tip | Fast checks |
|---|---|---|---|---|---|---|
| agent | 8c355a48e (c4d72b065d6e) | 431681a6d | 8,548,648 B, 820 files (514 test-like, 306 product-like) | NOT RUN (checkout denied) | 74f3f7edb is an ancestor of integration, so no drift | not run |
| app | 411ff10bd (0b19a5a9e) | 7c17cc9d9 | ~8.4 MB, 517 files (+85,947 / -3,816, 15 deletions) | NOT RUN (checkout denied) | efe83c77e, 27 commits past base. Per-file check: 510 of 517 apply, 7 conflicts (4 vitest/package.json/e2e files, groqSdk.ts add/add, tests/e2e/local/support/{app,harness}.ts) | PASS on the integration tree: tsc app and node, eslint, no-smoke-tests, known-failures, vitest subsets 444 + 2793 (stale shared composition 0.0.13: weak signal) |
| runtime | cfa0af0d4 (3675f446c) | a98fbc2f9 | 4,632,068 B, 245 files (173 tests, 72 product) | NOT RUN (checkout denied) | f23d1e43f (3 commits past base, one changes product code in runtime_protocol/visual_seam.py); 5 overlapping files, likely conflicts | not run (no lint/typecheck config; ruff denied) |
| composition | 635f4de06fda (5ab5191a2969) | 67b8aa3d0 | 493,374 B, 118 paths | PASS: applies cleanly, tree equals integration | main is still 67b8aa3d0: no drift | only node --check on three .mjs; npm ci denied |

Findings to act on:
1. The upstream drift is larger than the header says. App live tip efe83c77e is 27 commits past base (it includes the deferred 6e3445ee9 plus 26 others, e.g. 7f0067d01 and 2fbc6754c); Runtime live tip is f23d1e43f, not 6162e0e33.
2. App integration declares @supabase/supabase-js in package.json (CLAUDE.md forbids @supabase/*). No src/ import was found, so it may be unused. Owner: App.
3. The App composition pin uses the vendored tarball 635f4de…tgz while the shared node_modules has 0.0.13, so App checks here are weak signals for composition-dependent tests.

Draft ZIP layout (not built; layout only):
```
final.zip
  README.md          base SHAs (agent 431681a6d, app 7c17cc9d9, runtime a98fbc2f9, composition 67b8aa3d0), integration SHAs/trees above, per-repo apply and verify commands
  agent.patch        git diff --binary 431681a6d..<agent integration>
  app.patch          git diff --binary 7c17cc9d9..<app integration>
  runtime.patch      git diff --binary a98fbc2f9..<runtime integration>
  composition.patch  git diff --binary 67b8aa3d0..<composition integration>
  per-repo apply:    git checkout --detach <base>; git apply --check <repo>.patch; git apply <repo>.patch; verify `git write-tree` equals the stated tree
```
Not verified: tree equality for agent, app and runtime (the checkout in a fresh clone was denied). Recommended next step: the orchestrator permits `git checkout --detach` in a worker scratch clone (and Composition `npm ci`), then the farm re-runs steps 3 to 5; or accept this rehearsal as partial and do the full apply at F-final.
