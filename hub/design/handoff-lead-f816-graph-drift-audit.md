# f816 clean peer graph drift audit (read-only, 2026-10-20 ~17:52Z)

Verdict: the "+77" is real, but it is NOT a symlink alias and NOT a 16:34Z event. It is one stray `tar -xzf` of the 0.0.12 Composition tarball, done at **15:54:17.68Z** by worker `vw-m3-d09-labels-native-clean-proof`, through a symlinked `@banodoco` scope. The manager only noticed it at 16:34Z. Nothing existing was changed or removed.

## 1. Graph, manifest, method
- Graph root: `/home/user/work/wt/vw-m1-ssr-snapshot/remotion/node_modules` (realpath is itself; worktree HEAD f8164bef7321...; Composition 0.0.8 files directly in `@banodoco/timeline-composition/`).
- Clean manifest: `design/handoff-vw-m3-main-cap-controller-final-gate-graph-pre.json` (21,488 entries; also byte-identical in content to the other `*-graph-pre/post.json` files from the main-cap workers and `...-main-image-cap-render-proof-candidate-graph.json`). sha256 of canonical JSON = `9e556a876a02ee4f4ed3e8215eaaf793ac0ba66a6d85e503747f635521acc425` = EXPECTED_GRAPH in `workers/vw-m3-fresh-mouth-clean-f816-requalify/run-clean-f816-qualification.py`.
- Method (`graph_state` in `design/handoff-vw-m3-mouth697-physical-controller-prep-run-central.py`): cycle-checked walk, key = relpath (+ `key@link` = readlink for symlinks), value = sha256 of content; directories are not entries. Controller refuses on entry count / digest mismatch.
- Last proven clean: central `tests/vw-m3-fresh-mouth-clean-f816-requalify-...-1020155030-5614`, finished 15:50:54Z, 21488 / 9e556a... before and after.

## 2. Recompute (my own script, same method; files under the audit scratchpad)
- manifest 21,488 / current 21,565: **missing 0, changed 0, added 77**; 0 recursive loops; 0 symlinks anywhere under `@banodoco`.
- All 77 are regular files, all under `@banodoco/timeline-composition/package/**` (a NESTED `package/` dir inside the real package dir). Plus 23 empty-of-baseline directories (package/ and subdirs) which graph_state does not count.
- Times: every one of the 100 added paths has birth/ctime 15:54:17.677-.685Z (single 8 ms burst); file mtimes are 1985-10-26 (tar preserved). `find -newermt '2026-10-20 16:00:00'` under the graph = 0 paths. Only two pre-existing dirs have new mtime/ctime: `@banodoco/timeline-composition` (15:54:17.685) and `@banodoco` (15:54:32.989).
- Content: all 77 added files are byte-identical to the **0.0.12** tarball (`banodoco-timeline-composition-0.0.12.tgz`, sha 0a7b6152...; 77/77 names and bytes). Names also equal 0.0.13's (73/77 bytes); vs 0.0.8 only 55/77. package.json inside says 0.0.12. The existing (clean) 77 files in `timeline-composition/` still equal the 0.0.8 tarball byte-for-byte (77/77). Changed count = 0; no existing file touched.
- Not related to the shared App 0.0.8 -> 0.0.13 npm ci at 16:41-16:43Z (no aliasing; those would not be 0.0.12 and would have been touched later).

## 3. Cause (evidence: workers/vw-m3-d09-labels-native-clean-proof/log.txt lines ~5120-5215, ended 15:58:45Z)
Worker built a private project by symlinking EVERY top-level entry of the f816 peer graph into `$TMP/project/node_modules/` (including the `@banodoco` scope dir), then ran `mkdir -p .../@banodoco; tar -xzf remotion/artifacts/banodoco-timeline-composition-0.0.12.tgz -C "$TMP/project/node_modules/@banodoco"; mv .../@banodoco/package .../@banodoco/timeline-composition`. Because `@banodoco` was a symlink into f816, tar wrote `package/**` into the shared graph, and `mv` (target dir already existed) moved `package` INTO `timeline-composition/` -> the nested `timeline-composition/package/` (attempt 1, 15:54:17). Attempt 2 (15:54:32) re-extracted `@banodoco/package`, mv failed ("Directory not empty"). The worker noticed, listed the scope with `-maxdepth 2 -type f` (which missed depth-3 files), and deleted only `@banodoco/package` (this is the 15:54:32 `@banodoco` mtime). The nested `timeline-composition/package/` residue from attempt 1 stayed. The worker then rebuilt with a real private `@banodoco` dir and leaf links (correct) and finished; its "shared scope after cleanup" check only tested `@banodoco/package`.
This is the same COMMON read-only violation class (tar through a linked scope) as the shared-App 18+4 incident; the realpath-before-write brief rule was added at 16:19Z, after this event.

## 4. Extent
added 77 files (+23 dirs), changed 0, missing 0. Exact list with type/mtime/ctime/sha prefix: `lead/f816-drift-paths.txt`. Graph after drift: 21,565 entries, canonical sha 1da59de09db115da... (not blessed).

## 5. Repair options (NOT performed; lead to authorize)
A (minimal, recommended): delete only the added subtree `node_modules/@banodoco/timeline-composition/package`. Pre-checks: `test ! -L` on it and every ancestor; realpath of each ancestor starts with the graph root; `find -P` listing equals `lead/f816-drift-paths.txt` (77 f + 23 d, 0 l). Then `find -P <that dir> -depth -delete` (or unlink the 77 files then rmdir deepest-first). No other path is touched; 15:54 mtimes of the two parent dirs will change (dirs are not in graph_state).
B (symlink replace): not applicable, there is no aliasing symlink. C (bless 21,565 / new baseline): not advised, it adds a duplicate 0.0.12 tree and would invalidate every pinned digest.
Prevention: private Node projects must build real scope dirs (`@banodoco`, `@remotion`) with leaf links only, extract with `--strip-components=1` into a private dir; verify with realpath before any write; post-cleanup checks should compare the full graph, not one path.

## 6. Verify back to 0/0/0
1. Re-run the cmp (scratchpad `audit-f816/cmp.py`, or the controller's `graph_state`): expect `cur 21488 added 0 missing 0 changed 0`, canonical sha = `9e556a876a02ee4f4ed3e8215eaaf793ac0ba66a6d85e503747f635521acc425`.
2. `find -P <graph> -newermt '2026-10-20 15:00:00' -type f` = none; `find <graph>/@banodoco -type l` = none; `@banodoco/timeline-composition` still has exactly README.md, dist/, package.json (0.0.8 bytes = tarball 0.0.8).
3. Run `run-clean-f816-qualification.py` six-peer + Node 43d6 preflight (read-only part) and a fresh independent fingerprint before unblocking f816-dependent qualification. Results produced on the f816 graph between 15:54:17Z and the repair carry the drift caveat (the extra files were inert: nested `package/` is not resolved by Node for `@banodoco/timeline-composition`, but they still fail the digest guard).
