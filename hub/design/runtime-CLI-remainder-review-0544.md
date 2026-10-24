## Result: FAIL

The five exact selectors passed, but they do not qualify current G3/G5 C0 behavior.

| Original node | JUnit | C0 credit | Finding |
|---|---:|---:|---|
| `test_cli_assets.py::test_edit_replace_asset_and_swap_asset_forward_to_the_sdk` | PASS | No | `FakeCheckout` patched; detached path |
| `test_cli_voice_bindings.py::test_repeated_gap_flags_and_script_gap_override_preserve_sdk_rules` | PASS | No | `FakeCheckout`; no Runtime request |
| `test_cli_voice_bindings.py::test_replace_insert_and_from_script_forward_existing_sdk_arguments` | PASS | No | `FakeCheckout`; no Runtime request |
| `test_cli_edit_flags.py::test_edit_nudge_frames_set_and_close_gap` | PASS | No | `--file` forces `Checkout.load/save` |
| `test_cli_edit_flags.py::test_voice_line_swap_reflows_and_reports` | PASS | No | `--file` forces `Checkout.load/save` |

The reconciliation JSON independently marks all five `active_owner`, `open_held_or_unknown`, with empty post-proof references and `qualifying_original_behavior_credit: false`.

Evidence reviewed:

- Exact Agent base: `2007cf7aaf5d304964e68a33e967502a16de1d24`
- Exact Runtime source: `1d9ddba546f8fb1300f55ff62607ed492719cbaa`
- Retained JUnit: 5 passed in 6.30s; no skips/failures
- Source/body/AST identities: unchanged
- Import origins: pre/post paths equal
- `git diff --check`: passed
- Artifact and CLI-surface checks: passed
- Ruff: 2 existing diagnostics, zero new
- mypy: 2 existing diagnostics, zero new
- Evidence size: approximately 68 KB

The actual v2 mount is `_cmd_edit` → `dispatch_ordinary_edit` → `commit_edit` → `TimelineSession._flush` → `client.timelines.commit`. None of these five scenarios reaches that route. No captured C0 request, HTTP idempotency key, receipt, or accepted/merged/preview/conflict/invalid reply exists. Consequently, request fields and reply guards—including canonical document, digests, records, dependencies, history, undo steps, refusal attribution, and retry preservation—remain unverified.

Exact production seam: [`astrid/packs/timeline/cli.py:3185`](/home/user/work/wt/rt-F-CLI-remainder-review-0544/astrid/packs/timeline/cli.py:3185) falls back to detached `Checkout` editing after native dispatch returns `NotImplemented`; [`cli_native.py:213`](/home/user/work/wt/rt-F-CLI-remainder-review-0544/astrid/packs/timeline/cli_native.py:213) only dispatches ordinary numeric move/trim.

No files were changed; no merge is needed. Recommended next step: migrate or separately qualify these five writer families through the G3 emitter/C0 route, preserving every original assertion, then rerun the exact selectors with captured request/reply evidence.