# U2 D141m source validation

Candidate inspected at exact finalized merge `5d202569f3af3852476d182ff49683787bb1e881`, tree `92a3ffdb5a8bf476e10bfa1bbda3e2856fb9938c`, with approved base `28e56cacb42d3da85b02e5b3543895b44f3d0f70` and frozen upstream `64197afa297f86f1e738238d5e80aff6d33e303a`. Both parent ancestry checks passed. Historical author staging/BLOCKED language predates the final harness commit and was not treated as a current blocker.

Commands run and results:

- `git diff --check 28e56cacb42d3da85b02e5b3543895b44f3d0f70 5d202569f3af3852476d182ff49683787bb1e881` — passed.
- Independent `git ls-tree` path/blob conservation and author-manifest SHA-256 comparison — 54/54 changed paths matched; approved-base-only 906/906 and upstream-only 26/26 matched; no conflict markers; 40 changed Python files parsed successfully.
- `PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python scripts/artifact_manifest.py --check` — `artifacts.json is current`.
- `PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json --producer /home/user/work/wt/rt-pin-6a011d58` — `ok runtime.lock.json (matches producer manifest)`.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. RUFF_NO_CACHE=true /home/user/work/venv-agent/bin/python -m scripts.reshape.compare_ruff_baseline` — current 2143, baseline 2143, exit 0.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. MYPY_CACHE_DIR=/dev/null /home/user/work/venv-agent-typecheck-v2/bin/python -m scripts.reshape.compare_mypy_baseline` — current 1902, baseline 1902, exit 0.

Runtime producer is `6a011d58e69173d70e2e9bb3ac434ac8f9e87d8d`; all 15 lock entries and all 15 canonical packet entries match. No dependency was installed or changed. Normal artifact and vendor-lock tools used documented arguments.

Source checks: `generationId` and `variantId` are established by accepted importing and validated at plan input. Unmarked aliases receive upstream metadata conversion; no new authority surface was introduced. Custody retains native process-control/sandbox behavior and accepted exit proofs; generic host and platform helpers preserve upstream wiring. Native timeline paths, Runtime writer/reads/undo, and security checks remain present. Agent contains installer User-Agent behavior from `e1c751def` and its assertion; current App manifest remains pinned to `28e56cac...`, so App adoption is a manager handoff item.

No runtime qualification claims. Not run by explicit source-only scope: pytest or any test body, test collection, provider/product imports, localhost/browser/live-socket suites, full suite, bounded delta suite, P4 body, or behavior/receipt proof. No diagnostic was silenced and no baseline changed.
