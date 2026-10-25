## Report — F-R1/V2

Joined only the three reviewed production blobs onto normal `657bc2e8db`:

- `_commit_patch.py` → `7d4db9a32d`
- `native_word_anchor.py` → `edeb0a2425`
- `_commit_timing_validation.py` → `a5496a6d2a`

Baseline equivalence to common `7e23790248` passed. No tests, fixtures, locks, generated files, schemas, or pins changed.

Checks passed:

- In-memory compile: baseline and candidate
- Ruff: baseline and candidate
- Mypy: baseline and candidate
- Exact reviewed blob and AST equality
- Outside-file hash equality
- `git diff --check`
- Forbidden-path audit

Behavioral MAIN proof was not run; candidate remains `productcandidateHOLD` pending the later exact 8-target proof plus optional targets.

Evidence: [metadata](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-Agent-candidate13-join-0336/evidence/f-r1-v2-source-metadata.md>)

Commit message written for `F-R1/V2`; `DONE` created.