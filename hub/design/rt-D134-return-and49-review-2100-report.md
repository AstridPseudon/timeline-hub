## D134 report

- Verdicts: A PASS; B PASS with M1 behavior UNKNOWN; C PASS.
- A retained Runtime `6634a17f`; migrated Agent identity to current `a30e74e9`, preserving all seven cases and predicates.
- B verified current Agent/Runtime `a30e74e9`/`ab1e4f61` consistency. Two files changed; M1 remained byte-identical. Archive exists, but `on` behavior remains UNKNOWN.
- C verified 49 disjoint IDs: 35 fixture/setup, 22 UNKNOWN, 0 proved product gaps. Missing request/record/caller evidence was not reconstructed.
- Original 2045 assessments and 2046 `FAIL_AUTHORITY_CLAIMS` were preserved.

Validation:

- Branch scope and `git diff --check`: PASS.
- AST predicate/assert/raise conservation: PASS.
- Source blob and first-frame verification: PASS, 49/49.
- Ruff, private `py_compile`, and scoped mypy: prior PASS results reused against identical finalized blobs.
- Functional tests: NOTRUN; free space remained below the 5 GB admission floor.

Evidence written:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-D134-return-and49-review-2100/evidence/`

Commit message and `DONE` marker created.