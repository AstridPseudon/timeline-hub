## Report

- Merge-forward arrived with `MERGE_HEAD=25359ed...`; conflicts resolved in files only.
- Preserved v2 save/publication assertions and custody/source-identity safeguards.
- Adopted upstream Remotion fixture setup.
- Regenerated `artifacts.json` via the required tool.
- Harness must stage/commit the resolved merge. `MERGE_HEAD` contains the authorized upstream tip; post-commit ancestry is pending.

Tests/checks:

- Targeted pytest: **135 passed, 1 failed**. Failure was Runtime `history_unavailable` during duck runtime setup.
- `make ruff`: passed, baseline unchanged at 2145.
- `make mypy` with typecheck venv: failed ratchet, 1914 vs baseline 1902 (+12).
- `python scripts/artifact_manifest.py --check`: passed.
- `git diff --check`: passed.
- No conflict markers; targeted files compile.

Inventory:

- Actual merge deletion: `tests/test_h3_continuation_runner_contract.py`.
- D40/source-custody files and tests remain present.
- Registry/skip changes retained: registry module/validator updates, new registry corpus test, lane workflow, and `tests/removed.yaml`/lane guard updates.
- Vendor lock check blocked: lock expects producer `45c3a7f4`, mandated checkout is `34eac004`; no re-vendoring performed.
- No full/browser/live-suite run.

Commit message and `DONE` marker were created.