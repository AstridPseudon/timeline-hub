# Independent validation

## Targeted tests

Exact author selector, with reviewer-private basetemp/cache and output:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/user/work/wt/agt-U2-D141ee-installer2-decision-next-review:/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -n 3 --timeout=45 --junitxml=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-U2-D141ee-installer2-decision-next-review/evidence/targeted.xml --basetemp=/tmp/w-990444ed71/reviewer/basetemp -o cache_dir=/tmp/w-990444ed71/reviewer/cache tests/test_installer_schema.py
```

Result: `4 passed in 1.74s`; collection `4`; failures `0`; errors `0`; skipped `0`.

## Static and scope checks

- `ruff check tests/test_installer_schema.py`: PASS.
- `git diff --check 14ccf296f3768fcde857047b263834e4a6bbe52e HEAD`: PASS.
- Changed paths are exactly `tests/test_installer_schema.py`; excluding that path, `git diff --name-only` is empty.
- Strict AST/source conservation: parent has 8 top-level functions; reviewed file has 6; the six retained function source segments are byte-identical; the filtered AST is identical; both removed source hashes match the recorded scope.
- The reviewed tree is `36685788803295ce10a6399099535d5b90a5bc79`, parent tree is `6806fec5657f26097d0d0f3da29082907e6faadd`.
- Product/control hashes and the canonical schema digest were checked unchanged.
- Typecheck: N/A; tests-only deletion and no applicable typecheck lane for this file.
- No full/core/browser/install/render/child-body/live-socket suite was run; no credit is claimed for those nodes.

The first static wrapper attempt had a syntax typo in an unused print expression and was not counted. A corrected `set -euo pipefail` rerun passed all checks above.
