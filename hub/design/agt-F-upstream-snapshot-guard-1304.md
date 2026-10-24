## Report

- Corrected only `agent full-upstream-25359` in `suites.conf`.
- Guard accepts original `HEAD=25359` or an exact one-parent service snapshot with parent `25359`; tree, clean-status, environment, module, Runtime, profile, and pytest checks remain unchanged.
- Used guarded atomic replacement with predecessor backup.
  - Registry: `5b297d31…` → `a9d31cf4…`
  - Outside-row hash unchanged: `f14b6ef0…`
  - Backup: [suites.conf backup](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-upstream-snapshot-guard-1304/evidence/suites.conf.pre-20261024T130610Z.bak)

Validation:

- `bash -n`: PASS
- Exact row/outside-byte comparison: PASS
- Synthetic old-RED/new-GREEN custody guard: PASS
- Read-only Agent/Runtime custody checks: PASS
- Full suite/test-service request: not run, as instructed.

Worktree is clean. Completion marker and commit message were written. Next step: manager queues exactly one `full-upstream-25359` service run.