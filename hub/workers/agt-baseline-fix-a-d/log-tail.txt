## agt-baseline-fix-a-d: report

Groups A and D are fixed on tl/agt-baseline-fix-a-d. The change is three test-side edits, no product code. Group A is only partly cleared: its 27 nodes pass only on the provisioning that matches the pinned composition version. The `remotion-env-nodes` suite points at a stale provisioning, so the brief's suite alone cannot show A passing.

### Changes
1. **`tests/conftest.py` (group A):** removed `os.environ.setdefault("PYTHONPYCACHEPREFIX", …)`. `sys.pycache_prefix` is still set in-process. Children already get `PYTHONDONTWRITEBYTECODE=1`, so no bytecode is written either way. The probe's refusal is untouched.
2. **`tests/packs/astrid_motion/test_pixel_shape_geometry.py` (group D):** the helpers now load `shape-cells.ts` through esbuild from `ASTRID_REMOTION_PROJECT_DIR` or `remotion/`, as `test_remotion_render_contract.py` does. If no esbuild exists, they keep the direct `.ts` import. A skip gate on esbuild would have turned 11 passing normal-env tests into skips, so I didn't add one.
3. **`tests/sdk/test_host_recovery.py` (new, found during verification):** the `Harness` fixture now clears `ASTRID_REMOTION_PROJECT_DIR`. The fake host writes no Remotion launch marker, so once the probe actually runs, the reuse path refused it. This is the group B pattern. The Remotion gate keeps its own test (`test_host_whose_validation_does_not_cover_this_caller…`), which sets the variable itself.

No tests were skipped, xfailed or weakened, and no checks were removed.

### Before/after (`remotion-env-nodes`, same three files)
Before (`…-1020064151-5676`): **27 failed, 60 passed, 14 errors**.
After (`…-1020064448-17690` on an earlier tree; final `…-1020071309-7976` on the final tree): **16 failed, 85 passed, 0 errors**.

- Pixel: 11 now pass.
- Recovery: all 14 errors now pass.
- Bootstrap: 16 still fail. They stop at `installed Remotion package manifest has unexpected version: '0.0.8'; expected 0.0.10`. The `agent-remotion` provisioning has `@banodoco/timeline-composition` 0.0.8, which is stale. That is environment, not the harness.

### Fully provisioned run (`remotion-0010-nodes`, `/home/user/work/runtimes/agent-remotion-0010`, composition 0.0.10)
Final (`…-1020071309-13875`): **2 failed, 99 passed, 0 errors**. The two failures are `test_bootstrap_passes_inventory_identity_and_restarts_on_change` and `test_installed_profile_launch_preserves_identity_and_uses_isolated_interpreter`. Both fail with `'PosixPath' object has no attribute 'pack_root'` (`astrid/core/pack/discovery.py:296`). That is group C, outside this brief, so I did not fix it.

Group A nodes all pass in this run.

### Normal-env regression check (my sandbox, no Remotion env vars)
- `tests/packs/astrid_motion/test_pixel_shape_geometry.py`: 14 passed. The direct-import path was kept, so none are skipped.
- `tests/sdk/test_host_recovery.py`: 18 passed.
- `tests/test_structure_contracts.py`: 1 failed, `test_giant_file_inventory_matches_rationale`. That is group K, a stale doc count, and it fails for reasons unrelated to my edits.

### Notes and open items
- **Environment:** `remotion-env-nodes` points at a stale Remotion provisioning (`agent-remotion`, composition 0.0.8). Someone who owns that provisioning should update it to 0.0.10 or repoint the suite to `agent-remotion-0010`. This is the reason group A can't clear there.
- **Ruff:** the sandbox denied `ruff` (needs approval), so I did not lint or format. Long lines were checked by hand against the 100-column setting.
- **Judgment calls:** the esbuild-or-fallback loader, and the `ASTRID_REMOTION_PROJECT_DIR` isolation in the recovery harness. Both are the smallest version I found; say if you want either done differently.
- **Commit message:** written to `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-baseline-fix-a-d/commit-msg`. `DONE` is created. The worktree contains only the three edits and no build output.
- **Suites:** no `full*` suite was requested. Only named suites with targeted files were run.
