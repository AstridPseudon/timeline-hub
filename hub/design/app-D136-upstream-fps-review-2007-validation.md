# D136 validation record

All repository checks below were read-only. No product, fixture, schema,
generated file, upstream ref, or test file was edited.

## Source, Git, and hash checks

- Receiving `HEAD`: `3082cad490ce1cee764ff137f99cb791a67ddd08`;
  tree: `84e9d485a7ee8fdf2969eaf19d159e400f0ca1d4`.
- Worktree status: clean.
- Receiving diff from its parent: exactly
  `tests/sdk/test_timeline_capture_projection.py`.
- `git diff --check HEAD^ HEAD`: PASS.
- Projection SHA-256: `6e41a5bba04666275b9e252d7aeb30247a145207da3f9ed14f06b338563a1436`;
  Git blob: `16954294f9f70018e4bbd1012083f51594f6cb19`.
- Local object checks for supplied upstream tip: PASS. The projection path is
  absent at `886a3183bd4a4a44f0a2c08fabec4e8edcbf7b55`; this does not replace
  the supplied lead freshness evidence.

## AST, schema, and caller checks

- AST parse/count: 11 test functions, 44 current assertions, 43 assertions in
  the parent source. The protected D136 census/map records 43 original
  predicates, 11 test bodies, and 54 fixture statements with conservation true.
- `/usr/bin/python3.11` in-memory `compile()` of the touched projection and
  owning provider/caller modules: PASS for all five files. No bytecode cache was
  written.
- Captured upstream JSON Schema direct validation of a minimal valid timeline
  containing the exact nested FPS shape: 0 errors.
- Captured upstream `_timeline_fps` source extraction: list result `30.0`,
  scalar result `24.0`.
- Receiving source readback: `_fps_values` reaches the authored path and
  `_fps` accepts scalar/exact rational mapping only; the array is refused.
- Caller readback: `publish_authoring_candidate` builds the v2 request and
  calls `writer.commit_timeline`; independent D1001946 evidence records the
  registered RuntimeService route. No bypass or alternate route was credited.

## Ruff

`ruff check --isolated tests/sdk/test_timeline_capture_projection.py` returned
five existing diagnostics. Running the same check against the parent source
returned the identical five diagnostics, so no style change was made.

## Historical test separation

No pytest, service, socket, browser, native, profile, full, or nine-selector
run was performed by this reviewer. The independent D1001946 result remains
the historical source evidence: candidate27 was `27/27 PASS`, while the
authored projection lane was `9 setupERROR` with no body credit. Those results
remain separate and unchanged.

## C0 / holds

C0 §§1-3 and §6 were read for provider validation, closure guards, conflict
semantics, and open-field/meta preservation. D130 remains held. The finding is
handed to Runtime/Agent under D136; no product writer, body, retry, fixture
conversion, guard widening, or release action is proposed here.
