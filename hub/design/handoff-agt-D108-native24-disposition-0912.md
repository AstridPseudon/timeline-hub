# F-D108 native-batch24 disposition reconciliation

Verdict: `PARTIAL_EXISTING_DISPOSITION`; 24/24 actual2016 failed native-batch selectors are the exact unique D87 legacy-only selector set. Two rows retain the existing effective D87 disposition; 22 remain `CORE-OPEN`. This does not declare a new retirement, alter the board/classifier, or change any product/test file.

## Exact accounting

- Actual2016 XML contains 40 native-batch nodes: 16 passed and 24 failed.
- The 24 failed nodes partition exactly to the 24 D87 retained selectors, with no duplicate or missing selector.
- Actual failure shape is 22 `SystemExit: 2`, one parser assertion failure, and one `DID NOT RAISE` failure. The removed CLI/native label was not used as a blanket classification.
- Safe cohort A is 184 nodes: 43 `ENV-KNOWN-GAP` and 141 `NEW-OURS CORE-OPEN`; all 24 native-batch rows are in the latter set. Historical D85/D87 550 and prior 276 accounting remain historical. D95's two rows remain separate and are not recounted here.

Rows 16 and 17 (`late-invalid` and `media`) have the exact D87 purpose represented by the unchanged current NativeSheet refusal selector, whose three actual2016 parameter outcomes passed. Its current source hash equals the independently reviewed source hash. They therefore retain `QUALIFIED_EXISTING_LEGACY_ONLY`.

The other 22 rows do not have complete exact replacement proof. The current document-commit replacements error during setup at `tests/packs/timeline/test_cli_document_commit.py:34` with `timeline commit provider interface/contract mismatch`; the current native-checkout replacements error at `astrid/sdk/timeline/validation.py:650` with `candidate.timing: legacy word anchor is missing`. A passing companion selector cannot close a row whose mapped purpose also requires an unproven replacement. Those rows stay `CORE-OPEN`.

## Owner trace

The document replacement path is the unchanged registered `commitTimeline`/provider caller through `RuntimeService.commit_timeline`; the smallest named owner for its setup mismatch is `Runtime — commitTimeline provider / M1 outbox-restart`. The checkout replacement path reaches `validate_final_candidate -> validate_candidate_timing -> legacy_binding`; the smallest named owner for the missing-anchor mismatch is `Agent — F09 native-word-binding / R1-R2 provider`. These are unresolved ownership routes, not new approvals or repair instructions.

The row-by-row exact selectors, actual failure hashes, D87 citations, replacement outcomes, dispositions, and owners are in the companion [JSON](handoff-agt-D108-native24-disposition-0912.json) and [TSV](handoff-agt-D108-native24-disposition-0912.tsv).

## Source and approval custody

- Actual Agent: `070dfc5ef4f3dc35062fcb36a50cb571cd77fbd2`, tree `6056414359ae9fce08d999d54cbecf719fda33c3`.
- Actual XML SHA-256: `72872c77087719a692bff4b48b8d85ea62b9931d59a502c8e246daee0c81c18a`.
- Safe cohort A184 JSON SHA-256: `a215867211faac47f03242d17ec50c3f5ac0d50921a2fdb220af570ef736e77f`.
- D87 manifest SHA-256: `e128e2def01c11ec11ba21455ad6bb0ff79d68913bbdb61434d4eab0ca38fd0b`; D87 appendix SHA-256: `ffb22fae000f94992157ebee3c0d4756d53d5a6c86674e91b771dcde647c681b`.
- Independent review `rt-D87-coverage-review-0033` SHA-256: `a8153ca32f23d50473fbe8a02cf7fa0b722bdae4dd322fd8ad3affa8bca663dd`, reviewed Agent `0d142f79518ba4ec20eb195657ccc7eb6e903fc3`.
- Current 070dfc exact source hashes and reviewed 0d142f source hashes are recorded in the JSON. Native-batch and NativeSheet hashes match; document-commit and native-checkout replacement hashes do not.

## Checks

- JSON parse and row/source-hash readback: PASS.
- TSV header/row cardinality and unique-selector partition: PASS (24 data rows; 24 unique selectors).
- In-memory `ast.parse` and `compile()` of the five actual source files: PASS.
- `git diff --check` in the assigned Composition worktree: PASS; no worktree files were changed.
- Product tests, type checks, lint, services, and full suites: not run; scope is read-only evidence reconciliation.
