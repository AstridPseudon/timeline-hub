No Runtime candidate or product/test changes. All guards and original assertions remain intact.

The earlier assessment overstates Agent’s source-patch preservation: [`inverse_stages`](/home/user/work/agent/astrid/sdk/timeline/_step_undo.py:346) attaches `_inverse_effects` only for nested inverses. Ordinary `timeline.restore` undo recomputes effects, which does not guarantee Runtime’s contract-required reverse source order. Return this minimal seam to the existing Agent inverse owner.

Two further source discrepancies need exact-record comparison: leaf timing caches versus required native-range counts, and restored collection order versus Runtime’s append projection. The retained evidence does not justify a safe verifier change.

Run 10077 records all four historical failures. Run 11789 contains none of the exact four selectors. The original fixture directory is absent, and retained tracebacks omit complete prepared records; current functional behavior remains unverified.

Static checks:

- AST parsing/in-memory compilation: **PASS**, 24 Python files.
- `ruff check --no-cache runtime_protocol/timeline_commit_auth.py tests/test_timeline_inverse_stage_authentication.py`: **PASS**, true baseline and unchanged candidate.
- `mypy --no-incremental --follow-imports=skip --ignore-missing-imports --cache-dir <private-cache>` on those files: **PASS**, both copies; default untyped-body limitations apply.
- `git diff --check`: **PASS**; worktree clean.

No pytest, collection, fixture/helper execution, service, or full suite ran. D94 store and both D14 positives remain untouched.

[Full production trace, precise seams, evidence limits, and proposed existing D72/MAIN entries](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-R2-inverse-auth-sol-0333/evidence/source-trace-and-seams.txt). Evidence includes source/test hashes and totals approximately 106 KB.

Commit message and `DONE` created. Any subsequent candidate remains **HOLD** pending independent protected security/core review and targeted MAIN proof.