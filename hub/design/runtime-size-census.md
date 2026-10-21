# Runtime Timeline-core size census

Status: **provisional, pre-adoption; not an M4-complete claim**. Refreshed
2026-10-21 against the published014/current Runtime source. This is an honest
source census, not a threshold, target, gate, or deletion instruction. It uses
the PLAN boundary: authored Runtime code for Timeline Read/See/Edit, limited to
acceptance, history, projection, capture, and Timeline adapters.

## Source pins

| scope | commit | tree | source used |
|---|---|---|---|
| Main baseline | `b535646faaad2f8ae7968dfe0f4fa3057f960264` | `76613f05f9c7da7bcd555d972cf685d59b7501b9` | `origin/main` |
| published014/current | `b92d3e7a05eec65c142294ef4873edd059e9b31d` | `6abc2f117391de8e7e35c0283f575a002199894d` | `tl/integration` / published014 current tree; commit date `2026-10-21 03:48:20 +0000` |
| approved catalog add-on | `c81c0eb5aed4fa6b5cd23705aa84dfdf2b9922ed` | `9504b7b62574866bdfee45e4e159943f508152a9` | only the authority guard below |

The Main baseline is `b535646` (tree `76613f05f9c7da7bcd555d972cf685d59b7501b9`,
commit date `2026-10-20 15:41:28 +0000`). `c81c0eb` (commit date
`2026-10-20 22:39:01 +0000`) is an ancestor of the current merge, but its
restored catalog/Main infrastructure is not Timeline core and is therefore not
folded into the current total. Only its separately approved Timeline authority
guard is reported as an additive current-scope row.

## Counts

Physical counts include blank lines. Nonblank counts include a line iff
`line.strip()` is nonempty. A `full` row counts the committed blob; a mixed
file counts only the named fragments in the manifest below.

| path | baseline P/N | current `b92d3e7` P/N | delta P/N |
|---|---:|---:|---:|
| `runtime_protocol/capture_validation.py` | 0 / 0 | 225 / 205 | +225 / +205 |
| `runtime_protocol/managed_render_snapshot.py` | 217 / 194 | 217 / 194 | 0 / 0 |
| `runtime_protocol/seam_intent.py` | 88 / 69 | 88 / 69 | 0 / 0 |
| `runtime_protocol/shot_dependencies.py` | 155 / 131 | 155 / 131 | 0 / 0 |
| `runtime_protocol/snapshot_refs.py` | 224 / 202 | 278 / 246 | +54 / +44 |
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
| `runtime_protocol/timeline_inspection.py` | 845 / 785 | 846 / 786 | +1 / +1 |
| `runtime_protocol/timeline_view.py` | 214 / 196 | 214 / 196 | 0 / 0 |
| `runtime_protocol/visual_boundary.py` | 228 / 203 | 228 / 203 | 0 / 0 |
| `runtime_protocol/visual_seam.py` | 465 / 428 | 484 / 442 | +19 / +14 |
| `runtime_protocol/server.py` (selected AST methods) | 673 / 673 | 797 / 791 | +124 / +118 |
| `runtime_protocol/store.py` (selected AST methods) | 117 / 115 | 117 / 115 | 0 / 0 |
| `runtime_protocol/service.py` (selected AST methods) | 1,942 / 1,920 | 1,681 / 1,675 | −261 / −245 |
| `runtime_protocol/canonical_schema.py` (Timeline SQL ranges) | 121 / 121 | 139 / 139 | +18 / +18 |
| `runtime_protocol/cli.py` (Timeline audit ranges) | 37 / 36 | 37 / 36 | 0 / 0 |
| **measured Timeline scope** | **5,543 / 5,273** | **9,749 / 9,080** | **+4,206 / +3,807** |
| `service.py:_require_project_shot_scope` from approved `c81c0eb` | — | 6 / 5 | +6 / +5 |
| **current approved-scope total** | **5,543 / 5,273** | **9,755 / 9,085** | **+4,212 / +3,812** |

The additive catalog guard is the only `c81c0eb` code counted. Its call-site
changes and the restored catalog/Main service, lifecycle, worker, execution,
custody, and platform infrastructure remain excluded.

The current count is only 15 physical / 12 nonblank lines above the prior
`95bd3c5` measurement under this same manifest: the selected rational-FPS
visual seam and fraction parsing fragments account for that small change. The
narrow launcher change is in excluded `astrid_runtime/` infrastructure. The
Speech duration change is in an unselected `RealmStore` method, so the shared
`store.py` file is not counted wholesale. Staged/private `f53bf58`, `449d13d`,
and `c3d2656` sources are not ancestors of `b92d3e7` and are excluded from the
current source count.

## Exact manifest

The full-blob paths are exactly the 21 dedicated paths in the first 21 rows
above. `runtime_protocol/timeline_commit_types.py`, contracts, generated
clients/metadata, tests, fixtures, package data, `astrid_runtime/`, and
untouched Main worker/execution infrastructure are excluded.

Mixed-file AST fragments:

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
_record_internal_revision, _shot_revision_payload, _record_legacy_shot_revision,
_validate_published_shot_payload, _validate_published_text_bindings,
_apply_published_shot_projection, _shot_projection_matches_revision,
_verify_shot_head_projection, _record_timeline_revision, _timeline_revision,
_verified_source_media, _authored_clip_interval, _require_timeline_command,
update_timeline, replace_timeline_clip, _timeline_name, rename_timeline,
create_timeline, _adopt_empty_shell_create, create_timeline_document,
list_timelines, _shot_resource, _reference_resource, _publication_replay_result,
committed_receipt, _open_publication_directory, _begin_cas_publication_journal,
_remove_publication_journal_at, _publication_committed,
_recover_cas_publication_journals, _revision_digest, _revision_id,
_revision_payload, _complete_internal_timeline_payload,
_validate_timeline_track_roles, _complete_shot_payload, _complete_parent_payload,
get_project_shot_revision, get_project_timeline_revision, get_project_timeline,
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

Revision-specific non-AST ranges:

```text
b535646:
  canonical_schema.py 112-124, 153-165, 276-290, 322-388, 403-415
  cli.py              124-139, 181-201
b92d3e7:
  canonical_schema.py 12-27, 131-144, 172-184, 295-309, 341-408, 424-436
  cli.py              125-140, 182-202
c81c0eb add-on:
  service.py:_require_project_shot_scope, inclusive function body (6/5)
```

Counting command, run from this Runtime checkout without checking out a
revision: use `git show REV:path`, parse Python with `ast.parse`, resolve the
class/method names above, count each selected node's inclusive
`lineno..end_lineno` range, union overlapping ranges, and add the full-blob
and explicit-range counts. This is the reproducible arithmetic command:

```sh
python - <<'PY'
import ast, subprocess

REV = {"baseline": "b535646", "current": "b92d3e7"}
FULL = {"runtime_protocol/capture_validation.py", "runtime_protocol/managed_render_snapshot.py",
        "runtime_protocol/seam_intent.py", "runtime_protocol/shot_dependencies.py",
        "runtime_protocol/snapshot_refs.py", "runtime_protocol/visual_boundary.py",
        "runtime_protocol/visual_seam.py", "runtime_protocol/timeline_catalog.py",
        "runtime_protocol/timeline_commit.py", "runtime_protocol/timeline_commit_baseline.py",
        "runtime_protocol/timeline_commit_execution.py", "runtime_protocol/timeline_commit_inputs.py",
        "runtime_protocol/timeline_commit_port.py", "runtime_protocol/timeline_commit_producer.py",
        "runtime_protocol/timeline_commit_producer_checkpoint.py", "runtime_protocol/timeline_commit_provider.py",
        "runtime_protocol/timeline_commit_store.py", "runtime_protocol/timeline_commit_validation.py",
        "runtime_protocol/timeline_cutover.py", "runtime_protocol/timeline_inspection.py",
        "runtime_protocol/timeline_view.py"}
MIX = {
 "runtime_protocol/server.py": ("RuntimeHandler", "_project_mutation_body _timeline_options _commit_body _restore_body _commit_idempotency_key _authorize_timeline_commit _authorize_timeline_read _timeline_path _timeline_commit _is_timeline_commit _route"),
 "runtime_protocol/store.py": ("RealmStore", "_project_output_timeline timeline_render_publication prepare_timeline_render_publication complete_timeline_render_publication _append_timeline_event"),
 "runtime_protocol/service.py": ("RuntimeService", "_project_resource _timeline_resource _timeline_public_resource _legacy_timeline_payload _record_legacy_timeline_revision _record_internal_revision _shot_revision_payload _record_legacy_shot_revision _validate_published_shot_payload _validate_published_text_bindings _apply_published_shot_projection _shot_projection_matches_revision _verify_shot_head_projection _record_timeline_revision _timeline_revision _verified_source_media _authored_clip_interval _require_timeline_command update_timeline replace_timeline_clip _timeline_name rename_timeline create_timeline _adopt_empty_shell_create create_timeline_document list_timelines _shot_resource _reference_resource _publication_replay_result committed_receipt _open_publication_directory _begin_cas_publication_journal _remove_publication_journal_at _publication_committed _recover_cas_publication_journals _revision_digest _revision_id _revision_payload _complete_internal_timeline_payload _validate_timeline_track_roles _complete_shot_payload _complete_parent_payload get_project_shot_revision get_project_timeline_revision get_project_timeline get_project_parent_composition_revision list_project_parent_composition_revisions restore_project_parent_composition_revision inspect_timeline create_timeline_view replace_parent_composition_media _finite_number _normalize_occurrence _validate_media_dependencies _collect_digest_media publish_parent_composition list_timeline_history _diff_items diff_timeline archive_timeline recover_timeline register_timeline_commit_provider _timeline_commits _timeline_authorize commit_timeline _execute_timeline_commit _ensure_timeline_commit_baseline list_timeline_commits get_project_media_selection get_project_verified_media get_project_verified_document_object get_project_verified_document")}
RANGES = {"b535646": {"runtime_protocol/canonical_schema.py": [(112,124),(153,165),(276,290),(322,388),(403,415)], "runtime_protocol/cli.py": [(124,139),(181,201)]}, "b92d3e7": {"runtime_protocol/canonical_schema.py": [(12,27),(131,144),(172,184),(295,309),(341,408),(424,436)], "runtime_protocol/cli.py": [(125,140),(182,202)]}}
def show(rev, path):
    try: return subprocess.check_output(["git", "show", f"{rev}:{path}"], text=True, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError: return None
def count(rev, path):
    text = show(rev, path)
    if text is None: return (0, 0)
    lines = set(range(1, len(text.splitlines()) + 1))
    if path in MIX:
        lines = set()
        tree = ast.parse(text); cls, names = MIX[path]; names = set(names.split())
        owner = next(n for n in ast.walk(tree) if isinstance(n, ast.ClassDef) and n.name == cls)
        for node in owner.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name in names:
                lines.update(range(node.lineno, node.end_lineno + 1))
    elif path in RANGES[rev]:
        lines = {n for a,b in RANGES[rev][path] for n in range(a,b + 1)}
    raw = text.splitlines()
    return len(lines), sum(bool(raw[n - 1].strip()) for n in lines)
for label, rev in REV.items():
    total = tuple(sum(count(rev, p)[i] for p in FULL | set(MIX) | set(RANGES[rev])) for i in (0,1))
    print(label, total)
print("approved catalog add-on: 6 5; current approved: 9755 9085")
PY
```

No product files, tests, dependencies, caches, branches, or refs were
changed. No full or product suite was run; this task is source/blob arithmetic
only. The census remains provisional until the Runtime scope is adopted and
re-measured against the then-authoritative integration source.
