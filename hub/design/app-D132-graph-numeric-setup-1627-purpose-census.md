# D132 purpose census

The shared fixture is `tests/editing_conformance/test_recorded_graph_roots.py`.
Its `root_values()` helper is imported or qualified by:

- `tests/sdk/test_timeline_commit_graph_roots.py` (the registered Runtime provider path)
- `tests/sdk/test_timeline_semantic_reservations.py`
- `tests/sdk/test_timeline_created_root_stage_redo.py`

The graph consumer has 11 test functions, 33 assertions, and 7 parametrization
decorators. Its AST and assertion hashes are unchanged. The fixture itself has
22 test functions, 90 assertions, and 6 parametrization decorators; its
assertion AST is unchanged.

The only authored `gain` field in this fixture is the `occurrence:new-occ`
setup value at lines 46–51. The other `gain` occurrence is a deliberate
tamper (`value['gain'] = 0`) in the inverse-conflict/no-write test, not a null
handling or preservation assertion. No consumer adds a null-gain assertion.

The production route is genuine: `test_timeline_commit_graph_roots.py` builds
the full commit envelope and calls `RuntimeService.commit_timeline` after
registering the `astrid` Agent commit provider. Runtime prepared-candidate
validation applies the public occurrence schema, where `gain` is numeric;
the compiler does not normalize explicit null. Numeric gain `1` is also the
normal value used by the native occurrence producer and the passing video
unplace source case.

The migration therefore changes only an invalid authored setup input. It does
not change compiler, product, schema, provider, assertions, test bodies, or
other fixture inputs.
