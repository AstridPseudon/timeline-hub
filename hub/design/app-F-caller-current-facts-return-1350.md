## Report

Implemented the current-facts refresh seam across the existing caller/adapter/recipe artifacts.

- Added reproducible `--refresh` generation from current clean integration heads, all parents, interpreter/import origins, Runtime 14/15 mappings, client/schema hashes, and existing Remotion/Composition inputs.
- Removed stale hardcoded App `971a…` readiness gating; it remains only as the verified current App parent.
- Preserved protected template prefixes/suffixes, native and encoded stages, launch/export behavior, and 51/133 wire closures.
- Refreshed `caller-custody.json` with current tuple, counts, commands, and candidate hashes.
- Wrote commit message and `DONE` marker.

Current App tuple: `d24ed69d…`, tree `ead5ba0d…`, parents `971a29e…`, `fe0e040b…`.

Tests/checks passed:

- `python3 current-service-inputs.py --refresh`
- `python3 current-service-inputs.py`
- `python3 working-service-binding-control.py` — adapter controls pass
- `python3 caller-publication.py`
- `python3 -O caller-publication.py`
- Caller negative matrix: stale, wrong source, ref/tree/target/symlink, registry/concurrency, native, protected, encoded, binding, mappings, missing/extra inventory — all refused as expected.
- Python compilation, JSON validation, `git diff --check`

No live service, browser, backend, HTTP, native, or full suite was run. Central integration should run those next.