## PASS — F-track-label mapping

Mapped all three retained scenarios:

| Original node | Current node | Case |
|---|---|---|
| `test_track_label_dispatch_matches_native_capture[args0-\u753b\u9762 \U0001f3ac]` | `test_track_label_apply_matches_native_capture[args0-\u753b\u9762 \U0001f3ac]` | Unicode label `画面 🎬` |
| `...[args1-]` | `...[args1-]` | Empty string label |
| `...[args2-None]` | `...[args2-None]` | Clear/remove label |

Original assertions use `capture_track_set`, `source: {'via': 'cli'}`, receipt/publication `pub1`, and final label presence/value. Current assertions preserve the same command golden, receipt/publication and final-state predicates, with the intentional public route changed to sheet `show` → edit → connected `apply`, and `source: {'via': 'sheet'}`. No assertion was weakened.

Source identity:

- Original: `1794f0a2e^` / `c36ca8c94b695b0e25b7d42c89f194661f187423`
- Current: `9cd3dbe865a941c052bda04ae0d61306d18f8f26`
- Original test file SHA256: `94f395...f8f8f8?` — exact: `94f395884528cd252146d5ea2d5025cffb9633b760ae154f1943dfedc3b717c1`
- Current test file SHA256: `29d820f1623ec3b93978928a0bfbccd78cdbadc290e39c04b42ce3fee0bfcd2c`

Evidence reused:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" \
/home/user/work/venv-agent/bin/python -m pytest -q -oaddopts= \
-p no:cacheprovider --timeout=60 tests/packs/timeline/test_cli_native.py
```

Result: `11 passed in 1.63s` (CLI0404 receipt). Integrated0500 also ran the current file at `9cd`; its aggregate result was `71 + 5 + 53` passes. No test body was rerun here.

Fresh checks:

- Stdlib AST/source/predicate check: PASS; all three cases and exact predicates verified.
- `git diff --check`: PASS.
- `git status`: clean.
- No product/test files changed.

Production trace verified: `cli.py:_cmd_apply` → `cli_native.commit_edit` → `NativeSheet.load().apply` → `TimelineSession.commit_many` → generated `commitTimeline` request → Runtime `CommitExecutionCoordinator` and store `preview`/`accept` authority.

Limits: no pytest, lint, typecheck, HTTP, full-suite or original-body rerun per task restrictions.