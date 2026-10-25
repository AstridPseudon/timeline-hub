## Report

Produced corrected read-only evidence from exact run `1792917417224776367-32439`:

- [D111adistribution.json](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-D111a-distribution-return-0848/evidence/D111adistribution.json>)
- [D111adistribution.md](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-D111a-distribution-return-0848/evidence/D111adistribution.md>)
- [Parser](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-D111a-distribution-return-0848/evidence/D111adistribution_parser.py>)

Results: 6179.286447 ms wall, 235 samples, 20 ms interval, 4700 ms nominal coverage (76.06056201%), zero lost samples, 141.658980 ms observer CPU. Recursive frame counts are capped at one membership per sample; overlapping union is capped at 235. Exact per-sample distinct counts are `EXACTMISSING` because the retained profile has aggregate occurrences only.

Correct named timings include `deepcopy` 657 calls / 3966.175982 ms wall, `finite_json` 41 / 1501.569942 ms, and `RequestCommitPort._read` 11 / 4226.860125 ms. All operation byte fields remain `EXACTMISSING`.

Validation passed:

- Parser compile
- Arithmetic/source/JUnit/byte invariants
- Recorded source hashes verified against live sources
- JUnit: 1 test, 0 failures
- `git diff --check`

No source/product changes, rerun, optimization, or author recommendation. Verdict: `NOAUTHOR`. Original 0843 outputs were preserved. DONE and commit message markers created.