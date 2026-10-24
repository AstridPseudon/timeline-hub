## U4a report

Adopted the canonical Runtime45c3 client export via normal tooling.

- Producer SHA: `45c3a7f476e1c5f74fafc15956a58b9871eee21f`
- Producer tree: `f51124b7b5b37a73a3d660e34b3f543517f849ee`
- Checkout: `/home/user/work/wt/rt-pin-45c3a7f4`
- Changed only:
  - `astrid_runtime_client/__init__.py`
  - `runtime.lock.json`
- All 4 public client files byte-match the producer.
- All 15 mapped artifacts match canonical hashes.
- Schema, generated bodies, fixtures, contract metadata, and tests unchanged.
- Added `DocPatchArgs` root import/export only.

Checks passed:

- `vendor_lock.py check ... --producer ...`
- `artifact_manifest.py --check`
- 64 targeted pytest tests passed.
- Ruff: `2145` findings, baseline `2145`.
- Mypy: `1909` findings, baseline `1909`.
- `git diff --check`

No blockers. No full suite/readiness bench run, per brief.

Commit message written: `feat(agent): adopt canonical Runtime client export`

Recommended next step: independent review and normal merge, then App may create its single reviewed readiness child.