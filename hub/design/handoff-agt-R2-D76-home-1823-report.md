# R2/G4 D76 actual-home qualification: PASS

## Result

PASS for the exact combined actual-home scope on Agent `37bcba3af65ec583e899c3e8e09168dd5944a23e` (tree `37a80bd09ac3f43dae48ee7ec36994366fe48be6`) with Runtime `327da207ed30880fe2ae0cd0b116722bb2c6f7a6` (tree `0140a9ab2bf8582c4712dbf84498a6d5dcb132cf`). The ten-node run passed `10/10`, with no failures, errors, or skips, in `10.82s`; the only output warning is the existing `record_property`/xunit2 warning.

Ledger credit is intentionally restricted to exactly two named originals:

- `R2-source-retention-original`: `tests/sdk/test_timeline_selected_schema_runtime.py::test_native_retained_schema_replay_inverse_reload_and_exact_retry`.
- `D76-duplicate-original`: `tests/sdk/test_timeline_restructure.py::test_duplicate_of_a_chapter_film_keeps_one_distinct_shot_per_chapter_r4_original`.

The source NEW4 refusal controls and duplicate strict4 controls are guard evidence only and receive no additional ledger credit.

## Exact test command and result

Command was run once with the authentic Agent venv and Runtime checkout:

```text
PYTHONPATH=$PWD:/home/user/work/runtime ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime /home/user/work/venv-agent/bin/pytest -q -oaddopts= -pno:cacheprovider --timeout=45 --junitxml=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-agt-R2-D76-home-1823-qualification.xml tests/sdk/test_element_inverse_source_retention.py::test_inverse_loads_original_object_after_readmission_and_restart tests/sdk/test_element_inverse_source_retention.py::test_inverse_refuses_forged_historical_declaration_without_writes tests/sdk/test_timeline_selected_schema_runtime.py::test_native_retained_schema_replay_inverse_reload_and_exact_retry tests/sdk/test_timeline_restructure.py::test_duplicate_of_a_chapter_film_keeps_one_distinct_shot_per_chapter_r4_original tests/sdk/test_timeline_restructure.py::test_duplicate_of_a_chapter_film_keeps_one_distinct_shot_per_chapter tests/sdk/test_timeline_restructure.py::test_duplicate_guard_refuses_a_copy_that_collapses_shots_and_keeps_a_repeated_shot_repeated tests/sdk/test_timeline_restructure.py::test_duplicate_refuses_when_the_wrong_form_of_the_source_is_copied tests/sdk/test_timeline_restructure.py::test_duplicate_commit_keeps_a_repeated_shot_shared
```

Pytest expanded this to the exact ten XML-derived nodes:

1. source `test_inverse_loads_original_object_after_readmission_and_restart`;
2. source `test_inverse_refuses_forged_historical_declaration_without_writes[wrong-pin]`;
3. source `... [wrong-scope]`;
4. source `... [different-object]`;
5. source `test_native_retained_schema_replay_inverse_reload_and_exact_retry`;
6. duplicate `test_duplicate_of_a_chapter_film_keeps_one_distinct_shot_per_chapter_r4_original`;
7. duplicate `test_duplicate_of_a_chapter_film_keeps_one_distinct_shot_per_chapter`;
8. duplicate `test_duplicate_guard_refuses_a_copy_that_collapses_shots_and_keeps_a_repeated_shot_repeated`;
9. duplicate `test_duplicate_refuses_when_the_wrong_form_of_the_source_is_copied`;
10. duplicate `test_duplicate_commit_keeps_a_repeated_shot_shared`.

Durable evidence is flat in `design/`:

- `handoff-agt-R2-D76-home-1823-qualification.xml`
- `handoff-agt-R2-D76-home-1823-test.log`, `...-test.exit`, `...-command.txt`
- `handoff-agt-R2-D76-home-1823-origins.txt`, `...-hashes.txt`, `...-ast.txt`, `...-diffcheck.log`

## Source and duplicate identity

The source hydration commit `06226186149374f1e2c78c0d17f1cb76cc0bdc51` and duplicate fixture commit `6277434244fd30f6ac3259bd7339b17f7e4f745f` are exact ancestors in the actual integration head. The source test blob is byte-identical to author `062261`; the duplicate test blob is byte-identical to author/review `627743`. The protected retained-schema original assertion AST matches both source parent and source author. The D76 original’s six assertion ASTs match both duplicate review parent and duplicate author.

The D76 original preserves the six reviewed assertions exactly: three stored placements; one flat source shot with structure key; three distinct duplicated shots; `dup-` IDs; ordered `01 ONE`, `02 TWO`, `03 THREE` names; and three distinct occurrence IDs. Its setup is authenticated `saved_source`, `Checkout(flatten(bundle_from_document(document('t'))))`, and the production `td._duplicate(client, project, ...)` caller, with the result read from `physical_content(bundle_from_document(document('dup')))`. No fake media, mocked `Checkout.open`, mocked publish, receipts, skipped assertions, or weakened predicates are involved.

The source original’s production path uses authenticated historical inverse loading and `RequestCommitPort.document_object`; the three source refusal cases assert wrong pin, wrong scope, and different object rejection without writes. The independent source review and duplicate review were read as actual JUnit/provenance artifacts, not prose-only counts.

## ABI and static evidence

No product, test, schema, generated/client, pin, registry, or caller changes were made by this worker. The source independent review records the full v2 request/reply ABI unchanged, including scope/base, commands, label, steps/patches, merge, reads, idempotency, accepted/merged/conflict/invalid/dry-run fields. This worker reused the independent unchanged-source Ruff/mypy/compile/diff evidence from source review `agt-R2-source-review-1819` and duplicate review `rt-D76-duplicate-review-1809`; no dependency installation or full/P4/browser suite was run.

`git diff --check` is clean. The Runtime worktree is clean. Imports resolve from this Agent worktree and `/home/user/work/runtime`; the evidence records the resolved module paths and all relevant blob hashes.

## Ledger and limits

Exactly two rows were appended to the existing shared `design/deletion-ledger.md` after prefix/hash verification: `R2-source-retention-original` and `D76-duplicate-original`. Post-append ledger identity is 156668 bytes, SHA-256 `10e2109afaca434f87cb963860c4d18029a1640ce00c391fb9fa5309eba005c1`, with exactly one occurrence of each new row ID.

Unqualified gaps remain: no P4, full, browser, home29, source-neighbor, PARAM-original, or other retained range/status qualification is claimed. The actual-home PASS is scoped only to the ten named nodes and the two ledger originals above.
