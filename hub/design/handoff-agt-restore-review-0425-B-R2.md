# B — F-D86/R2 protected review

Verdict: `FAIL_SOURCE` (no behavior credit).

## Exact reviewed objects

- Commit: `99f2d183e724606628da41f9a885851832f39dd5`
- Parent/product review commit: `72a5e5333171bed4221865329ab48eb233b1bbda`
- New file blob: `8bf6c0833d370d9a0fb993d750ff83bb5066d522`
- File: `tests/sdk/test_timeline_restore_effect_order_runtime.py` (new, 152 lines)
- FIRST MAIN selector claimed by the author: `tests/sdk/test_timeline_restore_effect_order_runtime.py::test_id5_public_undo_of_restore_preserves_authenticated_effect_order`

## Static call-trace failure

The test creates a fresh explicit outbox and calls `opened()` at line 71, which calls public `timeline.open` at line 63. `TimelineSession.open` always reads `client.timelines.history(..., limit=1)` for an empty outbox (`astrid/sdk/timeline/sync.py:144–171`). The test replaces `client.timelines._resolve_timeline`, but its `WorkspaceClient.__new__` transport only assigns `transport._generated = SimpleNamespace()` and later assigns `generated.commit_timeline = send`; it never assigns `generated.list_timeline_commits`.

The actual public call continues through `RemoteTimelines.history` (`astrid/sdk/_remote_timeline.py:253–268`), `_RemoteFamily._typed` (`astrid/sdk/remote.py:328–405`), `WorkspaceClient.list_timeline_commits` (`astrid/sdk/workspace_client.py:502–517`), and `_call_generated` (`workspace_client.py:271–290`). That generated operation is absent from the test transport, so `_call_generated` returns a `not_ready` `WorkspaceClientError`; `_typed` converts it to a failed `DomainResult`, and `_response` at `sync.py:51–55` raises before the first commit. Thus the claimed public restore/undo path is unreachable under this exact fixture. This is a static source conclusion; the test was not executed.

## What was otherwise reviewed

The author evidence claims real `RealmStore`/`RuntimeService`, registered `load_timeline_commit_provider("astrid")`, ordinary `capture_track_create` plus `doc.patch` sibling changes, exact restore pins, authenticated history inspection, complete ordered inverse comparison, dry-run/no-write, head/history, and retry checks. The test has no `except` handlers or `pytest.raises`, and no raw SQL tokens. The product review of `72a5...` independently establishes the bounded authenticated singleton restore branch and effect-multiset comparison/order retention, with source trace through `sync.py:422–488`, `commit.py:1218–1261`, `_step_undo.py:349–359`, `inverse.py:1132–1186`, and `_commit_patch.py:538–557`.

Those positive source facts do not repair the missing history transport method. They therefore do not establish a genuine runnable public caller or any behavioral proof.

## Applicability and controls

The author’s stated scope is only the ordinary singleton `timeline.restore` then public `Timeline.undo` branch, excluding timing caches/range and parent-append seams. Historical old-RED evidence includes `tests/editing_conformance/test_word_binding_recipe.py::test_last_write_clear_undo_restore_and_restore_inverse` (10077: FAIL) and the parallel native-word-anchor selector (10077: setup ERROR). The new simple opaque-track fixture is not that original word-binding fixture, so applicability is bounded even if the transport defect is repaired. Existing negative selectors named by the author remain separate controls and receive no behavior credit here.

## Static commands/results

- `git diff 99f2^ 99f2 --check`: PASS.
- In-memory `ast.parse`/compile of the new file: PASS.
- Candidate Ruff through stdin: PASS (`All checks passed!`).
- Candidate author evidence reports scoped mypy PASS; no execution was performed here.
- Candidate AST inspection: 0 exception handlers, 0 `pytest.raises` calls, no raw SQL tokens.

No pytest, collection, helper/fixture execution, service, probe, browser, package install, or full suite was run.
