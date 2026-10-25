# D138 validation

- `TMPDIR=/tmp bash ops-d138-cli22/dry-check.sh --controls` — PASS; 11 tests.
- `TMPDIR=/tmp bash ops-d138-cli22/dry-check.sh --source-check` — expected exit 1; truthful `NOT_READY` because no receipt-rendered manifest was supplied.
- `PYTHONDONTWRITEBYTECODE=1 TMPDIR=/tmp python3 -m unittest discover -s ops-d138-cli22 -p 'test_recipe.py' -v` — PASS; 11/11, including the actual named-row pre-dispatch path.
- `ruff check --no-cache ops-d138-cli22/check.py ops-d138-cli22/test_recipe.py` — PASS.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m py_compile ops-d138-cli22/check.py ops-d138-cli22/test_recipe.py` — PASS.
- `bash -n ops-d138-cli22/dry-check.sh` — PASS.
- `git diff --check` — PASS.
- `TMPDIR=/tmp bash ops-d138-cli22/dry-check.sh --bind-check /tmp/d138-a/request-a/d66 /tmp/d138-b/request-b/d66` — PASS; distinct request/XML bindings.
- Exact selector assertion — PASS; 22 unique selectors, retired parser-only selector excluded.
- Source guard — PASS; Agent `41ad…` tree equals independently reviewed `4fec…` tree, lock source and actual vendored runtime select normal Runtime `f103…`, canonical 15 exact.
- Supported launcher positive control — PASS; exit 17, one body call, shell-sensitive argv preserved.
- Poison, duplicate, malformed, and tuple-lock mismatch controls — PASS; zero launcher/body calls for each refusal attack.

No central request-test run, live install, pytest collection/body run, provider, original22, or full suite was run.
