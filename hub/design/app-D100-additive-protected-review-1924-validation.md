# D100 protected source-purpose validation

## Final identity

- Candidate commit: `92eb2dafc6a3d4735253b14882fd336faa79837c`
- Candidate tree: `7a03ee6731d10d024419a3fd8c2383e5b2c29e44`
- Base commit: `9486cbb06e2ab53402086772e6c2bc18bc4849fc`
- Candidate test SHA-256: `9f4501c694dab5244d6e8bde1113d1c1a6b056f3fd5c0e4375c86a10ac8d2597`
- Protected product SHA-256: `018f174004bf9b9c275aa23ef6ceb432ce9d7294d71e3024f96353c25fa808a3`
- `git diff --name-only base candidate`: exactly `tests/sdk/test_d100_item_birth_boundary.py`
- Candidate worktree: clean at final inspection.

## Commands and results

- `/usr/bin/python3.11` AST parse plus `compile()` of
  `tests/sdk/test_d100_item_birth_boundary.py` — **PASS** (`AST_PARSE_COMPILE PASS`).
- `PYTHONPYCACHEPREFIX=/tmp/w-d5fc4c5c73/app-D100-additive-protected-review-1924/pycache /usr/bin/python3.11 -m py_compile tests/sdk/test_d100_item_birth_boundary.py` — **PASS**.
- `/home/user/work/venv-agent/bin/ruff check --no-cache tests/sdk/test_d100_item_birth_boundary.py` — **PASS** (`All checks passed!`).
- `/home/user/work/venv-agent/bin/mypy --cache-dir /tmp/w-d5fc4c5c73/app-D100-additive-protected-review-1924/mypy-cache tests/sdk/test_d100_item_birth_boundary.py` — **PASS** (`Success: no issues found in 1 source file`).
- `git diff --check 9486cbb06e2ab53402086772e6c2bc18bc4849fc 92eb2dafc6a3d4735253b14882fd336faa79837c --` — **PASS**.
- Python 3.11 JSON parsing and SHA-256 checks over author1921, actual1837,
  independent1843 evidence — **PASS**.
- Git outside-blob census (`git diff --raw`, changed-path count, protected
  product SHA comparison) — **PASS**: one additive test path, product byte
  equality, no Runtime/App/fixture/generated/schema mutation.

## Explicitly not run

No pytest, own27, original9, App projection, fixture receiving, provider/native,
collection/provider/socket, body, full, browser, acquisition, or D130 suite was
run by this protected source review. Source remains HELD until the later genuine
behavior/home/batch admission. The retained actual1837 and independent1843
results are not reclassified as current behavior execution.
