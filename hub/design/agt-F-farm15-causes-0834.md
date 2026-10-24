# F-farm15-causes report

- Reviewed all 15 unknown nodes from the bounded packet.
- Resolved: **0/15**; remaining: **15 unknown**.
- Counts unchanged: **80 environment / 1 regression / 15 unknown**.
- Added exact group evidence, owners, missing finite facts, and Farm offsets to [farm96-causes-source-and-limits.md](/home/user/work/wt/agt-F-farm15-causes-0834/farm96-causes-source-and-limits.md).

Remaining facts:

- 7 lifecycle/owner-marker nodes: child stderr/launch outcome or matched qualified tuple proving worker/process startup. Citations: `test_generic_host_actions_v3.py:1497`, `:1770`, `:1816`.
- 6 render-wire nodes: producer command status/stderr and exact `result.json` creation decision. Citation: `test_conformance.py:87`.
- 2 installer nodes: child stdout/stderr and exact failing command. Citation: `astrid/installer/backend.py:57`.

Validation:

- JSON syntax, 96 unique rows, counts, 15-node grouping, 2,976 mapped-cell JSON/CSV parity, offsets/citations, and artifact hashes — **PASS**.
- `git diff --check` — **PASS**.
- No product tests, probes, subprocesses, full suites, or new checkpoints run.

Commit message written; `DONE` marker created. Production v2 caller qualification remains unverified and was not altered.