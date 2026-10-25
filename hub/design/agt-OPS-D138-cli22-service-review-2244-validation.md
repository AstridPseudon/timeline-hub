# Validation

Disk at control start: `/tmp` had 5,103,886,336 bytes available (source
floor 5,000,000,000; stop 4,000,000,000).

Passed:

- `TMPDIR=/tmp/w-ops-d138-cli22-review-2244 bash ops-d138-cli22/dry-check.sh --controls`
  — 10/10 private controls passed.
- `TMPDIR=/tmp/w-ops-d138-cli22-review-2244 bash ops-d138-cli22/dry-check.sh --bind-check .../request-A/d66 .../request-B/d66`
  — PASS; per-ID artifact paths are disjoint.
- `python -m py_compile ops-d138-cli22/check.py ops-d138-cli22/test_recipe.py` — PASS.
- `python -m ruff check --no-cache ops-d138-cli22/check.py ops-d138-cli22/test_recipe.py` — PASS.
- `bash -n ops-d138-cli22/dry-check.sh` — PASS.
- `git diff --check` — PASS.

Expected fail-closed admission:

- `TMPDIR=/tmp/w-ops-d138-cli22-review-2244 bash ops-d138-cli22/dry-check.sh --source-check`
  — exit 1, status `NOT_READY`; reports the reviewed lock/helper mismatch,
  unchanged-launcher duplicate-key finding, current shared Agent identity
  mismatch after pending U4a movement, and missing real receiving inputs.

The private launcher fixture executed the supported run mode with exit 17 and
one body call, exercised shell-sensitive argv values, refused a malformed
manifest before body, and refused a poisoned runtime identity with zero body
calls. No central request, pytest collection, provider, exact22 body, package
acquisition, install, or full suite was run.
