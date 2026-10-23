# G5 test-import migration review

## Verdict: FAIL (test fidelity)

Reviewed `tl/agt-G5-test-imports-1137/4196a7bc9` against `086db31e4`.
The commit is scoped to the two assigned test files only and removes the two
retired `document_diff` imports in favor of the real G3 emitter. No product
source was changed, and no compatibility alias was added.

The pair collects **49 cases total**: **30 authoring-feedback cases** and
**19 native-sheet Runtime HTTP cases**. The Runtime HTTP body was inspected
but intentionally not executed in this review.

## Blocking finding

`tests/editing_conformance/test_native_sheet_current_runtime.py:279-286`
keeps the original safety assertion that adding undeclared `params["null"]`
must be refused, but now calls `emit_document_commands(before, unsupported)`
and expects `DocumentPatchError`. That is the wrong enforcement boundary for
G3:

- `astrid/sdk/timeline/emitter.py:239-244` describes the emitter as a
  structural adapter; it emits guarded patches and does not validate provider
  parameter schemas.
- `astrid/sdk/timeline/_doc_patch.py:254-267` validates known collection
  identities and parent mirror consistency, not element parameter declarations.
- `astrid/sdk/timeline/_doc_patch.py:296-314` owns the authoritative media
  dependency guard; `astrid/sdk/timeline/commit.py:1139-1156` invokes final
  candidate validation at the provider boundary.

An isolated reproduction using the current emitter fixture, with an `am-type`
clip carrying the existing `text` parameter plus `null`, produced a valid
`doc.patch` and `commands.execute()` also accepted it under the pure executor;
the emitter did not raise. Therefore the preserved Runtime test would fail at
the `with pytest.raises(...)` line when its HTTP setup is executed. The old
`document_diff` refusal was an adapter-level limitation and cannot simply be
retained against the generic emitter. The test must either assert the emitted
patch and separately exercise the authoritative provider refusal if that guard
is still required, or be revised according to the settled C0/G3 contract.

The related media rewrite in
`tests/timeline/test_authoring_feedback.py:180-189` is acceptable only as an
emitter serialization test: it asserts a source-bound `media_id` patch but
does not prove Runtime acceptance or authority. The same fixture's emitted
replacement with `NEW` is rejected by the authoritative executor with
`dependency_changed: patch references media outside Runtime-verified inputs`,
which is the required C0 media guard. Do not treat the serializer-only
positive as proof that this guard was preserved; the unexecuted Runtime body
does not cover it.

The narration rewrite is a valid generic patch case under C0/G3: it asserts
the exact `shot-revision` path and present `before` value. The remaining
presence, null/absence, mirror, pinned-base, source-bound physical-reference,
shared-source, raw-field, canonical/reload/undo, and accepted HTTP body
assertions were preserved or updated to exact `doc.patch` forms.

## Verification

All commands ran in the review worktree at `4196a7bc9`:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --basetemp=/tmp/agt-G5-review-authoring tests/timeline/test_authoring_feedback.py
30 passed in 1.17s

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --basetemp=/tmp/agt-G5-review-emitter tests/editing_conformance/test_document_patch_emitter_engine.py tests/editing_conformance/test_document_patch_emitter_v2.py tests/editing_conformance/test_native_sheet_ordinary.py tests/sdk/test_timeline_sheet_native.py
135 passed in 14.36s

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest --collect-only -q -o addopts= -p no:cacheprovider tests/timeline/test_authoring_feedback.py tests/editing_conformance/test_native_sheet_current_runtime.py
49 collected: 30 authoring-feedback, 19 native-sheet Runtime cases

/home/user/work/venv-agent/bin/ruff check tests/timeline/test_authoring_feedback.py tests/editing_conformance/test_native_sheet_current_runtime.py
All checks passed

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime /home/user/work/venv-agent/bin/python -m mypy tests/timeline/test_authoring_feedback.py tests/editing_conformance/test_native_sheet_current_runtime.py
Success: no issues found in 2 source files

git diff --check 086db31e4 4196a7bc9
passed
```

The target diff names only the two assigned test files. The retired-symbol
audit found no `document_diff`, `DocumentDiffError`, or
`document_diff_to_commands` references in either target file. No HTTP/body,
native14, P1/P4, full, browser, or duplicate suite was run.

## Required next step

Return the draft to the author for a bounded correction of the undeclared-param
assertion/coverage boundary, and add or identify an authoritative-provider
refusal witness if the safety contract requires rejection. Re-run the same
targeted checks and central Runtime HTTP suite before considering G5 review
complete. No product edit or assertion weakening was made here.
