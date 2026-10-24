## Report

Implemented `tools/run-env-cohort-2356.sh` and one named service row. No product or test bodies changed.

Final central run:

- ID: `agt-F-env-cohort-2356-env-cohort-2356-1023235906-11789`
- Exact inventory-derived cohort: 86 nodes from durable 267 failures
- Result: **69 passed, 17 failed, 0 errors/skips**, 247.29s
- Collection: exact 86 nodes
- Bench: child `c886d448`, Agent `c36ca8c9`, Runtime `abd47e68`, tree `6047ac3`, Node `20.19.4`, profile `819acf`
- Installed `-I` origins, RECORD/direct_url, source/body hashes, profile and registry inventory verified; before/after custody matched.
- No unsupported `PYTHONNOUSERSITE`, guard bypass, editable install, new bench, or shared mutation.

Remaining failures:

- `test_private_imports_add_no_repository_or_pack_pythonpath`: installed child lacks `PYTHONPATH`.
- 15 `tests/sdk/test_host_bootstrap_source_identity.py` cases: two fail installed-origin bootstrap validation; 13 fail `registry_discovery` with `original_wait_exit_code=1`.
- `test_generic_host_runs_external_python_orchestrator_from_admitted_pack`: installed child cannot import admitted `external_pkg`.

Full longrepr/source/owner evidence: `workers/agt-F-env-cohort-2356/evidence/pytest.log`, `junit.xml`, `outcome-map.json`.

Checks passed: `bash -n tools/run-env-cohort-2356.sh`, `git diff --check`, all eight selected source/body hashes unchanged.

Commit message and `DONE` marker written. Recommended next step: Agent/Runtime OPS repair installed child source/runtime binding and startup registry validation before another cohort run.