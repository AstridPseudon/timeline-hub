# Runtime RT07 writer-cut candidate

## Scope and result

This is an isolated deletion candidate from Runtime `6ab3243972f8dc49105819e6d7ba7aef1a2888b8`. It removes only the remaining canonical-document writer body from `RuntimeService.publish_timeline_render`.

- Deleted 172 product lines from `runtime_protocol/service.py`.
- Kept the decorated service method, HTTP route, worker-route authentication, generated clients, OpenAPI route, and existing project/target authority helper in place for the migration boundary.
- The service method now returns the visible retired-route refusal (`410`, `reason: command_required`, replacement `/v1/projects/{project_id}/timelines/{timeline_id}/commit`) before payload, attempt, lease, checkpoint, CAS, document, render-task, or event lookup.
- Added one focused zero-write refusal assertion in `tests/test_timeline_render_publication_authority.py`; all original legacy publication positives remain unchanged with all assertions.

The removed body was the only remaining direct path that updated `project_documents`, emitted `timeline.document.saved`, published a legacy timeline snapshot, admitted a `rendering.render` task, and completed `timeline_render_publications` for this operation. The Runtime task/checkpoint tables, normal task settlement/idempotency, canonical commit/history/receipt infrastructure, ordinary rendering admission, execution, catalog, and source-document paths were not changed.

## Callers and replacement boundary

The Runtime route remains at `runtime_protocol/server.py:1040-1042`; generated Python/TypeScript clients and the OpenAPI operation remain intentionally present so callers receive the refusal while migration is incomplete. The current Agent caller chain still includes `astrid/core/execution/generic_host.py:_publish_assembled_timeline` and its `run_task` dispatch, plus the remote/workspace client wrappers and `astrid/packs/rendering/shared/runtime_stitch.py`. This candidate does not modify those consumers.

Before landing, those callers must be migrated and qualified through the native path: settled proposal -> requester/outbox -> `/v1` commit, with producer authority checked by D13. The original positive replacement map remains the Agent `tests/packs/rendering/test_registered_assembler_producer.py` cohort: settled-proposal creation, requester/outbox handoff, commit retry, historical render pinning, MP4 output, and undo. Landing also requires the native two-positive gate, lost-ACK/restart/exact-retry identity, no duplicate render/CAS, and commit/history/undo evidence. The branch remains DRAFT and must not be merged or requested for merge before that cohort qualifies.

## Evidence

- `/home/user/work/venv-runtime/bin/python -m pytest -q tests/test_timeline_render_publication_authority.py -k retired_writer_refuses_before_lookup_without_writes`: **1 passed, 17 deselected**.
- `/home/user/work/venv-runtime/bin/python -m pytest -q tests/test_timeline_render_publication.py`: **3 failed**. These are the unchanged old positive publication/retry/restart tests, failing at the deliberate retired-route refusal; they were not skipped, xfailed, weakened, or converted to refusal expectations.
- Combined local authority/door/legacy attempt: **1 passed, 17 failed, 70 errors**. Door tests could not bind localhost in this sandbox (`PermissionError: [Errno 1] Operation not permitted`); the legacy publication authority positives fail for the same intentional refusal. The central localhost-dependent targeted lane `rt-m2-render-writer-cut-prepare-targeted-1020161414-17036` completed **17 failed, 13 passed in 50.24s**. Its failures are the unchanged legacy publication positives; its door/refusal controls passed.
- `/home/user/work/venv-runtime/bin/python -c '...compile service.py and test...'`: passed.
- `git diff --check`: passed.
- No full suite, renderer, browser, live socket, or merge was run locally. No shared dependency, cache, branch, or other worktree was modified.

## Decision / blocker

The deliberate choice is the prior RT07 native-first boundary: refusal is early and visible, while the route and compatibility surface remain available for consumer migration. The candidate is not green by design because the old registered-host positive path still calls the retired writer. The remaining blocker to landing is consumer qualification, not a Runtime source ambiguity.
