# Agent coherent profile release predicates

Audit completed 2026-10-21 08:40 UTC for the prior `agt-m4-active-dependency-lease-release-plan-0819` audit. No release predicate is fully satisfied, so no lease, KEEP marker, tree, shared dependency, or staged scratch was removed.

## Current evidence

- Agent integration is `a9f4cfdaee40f3382b51d6cdb291d7012be96b8c`, tree `93862f0accf8bbe2331ed551b69839b47f7b8e1b`.
- `profile-staging` is 944M at `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m4-private-coherent-pair-staging/profile-staging`. Its provenance records the exact 164-pin digest `478af081...034761`, Runtime `b92d3e7a` / tree `6abc2f11`, client `95bd3c5f` / tree `d3a290b4`, and Agent `6f2d8c35` / tree `698ae4df`. It explicitly says finalization is pending the aggregate D13 preflight and report; no native/socket/render/browser/full qualification is claimed.
- Private311 typing scratch is 1.5G at `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m4-gate7-private311-mypy-once/gate7-private311-source8afe`. The retained current proof used the exact private 3.11 environment and failed: `2075` findings versus `1979` baseline, Make exit `2`. The earlier source8afe attempt remains `UNKNOWN`, not pass/fail. The diagnostic partition says exact IDs/lines were not retained, and repair/qualification is unresolved.
- Pin `agt-pin-6efc8150` is detached at `6efc81500a0e0688c2bb41e736503f0fc3e04abb`, tree `2ed2b8a12b5b3391ca221ba6ff05390f71a73556`, with its own `KEEP`. It is an ancestor of current Agent integration and also of the staged Agent source (`6efc8150 -> 6f2d8c35`), but the coherent lease and current D13 work still retain the related evidence chain. Keep it held until the coherent profile is finalized and its ancestry is no longer needed; recycle only by manager/lead after a fresh predicate check.

## Active dependents and negative checks

- Worker `agt-m4-d13-current-wheel-profile-preflight-inventory-0838` is still running. Its brief requires the coherent 164-pin closure, origin/RECORD fences, exact current source `5be2918c` / tree `218da961`, and an exact next-build/install recipe. This is the concrete current consumer of the staged closure.
- The own notes lease `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/managers/agent/notes/coherent-gate-environments.lease` still names both `profile-staging` and `gate7-private311-source8afe`, and says to release only after final coherent current-source proof and diagnostic repairs no longer consume them.
- Registered wrappers remain in `orch/tests/suites.conf`: `lifecycle-coherent6f-integration` (line 145) and `wrapper-two-network-coherent6f-integration` (line 146), both naming the staged profile interpreter. No request for either wrapper is queued or running; the queue has no active test request for these targets. They must be deregistered or otherwise retired before the staged profile can be considered unused.
- No relevant live `pytest`, `mypy`, Runtime, pack-host, browser, Node, or coherent-profile process was found. The D13 preflight worker and the Gate13 repair worker are orchestration workers, not product processes; Gate13 has a recorded seven-case run failure on the Runtime schema digest mismatch and does not provide a release proof.
- The only own lease found is `coherent-gate-environments.lease`; there is no obsolete own notes lease safe to remove. Historical briefs still mention the targets, but the active D13 brief and the suite wrapper registrations are sufficient concrete holds.

## Release predicates and next task

Do not release now. The final task before a later release audit is: finish the active D13 current wheel/profile preflight, obtain the manager-approved current Agent source and exact wheel/RECORD/origin closure, perform the existing final coherent profile build/install and required D13 qualification, and separately close Gate7’s private311 diagnostic repairs with a recorded result. Then retire the two coherent wrapper registrations, confirm no queued/running test, snapshot, brief, lease, or process names either scratch path, and recheck pin ancestry before asking the manager/lead to recycle `agt-pin-6efc8150` and compact the two finished scratch bases. Preserve source, origin, wheel, and RECORD evidence; do not weaken checks.

## Disk

At final audit check: `/home` and `/tmp` had 13,519,073,280 bytes available (13G, 68% used). Target sizes were pin6ef 114M, profile-staging 944M, private311 1.5G, and current captured diagnostics 44K.

No tests were run or requested. No build, install, process start, suite full*, native, HTTP, browser, render, or shared-dependency mutation was performed.
