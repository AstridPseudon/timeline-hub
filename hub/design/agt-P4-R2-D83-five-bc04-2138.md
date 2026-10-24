## Report

- Submitted one authorized five-selector batch on Runtime `bc04...04702a`; one zero-body harness replacement was required due manifest self-copy. No original rerun after meaningful failure.
- Tuple:
  - Agent `197d780dca51949605c02352e7d1089a087aaa11`
  - Runtime `bc04caa23f4b503fc55e49769ead20677904702a`
  - App `245742dc778977a8404be2d1a7bc3b8721267416`
  - Composition `635f4de06fda22a85fc2e4cfc764d0153a4c9f40`

Preflight:

- Registry CAS install and repair passed; outside rows byte-identical.
- `bash -n`: exit 0.
- Positive probe: exit 17, one stub call.
- Wrong-SHA poison: nonzero, zero stub calls.
- Disk remained ≥8 GB; evidence size 660 KB.
- `P4_LIVE_PROFILE_DIR` unset.

Service:

`request-test integration:agent p4-current-becfe-http-3legs --no-cache`

- Zero-body ID: `agent-p4-current-becfe-http-3legs-1024214113-31062`
- Replacement ID: `agent-p4-current-becfe-http-3legs-1024214145-6749`
- Final result: automatic candidate-scope NO-GO, exit 1.
- Outcomes: 2 passed, 3 timed out; JUnit 218.304s, service wall 222s.

Timings:

`ten-note` 45.242s FAIL; `[False-None]` 45.006s FAIL; `[False-public-element]` 45.010s FAIL; `[True-None]` 39.261s PASS; `[True-public-element]` 40.053s PASS.

Evidence: [outcomes.tsv](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-P4-R2-D83-five-bc04-2138/evidence/outcomes.tsv), [JUnit](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-P4-R2-D83-five-bc04-2138/evidence/p4-r2-d83-unprofiled-five.xml), [receipt](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-P4-R2-D83-five-bc04-2138/evidence/service-receipt.txt).

No product edits; worktree is clean. Commit message and `DONE` created.