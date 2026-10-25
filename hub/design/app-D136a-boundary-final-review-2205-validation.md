# D136a final validation

| Check | Result |
|---|---|
| JSON parse of current review/table/manifest and prior coverage | PASS |
| Finite row inventory | PASS: 45 unique rows; 9 final predicates |
| Shared groups/maps | PASS count only: 6 groups; 30 condition maps; 31 AST entries |
| MGC source/helper/caller span match | FAIL: remaining findings F-D136A-FINAL-001..003 |
| Agent source hashes against supplied manifest | PASS: 9 files |
| Runtime immutable source hashes against supplied manifest | PASS: 6 files |
| Agent source-only diff from joined 90b59 | PASS: none |
| Assigned worktree status | PASS: clean |
| Agent AST parse-only validation | PASS: 15 manifest Python files |
| Pristine 886a comparison | PASS as source-absence-only; no behavior inferred |
| Dynamic execution, pytest, collection, fixtures, browser, service, profile, collector, benchmark, child/acquisition | NOT RUN by task rule |

Observed source identities: Agent HEAD `8b13a9829989150ac0387c31559c5d54d386cc57`, tree `897c318f237fbb78bebb3185c133f43ffc4fa38e`; Runtime immutable HEAD `ab1e4f6141987706132916e2da16477f5a019464`, tree `7d8e77b2f5a4af79305c9212ce5174d3ea9fd657`.

No source, test, fixture, pin, product, Runtime, or evidence-input file was modified.
