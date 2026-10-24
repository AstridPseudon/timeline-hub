## Report

No product or test files were changed. Worktree is clean. Required `commit-msg` and `DONE` marker were written.

Evidence: central run `agt-F-env-cohort-2356-env-cohort-2356-1023235906-11789` — **69 passed, 17 failed, 0 errors/skips, 247.29s**, exact 86-node collection.

Environment custody passed: child `c886d448`, Agent `c36ca8c9`, Runtime `abd47e68`, tree `6047ac3`, Node `20.19.4`, profile `819acf`. Installed origins, RECORD/direct_url, source/body hashes, and profile/registry before-after equality were verified. No unsupported variables or shared mutations.

### Failure ownership

1. `test_private_imports_add_no_repository_or_pack_pythonpath`

   - Error: installed child action raises `KeyError: 'PYTHONPATH'`.
   - Chain: test action reads `os.environ["PYTHONPATH"]`; installed `invoke_capability` intentionally removes `PYTHONPATH`.
   - Classification: source-mode test obligation run under the global installed profile, not yet a production defect.
   - Owner: D18/test invocation; preserve installed no-ambient-import behavior.

2. `test_bootstrap_passes_inventory_identity_and_restarts_on_change`  
   `test_bootstrap_stops_on_correlated_terminal_registration_failure`

   - Error: installed-origin probe reports missing installed origins for the synthetic `/tmp/.../source` fixture. The second therefore returns `pack_host_bootstrap_failed` before reaching the mocked `registration_unavailable`.
   - Chain: `ensure_pack_host` selects installed mode globally and calls `_installed_execution_origins` before the fake launcher.
   - Classification: source-fixture/mock obligation under the wrong profile.
   - Owner: D18 invocation. Run synthetic source fixtures in source mode; installed-positive coverage must use the real installed product tree.

3. The 13 polling cases:

   `foreign_birth`, `foreign_instance`, `foreign_pid`, `foreign_source`, `terminal`, `ready@25`, `ready@400`, `exit@1/30`, `exit@1/None`, `ready@120`, `ready@150.3/30`, `ready@25` with no budget, and `ready@300` with no budget.

   - Error: `RemotionValidationError` during `registry_discovery`, with `original_wait_exit_code=1`.
   - Probe stderr: `ValueError: ... no Node executable is available for Composition's public registry API`.
   - Chain: source-profile polling fixture → `_prepare_render_validation` → registry probe; the harness globally supplies Remotion settings while its restricted PATH omits Node, and the registry context does not retain the explicit Node override.
   - Classification: invocation contamination; custody assertions were never reached. Not evidence of a startup/custody product defect.
   - Owner: D18 harness invocation first. If the same failure remains under a clean source-mode invocation, then startup/host + Runtime OPS owns it.

4. `test_generic_host_runs_external_python_orchestrator_from_admitted_pack`

   - Error: installed child exits with `ModuleNotFoundError: No module named 'external_pkg'`.
   - Chain: admission correctly derives the external pack’s `python_path_roots`; installed `invoke_capability` validates and collects them but omits them when constructing the child environment.
   - Classification: confirmed installed-production defect.
   - Owner: Agent execution/host, with Runtime OPS boundary review.
   - Smallest meaningful change: preserve only validated admitted roots for installed external Python orchestrators; do not restore ambient `PYTHONPATH`, repository aliases, or bypass the installed guard.

### Prior run disclosure

- Run `14747` stopped on an initial harness preflight assertion before qualification.
- Run `11789` collected the exact 86 nodes, then its original postflight assertion incorrectly rejected ordinary writable profile paths. The postflight comparison was corrected manually without rerunning the cohort; the final 69/17 result remains authoritative.

### Future bounded acceptance

- Installed positive: all product imports resolve under the selected noneditable child installation; foreign source roots, aliases, and ambient `PYTHONPATH` are refused.
- Source bootstrap positive: inventory changes restart the host; terminal registration errors propagate; polling honors progress and cleanup.
- Registry negative: missing/failed probes never become readiness or cleanup proof; no profile or registry writes occur.
- External-pack positive: admitted `external_pkg` imports from the exact fenced pack root, while ambient paths are ignored.
- External-pack negative: outside-fence roots and changed source digests refuse before child execution.
- Private imports: source mode retains the required controlled environment while excluding pack/repository roots; installed mode retains no ambient or private-pack import authority.

No new test run was performed. The sole full run remains `FAIL267`; no full/body rerun was requested. Evidence files: [outcome-map.json](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-env-cohort-2356/evidence/outcome-map.json), [pytest.log](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-env-cohort-2356/evidence/pytest.log).