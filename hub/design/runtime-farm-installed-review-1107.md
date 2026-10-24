## Result: FAIL — publication gate only

Local integrity is PASS:

- All five live files match exact pins, root-owned, nonsymlinked, with modes `0644/0755/0755/0755/0755`.
- Four predecessor backups match exactly; component was previously absent; no `.new` leftovers.
- Ordered idle/install receipts and protected-route hashes pass.
- Production requester/maker/Store static trace passes, including Farm authority, schema carrier, staging/final/reuse, exact test2 inventories, and fail-closed schema/source checks.
- Missing schema input independently refuses with exit `2`.

Publication:

- Genuine normalhub now matches live for all five files, including the new component.
- Committed `HEAD b8cc9e75…` remains stale: old four-file hashes and no committed component. This is publication lag, not installer failure. Normalhub advanced via authorized hub-sync commit `b8cc9e75…`; no sync or Git write was performed.

Evidence reviewed: [install-receipt.txt](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-OPS-farm-kit-install-1105/evidence/install-receipt.txt), source `6de00342…` / tree `3e724905…`, security1053 PASS, result1058 PASS, installer1105 PASS. The receipt contains transient failed diagnostic probes, followed by successful reruns and final PASS markers.

Commands run:

- `bash -n` requester/maker — PASS.
- Python in-memory compilation and production-caller static trace — PASS.
- Physical hash/mode/ownership/backup audit — PASS.
- Read-only publication observation for 5 seconds — normalhub PASS; committed publication stale.
- No 268/140/74/54 reruns or real requests.

Existing schema/child admission hold, HTTP403 refusal, and Agent-owned remote verification remain unchanged. Commit message and `DONE` marker were written; worktree is clean.