# D136a independent boundary review

## Verdict

FAIL all findings once / NO_GO. The input has the requested 45 row IDs and maps all nine final predicates, but its source citations do not cover every helper guard and observation resolver statically traversed by the cited call sites. More importantly, B022 proves a current Runtime fail-closed refusal, not a product regression.

## Findings

### F-D136A-001 — PASS: finite row and selector mapping

`table.json` has 45 unique boundary IDs in P1–P4. B-FINAL-001 through B-FINAL-009 are nine distinct rows: three standalone predicates plus the six values `parent`, `child`, `new_shot`, `duplicate`, `remove`, and `sdk_bundle` from the parametrized selector. This is structural coverage only; no body result is claimed.

### F-D136A-002 — FAIL: source-citation completeness

The table groups the principal call sites correctly, but the citations do not cover helper definitions that contain statically traversed refusal/observation conditions. The complete bounded list is in `coverage.json` under `missing_guard_observation_citations`:

- Agent candidate compile helpers: `authoring_bundle.py:185-233, 679-772, 775-820, 837-888, 948-997` (B005–B007).
- Agent request materialization/fork helpers: `authoring_commit.py:190-261, 264-335` (B008).
- Agent commit execution between the cited ranges: `commit.py:1206-1398` (B014–B015).
- Runtime alias, path, read, projection, child and manifest helpers: `timeline_commit_auth.py:18-264, 608-778, 1833-2186` (B021–B025, B029, B032).
- Runtime sequential-capture helper definitions: `timeline_commit_auth.py:2338-2560` (B020, B026–B028).
- Runtime store helper/destination/reference-projection branches: `timeline_commit_store.py:1491-1565, 1576-1788, 1810-1905` (B018–B019, B034).

These are citation/condition coverage gaps, not newly asserted dynamic failures. Downstream outcomes remain UNKNOWN.

### F-D136A-003 — FAIL: B022 is overclassified as REG

The immutable Runtime source contains the refusal at `runtime_protocol/timeline_commit_auth.py:2209`:

`provider intermediate command lacks an authenticated physical observation`

The exact original9 evidence proves nine occurrences of that refusal and no later body reach. It does not expose the physical record, ref/path, command ordinal, or producer payload. A valid fail-closed guard refusal alone cannot prove that current behavior regressed from pristine behavior. It also cannot identify Agent core, provider capture, or Runtime adapter as the causal owner. The correct finite classification is:

`observed current Runtime refusal; regression UNKNOWN; causal owner UNKNOWN; setup failure not proven; D54a upstream REG not proven.`

No guard relaxation or product-fix authorization follows from B022 alone.

### F-D136A-004 — PASS_WITH_UNKNOWN downstream

B023–B036 and B-FINAL-001–009 are statically listed and correctly remain unreached/UNKNOWN. The table does not turn downstream predicates into setup failures or binary pass/fail results.

### F-D136A-005 — PASS: D54a/pristine separation

The retained D54a paired-cause reports qualify zero current upstream regressions for this path. The 886a comparison records source absence for the joined D136 files; absence is not behavior. No D54a REG is imported into this review.

## Evidence limits and handoff

No source, fixture, product, pin, test, branch, or release files were changed. No pytest, collection, fixture evaluation, source execution, browser, service, profile, benchmark, or full suite was run. The next evidence required is an exact safe record/ref/ordinal or a source-equivalence/pristine behavior comparison, followed by a new qualified original9 run.
