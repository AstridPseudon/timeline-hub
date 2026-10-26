# Validation

All checks were read-only documentary checks; no product imports, pytest, collection, body rerun, suite request, typecheck, or lint were run.

- `git show tl/agt-P4-D141-result-review-0114:evidence/*` — PASS: exact review blobs read; prior result review remains `FAIL` with one stale-JUnit finding.
- JSON/hash checks over the 0055 input/materialized manifests, runmanifest, body command, central request/summary/snap/ext/status/exit, registration, result, and source receipts — PASS for recorded hashes and paths.
- `shlex` parse of `p4-d141c-normal.command` — PASS: `-m pytest` precedes the pytest options, later `-m integration` is present, three concrete selectors are present, and `--junitxml` names the actual 0055 XML.
- `xml.etree.ElementTree` parse of `p4-d141c.xml` — PASS: one suite, 3 testcases, 0 failures, 0 errors, 0 skipped, time `23.668`.
- Exact source tuple comparison using read-only `git rev-parse HEAD`, `HEAD^{tree}`, and clean-status checks on the four pinned checkouts and `/home/user/work/agent` — PASS. Agent `28e56cac...` / tree `2ebe2ddf...e58a`; Runtime `6a011d58...` / tree `ac5b862...da28`; App `867cb273...` / tree `2b44a46...7dd`; Composition `635f4de...` / tree `5ab5191...148`.
- Exact original-test source hashes — PASS: CLI/sheet `8239ad0c...f213`, ten-note `c0132e0d...6d0a`, rerun `02ffa657...7f36`; combined launcher guard `b183e62ff08f9a56a9fe074cc84729eb9dba15e29f6590fe177df3ee42f4d6ac`.
- Selector manifest comparison — PASS: the 0047 selector file and 0055 `inputs/p4-d141c-final.selectors.tsv` are byte-identical at SHA `59a41669300bdd97fbe7925a36958534abb7a5d7e793dd4ee26fb8c197668ac4`; the old JUnit path is absent and the actual 0055 XML exists.
- CAS receipt comparison — PASS from retained `registration.json`: candidate row `21f407285a7f1476e9507add8d8d54e723776d6ce5074ac7cbbe8be5773c2f0b` installed exactly; registry preimage/backup `2a1b549f...a55858`; after `f59adb4816a5e8d0db445956af585daf9a771679cfbe2f2f1a6780529edb2aa0`; outside rows unchanged `660b72d846441f4fb4d79ad29c75dace7bfdc315f07eef4bd9f79f27e72c063c`.
- Historical conservation — PASS: 1347 is retained as exit 1/zero selectors/no JUnit; 10086 is a distinct service ID and actual 3/3 body. D97 is comparison-only and was not rerun.

Typecheck/lint are N/A: this worker made no executable source change. Full suite, live socket/browser suite, and product qualification are intentionally unverified.
