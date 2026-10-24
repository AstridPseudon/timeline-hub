Fixed D52 on base `2300c0a1d2`. Only `config/astrid-capability-census.lock.json` changed: one generated executor entry, `music.duck`.

Cause proved: D411 added duck to the authoritative output-result snapshot after the passing review. The unchanged lock therefore contained 113 executor IDs while reconstruction produced 114. The rendering catalog was not causal.

Validation:

- Existing CLI: `python -m astrid.core.execution.capability_ledger approve --checkout "$PWD"` — regenerated correctly; repeated invocation produced identical bytes.
- Exact seven selectors, run once through the central service — **7 passed in 53.24s**. [Exact command and result](<../../../../../../tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D52-census-sol-1213/evidence/seven-service-summary>).
- `python scripts/vendor_lock.py check runtime.lock.json` — PASS; all **15 mappings** also matched the pinned producer.
- `python scripts/artifact_manifest.py --check` — PASS.
- Targeted vendor-lock and artifact-manifest tests — **2 passed**.
- Scoped Ruff and mypy over the ledger and census tests — PASS.
- `git diff --check` — PASS.

All previous IDs remain. Production admission now accepts duck. Strict tests, counts, matrix, and the public fixture remain unchanged.

Durable `evidence/seven.xml` explicitly records a conversion of the central service summary; original request, log, summary, and generator trace are preserved alongside it.

No blockers or additional scope decisions. No full/gate run. Commit message and `DONE` are ready; next step is harness commit and integration.