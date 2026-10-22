# Handoff: AP2 P1 doc.patch request vectors fixed

The P1 request-vector correction is complete on the worker branch. The fixture
set is still collection-only and provider execution remains pending; this is
not an H3 GO or provider proof.

The validator now enforces the contract's exact absent/present tagged forms and
finite raw JSON recursively, with negative checks for malformed tags and
nested nonfinite/overflow numbers. Authored and derived witnesses are checked
against real canonical input/output fragments for trim, created collections,
parameter states, opaque/sibling preservation, and disjoint head/rebased
scenarios. The list read and derived refusal witnesses use the real collection
input. Same-field and list refusal heads are explicitly marked
`constructed-unexecuted on real base`, not attributed to an original corpus
test that did not construct them.

The same-field conflict detail is `value_conflict`; no `field_changed` claim
remains. C0c's addressing principle is adopted for correctness review, while
formal C0c approval remains pending. No provider status is treated as proof.

Required targeted evidence:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime /home/user/work/venv-app2-native/bin/python -m pytest -q tests/sdk/test_p1_doc_patch_requests.py tests/sdk/test_p1_case_corpus.py
25 passed, 1 warning in 4.51s

/root/.local/bin/ruff check tests/sdk/test_p1_doc_patch_requests.py
All checks passed!

/root/.local/bin/mypy --follow-imports=silent tests/sdk/test_p1_doc_patch_requests.py
Success: no issues found in 1 source file

git diff --check
clean (no output)
```

The root accidental `report.md` was deleted. No full/browser/socket/heavy run
was requested or performed.

