# F-D89 bounded successor continuation packet

Private source/static input for the existing MAIN runner. This is a continuation of published F-D89 packet 0200; packet 0200 remains READY on MAIN and is preserved byte-for-byte under `original-0200/`. No behavior or final-gate credit is claimed.

## Exact additional delta

The continuation adds 69 unique canonical selectors, disjoint from the original 0200 161. The corrected 0200 metadata is 15 disjoint family keys (not 16); the original report is not edited. The new union is 230 selectors across 18 family keys.

- current-sheet: 13 init/emitter-corrected FAIL rows from `64166f7`, normal home `3b8f341c`, review 0203.
- M1 baseline: all 10 authentic ERROR rows with the exact semantic-step assertion mismatch, source `4f4f26c`, normal home `9838f7ca34`, review 0147.
- word bootstrap: 37 native-word ERROR rows plus 9 next-cohort ERROR rows sharing the corrected rational-FPS fixture `9e88f5b`, normal home `5dc9f0c`, review 0152.

The current-sheet inverse-coverage row and three CLI-scope rows are LIVE HELD. The nine separate native-word semantic FAIL rows are LIVE HELD. There is no broad retirement.

## Authentic inputs and accounting

- Authentic actual10077 is copied as `actual10077.xml` with 268 selectors / 245 XML testcases and outcome counts 176 ERROR, 39 FAIL, 30 PASS, 23 NO_JUNIT_CASE. Outcomes are copied as `actual10077-outcomes.tsv`.
- Combined selected accounting is 157 observed rows (140 ERROR, 13 FAIL, 4 NO_JUNIT_CASE) plus 111 remainder rows = 268. The original 0200 remainder remains unchanged under `original-0200/remainder.tsv`; `combined-remainder.tsv` is the new exact complement.
- `original550-dispositions.tsv`, `original550-rollup.tsv`, `original-held.tsv`, and `unexecuted-23.tsv` are byte-preserved copies. The 23 authentic NO_JUNIT_CASE rows remain UNKNOWN/HELD; absence is never inferred as PASS.
- `additional-membership.tsv`, `additional-selectors.txt`, `combined-membership.tsv`, `combined-selectors.txt`, `additional-held.tsv`, and `per-node-source-map.tsv` are the runner inputs and audit tables.

## Source/dependency joins

The occurrence48 correction remains only in the original 0200 union: commit `095177db` changes `_create_fixture` in `test_commit_runtime_occurrence_media.py` to accept the semantic birth, then rehydrate the exact Runtime source mapping before guarded patches; home receipt is `25c1e182`. M2 pool, inverse-stage, parent-media, and auto-placement rows are not added because no new reviewed dependency after authentic10077 fixes their exact first exception.

The source manifest records current four-repo homes/trees/files and exact reviewed/home SHA-256 equality. The C0 v2 request/reply shape for sections 1–5 is retained unchanged in `c0-contract-sections1-5.json`: api_version 1, project/timeline IDs, exact base revision/publication IDs, command schema fields, label/steps/patch/optional reads, mergefields|atomic, optional declared reads, Idempotency-Key, dry_run/source/rationale/group_id, accepted|merged/conflict|invalid|preview replies, and unchanged authority/ABI/ABA/no-write/no-leak/45s guards.

## Verification boundary

Only static JSON/TSV exact-set, uniqueness, selector-existence, source-hash-equality, and inherited-recipe `bash -n` checks were used. No pytest, collection, helper/function/fixture execution, service, build, browser, render, probe, install, registry, pins, checkout, reconstructed outcome, or environment result was run. MAIN four-SHA custody/preflight/service and functional receipts remain PENDING.
