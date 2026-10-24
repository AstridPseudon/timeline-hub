# Report: G5 miscellaneous terminal diagnosis

No repository, test, fixture, generated, profile, pin, dependency, or harness files were changed. Worktree remains clean.

Pinned evidence:

- Agent: `c36ca8c…`, tree `50689a…`
- Runtime: `8ea0766…`, tree `6047ac…`
- Retained full run: `17,159 passed, 262 failed, 5 errors, 4 skipped`; exit 1.
- No retry, targeted test, pytest body, or test service was run.

For all items below, “proof” means failure evidence only; no repair is currently pass-qualified.

1. `test_edit_nudge_frames_set_and_close_gap` — call phase  
   Cause: retained assertion requires `next:` to be the final output line, but `_cmd_edit` prints the idempotency advisory afterward. Current production AST is unchanged; current HEAD has a test-only assertion adjustment in `1794f0a2e`. Failure is terminal-qualified; current fix is not rerun-qualified. Owner: Agent CLI test owner. Next: rerun the current test-only oracle adjustment.

2. `test_voice_line_swap_reflows_and_reports` — call phase  
   Same output-order cause and same test-only current-tree adjustment. Owner/action: same as item 1.

3. `test_track_label_dispatch_matches_native_capture[args0-画面 🎬]` — call phase  
   Cause: c36 invokes retired `edit track-label`; current parser rejects positional `t`. Current HEAD has a test-only migration to `show --as sheet --native` → `apply`; production AST unchanged. Terminal failure is qualified; migrated route is not rerun-qualified. Owner: G5/CLI test owner. Next: rerun the migrated sheet-path case.

4. `...[args1-]` — call phase  
   Same retired-route/parser cause, with empty-label input. Same owner/action.

5. `...[args2-None]` — call phase  
   Same retired-route/parser cause, with clear-label input. Same owner/action. Preserve parent-scoped selection and no-write assertions.

6. `test_d13_installed_native_preflight` — call phase  
   Cause: required D13 environment was absent; retained output names missing source profile, bindings, Node/Remotion/browser/FFmpeg/FFprobe inputs and profile `.`. Current AST unchanged. This is source/artifact-classified, not installed-positive-qualified. Owner: D13 installed-environment/farm owner. Next: run only with the manager-selected installed tuple and regular profile; do not synthesize bindings or claim prior D13 source checks as this proof.

7. `test_p4_sources_are_real_and_parseable` — call phase  
   Cause: `cases.json` names `test_ordinary_edit_literal_move_uses_native_outbox`, while the actual source function is `test_ordinary_edit_literal_move_uses_commit_outbox`. Current AST/data are unchanged. Failure is source-qualified. Owner: P4 fixture owner. Next: update only the stale symbol metadata, then rerun the bounded P4 source test.

8. `test_bootstrap_environment_is_accepted_by_the_remotion_probe_context` — call phase  
   Cause: the deliberately clean child receives only repository `PYTHONPATH`; importing `tests.conftest` then fails on missing `runtime_protocol`. Current AST unchanged. Source/environment-classified, not bootstrap-positive-qualified. Owner: test environment/Runtime import-fence owner. Next: repeat with the pinned Runtime tree explicitly available to the clean child and record module origins; do not weaken the clean-environment contract.

9. `test_repair_restarts_real_runtime_for_failed_service_and_preserves_healthy_pids[False-0]` — call phase  
   Cause chain reaches `Backend.runtime`, which invokes `version.python -I -m astrid_runtime`; the retained record contains only `CalledProcessError` and no child stdout. Static artifact evidence shows `astrid_runtime` exists in the Runtime checkout but not in the shared Agent venv site-packages. Exact child failure remains unconfirmed. Owner: installer/installed-runtime environment owner. Next: reproduce in a private, properly installed Runtime environment while retaining child output.

10. `...[True-1]` — call phase  
    Same pre-service failure before the log-open branch, so the `fail_log_open` and port offset semantics were never exercised. Same owner/action. Do not attribute this to service repair logic yet.

11. `test_a_missing_runtime_is_not_looked_for_in_the_default_lane_and_fails_in_the_integration_lane` — call phase  
    Cause: nested pytest child inherits harness `PYTEST_PLUGINS=origin_plugin_2215`, but its temporary cwd cannot import that plugin; lane logic is never reached. Source/environment-classified. Owner: observer/test harness environment owner. Next: sanitize harness-only plugin variables for nested lane probes, then rerun the exact default/integration assertions.

12. `test_a_module_of_a_lane_the_run_deselects_is_not_imported_and_fails_in_the_run_that_selects_it` — call phase  
    Identical pre-lane `origin_plugin_2215` import failure. Same owner/action; no lane behavior credit.

13. `test_document_publish_forwards_new_stale_head_to_runtime` — call phase  
    Cause: production changed from `fetch_bundle` to the opened session’s `_bundle` seam in `c2584a014`, but the retained test still monkeypatches nonexistent `helper.fetch_bundle`, producing `AttributeError`. Current production/test AST is unchanged from c36. Source-qualified seam mismatch; stale-head/no-write behavior remains unverified. Owner: timeline document-publication test owner. Next: retarget the test to the current session-open/bundle seam while preserving exact revision/publication assertions, stale-head refusal, and no-write checks.

The only relevant current-tree delta is test-only CLI migration in `test_cli_edit_flags.py` and `test_cli_native.py`; it does not retroactively qualify the c36 full run or the other eight nodes.

Operational `commit-msg` and `DONE` markers were created as required.