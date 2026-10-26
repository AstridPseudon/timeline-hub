# F/D141 review validation

Status: `PASS`.

## Exact read-only checks

- `python3 /tmp/w-bf1fcdf9b4/independent_check.py` → `PASS source_hashes=14 rows=370 roots=52 unique=370 pristine=3082+173=3255 matches=21 upstream=y21/n3/UNKNOWN346 pending=370`.
- The checker used only Python standard-library `json`, `csv`, `hashlib`, `pathlib`, `re`, and `collections`; it checked every source-manifest hash, all D134 row fields/frames, root membership, exact pristine records/statuses, upstream-basis policy, notes-input root membership, and the independent review rulings.
- Read-only Git object/tree checks for all eight frozen tuple commits → all commit objects and expected trees resolved exactly.
- Markdown/JSON table comparison → `370` Markdown rows, `370` JSON rows, `0` mismatches.
- Assigned worktree `git status --short` → clean.

## Retained facts

- D134: `370` unique IDs, `52` disjoint roots; scope `344 OURS_NEW_FILE + 14 UNVERIFIED_CURRENT_REG + 12 PRIOR_UNKNOWN`.
- Pristine: `3082` concrete IDs plus `173` explicit null-ID aggregate records; `3255` records total; `PASS=3250`, `FAIL=4`, `ERROR=1`.
- D134-row pristine matches: `17 PASS`, `3 FAIL`, `1 ERROR`; unmatched rows: `349 UNKNOWN`.
- Upstream presence: `y=21`, `n=3`, `UNKNOWN=346`.

No product/test execution was attempted because this task is documentary-only and explicitly excludes those lanes. No current cut XML exists; current statuses and final classifications remain pending.
