# Agent Gate 1 / Gate 3 current proof track

Date: 2026-10-20
Base: current Agent `tl/integration` (`a8a40afd3` before the worker snapshot)
Qualification cohort: current Agent snapshot with Runtime `/home/user/work/runtime`, public Composition 0.0.13 Remotion tree `/home/user/work/runtimes/agent-remotion-0013`, and the central child environment `/home/user/work/venv-agent-child-s2`.

## Suites and results

The two allow-list entries were added to `scratchpad/orch/tests/suites.conf`:

- `agent gate1-current-integration`
- `agent gate3-agent-current-integration`

Both were requested once through the central test service, after the final suite edits. No full suite was requested.

| Suite | Central result | Test-service result |
|---|---:|---|
| `gate1-current-integration` | 83 passed, 127 deselected, 19.88s | PASS, exit 0; run `agt-m2-gate13-current-proof-track-gate1-current-integration-1020212417-23926` |
| `gate3-agent-current-integration` | 26 passed, 8.69s | PASS, exit 0; run `agt-m2-gate13-current-proof-track-gate3-agent-current-integration-1020212417-13895` |

Logs:

- `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/agt-m2-gate13-current-proof-track-gate1-current-integration-1020212417-23926/log.txt`
- `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/agt-m2-gate13-current-proof-track-gate3-agent-current-integration-1020212417-13895/log.txt`

The exact environment and pytest commands are the two named lines in `suites.conf`; both disable pytest cache writes and use the current Runtime checkout/public 0.0.13 paths.

## Gate 1 inventory

Existing tests selected, without modifying assertions:

- CLI/Python/sheet cross-front-end runner: `tests/editing_conformance/test_conformance.py -k timing` (the timing scenarios exercise each declared front end and the runner's exact after/undo/redo comparisons).
- Opaque and explicit clear preservation: `test_recipe_m2_clip_add.py::{test_literal_seconds_and_opaque_json_exact_reload_inverse_redo,test_canonical_schema_closes_the_operation_and_preserves_opaque_row_fields}`, `test_recipe_m2_placement.py::{test_preserves_raw_identity_source_media_order_opaque_and_sibling,test_absence_null_and_relation_clears_roundtrip}`, `test_recipe_text_binding_spike.py::{test_empty_text_is_present_zero_byte_and_distinct_from_clear_and_absent,test_clear_of_absent_binding_is_refused_not_a_silent_noop}`, `test_word_binding_recipe.py::test_last_write_clear_undo_restore_and_restore_inverse`, `test_timing_compiler.py::test_explicit_clears_empty_formulas_and_opaque_maps_survive`, and the native sheet clear matrix.
- Occurrence identity/isolation and source metadata: `test_recipe_occurrence_media.py::{test_provider_exact_reload_inverse_redo_and_retired_asset_reservation,test_noninteger_positive_speed_preserves_source_units_and_half_open_boundary}`, `test_recipe_occurrence_delete.py::{test_delete_reload_exact_guarded_inverse_redo_order_and_metadata,test_explicit_single_occurrence_identity_only,test_exact_opaque_and_tagged_metadata_survive_last_consumer_history_inverse}`, and `test_recipe_m2_placement.py::test_parent_and_occurrence_golden_capture_replay_reload_inverse_redo`.
- Transcript/source binding identity and replay: `test_recipe_text_binding_spike.py::{test_set_round_trip_records_exact_identity_and_dependency,test_inverse_restores_absence_and_redo_restores_exact_row}`, `test_word_binding_recipe.py::{test_undo_recovers_before_binding_even_when_text_writes_are_equal,test_phrase_records_all_consecutive_main_word_ids,test_same_word_in_reused_cas_clips_retains_raw_source_through_undo}`, and `test_timing_retained_inputs.py::test_retained_v1_and_explicit_v2_keep_window_and_raw_source_identity`.
- Rational fps, half-open boundaries, and deterministic compiler behavior: `test_word_binding_recipe.py::{test_half_open_window_and_exact_rational_fps_are_validated_at_acceptance,test_typed_second_offset_preserves_main_precision_at_rational_frame_boundary}` plus `test_timing_compiler.py::{test_exact_binding_uses_selected_duplicate_word_and_preserves_authored_commands_and_clears,test_fixed_source_window_and_rational_half_frame_ties,test_after_word_end_at_source_out_is_included_and_onset_at_source_out_is_refused,test_rational_fps_anchor_and_exact_frame_offset,test_compilation_has_no_io_random_clock_renderer_or_mutable_checkout_dependency}`.
- Sheet-native retry/inverse path: `test_timeline_sheet_native.py::{test_label_clear_is_distinct_from_empty_and_literal_clear,test_omitted_native_clip_row_uses_normal_commit_retry_undo_redo_and_rebases}`.

The suite's 83 passes cover the requested semantic cases. The first local selector probe had one typo in an ad hoc node id; it was corrected before central submission. No product or assertion change was made.

## Gate 3 inventory

Existing tests selected:

- Renderer-independent save fences: all tests in `tests/sdk/test_scene_save_core.py`; they block renderer/scene imports, process launches, and diagnostics while exercising save, publish, transaction, dry-run, reload, and undo.
- Real provider reload/inverse without renderer: `tests/sdk/test_timeline_commit_provider.py::test_move_reload_and_inverse_import_no_renderer` and `::test_restore_undo_redo_exact_full_closure_and_unknown_fields`.
- Runtime restart/retry/inverse: `tests/sdk/test_timeline_commit_provider_runtime.py::{test_structural_reservations_and_receipt_retry_survive_runtime_restart,test_restore_inverse_redo_and_exact_retry_survive_runtime_restart}`.
- Working-copy restart persistence: `tests/sdk/test_timeline_persistence.py::test_restart_a_fresh_process_sees_every_edit_and_the_undo_history`.
- Honest preview/unavailability reporting: `tests/packs/timeline/test_visualize_drafts.py::{test_visualize_summary_uses_rendered_snapshot_label_for_candidate_and_unavailable,test_render_draft_without_checkout_fails_before_rendering}`, `tests/sdk/test_project_render_rrp.py::test_missing_publication_association_is_an_explicit_dependency_failure`, and `tests/sdk/test_workspace_client_timeline_commit.py::{test_workspace_client_commit_preserves_preview_null_receipt,test_workspace_client_absent_commit_method_is_actionable}`.

## Uncovered or not claimed

- Gate 1 is bounded; the full editing-conformance corpus was intentionally not run. Non-timing CLI/Python/sheet scenarios, including the broader structure/look/audio set, remain outside this result. The focused occurrence/source/transcript checks are recipe/provider tests rather than a new three-front-end scenario for every one of those data shapes.
- Gate 3 proves renderer independence with import/process fences and provider restart/reload tests. It does not prove a live browser, a real Composition frame, a physical preview artifact, or a stopped external renderer process behind the Runtime door.
- No full suite, localhost/browser/live-socket journey, or cross-product App journey was run. Runtime restart cases are the existing bounded provider/runtime fixtures, not a new full Runtime-door qualification.

## Follow-up: corrected Gate3 Door node

Date: 2026-10-20

Gate1's new three-front-end case was already qualified by the predecessor at 3
passes and was not repeated. The predecessor's Gate3 node reached authenticated
Door commit, reload, and undo, but its first run failed only on the new preview
error-shape assertion (`preview.error` is a mapping, not an object with
`.code/.message/.details`). After the test-only shape correction, the authorized
central rerun passed:

- `agt-m2-gate3-door-final-correction-proof-gate3-followup-new-node-1020213757-26194`
- `gate3-followup-new-node`: **1 passed**, exit 0, 37.85s

The passing case still asserts the authenticated `/v1` commit/reload/undo path,
`preview.ok is False`, the current structured
`CapabilityValidationError`/`validation` preview refusal, and both stopped-
renderer subprocess fences. This is a PASS for the corrected Gate3 node. The
preview result is an honest structured preflight refusal on the public013/C13
normal Door fixture; no renderer process was launched. No full suite was run.

## Follow-up: current rational explicit-occurrence landing

Date: 2026-10-20T22:14:37Z

Current Agent source is `32ebd610016195c69e6eceb5fc7530dbbf634cb5`, the
requested `tl/integration` snapshot. The donor `97f96218d` product hunk was
ported verbatim: only `commit_move` in `astrid/packs/timeline/cli_native.py`
now admits a non-`parent/clip:` selector; `commit_trim` and all command/schema
code are unchanged. The attached-trim, Gate3/sheet, and WC2 files remain
outside the worker diff.

The named `agent gate1-current-integration` allow-list now explicitly includes
all three required new groups: the opaque/clear YAML node, the
occurrence/source YAML node, and the rational explicit-selector native
three-frontend test. A collect-only run selected each node by identity:

- `look.clear.plate-asset-opaque`: CLI, sheet, Python
- `timing.occurrence.source-isolation`: CLI, sheet, Python
- `test_rational_explicit_occurrence_move_is_lossless_across_native_frontends`:
  CLI, Python, sheet

The narrowed current-source execution passed **9 tests** (3 + 3 + 3) in
6.01s. No prior Gate1/Gate3 success suite was replayed, and no full suite was
requested.

Remaining semantic gaps are unchanged: the full editing-conformance corpus,
non-timing frontend matrix, live browser/Composition parity, and the complete
cross-product journey remain unqualified. This is current Gate1 evidence only,
not a complete-foundation claim.

## Gate 1 follow-up: non-timing current integration

Date: 2026-10-20T22:19:50Z

The named `agent gate1-nontiming-current-integration` suite was added without
changing either prior named Gate1/Gate3 selection. It selects only the existing
non-timing IDs loaded by `tests/editing_conformance/test_conformance.py`:
`audio`, `code`, `look`, and `structure`. No new scenario or assertion was
added, and no product source was changed.

Central run:

- `agt-m2-gate1-nontiming-current-proof-gate1-nontiming-current-integration-1020221836-8218`
- result: **130 passed, 24 deselected**, exit 0, 28.96s
- log: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/agt-m2-gate1-nontiming-current-proof-gate1-nontiming-current-integration-1020221836-8218/log.txt`

Coverage tuple: **(44 scenarios, 130 nodes, 44 CLI, 43 Python, 43 sheet)**.
The one CLI-only node is the intentional refused scenario
`look.entrance.card-slide-up-refused`; its YAML declares no Python or sheet
path. Every selected node passed its original runner assertions, including
run/refusal, change/no-change, reports, equality, undo, redo, checks, and any
declared idempotence.

Per-scenario coverage (`✓` means that declared path was selected and passed):

| Scenario | CLI | Python | Sheet |
|---|:---:|:---:|:---:|
| `audio.add.media-bed` | ✓ | ✓ | ✓ |
| `audio.add.sfx-viral` | ✓ | ✓ | ✓ |
| `audio.look.music-volume` | ✓ | ✓ | ✓ |
| `audio.set.music-volume` | ✓ | ✓ | ✓ |
| `audio.set.unknown-key` | ✓ | ✓ | ✓ |
| `audio.trim-slip.music` | ✓ | ✓ | ✓ |
| `audio.volume.music-minus-3db` | ✓ | ✓ | ✓ |
| `code.python.two-sets-one-save` | ✓ | ✓ | ✓ |
| `look.add-then-swap.sprite` | ✓ | ✓ | ✓ |
| `look.add.label` | ✓ | ✓ | ✓ |
| `look.add.sprite` | ✓ | ✓ | ✓ |
| `look.clear.plate-asset-opaque` | ✓ | ✓ | ✓ |
| `look.entrance.card-fade-ease-out` | ✓ | ✓ | ✓ |
| `look.entrance.card-scale-in` | ✓ | ✓ | ✓ |
| `look.entrance.card-slide-up-refused` | ✓ | — | — |
| `look.exit.card-fade` | ✓ | ✓ | ✓ |
| `look.fade-in.card-8f-ease-out` | ✓ | ✓ | ✓ |
| `look.fade-in.card-8f` | ✓ | ✓ | ✓ |
| `look.look.rocket-opacity` | ✓ | ✓ | ✓ |
| `look.opacity.rocket-60` | ✓ | ✓ | ✓ |
| `look.remove.card` | ✓ | ✓ | ✓ |
| `look.set.card-text` | ✓ | ✓ | ✓ |
| `look.set.plate-zoom-focus` | ✓ | ✓ | ✓ |
| `look.set.plate-zoom-fraction` | ✓ | ✓ | ✓ |
| `look.set.rocket-enter` | ✓ | ✓ | ✓ |
| `look.set.rocket-keyframes` | ✓ | ✓ | ✓ |
| `look.set.rocket-x` | ✓ | ✓ | ✓ |
| `look.set.rocket-xy` | ✓ | ✓ | ✓ |
| `look.set.sprite-scale-range` | ✓ | ✓ | ✓ |
| `look.set.type-reveal-bad` | ✓ | ✓ | ✓ |
| `look.set.unknown-key` | ✓ | ✓ | ✓ |
| `look.swap-asset.rocket` | ✓ | ✓ | ✓ |
| `structure.add-cut.now` | ✓ | ✓ | ✓ |
| `structure.close-gap.live` | ✓ | ✓ | ✓ |
| `structure.cut-on.c2-now` | ✓ | ✓ | ✓ |
| `structure.cut-on.c3-four` | ✓ | ✓ | ✓ |
| `structure.extend-end.last-cut` | ✓ | ✓ | ✓ |
| `structure.film-end.extend-1s` | ✓ | ✓ | ✓ |
| `structure.gap-after.s1` | ✓ | ✓ | ✓ |
| `structure.remove-line.music-keep-end` | ✓ | ✓ | ✓ |
| `structure.remove-line.music-plays-on` | ✓ | ✓ | ✓ |
| `structure.remove-line.s2` | ✓ | ✓ | ✓ |
| `structure.shorten-end.last-cut` | ✓ | ✓ | ✓ |
| `structure.split.c1-went` | ✓ | ✓ | ✓ |

Failure classification: none. The central run produced no source, adapter,
environment, or unmatched private-artifact failure, so no narrow adapter patch
or migration task is indicated by this slice. Ordinary detached fixture
mutation remains only conformance-harness evidence; it is not claimed as
accepted Runtime traffic.

Concrete missing semantics and boundaries remain explicit:

- The 24 timing nodes were deselected intentionally; timing anchors, nudges,
  source-window isolation, half-open boundaries, and rational-frame behavior
  remain represented by the prior qualified timing/source/rational selections,
  not repeated here.
- This run does not prove Runtime-door acceptance, transport, idempotent
  Runtime receipts, App gesture production, browser/live-socket behavior, or
  renderer/Composition parity.
- It does not run the other `tests/editing_conformance` modules or add a
  broader scenario matrix. No private artifact was required or unmatched.

## Incremental watch: attached parent delete landing

Date: 2026-10-20T22:51:49Z

The Agent integration branch advanced from the prior proof snapshot with the
semantic merge `b43cd9571` (source commit `cb2eedc50`): attached parent
`clip.delete` now uses the durable native command/outbox publication path,
including dependency guards, exact retry identity, reload, and guarded undo.
This is a relevant Gate1/Gate3 adapter change, so only its existing focused
HTTP node was replayed; untouched prior Gate1/Gate3 evidence remains valid.

Live integration heads at this check:

| Repo | `tl/integration` head |
|---|---|
| Agent | `b43cd9571` |
| Runtime | `a6bce81` |
| App | `157eef8cf` |
| Composition | `ac918bb` |

Named central check:

- Suite: `current-owned-parent-delete-http`
- Run: `agt-m2-gate13-incremental-current-owner-current-owned-parent-delete-http-1020225129-10201`
- Agent source tree: `1d44801de4aa27559d39bc30c35800a13db5ad49`
- Result: **1 passed in 4.81s**, exit 0
- Exact node: `tests/editing_conformance/test_owned_move_publish_runtime.py::test_http_original_sdk_parent_delete_stale_rebase_lost_ack_reload_retry_undo`
- Environment: public Remotion `agent-remotion-0013`, C13 child Python environment,
  and the supported VibeComfy fixture override from the named suite.

The passing node covers stale rebase, lost acknowledgement, restart, exact
retry, parent deletion, and guarded undo. No full/full* suite, browser/live
journey, or unchanged prior qualification was run.

The next Agent semantic worker is currently preparing the existing attached
parent split path on top of this integration head; it has not landed, so no
split replay is claimed yet. Artifact/docs/env-only worker activity does not
require Gate1/Gate3 semantic replay.

At 2026-10-20T22:52:10Z the live App head was `e9d04f4bf` (the Agent, Runtime,
and Composition heads above were unchanged). Its merge changes only the App
viewing-parity audio controller and its tests; it has no Agent editing or
renderer-independent-save consumer overlap, so no Gate1/Gate3 Agent node was
replayed for that App-only change.

## Incremental watch: connected frontend label-clear proof

Date: 2026-10-20T22:55:01Z

Agent integration advanced to `d9a49344b` (source commit `34baa3856`), adding
one parameterized authenticated `/v1` proof for Python, CLI, and NativeSheet
label-clear edits. The merge is test-only; the relevant behavior was already
present in the preceding Agent source. It is nevertheless a new Gate1 proof
node, so it was selected for a bounded central check.

The first request failed before collection because the test service snapshotted
this worker's pre-merge branch (`b43cd9571`, tree
`1d44801de4aa27559d39bc30c35800a13db5ad49`), where the newly merged test node
did not exist. This was a test-service snapshot mismatch (`no tests ran`, exit
4), not a product or assertion failure. A test-only port of the exact merged
proof was used in this worker to obtain the correct source-equivalent snapshot;
no integration branch or product source was edited.

Successful named central check:

- Suite: `gate1-connected-frontends-integration`
- Run: `agt-m2-gate13-incremental-current-owner-gate1-connected-frontends-integration-1020225435-13125`
- Agent source tree: `11861a9611c050c3566f1df61b11fe1ecba4ead3`
- Result: **3 passed in 4.75s**, exit 0
- Exact node: `tests/editing_conformance/test_native_sheet_current_runtime.py::test_http_connected_label_clear_is_lossless_across_native_frontends`
- Coverage: Python, CLI, NativeSheet; authenticated `/v1` transport, reload,
  undo, opaque/source identity preservation, and retired publisher rejection.

Live heads at the successful check: Agent `d9a49344b`, Runtime `a6bce81`, App
`e9d04f4bf`, Composition `ac918bb`. No full/full* suite or unchanged prior
Gate1/Gate3 qualification was run.

At 2026-10-20T22:58:18Z the attached-parent split worker completed its
candidate (`feat(sdk): publish attached parent splits`) with 91 focused tests
and a 2-pass central HTTP lane, plus Ruff and `git diff --check`. It is not
merged into `tl/integration` and remains pending independent data-loss review;
therefore it is not current Gate1/Gate3 evidence and no split replay was
requested. The live Agent head remained `d9a49344b`.

At 2026-10-20T22:59:35Z Runtime advanced to `9d1c43c` from `a6bce81` with
catalog custody/project-scope regressions (`runtime_protocol/service.py` and
catalog/domain tests). The diff does not change the Runtime timeline-door
acceptance path exercised by the current Agent Gate1/Gate3 nodes, so no Agent
node replay was needed. Current heads are Agent `d9a49344b`, Runtime
`9d1c43c`, App `e9d04f4bf`, and Composition `ac918bb`.

The completed `agt-m4-full4555-fixture-repairs` worker reported 15 targeted
Remotion fixture/layer-tail tests passing against the public 0.0.13 package.
Those changes are in Agent rendering test fixtures and current public
TypeScript compatibility probes, not the Agent save/commit path or the
renderer-independence nodes listed above; no Gate1/Gate3 Agent replay was
needed, and the candidate is not merged into Agent integration.

The independent data-loss review for the pending attached-parent split
candidate then returned **APPROVE** at 2026-10-20T23:01:19Z (candidate
`404422aa3` against `b43cd9571`). This changes no integration head or current
Gate evidence; the split-specific replay remains queued behind the actual
merge.

## Incremental watch: attached parent split merge

Date: 2026-10-20T23:02:29Z

The approved split candidate merged into Agent integration as `8c12f559e`
(`404422aa3`). This is a new semantic/adapter path: attached parent
`Clip.split(on, *, id=...)` now uses native `clip.split` capture and the
durable owned outbox/retry/inverse path.

Bounded central replay on the actual integration branch:

- Suite: `current-owned-parent-delete-http`, invoked as `integration:agent`
  with the split node file override
- Run: `agent-current-owned-parent-delete-http-1020230207-9436`
- Agent source tree: `54c3c093d3df404d601c0efafe29cf70ce44dfa1`
- Result: **2 passed in 8.56s**, exit 0
- Nodes: existing parent-delete control and
  `tests/editing_conformance/test_owned_move_publish_runtime.py::test_http_original_sdk_parent_split_stale_rebase_lost_ack_reload_retry_undo`
- The split node covers stale rebase, lost acknowledgement, restart, exact
  retry, stable created ID, preserved source/opaque data, and guarded inverse.

Live heads at this replay: Agent `8c12f559e`, Runtime `9d1c43c`, App
`e9d04f4bf`, Composition `ac918bb`. No full/full* suite or unrelated Gate1/
Gate3 qualification was run.

By 2026-10-20T23:03:30Z Agent had also advanced to `1b526ce05` through
three non-editing merges: public Remotion fixture/registry test repairs and a
dead-leaf deletion in `astrid/packs/rendering/actions/timeline_visualize/model.py`.
These do not touch the Agent commit/undo/rebase implementation or the current
renderer-independent save nodes, so no additional Gate1/Gate3 replay was
needed. Current heads: Agent `1b526ce05`, Runtime `9d1c43c`, App `e9d04f4bf`,
Composition `ac918bb`.

At 2026-10-20T23:04:48Z Agent advanced to `d97f57810` with the approved
admitted-theme rendering export task adapter and its direct tests (5 passed in
the worker report). This is downstream render-task adapter code, not the
timeline edit/commit path or Gate3 renderer-independent save/preflight nodes,
so no Gate1/Gate3 replay was needed. Current heads are Agent `d97f57810`,
Runtime `9d1c43c`, App `e9d04f4bf`, Composition `ac918bb`.

At 2026-10-20T23:05:31Z App advanced to `ce6deafa3` with public export-alias
cleanup and viewing-parity native canvas fixture updates. These are App/Vite
and viewing fixture changes, with no Agent timeline edit or renderer-independent
save-path dependency, so no Agent Gate1/Gate3 replay was needed. Current heads:
Agent `d97f57810`, Runtime `9d1c43c`, App `ce6deafa3`, Composition `ac918bb`.

At 2026-10-20T23:11:21Z App advanced to `a12b19be5` with playback-rate
sanitization delegated from App viewing code to Composition, and Composition
advanced to `e7ef7a0` with a smoke-fixture input-authority tweak. These are
viewing/render fixture changes; neither changes Agent save acceptance,
workspace commit adapters, or the renderer-independent save nodes. No Agent
Gate1/Gate3 replay was needed. Current heads: Agent `01ee5b958`, Runtime
`9d1c43c`, App `a12b19be5`, Composition `e7ef7a0`.

The independent review of upstream497 returned **APPROVE FOR STAGING — HOLD
pending compatible Runtime**. It confirmed the candidate's 92-pass Gate1
report but also the `platform.durable_replace` Runtime dependency and an
unqualified Gate3; the candidate is not on current Agent integration, so no
replay or Gate claim was added.

At 2026-10-20T23:12:36Z Agent advanced to `d6608545b` with the root-build
write-guard rendering helper and staging tests. This is rendering test/support
code only and does not alter the timeline commit provider, save path, or the
current Gate3 nodes, so no replay was needed. Current heads: Agent
`d6608545b`, Runtime `9d1c43c`, App `a12b19be5`, Composition `e7ef7a0`.

At 2026-10-20T23:13:13Z Agent advanced to `2c34cb967` with a test-only
Gate5 media-import fixture (11 central `commit-integration` passes; no Agent
product/API/schema change). App advanced to `812a609ee` with clip-scalar
transition capture/gesture tests. The Agent fixture is outside Gate1/Gate3,
and the App producer change has no Agent-side node dependency in this watch;
no Gate1/Gate3 replay was needed. Current heads: Agent `2c34cb967`, Runtime
`9d1c43c`, App `812a609ee`, Composition `e7ef7a0`.

The independent review for the pending parent `afterClipId` source candidate
returned **APPROVE** with the existing carrier/schema preserved, but App2 and
Runtime qualification remain open and the candidate is not merged. The scene
proof clean-land report likewise remains a candidate with a missing exact
control lane; neither changed current Agent integration or warranted replay.

The `agt-m2-upstream497-current-merge` worker reported a pending upstream
merge candidate with 92 Gate1 tests passing and a broader conformance run
blocked by an incompatible shared Runtime checkout. It has not changed Agent
integration (`d97f57810`) and therefore is not current Gate evidence; no
replay was requested. If merged, its Timeline semantic delta requires a fresh
affected-node classification, and its reported Runtime incompatibility must be
resolved before any Gate3 claim.

## Incremental watch: RemoteTimelines extraction

Date: 2026-10-20T23:09:09Z

Agent integration advanced to `01ee5b958` (`00d84bc4d`), extracting
`RemoteTimelines` revision operations into the private `_remote_timeline.py`
adapter while preserving the public facade. This is a relevant SDK adapter
change because two existing Gate3 workspace-client nodes and two adjacent
RemoteTimelines scope nodes use the moved operations.

Bounded central check on actual integration:

- Suite: `targeted`, invoked as `integration:agent`
- Run: `agent-targeted-1020230856-15828`
- Agent source tree: `c9a44b4b6f17cbf689ee6e3fddb49485697b5d03`
- Result: **4 passed in 0.32s**, exit 0
- Nodes: `test_workspace_client_commit_preserves_preview_null_receipt`,
  `test_workspace_client_absent_commit_method_is_actionable`,
  `test_remote_timelines_commit_and_history_are_scoped`, and
  `test_remote_timelines_commit_rejects_body_scope_mismatch` from
  `tests/sdk/test_workspace_client_timeline_commit.py`.

No full/full* suite or unrelated Gate1/Gate3 node was run. Live heads at this
check: Agent `01ee5b958`, Runtime `9d1c43c`, App `ce6deafa3`, Composition
`ac918bb`.

The pending `agt-m2-parent-afterclip-guarded-source` candidate reports 7
focused and 267 neighboring tests passing, but remains before App2/Runtime
review and is not merged; no Gate replay was requested. The managed-scene
authority review separately returned REQUEST CHANGES (EOF hygiene and a real
host negative-control gap); it is also unmerged and does not alter current
Gate evidence.

The pending `agt-m2-wc7-next-existing-command-consumer` candidate adds
attached-parent `Clip.clear_asset()` through the existing `clip.set` carrier;
its worker report has 47 local and 2 central HTTP passes, but it is not merged
into Agent integration, so no replay is claimed yet. The concurrent root-build
write-guard report is rendering-test-only and likewise has no Gate1/Gate3
Agent replay impact.

## Incremental watch: attached parent clear-asset merge

Date: 2026-10-20T23:15:43Z

Agent integration advanced to `340a2d487`, adding attached-parent
`Clip.clear_asset()` publication through the existing `clip.set` carrier and
durable retry/undo path. This is a relevant semantic adapter change.

The first generic `targeted` request for the exact node collected zero tests
(exit 5) because that command does not apply the integration marker. It was a
selection/lane mismatch, not a product failure. The same node was then run
through the existing integration-marked named suite on the actual integration
branch:

- Suite: `current-owned-parent-delete-http`, invoked as `integration:agent`
  with the clear-asset node file override
- Run: `agent-current-owned-parent-delete-http-1020231514-26683`
- Agent source tree: `52239ff7c1c5d45ee0705aecdf5df1c35e765bf2`
- Result: **2 passed in 7.68s**, exit 0
- Nodes: existing parent-delete control and
  `tests/editing_conformance/test_owned_move_publish_runtime.py::test_http_original_sdk_parent_asset_clear_lost_ack_reload_retry_undo`

Live heads at this replay: Agent `340a2d487`, Runtime `9d1c43c`, App
`812a609ee`, Composition `e7ef7a0`. No full/full* suite or unrelated node was
run.

## Incremental watch: detached sheet adapter frontier

Date: 2026-10-20T23:18:01Z

Agent integration advanced to `e55d0616b` (`1a7349eb9`), narrowing the
detached `apply_sheet` adapter by removing an unused Runtime client/history
lookup while preserving local three-way merge and connected NativeSheet
behavior. The affected Gate1 sheet nodes were replayed on actual integration:

- Suite: `targeted`, invoked as `integration:agent`
- Run: `agent-targeted-1020231732-32658`
- Agent source tree: `4955a447a5d02d75b758a44266e8c65bb4063651`
- Result: **2 passed in 1.51s**, exit 0
- Nodes: `test_native_rows_cannot_fall_into_the_legacy_sheet_writer` and
  `test_omitted_native_clip_row_uses_normal_commit_retry_undo_redo_and_rebases`
  from `tests/sdk/test_timeline_sheet_native.py`.

No full/full* suite or unrelated node was run. Live heads: Agent
`e55d0616b`, Runtime `9d1c43c`, App `812a609ee`, Composition `e7ef7a0`.

The pending `agt-m2-wc7-parent-transition-clear` candidate adds exact parent
transition CLEAR capture via the existing `clip.set` carrier (145 local tests,
1 central HTTP test), but it has not merged into integration. No replay or
current Gate claim is made until its merge lands.

At 2026-10-20T23:19:18Z Agent advanced to `0542b4291` with an
`artifacts.json`-only manifest refresh. This is artifact metadata with no
timeline semantic or adapter source change, so no Gate1/Gate3 replay was
needed. Current heads: Agent `0542b4291`, Runtime `9d1c43c`, App `812a609ee`,
Composition `e7ef7a0`.

Closing watch snapshot at 2026-10-20T23:35:31Z: final live heads are Agent
`19c3cfc1c6283659c6fc864581d56c3a99e41873`, Runtime
`9d1c43c647301da48a6e86ad82e466b501bd2418`, App
`3ee1900621f5ae27450ce5b1b69a3b7987e4b8c8`, and Composition
`e7ef7a0729a2d7dad3c0ae60da9e6bb8f844d332`. No further Agent semantic merge
landed after the detached-sheet history replay; the last App update was
viewing-only. No full/full* suite was requested.

## Final incremental-watch snapshot

Date: 2026-10-20T23:35:19Z

No further Agent semantic merge landed after `19c3cfc1c`. The final live heads
are Agent `19c3cfc1c`, Runtime `9d1c43c`, App `3ee190062`, and Composition
`e7ef7a0`. The last App merge changes only viewing-parity audio controller
behavior/tests, so no Agent Gate1/Gate3 replay was needed. The current exact
evidence and remaining gaps are the bounded results recorded above; no full or
full* suite was requested.

At 2026-10-20T23:29:35Z App advanced to `a6fa6ff8c` with physical PCM parity
comparison tests only. The related speech-audio intent review is App/source
scope and remains unqualified against the known Runtime health-digest
mismatch; it does not touch Agent Gate1/Gate3 nodes, so no replay was needed.

The pending `agt-m2-sheet-documented-client-preserve` candidate proposes
restoring the documented detached `apply_sheet(..., client=None)` keyword and
Runtime-history fallback removed by `1a7349eb9`; its local sheet/history lane
passed 126 tests, while its central Runtime-history probe was unavailable
(fixture absent, exit 5). It is unmerged, so no replay or new Gate claim was
made; the API compatibility decision remains with the Agent manager.

## Incremental watch: detached-sheet history compatibility merge

Date: 2026-10-20T23:26:27Z

Agent integration advanced to `19c3cfc1c` (`fb465b336`), restoring the
documented detached `apply_sheet(..., client=None)` keyword and retained
Runtime-history fallback. This directly affects Gate1 sheet/history behavior.

The first three-node targeted request selected the Runtime-history test but
that module yielded one skip and no collector for the node in the central
snapshot; it did not produce an assertion failure. The two directly runnable
nodes were then checked on actual integration:

- Suite: `targeted`, invoked as `integration:agent`
- Run: `agent-targeted-1020232605-24043`
- Agent source tree: `7f005c0e121b2c3dd6c11203359ca305a5baa4ae`
- Result: **2 passed in 1.05s**, exit 0
- Nodes: `test_sheet_local_basis_does_not_cross_accepted_base` and
  `test_applying_the_printed_sheet_changes_nothing`.

The Runtime-history node
`tests/sdk/test_timeline_checkout_history_runtime.py::test_checkout_reload_undo_cli_redo_uses_retained_history`
remains unverified because the central Runtime fixture was unavailable (the
prior attempt ended with one skip and no collector). No assertion was changed
or weakened. Live heads: Agent `19c3cfc1c`, Runtime `9d1c43c`, App `e4ee1dceb`,
Composition `e7ef7a0`.

The pending `agt-m2-parent-clear-combined-current` candidate resolves the
asset/transition clear allowlist overlap (7 SDK controls and 2 central HTTP
passes) but is not merged into the live Agent head; no replay or current Gate
claim was added.

At 2026-10-20T23:23:30Z App advanced to `e4ee1dceb` with an ordinary-trim
member/generic-patch capture change. It is App command-producer work and does
not alter Agent Gate1/Gate3 nodes or the Agent save path, so no replay was
needed. Current heads: Agent `0542b4291`, Runtime `9d1c43c`, App `e4ee1dceb`,
Composition `e7ef7a0`.

## Corrected current frontier (2026-10-21)

The detailed bounded map is in the completed 0729 worker report
([report](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m4-gate1-current-frontier-proof-plan-0729/report.md)).
This page records the current correction and does not turn collected or staged
evidence into a current-head pass.

- Current Agent integration is `7c9ef2ed5e70da1a13e89278496c74321453955a`
  (tree `293084643595ddb6048456610e9f4e2a37217bcd`). Its latest relevant
  merges are installed-origin `45729a6be` (source `76f3337cd`), typed SDK
  forward `75a96ec95`, and Ruff shrink-only refresh `96eebbd70`. The merged
  document stopgap remains `ac9a93579` (source `a362c7fd`): it refuses some
  lossy row-presence changes, but does not close every parent/config/registry/
  container or mirror-deletion field.
- The 0727 document proof was not only a pre-pytest snapshot failure. The
  earlier run
  `agt-m2-document-approved-coherent-http-once-0721-document-diff-approved-coherent-http-once-0721-integration-1021072359-1130`
  stopped before pytest because the synthetic snapshot `9bcacb83` changed
  `HEAD` while preserving source commit `e51732a` and tree
  `f157ce2451296d8de1ba59a8567a46f4e112bd75`. After the guard correction, the
  authorized run
  `agt-m2-document-snapshot-identity-diagnose-and-one-proof-0727-document-diff-approved-coherent-http-once-0721-integration-1021072907-7153`
  executed the authenticated HTTP node once. It failed after acceptance at
  `persisted_bundle(accepted) == persisted_bundle(native["bundle"])`:
  Runtime created a new shot/shot-revision for the edited occurrence while
  `shared-sibling` retained the original. Reload and inverse were not reached;
  no retry was authorized. Exact run pins were Agent `e51732a...` / tree
  `f157ce...`, snapshot `9bcacb83...`, Runtime `b92d3e7a...` / tree
  `6abc2f117391de8e7e35c0283f575a002199894d`.
- Fresh transcript/source binding is still pending current-source port
  `agt-m2-gate1-fresh-transcript-current-source-port-0737`. Its predecessor's
  candidate result (`2000b0bc...`, Runtime `3dcae183...`, result
  `agt-m2-gate1-anchor-native-frontends-fix-gate1-fresh-word-transcript-frontends-1021020618-14833`)
  is staged evidence, not normal current-cohort proof. No current-source
  three-frontend result is claimed.
- The 0729 worker only collected the proposed selectors: 18 selected tests
  (20 including two deselected parametrized items); no test body ran. The
  existing 83-pass timing and 130-pass non-timing results remain bounded
  snapshots with their recorded identities, not a blanket current pass. The
  current full baseline remains red/unqualified (`cc372` / tree `0698`,
  15,840 passed, 138 failed, 4 errors, 456 skipped, 4 xfailed); no full suite
  was requested for this correction.

## Current transcript proof and next bounded requirements (2026-10-21)

The fresh retained-transcript proof is complete for its exact source snapshot,
but this does not close Gate 1/3 as a whole and it was not replayed. The
approved source `4a50ad896b17e28f939aa3b67b8bac0b121097c5` (tree
`856769372ca7e850d3be5eb10cd069182ffc6f11`) is merged into current Agent
integration through `d0cb9b56c`; current integration is `b81ff3804606`
(tree `0ce002cd6d59c3f682e1ac6c9a7b91d29035fe81`). The proof itself ran on
the exact source snapshot, not on the later integration head, so no repeated
native/transcript run is claimed.

Exact named-suite command (the `suites.conf` entry also guards the source,
Runtime, lock, and schema identities):

```sh
test "$(git rev-parse HEAD^{tree})" = 856769372ca7e850d3be5eb10cd069182ffc6f11 && test "$(git -C /home/user/work/runtime rev-parse HEAD)" = b92d3e7a05eec65c142294ef4873edd059e9b31d && test "$(git -C /home/user/work/runtime rev-parse HEAD^{tree})" = 6abc2f117391de8e7e35c0283f575a002199894d && test -z "$(git -C /home/user/work/runtime status --porcelain)" && test "$(sed -n 's/.*\"source_commit\": \"\([^\"]*\)\".*/\1/p' runtime.lock.json)" = 95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c && test "$(sha256sum astrid/core/timeline/schema/edit-command.schema.json | cut -d' ' -f1)" = 6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d && env -i HOME=/root LANG=C.UTF-8 PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/bin ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime /home/user/work/venv-agent/bin/python -P -c 'from pathlib import Path; import astrid, runtime_protocol, pytest, sys; assert Path(astrid.__file__).resolve().is_relative_to(Path.cwd().resolve()); assert Path(runtime_protocol.__file__).resolve() == Path("/home/user/work/runtime/runtime_protocol/__init__.py"); raise SystemExit(pytest.main(sys.argv[1:]))' -q -o addopts= -p no:cacheprovider -m integration tests/editing_conformance/test_gate1_fresh_word_transcript_frontends.py::test_fresh_word_transcript_frontends_exact_pin_roundtrip
```

Result
`agt-m2-gate1-fresh-transcript-b92-one-current-proof-0751-gate1-fresh-transcript-b92-current-source-integration-1021075556-26071`:
**3 passed in 5.63s** (Python, CLI, NativeSheet). It reached exact source/pin
guards, authenticated Door/health, reload, undo/redo, outbox/restart, and
scope/lock checks. The earlier `3dcae183` result remains historical and is
not substituted for this b92 proof. No Gate-complete claim follows.

Remaining exit gaps and ownership:

1. **Gate 1 document-presence/source closure — Agent manager, current
   `astrid/sdk/timeline/document_diff.py` and its native document adapter.**
   Current integration still has the `ac9a93579` stopgap; the reviewed repair
   candidate is not integrated. The exact node
   `tests/editing_conformance/test_native_sheet_current_runtime.py::test_http_document_diff_null_presence_and_track_roundtrip_is_authenticated`
   previously reached acceptance but failed at
   `persisted_bundle(accepted) == persisted_bundle(native["bundle"])` because
   the edited occurrence materialized a new shot/shot-revision while the
   shared sibling retained the original. Finish the current-source repair and
   then authorize one bounded HTTP proof; no retry/undo claim follows from
   the withdrawn run.

2. **Gate 1 rational and shared-occurrence current-source qualification —
   Agent manager.** Run the exact current-source nodes
   `tests/editing_conformance/test_native_sheet_current_runtime.py::test_http_connected_rational_move_is_lossless_across_native_frontends`
   and
   `tests/editing_conformance/test_native_sheet_current_runtime.py::test_http_connected_occurrence_move_preserves_shared_source_across_native_frontends`
   together once after the source frontier is fixed/selected. Earlier staged
   rational/occurrence results are not relabeled as proof for `b81ff3804`.
   Do not repeat the passed transcript node.

3. **Gate 3 current-source Door qualification — Agent manager with Runtime
   manager owning the b92 Door fixture.** The exact node
   `tests/editing_conformance/test_commit_runtime_native_checkout.py::test_authenticated_v1_commit_reload_undo_survives_stopped_renderer_and_preview_reports_unavailable`
   has prior bounded evidence on another source cohort, but no run on current
   integration `b81ff3804`; therefore current-source Gate 3 remains
   unqualified. This is a qualification gap, not a newly observed renderer
   failure.

No full, browser, native, render, or replay execution was performed for this
update.

## Latest current frontier — document presence closure (2026-10-21)

The bounded AG-DOC-PRESENCE gap recorded above is now resolved as a deletion
row, without turning the result into a whole-Gate claim.

- Current Agent integration is `a9f4cfdaee40f3382b51d6cdb291d7012be96b8c`
  (tree `93862f0accf8bbe2331ed551b69839b47f7b8e1b`). The complete repair is
  merged as `b4762b7c40d4bf480494f76366cd2a51d9d6731a` from source
  `2286b2b902f505f9e59d1ca3a140a9abe05388b7` (tree
  `41c38e8dde2e4e669031686a68a2444efff8fd34`). Only the three qualified
  donor blobs were ported; the stale direct merge of `811edb816`/tree
  `7920ab3` was rejected. No public pin changed.
- The exact donor blobs remain `e61de49fc6ccbcf66ab47fb41f254c47ab8110ba`
  (`document_diff.py`), `9b5e409b2bf1f233925cb4ff5446f0d3e2676f82`
  (current authenticated proof), and
  `22a0c0d0b9705fc64d6fcfd50c66a7b4f25f692d` (authoring-feedback controls).
  The independent `e51732a64` helper and retained-context/history-shape
  review `b920a8951` remain part of the evidence basis.
- Exact authenticated proof:
  `agt-m2-document-history-reviewed-one-http-0818-document-diff-null-track-http-integration-1021081908-10363`,
  selecting
  `tests/editing_conformance/test_native_sheet_current_runtime.py::test_http_document_diff_null_presence_and_track_roundtrip_is_authenticated`:
  **1 passed in 5.51s** on Agent `b920a8951`/tree `7920ab3` and Runtime
  `b92d3e7a`/tree `6abc2f1`. Retained offline evidence is **57 passed** and
  **39 passed, 52 deselected**, with Ruff and diff checks passing.
- This closes only the unsafe old presence comparison: unsupported presence
  changes remain visibly refused with the draft retained. It does not claim
  all fields supported, whole Gate 1/WC8/M2 completion, or any change to the
  public pin. PRIVATE017 remains a separate line.

