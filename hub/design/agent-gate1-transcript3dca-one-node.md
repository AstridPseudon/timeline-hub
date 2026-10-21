# Gate 1 retained transcript: one-node result

## Scope and exact identities

This qualification reran only the previously failed retained-transcript
Gate 1 node from Agent commit `786ee084be2b87bcc2c18d1eaea09bb8a4faf710`,
tree `565af4df4364131f7e0d1d9e34ab926a51ed90fa`:

```text
tests/editing_conformance/test_gate1_retained_transcript_sdk_read.py::
  test_verified_transcript_pin_reads_through_public_runtime_boundary
```

The server was the independently approved compatible Runtime successor
`3dcae1836a609363135d07ee435ce9beea975504`, tree
`4fa58b2551f716c35cab6005cc8add84e59da8a9`, whose parent is the immutable
normal Runtime `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`.

The normal Agent artifact pin was preserved and guarded: `runtime.lock.json`
still names `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`. The compatible Runtime
checkout was used only as the server/import source for this qualification; it
was not relabeled as the normal release or activated.

## Named central suite and provenance guards

Added the named test-service suite
`agent gate1-retained-transcript-3dca-one-node-integration` in the shared
allow-list. Before pytest it verifies:

- the snapshotted Agent tree is exactly `565af4df…`;
- the Runtime checkout is exactly commit `3dcae183…`, tree `4fa58b25…`, and
  clean;
- the normal `runtime.lock.json` source artifact remains `95bd3c5f…`;
- `astrid` imports from the snapshotted Agent tree; and
- `runtime_protocol` imports from `/home/user/work/wt/rt-pin-3dcae183`.

## Result

Central test-service run
`agt-m2-gate1-retained-transcript-one-node-gate1-retained-transcript-3dca-one-node-integration-1021013044-3912`
passed:

```text
1 passed in 1.82s
```

The earlier failure was the Runtime public kind guard:
`WorkspaceClientError: source input requires a registered config or project pack kind`.
With the approved Runtime successor, the exact pinned retained transcript read
passes through the existing public verified-document boundary.

No source test, authority, schema, endpoint, DTO, object-read path, or normal
artifact was changed. No full, browser, renderer, duplicate, or prior passing
node was run.
