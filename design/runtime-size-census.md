# Runtime Timeline-core size census

Status: **current Main baseline/core census; rough guide only**. This is an
honest source count, not a threshold, deletion instruction, or M4 gate. It
uses the PLAN boundary: authored Runtime code for Timeline Read/See/Edit,
limited to command acceptance, commit/history, projection, capture, and
compiler-facing adapters. Untouched Main infrastructure is not counted.

## Source pins

| scope | commit | tree | source used |
|---|---|---|---|
| Main baseline | `b535646faaad2f8ae7968dfe0f4fa3057f960264` | `76613f05f9c7da7bcd555d972cf685d59b7501b9` | `origin/main` |
| current candidate | `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c` | `d3a290b407fa61e6ab2d476f50c068073f70df00` | assigned current tree |

The current candidate is the requested `95bd` tree. Its post-`4dd6438`
unplaced project-shot catalog restoration is Main catalog infrastructure and
is excluded except for the separately approved Timeline authority guard noted
below. The included Timeline fragments do not change between `4dd6438` and
`95bd`; this is a remeasurement at the current pin, not a claim that every
current-source line is Timeline product code.

## Counts

Physical counts include blank lines. Nonblank counts include a line iff
`line.strip()` is nonempty. A `full` row counts the committed blob; a mixed
file counts only the named functions or explicit ranges in the manifest.

| path | Main b535 P/N | current 95bd P/N | delta P/N |
|---|---:|---:|---:|
| `runtime_protocol/canonical_schema.py` (Timeline SQL ranges) | 121 / 121 | 139 / 139 | +18 / +18 |
| `runtime_protocol/capture_validation.py` | 0 / 0 | 225 / 205 | +225 / +205 |
| `runtime_protocol/cli.py` (Timeline audit ranges) | 37 / 36 | 37 / 36 | 0 / 0 |
| `runtime_protocol/managed_render_snapshot.py` | 217 / 194 | 217 / 194 | 0 / 0 |
| `runtime_protocol/seam_intent.py` | 88 / 69 | 88 / 69 | 0 / 0 |
| `runtime_protocol/server.py` (selected Timeline handler methods) | 673 / 673 | 797 / 791 | +124 / +118 |
| `runtime_protocol/service.py` (selected Timeline service methods) | 1,942 / 1,920 | 1,681 / 1,675 | −261 / −245 |
| `runtime_protocol/shot_dependencies.py` | 155 / 131 | 155 / 131 | 0 / 0 |
| `runtime_protocol/snapshot_refs.py` | 224 / 202 | 278 / 246 | +54 / +44 |
| `runtime_protocol/store.py` (selected Timeline store methods) | 117 / 115 | 117 / 115 | 0 / 0 |
| `runtime_protocol/timeline_catalog.py` | 0 / 0 | 98 / 90 | +98 / +90 |
| `runtime_protocol/timeline_commit.py` | 0 / 0 | 55 / 44 | +55 / +44 |
| `runtime_protocol/timeline_commit_baseline.py` | 0 / 0 | 440 / 394 | +440 / +394 |
| `runtime_protocol/timeline_commit_execution.py` | 0 / 0 | 115 / 102 | +115 / +102 |
| `runtime_protocol/timeline_commit_inputs.py` | 0 / 0 | 707 / 645 | +707 / +645 |
| `runtime_protocol/timeline_commit_port.py` | 0 / 0 | 941 / 852 | +941 / +852 |
| `runtime_protocol/timeline_commit_producer.py` | 0 / 0 | 285 / 254 | +285 / +254 |
| `runtime_protocol/timeline_commit_producer_checkpoint.py` | 0 / 0 | 163 / 147 | +163 / +147 |
| `runtime_protocol/timeline_commit_provider.py` | 0 / 0 | 93 / 77 | +93 / +77 |
| `runtime_protocol/timeline_commit_store.py` | 0 / 0 | 1,026 / 964 | +1,026 / +964 |
| `runtime_protocol/timeline_commit_validation.py` | 0 / 0 | 103 / 83 | +103 / +83 |
| `runtime_protocol/timeline_cutover.py` | 217 / 200 | 217 / 200 | 0 / 0 |
| `runtime_protocol/timeline_inspection.py` | 845 / 785 | 844 / 784 | −1 / −1 |
| `runtime_protocol/timeline_view.py` | 214 / 196 | 214 / 196 | 0 / 0 |
| `runtime_protocol/visual_boundary.py` | 228 / 203 | 228 / 203 | 0 / 0 |
| `runtime_protocol/visual_seam.py` | 465 / 428 | 471 / 432 | +6 / +4 |
| **measured Timeline scope** | **5,543 / 5,273** | **9,734 / 9,068** | **+4,191 / +3,795** |
| approved `service.py:_require_project_shot_scope` guard | — | 6 / 5 | +6 / +5 |
| **current approved scope** | **5,543 / 5,273** | **9,740 / 9,073** | **+4,197 / +3,800** |

The physical/nonblank pair is the useful guide. The negative `service.py`
delta is a consequence of counting selected AST fragments after refactors and
deletions; it is not evidence that Runtime product work was removed from the
repository as a whole. The size guide is not a gate, and no working feature
was rewritten to change these numbers.

## Exact inclusion manifest

The full-blob paths are exactly:

```text
runtime_protocol/capture_validation.py
runtime_protocol/managed_render_snapshot.py
runtime_protocol/seam_intent.py
runtime_protocol/shot_dependencies.py
runtime_protocol/snapshot_refs.py
runtime_protocol/visual_boundary.py
runtime_protocol/visual_seam.py
runtime_protocol/timeline_catalog.py
runtime_protocol/timeline_commit.py
runtime_protocol/timeline_commit_baseline.py
runtime_protocol/timeline_commit_execution.py
runtime_protocol/timeline_commit_inputs.py
runtime_protocol/timeline_commit_port.py
runtime_protocol/timeline_commit_producer.py
runtime_protocol/timeline_commit_producer_checkpoint.py
runtime_protocol/timeline_commit_provider.py
runtime_protocol/timeline_commit_store.py
runtime_protocol/timeline_commit_validation.py
runtime_protocol/timeline_cutover.py
runtime_protocol/timeline_inspection.py
runtime_protocol/timeline_view.py
```

The following shared-file fragments are included:

```text
server.py / RuntimeHandler:
_project_mutation_body, _timeline_options, _commit_body, _restore_body,
_commit_idempotency_key, _authorize_timeline_commit, _authorize_timeline_read,
_timeline_path, _timeline_commit, _is_timeline_commit, _route

store.py / RealmStore:
_project_output_timeline, timeline_render_publication,
prepare_timeline_render_publication, complete_timeline_render_publication,
_append_timeline_event

service.py / RuntimeService:
_project_resource, _timeline_resource, _timeline_public_resource,
_legacy_timeline_payload, _record_legacy_timeline_revision,
_record_internal_revision, _shot_revision_payload,
_record_legacy_shot_revision, _validate_published_shot_payload,
_validate_published_text_bindings, _apply_published_shot_projection,
_shot_projection_matches_revision, _verify_shot_head_projection,
_record_timeline_revision, _timeline_revision, _verified_source_media,
_authored_clip_interval, _require_timeline_command, update_timeline,
replace_timeline_clip, _timeline_name, rename_timeline, create_timeline,
_adopt_empty_shell_create, create_timeline_document, list_timelines,
_shot_resource, _reference_resource, _publication_replay_result,
committed_receipt, _open_publication_directory,
_begin_cas_publication_journal, _remove_publication_journal_at,
_publication_committed, _recover_cas_publication_journals, _revision_digest,
_revision_id, _revision_payload, _complete_internal_timeline_payload,
_validate_timeline_track_roles, _complete_shot_payload,
_complete_parent_payload, get_project_shot_revision,
get_project_timeline_revision, get_project_timeline,
get_project_parent_composition_revision,
list_project_parent_composition_revisions,
restore_project_parent_composition_revision, inspect_timeline,
create_timeline_view, replace_parent_composition_media, _finite_number,
_normalize_occurrence, _validate_media_dependencies, _collect_digest_media,
publish_parent_composition, list_timeline_history, _diff_items, diff_timeline,
archive_timeline, recover_timeline, register_timeline_commit_provider,
_timeline_commits, _timeline_authorize, commit_timeline,
_execute_timeline_commit, _ensure_timeline_commit_baseline,
list_timeline_commits, get_project_media_selection, get_project_verified_media,
get_project_verified_document_object, get_project_verified_document
```

Revision-specific explicit ranges are:

```text
b535646:
  canonical_schema.py 112-124, 153-165, 276-290, 322-388, 403-415
  cli.py              124-139, 181-201
95bd3c5:
  canonical_schema.py 12-27, 131-144, 172-184, 295-309, 341-408, 424-436
  cli.py              125-140, 182-202
approved authority add-on:
  service.py:_require_project_shot_scope, inclusive function body (6/5)
```

`runtime_protocol/timeline_commit_types.py` is excluded as generated/client
type material. Contracts and schemas, generated Python/TypeScript clients and
metadata, tests, fixtures, package data, `astrid_runtime/`, and untouched Main
worker/execution, custody, lifecycle, and platform infrastructure are also
excluded.

The current `95bd` tree contains restored unplaced project-shot catalog CRUD
in `service.py` and its tests. Those methods are Main catalog infrastructure,
not Timeline command/commit/history product, and are deliberately absent from
the selected `service.py` AST manifest. Only `_require_project_shot_scope` is
counted because it is the separately approved Timeline authority guard.

## Reproduction

From this repository, the arithmetic is reproducible without checking out a
revision: read each blob with `git show REV:path`, parse Python with `ast`,
count the inclusive `lineno..end_lineno` ranges for the manifest above, union
overlaps, and count physical/nonblank lines. The resulting totals are:

```text
Main b535646:  5,543 physical / 5,273 nonblank
current 95bd:  9,734 physical / 9,068 nonblank
approved add-on:                 +6 physical / +5 nonblank
current approved: 9,740 physical / 9,073 nonblank
delta:             +4,197 physical / +3,800 nonblank
```

This is source/blob arithmetic only. No product, test, generated artifact, or
full/render/browser suite is implied by the count.
