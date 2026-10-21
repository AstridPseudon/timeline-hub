# RT03 private raw-capture custody review

**Decision: APPROVE the bounded Runtime carrier at committed source
`f53bf588bf70b090ce8e0bed5ccb7d91157771b6`, tree
`d82f37052847949e77c12e1704c3f27c6dd56a46`, against base
`95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`, for the exact Agent-ACKed
internal raw-media capture seam.** This is a custody/source approval only. It
does not qualify Agent's `timeline.reference` command, the original strict
timeline-reference positive, public adoption, or any placement behavior.

## Reviewed source

The committed diff contains only:

- `runtime_protocol/timeline_commit.py`
- `runtime_protocol/timeline_commit_port.py`
- `tests/test_timeline_raw_capture.py`

No contract schema, OpenAPI/generated client, artifact, table, endpoint, or
other product file changed. `contract/artifacts.json` remains 76 entries and
has the same SHA-256 on base and candidate:
`a902387c6a2315374f7e73511feea47da30191aba831b48820b3864b773a532d`.

## Custody findings

- `RequestCommitPort.raw_media_info` requires the exact existing
  `MediaManifestEntry` shape (`media_id`, `content_digest`), canonical
  `sha256:` identity, equal content digest, and membership in the recursively
  declared command objects. It has no fallback to caller metadata, public
  object reads, catalog lookup, `media_info`, or `selected_media`.
- `MediaReads.raw_media_info` joins `objects` to this request project’s
  `project_objects(relation='managed')` row, then reads the CAS object through
  one opened descriptor. The existing descriptor verifier checks regular-file
  identity, expected size, full SHA-256, and stable file identity/timestamps;
  the returned descriptor contains only the stored object identity, MIME, and
  size.
- The descriptor is memoized only in the request. During
  `TimelineCommitStore.accept`, the ledger replay lookup remains first. For a
  new request, the existing acceptance transaction calls `_validate` before
  `_persist_closure`, publication, projection, or `inputs.persist`; `_validate`
  re-runs every captured raw read, checks the exact pin is in the candidate
  manifest, and checks the captured object identity/result. Only captured raw
  media is added to the existing authorized-media set, so unrelated manifest
  media remains refused.
- Existing `media_info` base-closure behavior and five-field `selected_media`
  behavior are unchanged. The old direct reference route and original strict
  positive remain separate controls.

The six new focused tests cover an owned raw object from an empty parent with
no occurrences/clips/references, missing/unowned/foreign refusal with no
SQLite changes, CAS tamper detection during acceptance with no writes, and
exact retry after restart with ledger replay before a raw read.

## Evidence

Independent run against an archive of the exact committed tree, using the
shared Runtime venv:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$tmp" /home/user/work/venv-runtime/bin/python -m pytest -q -p no:cacheprovider --timeout=60 "$tmp/tests/test_timeline_raw_capture.py" "$tmp/tests/test_timeline_commit_port.py" "$tmp/tests/test_timeline_media_selection.py" "$tmp/tests/test_timeline_commit_acceptance.py"
113 passed, 1 deselected in 10.73s
```

The producer's direct candidate-tree runs also passed: raw-capture `6
passed`, port/media-selection `48 passed`, acceptance `59 passed, 1
deselected`, `scripts/artifact_manifest.py --check` reported
`contract/artifacts.json is current`, and `git diff --check` passed.

No full, browser, renderer, live-socket, integration, generated-client,
schema-generation, pin, release, or public-adoption suite was run. The
interrupted predecessor's WIP worktree was preserved and was not used as the
review target.

## Next step

Runtime/Agent managers may perform their separate reciprocal source handoff
and later qualify the Agent command. Keep the original strict positive and
its unsafe-object negative unchanged; do not relabel this bounded carrier as
the completed film-reference workflow.
