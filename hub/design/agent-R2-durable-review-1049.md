# R2 durable known-cases independent review — FAIL

## Scope

Reviewed `tl/agt-R2-durable-known-cases-1038` (`046538e0a`, one commit beyond
`7abfb8d69`) against PLAN §3 R2 and the durable-known-cases/auth58 reports.
The candidate changes exactly one file:

`tests/editing_conformance/test_inverse_stage_runtime_regressions.py`

The file hash is
`60141abc0bbdff2b20c5e1c9f427ff517c9f2c1847d3ffd5c8ee50acbc8e43e6`, matching
the author report. No production files, original tests, Runtime files, pins,
schemas, environment files, or generated files are changed.

## Blocking finding

The candidate does not satisfy the explicit trusted-genesis requirement
(authentic existing setup; no fake history/claims). In the fixture at lines
192–213, it:

1. builds a document from the local `original_document()` fixture and mutates
   project/timeline/media/digests;
2. constructs a `prepared(...)` value and a hand-built `publication`;
3. clears its recorder claims (`writes`, `reads`, `bindings`, `created`,
   `dependencies`, and `derived_writes`); and
4. installs that result by directly calling `TimelineCommitStore.accept(...)`.

The test itself calls this a “synthetic baseline” and a “no-write historical
edge.” This is a fabricated durable history/canonical claim installed outside
the public Runtime service/provider path. It is therefore not an authentic
trusted genesis and prevents this candidate from qualifying the requested
complete real-store custody proof. The later forward commits and inverse/redo
requests do use `RuntimeService.commit_timeline` with the Agent provider, so
the finding is specifically the genesis setup, not a claim that the seven
public-path operations were skipped.

Required correction: obtain the baseline from the approved authentic existing
Runtime setup (or create it through the public provider/service path), and do
not hand-author or directly accept a synthetic history record. Preserve the
five named case identities and all original tests.

## What passed inspection

- Exactly seven named tests are collected: case 4, 16, 28, 40, 49, plus the
  forged-source/step and native-write/ABA refusal controls.
- The five positive cases use the real pinned Runtime commit
  `49ce53289bc37d9387a7d9e6b9c9b16072162181`, and their forward, whole inverse,
  and inverse-redo requests go through `RuntimeService.commit_timeline` and
  the registered Agent provider.
- Accepted responses and receipts are checked for identity, base pair,
  commands, label, merge mode, reads, source, rationale, group id, and
  publisher. Durable history is read with `store.history_entry`; records,
  steps, dependencies, derived writes, bindings, range/boundary presence,
  physical `clips`/`config.clips` mirroring, whole undo, and exact redo are
  exercised. Refusal controls assert unchanged head and SQLite `iterdump()`.
- Agent source hashes match the reviewed `7abfb8d69` content:
  `commit.py` `7776e31c...810eb3b` and `inverse.py`
  `267b1b15...08f336d`. Runtime hashes match the pinned checkout:
  `timeline_commit_auth.py` `65fd735e...4466f1` and
  `timeline_commit_store.py` `243d312f...6323b9f`.
- `_origin_snapshot()` is checked at fixture setup and throughout each
  positive/refusal case. The immutable `/home/user/work/runtime` checkout was
  clean at the pinned commit/tree.
- No original 58-case matrix, full suite, HTTP/browser/live-socket suite,
  native14 run, or daemon was run.

## Exact verification

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --collect-only tests/editing_conformance/test_inverse_stage_runtime_regressions.py
7 tests collected in 0.62s
```

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --timeout=45 --tb=short tests/editing_conformance/test_inverse_stage_runtime_regressions.py
.......                                                                  [100%]
7 passed in 15.16s
```

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. /home/user/work/venv-agent/bin/python -m ruff check --no-cache tests/editing_conformance/test_inverse_stage_runtime_regressions.py
All checks passed!
```

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. MYPY_CACHE_DIR=/tmp/agt-r2-review-mypy.mJwgtY /home/user/work/venv-agent-typecheck-v2/bin/python -m scripts.reshape.compare_mypy_baseline
Mypy findings: current=1912 baseline=1912
```

`git diff --check` is clean. The candidate has no uncommitted or untracked
worktree changes in this review checkout.

## Disposition

FAIL for qualification because of the synthetic direct-store genesis above.
The test file is otherwise a useful seven-test behavioral witness, but it
should not be merged as the requested durable R2 proof until the genesis is
replaced with authentic existing setup/publicly-created history.
