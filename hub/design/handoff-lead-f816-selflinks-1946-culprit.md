# f816 self-links 19:46:49.6Z - culprit (forensic, read-only)

Verdict (high confidence): worker `vw-m3-d10-full-root-package-build` (agent, started 19:45:00Z, ended 19:48:59Z), one `exec` in its own log.

- Evidence file: `workers/vw-m3-d10-full-root-package-build/log.txt`, lines 7186-7232 (the executed script; line 7185 is the byte-identical copy that was Rejected by the sandbox at 19:46:41.497Z and not run). Retry ran right after, "exited 1 in 3046ms" (the exit 1 came from the final `remotion --version` help output, after the damage). Stage files it generated are stamped 19:47.
- Code (log.txt:7195-7213):
  `OLD=/home/user/work/wt/vw-m1-ssr-snapshot/remotion/node_modules`
  `for entry in "$OLD"/* "$OLD"/@*; do`            (line 7198)
  `  ... mkdir -p "$STAGE/remotion/node_modules/$base"`   (scope dir, real)
  `  for scoped in "$entry"/*; do ... ln -s "$(realpath "$scoped")" "$STAGE/remotion/node_modules/$base/$name"` (line 7210)
- Why it wrote through to f816: the glob list `"$OLD"/* "$OLD"/@*` visits every scope dir TWICE (`*` already matches `@*`). Pass 1 creates `$STAGE/.../@babel/code-frame -> f816/@babel/code-frame` (a symlink to a directory). Pass 2 runs the same `ln -s SRC $STAGE/.../@babel/code-frame` (no `-n`/`-T`); the destination exists and is a symlink to a dir, so GNU ln dereferences it and creates the link INSIDE it: `f816/@babel/code-frame/code-frame -> f816/@babel/code-frame`. The private scope dir was real (so the "real scope dirs + leaf links" rule was followed); the leaf links were the aliases.
- Fingerprint match: 106 = exact count of scoped packages in f816 excluding the skipped `@banodoco` (checked: 14 scopes, 106 leaf dirs; lead/f816-selflinks-candidates.txt has 106 lines, 0 under @banodoco). Link target = the f816 path itself (earlier incidents' targets were the peer path, same mechanism). Unscoped entries are not duplicated, so no other damage. Mini repro of the double-glob in scratchpad reproduced `old/@s/p/p -> old/@s/p`.
- Ruled out: accounted973-qualification (no f816 loop; only reads other logs mentioning it), complete-project-source-closure (its 19:46:48.676 command was Rejected; the probe that ran copied /tmp/vw-m3-public13-host-one-root-catalog-stage with node `cp` into a mktemp root and asserted the realpath was private), scene-private-dispatch-live-qualified (its builder copies PEERS with copytree symlinks=False, ended 19:47:32 with no f816 use), test-service runs (24719 / 31992 / 9628) never reference f816. No other worker was active in the window.
- Not verified directly: the links were removed by lead at 20:50:18Z (lead/node-modules-repair.log) so mtime/ordering could not be re-read from disk; the d10 stage dir was deleted by the worker so its stat times are gone. Attribution rests on log text + count + mechanism.

One-line prevention: build private scope links with a single pass over scopes (`"$OLD"/@*` only, non-scoped via `"$OLD"/[!@]*`) and always use `ln -sfn`/`ln -sT` into a verified-empty real dir (plus `realpath` check that dest parent is not under the shared graph) - or make the shared graph read-only (`chmod -R a-w` / bind-mount ro).
