# Source review report

## Result

The immutable A4 packet cannot be accepted unchanged. This is correctly rejected by current Runtime/Agent authority checks, not a Runtime defect.

However, the current App prepared-media production path has a genuine integration gap: Runtime captures `mediaSelection`, but `prepareGenerationAsset()` drops it; `ShotTimelineMediaControls` then sends only `preparedAsset` into a local `prepared-media` command, later serialized as `doc.patch`.

## Verified authority path

Runtime public methods:

- `runtime_protocol/service.py:2562` — `get_project_media_selection(project_id, selectors, authorize=...)`
- `runtime_protocol/service.py:2570` — `get_project_verified_media(project_id, selection, authorize=...)`
- Public selector forms are exactly either:
  - `{asset, generation_id, variant_id}`
  - `{association_id, object_id, version}`

Verified `MediaSelection` has exactly these five keys:

```json
{
  "asset": "variant-id",
  "generation_id": "generation-id",
  "variant_id": "variant-id",
  "object_id": "sha256:<64 hex chars>",
  "catalog_digest": "sha256:<64 hex chars>"
}
```

The IDs above are illustrative only. They must come from Runtime; they are not authority.

Verified metadata is bounded to `media_type`, positive `size`, and applicable positive `duration_seconds`, `width`, and `height`.

Runtime declaration and acceptance:

- `timeline_commit_port.py:128` — `RequestCommitPort.__declared`
- `timeline_commit_port.py:350` — `selected_media()`
- `timeline_commit_port.py:493` — `validate()`
- `timeline_commit_port.py:826` — selector resolution
- `timeline_commit_port.py:1022` — exact five-field selection validation

Agent’s current provider captures selections only from semantic media commands:

- `astrid/sdk/timeline/commit.py:968` — calls `port.selected_media(...)` for `clip.add-media`, `clip.swap-media`, `occurrence.*`, `placement.create`, and `shot.pool`.

Representative semantic command shape:

```json
{
  "schema_version": 1,
  "op": "clip.add-media",
  "version": "1",
  "select": "parent",
  "args": {
    "row": {},
    "media": {
      "asset": "illustrative-asset",
      "generation_id": "illustrative-generation",
      "variant_id": "illustrative-variant",
      "object_id": "sha256:<runtime-output>",
      "catalog_digest": "sha256:<runtime-output>"
    }
  }
}
```

## Immutable packet conclusion

Packet export hash:

`33934817ed76afaa7ff32968325e8aa4bc0212bfe9c62adb1c1f382f2dfff8b4`

All four requests are `commands: ["doc.patch"]`; none contains a five-field `MediaSelection`. The canonical dependency manifest has `media: []`, and the registry uses synthetic non-digest media IDs.

Therefore it cannot invoke Agent’s `selected_media()` path or satisfy Runtime’s declared-selection, CAS, manifest, and acceptance revalidation requirements. No `args.media`, manifest authority, reads, or synthetic IDs should be invented.

## App finding

Current App source:

- `ShotTimelineMediaControls.tsx:232-239` passes `preparedAsset`, not `selectedMedia`.
- `useTimelineCommandsService.ts:455-498` creates local `PlacePreparedMediaCommand` and applies `type: 'prepared-media'`.
- `localSaveSession.ts:163` converts the local intent to `doc.patch`.
- Runtime already captures the selection at `dataProvider.ts:1723-1738`.
- `useAssetManagement.ts:199-246` returns a `TimelineProvisionedAsset` without that selection.

An existing App path (`placementRequester.ts:162-190`) performs the authentic Runtime selector call, but it is not the `ShotTimelineMediaControls` path.

This distinguishes the results:

- Immutable A4 packet: fixture/input authority limitation.
- Current prepared-media App path: genuine production integration gap if semantic prepared-media acceptance is required.
- Runtime and Agent guards: behaving as designed.

## Pins and checks

Current integration heads:

- Runtime: `abd47e68de6d7a36bec8ac4f0f6e0bc01d98d14e`
- Agent: `07e6d83df69146c7dddea207f32330dc8b58dbc5`
- App: `d3bec9b4a3ead64d05021e37e5d418884434f2ab`

Relevant current source blobs:

- Runtime service: `9fe59146467fd2b5dfd62bc5e444bac7e657763e`
- Runtime commit port: `f53099bbb9daa8e034da8ae675ae1b368d097f5b`
- Agent commit provider: `e0903b7fd52e93b2cfda36d24bd9319f8a947bd8`

Checks:

- Runtime in-memory compile: passed.
- `git diff --check`: passed.
- Worktree: clean.
- Scoped Ruff: not available (`No module named ruff`).
- Existing author evidence retained: 41 media tests passed in 4.11s; not rerun per instruction.
- No product edits, tests, API/schema changes, or guard waivers made.