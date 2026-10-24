## Report

- No code changes made; worktree remains clean.
- Traced strict binding path:
  - `clip.anchor` requires `parent/clip:*`.
  - Child legacy word anchors are intentionally unresolved.
  - Timing compilation therefore requires an authenticated binding unavailable for `occ-film/film/inside.on`.
- Compared passing fixtures using `build_transcript`, exact document pins, stable `word_ids`, and Runtime `transcript_source` hydration. They only support parent typed anchors.
- Known failure evidence: setup fails with `missing exact word binding for ('occ-film', 'film', 'inside').on` before the helper body; the known-bad test was not rerun.
- Checks:
  - `git diff --check` — passed.
  - AST inspection confirmed original parameters/assertions unchanged: 4 parameters, 5 assertions.
- Precise gap returned to owner: a faithful repair requires an authoritative fixture/product seam for child word binding or a settled change to the original target semantics. No fake manifest, caller capture, weakened guard, or product edit was applied.
- `DONE` and commit message were written.