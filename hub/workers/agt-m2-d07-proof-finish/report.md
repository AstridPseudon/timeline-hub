## Completed

- Added native/compiler conformance proof for grouped `clip.trim` + `clip.move`:
  - Visual clips become `[0,1.5)` and `[1.5,2.5)`.
  - Source window `[8,9)` and audio `[0,2)` remain unchanged.
  - Compiled parent duration is `2.5`.
- Added SDK lazy-export relocation assertions.
- Removed stale detached retime guidance/imports from the three named docs.
- Wrote commit message and created `DONE`.

## Tests

- Reviewer command plus new proof/helper tests: **36 passed**
- `test_recipe_m2_clip_trim.py` + helper tests: **90 passed**
- Focused SDK facade tests: **4 passed**
- `git diff --check`: passed
- No full suite requested.

A broader combined suite hung after six visible passes and was stopped; it is unverified. No blocker remains for this bounded task.