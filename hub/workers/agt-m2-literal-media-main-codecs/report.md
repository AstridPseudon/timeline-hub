## Completed

- Added native `clip.trim v1` with source-unit `hold` semantics.
- Updated `clip.split` to accept MIME media types via the shared normalizer.
- Preserved static `fixed_start`/`for` intent from `clip.move`.
- Added split, trim, model-parity, refusal, and provider undo coverage.
- Wrote required commit messages and report.

## Verification

- Targeted tests: **415 passed, 17 deselected**
- Ruff: passed
- `git diff --check`: passed
- Full/browser/install/network suites: not run.

Report: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-literal-media-main-codecs/notes/report.md`

No blockers.