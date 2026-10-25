## Report

Implemented D87 exact Agent-authored migration prose in:

- `ORCH/delivery/README.template.md`
- `ORCH/delivery/gate-results.md`

Preserved D65/D67/D62/D77 requirements, C0 v2 shapes, pending qualification status, six live checkout cases, and upstream packaging checklist.

Verification:

- Source SHA: `8e97845820adeeb4aa1c3a65582137a3c68b27892a88de2173e24d9288e5d702`
- Installed README SHA: `06aa4386a58dd8e1f1dc3f5fdfa0114a0dd98723819f842adff8c6a5a8c243e5`
- Installed gate-results SHA: `7576346c402a7c59fd30f2007867542dc848f60be501cefac5bc730620d5e29c`
- Both files: regular mode `0644`
- Real installed `delivery-build.render_readme()` controlled four-repo stub: PASS; placeholders resolved, fences balanced, links present.
- Candidate byte equality, preservation checks, active-builder check, and `git status --short`: PASS/clean.
- Backups: `20261025T010843Z`; README correction backup `20261025T011024Z`.

No product/test/schema/pin/build/ZIP/full-suite changes or runs. Commit message written as `docs(delivery): F-final-D87 install CLI migration prose`; `DONE` created.