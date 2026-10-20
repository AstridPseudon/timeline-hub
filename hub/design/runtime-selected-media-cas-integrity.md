# Runtime selected-media CAS integrity

## Seam and source

The fix is in `runtime_protocol/timeline_commit_port.py`:

- `MediaReads.selected()` / `_selected_project_media()` now calls the existing
  `RuntimeService._verify_child_object_bytes()` helper for the selected managed
  object, after catalog metadata and intrinsic media checks and before the
  catalog digest is returned.
- Native command capture enters through
  `RequestCommitPort.selected_media()` (line 267), which records the verified
  result in the request-private consumed-selection map.
- Acceptance rechecks only that map in `RequestCommitPort.validate()` (line
  398), before `TimelineCommitStore.accept()` begins its persistence work.
- The helper uses descriptor-scoped no-follow CAS opens and
  `_verify_file_at()` / `_verify_open_file()` to require the exact catalog size,
  regular-file identity stability, and SHA-256 digest. No new DTO, endpoint,
  table, field, journal, decoder, scene evaluator, or public API was added.

The exact-ledger lookup remains first: `CommitExecutionCoordinator` and
`TimelineCommitStore._lookup()` resolve an accepted retry before constructing a
port or running selected-media capture/rechecks. Therefore a later CAS
corruption does not prevent an exact accepted retry from recovering its stored
receipt/result.

## Old red / fixed green

The supplied D04 design evidence records the old candidate behavior: a real
selected `old` object was changed in CAS and native `occurrence.swap-media`
accepted it; the original Main tampered-CAS refusal remained strict. The old
native test was therefore a strict xfail and was not retired or weakened.

With this fix, `--runxfail` passed the native refusal and retry controls,
including:

- pre-capture same-size corruption of the selected old source;
- corruption of the selected new source immediately after capture and before
  acceptance, with unchanged SQL rows, timeline head, receipt rows, and no
  acceptance CAS write;
- exact accepted retry after later corruption, followed by fixture restoration;
- valid video replacement, cross-project refusal, malformed import refusal,
  wrong-stream refusal, bounded duration refusals, generic visual stream
  refusal, and intervening-edit/reopen replay.

Direct non-HTTP native integration command:

```text
python -m pytest -q --runxfail -m integration tests/test_timeline_clip_replacement.py -k 'native_clip and not public_http'
9 passed, 13 deselected
```

The central explicit targeted run was:

```text
python -m pytest -q tests/test_timeline_clip_replacement.py tests/test_timeline_media_selection.py tests/test_timeline_commit_closure_invariants.py tests/test_timeline_commit_port.py
59 passed, 12 deselected, 10 xfailed
```

The ten xfails are the existing retired direct-writer markers, including the
original Main tampered-CAS refusal. The new native CAS xfail is absent.

## Cost and bounds

Each consumed selected command input is hashed at capture and once at the
acceptance recheck. Work is `O(sum(selected object bytes))` per pass, with the
existing 1 MiB chunked verifier and no hashing of unrelated film media added by
this patch. Duplicate selections are retained in the existing request-private
map for acceptance, so the recheck remains bounded by the unique consumed
selection identities. Existing closure/manifest checks are unchanged.

`git diff --check` passed. No full suite was requested. The native public HTTP
integration node was not run locally because this sandbox cannot open sockets;
the central targeted run intentionally deselected integration-marked nodes.
