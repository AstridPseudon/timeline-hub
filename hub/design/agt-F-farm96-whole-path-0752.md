# F-farm96-whole-path report

Read-only audit completed. No reviewed artifacts or product files changed; worktree remains clean.

Findings:

- Farm manifest/extract path is intact: 96 unique IDs, cohorts 88+8, all headers, offsets, extract hashes, and counts match.
- JSON retains the failed Farm tuple:
  - Agent `9cd3dbe8…`, tree `57f0231d…`
  - Runtime `45c3a7f4…`
- The 288 missing CSV cells originate at the JSON-to-CSV projection. Tuple data lives under `source_tuple` / `rows[*].failed_farm_tuple`, but the CSV projection reads flat row keys.
- Additional loss: `source_citation` is blank for all 96 rows (96 cells). Parent CSV had all 384 cells populated; all other shared cells are unchanged.
- Required mapping before publication:

  `rows[*].failed_farm_tuple.{agent_commit,agent_tree,runtime_commit}` → CSV tuple columns

  `rows[*].source_citations[*]` → CSV `source_citation`

- Farm 187 is not directly comparable as a schema: its tuple is packet-level `source_run`, while its CSV contains only mapped per-node setup fields. Farm 96 explicitly exposes tuple columns, so blank values are a real provenance loss.
- Preserve the distinction between failed Farm tuple and qualified prior-proof tuple. Do not substitute current Runtime `f320…`, invent PASS credit, or reopen current failures automatically.
- Existing `80 environment / 1 regression / 15 unknown` remains bounded evidence classification, not a literal-exception-only conclusion. Farm 187’s separate `47 Runtime tuple mismatch / 140 environment` classification must not be merged into it.
- Remaining limits: raw Farm log only has manifest-reported SHA/size; exact PASS IDs/JUnit are unavailable; seven summary failures lack node identities; production v2 caller qualification remains unverified.

Validation:

- Standalone stdlib source/manifest/extract validator: PASS.
- `python3 -m json.tool farm96-causes.json`: PASS.
- `git diff --check`: PASS.
- No product tests, probes, full suites, browsers, gates, or live caller execution run.

Commit message and `DONE` marker were prepared at the assigned worker paths.