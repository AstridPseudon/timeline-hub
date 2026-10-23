OPS-bench-store run leases — staged handback, 2026-10-23

Staged the production bin/test-run caller against core1858's names_for_suite/acquire API. Runtime product and integration remain clean. Nothing was installed, queued, retired or deleted on the live service. This is evidence-only; never merge.

Files use prefix /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-runtime-OPS-bench-store-leases-1850-
- test-run: complete staged production shell.
- test-run.original: exact installed predecessor, SHA256 2d1240303c0c82bf908377eeff3323a899d8929454ac2c316b05bf076fc35d35.
- test-run.patch: exact unified patch against that predecessor; bin/test-run only.
- lease-seam.py: exact embedded Python export for compilation and executable fixtures; no separate production installation.
- test-leases.py: private executable concurrency/security fixtures.
- hashmanifest.sha256: source/dependency/report/log hashes.
- report.md: this handback. Worker tests.log and validation.log contain full command results.
Core dependency: handoff-runtime-OPS-bench-store-core-resume-1854-bench_store.py, SHA256 53d90fb3108b24253a29416214ec5fa8f69402f50a515f0399b7464ec39a2e14. Identical core-precondition-1858 source was available. The final fixture verifies that the core hash stays stable across the run.

Behavior and decisions:
- Cache hits/fullqueue/slot/disk/snapshot-key guards retain original bytes. Cache hits return before any lease. request-test, stop-test, suites.conf and env files need no patch.
- An initialized /home/user/work/bench-store activates leasing before snapshot/worktree/link setup. Absent store preserves the legacy route; existing symlink/corrupt store refuses. Exact registration metadata identifies all dependencies, including child+Remotion. No env sourcing or command-string guesses identify benches.
- Existing awk-normalized CMD and appended --files remain unchanged. Adapter binds the command to the original exact allow-listed row. Core.acquire atomically revalidates immutable metadata and holds all shared locks under the core mutex; eviction between lookup and acquire refuses. Removed rows cannot become unmanaged fallthrough.
- Linux subreaping holds leases until run descendants exit. Actual shell/timeout/suite inherit the lease FDs. Control pipe reports the suite timeout group and closes its write FD before suite execution; supervision waits for processes rather than pipe EOF. There is no /proc scan.
- Existing stop-test still addresses the original runner PID. Cancellation/TERM/runner parent death forwards TERM then KILL after five seconds to the supervised runner and reported suite groups. Original GNU timeout stays 90m with 60s kill grace; supervisor also bounds descendant waiting from suite start.
- Normal/failure/timeout status is preserved, including suite exit 125. A tiny completion/error handoff distinguishes infrastructure failure from suite status. Missing completion refuses caching and retains a possible snapshot. Locks release after descendants finish, before parent Git snapshot cleanup, which does not use managed benches.
- Unregistered rows acquire no bench FDs and retain direct-child execution semantics. Existing legacy benches receive no adoption/deletion authority. Real test IDs, cache key, suite body, receipt/source qualification, product and frozen C0v2 wire shapes remain untouched.

Exact validation, all exit 0:
~~~
ORCH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch
P=$ORCH/design/handoff-runtime-OPS-bench-store-leases-1850-
python3 -I "$P"test-leases.py
# 21 tests PASS in 7.654s; stable core hash above.
bash -n "$P"test-run
PYTHONPYCACHEPREFIX=$TMPDIR/pycache python3 -m py_compile "$P"lease-seam.py "$P"test-leases.py
# Private target copied from test-run.original, inside TMPDIR:
patch --dry-run -p1 -d $TMPDIR/lease-patch-b4llncv6 < "$P"test-run.patch
patch -p1 -d $TMPDIR/lease-patch-b4llncv6 < "$P"test-run.patch
cmp $TMPDIR/lease-patch-b4llncv6/bin/test-run "$P"test-run
git -C /home/user/work/runtime status --porcelain
# empty
git -C /home/user/work/runtime diff --check
git diff --check
~~~
Embedded/exported Python byte comparison passed. Installed test-run still equals the predecessor.

The 21 fixtures invoke the exact extracted production Python entry/seam and exact shell suite branch with fake snapshot boundaries, tiny core-managed directories, separate processes and real flock -n probes. Coverage: normal/orphan-child lifetime, failure, timeout, cancellation including actual timeout group, TERM, runner parent death, supervisor SIGKILL with inherited command FDs, two components, simultaneous acquire/evict, resolved-then-evicted refusal, tampered registration, forged name, symlink root refusal, row whitespace binding, suite 125 vs infrastructure refusal, unmanaged rows, cache hit and unchanged original guard bytes. No real Git, body, sockets, queue, service or bench was used by fixtures.

Limitations and next steps:
- Independent Luna review remains required before installation. No live service/browser/product/full suite or 90-minute wall-clock timeout was run. Short fixture timeouts exercise lifecycle behavior around the exact production seam.
- Cancellation targets the two known groups. Descendants deliberately creating unrelated sessions are still subreaped/waited, but forced termination of escaped groups is unverified and can extend waiting. Review this before claiming arbitrary detached-process cancellation. Simultaneous SIGKILL of all holders with an escaped descendant that intentionally closed inherited FDs is not qualified.
- Missing supervisor completion retains possible active snapshot source for operator review.
- Earlier fixture imports created one small core bytecache in design/__pycache__; left untouched under the no-cache-cleanup rule. Final fixture imports disable bytecache writes. Other fixtures, patch targets and compile caches are in TMPDIR.
- No remaining API blocker. Next: independent adapter/core/creator review, then lead-owned atomic installation and smoke when runs are released. Existing retired requests remain stopped.

