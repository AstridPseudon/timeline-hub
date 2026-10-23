# G5 process-fixture port report

## Result

Implemented the bounded, test-only port in `tests/sdk/test_timeline_persistence.py`.
The child process still owns only local draft edits and persistence.  The
ported positive path now binds its publication/head movement to an in-process
current RuntimeService through the public `RemoteTimelines` client, with the
exact revision/publication pair and canonical closure retained in the child
working copy.  The original positive test function body is AST-identical to
the base (`f736dd2d...`); its nudge/save/restart/peer-head/publish assertions
were not rewritten.

The fixture also adds a setup-only smoke case covering exact revision and
publication receipt binding, canonical digest/full closure, timeline scope,
missing commit fields, and SQLite no-write preservation on refusal.

## Evidence

- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/sdk/test_timeline_persistence.py::test_genuine_persistence_fixture_binds_exact_pair_and_refuses_bad_scope_without_writes --basetemp=/tmp/w-09fc76b42d/persistence-smoke-final`
  - **1 passed**.
- Same file excluding the known disjoint positive:
  `.../python -m pytest -q -o addopts= -p no:cacheprovider tests/sdk/test_timeline_persistence.py -k 'not test_publish_after_a_restart_merges_other_clips_onto_the_moved_head' --basetemp=/tmp/w-09fc76b42d/persistence-legacy`
  - **8 passed, 1 failed**. The failure is the unchanged adjacent same-clip refusal reaching the retired fake-client boundary (`AttributeError: SimpleNamespace has no _remote`); no expectation was changed.
- The requested disjoint positive was **not run**, per the brief: current `Cut.nudge` capture is separately owned and known to fail before meaningful G5 capture qualification.
- `python3 -m py_compile tests/sdk/test_timeline_persistence.py`: pass.
- `git diff --check`: pass.
- Scoped Ruff current vs base: both contain only the inherited `BLE001` at the worker's pre-existing broad exception handler; no new diagnostics.
- Scoped mypy with `--follow-imports=skip`: current and base both contain the same four inherited `union-attr` diagnostics in `Writer`'s subprocess streams.
- Diff scope: only `tests/sdk/test_timeline_persistence.py`.

## Decisions and limits

- Runtime setup uses trusted test seeding only to install the tiny authored
  closure and ingested media; the publication/read exercise uses the current
  public client and Runtime commit provider.
- The legacy adjacent same-clip test remains unchanged and remains blocked by
  the retired fake publication seam.  No production code, contract, schema,
  generated client, shared dependency, browser, daemon, or full suite was
  touched or run.
- End-to-end success of the port remains unverified until the separate
  `Cut.nudge` capture owner supplies the meaningful capture behavior.
