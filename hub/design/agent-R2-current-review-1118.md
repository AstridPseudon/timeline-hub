# R2 current-port independent review — PASS

## Scope

Reviewed `tl/agt-R2-current-review-1118` at `7d58e0682253b7c2e204652ee14a48a39c7105ff`.
The parent is actual Agent integration `abfa78a657b4ce1cc625104e8472fb29938e3d64`.
The only product-tree change is the new test file
`tests/editing_conformance/test_inverse_stage_runtime_regressions.py`.

Compared with `db3c11ca6`, the test diff is exactly three replacements:
`AGENT_COMMIT` and the two Agent source hashes. No assertions, cases, setup,
or Runtime pins changed. Compared with the actual integration head, the
worker commit is exactly that one added test file.

The seven tests remain the named new regressions, not recovery or qualification
of the lost original 58-case probe: cases 4, 16, 28, 40, and 49; forged source;
forged step; and native ABA/no-write coverage. The forward, whole inverse,
redo, history, steps, patches, reads, dependencies, effects, bindings, and
canonical-document assertions remain intact.

## Authenticity and provenance

All authored baseline, forward, inverse, and intervening writes go through the
registered Agent provider and `RuntimeService.commit_timeline`. Direct store
access is limited to canonical bootstrap and read-only closure/history/SQLite
snapshot inspection. There is no synthetic prepared record, direct accept,
hand-built history/publication, SQL injection, alternate executor, or bypass.

Runtime checkout `/home/user/work/runtime` was clean at
`49ce53289bc37d9387a7d9e6b9c9b16072162181`, tree
`364380ae064c512c0a0d2b8903a599b7026642f4`.
The test asserted actual module origins and SHA-256 identities before and after
each case/node; the independently checked values were:

- Agent `commit.py`: `741e8afcca27577e3a620b60351880a8df60aa2f4b48f15e0961fb63695edabc`
- Agent `inverse.py`: `fdae9b17f000a6968009222233327a0662748d0289d090a03c36f0e213121ee7`
- Runtime `timeline_commit_auth.py`: `65fd735edfa0e9f4a77aaf4f473095f1539ea1ce453439177e9fe7f39b4466f1`
- Runtime `timeline_commit_store.py`: `243d312fe404f5ed80f0ef1aa9d7405b93ff77949eef5157827a7779c6323b9f`

## Evidence

Exact acceptance command:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --timeout=45 --tb=short tests/editing_conformance/test_inverse_stage_runtime_regressions.py
```

Result: `7 passed in 14.61s`.

Additional checks:

- Scoped Ruff: passed (`All checks passed!`).
- `MYPY_CACHE_DIR=... make PY=/home/user/work/venv-agent-typecheck-v2/bin/python mypy`: `current=1912 baseline=1912`.
- `scripts/vendor_lock.py check runtime.lock.json`: passed.
- `scripts/artifact_manifest.py --check`: `artifacts.json is current`.
- `git diff --check db3c11ca6..HEAD` and working-tree diff check: clean.
- Worktree and actual integration Agent/Runtime checkouts: clean.

The prescribed worker `tmpdir` is an existing regular file, so the first
cache-directory setup could not run; Ruff was rerun successfully with a
private `/tmp` cache. This did not modify the worktree or shared dependencies.
The supplied historical control-doc path
`/home/user/peteromallet/astrid-agent/docs/projects/timeline-r4/` is absent;
the review used the provided PLAN and available prior worker report.

No full, original-58, HTTP/browser/live-socket, native14, daemon, install, Git
write, or shared-dependency mutation was run. No blocker remains for this
read-only review. Recommended next step: merge the test-only current-port
review, preserving the explicit limit that it qualifies seven named tests,
not the original 58-case probe.
