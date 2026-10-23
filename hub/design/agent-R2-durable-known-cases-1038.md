# R2 durable known-case regressions — PASS

## Scope and disposition

This is a test-only Luna result on Agent `7abfb8d69f625d0aada79346d5806f5f9525ed8c`.
It does not recreate, recover, or claim the irrecoverable original 58-case
probe. It adds seven independently named regressions covering the five
retained historical failure labels and three guarded refusal dimensions.

The new test file is:

- `tests/editing_conformance/test_inverse_stage_runtime_regressions.py`
- SHA-256: `60141abc0bbdff2b20c5e1c9f427ff517c9f2c1847d3ffd5c8ee50acbc8e43e6`

No production files, original tests, fixtures, generated clients, schemas,
pins, environment files, Runtime files, or other test files were changed.

## Exact new case inventory

| New node id | Historical class exercised |
| --- | --- |
| `case-4-two-step-clips-before` | two-step, `clips`, output-before, whole inverse |
| `case-16-two-step-clips-after` | two-step, `clips`, output-after, whole inverse |
| `case-28-two-step-config-clips-before` | two-step, `config.clips`, output-before, whole inverse |
| `case-40-two-step-config-clips-after` | two-step, `config.clips`, output-after, whole inverse |
| `case-49-native-whole` | split followed by native move, whole inverse |
| `test_known_inverse_refuses_forged_source_publication_and_step_without_writes` | authenticated source-publication and step-forgery refusals |
| `test_known_inverse_refuses_native_write_and_aba_without_writes` | native intervening write and native A→B→A refusal |

Each positive case creates a complete real Runtime realm, installs the
fixture closure, accepts the forward v2 request through the public
`RuntimeService.commit_timeline` → Agent provider → Runtime store path, reads
the exact accepted entry with `store.history_entry`, then performs public
whole inverse and public inverse redo. The assertions cover the full request
envelope (base pair, commands, label, steps, merge, reads, dry-run, source,
rationale, group id), accepted `{data, receipt}` identity, canonical command
copies, history label/merge/steps/dependencies, reads, effects, bindings,
ranges, physical `clips`/`config.clips` equality, whole undo, and exact redo.

Refusal tests use accepted durable forward history. They assert the Runtime
head and complete SQLite durable snapshot are unchanged. Forged source
publication, forged step id, native intervening write, and native ABA all
refuse without an accepted inverse.

## Source identity checked by the tests

Agent source is verified before and after every case. The `commit.py` and
`inverse.py` blobs are byte-identical at both `ef851b22c506245441b9a630c093b3460e39cbdc`
and `7abfb8d69f625d0aada79346d5806f5f9525ed8c`:

```text
astrid/sdk/timeline/commit.py  7776e31c83a7f0fc58965141b5863548c7cd4bb60f58f5c827848254c810eb3b
astrid/sdk/timeline/inverse.py 267b1b1589c0254345a13bf802df8b40301f70020389c223c91f4b14808f336d
```

Runtime is loaded from exact commit `49ce53289bc37d9387a7d9e6b9c9b16072162181`,
tree `364380ae064c512c0a0d2b8903a599b7026642f4`. The test checks the imported
Runtime module origins and hashes before/after each case:

```text
runtime_protocol/timeline_commit_auth.py   65fd735edfa0e9f4a77aaf4f473095f1539ea1ce453439177e9fe7f39b4466f1
runtime_protocol/timeline_commit_store.py  243d312fe404f5ed80f0ef1aa9d7405b93ff77949eef5157827a7779c6323b9f
```

The Runtime archive is used only to load the frozen source; the accepted
forward and inverse operations use the real SQLite `TimelineCommitStore` and
the public service/provider path. No detached realm, fabricated candidate
history, cache, executor, guard drop, skip, xfail, or normalizer was used for
the five proof cases.

## Evidence

Collection was exactly seven tests:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --collect-only tests/editing_conformance/test_inverse_stage_runtime_regressions.py
7 tests collected in 0.53s
```

Final named test run:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --timeout=45 --tb=short tests/editing_conformance/test_inverse_stage_runtime_regressions.py
.......                                                                  [100%]
7 passed in 15.39s
```

Static checks:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. /home/user/work/venv-agent/bin/python -m ruff check --no-cache tests/editing_conformance/test_inverse_stage_runtime_regressions.py
All checks passed!

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. MYPY_CACHE_DIR=<private worker tmpdir>/mypy-cache /home/user/work/venv-agent-typecheck-v2/bin/python -m scripts.reshape.compare_mypy_baseline
Mypy findings: current=1912 baseline=1912

git diff --check
clean
```

No full suite, HTTP/browser/live socket/native14, original 58-case matrix,
or broad known-regression rerun was requested or run. This result qualifies
the new durable named regressions only; it does not relabel the historical
53/58 result or claim recovery of the original matrix.

## Decision and next step

The only implementation decision was to use a real Runtime SQLite realm with
an authenticated immutable fixture closure, then let each new forward edit
create its own durable history entry. This preserves the brief's requirement
that inverse authentication consume actual accepted history while avoiding
the irrecoverable original matrix. The orchestrator can merge this single
test file and retain the five historical labels as separate, reviewable R2
regressions.
