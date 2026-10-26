Ask: confirm or correct the CANDIDATE farm values below (table only, nothing executed); name the owner of each UNDETERMINED row / Owner: lead (central test service, normal receiving route, profile and admission owners) / By: before the next census

# Farm-side binding table for the fresh census (written 2026-10-26T02:35Z, no execution, no census re-run)

O = /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch

1. FARM_CURRENT_COMPOSITION_RECEIPT is REBOUND for the next run:
   path  O/queue/done/checkout-composition-635f4de06fda22a85fc2e4cfc764d0153a4c9f40  (40 hex, not the 39-hex file)
   sha256 ea43438c8e7327f152faf44d2d8e56133dd4b6aaf2205c4196d61b6c7b1e9ab1  (computed by Farm today)
   The old 39-hex file (sha 74a23cc9...) is not used again.

2. Remaining Farm-side bindings. "Candidate" = an existing object that looks right; I did not run or create anything.

| Binding | Value | State | Why / what is missing |
|---|---|---|---|
| CENTRAL_SERVICE | O/bin/request-test | candidate | Existing executable test-service client. The central service owner must confirm it is the object the receiver means (receive-farm.sh only checks that it exists and is executable). |
| CENTRAL_SUITE | O/tests/suites.conf | candidate | Existing file. I cannot see a suite entry for the 22-root core in it; the receiver only checks the file exists. Owner to confirm. |
| D73_DRY_ROUTE | D73 launcher /home/user/work/wt/agt-pin-28e56cac/tools/p4-d73-pinned-launch.sh | candidate | commands.md line 164 calls `"$D73_DRY_ROUTE" "$P4_D73_MANIFEST" dry -- ...`, the launcher's own argv shape, so the same launcher (sha 9f668e39..., 8487 B, 755) fits. No separate dry wrapper exists that I know of. Confirm. |
| CORE_ROUTE | same launcher path | set per lead 02:24Z | Launcher is the only launcher (README: no wrapper). |
| PROFILE | not determined | UNDETERMINED | Needs the Farm Remotion profile directory (managed root, Node 20.19.4, key 5ca5c561...). I could not locate it from /home/user/work/runtimes (no name with "farm") and a wider search timed out. The bench-store/registration owner (the lead, who issued agent-remotion-farm-* requests) must give the directory path. |
| DISK_ADMISSION | file to be written under the worker evidence/ folder | UNDETERMINED (not a pre-existing object) | commands.md writes it with `df -P "$OUTPUT_ROOT"`. The receiver wants an existing non-empty file before the child, so the Farm admission owner must say whether a worker may write a pre-child `df -P` witness there. Disk at last check ~9.98 GB free (child needs 5,905,580,032 B, core 4,700,000,000 B, stop 4,000,000,000 B). |
| RETAINED_ROOT | durable dir under the next census worker's own evidence/ (e.g. evidence/retained) with a KEEP marker | UNDETERMINED until the worker exists | A dir must exist when the check runs; the worker creates it with mkdir -p. The retained-state owner should confirm this location. |

3. Cannot determine (not Farm values, requested from Runtime/MAIN): the D139a schema group (installed distribution, source manifest, RECORD closure, direct_url), CANONICAL_CENSUS, DEPENDENCY_SEED, FARM_INSTALLED_KIT_SUMMARY / FARM_KIT_INSTALLATION / KIT_SOURCE_CHECKOUT.

No census re-run until MAIN/Runtime supply that group; then ONE fresh census with a fresh worker (perms rule for receive-farm present, grep count 1). No child request until READY.
