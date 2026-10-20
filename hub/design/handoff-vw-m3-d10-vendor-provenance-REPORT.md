Completed the unapplied D10 owner proposal.

- Patch: [UNAPPLIED.patch](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-d10-vendor-provenance-retirement-seam/UNAPPLIED.patch>)
- Report: [report.md](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-d10-vendor-provenance-retirement-seam/report.md>)
- Handoff: [design handoff](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-d10-vendor-provenance-retirement-seam.md>)

The patch adds a manifest-driven exclusion seam for exactly the nine package-owned component implementations and records exclusions in generated provenance. Catalogs, descriptors, schemas, diagnostics, assets, custom packs, and checkout overrides remain intact.

Evidence:

- `git apply --check` — PASS.
- Focused App tests — PASS, 18 tests.
- Vendor verifier — PASS.
- Public boundary test — PASS.
- Agent source/catalog audit — PASS.
- Generator execution was unverified because sandbox Node `spawnSync('git')` returned EPERM.

No App product files were modified. `DONE` and commit message were written.