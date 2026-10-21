# Agent custody/Main invariants: independent security review

**APPROVE the bounded correction** at `2c2c679c983d40e4370402c962dc37be5f94dc79`, tree `60ada95e47a13849556456fe1b3917620954e575`, branch `tl/agt-m4-custody-main-finally-private-directory-0612`. No blocking finding in its retained-pidfd transfer or newly allocated Windows directory paths. Approval does not certify native Windows/macOS, the current D13 join, or all infrastructure differences from Main.

Read PLAN first. Reviewed the committed candidate directly in this assigned worktree, whose HEAD/tree and product/test bytes match the candidate. Compared its parent `de36e302e3ee6e950e22aed5c02c02163f7cf5c8` and Main497 `497714c73531f164082555ec81b61ca5bc8b6554` (tree `daaeb1149898dd327947e21c554b484094f960b2`). Candidate scope: only `custody_broker.py` (+29/-15) and `generic_host.py` (+9/-2); no test changes. This is the independent review required by the owner 16:16 condition, limited to this correction.

## Ownership and exact-incarnation authority

Before the commit, Linux registration opened the pidfd and performed identity/inheritability setup without Main's encompassing cleanup guard. It also inserted the signal handle before constructing/registering its proof. Exceptions could therefore leak an untransferred descriptor or leave partially registered custody.

At `custody_broker.py:3126–3157`, the candidate restores Main's `retained = False`/`finally` structure and extends it through proof construction and registration. Initial birth admission remains unchanged. After open, identity mismatch/exception, inheritability failure, or a propagating proof/setup exception reaches cleanup before ownership transfers. The descriptor is installed in `_handles` only after proof registration and stale terminal-provenance removal. The custody lock covers this sequence, proof queries and release; no observer can consume its intermediate ledger state.

Failure before proof creation closes the pidfd once. Failure after a returned proof exists closes its watch; if registered, that same proof is removed from the proof map before closing the pidfd. A failed `_handles` insertion therefore does not strand a registered proof. Success sets `retained` and leaves both resources to `release_pidfds`; repeated registration returns the existing entry. The four strict controls explicitly verify that later release does not close a failed-admission descriptor twice. `bind_launch` still retains the original Popen and latches its admission error.

The existing `_PidfdExitProof` implementation and process-group code are unchanged by this commit. Expected epoll allocation/registration errors produce an unavailable watch, which cannot prove exit; custody may retain its signal handle without granting an exit exception. Other constructor exceptions propagate through the restored pidfd guard. Proof remains the private bind-time watch with MOD → poll → MOD and the exact accepted event masks, rather than descriptor metadata or generic readiness. The exact `(pid, birth)` ledger lookup, conditional-release terminal birth, and absence of terminal provenance on unconditional release are unchanged. A live original, dead substitute, changed PID, or missing observation cannot acquire positive exit authority. Existing original-Popen reap and retained-incarnation checks remain the only relevant reuse exceptions; replacement descendants remain excluded.

Inspection covers the proof-construction and dictionary-registration exception windows. No new fault-injection tests were authored or run for those windows. The existing private observer must remain exclusively custody-owned, as documented by the earlier kernel-watch review.

## Windows allocation and accounted roots

At `generic_host.py:5317–5344`, configured Windows attempt-base children and ephemeral Windows roots again call `platform.private_directory` before use. The explicit Runtime source routes that helper to restricted-DACL creation and validates existing directories; plain mkdir/chmod is no longer the creation operation on these paths. POSIX behavior is retained.

Ephemeral Windows names remain `astrid-attempt-` plus a random token, without task/attempt identity in the basename. Configured base children retain their existing task/attempt namespace and collision check. Allocation returns to the same claimed-attempt path: identity stays in the lease/progress marker; the same root contains scratch and outputs; live storage/evidence accounting and owned-root deletion/budget release are untouched. The newer `.r-` scratch marker and accounted-root resolver are unchanged. This is source-composition review plus the two mocked Windows controls, not native DACL or Windows renderer qualification.

One inherited Main difference remains outside these newly allocated paths: the explicit caller-owned `attempt_root` branch lacks Main497's final Windows `platform.owner_only(root)` call. This predates the candidate and is unchanged by it. Orchestrator should triage that difference separately; this approval does not assert Main-equivalent Windows permissions for caller-owned spools. The known rendering resolver platform-boundary issue is likewise outside this patch.

## Test preservation and evidence

Byte comparison against parent and worktree passed for all six relevant files: `test_pidfd_callers.py`, `test_platform_helpers.py`, `test_process_group.py`, `test_custody_broker.py`, `test_generic_host_attempt_isolation.py`, and `test_remotion_attempt_temp.py`. Every original top-level test definition (including decorators/assertions) present in Main497's corresponding five existing files is source-identical. The first two files differ from Main only by a pre-existing trailing blank line; process-group tests contain the earlier additive proof controls. No assertions, skips, xfails or behavior expectations changed here.

Fresh reviewer command, from the assigned candidate worktree:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" \
  /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider \
  tests/core/execution/test_pidfd_callers.py::test_custody_post_open_failure_closes_untransferred_handle \
  tests/core/execution/test_platform_helpers.py::test_windows_attempt_directory_is_private_from_creation \
  'tests/core/execution/test_process_group.py::test_pidfd_kernel_watch_refuses_descriptor_faults_with_shared_metadata[live-False]' \
  'tests/core/execution/test_process_group.py::test_pidfd_kernel_watch_refuses_descriptor_faults_with_shared_metadata[other-exited-True]'
```

**8 passed in 0.97s**, exit 0, no skips: four post-open failures, two Windows controls, live-original and exited-other-pidfd substitution negatives. The latter keeps a duplicate original descriptor, models shared metadata, and refuses proof, conditional release and synthetic PID-reuse census while the original is alive. Numeric PID recycling was simulated, not forced. Runtime was `/home/user/work/runtime` at `b92d3e7a05eec65c142294ef4873edd059e9b31d`, tree `6abc2f117391de8e7e35c0283f575a002199894d`; dependencies remained read-only.

Inspected the implementation worker's raw log, `workers/agt-m4-custody-main-finally-private-directory-0612/log.txt` (results at lines 5611, 5617, 5626). Its preceding commands use the same worktree-first PYTHONPATH and Python, with these selections:

- Four failure cases + both Windows cases + `test_custody_retains_runtime_pidfd_and_preserves_signal_fences`: **7 passed in 0.92s**.
- `tests/core/execution/test_process_group.py -k pidfd`: **23 passed, 69 deselected in 0.88s**; includes genuine zombie/reaped exit, conditional release, watch failure and substitution controls.
- `tests/core/test_generic_host_attempt_isolation.py tests/packs/rendering/test_remotion_attempt_temp.py tests/core/execution/test_platform_helpers.py -k 'attempt or windows_attempt_directory'`: **11 passed, 21 deselected in 1.13s**.

These 7+23+11 results are implementation-worker evidence, not fresh reviewer reruns. Fresh `git diff --check HEAD^ HEAD` and the byte/source-definition audit both exited 0. No full, native, D13, browser, renderer, socket or central suite was requested or run.

## Delivery and next step

The required Main-infrastructure delivery note is present at `design/agent-main-infrastructure-touched.md`, including the 2026-10-21 line naming post-open cleanup/proof transfer and Windows private attempt-root restoration. Preserve it in delivery notes. The orchestrator may integrate this exact bounded correction and handle the inherited caller-owned Windows difference separately. No blocker for this review task. No product/test edits, shared-dependency writes, commits, merges, checkouts, pushes or ref mutations were performed.
