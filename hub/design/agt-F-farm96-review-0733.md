# FAIL — F-farm96 cumulative evidence review

Reviewed author commit `cf0218cf5e` read-only. No product, source, census, test, or author-file edits made.

Mechanical packet checks: PASS

- Exact membership: 96/96; historical `88` + newer `8`; zero duplicates.
- Counts: environment `80`, regression `1`, unknown `15`; historical `72/1/15`, newer `8/0/0`.
- Raw Farm SHA is correctly Farm-reported only: `06d435...4dea06`, 2,089,428 bytes.
- Extract hashes and limits match:
  - Manifest: 78,899 bytes, `dad95d...fd6ee7`
  - Historical: 742,107 bytes, `597c74...97563`
  - Newer: 43,677 bytes, `ff2fa8...95e21`
- All 96 manifest line/byte offsets match.
- JSON/CSV parity: 0 mismatches.
- All 96 node sections contain the declared exception class:
  - Environment: 78 `ModuleNotFoundError`, 1 `AssertionError`, 1 `ImportError`
  - Unknown: 7 `AssertionError`, 6 `FileNotFoundError`, 2 `CalledProcessError`
  - Regression: 1 `AssertionError`
- All 12 unique source citation targets resolve to the frozen Agent `9cd3dbe...` or Runtime `45c3a7...` commits and valid source lines.
- The regression source fact is exact: `generic_host.py` is 14,313 lines while the rationale claims 13,998. `changed_source_already_addresses=false` is correct.

Blocking FAIL: prior CLOSED proof accounting

All 96 rows populate `counted_closed_proof`, but all 96 use only:

> “Farm raw log section exported verbatim; exact node header matched manifest”

That is failure-packet evidence, not a prior qualified CLOSED proof. The packet contains no genuine prior proof reference, qualified source/import scope, or relevant proof-blob/source comparison.

The official 261-closed/6-open census shows all 96 IDs already `proven_passed`, with prior proof references distributed across `env86_installed` (62), `render_cohort_0013` (9), H3 current/import (7 each), `render_wire_27934` (6), `render_node_five` (4), and other bounded proof records. Those records use distinct qualified scopes; for example H3 current uses Runtime pin `f3208b26...`, not Farm Runtime `45c3a7...`. Historical `202/65/236` counts are provenance snapshots, not Farm closure proof.

Therefore the packet currently risks duplicate credit or reopening already-closed nodes from an old failing tuple. It must either attach the genuine prior proof record and scope per node, or explicitly mark closed-proof data missing. Farm failures must not be counted as prior passes.

Additional FAIL: the single current giant-file/docs regression is classified correctly, but it is not explicitly flagged as the required current challenge.

Unknown scope: PASS

All 15 unknowns name finite missing facts:

- 7 execution shutdown/ownership nodes: retained child/process observation plus launch outcome or matched qualified tuple.
- 6 rendering nodes: producer command status/stderr and exact result-path decision.
- 2 installer nodes: child stdout/stderr and exact failing command.

No unknown was guessed.

Limits

Only standalone stdlib/hash/manifest/parity/source-boundary validation was run. No product tests, full suites, browsers, probes, installs, v2 caller tests, or production code execution were run. The v2 request/reply contract and “production caller uses it” requirement remain unproven by this narrow packet.

The worktree is clean. Commit message and `DONE` marker were created for the harness.