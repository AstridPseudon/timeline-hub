# Report

Completed the read-only release-predicate audit requested as the follow-up to `agt-m4-active-dependency-lease-release-plan-0819`.

Result: **blocked; retain all targets**. The active D13 worker `agt-m4-d13-current-wheel-profile-preflight-inventory-0838` still requires the exact coherent 164-pin closure and its final report. The staged profile's own provenance says finalization is pending that preflight. Gate7 private311 is not qualified: the durable current run reported 2075 findings versus a 1979 baseline and Make exit 2; the earlier source8afe run remains UNKNOWN. Pin6ef is an ancestor of current integration and the staged Agent source, but remains held by the live coherent evidence chain.

Concrete holds:

- Own lease: `orch/managers/agent/notes/coherent-gate-environments.lease`, naming `profile-staging` (944M) and `gate7-private311-source8afe` (1.5G).
- Registered wrappers: `lifecycle-coherent6f-integration` and `wrapper-two-network-coherent6f-integration` in `orch/tests/suites.conf` lines 145-146. Neither is queued or running, but both still name the staged profile interpreter.
- Active D13 preflight brief/worker; current source is Agent `5be2918c` / tree `218da961` and the staged closure remains required for its inventory.

No relevant live pytest, mypy, Runtime, pack-host, browser, Node, or coherent-profile process was found. No obsolete own lease was safe to remove. I did not remove the lease, KEEP marker, tree, or shared dependency.

Safe release condition: finish the D13 current wheel/profile preflight and manager-approved exact current Agent wheel/RECORD/origin qualification; close Gate7 private311 diagnostics with a recorded result; retire the two wrapper registrations; then recheck all queued/running tests, snapshots, briefs, leases, and processes before manager/lead recycles pin6ef and compacts the two scratch bases. Preserve all source/origin/RECORD evidence.

Durable summary: [agent-coherent-profile-release-predicate-notes-0837.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-coherent-profile-release-predicate-notes-0837.md)

Checks and results:

- `git -C /home/user/work/wt/agt-pin-6efc8150 rev-parse HEAD HEAD^{tree}`: `6efc81500a0e0688c2bb41e736503f0fc3e04abb` / `2ed2b8a12b5b3391ca221ba6ff05390f71a73556`.
- `git -C /home/user/work/agent rev-parse tl/integration tl/integration^{tree}`: `a9f4cfdaee40f3382b51d6cdb291d7012be96b8c` / `93862f0accf8bbe2331ed551b69839b47f7b8e1b`; pin6ef is an ancestor.
- `ps -eo user,pid,ppid,etime,stat,args | rg -i 'pytest|mypy|gate7|gate13|profile-staging|private311|coherent|astrid-runtime|vitest|node|uvicorn|remotion|pack-host'`: no matching live product/test process.
- `df -B1 /home /tmp`: 13,519,073,280 bytes available, 68% used (final check).
- No product tests were run or requested; no build/install/process start/full suite/native/HTTP/browser/render action was performed.
