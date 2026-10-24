# FAIL — F-farm96 cumulative review

Reviewed `856de6e3f2` read-only. No artifact or product files changed.

Passed:

- 96/96 members; 88 historical + 8 newer; zero duplicates.
- Exact manifest offsets and extract hashes preserved.
- Counts remain 80 environment, 1 regression, 15 unknown.
- All 96 nodes match official 261-closed census entries and genuine prior proof memberships:
  - env86: 62
  - render cohort: 9
  - H3 current: 7
  - remaining scoped proofs: 18
- Exact outcome-map membership verified for all mapped cohorts.
- Farm SHA remains manifest-reported only; no local raw-log rehash.
- Giant-file challenge is explicit: 14,313 current lines versus 13,998 documented; docs repair remains unclaimed.
- Unknown facts remain finite: 15 total, with no guessed causes.
- Source citations resolve to valid frozen source lines.
- No Farm failure receives pass credit; current Runtime `f320` scopes remain distinct from Farm Runtime `45c3`.

Blocking failure:

- `farm96-causes.csv` loses the original source tuple for every row. Its `agent_commit`, `agent_tree`, and `runtime_commit` columns are blank in all 96 rows (288 lost cells), while JSON and the parent CSV retain the values.
- Therefore required JSON/CSV parity and source-tuple preservation fail. Correction should go to Sol as the second failure.

Validation was limited to standalone stdlib JSON/CSV/hash/manifest/source checks. No product tests, probes, bodies, full suites, browsers, gates, or v2 caller execution were run. The v2 production-caller requirement remains unverified.

Worktree is clean; commit message and `DONE` marker are prepared.