Implemented the reviewed raw-audio trim delta from `9bf503f9` onto current `3c4f6de4`.

Changed only seven intended files; blobs match reviewed `9bf503f9`. Preserved schema, client, artifact, and current ordinary-source bytes. Vendor check against `a0dca169` passed.

Tests:

- `test_recipe_m2_clip_trim.py`: 122 passed
- CLI/provider lane: 126 passed
- Parent-media lane: 25 passed
- Ruff, `py_compile`, `git diff --check`: passed

The exact `9bf/7d1` Runtime historical-audio pair remains unqualified and was not duplicated. Runtime authority mismatch is documented as the blocker and future gate in [report.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-raw-trim-current014-source/report.md).

Wrote `commit-msg`, `commit-msg.txt`, and `DONE`.