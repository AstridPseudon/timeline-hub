# G5 publisher fidelity independent review

## Disposition

Bounded review **PASS** for the test-fidelity slice. G5 remains **DRAFT-only / P1 NO-GO**:
the original cut-linked `a-rocket` positive was not run and is not qualified by this
review. No production, Runtime, schema, generated client, pin, contract, dependency,
or alternative executor changed.

The worktree change is limited to `tests/sdk/test_timeline_persistence.py`. The current
`tests/sdk/test_timeline_normal_publish.py` cases were reviewed but needed no further
edit.

## What was repaired and checked

- The genuine Runtime fixture is now a direct dependency of both retained persistence
  targets: the original disjoint positive and the original same-clip refusal. This is
  a function-argument dependency, not a late marker. `pytest --setup-only --setup-show`
  reported `genuine_runtime` in both fixture closures. The setup-only run executes no
  tests and therefore exits 5; that is recorded as setup evidence, not a product test
  result.
- The fake child client now reports the project/timeline identity from the head bundle,
  so the generated Runtime project identity is not replaced by legacy `p`/`t` values.
  The candidate transport carries the saved checkout path. The genuine publication
  seam reloads that saved checkout and asserts its bundle equals the child candidate,
  preserving the persisted path and journal-backed helper-call source for publication.
- The original persistence test bodies were not rewritten. Their body AST SHA-256
  values remain identical to the upstream originals:

  | test | AST body SHA-256 |
  |---|---|
  | `test_publish_after_a_restart_merges_other_clips_onto_the_moved_head` | `e1eb217ab5fcccbfe64ac9c4b66db125c5b3028766808c7fd57e904c542f5ece` |
  | `test_publish_after_a_restart_refuses_a_clip_both_sides_changed` | `9cb7a13485b8b257eb1e45173366a1a5def4b55425905e5d52b293c6fbba00b3` |

  Both hashes matched refs `431681a6d3cfa0bba2c8c9baa03f152d33032df1` and
  `d1fa6c1332011e4c6f6e075ca458c7dff6bf130c`.

## Provenance and no weakening

The source-provenance finding from the 1258 review remains in force: the old direct
opaque disjoint test was introduced by blocked `aa2fa8677`; it was not an inherited
positive. The retained positive is the persistence test's operation-time
`a-rocket` nudge, which is cut-linked/anchored and still lacks the required genuine
operation-time capture. No old positive or refusal assertion was converted to a
refusal, skipped, deleted, or weakened.

The normal-publish split is correctly classified:

- `test_nudge_disjoint_clips_merge_onto_peer_head` is the known captured `cross.nudge`
  positive and checks `fields`, operation-time reads, the base publication pair,
  merged status, and both resulting clips.
- `test_ordinary_direct_opaque_edit_is_atomic_and_refuses_peer_head` is new coverage
  for an unknown/free transform. It supplies no invented reads, requires `atomic`,
  and checks document, head, history, and SQLite no-write preservation.

The reviewed request construction retains the v2 base revision/publication pair,
commands, label/source, step ids/intents/tags/ordinals/patch/reads, merge mode,
idempotency key, and the existing receipt/canonical/history/conflict paths. No fake
authority, closure substitution, scope widening, source binding, guard waiver, or
schema/tool/generated-file change was added.

## Evidence

Runtime-backed focused cases, run once with the pinned Runtime checkout:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-3b926efa \
ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-3b926efa \
/home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider \
  tests/sdk/test_timeline_persistence.py::test_genuine_persistence_fixture_binds_exact_pair_and_refuses_bad_scope_without_writes \
  tests/sdk/test_timeline_persistence.py::test_publish_after_a_restart_refuses_a_clip_both_sides_changed \
  tests/sdk/test_timeline_normal_publish.py::test_nudge_disjoint_clips_merge_onto_peer_head \
  tests/sdk/test_timeline_normal_publish.py::test_ordinary_direct_opaque_edit_is_atomic_and_refuses_peer_head \
  --basetemp=/tmp/agt-g5-publisher-fidelity-focused
```

Result: **4 passed in 18.54s**.

Fixture dependency proof:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-3b926efa \
ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-3b926efa \
/home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider \
  --setup-only --setup-show -rA \
  tests/sdk/test_timeline_persistence.py::test_genuine_persistence_fixture_binds_exact_pair_and_refuses_bad_scope_without_writes \
  tests/sdk/test_timeline_persistence.py::test_publish_after_a_restart_merges_other_clips_onto_the_moved_head \
  tests/sdk/test_timeline_persistence.py::test_publish_after_a_restart_refuses_a_clip_both_sides_changed \
  tests/sdk/test_timeline_normal_publish.py::test_nudge_disjoint_clips_merge_onto_peer_head \
  tests/sdk/test_timeline_normal_publish.py::test_ordinary_direct_opaque_edit_is_atomic_and_refuses_peer_head \
  --basetemp=/tmp/agt-g5-publisher-fidelity-setup-only
```

Result: both persistence targets showed `genuine_runtime`; normal-publish targets
showed `restructure_runtime`. Pytest reported `no tests ran` / exit 5 because
`--setup-only` intentionally performs setup without executing tests.

Static checks:

- `python -m py_compile tests/sdk/test_timeline_persistence.py tests/sdk/test_timeline_normal_publish.py`: **pass**.
- `git diff --check`: **pass**.
- `PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/ruff check --no-cache
  tests/sdk/test_timeline_persistence.py tests/sdk/test_timeline_normal_publish.py`:
  **fails only on inherited diagnostics** (10 existing findings: worker `BLE001`,
  existing import ordering, and existing `F811` fixture imports).
- Scoped Ruff on the two test files reports only inherited legacy diagnostics (the
  worker's `BLE001`, existing import ordering, and existing `F811` fixture imports).
  `RUFF_CACHE_DIR=/tmp/agt-g5-publisher-fidelity-static/ruff PYTHONDONTWRITEBYTECODE=1
  /home/user/work/venv-agent/bin/python -m scripts.reshape.compare_ruff_baseline`:
  **current=2149, baseline=2149**.
- `MYPY_CACHE_DIR=/tmp/agt-g5-publisher-fidelity-static/mypy PYTHONDONTWRITEBYTECODE=1
  /home/user/work/venv-agent-typecheck-v2/bin/python -m
  scripts.reshape.compare_mypy_baseline`: **current=1912, baseline=1912**.
- Diff/file census: only `tests/sdk/test_timeline_persistence.py` changed; no added
  identity/schema/generated/pin/tool files.

No full suite, browser, HTTP/socket, native, P1/P4, daemon, or complex original
process positive was run.

## Remaining qualification and owner

The original `a-rocket` positive remains unqualified. Its `Clip.nudge` is anchored to
the cut/word path, and the existing bounded capture does not yet record and
authenticate the operation-time word/transcript resolution, cut/child timing,
occurrence, retime, theme/FPS, and related closure inputs. This belongs to the Agent
helper-capture / G3-provider boundary owner identified in the 1258 report. After that
owner supplies the real capture and authenticated replay, the process-fixture owner
must run the retained complex body through this now-correct genuine fixture.

This review does not claim that the original complex behavior is resolved merely
because fixture setup is genuine or because the detached `Checkout(candidate)` seam
now reloads the saved path. End-to-end persisted-call/capture proof for that original
body remains pending the owner above.

