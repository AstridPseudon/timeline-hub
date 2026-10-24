## Report

Created corrected finite evidence artifacts:

- [276-row JSON](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-core-counts-return-1343/evidence/d54-current-rollup-return-1343.json)
- [276-row TSV](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-core-counts-return-1343/evidence/d54-current-membership-return-1343.tsv)
- [Count assertions](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-core-counts-return-1343/evidence/d54-current-count-assertions-return-1343.json)

Results:

- 276 unique rows: 159 core, 117 non-core.
- Qualification: 162 PASS, 112 open, 2 deferred.
- Core: 152 PASS, 5 blocking open, 2 D23 deferred.
- Non-core: 10 PASS, 107 open.
- Categories: 78 env, 2 deferred, 196 UNPROVEN.
- Current core: 152 PASS / 6 FAIL / 1 UNKNOWN; required blocking set: 152 PASS / 4 FAIL / 1 UNKNOWN.
- D23 now covers exact orders 170 and 213.
- Current FAIL overrides prior PASS for orders 98 and 99; historical 164-qualified claim is retained as historical only.
- Complete v2 request/reply field scope and production caller evidence are preserved.

Validation:

- JSON parsing: PASS.
- Finite 276 uniqueness, sums, XML membership/parameters, category counts, and FAIL-not-qualified contradiction checks: PASS.
- `git diff --check`: PASS.
- No product/test/registry changes or test bodies rerun. Final 924/full regression comparison remains unverified.

Created the required commit message and `DONE` marker.