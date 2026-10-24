# FAIL — rework required

Candidate `020a2efc3897da5e809c80f76f8ed5c9376f5ef1` (tree `5d32018b…`), compared with `458595850c354f4403dabc58a72b98bebbc2c3a3` (tree `703b1aac…`). Only the allowed test file changed; worktree is clean.

Checks:

- Targeted pytest: `12 passed in 3.35s`
- Ruff: passed
- Pyright: candidate 0 diagnostics; parent 4 inherited `reportOptionalSubscript`; 0 new normalized identities/multiplicities
- In-memory compile: passed
- `git diff --check`: passed
- No skips, deselection, xfails, or guard weakening detected

Finding:

- All refusal cases use `_unavailable_base()` (`tests/test_timeline_headless_overwrite_refused.py:115`) and fail before provider construction with generic `history_unavailable`. Direct probe confirmed `provider_calls_after_refusal=0`.
- Therefore authored, hidden-content, empty-shell, and scoped-row inputs are not exercised by the authenticated provider path. The old empty publication operation and scenario-specific predicates (`stale_head`, `headless_content_not_empty`) were removed.
- Positive cases do reach the real `RuntimeService.commit_timeline()` → `RequestCommitPort.accept()` path and update the durable head, but use a generic `clip.move` plus `PreparedProvider(same=True)`, not genuine empty publication or the original raw parent/CAS inputs.
- Original test names remain, with one added legacy-410 test, but raw operation fields and receipt/event/closure/pin/integrity assertions are not preserved.

The retained full census remains `6479 passed, 36 failed, 26 skipped, 15 xfailed`; no full suite or final-gate run was performed. Commit message and `DONE` marker were written.