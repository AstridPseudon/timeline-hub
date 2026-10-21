# Runtime-owned KEEP/pin release check — 2026-10-21

This is the matching concise audit report. The detailed table and evidence are in:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-m4-owned-keepers-release-check-1025/report.md`

Result: no Runtime-owned KEEP/pin is eligible for release. `rt-pin-95bd3c5f` is the only ancestor of Runtime `tl/integration`, and it is the current published producer. `rt-pin-42a7203f` is the active private017 candidate. `rt-m2-pin-a0dca169-b` is explicitly leased, and `a0dca169`, `7d1cfa6b`, `95202c2b`, `f8da4b6d`, and `fcf4c3d5` remain ambiguous because inactive configured wrappers still name them. Other clean pins have no live consumer found but are non-ancestor KEEP snapshots.

No `bin/recycle` invocation is authorized or recommended. No central test job or owned heavy job is active; the only live Runtime worker is the non-heavy private017 review (`heavy=0`). Disk free is `10,817,384,448` bytes on both `/home/user/work` and `/tmp`. No tests or mutations were performed.
