## Report

Status: **PREPARED / NOT QUALIFIED**

- Added offline inline/reference carrier mapping in [tests/test_timeline_legacy_occupancy.py](/home/user/work/wt/rt/rt-R5-occupancy-historical-fixture-0246/tests/test_timeline_legacy_occupancy.py).
- Uses `occurrence.place-shared`, exact five-key `source_ref`, `source_occurrence_id`, `select: parent`, destination-only `created`, dry-run mapping, and external idempotency key.
- Existing occupancy test bodies remain unchanged. No Runtime/Agent/product changes.

Checks:

- Offline prep tests: **2 passed**
- Full direct file: **17 passed, 1 sandbox socket failure**
- Central targeted run: **blocked** by missing `/home/user/work/wt/astrid` checkout
- Ruff: **passed**
- Compile: **passed**
- AST/body-property mapping: **passed**
- `git diff --check`: **passed**

Future acceptance, only after reviewed Agent handoff:

```sh
ASTRID_CHECKOUT=/home/user/work/agent \
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:packages/python \
/home/user/work/venv-runtime/bin/python -m pytest -q \
tests/test_timeline_legacy_occupancy.py --tb=short
```

Provider acceptance remains unverified and not claimed. Commit message and `DONE` marker created.