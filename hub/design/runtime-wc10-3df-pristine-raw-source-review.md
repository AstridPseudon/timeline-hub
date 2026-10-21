# Runtime WC10 reciprocal review: Agent `timeline.init@2` raw source

Date: 2026-10-21

## Exact verdict

**SOURCE ACK — bounded to the committed Agent source tuple, with activation
held.** Agent commit `3dfdb1fa8c51b51f142cf6630816b313dc212cbd` (tree
`20f436e18f6291eb5e38e3e5e058d02bac0f3fb5`, parent
`7c9ef2ed5e70da1a13e89278496c74321453955a`) is compatible with Runtime's
existing prepared canonical-document carrier at Runtime `b92d3e7a05eec65c142294ef4873edd059e9b31d` (tree
`6abc2f117391de8e7e35c0283f575a002199894d`). No Runtime DTO, port, provider
ABI, endpoint, store, or Runtime source change is required for this source
tuple.

This is not approval of caller activation, migration, generated artifacts,
pinning, release, route retirement, or a paired product qualification.

## Source and schema checks

- The Agent schema is raw and canonical as the packet specifies:
  `d6aa2a9e76544cf3c58b313830b0fce7ce767577a0073192ff26dc88a2e97f7c`;
  it has 56 definitions and 29 closed `EditCommand` clauses. The parent
  schema is `6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`.
- `timeline.init@2` closes the args to exactly `name`, `slug`, and `config`;
  `config` is the sole open semantic-JSON subtree. The v1 args remain exactly
  `name`, `slug`, and `output`.
- The v2 handler admits only ordinal zero, the exact authenticated pristine
  empty parent, empty placements/shots, and absent parent `name`/`slug`.
  `_require_empty_structure` runs before the first `ctx.write` and covers
  `tracks`, `clips`, `occurrences`, `placements`, `shots`, `groups`,
  `pinnedShotGroups`, `media`, `references`, `reference`, `assets`, and
  `registry.assets`. Nonempty values are refused as unrecorded births. Forged
  `created` claims do not become authoritative and are refused by the
  existing claim/capture checks; they do not produce an accepted recorder
  write.
- The only v2 authored writes are scoped `parent.config`, `parent.name`, and
  `parent.slug`. The raw initializer suppresses the ordinary mirrored-clips
  derived write, so absent/raw config members are not synthesized.
- The v1 handler remains the existing output recipe, including its
  `registry.assets` write. The exact `remote.py` and `timeline_duplicate.py`
  caller blobs are unchanged from the parent. The custom-canvas
  `RemoteTimelines.create_empty` positive and populated duplicate workflow
  therefore remain live and are not treated as v2 pristine initialization.

## Runtime carrier compatibility

Runtime's `ParentComposition.config` is `RawTimelinePayload`, an open object;
the prepared commit already carries the complete canonical document. Runtime
persists and reloads that payload through its existing canonical JSON storage,
so semantic raw values, explicit `null`, absent members, opaque siblings, and
array order are carried without a DTO or ABI addition. The existing provider
boundary continues to own authenticated bootstrap intent, original
publication/base-head identity, CAS/head checks, and retry history. Runtime's
legacy `publish_parent_composition` path remains refused for tracked
publications with `timeline_commit_required`.

The precise limitation remains: Runtime canonical JSON sorts object keys.
This ACK promises semantic JSON and array/member order, not textual JSON
object-key ordering. If textual object-key bytes become a requirement, this
verdict no longer applies and a codec decision is needed.

## Evidence and boundaries

The packet's independent Agent review recorded 75 focused tests passed and a
compact probe refusing all 12 structural paths plus a forged-claim case with
no recorder writes. Its provider controls cover init -> undo -> reinit refusal,
authenticated bootstrap/history identity, and the v1 positive/registry
consequence. I did not replay that broad Agent lane, per the task boundary.

I ran only these Runtime unit probes on the current `b92d3e7` source:

```text
PYTHONPATH="$PWD" /home/user/work/venv-runtime/bin/python -m pytest -q \
  tests/test_timeline_commit_port.py::test_create_has_real_atomic_empty_bootstrap \
  tests/test_timeline_commit_port.py::test_created_timeline_provenance_and_exact_retry_survive_restart \
  tests/test_timeline_commit_port.py::test_opaque_foreign_looking_json_is_preserved \
  tests/test_timeline_commit_port.py::test_tracked_legacy_publication_rejected_before_writes
=> 4 passed in 1.34s
```

No HTTP, native, full, browser, renderer, install, live caller, private017
widening/allocation, pin, release, or activation run was performed. Existing `RemoteTimelines.create_empty`, its
custom-canvas positive, and the populated duplicate remain outside this source
ACK's qualification claim. The next step is a separately authorized paired
qualification that proves those positives, exact retry/restart, inverse, and
later-edit refusal without changing v1 or retiring the legacy caller here.
