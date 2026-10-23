# G5 inverse reader return — fixture authority smoke

## Disposition

**SOURCE PASS for the bounded Agent fixture correction; Runtime behavior remains
PENDING and G5 remains draft-only / P1 NO-GO.**

The change is limited to
`tests/sdk/test_timeline_restructure_guarded_runtime.py` in Agent. The inherited
`restructure_runtime` fixture in `tests/sdk/test_timeline_restructure.py` is
untouched. No Runtime, provider, production SDK, sync, pin, schema, contract,
dependency, or helper changes were made.

## Correction and authority mapping

The previous candidate restored production `RemoteTimelines.open_bundle`, but
left the inherited `open_composition(project, timeline)` lambda in place. The
production reader calls `open_composition(..., revision_id=..., limit=1)` at
`astrid/sdk/_remote_timeline.py:48`, so setup failed before any public read or
Runtime seam.

The new local fixture binds the real production methods and the generated-client
shapes to the one inherited Runtime service owner:

| Test binding | Actual boundary / forwarding |
| --- | --- |
| `generated.list_timelines(project_id, *, cursor, limit)` | `RuntimeService.list_timelines`; converts its page mapping to the generated `(items, next_cursor)` return shape |
| `generated.inspect_timeline(project_id, timeline_id, options=None)` | `RuntimeService.inspect_timeline(project_id, timeline_id, options)` |
| `generated.list_timeline_commits(project_id, timeline_id, *, cursor, limit)` | `RuntimeService.list_timeline_commits(..., authorize=...)` |
| `RemoteTimelines._resolve_timeline` | Existing production resolver, using the public timeline listing |
| `RemoteTimelines.open_composition` | Existing production inspection adapter, preserving revision, filter, and limit arguments |
| immutable parent/shot/internal revision handlers | Existing fixture transport methods, forwarding exact project/timeline/shot/revision arguments |
| `RemoteTimelines.open_bundle` | Existing production exact closure reader, including publication receipt, digest, and canonical/full-closure equality checks |

No kwargs are absorbed, no historical revision is replaced with head, and no
private closure cache or fixture-supplied `_runtime_document` is introduced.
The service remains the single owner and is closed by the inherited fixture's
`finally` block.

## New behavioral smoke

`test_fixture_reader_authorizes_exact_pair_and_refuses_wrong_scope_without_writes`
actually calls `timeline.open`, then hydrates its session through the exact
revision/publication pair. It also opens a real historical receipt pair and
asserts:

- the returned revision is historical, `is_current_head` is false, and the
  parent pin matches the requested revision/publication;
- the hydrated runtime document equals the selected receipt's canonical
  document and carries a nonempty parent content digest;
- the current-head publication paired with the historical revision is refused;
- a missing timeline scope is refused; and
- history and the current head are byte-equal before and after both negatives.

The original accepted restructure request assertions, canonical/equivalence
checks, opaque null/order preservation, whole undo/redo assertions, overlap
refusal, explicit head/history checks, and canonical readback remain unchanged
in the existing guarded inverse body (lines 157 onward). The legacy fixture is
not in the diff.

## Verification

Agent worktree: `/home/user/work/wt/agt-G5-inverse-reader-return-1250`.

Runtime origin used for local verification: `/home/user/work/wt/rt-pin-3b926efa`,
commit `3b926efab2eed122d374540baee297d4cdcec62a`, tree
`b794170504544b259781e50d7ca4d61b6729e67c`.

Exact bounded smoke command:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-3b926efa ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-3b926efa /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --timeout=25 tests/sdk/test_timeline_restructure_guarded_runtime.py -k fixture_reader
1 passed, 1 deselected in 7.37s
```

Additional required checks:

```text
... pytest --collect-only -q -o addopts= -p no:cacheprovider tests/sdk/test_timeline_restructure_guarded_runtime.py
2 tests collected in 0.77s

/home/user/work/venv-agent/bin/ruff check --no-cache tests/sdk/test_timeline_restructure_guarded_runtime.py
All checks passed!

... python -m mypy --cache-dir=/tmp/agt-G5-inverse-reader-return-1250-mypy-final tests/sdk/test_timeline_restructure_guarded_runtime.py
Success: no issues found in 1 source file

git diff --check
passed
```

The final repository diff names only the guarded-runtime test. The original
whole inverse/undo/redo body was not rerun, and no broad/full, browser, HTTP,
native, D17, P1, or P4 suite was run. Runtime's one bounded observer must only
resume after this source correction has independent review; the prior 1236
observer captured no Runtime traceback because setup failed before the public
reader.

