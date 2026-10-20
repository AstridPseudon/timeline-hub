# Runtime main archive/recover lifecycle witness

Date: 2026-10-20 UTC  
Snapshot: `origin/main` at `240d5bb202af709294551045554012f079fd06ca`  
Scope: one normal Runtime service-API before/after witness; no source changes.

## Result

The old main behavior is a genuine D04 preservation gap if timeline archive/recover is kept as a supported lifecycle operation. It is catalog/visibility lifecycle state, but `recover(version=old)` also restores the old legacy flat film projection. It does not restore ordinary timeline-document bytes or canonical parent film state.

The current integration API is already retired: `RuntimeService.archive_timeline()` and `recover_timeline()` call `_require_timeline_command()` (`runtime_protocol/service.py:3846-3852`), which raises 410 `retired_route`, reason `timeline_commit_required`, and names the `/commit` route. No replacement semantic mapping was assumed.

## Normal API witness

The immutable snapshot was extracted with `git archive origin/main` to a private `/tmp` directory and run from that snapshot. Setup used normal `RuntimeService` methods only:

1. `create_project`.
2. `create_timeline_document` with nonempty config/registry state A.
3. `update_document` for `timeline:main` to ordinary config/registry state B, including `registry.flatlinks = {clip-b: asset-b}`.
4. Two `update_timeline` calls to create flat states at versions 2 and 3: state A has `flat-shot-a`/`flat-ref-a`; state B has `flat-shot-b`/`flat-ref-b`.
5. `publish_parent_composition` for one immutable canonical parent revision `parent-1`.

Only after this setup were `archive_timeline(expected_version=3)` and `recover_timeline(expected_version=4, version=2)` called. Read-only SQL was used only to inspect relational rows/heads; it did not seed or mutate the fixture. No renderer, fake history, or default timeline was used.

## Before / after facts

| Observation | Before archive | After archive | After recover old version 2 |
|---|---|---|---|
| `timelines.version` / `archived_at` | `3` / `NULL` | `4` / non-null | `5` / `NULL` |
| ordinary document config version | `2` | unchanged `2` | unchanged `2` |
| ordinary config marker | `B` | unchanged `B` | unchanged `B` |
| ordinary `registry.flatlinks` | `{clip-b: asset-b}` | unchanged | unchanged |
| flat shots | `flat-shot-b`, 250ms/1500ms | unchanged | `flat-shot-a`, 0ms/1000ms |
| flat references | `flat-ref-b -> asset-b (hero)` | unchanged | `flat-ref-a -> asset-a (source)` |
| timeline history versions | `1,2,3` | `1,2,3,4` | `1,2,3,4,5` |
| canonical parent head | `parent-1` | unchanged | unchanged |
| canonical parent digest | `sha256:d4a5cb578697ae86e11834eabb3c3229fa249c307a52f036182701fb1ed6263f` | unchanged | unchanged |
| canonical parent history | `[parent-1]` | unchanged | unchanged |

The canonical head payload was the same before archive, after archive, and after old-version recover:

```json
{"clips":[],"config":{"canonical_marker":"one"},"occurrences":[{"duration_ms":1000,"gain":1,"muted":false,"occurrence_id":"occurrence-1","placement":{"start_ms":0},"provenance":{},"shot_id":"shot-1","shot_revision_id":"shot-rev-one","source_offset":0,"speed":1,"track":"video-1","transform":{}}],"registry":{}}
```

The archive result was `timeline.archive`, version 4, `archived=true`. The recover result was `timeline.recover`, version 5, `archived=false`; its returned shots/references were exactly the saved version-2 flat state. The old timeline history entries remained immutable, and archive/recover added new v4/v5 entries rather than rewriting v2/v3.

Exact bytes/heads that changed:

- `timelines`: `version` and `archived_at` on archive; `version` and `archived_at` on recover.
- `timeline_shots` and `timeline_references`: archive leaves state B in place; recover deletes/reinserts the old state-A rows. Recreated shot/reference state rows have version 1 and no archive timestamp.
- `timeline_revisions`: new snapshots for v4 and v5; prior v1-v3 snapshots remain.
- `timeline_events` and idempotency receipts: `timeline.archived` and `timeline.recovered` events were appended.
- The ordinary `project_documents` row, its config/registry bytes, and its version 2 digest did not change.
- `parent_composition_heads`, `parent_composition_revisions`, canonical payload bytes, canonical digest, and canonical history did not change.

This proves the important boundary: old recover is not catalog-only in its implementation, because it rebuilds the old flat film state; however, it is also not canonical-film restore and must not be mapped to the existing `timeline.restore` command without an explicit semantic decision.

## Existing coverage and consumers

- The original main positive is `tests/test_runtime_domains.py::test_generated_domains_preserve_project_media_and_timeline_recovery` (origin/main lines 300-321): it asserts archive/recover visibility and saved flat shots.
- Current integration retains that behavior as an explicit strict xfail in `tests/test_runtime_domains.py::test_generated_timeline_recovery_is_retired_pending_commit_replacement` (lines 366-381).
- The direct service positive is also retained as strict xfail in `tests/test_stage1_runtime_contract_completion.py::test_timeline_update_archive_recover_replay_the_same_committed_receipt` (lines 51-66), with the D04 replacement note.
- Agent real consumers remain in `astrid/sdk/remote.py:1603-1616`, `astrid/packs/timeline/cli.py:1382-1397`, and duplicate cleanup `astrid/sdk/timeline_duplicate.py:181-185`. App search found no non-generated archive/recover caller.
- Agent's `timeline.restore` opcode is an authored canonical timeline restore (`astrid/sdk/timeline/commands.py:96`, `168-193`), not an archive/visibility operation. The Agent `timeline.recovered` event projection is likewise a config projection event (`astrid/core/timeline/projection.py:649-658`), not proof of a Runtime archive/recover replacement.

## Recommendation

Keep the boundary catalog/visibility-oriented only if the workflow remains required, but define one narrow, guarded replacement that explicitly preserves the observed two-part behavior: archive/recover relational visibility and, when requested, lossless restoration of the legacy flat projection. Do not use `timeline.restore` as the mapping, and do not add a new command/route/DTO in this witness. Manager decision is required before implementation or before removing the live Agent CLI/remote consumers.

## Commands and results

- `git archive origin/main | tar -x -C <private /tmp snapshot>; PYTHONPATH=<snapshot>/packages/python:<snapshot> python <witness>` — **pass**; all before/after assertions above passed on `origin/main` `240d5bb...`.
- `PYTHONPATH=<worker packages>:<worker> python <current-service-410 probe>` — **pass**; normal current service call raised `RetiredRouteError`, status `410`, code `retired_route`, reason `timeline_commit_required`.
- `python -m pytest -q tests/test_stage1_runtime_contract_completion.py::test_timeline_update_archive_recover_replay_the_same_committed_receipt` — **1 xfailed**, as required by the existing D04 strict-xfail; one unrelated pytest `timeout` config warning.

No full suite, localhost/browser suite, renderer, package install, source edit, or shared-dependency write was performed.
