# F-D86 numeric6 protected source review

Verdict: `PASS_SOURCE`

Candidate: `9c08deda0e4ffb6d3632d87ef255e13870d71791`

Exact parent: `657bc2e8dba066df1c7d21851315bdb6b0f16a3a`

Candidate file blob: `7526ef8da7527d66181c0c97275c32c47927f3a1`

Parent file blob: `572955522fea53237863e5d1fef68d7b1f24c5ef`

Changed-path check: candidate-to-parent contains exactly
`tests/editing_conformance/test_commit_runtime_numeric_move.py`.

`tests/editing_conformance/test_commit_runtime_numeric_params.py` is unchanged
(candidate and parent blob: `1dbc32cc5de5a1d17b6ddf572bc213a7ad0e5683`).

## Exact source/provenance findings

- The candidate removes only the unsupported `capture_clip_set` baseline setup.
  It deep-copies the opened bundle, mutates the selected entity with the same
  authored values, and calls `emit_document_commands(bundle, candidate)`.
- The submitted request still carries the exact base revision/publication
  pair, command envelopes, label, atomic merge, source/rationale/group_id,
  idempotency key, dry-run false, and one step. For emitted `doc.patch`
  commands, the candidate now flattens the actual emitted changes into the
  step patch, satisfying the provider's exact doc.patch step-claim check.
- The real call trace is preserved: emitter -> `case.submit` ->
  `RuntimeService.commit_timeline` -> Runtime coordinator/`RequestCommitPort`
  -> the startup-validated `load_timeline_commit_provider('astrid')` provider
  -> `RuntimeCommitService.commit` -> command validation/execution -> port
  accept. Registration remains the single existing registration.
- `emit_document_commands` uses canonical JSON comparison, tagged `before`
  values, and deep copies; this keeps `0` versus `0.0`, `1` versus `1.0`,
  `None`, and `False` distinct in the emitted authored image. It refuses
  closure membership/provenance and managed-edge changes, so the candidate
  cannot fabricate a source pin or history boundary. The unchanged assertions
  still require exact current and prior documents, exact media dependency
  manifest, and the selected history write.
- `reads: []` is an explicit C0 request/step declaration already present in the
  parent and is not used to disable capture: emitted changes carry their own
  previous-value guards and the request remains `merge: atomic`. The native
  move continues through unchanged `capture_move`, including its move intent,
  selected identity, reads, bindings, and guards. Publisher remains the real
  test actor passed to Runtime (`author`); no fake provider/publisher route was
  introduced.

## AST and predicate mapping

In-memory `ast.parse`/`compile` passed for parent and candidate. The one
parameterized test retains the exact decorators and six Cartesian inputs:

1. parent, `start=0`, `on=0`
2. parent, `start=0.0`, `on=0`
3. parent, `start=0`, `on=1`
4. occurrence, `start=0`, `on=0`
5. occurrence, `start=0.0`, `on=0`
6. occurrence, `start=0`, `on=1`

All five `assert` ASTs in the original test function are exact-equal in the
candidate. The selected refs are unchanged:
`parent/clip:music-bed` and `occurrence:occurrence-1/clip:clip-1`.
The authored baseline values remain `at=start`, occurrence `hold=0.25`, and
the complete opaque app topology
`app.astrid.fixed_start=True`, `app.astrid.for=hold`,
`app.org.example/opaque=[None, False, 1, 1.0]`. The move remains the original
`capture_move(bundle, ref, on)` call. No refusal, retry, inverse, ABA, or
no-write predicate was removed or weakened (this file contains the six
numeric-image cases only; the separately live three numeric-parameter
inversecoverage failures are not changed).

## Static qualification evidence

- `/home/user/work/venv-agent/bin/python -m ruff check tests/editing_conformance/test_commit_runtime_numeric_move.py`
  (parent source): PASS, `All checks passed!`
- Candidate source piped to Ruff with the target filename: PASS, `All checks passed!`
- `/home/user/work/venv-agent/bin/python -m mypy tests/editing_conformance/test_commit_runtime_numeric_move.py`
  (parent source): PASS, `Success: no issues found in 1 source file`.
  Candidate in-memory compile passed; candidate mypy was not run from a copied
  source file because this review forbids source/scratch copies outside the
  assigned evidence/tmp paths.
- `git diff --check 657bc2e8dba066df1c7d21851315bdb6b0f16a3a 9c08deda0e4ffb6d3632d87ef255e13870d71791`: PASS.
- No pytest, collection, fixture/helper/function execution, service, probe,
  browser, render, package install, or full suite was run.

## Proposed exact D72 setup log entry

> **D72(2), F-D86 numeric6 setup migration (independent source review 0330): PASS_SOURCE.** Candidate `9c08deda0e4ffb6d3632d87ef255e13870d71791` (exact parent `657bc2e8dba066df1c7d21851315bdb6b0f16a3a`) changes only `tests/editing_conformance/test_commit_runtime_numeric_move.py`: replaces unsupported `capture_clip_set` baseline setup with the real guarded `emit_document_commands` path and supplies the exact emitted `doc.patch` changes as the step patch. The original six numeric inputs, exact int/float/null/bool opaque values, selected parent/occurrence identities, source pin/history/media predicates, move intent, guards, and all five original assertions remain exact; the single registered `astrid` provider and `commitTimeline` route remain intact. `numeric_params.py` is unchanged; its three inversecoverage failures remain separately live. This is source-qualified only; the meaningful MAIN6 behavior proof is still owed.
