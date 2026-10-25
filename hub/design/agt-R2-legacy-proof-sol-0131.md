Candidate complete on base `2050221347a536d0fd698817c4a200004f960564`; no merge performed.

- Updated [inverse.py](/home/user/work/wt/agt-R2-legacy-proof-sol-0131/astrid/sdk/timeline/inverse.py:1007) to expect the complete stage materialization set when those claims accompany effect proofs. Effect-only v2 stages retain their existing requirements.
- Added a four-case provider regression covering legacy/v2 proof representations, whole/step redo, preview no-write, and full canonical equality.
- Preserved every original test body/decorator and the complete fork-proof matrix. `_commit_patch.py`, `commit.py`, Runtime, net-zero expectations, and replace-existing remain unchanged.

Source-only validation:

- `python3 /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-legacy-proof-sol-0131/evidence/source_checks.py` — PASS: AST, in-memory compile, source hashes, predicate conservation, baseline/candidate scoped Ruff and mypy.
- `git diff --check` — PASS.
- Exact tool commands and results: [source-checks.json](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-legacy-proof-sol-0131/evidence/source-checks.json).

No tests, collection, fixtures, services, or probes ran. Functional behavior remains unverified. Independent protected review and actual MAIN candidate qualification of the original redo cases and strict controls are required before merge; [focused selectors](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-legacy-proof-sol-0131/evidence/selectors.txt) are provided.

Evidence is 68 KB. Conventional commit message and `DONE` marker written for the harness.