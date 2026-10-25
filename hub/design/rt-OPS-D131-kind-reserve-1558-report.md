## OPS D131 report

Implemented private `ops-d131` candidate only:

- Child reserve: `5.5 GiB = 5,905,580,032 bytes` (4.0 GB + twice 740 MB).
- Runtime reserve remains `8 GiB = 8,589,934,592 bytes`.
- Direct `Store.ensure` tests cover boundaries, 6.1 GB cross-kind behavior, reuse, unknown kinds, and rejected builder/registration calls.
- Callers preserved: `make-child-venv:566` and `make-runtime:396`.

Files: [bench_store.py](/home/user/work/wt/rt-OPS-D131-kind-reserve-1558/ops-d131/bench_store.py), [test_reserve.py](/home/user/work/wt/rt-OPS-D131-kind-reserve-1558/ops-d131/test_reserve.py)

Validation:

- Required Python tests: PASS, 5 tests.
- Required Ruff command: PASS.
- In-memory compile: PASS.
- `git diff --check`: PASS.
- Live preimage SHA256 unchanged: `7d587043...f27bf26495`.
- No qualified mypy/pyright lane applies.

Evidence written to the required worker `evidence/` paths. No blockers. Recommended next step: independent review, then exact installer-worker promotion.