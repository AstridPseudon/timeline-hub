# D118d report

- Updated only [`tests/sdk/test_timeline_capture_projection.py`](/home/user/work/wt/app-D118d-projection-first-return-1551/tests/sdk/test_timeline_capture_projection.py), projecting Runtime child reads to the exact canonical-document fields used by the genuine public caller.
- Preserved all authored inputs, assertions, goldens, pins, opaque fields, ordering, and topology. Test ASTs unchanged.
- Checks passed:
  - Ruff
  - py_compile
  - mypy
  - `git diff --check`
- Own 9-node run: NOTRUN. `/tmp` had 4,953,280,512 bytes, below the required 5,000,000,000-byte floor. Prior protected run failed before the commit path at the malformed row shape.
- Evidence: [facts.json](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-D118d-projection-first-return-1551/evidence/facts.json), [facts.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-D118d-projection-first-return-1551/evidence/facts.md).
- Commit message written; `DONE` created. Next step: run the exact own-node command once disk admission reaches 5 GB, then obtain protected review.