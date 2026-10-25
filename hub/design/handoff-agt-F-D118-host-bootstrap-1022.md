D118 urgent read-only host-bootstrap REG14 source diagnosis and exact accounting

- No source/test changes made. Worktree remains clean.
- Commits checked: current `120d7120` and retained `070dfc5e` have identical hashes for:
  - `tests/sdk/test_host_bootstrap_source_identity.py`: `08dfa8dc...5161b`
  - `astrid/sdk/host_bootstrap.py`: `c05d1566...e4b78`
- REG14 function AST/body hashes match pristine Agent `08e6b905`; upstream passed, integrated retained run failed.

REG14 selectors:

1. `test_bootstrap_stops_on_correlated_terminal_registration_failure`
2. `test_startup_budget_polling_preserves_identity_and_original_cleanup[None-25-ready-True-25-None]`
3. `[None-None-ready-False-300.0-None]`
4. `[120-25-ready-True-25-None]`
5. `[120-None-ready-False-120-None]`
6. `[120-1-terminal-False-1-None]`
7. `[120-1-foreign_pid-False-1-None]`
8. `[120-1-foreign_birth-False-1-None]`
9. `[120-1-foreign_instance-False-1-None]`
10. `[120-1-foreign_source-False-1-None]`
11. `[120-None-exit-False-1-None]`
12. `[120-400-ready-True-400-400]`
13. `[120-None-ready-False-150.3-30]`
14. `[120-None-exit-False-1-30]`

Actual retained failure for all 14:

`astrid.core.rendering.remotion_runtime.RemotionValidationError: runtime validation refuses unsupported loader/interpreter overrides`

The failure occurs before fake `popen_owned_group` launch or registration assertions: `ensure_pack_host()` → `_host_render_environment()` → `_prepare_render_validation()` → `prepare_remotion_validation()` → `probe_context()`. Terminal failure is at test line 363; budget-success rows at line 727; remaining budget rows at line 731.

Root cause/evidence boundary:

- `probe_context()` rejects inherited loader/interpreter overrides, including `PYTHONNOUSERSITE`.
- Retained D108 invocation explicitly sets `PYTHONNOUSERSITE=1`.
- `_prepare_render_validation()` strips `LD_*/DYLD_*` only; it does not remove Python startup overrides.
- The retained D118 JSON omitted the forbidden-key detail and does not prove why `ASTRID_REMOTION_PROJECT_DIR` was present, so the exact triggering key/source is not independently complete. The validator preflight failure itself is proven.

Minimal next-writer fix:

- Allowed production file: `astrid/sdk/host_bootstrap.py`.
- Confirm the exact inherited forbidden key, then align the source host environment with the existing `probe_context()` contract without weakening validation or changing tests.
- Do not edit the 14 assertions or `remotion_runtime.py` unless independent evidence proves the validator contract is wrong.
- RED: rerun the retained pinned D108 environment and the 14 selectors above; expected common validation failure.
- GREEN: rerun the same environment/selectors after the narrow host-bootstrap environment correction; all 14 assertions must pass unchanged.

Accounting:

- Bounded 23: `PRE0 / REG14 / NEW-OURS8 / UNKN1`.
- Immutable 506 original: `PRE0 / KNOWN1 / ENV59 / NEW-OURS CORE438 / NON-CORE8`.
- Overlay:
  - 14 `ENV` + non-core → `REG` + non-core.
  - Render adapter: original `NON-CORE` + non-core → `UNKN` + non-core.
  - Approved changed-body host remains `NEW-OURS`, `ENV`, non-core.
  - Five NEW rows remain core; forced-caption and D13 rows remain non-core.
- Conserved result: `PRE0 / KNOWN1 / ENV45 / REG14 / NEW-OURS CORE438 / NON-CORE7 / UNKN1 = 506`. Core-open remains 438. Historical 924 remains outside scope and isolation-uncertain.

Validation performed:

- `git diff --quiet 070dfc5e 120d7120 -- ...`: passed.
- `git diff --check 08e6b905 120d7120 -- ...`: passed.
- AST parse: production/test sources passed.
- D118 result/accounting JSON parse: passed.
- Worktree `git diff --check`: passed.
- No tests/typecheck/lint rerun, per read-only diagnosis scope. Retained D108 result was `8763 passed, 159 failed, 347 errors`; retained D118 upstream23 result was `15 passed, 1 failed, 0 errors`.

Ownership: existing Agent/Remotion environment ownership overlaps this source seam; the three approved App tails are disjoint. No App tail reassignment is appropriate.