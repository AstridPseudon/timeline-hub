# Runtime selected-media CAS integrity final review

## Decision

**APPROVE `3021a5b79102e9c0873f70df46f5a686bd1276ff`** for the selected-media
CAS integrity fix, subject to preserving the current integration catalog-head
fence during merge. Reviewed tree: `521fb1dc9aa9e4094e0f901aa3961a1f9db0d471`.

This is an approval of the two-file candidate change (`runtime_protocol/
timeline_commit_port.py` and the native replacement tests), not permission to
replace newer integration code with the candidate's older base. `81f8c7e0b22c34804015c054762af3d737e4698a`
is not an ancestor of the candidate. Its newer catalog-head fence must survive
the future merge; specifically, do not resolve `timeline_commit_store.py` by
taking the candidate side where that would discard the current shot/catalog
head comparison.

## Source findings

- `RequestCommitPort.selected_media()` captures through `MediaReads.selected()`.
  `_selected_project_media()` keeps the existing project, generation/variant,
  managed-association, intrinsic metadata, and catalog-digest checks, then calls
  the existing `RuntimeService._verify_child_object_bytes()` for the exact
  catalog object before returning the catalog digest.
- `RequestCommitPort.validate()` re-reads only the request-private consumed
  selection map. Therefore each unique consumed selection is checked again at
  acceptance; no unrelated film media is walked or rehashed. The verifier is
  streamed in existing 1 MiB chunks, checks exact size and SHA-256, and checks
  regular-file/device/inode stability. `mtime_ns`/`ctime_ns` are race signals
  after the byte hash, not cached authority; bytes and the catalog size/digest
  remain authoritative. No decoder, whole-film hash, DTO, endpoint, table,
  field, or journal was added.
- `CommitExecutionCoordinator.execute()` performs the durable exact-ledger
  lookup before constructing the request port. `TimelineCommitStore._lookup()`
  validates the accepted prefix and returns the stored envelope. Thus an exact
  accepted retry remains ledger-first even if a consumed CAS object is corrupted
  later; it does not re-run capture or acceptance rechecks.
- The fix does not alter the existing project/catalog/attempt authority checks,
  acceptance closure checks, or acceptance persistence ordering. Corruption is
  treated as a local CAS integrity/corrupt-state refusal, not as a normal API
  security claim.

## Native fixture and mutation review

The native fixture creates distinct real managed `old` and `new` media objects;
the occurrence clip initially consumes `old`, while the swap selects `new`.
The same-size old-object bit flip proves the original D04 tampered-source
refusal. The capture-to-accept race corrupts the selected new object only after
the first verification, proving the acceptance recheck. The race test asserts
unchanged SQL dump, timeline head, and command-idempotency receipt rows; the
corrupted CAS bytes remain unchanged (no CAS repair/write). The pre-capture
tamper test asserts the same SQL no-mutation boundary, and the exact accepted
retry test succeeds after later old-object corruption. Existing legacy direct-
writer xfails remain; no new xfail or skipped coverage was introduced.

## Test evidence

Central decisive public HTTP node (socket-capable service):

```text
env ASTRID_CHECKOUT=/home/user/work/agent \
PYTHONPATH=$PWD:/home/user/work/agent \
/home/user/work/venv-agent/bin/python -m pytest -q -n 3 -m integration \
tests/test_timeline_clip_replacement.py::test_native_clip_swap_public_http_route
1 passed in 4.90s
runtime tree: 521fb1dc9aa9e4094e0f901aa3961a1f9db0d471
```

The current `/home/user/work/agent` checkout did not contain the native source,
so the test's existing fallback used the prepared private ordinary Agent source
(the frozen/private pair path), not a published pin.

Direct native CAS controls, local:

```text
... pytest -q -p no:cacheprovider --runxfail -m integration \
tests/test_timeline_clip_replacement.py::test_native_clip_swap_rejects_tampered_cas_without_mutation \
tests/test_timeline_clip_replacement.py::test_native_clip_swap_rejects_selected_source_corruption_between_capture_and_accept \
tests/test_timeline_clip_replacement.py::test_native_clip_swap_is_atomic_cas_and_exactly_replayable
3 passed in 6.87s
```

Focused host lane, local:

```text
pytest -q -p no:cacheprovider \
tests/test_timeline_clip_replacement.py tests/test_timeline_media_selection.py \
tests/test_timeline_commit_closure_invariants.py tests/test_timeline_commit_port.py
59 passed, 9 xfailed, 12 deselected, 1 failed
```

The one failure was the retired legacy HTTP test attempting to bind a socket in
the sandbox (`PermissionError: [Errno 1] Operation not permitted`). It is not
evidence against this change; the corresponding native public HTTP replacement
passed centrally. No full, broad, matrix, renderer, or live suite was run.

## Limits and merge note

The central HTTP evidence is the current public-media positive path; no
HTTP-level tampered-CAS mutation case was added or run. The native corruption
controls are direct Runtime integration tests. The old retired endpoint's ten
markers remain until consumer replacement, as required. Future integration
must retain the `81f8c7e` catalog-head fence and rerun the focused lane after
merging this candidate.
