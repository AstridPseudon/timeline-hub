## Report

Implemented the final caller custody repair in:

- `caller-publication.py`
- `caller-dry-preflight.py`
- `caller-custody.json`

The caller now derives and freezes the current clean `tl/integration` tuple:

- App: `0971c645...`, tree `60cdf06f...`
- Agent: `cba425b6...`, tree `d19ce2e5...`
- Runtime: `becfe6db...`, tree `7edc08e3...`

All exact parents, registry/template/body/tail digests, duplicate/concurrency guards, symlink rejection, and both decoded P2/P3 source guards are enforced.

Validation passed:

- Normal and `-O` Python compilation
- JSON validation
- `git diff --check`
- Caller preparation: `PREPARED`, `NOT_GRANTED`, `NOT_RUN`
- P2 source guard: PASS, 0.353s
- P3 source guard: PASS, 0.452s
- Decoded/wrapped `bash -n`
- Wrapped `bash -c` argv/export/failure proof
- 13/13 negative controls refused correctly

No browser, HTTP, child, backend, schema, service, full-suite, or original journey execution was performed. Genuine custody inputs and coordinator admission remain missing; the artifact is intentionally not READY.

Commit message written and `DONE` created.