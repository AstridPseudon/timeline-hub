# agt-m2-occurrence-delete — candidate, integration HELD

Implemented closed `occurrence.delete` v1 on base
`a31d712d4a5c9ad08f385e12d71d3f1f7cbfef83`. Read PLAN, the actual App
`useClipEditing.test.ts` whole-group positive, app-writers, group ownership,
and migration/real-source reports. No settled decisions were changed.

## Changes and contract

- `native_occurrence_delete.capture_occurrence_delete(bundle, owner)` seals one
  explicit `occurrence:<raw ID>` command using native execute. Empty closed args;
  intent is exactly `ownership: occurrence`. No display-ID or shot/lane inference.
- Native records clear exactly one placement root, retain its complete original
  object, bind its owner, and guard its own child/track membership/order and full
  source content. Unrelated occurrence collections are never selected or written.
  Nonempty legacy `config.pinnedShotGroups` refuses `migration_needed`.
- The shared inverse now recovers missing immutable shot/compiler inputs from
  authenticated accepted boundaries and restores placement order relative to
  surviving historical rows. It also restores original placement compiler
  baselines, preserving existing nonliteral source maps exactly. Record-only
  inverse without accepted boundaries refuses when original occurrence order is
  needed. No snapshot replacement, source-content deletion, physical row purge,
  media pruning, history pruning, new DTO/ABI/table, or allocation framework.
- Fixed a concrete generic root-guard failure: after deleting one of two shared
  occurrences, reload changes the survivor's compiler shot/item aliases. The
  other captured delete now rebases using only the exact source/main-generated
  occurrence alias pair and verified item_id_map. Full occurrence metadata stays
  guarded; different-source, same-ID and ABA publications still refuse.
- Added the read-only `occurrence:<id>/shot` path `["payload"]` view for exact
  authored source capture. Main's existing known-item-reference codec reverses
  verified item aliases and removes only the derived internal revision link;
  opaque metadata is preserved. Raw internal content uses the existing `/source`
  view. Existing command/schema definitions and M1/scalar goldens are unchanged.
- Added native portable golden plus recipe/provider tests. The original App
  fixture's two hold clips (0/5 seconds, hold 5, V1) map to one canonical group
  occurrence; deletion leaves its V1 lane empty and registry intact. This is a
  canonical-boundary fixture, not proof that the separate migration or App hook
  ran. No App files/assertions/staging were edited.

Shared coordination contract (automatic hub design mirror):
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/m2-occurrence-delete.md`.
Published during implementation for the independent group migration worker/App;
no shared worker WIP was edited. Final capture/golden SHA-256 values there replace
initial candidate values. Schema SHA-256 is
`08640f6fd9abd33ee00c5e5f5a4048c0fe66ab3889b1e1e7cf14537b1ba718e2`.
Golden SHA-256 is
`7314e537de01867fc5a4183a45e091d4b9b9f5138805802e3a697b5d44868d9f`.
This schema is a LATER group-source candidate; no frozen Bundle 2 ref/schema
release, Runtime lock, or generated client was updated.

## Final evidence

From `/home/user/work/wt/agt-m2-occurrence-delete`:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider --tb=short \
  tests/editing_conformance/test_recipe_occurrence_delete.py \
  tests/editing_conformance/test_recorded_graph_roots.py \
  tests/editing_conformance/test_recipe_m1_commands.py \
  tests/editing_conformance/test_recipe_clip_delete.py \
  tests/editing_conformance/test_recipe_add_delete_composition.py \
  tests/editing_conformance/test_recipe_internal_stages.py \
  tests/editing_conformance/test_recipe_occurrence_media.py \
  tests/editing_conformance/test_occurrence_media_manifest_inverse.py \
  tests/editing_conformance/test_recipe_scalar_commands.py \
  tests/editing_conformance/test_recipe_clip_scalar_fields.py \
  tests/sdk/test_timeline_occurrence_delete_provider.py \
  tests/sdk/test_timeline_commit_graph_roots.py \
  tests/sdk/test_timeline_commit_provider.py \
  tests/sdk/test_timeline_commit_provider_document.py \
  tests/timeline/test_authoring_bundle.py
```

**743 passed, 1 deselected in 78.97s; exit 0.** The deselected test is an existing
lane-marked neighbor under default pytest configuration. No new skip/xfail or
changed original expectation. Tests prove first/middle/last/sole occurrence
reload, exact authored metadata/order and immutable images on undo/redo, shared
content isolation, grouped and independent deletes, the two-shared-to-last
materialization case, source/membership/opaque changes refusing atomically,
equal-state/ABA publication refusal, and retired-ID reservation with trusted
same-ID inverse restoration.

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m ruff check --no-cache \
  astrid/sdk/timeline/native_occurrence_delete.py astrid/sdk/timeline/_root_inverse.py \
  astrid/sdk/timeline/_command_state.py astrid/sdk/timeline/inverse.py \
  astrid/sdk/timeline/commands.py astrid/sdk/timeline/commit.py \
  tests/editing_conformance/test_recipe_occurrence_delete.py \
  tests/sdk/test_timeline_occurrence_delete_provider.py

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m mypy --follow-imports=skip \
  --cache-dir=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-occurrence-delete/mypy-cache \
  astrid/sdk/timeline/native_occurrence_delete.py astrid/sdk/timeline/_root_inverse.py \
  astrid/sdk/timeline/_command_state.py astrid/sdk/timeline/inverse.py \
  astrid/sdk/timeline/commands.py astrid/sdk/timeline/commit.py

git diff --check
```

All pass; mypy checks six source files. The temporary mypy cache was removed.
An initial `--follow-imports=silent` attempt stopped on NumPy's Python-3.12 type
syntax under the repository's Python-3.11 target; `skip` is the repository's
configured import policy. A read-only JSON comparison against HEAD also verified
all original schema definitions (except additive EditCommand dispatch) and all
original dispatch entries are preserved.

Intermediate runs exposed and corrected the new root/member predicate error and
then the existing two-shared-occurrence alias refusal. Their positive tests remain
in the final passing suite. The final command above is on the final product tree.

## Size, limits, next steps

The new operation/capture is **31 lines**. Product Python diff is **182 added /
10 removed (net +172)**, plus **40 closed schema lines**. This exceeds the 80-line
target because the shared root primitive lacked exact order restoration,
last-consumer source/baseline recovery, and stable root aliases across normal
compiler materialization. The 93-line `_root_inverse.py` uses existing
AcceptedRecords/boundaries and ordered root writes; it does not introduce a
second history or editing framework. Tests and the portable golden are separate.

No full suite, make check, installation, socket/browser run, actual Runtime
acceptance/source probe, renderer test, commit, merge or push was run. Provider
proof uses the existing detached native-provider test port and fake ABI metadata;
it is not Runtime durability/idempotency/restart or App acceptance evidence.
No App shot-delete writer was retired and no all-group-gestures claim is made.

Compose this bounded registry/schema delta with the independent migration worker
in the later group bundle, review the generic-root changes together, then obtain
normal Runtime generation/consumer pins and real canonical migration → delete →
accepted reload → guarded inverse/redo proof. App must consume explicit canonical
bindings and keep its original positive assertions. Retire its old shot-delete
writer only after that actual native proof. All M2 integration stays HELD until
PLAN's M1 gate record permits it.
