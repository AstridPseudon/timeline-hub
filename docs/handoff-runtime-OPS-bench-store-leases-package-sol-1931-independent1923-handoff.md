# OPS-bench-store leases review 1923 — FAIL

Independent Luna source/private review of lease1918 on Runtime `2a9e347ff0e1df1dedff5ab7b59ddb27dfe3129d`.

The exact embedded production seam uses the changed core `88ae9e5af3425639b7eba0b79aa6b84e78a319fe810c0c6a2d3ceece1be8b5f3`; it loads the production `bench_store.py`, resolves genuine custom rows through `names_for_suite`, acquires managed leases, passes inherited FDs through the command lifetime, supervises descendants, and rechecks the suite row before command start. Legacy no-managed rows retain `([], [])` behavior.

Independent run: `python3 -I .../handoff-runtime-OPS-bench-store-leases-return-1918-test-leases.py` with private TMPDIR — **24/24 PASS, 8.631s**. This is prior 21 scenarios plus custom absolute managed-path lifetime, conservative managed-row coverage, and row removal/tamper refusal (two subcases), with real processes/flock, descendants, cancellation/timeouts/stop, reuse/generated rows, refusal/exit handling, and cache/snapshot/zero-test guards. The old race diagnostic remains RED before the two-line caller recheck (exit 1, two failing subcases, 0.064s).

Scoped source checks pass: validator, shell syntax, embedded Python compile, patch replay/cmp, predecessor cmp, core1915 manifest, lease1850/immutable/live manifests, clean Runtime status/diff. C0v2 request/reply sections and frozen34e (`34eac0041b0891e9011966b39bcbd26053fde5bc`, tree `9853574865f25e08284e82ffb26c0bdecaa16a30`) were read/verified unchanged.

FAIL findings:

- Final lease1918 hash manifest is not fully green: 15/16 entries pass; worker `report.md` is recorded as `a90a816b56c51e568129b77491888776ba3267a0aaa6fb4b79d583cdfd209286` but currently hashes `d66d207226ea20a4d8414a5b8702af98d33b7c337533dfa45f1069fc0192d143`. The canonical flat report itself is `a90a…9286`.
- Core1915’s separate original matrix remains 17/18 due the inode-nonreuse assertion, also red on frozen1858.
- Permission1905 readonly/combined lifecycle remains pending; no forbidden live or installation action was attempted. Overall combined store child remains FAIL/UNQUALIFIED.

TMPDIR was 292700 bytes (<15 MiB); durable evidence remains <3 MiB. No product/source/test fix was made. Reconcile the report hash, resolve the core RED and permission disposition, then perform authorized combined proof before installation.
