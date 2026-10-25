Implemented the U1/D135 Farm preflight correction in the private packet:

- Enforced exact Runtime/Agent commit and tree identities.
- Required `/home/user/work/venv-agent/bin/python` as CPython 3.13.
- Enforced declared dependency versions and accumulated all prerequisite failures.
- Added transitive local-origin guards and platform-optional AST handling.
- Fixed JUnit `<testsuites>` child aggregation and malformed/missing XML refusal.
- Preserved 21 source hashes, 7 AST manifests, and the six-file argv.

Validation:

- Ruff, JSON validation, private compile, and `git diff --check`: PASS.
- Frozen source audit: 21/21 hashes, 7/7 AST manifests.
- Negative census: exit 1 as expected; all seven imports attempted; all findings accumulated.
- XML controls: single/multiple positive and malformed/missing negative cases passed.
- Farm preflight and six-file body: NOTRUN.

Evidence: [preflight.py](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-U1-Farm-preflight-return-2127/evidence/preflight.py), [validation.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-U1-Farm-preflight-return-2127/evidence/validation.md), [readiness.json](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-U1-Farm-preflight-return-2127/evidence/readiness.json).

Commit message and `DONE` marker are present. Next step: run the recipe on Farm with the receipted exact checkouts, then authorize the six-file body only after preflight PASS.