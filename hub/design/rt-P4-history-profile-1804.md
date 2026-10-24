## Report

- Profiled existing genuine control: `test_redo_reopens_exact_retired_images_with_one_native_write`.
- Result: **1 passed in 27.77s**, exit 0.
- Runtime remained at `327da207ed30880fe2ae0cd0b116722bb2c6f7a6`; worktree clean. No product/test changes.

Measured:

- 107 `_historical_sequential` calls.
- 110 sequential-capture validations.
- 440 canonical-document and 220 recorder schema validations.
- 1,418 finite-JSON walks; 2,817 observed digest calls.
- Inclusive profiled CPU: schema validation 17.41s, historical sequential 18.55s, image capture 1.27s, digest 0.49s.
- SQLite whole-control CPU was comparatively small (~0.37s across execute/fetch calls), not isolated solely to historical calls.

Evidence:

- [observer aggregates]( /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-P4-history-profile-1804/evidence/redo-history-observer.json)
- [raw cProfile]( /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-P4-history-profile-1804/evidence/redo-history.prof)
- [test XML/log]( /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-P4-history-profile-1804/evidence/redo-history.xml)

Timings are inclusive and observer/cProfile overhead applies; they are not uninstrumented latency claims. The result supports repeated schema validation as the dominant measured work, without establishing the original P4 cause. No blockers. Commit message and `DONE` marker were written.