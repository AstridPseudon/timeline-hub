## G4 media-home report

- Qualified exact home `0ff3d103fb…`, containing reviewed `f9df90aa…`; worktree clean.
- Runtime pin verified clean: `becfe6db88…`, tree `7edc08e3…`; imports resolved explicitly from Agent home + Runtime worktree.
- Acceptance command: three specified test files with `PYTHONPATH="$PWD:/home/user/work/wt/rt-pin-becfe6db"` and `ASTRID_RUNTIME_CHECKOUT` set.
  - Result: **20 passed**, 0 skipped/deselected/errors.
  - Durable JUnit: [g4-integrated.xml](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/evidence/g4-integrated.xml), SHA256 `52ec8bb8…`.
- Compile, Ruff, vendor lock (15/15, becfe source), artifact manifest, and `git diff --check`: **passed**.
- Typecheck-v2: `current=1902 baseline=1902`, **passed**.
- Duck fixture: 17 assertion ASTs unchanged; original bytes/topology controls verified.
- Staged row: [g4-managed-duck-0832.row](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-G4-media-home-0832/evidence/g4-managed-duck-0832.row), SHA256 `ee3739fe…`, held because available provisioned child bench is for Agent `ba8f0bc8…`/Runtime `f3208b26…`, not this tuple. Managed duck body was not rerun; prior service `31491` remains `1 failed, 135 passed`.

No installer, registry, product, browser, full-suite, or new-child changes. Commit message and `DONE` marker created.