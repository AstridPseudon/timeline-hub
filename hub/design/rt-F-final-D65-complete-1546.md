## Report

Completed F-final-D65.

- Installed the authentic App command into:
  - [README.template.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/delivery/README.template.md)
  - [gate-results.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/delivery/gate-results.md)
- Documented Runtime → Agent → App order, actual lock/digest guards, supported vendor-rebind seam, and D68 isolated staging.
- Preserved D67 appendix bytes and all qualification statuses as `PENDING`.
- Backups, candidates, hashes, and render evidence are under `evidence/`.
- Final modes/hashes: `0644`; README `f992e70a…`, gate results `8cdaa114…`.

Validation:

- `node --check .../update-manifest.mjs` — PASS
- Installer `--help` — PASS
- Controlled `delivery-build` renderer — PASS: four repo rows, resolved template markers, balanced fences.
- `git diff --no-index --check` — PASS for both docs.
- D67 appendix `cmp` — PASS.
- No active builder/service during install.
- No full suite, build, ZIP, or product tests run; intentionally out of scope.

Commit message written and `DONE` created.