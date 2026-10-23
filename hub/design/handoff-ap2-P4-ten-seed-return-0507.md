# Handoff: ap2-P4-ten-seed-return-0507

## Exact delta

Base: `tl/ap2-P4-ten-stage-0505`, commit
`9b658b28c3a7bc3ebda3ad5a7b5b417d78553720`, tree
`84bd8ef3429c06ced18c0639388be8b2c8ecd030`.

Changed only `tests/editing_conformance/test_p4_ten_note_v2_runtime.py` in
the source tree: `_seed_original` now passes the unchanged shared fixture
through `bundle_from_document` and `compile_authoring_candidate`, seeds the
compiled canonical parent/child closure, and applies the normal Runtime
`registry` default. The ten-note source, assertions, and all other repository
files are unchanged. The resulting source blob is
`8a93768271fc1ca4f48db927c25d70cbbe97a3d9`.

`report.md` records the evidence and exclusions.

## Evidence

- Exact one-test collection: **PASS**, 1 collected.
- Scoped Ruff: **PASS**.
- Private mypy source scope (`commit.py`, `commit_session.py`, `emitter.py`,
  `sync.py`): **PASS**, no issues.
- `git diff --check`: **PASS**.
- Offline compiler/trusted-seed-shape witness: **PASS** for exact authored
  payload fields and canonical compiled closure.

No HTTP, service, socket, browser, full suite, build, or live inverse/redo run
was performed.

## Decision/seam for manager

The normal authoring adapter intentionally virtualizes repeated physical shots
into independent per-placement authoring identities. The original shared
placement assertion remains untouched per task scope; no invented identity
binding or fixture substitution was added. Manager owns the next actual body
run and any decision about that pre-existing authoring-layer seam.
