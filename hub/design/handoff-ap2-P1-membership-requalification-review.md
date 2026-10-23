# P1 membership requalification review

Result: **PASS**, bounded to the assembled direct Agent provider/service slice.

- candidateSHA: `52e9c0ea659123c86d6cbadc94f78ef972d74308`
- providerSHA: `e6f7167d6171638f0bfcd5b9f88ae04f05b7b64c`
- donorSHA: `d8e1578bd9f717eb975addb50c2654de70815475`
- packet integrity: 15/15 fixture/test blobs byte-identical to donor; 0 mismatches.
- product integrity: 0 non-imported product diffs from provider; only the three permitted test/fixture imports are present.
- assertion integrity: no skip/xfail/fails weakening markers; imported tests are exact donor blobs.
- changed behavior: ordered membership removal returns `selection_changed`; stale same-field remains `value_conflict`; refusal leaves head and history-entry count unchanged. Trim, params absent/null/remove, shared aliases, opaque preservation, order, inverse, and reload/round-trip cases remain asserted and pass.

## Commands and logs

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime /home/user/work/venv-app2-native/bin/python -m pytest -q tests/sdk/test_p1_doc_patch_provider.py tests/sdk/test_p1_doc_patch_requests.py tests/sdk/test_p1_case_corpus.py
```

Result: `42 passed, 1 warning in 5.27s`, exit 0.
Log: `/tmp/ap2-P1-membership-requalification-review-pytest.log`

```text
/root/.local/bin/ruff check tests/sdk/test_p1_doc_patch_provider.py tests/sdk/test_p1_doc_patch_requests.py
```

Result: passed, exit 0. Log: `/tmp/ap2-P1-membership-requalification-review-ruff.log`

```text
/root/.local/bin/mypy --follow-imports=silent tests/sdk/test_p1_doc_patch_provider.py tests/sdk/test_p1_doc_patch_requests.py
```

Result: passed, exit 0. Log: `/tmp/ap2-P1-membership-requalification-review-mypy.log`

```text
git diff --check
```

Result: passed, exit 0. Log: `/tmp/ap2-P1-membership-requalification-review-diff-check.log`

The disjoint acceptance is still `rebased` under the old detached Runtime fixture; this is a remaining required-v2-merged gap, not historical exact-retry proof or H3 evidence. The real mounted App+Runtime+Agent chain remains unexecuted. No full, browser, heavy, or socket suite ran. Agent-owned R1 landing/review remains outside this bounded proof.
