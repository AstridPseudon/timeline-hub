# R2r Runtime handoff

**PASS (bounded Runtime metadata/wire slice).**

Implemented the durable Runtime seam for v2 commit metadata and replies:

- `runtime_protocol/timeline_commit_store.py`: authoritative v2 detection, provider-step requirement for v2 controls, effective merge metadata, authenticated publisher/history persistence, and legacy ABI-1 receipt/history preservation.
- `runtime_protocol/timeline_commit_execution.py`: accepts provider `invalid` failures.
- `contract/schemas/timeline-commit.json`: `invalid` failure status plus structured `code`, `path`, `hint`, and `suggested_command` fields.
- Regenerated Runtime/Python/TypeScript DTOs, contract metadata, schema bundle, conformance client artifacts, and `contract/artifacts.json` through the normal generators.
- Added durable restart/replay coverage for legacy rebased receipts and a contract test for structured invalid replies.

Source provenance: approved C0c contract `tl/integration` `7c92c39fe`; Agent R1 interface draft `8a66b1ac8`; Runtime WIP base `7f8a9a67aa7fa8d0a65e88dbf8eb3d103e3ae8f3`.

## Verification

- Central targeted service, exact final tree: **154 passed, 1 deselected**.
- Local focused final tests: **2 passed**.
- `npm run build --prefix packages/typescript`: **PASS**.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. /home/user/work/venv-runtime/bin/python generators/generate.py --check`: **PASS**.
- TypeScript conformance generator `--check`: **PASS**.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. /home/user/work/venv-runtime/bin/python scripts/artifact_manifest.py --check`: **PASS**.
- `git diff --check`: **PASS**.
- Ruff/Pyright ran on the touched Runtime scope but report existing repository diagnostics (Ruff 92, Pyright 76); no baseline-clean/no-new-diagnostic proof was available.

## Limits / next steps

The Agent provider's real R1 output and cross-repo integrated P1 path remain unverified here; this worker did not touch Agent/App/Composition. The normal TypeScript generator was first invoked with an incorrect output root and left untracked staging/build files in the worktree; the task's explicit no-cleanup rule was followed, and the intended tracked consumer artifacts are the generated files listed above.
