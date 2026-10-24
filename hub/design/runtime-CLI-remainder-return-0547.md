## Report — SOURCE-GAP HANDback

- Read PLAN, author0540 report/evidence, and reviewer0544 report.
- Traced all five selectors through current source.
- No product or test files changed.
- No unchanged selector bodies rerun.

### Source findings

`_cmd_edit` calls `dispatch_ordinary_edit` at `astrid/packs/timeline/cli.py:3185`. That dispatcher only supports numeric move/trim (`cli_native.py:176-224`). Each assigned scenario returns `NotImplemented`, then uses the detached `Checkout` path (`cli.py:3190-3222`).

The actual v2 mount is `commit_edit` → `TimelineSession._flush` → `client.timelines.commit` (`cli_native.py:401-409`, `sync.py:518-550`). None of these five reaches it.

| Selector | Retained writer and arguments | Smallest owner seam |
|---|---|---|
| `test_cli_assets.py::test_edit_replace_asset_and_swap_asset_forward_to_the_sdk` | `--replace-asset BROOM=run:r/sprites#0` → `_apply_edit:3318-3323`; `--swap-asset BROOM=run:r/sprites#0` → `:3413-3414`; detached `_edit_checkout` / `Checkout` | G3 CLI adapter/emitter at `_cmd_edit`, preserving both calls and output |
| `test_cli_voice_bindings.py::test_replace_insert_and_from_script_forward_existing_sdk_arguments` | `--replace-line vo-1 --take take.wav --words take.words.json --text "New words"` → `:3271-3280`; insert and script variants → `:3281-3299` | Same G3 voice-operation adapter, preserving argument forwarding/order |
| `test_cli_voice_bindings.py::test_repeated_gap_flags_and_script_gap_override_preserve_sdk_rules` | `--from-script script.json --takes takes --gaps`, then `--gap-after vo-1=0.2`, `vo-2=0.4` → `:3294-3299`, `:3332-3338` | Same G3 adapter; preserve script-before-gap ordering |
| `test_cli_edit_flags.py::test_edit_nudge_frames_set_and_close_gap` | `--file ... --nudge-frames 3 --set x=42`, then `--close-gap-before now`; explicit `Checkout.load` at `:3194-3195`, mutations at `:3327-3328`, `:3378-3403`, save at `:3222` | G3/G5 must decide and mount the `--file` writer through C0 before deleting fallback |
| `test_cli_edit_flags.py::test_voice_line_swap_reflows_and_reports` | `--file ... --line s1 --take P --words <path>` → `:3271-3280`, detached load/save path | Same `--file` C0 migration seam |

The tests’ FakeCheckout/local-file collaborators therefore prove legacy forwarding only; they provide no C0 request, idempotency key, receipt, or accepted/merged/preview/conflict/invalid reply evidence.

### Validation

- `git diff --check` — passed.
- Worktree — clean.
- Prior exact baseline evidence: 5 passed in 6.30s, unchanged source/body/AST/import identities.
- Ruff/mypy prior evidence: zero new diagnostics.

No fixture correction was authorized because the current production path lacks C0 support for these operations. The retained writers are reachable and remain open; G3/G5 ownership must migrate them before qualification.