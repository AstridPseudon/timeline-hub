## Result

Produced successor evidence under 1.4 MB:

- [rehearsal-rollup.json](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-rehearsal-rollup-return-2320/evidence/rehearsal-rollup.json)
- [rehearsal-rollup.tsv](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-rehearsal-rollup-return-2320/evidence/rehearsal-rollup.tsv)
- [dispatch-clusters.json](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-rehearsal-rollup-return-2320/evidence/dispatch-clusters.json)
- [verify_rollup.py](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-rehearsal-rollup-return-2320/evidence/verify_rollup.py)

Counts: `PRE16 / KNOWN37 / ENV73 / NEWcore424 / NEWnoncore0 / REG0 = 550`.

Bounded decisions applied:

- 97 retired-route rows → `NEW-OURS core`, preserving statuses and IDs.
- Exact 18 → historical `ENV` with authenticated `ACTUAL-PASS` overlay (`18 passed in 12.70s`).
- D67 preflight remains known gap.
- D77a daemon render is ENV, cut-blocking, proof-owed.
- P4 is `NEW-OURS core` with `KNOWN-P4` subscope flag.
- Proposal-35 and D23 named scopes retained.
- Ready clusters: Agent2318 continuation for 48; 49 ready-critical.

Validation:

- `PYTHONPYCACHEPREFIX=/tmp/agt-f-rollup-return-2320-compile-cache python3 -m py_compile .../verify_rollup.py` — pass.
- `python3 .../verify_rollup.py` — pass.
- Exact JSON/TSV membership parity — pass, 550 unique rows.
- `git diff --check` — pass; worktree remains clean.

No product tests, lint, or full suites were run per brief. No blockers. `commit-msg` and `DONE` were written.