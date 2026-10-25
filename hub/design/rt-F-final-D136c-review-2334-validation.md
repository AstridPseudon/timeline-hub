# D136c private preservation review validation

Status: FAIL on F1. All bounded checks below were run read-only against the private
candidate. No product behavior or real test body was run.

## Exact private checks

- `PYTHONPYCACHEPREFIX=/tmp/rt-F-final-D136c-review-2334-private-cache/pycache python3 -m py_compile $(find candidate -type f -name '*.py' ! -path '*/__pycache__/*' -print | sort)` — PASS, 19 files.
- Node `JSON.parse` over candidate JSON files — PASS, 7 files.
- `bash -n` over candidate shell files — PASS, 3 files.
- `RUFF_CACHE_DIR=/tmp/rt-F-final-D136c-review-2334-private-cache/ruff-cache /root/.local/bin/ruff check --select F` over all candidate Python files — PASS.
- `/root/.local/bin/mypy --ignore-missing-imports --follow-imports=skip --explicit-package-bases --cache-dir /tmp/rt-F-final-D136c-review-2334-private-cache/mypy-cache` over the 7 harness files plus 6 source-input files — PASS, 13 files.
- `PYTHONDONTWRITEBYTECODE=1 python3 candidate/acceptance-d73.py` — PASS: one capture, four checkout receipts before request, newer-home accepted, selected-checkout drift refused.
- `PYTHONDONTWRITEBYTECODE=1 python3 candidate/d59-final-matrix/stubcontrols.py` — PASS: positive dispatch count 1, poisoned dispatch count 0; pending owner route refused before dispatch.

## Preservation and source checks

- Candidate predecessor comparison: 64 files unchanged; one intentional `core-inventory.json` metadata change; one new D136c source-input file.
- Authentic 2252 matrix comparison: all 41 physical matrix blobs unchanged byte-for-byte.
- Inventory comparison: predecessor 100-target set is an exact subset; no removals or changed predecessor hashes; exactly one added target.
- Runtime source identity: `0ca306dfd3cf4e21976271cc4b2e779b10e025b0`, tree `37cfcd4f6108c1fdda401e563e3674503bc328ef`; new test blob `15c35c662480d98443b66210a823e3f00967d6db`, SHA-256 `e2c82f375397a7bc64c198b61b06561e2d11e7fda205ed4aeb2f721af117dc4e`.
- D136c security receipt: `rt-D136c-security-review-2312/evidence/review.json`, SHA-256 `ed84fc47edf2f984679ed73b3e0dd094ee3cbe788c54264587d1e6259d8eeeea`, status PASS.
- D136c integrated home result: `rt-D136c-home-2318/evidence/result.json`, SHA-256 `7938cd7604df4ec588f6dd31e91aad1f4f79bc92ca11c7b3fd70d3c5efa7045c`, status PASS; durable 4-case XML SHA-256 `8a9ce803297c6e0de66c0014203aad75f80c8b235e727df58cfbf8488a8bd397`.
- Production source grep confirms the released path `guard -> reject/CommitRejected -> public_failure -> mounted Service._execute_timeline_commit`.
- Contract spot-check against Runtime `contract/schemas/timeline-commit.json`: `RequestedStep` has `reads` (not `optionalreads`), accepted steps retain `reads`/`dependencies`, and no candidate client regeneration or renamed canonical aliases were introduced.
- C0 wire-shape inventory remains the inherited source shape: request `api_version`, `project_id`, `timeline_id`, `base_revision_id`, `base_publication_id`, ordered `commands`, `label`, `steps` (`id`, `label`, `intent`, `tags`, `command_ordinals`, `patch`, `reads`), `merge`, request `reads`, `dry_run`, `source`, `rationale`, `group_id`, and `Idempotency-Key`; accepted/merged `canonical_document`, `receipt`, heads, `rebased_onto`, records, bindings, effects, dependencies, and history; conflict `details.current`; invalid `code`, `path`, `hint`, `suggested_command`; preview `would_status` with `receipt: null`.
- No stale `547e` marker or final tuple capture found. D127, WAL, and D130 markers are absent; SWAP is mentioned only as an excluded/held item in inherited prose.

## Blocking finding proof

The candidate `run-final-services.py` contains a hard-coded 98-entry `CORE_TEST_FILES`
list and no `core-inventory` read. Comparing that list with the candidate’s 101-entry
`core_selector.python_targets` yields exactly:

```text
tests/test_timeline_commit_ancestry_reads.py
tests/test_timeline_commit_closure_growth.py
tests/test_timeline_missing_observation_diagnostics.py
```

Therefore the new target inventory is not consumed by the existing runner. This is a
static proof only; no core or full suite was run.
