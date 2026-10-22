# P1 doc.patch request vectors

## Result

Collected eight contract-shaped `doc.patch` request vectors in
`tests/sdk/fixtures/p1_feasibility/doc_patch_requests.json` and added fixture-only
validation in `tests/sdk/test_p1_doc_patch_requests.py`. Existing corpus fixtures
and tests are unchanged.

The set is sourced from the merged Agent corpus at `3f1ceaed` (`tl/integration`,
including collection commit `250db8c8`):

- parent clip-window operands and compiled effects from `recipe_m2_clip_trim.json`;
- ordered track/clip creation rows and opaque values from `recipe_m2_clip_add.json`;
- absent, explicit-null, and remove transitions from the three scalar parameter fixtures;
- the real occurrence-addressed disjoint field/head edit from `recipe_m2_scalar_disjoint.json`;
- same-field refusal plus membership/order dependency cases using the real parent clip collection.

The trim and ordered-list vectors use the physical `parent` payload root because
the real fixture stores authored `from`/`to` and the ordered `clips` collection
there. The internal child contains compiled `at`/`hold`; it is not guessed as the
authored patch root. The scalar/disjoint vectors retain the existing
`occurrence:o/clip:c` address from the source command records.

## Evidence

Commands run from this worktree:

```text
python3 -m json.tool tests/sdk/fixtures/p1_feasibility/doc_patch_requests.json >/dev/null
JSON_OK

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime /home/user/work/venv-app2-native/bin/python -m pytest -q tests/sdk/test_p1_doc_patch_requests.py
7 passed, 1 warning (pytest config option `timeout` is unknown in this environment)

/root/.local/bin/ruff check --fix tests/sdk/test_p1_doc_patch_requests.py
1 import fix applied; clean afterward
```

Final acceptance commands:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime /home/user/work/venv-app2-native/bin/python -m pytest -q tests/sdk/test_p1_doc_patch_requests.py tests/sdk/test_p1_case_corpus.py
20 passed, 1 warning (pytest config option `timeout` is unknown in this environment)

/root/.local/bin/ruff check tests/sdk/test_p1_doc_patch_requests.py
All checks passed!

/root/.local/bin/mypy --follow-imports=silent tests/sdk/test_p1_doc_patch_requests.py
Success: no issues found in 1 source file

git diff --check
clean (no output)
```

## Current implementation boundary

There is no `doc.patch` operation in the current `astrid.sdk.timeline.commands`
operation registry. Current production execution remains
`astrid.sdk.timeline.commands.execute(bundle, commands, ...)` for registered
semantic/native operations, and Runtime integration is callable as
`astrid.sdk.timeline.commit.RuntimeCommitService.commit(context, port)` (the
existing test harness reaches it through `create_runtime_commit_service().commit`).
No provider execution, Runtime publication, socket, browser, or full-suite run
was attempted.

The corpus has Agent `project_id`/`timeline_id` and revision identities, but no
Runtime `base_publication_id` or idempotency key. The vectors intentionally record
those as missing runtime facts instead of using placeholders. They are operand
sets ready to be placed in a live `commitTimeline` envelope once R1 supplies the
provider and Runtime head.

## Unexecuted provider cases

All eight vectors remain provider-unexecuted: accepted parent field patch,
created-ID list inserts and mirror/allocation validation, absent/null/remove
parameter semantics, disjoint `merged` landing, same-field conflict/refusal,
accepted `list.move`, and collection membership/order `selection_changed`
conflicts. The test file validates guards, provenance, exact deltas, opaque
values, and expected reply fields only; it does not implement a patch executor,
diff engine, or golden.
