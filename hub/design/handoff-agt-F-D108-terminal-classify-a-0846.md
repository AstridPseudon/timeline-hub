# F-D108/D54a terminal classification — cohort A

Status: `complete_source_only`; no product/test/generated/pin/ledger edits and no body rerun.

Cohort A is independently complete: `184` unique bad current nodes, exactly the required `184`. The selector partition used only outcome != `passed`, `path=nodeid.split("::")[0]`, and the settled A regex. The remaining bad nodes were not classified here.

## Result

| category | disposition | rows | core-blocking |
|---|---|---:|---:|
| ENV | ENV-KNOWN-GAP | 43 | 0 |
| NEW-OURS CORE | CORE-OPEN | 141 | 141 |
| total | — | 184 | 141 |

The 43 ENV rows are the authenticated-legacy-archive setup boundary: current XML safely reports `KeyError` for the missing archive input, and the retained D54a rehearsal evidence classifies the matching family as `ENV-KNOWN-GAP`. The other 141 current-only rows have no upstream exact node and no same-function/body counterpart in the pinned upstream source, so D63 requires NEW-OURS; they remain core-open because terminal setup/assertion evidence does not prove a source fault or clearance.

All 184 rows are in D54 core scope. Existing owner groups are recorded per row in the TSV/JSON; the minimal groups are: F09 native-word provider, F08 CLI/native batch, F10 timing provider, M1 commitTimeline/outbox, F06 word-transcript frontend, D107 legacy read, and Runtime authenticated archive fixture authority.

## Evidence and limits

- Current XML: `72872c77087719a692bff4b48b8d85ea62b9931d59a502c8e246daee0c81c18a`; upstream-924 XML: `2941565205663912985f766210bfead7db42264976fabee7dc899d03d4f4657f`.
- Current source hashes were read from Agent `b27ff3449ec4d9b5e14ac25b8f5a18c1999c21f6` and verified against all 184 outcome rows.
- Upstream exact selectors, status, evidence and hash are explicit per row. All are `ABSENT_NO_EXACT_NODE`; upstream status/hash are therefore empty, not substituted from historical 550/276 material.
- The one cheap same-function/body AST check found no upstream test function with the cohort function name for every row (`no_function_name_match: 184`).
- Runtime isolation remains explicitly uncertain per the baseline custody review; no upstream-pass/regression claim is made.
- Missing evidence remains unresolved and core-open where live core; this report contains only safe selectors, exception classes/locations, hashes and source references, not traceback/request/credential bodies.

See `handoff-agt-F-D108-terminal-classify-a-0846.tsv`, `handoff-agt-F-D108-terminal-classify-a-0846.json`, and worker evidence under `workers/agt-F-D108-terminal-classify-a-0846/evidence/`.
