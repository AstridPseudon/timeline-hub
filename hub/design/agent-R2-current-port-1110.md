# R2 current test-only port — PASS

## Change

Added exactly one file:

- `tests/editing_conformance/test_inverse_stage_runtime_regressions.py`

The file is the `db3c11ca6` regression blob (413 lines) with only the required finite Agent provenance adaptation:

- `AGENT_COMMIT = abfa78a657b4ce1cc625104e8472fb29938e3d64`;
- `astrid/sdk/timeline/commit.py` SHA-256 =
  `741e8afcca27577e3a620b60351880a8df60aa2f4b48f15e0961fb63695edabc`;
- `astrid/sdk/timeline/inverse.py` SHA-256 =
  `fdae9b17f000a6968009222233327a0662748d0289d090a03c36f0e213121ee7`.

A direct diff against `git show db3c11ca6:tests/editing_conformance/test_inverse_stage_runtime_regressions.py` reports only those three constant changes. The Runtime pin and hashes are unchanged.

The seven tests preserve cases 4/16/28/40/49, forged source, forged step, native ABA, and all no-write assertions. No original 58-case recovery was attempted, and no assertion was weakened.

## Verification

Exact collection:

```
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --collect-only tests/editing_conformance/test_inverse_stage_runtime_regressions.py
```

Result: 7 tests collected.

Exact seven-test run against Runtime `49ce53289bc37d9387a7d9e6b9c9b16072162181`:

```
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --timeout=45 --tb=short tests/editing_conformance/test_inverse_stage_runtime_regressions.py
```

Result: 7 passed in 14.52s. The test assertions verified actual Agent and pinned Runtime module origins and hashes before/after each case.

Additional checks:

- Scoped Ruff: passed.
- `scripts.reshape.compare_mypy_baseline`: current=1912, baseline=1912.
- `scripts/vendor_lock.py check runtime.lock.json`: passed.
- `scripts/artifact_manifest.py --check`: `artifacts.json is current`.
- `git diff --check`: clean.
- Current Agent HEAD: `abfa78a657b4ce1cc625104e8472fb29938e3d64`.
- Runtime checkout HEAD: `49ce53289bc37d9387a7d9e6b9c9b16072162181`, with expected Runtime file hashes.

## Decisions and limits

The only decision was updating the historical Agent provenance to the actual current D17 core files, as explicitly required. The old Agent hashes were not retained because they would fail the current-source custody assertions.

No full suite, browser/HTTP/live-socket suite, native14, daemon, original58 matrix, Git write, install, or shared-dependency mutation was run.

Recommended next step: perform the orchestrator’s independent current-port fidelity review, then merge the single test file.
