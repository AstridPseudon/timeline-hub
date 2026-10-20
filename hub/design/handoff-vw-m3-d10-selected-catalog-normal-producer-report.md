## Report

- Confirmed normal descriptor: `rendering/effect/audio-reactive-colour@sha256:8e3a…`
- Confirmed hosted builtin remains distinct: `@sha256:2a9b…`
- Identified exact missing seam: hosted App disables the existing virtual admission module and `/api/astrid-element-admissions` when `runtimeOrigin() !== ''`; therefore no normal `DocumentPin`/snapshot reaches `admittedCatalogEntries()`.
- No product files changed; no descriptor/hash/API was forged.
- Targeted tests: **93 passed in 15.19s**
- Pure identity/schema/component probe: **PASS**
- `git diff --check`: **PASS**
- Handoff: [report.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-d10-selected-catalog-normal-producer/report.md)
- `DONE` and commit message were written.

Next step requires Agent/Runtime owner agreement to publish the normal admission tuple through the existing supported carrier before App2 adds the selected-PARAM journey.