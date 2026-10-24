## PASS — bounded scope review

Verified exact retained scope: 30 IDs from original 267-map/reconciliation 0118.

- 24 `test_native_sheet_current.py` rows: custom-pack refusal; 8 CLI/Python/sheet parity cases; unchanged-text case; 14 unsupported-cell refusal cases.
- 4 `test_cli_native.py` rows:
  - `test_cli_matches_full_app_portable_golden`
  - `test_cli_native_preview_and_lost_ack_retry`
  - `test_cli_native_track_selector_is_parent_scoped`
  - `test_help_exposes_native_entry_and_explicit_legacy_working_copy`
- 2 Scene setup rows:
  - `test_scene_request_and_sdk_admission_keep_certified_source[False]`
  - `[True]`

Correctly excluded the 3 separately owned track-label rows and adjacent FakeCheckout nodes. No proof refs qualify these 30; prior 92/378-test results apply only to older heads and are not current behavior qualification.

## Findings

- Confirmed production replacement seam:
  `_cmd_apply` connected native path → `cli_native.commit_edit` → `NativeSheet.apply` → `TimelineSession.commit_many` → Runtime `commitTimeline`.
- The public path preserves base revision/publication, commands, labels/steps, reads/merge mode, dry-run, idempotency key, canonical accepted/merged reply, receipt, and full document adoption.
- Genuine remaining gap: detached legacy sheet fragments still use `apply_sheet` → `Checkout.save`.
- Ordinary no-`--commit` undo/redo is local working-copy behavior, not a Runtime writer; it should not be treated as an R5 retired route without an explicit PLAN decision.
- The two Scene rows do not prove a current retired `publish_parent_composition` caller. Current setup uses `service.commit_timeline`; the Scene test directly exercises the existing managed visualization executor. Do not infer a new managed Scene CLI feature. The real CLI seam is `_cmd_check` carrying a candidate into the existing managed Scene/check path.
- This census does not establish completion of all G4 writers or R5 route retirement.

No product, test, fixture, or source files changed. No tests/full/live suite run by instruction.

Checks:

```text
git diff --check        PASS
git status --short      clean
base HEAD               8657e83653f48c935f52f209516456bcb5a36282
```

Commit message and `DONE` marker were written.