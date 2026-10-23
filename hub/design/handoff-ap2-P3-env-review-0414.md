# P3 environment review handoff

## Verdict

**FAIL for current operational approval; Gate 5 remains execution-blocked.**

The durable graph at
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-P3-env-final-0407/record/private/node_modules`
passes the exact locked Composition archive check: SHA-256
`819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234`,
73,451 bytes, 80 regular files, byte-identical extraction. The final worker's
tmpdir `/tmp/w-a16893f843` is gone, while the durable graph remains and has no
dangling or deleted-tmpdir references. No package-root generated-module,
`typescript`, source, or fallback links are present. Normal Node exports all
resolve to the archive's `dist/*` paths.

The current suite row hash is
`8757a47e1476be8d75cb0baa73a8014fced17b082891375edeb3063a71ab3282`. It has
the durable snapshot-owned `node_modules` replacement, supported Python paths,
full Agent/Runtime pins, and the exact original Gate-5 selector exactly once.
However, it pins Agent `f894c3c9dda25ab03527eeb7f52da5da31d627c1` while
`/home/user/work/agent` currently points to clean descendant
`ccc521b7811231984564f07ea50e9eb710466b1a`; Runtime still matches exact
`34eac0041b0891e9011966b39bcbd26053fde5bc`. This stale exact-source pin is an
operational blocker, even though the graph/archive itself is ready.

The separate existing App-owned Vite alias defect remains explicitly
**execution BLOCKED**: the exact graph's public generated Composition imports
are intercepted as package-root paths and return `noResolved`, whereas the
archive exports them from `dist/*.js`. Do not use package shims/fallbacks or
call prep/selector collection a journey PASS. Prior `19140` and `29980` setup
failures have no acceptance credit; no browser/body/service/full run was
performed here.

Next action: supply an owned clean Agent checkout at exact `f894`, or obtain an
approved reviewed source-pin update, then have App resolve the public exports
without changing the archive. Only after both blockers are resolved should the
single central same-case Gate-5 run be requested.

