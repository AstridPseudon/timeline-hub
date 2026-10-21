# Agent M2 transition complete current-source composition

## Result

Prepared the complete future-source successor from approved PRIVATE017 consumer
`6c1989adf723ae0ea0f4205c1cc8f1c0e4b22e79`, using corrected transition source
`1acc64610019cd13e344a4a4d75e84280b8b7f16` and its ca9 provenance. This is
source only: no caller, Runtime/App worktree, pin, generation, freeze, or
release was changed.

The carrier remains the existing `clip.set`. It now supports guarded incoming
transition SET and paired transition/elementRef clear, with predecessor
selection, same-track adjacency, shortest-fit, authored-seconds, exact raw
reference presence/value, retained P1 authority, opaque/raw parameter
preservation, and visible object-to-null refusal. Main integer-frame conversion
remains at the caller; Agent seconds were not narrowed. Builtin cross-fade
descriptor IDs and authored seconds remain verbatim.

## Exact source/schema change matrix

| Path | Exact changed surface |
| --- | --- |
| `astrid/core/timeline/schema/edit-command.schema.json` | Existing `$defs.ClipSetArgs` only: transition value, `elementRef`, paired clear enum, `schema_source`; no new definition and no new operation clause. |
| `astrid/sdk/timeline/_clip_scalar_commands.py` | Existing `clip.set` capture/handler: transition SET, paired clear, presence/ref guards, parameter semantics, adjacency/fit checks. |
| `astrid/sdk/timeline/_recording.py` | Additive `transition.predecessor` selection. |
| `astrid/sdk/timeline/_collections.py` | Additive overlap guard for predecessor selection. |
| `astrid/sdk/timeline/_selected_param_authority.py` | Existing selected-source association extended to `clip.set`, preserving exact P1 authority. |
| `astrid/sdk/timeline/commit.py` | Existing hydrate/schema-resolver hooks extended for `clip.set` selected project-pack sources. |
| `tests/editing_conformance/test_recipe_clip_scalar_fields.py` | Compact adjacent-transition fixture adjustment. |
| `tests/sdk/test_timeline_transition_schema.py` | Direct transition SET/clear, presence, guard, parameter, and P1 tests. |
| `tests/sdk/test_timeline_materialization_schema_union.py` | Exact transition-stripping floor reconstruction and hash assertions. |

No later trim/delete/caption/position/effects/mixed-reorder/raw-init source was
included. No feature operation was added or removed; the existing `clip.set`
operation is the only operation whose behavior is extended.

## Identity and floor reconstruction

- Base commit/tree: `6c1989adf723ae0ea0f4205c1cc8f1c0e4b22e79` /
  `cc0a8dd1360324a1b440ba7d318a083e7f8814cc`.
- Provisional final worktree tree (harness will commit):
  `2a27ce39faa71fd0c111ad8db5678727bbee7b88`.
- Complete schema raw SHA-256:
  `95193e5a1f90a8072f55deb19f8b7ac63dc5054130c14eab097f0dd73f149729`.
- Complete schema canonical SHA-256 (`json.dumps(indent=2)+newline`):
  `8500046e82587856c16cd6e241f27c886f9089538884a0b806fa75138a57cb49`.
- Transition-stripped canonical SHA-256:
  `9f5612ff34a5758ecacae948d5c0bfb1acc867d6ecb7a6af037bf8e3974fd9d6`.
- Transition-stripped raw reference floor:
  `6dd2b082ebdb630b4fc8ec3eeeea3b40c1eebe910c84557e45ab8fab05322b16`.
- Transition-stripped inventory: **65 definitions / 37 `EditCommand.allOf`
  clauses**, exact ed5 canonical floor.
- Ordinary floor canonical SHA-256:
  `6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`.

The complete source schema has 65 definitions and 37 operation clauses. A
comparison with the approved base reports: definitions added `[]`, removed
`[]`, changed `['ClipSetArgs']`; operation clauses added `[]`, removed `[]`,
and reordered/changed `[]`.

## Current/protected blob matrix

The following current safety/non-feature blobs were verified unchanged from the
base (blob IDs shown):

| Blob | Base blob |
| --- | --- |
| `astrid/sdk/timeline_sheet.py` | `eec3f1f6c49bfd95139a5800b8e60d1bfd09d9ca` |
| `tests/sdk/test_timeline_sheet_native.py` | `69edb1e781aea40ed1024cf4375ecb4544f4aa6b` |
| `tests/editing_conformance/test_native_sheet_ordinary_runtime.py` | `04c4ff7e55a2d4d3d7a0ccc29be04916667ab0aa` |
| `tests/test_timeline_clip_replacement.py` | `d09d29a488283aa1e0f08467ff5ec23007f2063b` |
| `tests/sdk/test_timeline_sync.py` | `82b56b194387f5936ed972a1720c420c9372d9c6` |
| `tests/sdk/test_timeline_sync_native.py` | `da007e2e26db2e1d6289a187ae0dbbaf52f5d8d6` |

`runtime.lock.json`, `artifacts.json`, `cli-surface.json`, and the generated
client files (`astrid_runtime_client/{__init__,contract_metadata,generated,timeline_commit_types}.py`)
were not touched. Frozen ed5/42a lock/generated provenance therefore remains
outside this source-only feature diff. Theme fixture, dormant transcript result
metadata, WC8 parameter slice, and WC1 test packet are outside the changed
path set.

## Tests and checks

All commands used `PYTHONPATH="$PWD:/home/user/work/runtime"`, the shared
Agent venv, and no shared dependency writes.

- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/pytest -q -o addopts= -p no:cacheprovider tests/editing_conformance/test_recipe_clip_scalar_fields.py tests/sdk/test_timeline_clip_scalar_provider.py tests/editing_conformance/test_native_sheet_current_runtime.py` — **128 passed, 17 skipped**.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/pytest -q -o addopts= -p no:cacheprovider tests/sdk/test_timeline_transition_schema.py` — **12 passed**.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/pytest -q -o addopts= -p no:cacheprovider tests/sdk/test_timeline_transition_schema.py tests/editing_conformance/test_recipe_clip_scalar_fields.py -k 'transition or original_app_journey'` — **20 passed, 104 deselected**.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/pytest -q -o addopts= -p no:cacheprovider tests/sdk/test_timeline_materialization_schema_union.py` — **28 passed**.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/pytest -q -o addopts= -p no:cacheprovider tests/sdk/test_timeline_current_union_schema.py -k 'next_successor or current_candidate or operation_inventory or published_floors'` — **10 passed, 24 deselected**.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/pytest -q -o addopts= -p no:cacheprovider tests/editing_conformance/test_pristine_initialize.py -k 'schema'` — **1 passed, 21 deselected**.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/pytest -q -o addopts= -p no:cacheprovider tests/sdk/test_timeline_composed_schema.py tests/sdk/test_timeline_selected_schema.py tests/sdk/test_timeline_clip_scalar_provider.py tests/editing_conformance/test_native_sheet_current.py` — **90 passed**.
- Final rerun: `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/pytest -q -o addopts= -p no:cacheprovider tests/sdk/test_timeline_transition_schema.py tests/sdk/test_timeline_materialization_schema_union.py` — **40 passed**.
- Ruff on all changed Python files — **passed**.
- `python -m json.tool astrid/core/timeline/schema/edit-command.schema.json` — **passed**.
- `py_compile` on all changed Python files — **passed**.
- `git diff --check` — **passed**.

No full suite, native/HTTP/render/browser/install, live-caller, pin update, or
generation run was requested or performed.

## Blockers / next steps

No implementation blocker remains. Runtime/App should review the provisional
tree and the exact complete/stripped schema identities above for reciprocal
ACK. The harness should commit the worktree; the reported tree hash is the
pre-commit content tree and will remain the same after metadata-only commit
creation.
