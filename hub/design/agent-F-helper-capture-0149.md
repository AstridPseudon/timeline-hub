Implemented [helper-sequential-diagnostic-0149.py](/home/user/work/wt/agt-F-helper-capture-0149/tools/helper-sequential-diagnostic-0149.py), with source-preserving capture, Runtime map tracing, origin/hash preflight, bounded JSON, and credential scanning.

Test command ran once after observer correction; result: `FE`, exit 1. The observer’s final flush failed on its own float validator, so only preflight evidence survived:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-helper-capture-0149/helper-sequential-diagnostic-0149.json`

SHA-256: `b79993dd34e6b1921a1a1cd3a82263cd290f46dcc6a00ae9126d40a84eee0df3`

Runtime preflight passed for 8ea0766f/tree 6047ac30; credential scan found 0 matches. No causal claim is made, and the original test was not rerun.

Additional checks: Ruff, AST parse, `git diff --check` passed. No product/tests/Runtime files changed. BLOCKED marker and commit message were written.