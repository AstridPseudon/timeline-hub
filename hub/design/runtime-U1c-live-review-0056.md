## PASS — branch-only freeze draft

- `HEAD`: `40427e8b5d658ecc0eb117d576b2a4e9de6c6d59`
- Tree: `34ca7af13426512ab6ce3584a65582e393fe8675`
- True merge parents:
  - reviewed `0138e3af696d907b4c90b787ae86652f7f8a2153`
  - upstream `795379a67ed71bfc5c0eeee51a0ab883b3210fb8`
- Only candidate delta: `runtime_protocol/service.py`, `tests/test_managed_output_export.py`
- Worktree clean; no tracked edits or deletions.

Checks:

- Targeted pytest: `224 passed`
- Ruff agent venv: `78` diagnostics, exactly matching baseline; `0` new
- Pyright: `375` vs `375`; `0` new
- In-memory compilation: passed
- `git diff --check`: passed
- Conflict markers: none
- Protected 69 contract/package/generator/schema paths: byte-identical against `0138e3af` and `abd47e68`
- Schema digest `35c2d9…` and producer digest `d5f98d…` unchanged
- R0 `public-export-0049` is not an ancestor
- Production caller and HTTP export tests pass; safety/idempotency/containment/collision/strict-auth assertions remain covered.

No full, browser, integration, or gate suite was run. Integration remains on hold until freeze; no merge requested.