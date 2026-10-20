# Runtime Timeline-core size census

Pinned for M4 on 2026-10-20. This is a rough-guide measurement, not a gate or
a target to optimize against. It follows PLAN's settled boundary: authored
Runtime product code implementing Timeline Read/See/Edit. It excludes untouched
worker/execution/catalog/custody infrastructure, generated contracts/clients,
tests, fixtures, and package data.

## Exact source revisions

The current-integration measurement is pinned to the task's assigned base,
`cc3796a`; the mutable `tl/integration` ref advanced while this census was in
progress and is deliberately not used as an input. The private `a6a` candidate
is measured separately and was not merged.

| label | commit | tree | commit date |
|---|---|---|---|
| main baseline (`origin/main`) | `240d5bb202af709294551045554012f079fd06ca` | `2e77d0df220885e978c5fbdf5d6072292ac07284` | `2026-10-20T17:31:38+02:00` |
| current integration snapshot | `cc3796a0c333b956b171c68dc876d41f40f6219f` | `18e037810a8b61551c23fc33e5639775b7da8623` | `2026-10-20T17:58:50+00:00` |
| private `a6a` snapshot (not merged) | `a6a11a806a51262192447fdeccc726b01ffd78fb` | `8c027992e34ddf9a940d3e90cd38f7b9e11e4c25` | `2026-10-20T17:53:10+00:00` |

## Boundary and method

Counts are committed-blob physical source lines (`splitlines`, blank lines
included), with one manifest applied to all three revisions. For mixed files,
the manifest selects named top-level AST methods and counts each selected node's
inclusive `lineno..end_lineno` range. Overlapping ranges are unioned. This
keeps whole `service.py`, `store.py`, and `server.py` totals from being
presented as Timeline code.

Single-purpose handwritten Timeline modules are counted in full. The private
`runtime_protocol/timeline_materialization.py` module is included because it is
authored source-bound Edit-path product code; it is zero in main and current.
The generated `runtime_protocol/timeline_commit_types.py`,
`runtime_protocol/schemas/timeline-commit-bundle.json`, contract schemas,
generated Python/TypeScript clients and metadata, and all tests/fixtures are
excluded.

### Selected-range census

| path | main | current `cc3796a` | delta | private `a6a` | delta | selection |
|---|---:|---:|---:|---:|---:|---|
| `runtime_protocol/canonical_schema.py` | 121 | 139 | +18 | 139 | +18 | explicit Timeline SQL ranges; current commit schema included |
| `runtime_protocol/cli.py` | 37 | 37 | 0 | 37 | 0 | `audit-timelines` parser/handler ranges |
| `runtime_protocol/server.py` | 670 | 794 | +124 | 794 | +124 | selected `RuntimeHandler` helpers, commit routing, and `_route` |
| `runtime_protocol/service.py` | 2,112 | 1,729 | −383 | 1,729 | −383 | selected `RuntimeService` Timeline/commit/projection/view methods |
| `runtime_protocol/store.py` | 117 | 117 | 0 | 117 | 0 | selected Timeline projector/publication/event methods |
| `runtime_protocol/capture_validation.py` | 0 | 225 | +225 | 225 | +225 | full handwritten capture module |
| `runtime_protocol/managed_render_snapshot.py` | 217 | 217 | 0 | 217 | 0 | full handwritten Timeline See module |
| `runtime_protocol/seam_intent.py` | 88 | 88 | 0 | 88 | 0 | full handwritten Timeline See module |
| `runtime_protocol/shot_dependencies.py` | 155 | 155 | 0 | 155 | 0 | full handwritten Timeline See module |
| `runtime_protocol/snapshot_refs.py` | 224 | 278 | +54 | 278 | +54 | full handwritten Timeline snapshot/projector module |
| `runtime_protocol/timeline_commit.py` | 0 | 55 | +55 | 59 | +59 | full handwritten commit module |
| `runtime_protocol/timeline_commit_baseline.py` | 0 | 441 | +441 | 441 | +441 | full handwritten commit module |
| `runtime_protocol/timeline_commit_execution.py` | 0 | 115 | +115 | 115 | +115 | full handwritten commit module |
| `runtime_protocol/timeline_commit_inputs.py` | 0 | 707 | +707 | 707 | +707 | full handwritten commit module |
| `runtime_protocol/timeline_commit_port.py` | 0 | 941 | +941 | 1,041 | +1,041 | full handwritten commit port |
| `runtime_protocol/timeline_commit_producer.py` | 0 | 285 | +285 | 285 | +285 | full handwritten producer module |
| `runtime_protocol/timeline_commit_producer_checkpoint.py` | 0 | 163 | +163 | 163 | +163 | full handwritten producer module |
| `runtime_protocol/timeline_commit_provider.py` | 0 | 93 | +93 | 93 | +93 | full handwritten provider module |
| `runtime_protocol/timeline_commit_store.py` | 0 | 1,008 | +1,008 | 1,184 | +1,184 | full handwritten commit store |
| `runtime_protocol/timeline_commit_validation.py` | 0 | 103 | +103 | 103 | +103 | full handwritten validation module |
| `runtime_protocol/timeline_cutover.py` | 217 | 217 | 0 | 217 | 0 | full handwritten Timeline audit module |
| `runtime_protocol/timeline_inspection.py` | 845 | 844 | −1 | 844 | −1 | full handwritten Timeline Read module |
| `runtime_protocol/timeline_view.py` | 214 | 214 | 0 | 214 | 0 | full handwritten Timeline Read/See module |
| `runtime_protocol/visual_boundary.py` | 228 | 228 | 0 | 228 | 0 | full handwritten Timeline See module |
| `runtime_protocol/visual_seam.py` | 465 | 471 | +6 | 471 | +6 | full handwritten Timeline See/projector module |
| `runtime_protocol/timeline_materialization.py` | 0 | 0 | 0 | 183 | +183 | full private handwritten source-bound materialization join |
| **selected Timeline-core total** | **5,710** | **9,664** | **+3,954** | **10,127** | **+4,417** | |

The current and private revisions share the same selected baseline product
surface except for the private source-bound candidate. Relative to current,
private `a6a` adds **+463 selected product lines**: `timeline_commit.py` +4,
`timeline_commit_port.py` +100, `timeline_commit_store.py` +176, and the new
`timeline_materialization.py` +183.

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
`_route`; current/private-only names are skipped at the baseline.

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

`server._route`, selected service replay/publication helpers, and selected
store projector helpers are shared with non-Timeline concerns inside one AST
node. Their complete node ranges are retained so the result is reproducible;
their generic portions are an explicit allocation uncertainty, not silently
reported as Timeline-only precision. Dedicated modules have no such mixed-file
allocation. This is why the total is a rough guide and must not be used as a
threshold or a deletion instruction.

The module-level non-AST ranges are also explicit:

```text
origin/main canonical_schema.py: 112-124, 153-165, 276-290, 322-388, 403-415
current/private canonical_schema.py: 12-27, 131-144, 172-184, 295-309,
  341-408, 424-436
origin/main cli.py: 124-139, 181-201
current/private cli.py: 125-140, 182-202
```

## Private generator versus product delta

The complete `a6a`-versus-assigned-current diff is 35 files (+5,167/−683
physical lines), but only four handwritten product paths contribute the +463
selected-line delta above. The remaining changes are private generator source,
contract/schema data, generated Python/TypeScript clients and metadata, or
tests/fixtures. They are deliberately not counted as Runtime Timeline-core
product lines. In particular, a generated command union or its checked-in
schema is not evidence of additional authored Read/See/Edit implementation.

The private source-bound join is therefore reported twice only in the useful
sense: its handwritten Runtime implementation is counted in the private
product total, while its generated contract/client consequences remain outside
the total. `a6a` is a private qualification candidate, not current
integration, and this census makes no consumer-adoption or release claim.

## Existing post-D01 cuts and holds

These are already named Runtime ledger rows, recorded here for size context;
they are not new deletion proposals and this documentation task performs none
of them. See
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/deletion-ledger.runtime.md`.

| ledger row | existing named cut/hold | current decision boundary |
|---|---|---|
| `D04` | legacy canonical timeline publication bodies | held until both App D01 and Agent whole-candidate/`clip.set-element` migration qualify; no speculative removal here |
| `D13` / `RT07` | producer-uncustodied render admission and the legacy `publish_timeline_render` direct writer | authority primitives are merged, but the registered replacement remains open; cut only after accepted proposal/custody, duplicate-CAS, lost-ACK/restart, and revision-pinned proof |
| `RT08` | blanket identity-only `id_map` admission / missing source-bound allocation join | open/held current cohort; private `a6a` is the separately measured candidate, not an integrated cut |
| `WC10` | restored `publish_parent_composition` route | held until its named `remote.create_empty`, `reference_realm.py`, and `shot_composition_migration.py` consumers migrate |

`RT06` commit-path deduplication is already recorded as merged, not an
additional post-D01 size claim. No threshold, target, gate, or ledger status is
changed by this census.

## Reproduction

Pin identities without checking out either revision:

```sh
for rev in \
  240d5bb202af709294551045554012f079fd06ca \
  cc3796a0c333b956b171c68dc876d41f40f6219f \
  a6a11a806a51262192447fdeccc726b01ffd78fb
do
  git show -s --format='%H %T %cI' "$rev"
done
```

For the selected total, run Python's `ast.parse` on each
`git show REV:path` blob, resolve the exact class/method names in the manifest
above, sum inclusive `lineno..end_lineno` ranges after unioning overlaps, and
add `splitlines()` counts for the dedicated-module paths in the table. Apply
the explicit module-level ranges exactly as listed. The reproducible result is:

```text
                         main     current cc3796a     private a6a
selected Timeline core   5,710    9,664 (+3,954)      10,127 (+4,417)
```

The same committed path family counted as complete blobs, solely as context,
is 19,917 lines at main, 24,304 at current, and 24,767 at private. Those
whole-file figures include generic code inside mixed files and must not be
compared with the selected total or used as a target.

## Exclusions and evidence status

- `runtime_protocol/local_*`, `remote_worker_*`, `verified_host_launch.py`,
  `astrid_runtime/`, and generic auth/backup/CAS/platform/lifecycle paths are
  outside the Timeline Read/See/Edit boundary.
- Contract/OpenAPI schemas, generated clients/metadata,
  `runtime_protocol/timeline_commit_types.py`,
  `runtime_protocol/schemas/timeline-commit-bundle.json`, conformance output,
  tests, fixtures, archives, and package data are excluded even when
  Timeline-named.
- Project-shot/reference catalog CRUD and generic media/catalog/task execution
  code are not counted as Timeline core; only the selected projection,
  publication, history, commit, and Timeline route ranges are included.
- This refresh changed no product repository, dependency, cache, branch, or
  ref. No product tests or full suite were run; only read-only Git/blob and
  AST arithmetic was performed.
- This document makes no architecture-complete, delivery-complete, target-met,
  or gate-met claim. Known mixed-node allocation uncertainty and the exclusion
  of generated/test surfaces remain explicit omission bounds.
