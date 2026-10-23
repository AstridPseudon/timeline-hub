# A4 track `doc.patch` witness — Luna

Date: 2026-10-23

## Source identity

- Agent worktree base: commit `079580ca46af77e0292d49dc34386b25c8391f99`, tree `2deab1a1494fbccfce5e9235412bacb8a949c0cd`.
- App frozen qualified ref read-only: `origin/codex/handover-timeline-r4-20261019-candidate-app-qualified` at commit `8f0c2484463e9b666d184a744d52e252984e551a`, tree `26ad064632fac9ff123670aa7d6ed0e3d8f89178`.
- App dormant capture donor read-only: commit `7f7e2daffad39a6d9aa3917a9fc526ba91caf2e6`, tree `2652d85a0ab40bcf0e88443f721dc4b868eeb743`; this is the exact `src/tools/video-editor/commands/trackReorderCapture.test.ts` source. It is not present at the qualified-ref tip.
- Agent witness blob: `ca046a721d527a1f6bf383659b8b5bbaada4d13d`; SHA-256 `fa9aa1ce49e3acab4fda0be91f62ad6c3f98b704b3b063c4c7450d6febeff546`.

## Exact App-to-Agent map

The dormant App capture test preserves three App-shaped rows: the authored
`picture` row, an `audio` row with explicit null/false/zero opaque values, and
an `overlay` row with an opaque array. The new Agent witness loads that
existing fixture and carries those rows into a real runtime document; it does
not assert the dormant `track.reorder` envelope.

| App source/test claim | Agent witness | Result |
| --- | --- | --- |
| `trackReorderCapture.test.ts` donor: raw rows, opaque values, sibling preservation, desired order, source immutability, JSON round-trip, stale identity/order and malformed/duplicate refusal | `test_detached_track_doc_patch_preserves_rows_and_json_replays_without_source_write` | Covered for the current generic `doc.patch` `list.move` shape. |
| Frozen mounted `useTimelineTrackManagement.test.ts:55-93`: mixed-kind/order pure helpers | Existing App suite remains authoritative; Agent witness tests the emitted document order, not the TS helper | Not duplicated in Agent. |
| Frozen mounted `useTimelineTrackManagement.test.ts:163-193`: missing data/authored rows, incomplete/stale projection, duplicate/empty/foreign/delimiter/non-string identity refusal | `test_detached_track_doc_patch_refuses_duplicate_identity_before_mutation`; public malformed operand cases | Duplicate collection refusal and provider no-write are covered. TS projection/editability cases remain App-owned. |
| Frozen mounted `useTimelineTrackManagement.ts:1064-1094`: local `applyEdit({type: 'track-order'})` with an internal `timeline.reorder` edit command | `test_public_provider_accepts_current_doc_patch_and_persists_c0_step_and_read_records` | The mounted persistence boundary is labeled `doc.patch`; no `timeline.reorder` provider is invented or claimed. |
| Current A2 local-save boundary identified by peer handoff: persisted document intent becomes generic `doc.patch` with previous values, reads and created claims | Public provider test plus refusal/conflict tests | Covered through the existing `DetachedRealm`/real command provider harness. `createTimelineCommandSession` is not treated as mounted: it has no production value callers, only type imports. |

## Covered provider invariants

- Generic `doc.patch`, `list.move`, exact previous row, declared collection
  membership/order read, empty created claims, C0 label/merge/step patch,
  accepted response and dry-run null receipt.
- Explicit null and opaque row values, untouched `config.app`/parent opaque
  data, order change, detached source immutability, and JSON command replay.
- Invalid previous/order/anchor rejection with structured invalid status and no
  head/history/document write.
- Membership change rejection (`selection_changed`), order ABA rejection after
  returning to the original final order, and a disjoint sibling field change
  merging with the reorder.
- Duplicate identity refusal before mutation and occupied/forged created claim
  refusal. No alternate executor, golden drop, TS execution, product mutation,
  new operation, schema, client, or pin was added.

## Precisely uncovered

- The dormant App `track.reorder` command envelope (`select`, qualified order
  refs, `expected_order`, authorship/selection claims) has no registered Agent
  provider and is intentionally not revived.
- Exact App drag-helper behavior (mixed-kind boundary helper semantics,
  editability recheck, projection validation and local `applyEdit` call shape)
  remains covered only by the existing App suite.
- This Agent witness does not prove browser/HTTP/live App execution or that the
  mounted App local state has emitted this exact patch at runtime; it proves
  the registered current provider boundary once the mounted A2 persisted
  intent is a generic `doc.patch`.
- It does not claim transcript association, after-anchor capture parity, or
  any old operation-specific claims. Existing App implementations and tests
  remain retained as required.

## Acceptance

The new file is test-only and is the only repository file changed:
`tests/editing_conformance/test_a4_track_doc_patch_witness.py`.

Targeted evidence:

```text
PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m pytest -q tests/editing_conformance/test_a4_track_doc_patch_witness.py
9 passed in 2.36s

PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m pytest -q tests/editing_conformance/test_doc_patch_v2.py
102 passed in 13.64s

/home/user/work/venv-agent/bin/ruff check tests/editing_conformance/test_a4_track_doc_patch_witness.py
All checks passed!

/home/user/work/venv-agent/bin/mypy --config-file pyproject.toml tests/editing_conformance/test_a4_track_doc_patch_witness.py
Success: no issues found in 1 source file
```

No full/browser/HTTP/native journey suite was run or requested.
