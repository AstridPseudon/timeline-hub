## Result: PASS — branch-only D39 candidate

Candidate `fe637f6c5170a8f5c4c01594a1f8052812032f8b`, tree `b1808e1638aab76a6b6125a24f2b044de47718cf`; parent `1d9ddba546f8fb1300f55ff62607ed492719cbaa`, tree `f56c396c4495547680b46e832565278d2c375e69`.

Changed paths are exactly five generated outputs:

- `contract/artifacts.json`
- Python contract metadata/client
- TypeScript contract metadata
- Runtime contract metadata

Schema source digest is `4118b1e26d30…b413d2` in both parent and candidate; parent generated metadata contained stale `35c2d9c5e0b5…398d4c`, correctly regenerated to `4118…`. OpenAPI, bundle, and TypeScript generated client remained unchanged.

Checks passed:

- `generators/generate.py --check`
- `scripts/artifact_manifest.py --check`
- `git diff --check`
- Private normal generation reproduced all 13 generator outputs byte-for-byte.
- Ruff: 28 parent-baseline diagnostics; zero new identities.
- Pyright: 60 parent-baseline diagnostics; zero new identities.
- Reused author evidence: generated-client suite **147 passed**, TypeScript `tsc --noEmit` passed.
- Authorized command:

  `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:packages/python ASTRID_CHECKOUT=/home/user/work/agent /home/user/work/venv-runtime/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/test_recorded_responses.py --junitxml=.../evidence/recorded-responses.xml`

  Result: **16 passed**.

Recorded cases preserve complete assertions: `retired_route` HTTP 410 versus canonical `commitTimeline` stale-head conflict HTTP 409, schema validation, byte-identical rerecording, client error parsing, auth, and idempotency/request shapes.

Agent source identity: `2007cf7aaf5d…`, tree `68b0309cede3…`; App: `5f43d9e86a11…`, tree `464333ff8be4…`. Both remain pinned to `35c2…`; candidate is not adopted. Mounted callers remain Agent `_remote_timeline.py:249`, App `dataProvider.ts:751–758`, and Runtime route `server.py:302` → `RuntimeService.commit_timeline`.

No product files were modified. Branch remains held for freeze; no full/browser/adoption suite was run. Durable XML evidence is 8 KB. `DONE` and commit message were written.