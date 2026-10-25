## D122 report

- Classification: genuine `REG14`; candidate run `ef4c40e8` / tree `86fadb…`, Runtime `369ffa7c` / tree `9bf331…`, Composition tree `5ab519…`.
- Result: `14 failed, 59 deselected in 117.11s`; no passes.
- Exact first child cause, verified from retained stderr: `ModuleNotFoundError: No module named 'runtime_protocol'` at `astrid/core/rendering/remotion_runtime.py:26`, during `registry_discovery`.
- Terminal `RemotionValidationError` at line 700 is only the wrapper. Callchain: `ensure_pack_host` → `_prepare_render_validation` → `prepare_remotion_validation` → `_settle_registries` → `_registry_probe` → owned child import → missing `runtime_protocol`.
- All 14 receipts: `original_wait_exit_code=1`, `census_complete=true`, `custody_admitted=true`; all 14 stderr hashes equal `95425eb5…`.
- All 14 selectors are body-equal to pristine upstream REG rows; budgets/inputs/provenance unchanged. Per-selector PID/stderr accounting is in [D122-host14-wholepath-return.json](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-D122-host14-wholepath-return-1217/evidence/D122-host14-wholepath-return.json).
- Comparisons: pristine upstream14 `15 passed, 1 failed, 0 errors`; current original/path comparison passed the `[120-400-ready-True-400-400]` selector.
- Checks: JSON validation passed; SHA-256/hash checks passed; candidate test diff from bae5 was clean; assigned worktree remains clean.
- No pytest, typecheck, lint, source/test/suite/profile/guard edits, or product fix performed. The retained receipt omits the complete child environment, so projection failure beyond the exact missing import is not claimed.
- Commit message written and `DONE` marker created.