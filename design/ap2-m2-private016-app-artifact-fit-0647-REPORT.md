# App2 PRIVATE016 source/artifact-fit review

## Outcome

**HOLD — bounded source/artifact fit only.** The final Runtime and Agent
objects are present and the transcript plus v1 selected-media dormant carriers
fit. Ordinary project-data remove does not fit the existing App capture, and
selected project-pack element/schema-source capture remains explicitly
refused. The frozen tuple has no `insertion_order` carrier, so the ordered
remove prerequisite is not met. No consumer pin, generation, native proof,
activation, or public release is claimed.

Live callers changed: **NONE**. `public014` is unaffected.

## Exact committed tuple

- Runtime commit/tree: `da77e2ddc35bf07ddd8d9e1aae5e31ea69e82406` /
  `486fe045f66182b33520bea971d31add3f713ea9`.
- Runtime parent/corrected source: `b59d22b607cbb12bb941cdcf0812b0446e5b77f1` /
  `671532c57c04ff9b9a9c232f29753fc46d82f423`.
- Agent source commit/tree: `10226a7f08a739ba3e41f8e91de6971eed63aa9d` /
  `e2c08fbe9b21a3082db7bcf62d9677babfc15e98`.
- Agent raw schema: `sha256:9cb9597a618f51949fe9ec35686e544dca812b8b252a96a4cff1f686afdfb3ec`.
- Agent canonical schema: `sha256:322733a57e781847e50228f91b6c6a9237ad2237406a188515c8f9da5e554bcc`.
- Schema inventory: **65 definitions / 37 closed clauses**.
- Runtime health/schema: `sha256:97724260188a1b07c06520d2233bf3cbae52370185b0c0b6e4c9f0bf2accdfdd`.
- Runtime raw bundle: `sha256:1bbc786daab05597f7a4d910ef0f8dcda531912b2d1e37318a35544ef039d7e9`.
- Component manifest: `sha256:1ad76db27c1d9716bb234f811bf63e1f5898cb3d5f9b835a821765e6cad895e5`.
- Artifact manifest/version: `sha256:b045b4ecc9bfc026de12b64defa31b064b1187c3638554a129403e6a6356e7d5` /
  `0.2.16`, 76 artifacts.

`git show` verified both commits and trees from the Runtime and Agent object
databases. The two required independent reports are both **APPROVE**:
`runtime-private016-typed-guard-delta-review.md` (b59 repair) and
`runtime-private016-conversion-independent-review.md` (09d0 test conversion).

## Carrier comparison

### HOLD: ordinary project-data remove

The frozen schema and generated Runtime TS define
`ProjectDataWriteArgs` as a replace/remove union: replace requires
`target`, `key`, `value`, and `mode: "replace"`; remove requires `target`,
`key`, and `mode: "remove"` and forbids `value`.

The dormant App carrier is replace-only:

- `src/tools/video-editor/commands/projectDataMember.ts:23-34` makes `value`
  required and only models replace/merge patch input.
- `src/tools/video-editor/commands/projectDataMember.ts:111-145` rejects a
  missing value and rejects every command mode except `replace`.
- `src/tools/video-editor/commands/projectDataMember.ts:316-329` always
  emits `value` and `mode: 'replace'`.

Required next carrier/owner: App2’s `projectDataMember` must gain the exact
Runtime `ProjectDataWriteArgs` remove form, including absent-versus-null
semantics and pruning only empty target/app containers. The generated App
contract export must be refreshed only as part of the separately authorized
matched consumer tuple; no shape was guessed here.

### FIT: transcript association, conditional on the frozen source plane

The final generated shape is exactly
`asset_id`, `media_id`, `source_id`, `document`, `previous_document` (null or
`DocumentPin`), and `source_schema_ref`. The dormant App command emits those
fields at `src/tools/video-editor/commands/transcriptAssociateCapture.ts:527-541`.
It preserves exact new/prior pins and null presence, records the source-item
membership/order selection at `:168-183`, and writes only the canonical
transcript reference/item planes at `:459-500`. Existing unrelated source
items and opaque payload/carrier data remain outside the replaced owner set.

The current App generated type file does not yet export
`TranscriptAssociateArgs` (`src/integrations/runtime/timeline-commit-types.ts:1-45`),
but the dormant capture uses the generic command envelope and its emitted
carrier matches the frozen schema. This is source fit, not activation.

### FIT: selected media v1; no v2 adoption

The final Runtime `MediaSelection` remains the closed five-field carrier
(`asset`, `generation_id`, `variant_id`, `object_id`, `catalog_digest`), and
`ClipAddMediaArgs` remains `{ row, media }`. App validates that exact selection
at `src/tools/video-editor/commands/parentClipAddCapture.ts:36-43`, emits it at
`:358-414`, and retains detached verified-media evidence through the dormant
capture basis at `:463-480`. Parent swap emits v1
`old_media: MediaSelection` plus `media` at
`src/tools/video-editor/commands/parentClipSwapCapture.ts:19-27`, matching the
final schema’s v1 branch. The additive Runtime v2 raw-old-media carrier is not
selected or adopted.

### FIT only for ordinary element refs; selected-pack path is held

The final `ElementRef`/`ClipSetElementArgs` shape matches the local dormant
types at `src/tools/video-editor/commands/elementCapture.ts:15-25`, and the
ordinary `clip.set-element` capture preserves the existing element identity
and optional schema pin envelope at `:103-161`.

However, `schemaSource()` refuses any `packId` at
`src/tools/video-editor/commands/elementCapture.ts:69-75`; literal parameter
capture likewise refuses `schema_source` and selected pack ownership at
`:212-234`. The overlay path refuses a row carrying `packId` at
`src/tools/video-editor/commands/elementOverlayCapture.ts:214-220`.

Required next carrier/owner: the authoritative Agent selected-pack/schema
source capture and its matched App consumer proof. Until that exists, the
existing ordinary element carrier is the only qualified dormant subset.

### `insertion_order` prerequisite is absent

There is no literal `insertion_order` in the App source/test tree, and no such
field in the frozen PRIVATE016 Agent schema or generated Runtime TS. The App
persisted source-item schema is strict at
`src/tools/video-editor/data/typed/timelineBundle.ts:82-106`; its allowed
carrier fields do not include it. The App2 status explicitly leaves
ordered-remove waiting on a real generated `insertion_order` carrier. This is
therefore an upstream contract prerequisite, not something this review can
invent or infer.

The App patch’s existing `order` field is only local batch ordering
(`src/sdk/video/timeline/patch.ts:82-103` and
`src/tools/video-editor/commands/projectDataMember.ts:223-235`); it is not an
`insertion_order` authored carrier and cannot close that prerequisite.

## Narrow evidence and next prerequisite

- `git show --no-patch` verified the exact Runtime and Agent commit/tree
  identities from committed objects.
- `git show` plus SHA-256 probes verified Agent raw schema, Runtime raw bundle,
  and component-manifest object identities; the final handoff tuple supplies
  the health, canonical, raw-bundle, artifact-manifest, and version identities.
- Offline schema/type probes compared the final generated Runtime TS and
  Agent schema branches for project-data, transcript, selected media, and
  element carriers against the App captures above.
- No existing App suites, browser/socket/native tests, generation, install,
  pin, activation, or full suite were replayed.

Next prerequisite: obtain the orchestrator-approved exact generated
`insertion_order` carrier and a matched App consumer change/proof for
project-data remove; separately qualify selected-pack element/schema-source
capture before any consumer adoption decision.
