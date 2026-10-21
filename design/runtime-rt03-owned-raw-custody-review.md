# RT03 owned raw-object custody review

**Decision: conditional ACK of the safety boundary; correction required before a
carrier can be called executable.** The original strict positive remains open:
an owned raw CAS object must create an unplaced `timeline_references` result
with the exact `reference_id`, `object_id`, and `role: "source"`, while the
unsafe unowned-object case remains an independent refusal. Preserve the
changed-payload, restart/retry, and occupied-identity assertions unchanged.

## Existing Runtime seams

There are three relevant pieces on Runtime 95bd:

1. `RuntimeService.ingest` is the existing raw-object admission. In
   `runtime_protocol/service.py:4793-4866`, it verifies the byte digest,
   publishes the CAS object, inserts `objects`, and for a project inserts
   `project_objects` with `relation='managed'`, all behind the existing durable
   `object.ingest` identity. This is the safe ownership fact available for a
   raw object; it is not a generation/variant or catalog reference.

2. `TimelineCommitStore._validate_closure` can structurally carry a new raw
   registry entry without placement. At
   `runtime_protocol/timeline_commit_store.py:518-547`, every manifest media
   pin must be a canonical digest, point to a project-managed object, and
   match the CAS bytes; every `object_id`/`media_id` found recursively in the
   parent, shot, and internal payloads must be in that manifest. It does not
   require an occurrence or clip merely because a registry asset is present.
   `_persist_closure` stores the authored parent payload and its registry at
   `:860-879`; this is the existing registry-birth storage seam, not a separate
   registry-alias API.

3. The commit request port currently prevents those two pieces from forming
   an executable RT03 path. `RequestCommitPort.validate` at
   `runtime_protocol/timeline_commit_port.py:391-415` authorizes manifest media
   only from captured parent/shot closures, `selected_media`, text, or
   narration. Any other manifest object is refused as
   `dependency_unavailable`. `selected_media` at `:835-842` requires the exact
   five-field `MediaSelection`, and its resolver at `:734-755` requires a
   completed generation/variant/object binding. Runtime 95bd has no raw
   two-field `MediaPin` read/capture method in `RuntimeCommitPort` or
   `MediaReads`.

The empty-parent behavior is separately real: `empty_bootstrap_document` in
`runtime_protocol/timeline_commit_baseline.py:416-423` has no media, and
`TimelineCommitStore.bootstrap` at `:1004-1018` accepts that empty closure.
However, a subsequent RT03 commit cannot introduce a newly ingested raw
object through the normal request port merely by putting its digest in the
manifest; the port-level capture gate fails before `_validate_closure` can
accept it.

## Required correction to the proposal

The source-only proposal's requirement that `asset` “must name one
already-existing parent registry asset” is stronger than the original owned
raw-CAS positive and is therefore a mismatch. The witness starts from an
empty parent with an owned raw object, not from visible media or an accepted
registry alias. The proposal must not present that alias precondition as the
smallest safe carrier, and must not use occurrence placement, managed-media
five-tuples, project-catalog roles, or the retired direct reference writer as
substitutes.

The minimum safe correction is to retain the existing raw-ingest ownership
fact and the existing closure media pin/registry-birth storage, but hold the
carrier until the Agent/Runtime owners explicitly authorize an internal
request-scoped raw-pin capture at the commit-port boundary. This review does
not invent that method, DTO, command subshape, endpoint, schema, or registry
alias rule. Without that owner-approved capture seam, the accurate status is
“no executable existing raw owned MediaPin carrier on Runtime 95bd,” not a
qualified positive.

The retired route is not a fallback: current `RuntimeService.create_reference`
at `:4220-4223` immediately requires the timeline-command path, while the
preserved strict test remains `xfail` in
`tests/test_runtime_exact_idempotency.py:81-123`. The old untouched-Main
acceptance of arbitrary `object_id` is the unsafe negative mapping, not a
behavior to restore.

## Bounded evidence

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" \
  /home/user/work/venv-runtime/bin/python -B -m pytest -q -p no:cacheprovider \
  tests/test_timeline_commit_acceptance.py::test_nonmanaged_project_media_relation_cannot_authorize_commit \
  tests/test_timeline_fresh_bootstrap_scope.py::test_fresh_or_empty_scope_bootstraps_and_replays
4 passed in 1.59s
```

No source, artifact, pin, schema, endpoint, or test expectation was changed;
no full, browser, socket, renderer, or render suite was run.
