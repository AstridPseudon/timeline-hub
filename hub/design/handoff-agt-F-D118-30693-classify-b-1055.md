# D118 terminal30693 accounting — Part B

Read-only accounting for `agt-F-D118-30693-classify-b-1055`; no product, test, generated, pin, credential, hub, or Composition files changed.

## Terminal and partition

The genuine terminal XML is `workers/agt-F-D118-core-D89a-1024/evidence/agent-core-full-terminal.xml`. It contains 9,273 testcase elements and 450 bad nodes: 159 failed, 291 errors, 8,823 passed, and 173 passing subtests. Immutable XML enumeration gives Part A = 365 bad nodes whose authentic file maps `tests/editing_conformance/`; Part B = **85** all other bad nodes. Node IDs are unique, partitions are disjoint, and their union is exactly 450.

Part B IDs and the full partition proof are in the worker evidence files.

## Classification

| category | rows | scope/core detail |
|---|---:|---|
| PRE | 0 | none |
| KNOWN | 1 | exact D23 retained; nonblocking |
| ENV | 1 | exact D13 retained; nonblocking |
| NEW-OURS | 67 | 59 core, 8 noncore |
| REG | 14 | noncore; regression count kept separate |
| UNKNOWN | 2 | 1 core, 1 noncore |

Current core open from per-node evidence is **60**; proven regression count is **14**. One upstream-PASS/current-failure candidate remains unproven because the current timeout has no traceback and the source changed. No independent NO-GO verdict is issued.

The exact 23-node replacement scope uses `rt-D118-result-review-1001.tsv`; its bootstrap REG14 is retained, D13 remains ENV by the approved exception, and D23 remains KNOWN. The one current-only visualization timeout is UNKNOWN core, not PRE or REG.

## Evidence and limits

- `part-b-classification.tsv/json` contain one row per assigned bad node with ordinal, exact node ID, authentic XML file, outcome, safe exception/location metadata, source hashes, category, scope, core-open flag, and regression flag. No traceback, request, body, credential, or raw stack is exported.
- Historical exact506 membership remains retained through the three D108 A/B/C artifacts; their union is 506 unique IDs.
- Static XML/JSON/TSV/hash validation only. No pytest, body rerun, collection/import/helper/probe, new observer, lint, or typecheck was run.
