## Report

Updated only the two assigned test oracles:

- Added `timeline.restructure` with `{}`.
- Added `clip.duplicate-media` with valid closed `id`, `old_media`, and `media` selections.
- Extended the provider-only operation set to five.
- Preserved the 30 wire tuples, 58 definitions, canonical/unknown/refusal assertions, and schema fingerprint.

Tests:

- `test_timeline_composed_schema.py`: 6 passed.
- Relevant union/oracle checks: 3 passed.
- Existing provider registry negatives: 13 passed.
- Direct `validate_command` positives and malformed missing/extra/wrong-type cases: passed.
- Scoped Ruff: passed.
- Full current-union file: timed out at 45s after 8 tests; no assertion failure observed.

No generated/schema/source/pin files changed. Completion marker and commit message were written.