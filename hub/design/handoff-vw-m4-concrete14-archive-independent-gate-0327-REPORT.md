# Immutable14 archive independent review

**BLOCKED.** The authorized producer terminated before creating the concrete
0.0.14 archive. Its guarded pack passed source/tree, registry-check, build, and
build:test gates, then failed the required `scripts/gen-registry.test.mjs`
focused test because child Node `spawnSync` returned `EPERM`; `npm pack` was
never reached. No archive SHA exists, and no archive/member/export/provenance
or packed consumer review was performed.

Producer report and raw result paths, plus exact hashes and commands, are in
the worker report:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m4-concrete14-archive-independent-gate-0327/REPORT.md`
