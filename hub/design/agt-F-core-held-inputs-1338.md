## Report

- D23 explicitly covers both failures:
  - `tests/sdk/test_timeline_helper_capture.py::test_cut_nudge_restart_merges_other_cut["second"]` (line 222), missing `('occ-film', 'film', 'inside').on` binding.
  - `tests/sdk/test_timeline_persistence.py::test_publish_after_a_restart_merges_other_clips_onto_the_moved_head` (line 711), missing `('occ-A', 'A', 'a-rocket').on` binding.
- Therefore order213 is covered by existing owner approval; no invented deferral is needed. Both remain unchanged and visibly deferred under D23 relational timing.

D13 remains held/UNKNOWN. The ordinary installed profile is insufficient: the preflight separately requires `ASTRID_D13_SOURCE_PROFILE`, a regular `ASTRID_D13_EXPECTED_BINDINGS` JSON containing exactly seven keys, and current Node/Remotion/browser/ffmpeg/ffprobe paths plus hashes. Existing reports identify the materialized seven-key binding carrier as missing. No input was fabricated or relabeled.

Inspected selectors and harness source with `rg`, `sed`, and `nl`; no tests or original bodies were rerun per task limits. Worktree remains clean; no production/test/fixture changes. Commit message and `DONE` marker created.

Next step: the environment owner must provide the existing approved seven-key D13 binding carrier and matching current tool tuple; then perform only the prescribed preflight/collection checks before any native proof.