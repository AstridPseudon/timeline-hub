# Runtime U1b independent review — FAIL

Reviewed `62926bd1d56bda30b6f36a0bb6b1d9435f7214e` (tree
`9804dbcc34600143aae6cc05881d1025faf1ad8d`), parents integration
`1365e4b17b31c4a7093d5943674637067fd2bab4` and upstream
`a98fbc2f9544a8be14281e32afde8aafa098f5f7`.

Ancestry and live remote checks PASS: `git merge-base --is-ancestor origin/main
HEAD` status 0, and `git ls-remote origin refs/heads/main` exactly returned
`a98fbc2f9544a8be14281e32afde8aafa098f5f7`. The authorized upstream range is
the upstream merge plus six expected commits; no unrelated worker ancestry was
found. Contract/schema/generated/package/generator surfaces are unchanged from
integration; schema v32 and D17/current-source authority are preserved.

Exact tests PASS: lane 1 `264 passed, 13 skipped` (all 13 visibly declared
Windows capability skips), lane 2 `186 passed`, generator/manifest/client
parity `23 passed`. Ruff, compile, diff-check, marker scan, and exact-parent
Pyright comparison PASS (41 identical pre-existing platform diagnostics, zero
added).

Blocking finding: `DECLARED_XFAILS` is keyed by reason name and `(reason, ci)`
only (`tests/lanes.py:102-120`), with no exact node registry. `_SkipGuard` and
the AST policy accept any test reusing a registered reason. A direct probe shows
`is_declared_xfail(declared_xfail_reason("runtime-domains-publication"))` is
true without a node. Thus new/moved/changed xfails can be hidden by a known
reason, contrary to the required exact node/reason fail-closed controls.

**Disposition: FAIL; do not merge.** No product/test repair was made. Full,
browser/HTTP/native/crash/Agent-heavy suites were not run per the task.
