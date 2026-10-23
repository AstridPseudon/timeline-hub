OPS-bench-store lease return1918 — private lease qualification PASS; installation UNQUALIFIED

Completed 2026-10-23. Evidence-only, never merge. Runtime worker/integration both remain clean at 2a9e347ff0e1df1dedff5ab7b59ddb27dfe3129d; no product, tests, schema, generated, pin, config, queue, Git, installation, provision, or network changes. Full C0v2 request/reply shapes and frozen34e are unchanged.

Dependency and final binding:
- Sole core author: core-projection1915; no core was patched or reimplemented here.
- Final published bench_store.py SHA256: 88ae9e5af3425639b7eba0b79aa6b84e78a319fe810c0c6a2d3ceece1be8b5f3. This differs from failed lease1910 dependency 53d90fb3108b24253a29416214ec5fa8f69402f50a515f0399b7464ec39a2e14.
- Tests bind exact core, staged caller, embedded seam, predecessor, patch and fixture hashes before AND after execution; all equal. See tests.log and hashmanifest.sha256 for full hashes/paths.

Changes and decisions:
- Exported all artifacts under NEW handoff-runtime-OPS-bench-store-leases-return-1918-* prefix. Every lease1850/precondition1858 artifact and live test-run/stop-test/request-stop-test/suites.conf checksum remains unchanged.
- Core1915 owns conservative registered-dependency leasing for genuine custom rows. No command parsing, inferred path authority, alternative core, or adoption of unknown legacy benches was added.
- Prepared the faithful independent1910 regression: two runtime entries have BENCH_PATH={bench_path} env and empty managed suite; a separate existing custom row uses the first entry's absolute generated path. The exact exported production entry runs test -d <path> && echo ready > <marker> && sleep 1. A separate flock -n -x probe refuses while alive, third ensure retains that first path while the command is demonstrably alive, command exits 0 with completion handoff, flock succeeds afterward, and fourth ensure reclaims the released old path.
- Concrete caller bug found on FINAL core1915: lookup now returns nonempty conservative names, bypassing the old caller's empty-name-only row recheck. A mutation injected immediately after real lookup removed the custom row or changed its command; both reached the command boundary. The hash-bound pre-fix test exited 1 with TWO failing subcases (caller-race-core1915-before.log).
- Authorized narrow caller fix: TWO added lines inside acquired lease recheck the raw row before yielding. caller-only.patch is the entire delta from staged lease1850 test-run. All other staged shell bytes stay identical, including snapshot/cache/timeout/zero-test/exit-mismatch/stop guards. Full patch remains against the exact installed predecessor. No API change was needed.
- Retained the old empty-store/no-lease behavior, explicitly named test_legacy_without_managed_entries_has_no_lease; added stronger conservative-managed coverage. All prior 21 scenarios remain, plus the faithful race, conservative control, and removal/tamper race (24 tests total).
- Strengthened four existing refusal assertions: removed self.fail inside assertRaises(Exception), which could incorrectly swallow its own AssertionError. Expected refusal behavior is unchanged and now actually tested. No test skipped, disabled, marked expected-fail, or weakened.

Exact commands/results (executed from assigned Runtime worktree):
~~~bash
ORCH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch
P=$ORCH/design/handoff-runtime-OPS-bench-store-leases-return-1918-
python3 -I "${P}test-leases.py" LeaseTests.test_row_removed_or_tampered_between_resolution_and_acquire_refuses
# BEFORE fix: exit 1, 1 test / 2 failing subcases, 0.064s; exact core hash above.
python3 -I "${P}test-leases.py"
# AFTER fix / final packet: exit 0; Ran 24 tests in 8.643s; OK. Bound hashes stable.
python3 -I "${P}validate.py"
# exit 0; exact commands and outputs in worker validation.log:
# bash -n staged test-run; compile embedded/exported Python + fixture + validator;
# exact embedded/exported byte equality; patch --dry-run -p1, patch -p1, cmp;
# installed predecessor cmp; old/live manifest verification; shell outside seam identical;
# git status --porcelain empty, git diff --check exit 0, rev-parse HEAD unchanged
# for assigned worktree AND /home/user/work/runtime.
sha256sum -c "${P}hashmanifest.sha256"
# Final exported/dependency/log/report manifest verification: exit 0.
~~~
A preliminary one-case empty-name diagnostic against immutable core1854 passed before final source publication; it is NOT final qualification. All final evidence above uses core1915. Source validation additionally verifies the original lease1850 full hashmanifest, not merely copied files.

Artifact inventory: complete test-run, installed test-run.original, test-run.patch, exact embedded lease-seam.py, caller-only.patch, executable test-leases.py, executable source-only validate.py, interface-needs.md, this report, hashmanifest.sha256. Logs and before/live input manifests are in the assigned worker folder.

Limits and next steps:
- This qualifies the tiny writable lease fixtures only. All scratch is in harness TMPDIR /tmp/w-05c5d81085, 2.4 MiB at final fixture completion (<20 MiB); payloads contain only fixture bytes. The two-component scenario creates synthetic writable core entries, never an actual child/combined creator or readonly publication.
- No combined creator, HOST, central test-service, live sockets, chmod, denied-path retry, actual child readonly publication/deletion, install, cleanup, product test suite, or full suite was run. Permission escalation1905 remains pending. Overall child/store installation stays UNQUALIFIED.
- Actual 90-minute wall-clock timeout was not run; short timeout/cancel cases use the exact embedded production seam and actual shell timeout branch. Supervisor waits for orphan descendants and inherited lease FDs survive supervisor SIGKILL. Forced cancellation of descendants escaping the known process groups remains unverified, as in lease1850; it can extend waiting. No arbitrary-detached-process termination guarantee is claimed.
- This worker did not requalify report projection, provision receipts, readonly lifecycle or the core's separate full fixture matrix. Preserve core1915's own reported limitations.
- Next: independent Luna review of this exact hash-bound lease packet with core1915. Resolve permission1905 and remaining creator/core review gates before orchestrator-authorized installation. No merge is recommended for this evidence-only packet.
