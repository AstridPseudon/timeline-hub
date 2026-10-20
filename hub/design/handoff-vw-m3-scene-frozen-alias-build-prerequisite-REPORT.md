# Frozen Scene alias/build prerequisite handoff

The private central harness now keeps `remotion` beside the copied Agent
source tree, which is required for the normal `webpack-alias.mjs` root
calculation (`remotion/..` -> `astrid/packs`). It preflights the normal
generated registries, resolves all 45 component imports, runs TypeScript, and
bundles the immutable public13 package before any managed query.

Evidence and exact commands are in the worker report:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-scene-frozen-alias-build-prerequisite/REPORT.md`

Artifacts:

- `handoff-vw-m3-scene-frozen-alias-build-prerequisite.patch`
- `handoff-vw-m3-scene-frozen-alias-build-prerequisite.source.py`
- worker `COMMAND` (one deferred `scene-central-owned-suite-retarget` command)

The owner `owner-source-registry.patch` remains unapplied. Do not submit the
managed command until Agent confirms the exact staged preflight and no
duplicate proof.
