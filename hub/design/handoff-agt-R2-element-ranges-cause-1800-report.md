# R2 source-cause report

Source-cause result: PASS — cause proved, not behavioral qualification. All four remain core-unknown until repaired and qualified.

1. `existing=None, params=None` → helper `_calls` emits equal-value `clip.set` → Agent produces non-empty native range with empty effect range `[0,0]`; Runtime auth rejects `effect_start < effect_end` at `_inverse_stage_ranges:1360` → Agent helper/producer: `astrid/sdk/timeline_elements.py`, `_commit_patch.py`; Runtime repair proposal: change only `<` to `<=`, preserving contiguous coverage, native ranges, source bindings, and final guards.

2. `existing=None, params={}` → same accepted `['clip.set']` shape because `{}` is falsy → same proved Runtime rejection → same disjoint files and minimal Runtime-only repair.

3. `existing={}`, `params=None` → same accepted `['clip.set']` shape; existing params do not alter the command → same proved Runtime rejection → same disjoint files and minimal Runtime-only repair.

4. `existing={}`, `params={}` → same accepted `['clip.set']` shape → same proved Runtime rejection → same disjoint files and minimal Runtime-only repair.

Evidence:

- Retained traceback reaches `runtime_protocol/timeline_commit_auth.py:1360`, after the inverse request and before inverse execution.
- C0 permits empty semantic/authoritative effect patches and requires ordered coverage, not non-empty per-stage effect ranges.
- Retained positive comparator `test_inverse_aba_partition.py` provider-produces `[0,0]` and completes inverse/redo/preview successfully.
- D72 cleanup is disjoint: `_orphan_cleanup` returns no cleanup when the old and selected element refs are equal.
- Source pins: old helper `ecee31fe20427add52c87e2cdf782379173baa05`; current helper `bfd22e2b58082db71131cf27bd976d3bd18a76d9`; current producer `b420634307da60e560e70c5b34eca7c636fc22c1`; current consumer `57c246395cf662d831f100522f2ce45c0bb5b708`; Runtime auth `fe9a673704de4854ec79de9e1b6150215e024ee8`.

Validation:

- `git diff --check` — PASS.
- AST parse of the four current source files with `PYTHONDONTWRITEBYTECODE=1` — PASS.
- No product/test changes, original-body rerun, or behavioral suite run.

Worktree remains clean. Required `commit-msg` and empty `DONE` markers were created.