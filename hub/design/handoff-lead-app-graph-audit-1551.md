# Shared App graph audit 15:51Z (READ-ONLY; nothing repaired)

Target: /home/user/work/app/node_modules. Full path list: $ORCH/lead/app-graph-1551-changes.txt

## Summary
- Extent: **MODIFIED BYTES (not additive-only).** Only `@banodoco/timeline-composition` is affected (+ a benign mtime on empty `.vite-temp`). Every other package/path in the graph has ctime < 15:00Z; the 6 audited self/overlay symlinks (07:57:23Z) are intact.
- `@banodoco/timeline-composition/package.json` version is now **0.0.12** (was 0.0.8). The tree = exact contents of banodoco-timeline-composition-0.0.12.tgz (sha256 0a7b6152...f1a3; all 77 files match it byte for byte) **plus** 4 leftover 0.0.8-only chunk files.
- GlobalQUIET hashes (recomputed): all four MISMATCH.
  | file | GlobalQUIET (0.0.8) | installed now (= 0.0.12) |
  |---|---|---|
  | dist/index.js | 2111490c...6078 | 364460a558df5b0b9c6633113943f3414fd1c1873cb1357d01ecf7d279a41e52 |
  | dist/index.d.ts | afd74b9c...e794 | da76faee7226e65a18f91a2fb45e2a260f33aef8768609093872c7eff1a76e03 |
  | dist/evaluation.js | 0ee058ca...8b96 | 5bfa7ac353d7e584c8cb7d3082cb6b49c209a1ec679bc31c25c4b6d8dc7a9390 |
  | dist/registries.js | 50acbe4e...1cb4 | dd8b245ba3a2204af3cef9ae6858148a146997d84315c0ce8def3e7133f9019c |
  The 0.0.8 tarball (sha256 93bc66b5...6caa, sha512-dzRWuIge... == lock integrity) still yields the GlobalQUIET hashes. `.package-lock.json` is untouched and still claims 0.0.8 (so the install is now inconsistent with its lock).

## Classification (relative to the 0.0.8 package; 77 files rewritten at ctime 15:47:02.12-.13Z)
- MODIFIED_FILE (bytes differ from 0.0.8): 18 — README.md, package.json, dist/{index.js, index.d.ts, evaluation.js, evaluation.d.ts, registries.js, registry.generated.js, theme-api.js, types.d.ts, TimelineComposition.d.ts, effects-types.d.ts, scene-capabilities.d.ts, scene-evaluation.d.ts, lib/clip-look.d.ts, lib/transition-declarations.d.ts, lib/transition-spans.d.ts, lib/transitions.d.ts}
- ADDED_FILE (absent from 0.0.8): 4 — dist/chunk-DMRW7SC3.js, chunk-GWYPEUCA.js, chunk-KA66CXRB.js, chunk-LG3Y3LFP.js
- REWRITTEN_SAME_BYTES (new inode/ctime, bytes == 0.0.8): 55
- LEFTOVER 0.0.8 files not in 0.0.12 (untouched, original bytes and ctime): dist/chunk-3ZOH3R7U.js, chunk-H6GRHVIL.js, chunk-QHXOB7ZR.js, chunk-XIJFC4F7.js (hash-equal to 0.0.8 copies; now orphaned/unreferenced by 0.0.12 entrypoints)
- REMOVED files: none. ADDED dirs: none (dir set == 0.0.8 set). ADDED symlinks: none. 16 existing dirs got mtime/ctime 15:47:02Z (file replace). `.vite-temp` (empty, born 00:09Z) mtime 15:47:27.56Z: a vite/vitest config-load temp touch, not attributable to a specific command, no content.
- Why mtimes of files look old: tar preserved tarball mtimes (1985-10-26 08:15). Only ctime (and dir mtimes) reveal the rewrite; `find -newermt` on files misses it, use `-newerct`.

## Culprit commands (worker vw-m3-app-cap3a-current-owner-gate, log.txt, started 15:45:08Z, STOPPED 15:47:27Z)
Single `exec` block, log lines 8862-8873 (cwd /home/user/work/wt/vw-m3-app-cap3a-current-owner-gate):
- 8866 `ROOT=.../workers/vw-m3-app-cap3a-current-owner-gate`; 8867 `mkdir -p "$SRC" "$DEPS/node_modules"` (private; harmless)
- 8868 `git archive 3a4350f9d | tar -xf - -C "$SRC"` (private; harmless)
- **8869 `for path in /home/user/work/app/node_modules/*; do name=${path##*/}; ln -s "$path" "$DEPS/node_modules/$name"; done`** — made `deps12/node_modules/@banodoco -> /home/user/work/app/node_modules/@banodoco` (whole scope; same for every @scope dir). Glob skips dotfiles (.bin, .package-lock.json not linked). Links themselves are in the private deps12, not in the shared graph.
- 8870 `mkdir -p "$DEPS/node_modules/@banodoco/timeline-composition"` — resolves through the link to the existing shared dir: no-op.
- **8871 `tar -xzf "$SRC/vendor/artifacts/banodoco-timeline-composition-0.0.12.tgz" -C "$DEPS/node_modules/@banodoco/timeline-composition" --strip-components=1`** — THE WRITE: overwrote the shared package (unlink+create per file).
- 8872 `ln -s "$DEPS/node_modules" "$SRC/node_modules"` (private).
Earlier in that worker: 8563-8565 `mkdir -p "$OV"; git archive | tar -xf - -C "$OV"; ln -s /tmp/app-coherent-deps12/node_modules "$OV/node_modules"` — private only (dangling target). Line 8743 (`find ... /home/user/work/app/node_modules -mindepth 1 -maxdepth 1 | wc -l`, "427") and 8878/8899 (`node /home/user/work/app/node_modules/vitest/vitest.mjs run ...`) are reads/executions; they ran AFTER the overwrite against the corrupted graph (their results were consumed with 0.0.12 under the shared path). No npm pack/cp/rm in the shared graph.
Still-live aliases: `workers/vw-m3-app-cap3a-current-owner-gate/deps12/node_modules/*` and `exact3a-private/node_modules` still point into the shared graph; do not rm -r through them.

## Would a link-only / additive-only removal restore the 23:59Z state?
**No.** 18 files were overwritten in place and 4 files were added; deleting added items cannot recover the old bytes of the 18 (or package.json version). Restoration needs a content rewrite of the one package dir from the pinned 0.0.8 tarball, while keeping the `package` symlink:
1. (not run) `tar -xzf artifacts/banodoco-timeline-composition-0.0.8.tgz -C .../@banodoco/timeline-composition --strip-components=1` (restores all 77 files incl. 18 modified), then
2. remove exactly the 4 added chunk files (DMRW7SC3, GWYPEUCA, KA66CXRB, LG3Y3LFP); leave the `package` link and the 4 leftover 0.0.8 chunks (they are legitimate 0.0.8 files). Optionally `touch -d` dir mtimes; original ctimes cannot be restored (ctime will read as repair time).
Verification: (a) file set == 77 files of the 0.0.8 tgz + the `package` link; (b) per-file sha256 == tgz extraction (reference sums: $ORCH/lead/app-graph-0.0.8-reference.sha256, 77 lines); (c) the four GlobalQUIET hashes and package.json version 0.0.8; (d) tgz sha512 == `.package-lock.json` integrity (already true); (e) rerun the audited tab-audio-capture.controller.mjs packageGraphFingerprint/hashTree (pinned node 20.19.4, which is not currently present at /tmp/vw-m3-agent-gate-node20.19.4) and expect the six approved package hashes and old graph hash 215e32c6fc86ba57ad36f766a273e43b8c9d328341308fafcda752b03e9eb858 with the same six link exclusions; (f) `find -P node_modules -newerct <repair time>` shows only that package dir. Lead decides who repairs; any consumer evidence produced against the shared graph since 15:47:02Z (including the worker's 15:47 vitest runs) was run on 0.0.12 bytes, not 0.0.8.
Other considered alternative: leaving 0.0.12 in place is not consistent with the lock, GlobalQUIET, or the six-link-excluded graph hash.
