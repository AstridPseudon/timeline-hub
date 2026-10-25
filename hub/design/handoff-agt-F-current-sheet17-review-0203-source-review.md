# F-D86 protected source review

Verdict: PASS_SOURCE

Candidate: `64166f709dd86cf4998d5c66dedf305f1989d867`
Parent: `b0ac6891b22f57b2f9744832563556ad5a7cca05`
Assigned file: `tests/editing_conformance/test_native_sheet_current_runtime.py`

## Custody and hashes

- `HEAD` equals `tl/agt-F-current-sheet17-actual-0157` and
  `hub/tl/agt-F-current-sheet17-actual-0157`.
- Candidate file SHA-256:
  `f8b994ff51c972e1fad821f61713ad9010866505e237c07357f71e8daea5e6fc`.
- Protected 6cfb file SHA-256:
  `6e8b187f8a3bcef57056462974002e7bf27f9d5c04d98e278cbbbfee9c632d8d`.
- True original file SHA-256:
  `2dd71d0be3d2f455427de6f96f8926a9d0095d2dd244a5426e9367a598e697c4`.
- Diff protected 6cfb to candidate SHA-256:
  `5096304919e4318d98e2ecb3036081bddb49ae888b5d673f798543ddf7ccc704`.
- The candidate commit changes only the assigned test file.

## Source conservation

- The 10 original test function ASTs are byte-for-byte equal by normalized
  `ast.dump` to both the true original and protected 6cfb source, including
  decorators, parameters, parameter values, assertions, raises, and branches.
- The assigned 17 cases remain: 4 non-parameterized cases, 3 label frontend
  cases, 3 rational frontend cases, 3 connected-occurrence frontend cases,
  and 4 semantic-batch frontend cases.
- The current correction changes only the detached authoring baseline at line
  173, replacing the derived parent `occurrences` field with its placements /
  source mapping representation. It does not remove or edit Runtime physical
  occurrence rows.
- The source bootstrap at lines 302-310 uses the schema-required App defaults:
  resolution `1280x720`, integer fps `30`, `output.mp4`, and null background
  fields. The later authoring candidate still starts from the fixture's exact
  parent payload, including its authored `{'fps': 30}` representation.
- The destination emitter at lines 383-392 starts from the exact authenticated
  Runtime parent, overlays only non-`occurrences` authored fields, and retains
  the full occurrence edges, child closure, source mappings, and provenance.

## Static checks

Commands run against original, protected, and candidate source:

- In-memory `ast.parse` plus `compile(..., 'exec')`: PASS for all three.
- Scoped Ruff with the repository `pyproject.toml` and `--no-cache`: PASS for
  original, protected, and candidate.
- Scoped mypy with `--follow-imports=skip --ignore-missing-imports
  --no-incremental` and private caches: PASS for original, protected, and
  candidate (`Success: no issues found in 1 source file`).
- `git diff --check efa0504f352e7c90149e8a9094d7b5400fc1d81e HEAD --
  tests/editing_conformance/test_native_sheet_current_runtime.py`: PASS.

No pytest, collection, helper/function/fixture execution, service, build,
browser, render, or probe was run.

Inverse effect coverage and the three retired CLI scope findings remain open;
this source review grants no behavioral closure or retirement. Functional
qualification remains a separate MAIN proof for the assigned selectors.
