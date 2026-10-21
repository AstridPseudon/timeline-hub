# App M2 popup original SWAP closure/carrier custody

## Verdict

**historical closureUNKNOWN — blocked.** No retained original Runtime-accepted
popup SWAP closure was found. The `localend6` versus `accepted4` /
`omittedclip-b` difference therefore remains an unqualified source-projection
diagnostic, not an accepted-document projection verdict.

The bad result is withdrawn/unqualified for acceptance purposes. It must not
be replayed, reconstructed from flattened UI/source windows, or used to retire
the popup writer.

## Exact unavailable artifact

The following exact tuple is unavailable in the retained records:

```text
accepted canonical_document
accepted dependency_manifest
accepted head {revision_id, publication_id}
accepted receipt/publication result
the corresponding original accepted local+accepted SWAP projection pair
```

The historical original-positive records do not supply it. The retained
“approved original” diagnostic was cancelled or stopped at a snapshot mismatch;
the later `15911` and `28969` records are ADD-only attempts and failed before
an accepted popup mutation. No authenticated accepted realm/response survives
in those records.

## Preserved source witness (not acceptance evidence)

The exact source packet remains at:

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-popup-analog-playable-vp8-native.json
SHA-256: e30ed3303532e3d73adfd07670e04d1312003b7e10d2c5c008629b8b9bffad46
```

Its original fixture source pin is App commit
`309cb7a463833126e3af730fb3c6ff536d9e457c`, path
`src/tools/video-editor/commands/fixtures/recipe_m2_occurrence_media.json`,
with the same SHA-256 (`105697` bytes). That fixture is not present at the
current integration checkout; the pinned git object is present and was checked
read-only. The retained pure-vector witness is
`handoff-vw-m3-popup-original-document-pure-projection-witness-0827-vectors.json`
(SHA-256
`f04b9dbf1fb35d4173a92de49d4756c02398b811cd42bc3b551d3c249a9e71ae`). The
compact custody/witness reference is
`app-popup-original-projection-closure-witness-0917.md` (SHA-256
`c1672b8624c7dcdf4a471f39589d3c52b021c455e0571016ea9750b93b4da1cf`).

The packet's `swap` object has the raw source keys/order intact. Evidenced
source-only facts are:

- `swap.input.parent_revision.revision_id = parent-1`, content digest
  `sha256:86c97a97fb837467f83918e31ce27d76c59740c83fec38a22562ce4d213c249b`;
  `swap.output.parent_revision.revision_id =
  authoring-parent-revision-d35a5f7f583efa7dfd35b1d753cb32828cc5883957a1b396696c1e433871e09b`,
  content digest
  `sha256:2ef8479aa665cdc745c75c23a615e0edae99235c3db7de6822b5715a38efd9b`.
- The source manifest counts are input `shots=1`,
  `internal_timelines=1`, `media=1`, `documents=0`; output `2,2,2,0`.
  These are source-manifest counts, not an accepted dependency manifest.
- Parent payload order has two occurrences `[occ-a, occ-b]` and two clips
  `[clip-a, clip-b]`. The guarded clip selection order is
  `[occurrence:occ-a/clip:clip-a, occurrence:occ-a/clip:clip-b]`; the track
  selection is `[occurrence:occ-a/track:picture]`.
- The raw swapped child is `occ-a/clip-a`, `track=picture`,
  `at=1`, `hold=4`, `[from,to)=[2,6)`, `speed=2`, with the source opaque/app
  data retained (including `org.example.literal = "clip-a"` and
  `clear = null`). The source packet records occurrence A at `8000 ms` with
  stored duration `10000 ms`, occurrence B at `10000 ms` with duration
  `10000 ms`, and FPS `{numerator:30000,denominator:1001}`.
- The one source command is exactly
  `occurrence.swap-media@1`, selector
  `occurrence:occ-a/clip:clip-a`, intent `{ownership:"occurrence"}`. Its
  source fixture carriers are the closed five-field selections:
  `old_media={asset:"picture",generation_id:"generation-old",variant_id:"variant-old",object_id:"sha256:1111111111111111111111111111111111111111111111111111111111111111",catalog_digest:"sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"}`
  and
  `media={asset:"reserved-new",generation_id:"generation-new",variant_id:"variant-new",object_id:"sha256:2222222222222222222222222222222222222222222222222222222222222222",catalog_digest:"sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"}`.
  These are fixture source pins only; neither is an accepted Runtime carrier.
- The source command creates only
  `occurrence:occ-a/asset:reserved-new` and writes the target asset binding;
  no accepted receipt or publication is present.

The existing consumer/projection locations to use once the accepted tuple is
actually supplied are:

```text
App accepted consumer:
  src/tools/video-editor/hooks/useTimelineCommandSession.ts:102-117
  (accepted canonicalDocument + accepted head pair; default projection)

App projection/cap:
  src/tools/video-editor/data/shotCompositionProjection.ts:442-448,527-534

App popup/local source projection:
  src/tools/travel-between-images/components/shotTimelineDataProvider.ts:437-480
  (explicit clampToOccurrenceDuration:false)

Render-only boundary:
  src/tools/video-editor/lib/canonicalRenderBounds.ts:80-104
```

The retained pure witness reports the conditional/source-only difference as
`occ-a:clip-a.to` local `6` versus capped `4`, with local `occ-a:clip-b`
present and capped `occ-a:clip-b` omitted. This must not be relabelled as the
original accepted SWAP result.

## Peer request to Viewing + Agent

Please return one actual original accepted tuple, without replay or
reconstruction:

```text
{canonical_document, dependency_manifest,
 accepted_head:{revision_id,publication_id},
 receipt/publication_result,
 command:{op,version,select,args,intent}, source_pin}
```

The accepted document must preserve raw keys/nulls/order/all children and the
old/new media authority carriers, and must be tied to the same original
SWAP command/source pin. Viewing should then run the existing local versus
accepted projection verdict against that tuple; Agent should verify command
scope, manifest dependencies, and accepted identity. Until that arrives,
popup SWAP projection readiness is **blocked** and the historical closure is
**UNKNOWN**.

No product files, fixtures, DTOs, authorities, or tests were changed. No
browser, build, install, full suite, harness, graph, or historical replay was
run.
