Source fix ready; genuine E2E remains blocked.

- Audited 20 remaining verifier conditions and prerequisites before editing.
- Changed both report sections to use one installed-distribution inventory, addressing pip freeze differences in provenance, sorting and duplicate handling.
- Preserved `STORE_VERIFY`, `STORE_PY`, protected helpers, prior fixes and all 29 inherited controls. Candidate SHA-256: `c3226b93d08e035f662ff57a7512522eb13f354acf2f13123999d71772e7142e`.

Validation:

```sh
bash -n ops-child-custody/make-child-venv
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python -m unittest discover -s ops-child-custody/tests -v
/home/user/work/venv-agent/bin/ruff check --no-cache ops-child-custody/tests
git diff --check
```

All passed: **40 tests in 4.124s**, including 11 new controls. All seven embedded Python blocks compile in memory. Type baseline: N/A.

Prepared the whole-make tiny-package fixture runner. Its preflight exited **2**, with E2E explicitly **NOTRUN**: approved fixture venue, Store custody, committed tiny sources and local-wheel inputs are missing. Observed free space was 5,027,573,760 bytes versus the unchanged 5,905,580,032-byte normal reserve. No admission was lowered.

Farm’s exact differing production rows remain **EXACTMISSING** pending the requested safe census. The source proves contract differences without identifying an invented production culprit.

Required evidence, exact E2E command and handoff details are in [validation.md](/home/user/work/wt/rt-OPS-child-inventory-contract-sol-1725/ops-child-custody/validation.md). Commit message and `BLOCKED` marker are written.

Next: supply census and admitted fixture inputs, run genuine E2E, then independent review and exact installation. No live installation, child request or body occurred.