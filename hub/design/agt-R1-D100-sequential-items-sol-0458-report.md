Implemented R1/G3 D100 in the two allowed files.

- Physical item projection now authenticates exact immutable shot/internal pins while allowing a genuinely created same-batch shared owner.
- Placement alias maps retain their strict correspondence checks.
- Added eight test functions covering sequential consumption, shared owners, malformed correspondence, retargeting and no-write refusals.
- D91 remains byte-identical, including all 29 assertions. `capture.py` and Runtime are unchanged.

Verification completed through [source_audit.py](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R1-D100-sequential-items-sol-0458/evidence/source_audit.py):

- AST/in-memory compile and input conservation: PASS.
- Scoped Ruff, baseline/candidate: PASS.
- Scoped mypy, baseline/candidate and new tests: PASS; zero diagnostics.
- `git diff --check`: PASS.

Exact commands and outputs are recorded alongside the audit script. No pytest, collection, project helpers, fixtures or services ran.

C0 requires resolving operands against sequential state; the correction therefore authenticates the physical source without requiring the new owner in the original parent document.

The [caller trace and proof recipe](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R1-D100-sequential-items-sol-0458/evidence/source-trace-and-proof.txt) specifies retained RED evidence and the proposed combined MAIN proof. **Behavior remains unverified and held for independent review**, followed by one combined D100 run with the reviewed exact-time and host-fixture corrections.

F-D86 conventional commit message and `DONE` written. Harness commit pending.