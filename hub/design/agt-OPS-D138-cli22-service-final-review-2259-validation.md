# Validation

Disk at control start: 5,211,885,568 bytes available on `/tmp` (5 GB floor; 4 GB stop line). Scratch used the harness-resolved private directory `/tmp/w-77f09746ad`.

Passed:

- `TMPDIR=/tmp/w-77f09746ad bash ops-d138-cli22/dry-check.sh --controls` — 11/11 private operational controls passed in 0.757s.
- Independent named-row marker harness — valid manifest `rc=0`, one launcher marker call; duplicate, malformed, and tuple-mismatch manifests `rc=2`, zero additional launcher calls and zero artifacts.
- `/home/user/work/venv-agent/bin/python -m py_compile ops-d138-cli22/check.py ops-d138-cli22/test_recipe.py` — PASS.
- `/home/user/work/venv-agent/bin/python -m ruff check --no-cache ops-d138-cli22/check.py ops-d138-cli22/test_recipe.py` — PASS (`All checks passed!`).
- `bash -n ops-d138-cli22/dry-check.sh` — PASS.
- `git diff --check` — PASS.

Expected fail-closed admission:

- `TMPDIR=/tmp/w-77f09746ad bash ops-d138-cli22/dry-check.sh --source-check` — exit 1, JSON status `NOT_READY`; checkout/tree/parent/origin/hash/source/tuple/AST/launcher guards passed, while the receipt-rendered `D138_MANIFEST` and real receiving inputs were absent.

Not run by instruction: product imports, collection, provider/body, exact22/22-case execution, real preflight, central request, install/package acquisition, child/core/Store paths, credentials/Git/hub operations, and full suite.
