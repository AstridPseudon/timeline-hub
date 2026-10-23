# Handoff: ap2-P4-cli-sheet-first-return-0218

## Result

The first return is corrected and targeted evidence is green. The earlier
0214 claim that this path was a G3 defect was false: the installed production
caller uses the valid semantic sheet route.

The updated test uses the actual original
`tests/sdk/test_timeline_sync.py::initial_bundle` unchanged. Its parent clip
`a` starts at `0`, FPS is `30`, and the test edits only the bound `at` cell to
`5`. It asserts the exact `capture_move(original, "parent/clip:a", 5)` command,
including captured reads, exact `r0`/`pub0` base, `Apply sheet`, `sheet-1` with
tags `sheet`, ordinal `0`, and submitted `patch: []`; it also asserts
`merge: fields`, `source: {"via": "sheet"}`, `dry_run: false`, and the
`p4-cli-sheet-v2` idempotency header.

Accepted state is compared structurally to
`execute(original, [capture_move(original, "parent/clip:a", 5)]).bundle`, so
all original IDs, strings, raw values, absence, ordering, and closure are
preserved except for the authored move and the proven native-derived
`app.astrid.fixed_start/for` fields.

## Production path established

The test exercises the actual parser → handler → NativeSheet → semantic helper
→ persisted session/outbox path:

```text
cli._cmd_apply
  -> cli_native.commit_edit(sheet=True)
  -> NativeSheet.load(session).apply
  -> NativeSheet.preview / clip.move capture
  -> TimelineSession.commit_many
  -> TimelineSession._flush / client.timelines.commit
```

The generated-client boundary remains the only fake transport boundary. No
emitter, semantic executor, provider, or outbox behavior is stubbed.

## Checks

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime /home/user/work/venv-app2-native/bin/python -m pytest -q tests/sdk/test_p4_cli_sheet_v2.py tests/sdk/test_p4_commit_cases.py
3 passed, 1 warning in 1.37s

/root/.local/bin/ruff check tests/sdk/test_p4_cli_sheet_v2.py
All checks passed!

/root/.local/bin/mypy --follow-imports=silent tests/sdk/test_p4_cli_sheet_v2.py
Success: no issues found in 1 source file

git diff --check
PASS
```

The pytest warning is the pre-existing unknown `timeout` option. No full or
Runtime/browser/live-socket suite was run.

## Remaining scope

This is not Runtime acceptance, CLI history/show readback, ten-note end-to-end,
H3, or a P4DONE claim. The generated transport fake does not supply complete
accepted/merged canonical closure/digest/head/receipt/commands/steps/
dependencies/merge-mode wire evidence, nor conflict reason/head, invalid
code/path/hint/suggested-command, or preview `would_status`/history evidence.
Those remain separate next steps, along with the pending ten-note one-commit
and guarded per-step undo proof. Earlier reviewed provider13 and fn3 proofs
remain scoped and are not invalidated by this pending collection manifest.

