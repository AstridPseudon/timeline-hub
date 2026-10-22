# U1 v1 operational cleanup audit

## Result

**PASS — cumulative safety/configuration review of the partial cleanup.** No unauthorized deletion, product change, active-reference loss, or suite syntax defect was found. This is not a completion certificate: the artifact cleanup remains blocked and the 15 GB free-space target was not reached.

## Configuration diff

Compared:

- Before image: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-U1-v1-cleanup/suites.conf.before-u1-v1-cleanup`
- Current: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/suites.conf`

The before image is 152 lines / 110 non-comment rows; current is 145 lines / 103 non-comment rows. The exact diff contains only these seven removals:

```text
runtime producer-agent0a-integration
runtime capture-agent92427b3a-integration
runtime capture-agent92427-integration
runtime capture-agentcf7448-integration
runtime producer-agent-s2-integration
runtime registered-assembler-canonical-target
runtime text-native-private-pair-integration
```

Each removed command points to one of the explicitly named abandoned v1 worker outputs in the cleanup brief: the producer/capture source copies, registered probe, S2 producer source, or private text/runtime pair. No removed row names v2, current, generic, farm, or common controls. The current `full` and `targeted` controls remain present for Agent, Runtime, App, and Composition, and Runtime `quick` remains present; exact unchanged diff also preserves all other current/reference rows.

Final current-config SHA-256: `8e8a504d4c216fd8b05f860353d5dfb6230cfd9a1e78d06ecc8f64dc5002350a`.

Before-image SHA-256: `df6d8d504c8dd174b96944ff681ea7ea2dd7a017348c90f9be7be55556b3ce48`.

## Independent validation

- Parsed every non-comment line as `repo`, `suite`, and `command`: 103 rows, 0 malformed rows.
- Duplicate `(repo, suite)` keys: 0.
- Ran `bash -n` separately on every extracted command, without executing commands: 103 checked, 0 failures.
- Rechecked all six named `agent-source` trees and the private `runtime-candidate`: 7 entries, 704,053,248 bytes, all present; no symlink entries.
- Rechecked the remaining classified inventories: 885 design entries / 401,340,741 bytes; 1,465 test entries / 82,546,688 bytes; 12 delivery directories / 132,501,504 bytes; 1 work-wt test tree / 15,032,320 bytes; 1 v1 artifact / 4,037,153 bytes. All 2,371 entries (1,339,511,654 bytes) remain present and non-symlinked.
- Candidate process/marker scan found no target worker/test process, `running`, `lease`, `READY`, or `KEEP` marker. No candidate path was referenced by the current suite config.
- `git status --porcelain` was empty in `/home/user/work/{agent,runtime,app,composition}`.
- The original log, original `meta`, original `brief.md`, preserved before-image, resumed log/meta/brief/report, and blocker markers remain present. The stopped original worker has no `report.md`; its `STOPPED` marker and log are present, so this is an expected absent final report, not evidence of deletion.

The original deletion attempt and resumed deletion attempt were both rejected before execution by the platform safety guard (`rm -f style commands are not permitted`). Therefore cumulative deleted artifact bytes are **0**; no credentials, toolchain, shared dependency, symlink target, product worktree, worker evidence, or active v2 reference was deleted. The resumed report's statement that the six integration worktrees were already missing is consistent with the separate worker scratch source copies still being present; no product worktree was removed.

## Disk and limits

The original worker recorded 10,574,262,272 available bytes immediately before and after its rejected deletion. The resumed worker recorded 10,519,494,656 bytes at its final check. My final read-only check observed 10,511,495,168 available bytes (filesystem activity accounts for the variation); none is attributable to this cleanup. Against 15 GiB, the final reading is short by 5,594,632,192 bytes; against decimal 15 GB, it is short by 4,488,504,832 bytes. Even reclaiming the entire currently classified 1,339,511,654-byte inventory would not reach 15 GB.

Reference validation is limited to the exact before/current config diff, current process/marker/queue/path scans, and the preserved worker evidence. No historical dependency proof can be inferred for inactive artifacts, and no product branch was checked out, altered, or tested. No full, browser, live-socket, product lint/typecheck, or deletion test was run; these are N/A and were prohibited for this operational prose/configuration audit.

## Recommendation

Keep this review PASS for the work actually performed. If cleanup is still required, use an approved/sanctioned deletion mechanism outside the refused worker route, then revalidate the inventories, active references, symlinks, product worktrees, suite diff, and disk reading before claiming completion.
