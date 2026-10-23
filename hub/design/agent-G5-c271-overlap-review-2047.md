Verdict: evidence PASS; causal qualification FAIL. Source owner: Agent R2 (`_step_undo.py`), not Runtime. Do not mark whole-body PASS.

- Replayed retained packet SHA `8bf50ade…`; forward restructure, undo, redo, and later `bed.volume 0.5→0.25` edit all accepted.
- Refusal was no-write: SQL, head, and history unchanged.
- Exact failure: redo publication `txn-cf7414…` fails `_step_undo.py:185` because its root `config` effect is compared against a seed containing only `config.clips`. This is valid accepted history, not malformed evidence.
- Therefore strict nested-history authentication runs before the later-overlap guard and misreports the legitimate overlap as `history_unavailable` instead of `intervening`.

Checks:

- Targeted pytest: `71 passed in 56.66s`
- Ruff: passed
- Mypy: no issues in 3 files
- Diff, vendor-lock, and artifact-manifest checks: passed
- Worktree unchanged; no source/test edits.

Recommended next step: fix the existing Agent R2 seam in `_native_mirror_partition` to handle root/config write ordering, preserving strict malformed-history rejection and the original overlap assertion.