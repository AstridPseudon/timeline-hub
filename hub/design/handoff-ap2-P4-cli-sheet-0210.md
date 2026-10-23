# Handoff: ap2-P4-cli-sheet-0210

Source: Agent worktree at joined R2/G3 schema source `68f2b23f` (`hub/tl/agt-R2-G3-schema-join-0157`).

Added `tests/sdk/test_p4_cli_sheet_v2.py` only. It exercises the installed timeline parser/handler and real `NativeSheet` adapter against the persisted scoped outbox. The generated client method is the explicit fake boundary; acceptance still uses the repository command engine and canonical document compiler.

Evidence:

- exact targeted pytest: `2 passed, 1 xfailed, 1 warning`;
- ruff: `All checks passed!`;
- mypy: `Success: no issues found in 1 source file`;
- `git diff --check`: clean.

The strict xfail is intentional. The actual caller is `_cmd_apply` → `cli_native.commit_edit(sheet=True)` → `NativeSheet.load(...).apply` → `TimelineSession.commit_many`, which emits `clip.move`, empty step patches, and `merge: fields`. It does not call `Timeline._capture_free_edits` → `emit_document_commands`. Therefore the test records the original edit and unchanged closure fields but keeps the required v2 doc.patch expectation red.

Missing/simulated reply coverage is explicitly named in `report.md`: generated transport does not provide step dependencies/merge mode, conflict/invalid details, authenticated preview status, or history. No H3 GO/P4 DONE claim.
