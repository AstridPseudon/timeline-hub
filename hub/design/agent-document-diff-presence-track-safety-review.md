# Agent document-diff presence/track safety review

## Verdict

**DO NOT APPROVE** `tl/agt-m2-document-diff-null-presence-track-fix-0607` at
commit `aba0346aec2ea15c80cd9ea2cc850c75081594b8`, tree
`2d3877e082d12c3c08e7d0eca6e9ba55883e2ad8`.

The new sentinel comparison fixes only some paths. The adapter still accepts
real presence changes as a zero-command result.

## Concrete counterexample

Using the existing `tests.timeline.test_authoring_feedback.bundle()` fixture,
I made the exact pinned Runtime child clip contain `params: None`, `from:
None`, or `at: None`; copied the same value into that candidate's
`base_internal_timeline`; then deleted the field from the candidate's live
`internal_timeline`. `document_diff_to_commands(candidate, base)` returned
success with `commands == []` for each case.

This is data loss: the detached document changed explicit `null` to absence,
but no command or refusal records it. The source is:

- `astrid/sdk/timeline/document_diff.py:67-71`: `_params()` normalizes
  `params: None` to `{}`.
- `astrid/sdk/timeline/document_diff.py:196-212`: `_emit_clip_commands()`
  still uses `.get()` for `at`, `from`, and `to`.
- `astrid/sdk/timeline/document_diff.py:401-403`: the internal-timeline
  held-field loop iterates only `set(candidate_internal)`, so deleting an
  existing opaque/extension field is also accepted with zero commands. A
  fixture probe deleting `layout`, `effects`, `audio`, or `opaque_timeline`
  returned success with zero commands.

The Main contract says the internal timeline is a “complete” authored payload
and that ordinary authored edits are lossless
(`astrid/core/timeline/authoring_bundle.py:64-70,101-113`). Main also retains
an explicit null field (`tests/editing_conformance/test_compile_contracts.py:148-151`).
Therefore these are reachable lossless-presence cases, not malformed-input
noise. The fix must compare the union of keys with an explicit missing
sentinel, and either emit a lossless native clear or refuse visibly while
retaining the draft.

## Other review points

- `_changed_keys()` and `_require_explicit_rows()` now distinguish missing from
  explicit `None`; the parent-track rename path captures `track.set` and
  validates the resulting rows. The new direct tests for those paths pass.
- Row membership/order and foreign-row changes are guarded by `_rows()` and
  the exact key-order comparison; no foreign-row acceptance was found.
- Refusal paths operate on a deep-copied working bundle and the added tests
  retain the candidate draft. No draft mutation was found.
- Native capture uses the pinned `base`/working bundle and does not refresh a
  guard from a newer Runtime read. No HTTP, Runtime, browser, native-private,
  or full-suite test was run.
- The existing `_replace_known_payload_media()` normalization is scoped to
  known media mirrors. The separate `_params()` normalization is not safe for
  presence-sensitive data and is part of the blocking finding above.

## Evidence run

- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/timeline/test_authoring_feedback.py -k 'document_view_adapter'`
  — **9 passed, 15 deselected**.
- `... pytest --collect-only ... tests/timeline/test_authoring_feedback.py` —
  **24 tests collected** (the original direct test count retained).
- The immediately preceding committed worker's handoff records the retained
  original evidence as **24 adapter tests passed** and **49 neighboring
  provider tests passed**. I did not rerun that broader provider lane under
  the compact-tests-only instruction.
- The authenticated round-trip worktree
  `/home/user/work/wt/agt-m2-document-diff-authenticated-roundtrip-0614` is
  clean at the same `aba0346...` commit; it has no added normal
  capture/commit/reload test or artifact yet. The existing source path in
  `astrid/packs/rendering/docs/scripts/timeline_document.py:210-299` is
  structurally correct (preflight capture, exact media resolution, then
  `commit_many` with the pinned base), but source inspection is not proof of
  normal authenticated round-trip behavior. Required follow-up: add the
  worker's committed non-HTTP-duplicating normal capture/commit/reload
  artifact, then qualify that artifact separately.

