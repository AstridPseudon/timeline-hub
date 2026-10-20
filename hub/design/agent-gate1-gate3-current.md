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
