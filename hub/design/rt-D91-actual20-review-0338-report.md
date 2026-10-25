## F-D91 source review

PASS_SOURCE:
- Candidate `1f975859ba` changes only the allowed fixture.
- Canonical staged closure/provenance preservation avoids emitter guard `emitter.py:267`.
- Original five test bodies, selectors, assertions, raises, parameters, and opaque/shared identity checks are unchanged; static count is 10 parameterized cases.
- No product, SQL, history, writer, or generated-file changes.

FAIL_SOURCE:
- `authoring_bundle.py:400-401` removes `occurrences` from `parent`; timings live separately in `placements` (`:528`).
- Candidate copies only `parent` at fixture lines 63–67 and 111–116, not `placements`.
- Therefore the approved `occurrence-3` duration `2000` and authored placement timing edits are omitted before `emit_document_commands`; the intended timing setup is not preserved.

No functional PASS claimed. Reviewer did not modify source. Follow-up should preserve staged base/provenance while explicitly carrying the intended placement changes.

Checks:

- In-memory compile/AST: PASS.
- Mypy baseline and candidate: PASS, no issues.
- Scoped Ruff baseline and candidate: same pre-existing `I001` import-order finding; no candidate regression.
- `git diff --check`: PASS.
- Pytest, collection, fixtures, Runtime service, browser, and full suites were not run per instructions.

`DONE` and the required commit message were created.