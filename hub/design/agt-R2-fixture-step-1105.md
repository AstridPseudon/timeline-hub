Implemented R2 fixture migration in [test_step_undo_v2.py](/home/user/work/wt/agt-R2-fixture-step-1105/tests/editing_conformance/test_step_undo_v2.py).

- Added authentic Runtime closure/media manifest and compiler-generated accepted step boundaries/full v2 history fields.
- Preserved all test bodies and assertions: 23/23 AST hashes unchanged.
- Baseline: 14 failed, 21 passed.
- Final pytest: 35 passed.
- Ruff, qualified mypy, and `git diff --check`: passed.
- No product/runtime/schema/pin changes; no skipped or xfailed tests.
- Runtime path deviation: requested `rt-pin-bec76fe6db` was absent; used available clean pin `rt-pin-becfe6db` (`becfe6db88b2...`).
- Evidence retained under the assigned worker evidence directory; completion marker and commit message created.