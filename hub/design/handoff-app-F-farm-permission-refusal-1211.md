# farm: tf-app-full-ad96 — App full-suite run on ad96a4cac

**Status: BLOCKED. No test run was performed. No PASS/FAIL verdict.**

## Identity (verified)
- HEAD: `ad96a4cac58771baf5fbe2b07f30cccce4340040`
- HEAD^{tree}: `f7ae7964edfb4a6152e9e693fd443656aa6ab601`
- Both match the brief.

## Private dependency graph (not built)
- Archive `vendor/artifacts/banodoco-timeline-composition-635f4de06fda22a85fc2e4cfc764d0153a4c9f40.tgz`: 73451 bytes, SHA-256 `819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234`. Matches the recipe.
- Not done: the private `node_modules` with symlinks to the shared top-level packages (424 entries) and the extracted 0.0.14 `@banodoco/timeline-composition`. Creating links (`ln -s`), extracting (`tar -xzf`) and `cp -r` all required approval I could not obtain.
- Worktree `node_modules` symlink: untouched, still `/home/user/work/app/node_modules`. Shared `node_modules` untouched.

## Command
- Not run: `npm test -- --maxWorkers=3`. Exit code: n/a.
- Reason: running against the shared graph would load the stale `@banodoco/timeline-composition` 0.0.13, which is not qualification evidence. The central test service runs the worktree's own graph, so it cannot substitute for the private graph.

## Counts and failures
- Not available. Comparison against the original 89 failed / 18706 passed (20 files, run `app-full-1023100721-23537`) is therefore not possible. No failures were classified.

## Cleanup
- Empty dirs I created were removed.
- Leftover draft: `$ORCH/workers/tf-app-full-ad96/build-nm.sh`. `rm` was denied, so it needs deleting by apply_patch Delete File.

## To unblock
Approve ln/tar/cp inside a private `$ORCH/workers/tf-app-full-ad96/nm` directory (not shared), or have the orchestrator build that graph and point a run at it. Then re-run the single `npm test -- --maxWorkers=3`.
