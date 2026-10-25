# PASS — scalar fixture migration

Scope: `tests/editing_conformance/test_commit_runtime_clip_scalar_fields.py`

Candidate: `fa81e23749d7a7c58a386dc0ce11ce058d359047`, parent
`f2def38890237646943fdad185d0b21d1d7f9938`; the cumulative diff is only the
original scalar migration plus the first-return correction. The author-only
candidate file SHA-256 is
`3ff8e7792e2f9ba3e4b052f431bbea28cbea8d4bd3daf2250a87ea4e3ec707ee`.

The prior protected failure is repaired at line 36 with the genuine call:
`value_at(Closure(bundle).payload(physical), physical, path)`. `physical` is
obtained from `Closure(bundle).resolve(ref)`, so the root, physical image,
reference, and path agree with `_doc_patch.value_at(root, ref, path)`; this is
not an arity-only adjustment. The current seed registers the commit provider,
uses bootstrap state and registered occurrence/track captures, and submits a
full C0 request envelope. The original scalar/compound/separate parameter,
null/bool/numeric inputs, opaque values, assertions, raises, branches,
decorator, and test topology are retained. No retired publisher, synthetic
history, SQL, or guard bypass was introduced.

Checks:

- In-memory compile: baseline and candidate PASS.
- Ruff: baseline and candidate PASS; `git diff --check` PASS.
- Default mypy baseline and candidate both exit 2 on the identical installed
  NumPy stub Python-version diagnostic (`numpy/__init__.pyi:737`); this remains
  an explicit environment result, not a green source result.
- `mypy --python-version 3.13 --follow-imports=silent`: baseline and candidate
  PASS (`Success: no issues found in 1 source file`).
- No pytest, collection, fixture/helper execution, service, build, browser,
  render, probe, or full suite was run.

Merge receipt: requested only for original author worker
`agt-F-scalar-first-return-0100`; queue receipt says
`merged tl/agt-F-scalar-first-return-0100 into agent tl/integration ->
219b9ca8b196bcf4ee6fda6e08c2e50ae251ae4b`. The merged integration head
contains the author commit and its scalar file SHA-256 is the same
`3ff8e7792e2f9ba3e4b052f431bbea28cbea8d4bd3daf2250a87ea4e3ec707ee`.

Functional qualification remains deferred to the later incremental MAIN batch.
