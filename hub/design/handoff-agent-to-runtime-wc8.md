# Agent -> Runtime handoff: WC8 detached-sheet basis and target

Date: 2026-10-21 04:30 UTC  
Row: WC8  
Result: Runtime owns the server half of a future detached-sheet migration:
consume a batch whose original native basis, stable row intent/identity, and
Runtime target were retained before mutation, using the existing `/v1`
commit, server-side rebase, exact guards, durable requester flight, and
history/inverse. The current detached sheet is not yet eligible for that
route. Runtime must not invent a snapshot diff, client rebase, new DTO, or
replacement refusal.

## Exact base

Agent base used for this handoff: `5a625dd4c01149a085a9df85952b34cad70801f9`.
This is the worker `HEAD` and `refs/remotes/hub/tl/integration` at capture
time. The local `refs/heads/tl/integration` value `634060e09a3881708803587378477231c9f7eff4`
was stale and was not used.

## Boundary and permitted paths

The Agent-side evidence is deliberately read-only context:

- connected native basis/intent/target path:
  `astrid/sdk/timeline_sheet.py:603-846`,
  `astrid/sdk/timeline/sync.py:124-168,334-359`
- remaining detached caller:
  `astrid/packs/timeline/cli.py:3607-3612` ->
  `astrid/sdk/timeline_sheet.py:849-1085` ->
  `astrid/sdk/timeline/checkout.py:151-169`
- current native/legacy positive neighbors:
  `tests/sdk/test_timeline_sheet_native.py`,
  `tests/packs/timeline/test_cli_native_sheet.py`,
  `tests/sdk/test_timeline_sheet.py`, and
  `tests/packs/timeline/test_verbs_working_copy.py`

Runtime may work only in these Runtime-relative paths:

- the existing commit transport/acceptance seam in
  `runtime_protocol/timeline_commit_port.py` and its current provider-facing
  acceptance path; no new endpoint or DTO
- existing tests only, unless a bounded failing test proves a necessary
  server acceptance correction:
  `tests/test_timeline_commit_acceptance.py`,
  `tests/test_timeline_commit_execution.py`,
  `tests/test_timeline_commit_contract.py`, and
  `tests/test_timeline_current_union_contract.py`

Do not edit `astrid/sdk/timeline_sheet.py`, `checkout.py`, `cli.py`, or the
Agent provider from the Runtime worker. Do not touch WC10's native creator,
WC6's document-script landing, D13 origin security, raw OLD media swap, or
transcript/order work.

## Current gap and dependencies

The connected path already retains an exact revision/publication pair,
selection, native `# ref` bindings, opaque values, explicit clears, one
atomic `TimelineSession.commit_many` batch, and the exact persisted flight.
The detached path instead has only a whole-document `v` digest and optional
local `_exported` snapshots; it mutates a local Checkout through
`apply_sheet -> merge_sheet -> _apply_parsed -> Checkout.save`. It has no
verified Runtime publication pin, stable native row refs, captured
read/selection/order claims, or Runtime/outbox target.

Therefore the dependency order is fixed:

1. Agent must first add a bounded author-time retention seam for the native
   basis, stable row intent/identity, and the original Runtime target, or
   explicitly keep unsupported legacy/mixed rows detached. It must preserve
   the documented broad grammar and local rollback while doing so.
2. Only after that seam exists may Runtime pair the retained commands with
   its existing normal commit acceptance/rebase path. The original base and
   guards must not be refreshed at send time; a conflicting membership/order
   or row write refuses visibly and keeps the draft/outbox.
3. The requester must retain the exact request body and idempotency key across
   lost acknowledgement/restart, then use the existing history/inverse path.
   Runtime must not receive a detached snapshot or infer intent from a
   current document.

## Original positive floor

Keep these connected native positives unchanged as the floor for the future
paired route:

- `tests/sdk/test_timeline_sheet_native.py::test_atomic_batch_commit_lost_ack_restart_and_undo`
- `tests/sdk/test_timeline_sheet_native.py::test_stale_original_guards_conflict_without_refreshing`
- `tests/sdk/test_timeline_sheet_native.py::test_disjoint_head_edit_rebases_without_writing_unchanged_cells`
- `tests/packs/timeline/test_cli_native_sheet.py::test_export_preview_apply_and_undo`
- `tests/packs/timeline/test_cli_native_sheet.py::test_lost_ack_immutable_retry_and_pending_export_refusal`
- `tests/packs/timeline/test_cli_native_sheet.py::test_stale_export_refuses_without_recapturing`

Keep the detached Main positives open and unchanged; representative IDs are
`tests/sdk/test_timeline_sheet.py::test_a_fragment_touches_only_its_cuts_and_a_new_line_adds_a_layer`,
`::test_the_music_bed_is_in_the_sheet_and_its_line_edits_it`,
`::test_visual_clip_looks_round_trip_and_omission_clears_them`, and
`::test_sound_trim_is_rendered_and_parsed_and_unchanged_window_is_noop`.
The exact current Agent command from the WC8 reports is:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" \
  /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider \
  tests/sdk/test_timeline_sheet_native.py \
  tests/packs/timeline/test_cli_native_sheet.py \
  tests/sdk/test_timeline_sheet.py \
  tests/packs/timeline/test_verbs_working_copy.py
```

The Runtime acceptance command for the eventual paired batch is:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" \
  /home/user/work/venv-runtime/bin/python -m pytest -q -p no:cacheprovider \
  tests/test_timeline_commit_acceptance.py \
  tests/test_timeline_commit_execution.py \
  tests/test_timeline_commit_contract.py \
  tests/test_timeline_current_union_contract.py
```

## Preserve, hold, and deletion condition

Preserve all detached grammar positives, local three-way/rollback behavior,
draft visibility, connected native behavior, opaque fields, explicit clears,
stable IDs, exact original basis, rationale, outbox/history, retry identity,
server-side rebase, inverse/ABA guards, and atomic mixed-shape refusal. Do
not replace the live detached positive with a refusal or a renamed whole
writer. The current `apply_sheet`/`merge_sheet`/`Checkout.save` route stays
held until its missing basis/intent/target seam exists and is qualified.

No `full*`, browser, renderer, live-socket, installed-launcher, schema,
generated-client, version-pin, or activation run is part of this handoff.
Do not create a Runtime pin or activate a private Agent source. No Runtime
source change is authorized unless an existing acceptance test fails for the
retained command batch.

Delete the detached local merge writer only after every supported detached
edit has a retained native basis/intent/target, all unsupported grammar stays
visibly held, the connected and detached positive floor remains green, and a
real Runtime requester proof covers stale-head rebase/conflict, exact retry
after restart, and guarded inverse/ABA. This note alone authorizes no
deletion.

## Remote merge route

Runtime manager owns any Runtime source/test change. After a committed worker
branch has the bounded evidence, submit it through:

```sh
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-merge-remote runtime <runtime-worker-name> "WC8 detached-sheet retained basis/intent/target acceptance"
```

The Runtime home machine merges into its `tl/integration`; Agent reviews the
paired native capture separately. No direct merge, push, pin, or branch
mutation is requested here.
