# Runtime Timeline-core size census

Refreshed for M4 on 2026-10-20. This is a rough-guide measurement, not a gate
or a target to optimize against. It follows PLAN's settled boundary: authored
Runtime product code that implements Timeline Read/See/Edit. It excludes
untouched worker/execution/catalog/custody infrastructure, generated DTOs,
generated schemas and clients, tests, fixtures, and package data.

## Exact source revisions

| label | commit | tree |
|---|---|---|
| main baseline | `origin/main` `29d0954b6d78a7d7937d81bc36567b6dee7ca976` | `eb06dfd08e6d489204f03d65e55951bcf521b326` |
| current integration | `tl/integration` `7f6dd8920e1ceec41b137358df5e7fecc304888d` | `4cccb2d643194df7df95d624e89a6cd9f6f268fc` |

The current integration SHA is the live Runtime integration ref in
`/home/user/work/runtime` and in this worker's read-only ref view. Frozen R4
candidate branches are not included. No prior-hold branch delta is included;
the current integration diff is measured directly from the exact two commits
above.

## Boundary and method

The count is committed-blob source lines, including blank lines, with one
explicit manifest applied to both revisions. For shared files, the manifest
selects named top-level AST functions/methods and counts each selected node's
inclusive `lineno..end_lineno` range. Overlapping ranges are unioned. This
prevents whole `service.py`, `store.py`, or `server.py` totals from being
presented as Timeline code.

Single-purpose handwritten Timeline modules are counted in full. The generated
`runtime_protocol/timeline_commit_types.py`,
`runtime_protocol/schemas/timeline-commit-bundle.json`, contract schemas,
generated Python/TypeScript clients, and all tests/fixtures are excluded.

### Selected-range census

| path | main | current | delta | selection |
|---|---:|---:|---:|---|
| `runtime_protocol/canonical_schema.py` | 121 | 139 | +18 | Timeline SQL ranges; current `TIMELINE_COMMIT_SCHEMA_SQL` included |
| `runtime_protocol/cli.py` | 37 | 37 | 0 | `audit-timelines` parser/handler ranges |
| `runtime_protocol/server.py` | 670 | 794 | +124 | Timeline helpers, commit routing, and `RuntimeHandler._route` AST range |
| `runtime_protocol/service.py` | 2,112 | 1,706 | −406 | named `RuntimeService` Timeline/commit/projection/view ranges |
| `runtime_protocol/store.py` | 117 | 117 | 0 | named Timeline projector/publication/event ranges |
| `runtime_protocol/capture_validation.py` | 0 | 225 | +225 | full handwritten capture module |
| `runtime_protocol/managed_render_snapshot.py` | 217 | 217 | 0 | full handwritten Timeline See module |
| `runtime_protocol/seam_intent.py` | 88 | 88 | 0 | full handwritten Timeline See module |
| `runtime_protocol/shot_dependencies.py` | 155 | 155 | 0 | full handwritten Timeline See module |
| `runtime_protocol/snapshot_refs.py` | 224 | 278 | +54 | full handwritten Timeline snapshot/projector module |
| `runtime_protocol/timeline_commit.py` | 0 | 55 | +55 | full handwritten commit module |
| `runtime_protocol/timeline_commit_baseline.py` | 0 | 441 | +441 | full handwritten commit module |
| `runtime_protocol/timeline_commit_execution.py` | 0 | 115 | +115 | full handwritten commit module |
| `runtime_protocol/timeline_commit_inputs.py` | 0 | 707 | +707 | full handwritten commit module |
| `runtime_protocol/timeline_commit_port.py` | 0 | 933 | +933 | full handwritten commit module |
| `runtime_protocol/timeline_commit_producer.py` | 0 | 285 | +285 | full handwritten commit module |
| `runtime_protocol/timeline_commit_producer_checkpoint.py` | 0 | 163 | +163 | full handwritten commit module |
| `runtime_protocol/timeline_commit_provider.py` | 0 | 93 | +93 | full handwritten commit module |
| `runtime_protocol/timeline_commit_store.py` | 0 | 995 | +995 | full handwritten commit module |
| `runtime_protocol/timeline_commit_validation.py` | 0 | 103 | +103 | full handwritten commit module |
| `runtime_protocol/timeline_cutover.py` | 217 | 217 | 0 | full handwritten Timeline audit module |
| `runtime_protocol/timeline_inspection.py` | 845 | 844 | −1 | full handwritten Timeline Read module |
| `runtime_protocol/timeline_view.py` | 214 | 214 | 0 | full handwritten Timeline Read/See module |
| `runtime_protocol/visual_boundary.py` | 228 | 228 | 0 | full handwritten Timeline See module |
| `runtime_protocol/visual_seam.py` | 465 | 471 | +6 | full handwritten Timeline See/projector module |
| **selected Timeline-core total** | **5,710** | **9,620** | **+3,910** | |

The current additions are visible as the handwritten commit/capture modules;
the selected shared-code delta also records the current retirement of old
direct timeline writers and the current Runtime route/service changes.

### AST method manifest for mixed files

The following exact method names are the shared-file manifest. Each name is
resolved in the indicated class at each source revision; a missing name at the
main baseline contributes zero. The count is the AST node's inclusive source
range, not a guessed percentage of its containing file.

`runtime_protocol/server.py`, class `RuntimeHandler`:

```text
_project_mutation_body, _timeline_options, _commit_body, _restore_body,
_commit_idempotency_key, _authorize_timeline_commit, _authorize_timeline_read,
_timeline_path, _timeline_commit, _is_timeline_commit, _route
```

The baseline has only `_project_mutation_body`, `_timeline_options`, and
`_route`; current-only names are skipped at the baseline.

`runtime_protocol/store.py`, class `RealmStore`:

```text
_project_output_timeline, timeline_render_publication,
prepare_timeline_render_publication, complete_timeline_render_publication,
_append_timeline_event
```

`runtime_protocol/service.py`, class `RuntimeService`:

```text
_project_resource, _timeline_resource, _timeline_public_resource,
_legacy_timeline_payload, _record_legacy_timeline_revision,
_record_internal_revision, _shot_revision_payload, _record_legacy_shot_revision,
_validate_published_shot_payload, _validate_published_text_bindings,
_apply_published_shot_projection, _shot_projection_matches_revision,
_verify_shot_head_projection, _record_timeline_revision, _timeline_revision,
_verified_source_media, _authored_clip_interval, _require_timeline_command,
update_timeline, replace_timeline_clip, _timeline_name, rename_timeline,
create_timeline, _adopt_empty_shell_create, create_timeline_document,
list_timelines, _shot_resource, _reference_resource,
_publication_replay_result, committed_receipt, _open_publication_directory,
_begin_cas_publication_journal, _remove_publication_journal_at,
_publication_committed, _recover_cas_publication_journals, _revision_digest,
_revision_id, _revision_payload, _complete_internal_timeline_payload,
_validate_timeline_track_roles, _complete_shot_payload, _complete_parent_payload,
get_project_shot_revision, get_project_timeline_revision, get_project_timeline,
get_project_parent_composition_revision,
list_project_parent_composition_revisions,
restore_project_parent_composition_revision, inspect_timeline,
create_timeline_view, replace_parent_composition_media, _finite_number,
_normalize_occurrence, _validate_media_dependencies, _collect_digest_media,
publish_parent_composition, list_timeline_history, _diff_items, diff_timeline,
archive_timeline, recover_timeline, publish_timeline_render,
register_timeline_commit_provider, _timeline_commits, _timeline_authorize,
commit_timeline, _execute_timeline_commit, _ensure_timeline_commit_baseline,
list_timeline_commits, get_project_media_selection, get_project_verified_media,
get_project_verified_document_object, get_project_verified_document
```

The `server._route`, selected service replay/publication helpers, and selected
store projector helpers are shared with non-Timeline concerns inside one AST
node. Their complete node ranges are retained so the result is reproducible;
their generic portions are an explicit allocation uncertainty, not silently
reported as Timeline-only precision. Dedicated modules have no such mixed-file
allocation. This is why the total is a rough guide and must not be used as a
threshold or a deletion instruction.

The module-level non-AST ranges are also explicit:

```text
origin/main canonical_schema.py: 112-124, 153-165, 276-290, 322-388, 403-415
tl/integration canonical_schema.py: 12-27, 131-144, 172-184, 295-309,
  341-408, 424-436
origin/main cli.py: 124-139, 181-201
tl/integration cli.py: 125-140, 182-202
```

### Reproduction

The source identity and per-file whole-blob context can be reproduced without
checking out either ref:

```sh
git show -s --format='%H %T' origin/main
git show -s --format='%H %T' tl/integration
git show tl/integration:runtime_protocol/service.py | wc -l
```

For the selected total, parse each `git show REV:path` blob with Python's
`ast.parse`, resolve the exact class/method names above, sum inclusive
`lineno..end_lineno` ranges after unioning overlaps, and add the full-line
counts for the dedicated-module paths in the table. This produced **5,710 →
9,620 (+3,910)**. Re-running that procedure against the two exact commits is
the intended final-M4 refresh method.

## Whole-file context only

These figures are deliberately not the census: they show why the old document
was misleading. Counting the same authored path family as complete blobs gives
**19,917** lines at `origin/main` and **23,769** at `tl/integration` (**+3,852**),
including generic worker/execution and other unrelated code in the mixed
files. They must not be compared with the selected Timeline-core total or used
as a target.

## Exclusions and evidence status

- `runtime_protocol/local_*`, `remote_worker_*`, `verified_host_launch.py`,
  `astrid_runtime/`, and generic auth/backup/CAS/platform/lifecycle paths are
  outside the Timeline Read/See/Edit boundary.
- Contract/OpenAPI schemas, `runtime_protocol/timeline_commit_types.py`,
  generated clients/metadata, conformance output, tests, fixtures, archives,
  and package data are excluded even when Timeline-named.
- Project-shot/reference catalog CRUD and generic media/catalog/task execution
  code are not counted as Timeline core; only the selected projection,
  publication, history, commit, and Timeline route ranges are included.
- This refresh changed no product repository, test, dependency, cache, branch,
  or ref. No test or full suite was run by this docs-only worker.
- This document makes no architecture-complete or delivery-complete claim.
