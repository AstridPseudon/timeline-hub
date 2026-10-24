Blocked — no safe code change made.

- Current fixture is not genuine: `_seed_fixture` directly accepts a fabricated `clip.move` record (lines 80–120), outside `commitTimeline`.
- Runtime bootstrap only creates an empty closure; no supported setup path here installs the required shared `occ-a`/`occ-b` closure with real history and custody.
- Retained failure: `test_exact_capture_acceptance_inverse_redo_restart_and_retry[image-add]`; Agent `astrid/sdk/timeline/commit.py:1019`, wrapped by Runtime `runtime_protocol/service.py:2504`.
- No production defect claimed; all 48 remain CORE-OPEN.
- Tests intentionally not run per brief. `git diff --check`: passed.
- Wrote `BLOCKED` and commit message. Next step: owner-provide a supported complete-closure fixture/API, then run the targeted integration test.