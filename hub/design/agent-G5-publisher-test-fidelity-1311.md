# G5 publisher test-fidelity return

## Scope and decision

This is a bounded, test-only return on `57f0d32f370ac7c1f0c3959ac65ab1351a6ffc2c`
(`tl/agt-G5-process-fixture-port-1258`) with parent
`6bd5e1a89ad12bf23c6c2ccb0f29cedfd4fd234f`. No product, Runtime, schema,
generated client, pin, contract, shared dependency, or alternative executor was
changed.

The process refusal test is now activated with the existing
`genuine_runtime` fixture. Its peer-head setup uses the public `RemoteTimelines`
client against the in-process `RuntimeService`, an exact revision/publication
pair, `emit_document_commands`, and an atomic commit with a timeline-scope read
in the step. The child process still owns only its local draft/nudge/save/
restart state. Its legacy `world.head` keeps the test's asserted `rev-1` label;
the parent publication and conflict decision use Runtime's actual head and
closure. A Runtime `CommitConflict` is translated by this test-only adapter to
the original `Refused("not published: someone published")` expectation.

The normal-publish draft is split honestly:

1. `test_nudge_disjoint_clips_merge_onto_peer_head` uses the existing captured
   `Clip.nudge` operation on `cross`, checks `fields` plus operation-time reads,
   and preserves the successful disjoint merge with peer `p2`.
2. `test_ordinary_direct_opaque_edit_is_atomic_and_refuses_peer_head` keeps the
   direct opaque edit separate as an unknown/free transform. It requires
   `atomic` with no caller-invented reads and checks canonical document, head,
   history, and SQLite no-write preservation after the peer head intervenes.

The original complex `a-rocket` disjoint process positive remains held as
requested; its missing operation-time `Cut.nudge` capture is not encoded as a
refusal or weakened expectation.

## Provenance and body locks

The independent review established that `tests/sdk/test_timeline_normal_publish.py`
was absent at `aa2fa8677^` and at upstream refs
`431681a6d3cfa0bba2c8c9baa03f152d33032df1`,
`74f3f7edba35230d0a01824eae7b663143e6aa5b`, and
`d1fa6c1332011e4c6f6e075ca458c7dff6bf130c`. The direct-opaque test added by
`aa2fa8677` (its lines 167–180) therefore was not retained as an original
positive promise.

The actual pre-existing positive is
`tests/sdk/test_timeline_persistence.py::test_publish_after_a_restart_merges_other_clips_onto_the_moved_head`,
present at all three upstream refs above (for example lines 446–462 at
`431681a6d3cfa0bba2c8c9baa03f152d33032df1`): operation-time `a-rocket`
`nudge`, save/restart, `b-type` peer edit, merged head, and both clip assertions.

The two original process test bodies remain AST-identical:

| test | before body AST SHA-256 | after body AST SHA-256 |
|---|---|---|
| `test_publish_after_a_restart_merges_other_clips_onto_the_moved_head` | `e1eb217ab5fcccbfe64ac9c4b66db125c5b3028766808c7fd57e904c542f5ece` | same |
| `test_publish_after_a_restart_refuses_a_clip_both_sides_changed` | `9cb7a13485b8b257eb1e45173366a1a5def4b55425905e5d52b293c6fbba00b3` | same |

Only fixture activation/transport setup changed around those bodies. The
assertion mapping remains:

| original assertion | retained evidence |
|---|---|
| process nudge → save → restart | unchanged child-process body; genuine refusal run reaches the saved `a-rocket` start `1.8` |
| peer/head movement | genuine Runtime public atomic peer commit with exact base pair; child file retains `rev-1` assertion label |
| overlap refusal | genuine Runtime conflict on the guarded `a-rocket` address |
| no-write | original working-copy/head assertions plus direct-opaque test's canonical/head/history/database snapshots |
| disjoint positive | captured `cross.nudge` test asserts `fields`, reads, merged status, moved `cross`, and peer `p2` |

## Exact evidence

Pinned environment for Runtime-backed tests:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-3b926efa \
ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-3b926efa \
/home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider \
  tests/sdk/test_timeline_persistence.py::test_genuine_persistence_fixture_binds_exact_pair_and_refuses_bad_scope_without_writes \
  tests/sdk/test_timeline_persistence.py::test_publish_after_a_restart_refuses_a_clip_both_sides_changed \
  tests/sdk/test_timeline_normal_publish.py::test_nudge_disjoint_clips_merge_onto_peer_head \
  tests/sdk/test_timeline_normal_publish.py::test_ordinary_direct_opaque_edit_is_atomic_and_refuses_peer_head \
  --basetemp=/tmp/agt-g5-publisher-fidelity-focused-final
```

Result: **4 passed in 17.93s**.

The independent simple-helper neighbor was also run against the same pin:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-3b926efa \
ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-3b926efa \
/home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider \
  tests/sdk/test_timeline_helper_capture.py::test_nudge_restart_merges_peer_other_clip \
  --basetemp=/tmp/agt-g5-known-nudge-final
```

Result: **1 passed in 8.65s**.

Collection of both edited files: **22 tests collected**.

```sh
RUFF_CACHE_DIR=/tmp/agt-g5-publisher-fidelity-checks/ruff \
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python \
-m scripts.reshape.compare_ruff_baseline
```

Result: **current=2149, baseline=2149**.

```sh
MYPY_CACHE_DIR=/tmp/agt-g5-publisher-fidelity-checks/mypy \
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent-typecheck-v2/bin/python \
-m scripts.reshape.compare_mypy_baseline
```

Result: **current=1912, baseline=1912**.

`git diff --check` passed. Direct scoped Ruff reports the repository's existing
legacy diagnostics (`BLE001` in the process worker, existing import/F811
findings in the normal-publish file); the repository baseline comparator is
unchanged and no new baseline finding was introduced.

No full suite, browser, HTTP/socket, native, P1/P4, daemon, or complex original
disjoint process positive was run. G5 remains DRAFT-only / P1 NO-GO pending the
separately owned cut/anchored operation-time capture and the other review gates.
