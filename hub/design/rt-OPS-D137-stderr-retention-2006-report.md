## D137 report

Implemented:

- Retained each stage’s original stderr at `.provision-stderr/<stage>.stderr`, mode `0600`, preserving exit status and stage attribution.
- Added failure and timeout tests; public output remains bounded and payload-free.
- Imported reviewed CAS installer preparation and replaced stale E2E-PASS gating with explicit D137 `WITHDRAWN`/`NOTRUN` decision input.
- Preserved `STORE_PY`, `STORE_VERIFY`, protected helpers, CAS/no-follow/no-clobber/RECORD checks.
- Updated manifests, validation, and evidence files.

Final maker: `7a065c078972d9fe91041bcd895ec8be151a034ef66539fed59aa884950119f8`, 70,119 bytes, `0755`.

Tests:

- `bash -n ...` — PASS
- Runtime unittest discovery — 42/42 PASS
- CAS dry-run — PASS
- `/home/user/work/venv-agent/bin/ruff check --no-cache` — PASS
- Python compile — PASS
- Embedded verifier byte comparison — PASS
- `git diff --check` — PASS

No fixture body, Store, child request, acquisition, production request, or install was run. E2E remains `NOTRUN`; acceptance remains `UNVERIFIED`.

The final Git commit/tree is not yet materialized because the harness commits on exit; base commit is `09ed4999741b822fba7e8b3033ca28db6bcf8fa1`. Independent review and the later real CAS install remain next steps.