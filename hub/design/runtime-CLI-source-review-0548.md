## Report — rt-F-CLI-source-review-0548

Result: **PASS for source-boundary review; FAIL for C0 qualification of all five scenarios.**

Reviewed Agent `2007cf7aaf5d304964e68a33e967502a16de1d24` and Runtime `1d9ddba546f8fb1300f55ff62607ed492719cbaa`; frozen refs were read with `git show` only.

Findings:

- `test_cli_assets.py::test_edit_replace_asset_and_swap_asset_forward_to_the_sdk`
- `test_cli_voice_bindings.py::test_replace_insert_and_from_script_forward_existing_sdk_arguments`
- `test_cli_voice_bindings.py::test_repeated_gap_flags_and_script_gap_override_preserve_sdk_rules`

All bypass `dispatch_ordinary_edit` because they are neither numeric move nor trim. They enter `_edit_checkout()` and `_apply_edit()`, then `Checkout.save()` at `cli.py:3222`. Their green assertions prove exact SDK arguments, ordering, and replacement output only. The live CLI route is not dormant; G3/G5 owns migration if these are promised film edits.

- `test_cli_edit_flags.py::test_edit_nudge_frames_set_and_close_gap`
- `test_cli_edit_flags.py::test_voice_line_swap_reflows_and_reports`

Both use `--file`, which explicitly selects `Checkout.load()` and local `Checkout.save()`. They prove local document transformation and reload behavior, not Runtime film authority. They may retain faithful offline forwarding/local-edit credit, but have no C0 qualification.

The existing numeric C0 path is distinct:

`dispatch_ordinary_edit()` → `commit_edit()` → `TimelineSession.move/trim()` → `_flush()` → `client.timelines.commit()` → Runtime `/v1/projects/{project}/timelines/{timeline}/commit`.

The existing semantic emitter is `astrid/sdk/timeline/emitter.py`, reached through `Timeline._capture_free_edits()` and `Timeline.commit()`. No new API or emitter is indicated.

Absent from all five scenarios: the C0 request envelope, HTTP idempotency key, Runtime mount, accepted/merged/preview/conflict/invalid reply, canonical document/head/revision/digests, records/effects/bindings/dependencies/history/undo steps/receipt, attribution, and retry guards.

Tests were not rerun per the read-only/unchanged-original instruction. Prior evidence reviewed: the five exact selectors passed, **5 passed in 6.30s**, with unchanged source/body/AST/import identities; no source files changed. Worktree remains clean.

Required `commit-msg` and `DONE` marker were created. No blockers beyond the five intentionally open C0 qualifications; next step is an Agent-owned G3 adapter review if Runtime film authority is required.