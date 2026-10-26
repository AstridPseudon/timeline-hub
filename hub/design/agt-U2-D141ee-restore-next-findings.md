# Findings

- The bound writer15 manifest and both terminal dependency manifests were read. Inverse38 classified all 38 IDs as class(c); schema8 classified 2 installer IDs as class(c), 6 rendering IDs as class(a), and no IDs as owner-approved retirement.
- All restored writer15 and schema8 selected function ASTs match the pristine source. `tests/timeline/test_inverses.py` is byte-identical to the pristine file SHA.
- No product source was changed. Missing/retired old routes were not recreated.
- The exact writer15 targeted run executed 15 tests before the final import-preservation adjustment; all 15 failed with real current behavior. The final combined selector command is blocked at collection by the exact old `promote_approved_authoring_candidate` import, which is absent from current production. A final 13-node non-authoring run also executed and all 13 failed.
- Inverse targeted collection fails with `ModuleNotFoundError: astrid.core.timeline.inverses`; restoring that product module was explicitly outside this task.
- Installer targeted tests execute and both fail against current canonical-schema staging and artifact pins.
- Ruff reports only two issues in the exact pristine inverse file (`I001` import formatting and unused `InverseRequest`); changing them would violate byte/source conservation. `git diff --check` passes.
