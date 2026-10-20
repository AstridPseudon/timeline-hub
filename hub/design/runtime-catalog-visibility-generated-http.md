# Runtime generated catalog-visibility test report

Implemented `tests/test_timeline_visibility_generated_http.py` only.

The test reuses the existing restored realm/auth daemon fixture from
`test_timeline_authority_door.py` and the generated `WorkspaceClient`. It
verifies one existing timeline's archive and explicit-current-version recover
operations, exact retries, visible archived/unarchived responses, and a
read-only credential denial with no Runtime database/CAS changes. It compares
the public canonical head, canonical composition document, composition
revision closure listing, and legacy film history before and after the
visibility lifecycle.

No Runtime service, schema, DTO, provider, or existing test files were changed.
The test deliberately does not use the retired timeline-document read or the
provider-dependent canonical commit-history route; this remains a catalog
visibility boundary, not another provider-restore journey. It does not test or
approve legacy receipt provenance behavior.

## Evidence

- `git diff --check` — passed.
- `R=$(.../orch/bin/request-test rt-m2-catalog-visibility-generated-http targeted --files "tests/test_timeline_visibility_generated_http.py") && .../orch/bin/wait-test "$R"` — passed; **1 passed in 1.74s** on final exact tree `e85981f6c348e977e14dfcb379e5d71fbce98a31`.
- A direct local invocation reached the daemon fixture but could not bind a
  socket in the worker sandbox (`PermissionError: Operation not permitted`);
  the central targeted run is the authoritative localhost evidence.
- No full, browser, or broad suite was run or requested.

No blockers remain.
