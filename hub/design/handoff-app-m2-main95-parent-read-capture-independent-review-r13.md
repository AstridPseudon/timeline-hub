# HANDOFF — App Main95 capture parity (r13)

Decision: APPROVE exact mirror `bca02baa3c3e43d39f17e149ced8f0422072fed4`.
Fixture: `src/tools/video-editor/commands/fixtures/recipe_m2_app_bootstrap.json`.
Agent source: `6efc81500a0e0688c2bb41e736503f0fc3e04abb`.
App source: `src/tools/video-editor/commands/bootstrapCapture.ts`; first read is `parent / []` present/pristine.
Saved Runtime95 `request.json` + `response.json` reproduce old 409 `capture_mismatch`.
Old request has 4 init reads; `actual-authoritative.json` has the same 4 after removing its first whole-parent read; no semantic diffs remain.
App command/record/bundle parity control: 20 passed; exact parsed values and ordering of reads/records match the Agent fixture.
Independent frozen-Agent parity: 8 passed, 4 failed; same four r12 failures, unchanged/preexisting:
`bootstrap_parity.py::test_inverse_preserves_unrelated_opaque_parent_fields[None]`
`bootstrap_parity.py::test_inverse_preserves_unrelated_opaque_parent_fields[False]`
`bootstrap_parity.py::test_inverse_preserves_unrelated_opaque_parent_fields[value2]`
`bootstrap_parity.py::test_inverse_preserves_unrelated_opaque_parent_fields[value3]`
All fail at frozen Agent `inverse.py:364` (`inverse_dependency_changed`); do not make adoption prerequisites without a pristine-bootstrap counterexample.
No live replay; adoption remains unqualified. Raw JSON stringify differs only by object-key insertion order, not parsed command/record values.
