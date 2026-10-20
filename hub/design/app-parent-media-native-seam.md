# Parent-media ADD: native contract and App consumer boundary

2026-10-20. Design/read-only review for `app-m2-parent-media-read-contract-review`.
PLAN remains authoritative: **M2 held; global M1 unchanged.** No writers, positive
tests, integration branches, packages or pins changed.

**Result:** frozen Bundle2 has no parent-media ADD. A later, registered Agent
successor has **`clip.add-media` v1**, supporting a useful bounded image/video
subset. It is not in the reviewed Runtime artifacts, has no actual ADD acceptance
proof here, and cannot replace all current App media callers. Runtime
`parent-media-door-proof2` proves editing an already published film, not ADD or
registry birth. Thus “parent-media ADD has no native source anywhere” is now too
broad; “App has qualified parent-media ADD” would still be false.

## Exact sources (portable git references)

Paths in this report are relative to the named repository at these exact SHAs;
use `git -C <repo> show <sha>:<path>`, without checking out branches.

| Input | Exact identity and scope |
| --- | --- |
| App under review | `/home/user/work/wt/app-m2-parent-media-read-contract-review`, `4f79aea853a53852f50456ac295588c19016f1f7` (`tl/app-m2-ordinary-qualified-compose` base). Worktree remains clean. |
| Frozen Agent Bundle2 | `/home/user/work/agent`, `027bd16d96010544331c953c0e1014e161786e71`; `_clip_commands.py` SHA256 `50a0164ddcc7686e3d13aa90f43ccbec044a975809c4aa0a6fb9e8dc49fe080e`. |
| Frozen Runtime/App pin | `/home/user/work/runtime`, `4c145dc62192f0e942e3ee3922a11488aefe9b41`, client `0.2.3`; canonical `contract/schemas/edit-command.json` SHA256 `472622c45fa6b5c7a425c949516a64a52d83192d3749e78a0f000decd088aee9`. App `runtime.lock.json` still pins this commit/aggregate `sha256:0f3d217ba0f3ca51d580bf3938fb3df1361a561de5acae7a911d21a9eea8bd9e`. |
| Actual existing-media Door proof | Runtime `19d5cecf88c8a3b215c9c14c497ce690d775606e`, `hub/tl/rt-m2-parent-media-door-proof2`; test requires exact clean Agent `f423074778f4220df808799a4f7b308e56885397`. Its `_clip_commands.py` is byte-identical to frozen027. |
| Native ADD successor | Agent `b1ec87a1e7e7bacbdbec09b6be24a02577336141`, `hub/tl/agt-m2-producer-insertion-native`, tree `580263527d7fb381ff16f2c704ad970e201b6832`; `astrid/core/timeline/schema/edit-command.schema.json` SHA256 `176108d078da49e2c925b9dfabb53f6ca003c36e0336856ac30736fd273f7b11`. This matches the source tree announced in `m2-producer-insertion.md`. |
| Public verified-input read candidate | Runtime `a9a81078e2aa30f071f84d3c64e1025e9ed62df1`, `hub/tl/rt-m2-popup-verified-media-read`, client `0.2.6`; read also present in cohort `efd2f41b3a1b76667cfd0d62e25d1ac760d08d56`. Its canonical edit-command file is still exactly `472622…ee9`, **not the ADD successor schema**. No pairing/adoption inferred. |

Shared inputs read: `PLAN.md`, `managers/app/STATUS.md`,
`design/app-writer-contract-gaps.md`, hub `design/m2-producer-insertion.md`,
`design/runtime-coordination.md`, and `hub/status/{agent,runtime}.md`.

## What the real Runtime proof settles

At Runtime `19d5ce…`, `tests/test_timeline_parent_media_http.py:236` exercises
`clip.set(clear=['hold'])`, trim, split, track label, guarded undo/redo,
lost acknowledgement followed by daemon restart/exact retry, and refusal to reuse
a retired split ID. Two parametrized cases at `:365` refuse unsupported until
and effects with unchanged storage. It uses the normal authenticated Door,
official `0.2.3` client and actual startup Agent provider, with renderer and
legacy writer tripwires **after setup**. Full authored payload, nulls/opaque
fields, manifest/history and original CAS bytes are checked.

Crucial boundary: `seed_film:27-98` ingests real ffmpeg video/audio, then calls
**`publish_parent_composition` at :90** to seed existing clips/registry. No
`clip.add-media` or media-selection read appears in the tested edit sequence.
The legacy seed is explicit setup for existing-film behavior, not new-media
acceptance. Hub Runtime STATUS reports **3 passed**, not yet manager diff-reviewed
at its recorded 03:40 update. This reviewer inspected source, did not run that
socket suite, and does not have its exact central command/log in the available
hub report. Do not convert those three passes into ADD coverage.

## Actual native ADD and capture

Frozen027 `astrid/sdk/timeline/_clip_commands.py:17-36` rejects clip types
media/image/video/audio and any asset/asset_id/media_id/object_id key, **including
explicit null**. App `commands/parentClipAddCapture.ts:39-43` intentionally ports
that refusal. A hold clip with `asset` is also rejected. Neither command is
registry registration. Frozen `commands.operations()` lists occurrence media,
not parent media swap/add; the historical separate `clip.swap-media` branch is
not part of this frozen pair.

Successor `native_parent_media_commands.py:21-32` registers this exact command
through normal `commands.operations()`:

```python
call = {'schema_version': 1, 'op': 'clip.add-media', 'version': '1',
        'select': 'parent', 'args': {'row': row, 'media': selection}, 'intent': {}}
plan = execute(original_bundle, [call], verified_media=verified_media)
captured_command = plan.commands[0]  # retain every capture claim unchanged
record = plan.records[0]
```

This uses the actual native executor/capture mechanism, not a proposed helper.
There is no dedicated public `capture_parent_add_media` export in this source.
The public `capture_assembled_media(bundle, assembled, media, *, replace_clips,
verified_media)` serves the real assembler; do not fabricate assembler children
to adapt an App drop. Ordinary `clip.add-media` also works without
`timeline.assembled-target` and without requiring empty occurrences (permanent
`test_parent_media_append_creates_visual_track_and_keeps_shared_closure_pins`).
The separate assembled target command asserts the exact entire flat clip
collection, optionally composes deletes, and is not an App single-clip replace
operation.

Closed `args` require `row` and unchanged five-field `media` selection:
`{asset,generation_id,variant_id,object_id,catalog_digest}`. Closed intention is
`{}`, select is `parent`; row uses the existing open complete ClipRow schema
requiring `id,track,clipType,at,hold`. **`row.asset` may differ from
`media.asset`**: the former is the authored parent alias; the latter remains the
exact selected variant alias. Never rewrite the selected pin to match a UUID.

Portable native fixtures, copied without stripping fields:

* Agent `tests/editing_conformance/fixtures/recipe_parent_media.json`, SHA256
  **`9738d7e34b1a2b2a68bba40313ba78839e1f8b8f7a5b1e93a4c585e436b0ff1f`**;
  exact local copy [native-parent-media-golden.json](../workers/app-m2-parent-media-read-contract-review/notes/native-parent-media-golden.json).
  `commands[1]`/`records[1]` is a full native parent video ADD;
  `commands[2]`/`records[2]` is the second sequential ADD over the staged first.
  `bundle`, `verified_media`, `after_bundle` preserve the complete native fixture.
* [native-parent-media-cases.json](../workers/app-m2-parent-media-read-contract-review/notes/native-parent-media-cases.json)
  contains full independent `video-new-alias`, `video-existing-exact-alias` and
  `image-media-row` inputs/captured commands/records/after bundles. These are
  **detached pure inputs**, never Runtime custody or acceptance receipts.

The record observes parent config fps and `parent/source.source_window` (this
ref resolves to parent.config), complete destination track and track membership,
registry container shape and exact alias state, clip collection shape/order and
clip ID absence. Bindings are `media.owner -> parent`,
`media.track -> parent/track:<id>`; dependency is `media.new`, kind `media`,
policy `exact`, with the original full selection. Writes are complete alias and
clip leaves when born, plus normal derived clip mirror writes. Command claims
include reads/selections/bindings/created/expect/authorship/resolved. Never
reconstruct just the row or a before/after diff at send/ACK time.

## Authority, storage and timing limits

Authority follows existing Runtime `timeline_commit_port.py`:
`MediaReads.selection:467`, `_selected_project_media:560`, `selected:656`, and
`RequestCommitPort.selected_media:266`. Public frozen
`getProjectMediaSelection(project, query)` resolves either explicit
asset/generation/variant or exact managed association/object/lifecycle version
into the five-field pin. It checks project/realm, completed registered catalog
identity, managed object and catalog metadata; output selection additionally
checks exact settled attempt/provenance, durable eligible lifecycle and unique
variant binding. It does not select today's primary implicitly.

Server commit always supplies/revalidates metadata via `selected_media`; caller
MIME, URL, browser-probed duration, CAS spelling and generation ID alone are not
authority. Native `_media_inputs._verified` requires matching detached selection
and unambiguous identical verified values, positive integer size, image/video
MIME kind, and positive intrinsic video duration. Local pure capture cannot
establish where those values came from. Frozen App public selection read returns
the pin, **not VerifiedMedia**. Reviewed `0.2.6`
`getProjectVerifiedMedia(project, selection)` reads
`GET /v1/projects/{project}/media-selection/verified` with all five fields and
returns the existing VerifiedMedia shape. This read closes the metadata-fetch
seam only; it neither registers ADD nor qualifies a new pair.

| Case | Exact successor behavior; no inferred widening |
| --- | --- |
| New alias | Existing authored registry/assets containers required. Creates exactly `{media_id:object_id,type:'image'|'video',generationId,variantId}` and records `parent/asset:<alias>` birth. No URL/duration/thumbnail/provenance/opaque metadata argument or standalone register operation. |
| Already bound alias | Requires **whole entry equality** with that four-field binding. Even one extra `opaque:null`, file, duration or MIME-form type differs and refuses; it is not an upsert/merge. Only clip is born; inverse leaves the reused alias intact. Never trim the entry to make it pass. |
| Registry location | Uses main `parent_registry.effective_parent_registry`: direct-only/config-only retain location; equal dual storage mirrors leaf writes. Unequal dual storage, null/opaque registry or assets and absent containers refuse without manufacturing containers. Unknown sibling entries/fields survive. |
| Source kind | Verified image/video only, active visual output track only. `clipType` must be `media` or exactly the verified kind (`image`/`video`); App image `hold` and audio are unsupported. Frontend drag `sourceKind` and provisioning `source` labels confer no authority and are not new wire fields. |
| Literal timing | Finite nonnegative `at`; positive explicit `hold`; positive speed (absent means 1, null refuses). Video requires finite `0 <= from < to <= intrinsic duration` and exact `hold == to-from`; timeline length is hold/speed. Image allows no nonnull from/to and requires speed 1. No fabricated source window from a URL/duration fallback. |
| Null and unsupported forms | Additional asset_id/media_id/object_id/clip_type keys refuse even null. Nonnull source/URL selectors, time maps, nested clips/children, anchor, transition and declared timing relations refuse. Null source/transition survive; opaque row fields survive exactly. Parent config source_window may be absent or null, but any nonnull value refuses. fps accepts rational/positive scalar and the native null/absent 30 default; tagged reads preserve null versus absence. |
| Identity | Caller allocates raw row.id and alias once before capture. Native absence checks do not prove never-before-used IDs. Provider `commit.py:_check_reservations:471-563` scans accepted boundaries/created records monotonically, including registry authority. Retired ordinary clip/asset identities cannot be reborn; trusted inverse/redo can restore. A current-row allocator alone is insufficient. No actual parent-ADD retired-ID acceptance test was run here. |

## App caller mapping (App 4f79)

| Active route and durable effect | Mapping and remaining requirement |
| --- | --- |
| Existing AssetPanel/asset-key drop: `useExternalDrop` -> `external-drop-utils.handleAssetDrop:745` -> `useAssetManagement.handleAssetDrop:311-365` -> `buildAssetDropEdit` -> rows/applyEdit. | Parent ADD is the right semantic operation only after selecting the exact raw owner/track, clip row, full registry binding and five-field pin. Existing App entries are commonly MIME/URL/metadata-rich and fail exact-binding reuse. `getPlayableAssetKind` also derives kind from MIME/extension, not verified metadata. Do not certify a resolved/display registry as raw accepted state. |
| Gallery single/multi-generation drops: `external-drop-utils:544-743`, `useAssetManagement.prepareGenerationAsset:205-249`; shot final-video/image-pack drop in `useExternalDrop:140-408`. | Current registration planner creates an alias and metadata from generation/variant hints, URL, duration and MIME; variant may be absent. Resolve exact chosen variant first. Multi/shot paths also create tracks/groups and depend on order, snapping and free-lane choice; one ADD does not cover those observations or canonical group migration. Capture ordered batches against staged original state, never independently against the pre-batch collection. |
| File import: `external-drop-utils.handleFileDrop:275`, `useAssetManagement.uploadImageGeneration:366` / `uploadVideoGeneration:453`, Runtime `dataProvider.prepareMediaImport:1168`. | Host import is valid media preparation and must remain. It persists import-operation recovery, returns registered generation/variant/object and updates local activeRegistry; this is not canonical ADD. `toPreparedMediaImport:1507` authors file, content_sha256, MIME type, duration, provenance/extensions. Native ADD creates only the four-field binding; it cannot claim preservation of that full authored entry. Audio preparation/placement is also outside the ADD subset. Upload skeleton replacement must remain coherent with accepted state. |
| `useTimelineCommandsService.addClip:458` prepared path -> `place-prepared-media`; unprepared path plans target/rows. `useAssetManagement.placePreparedAsset:265-309` shares this route. | Local semantic commands are still local: `useTimelineCommit:433-453` runs `applyPreparedMediaCommand` then `commitData`, with snapshot-save fencing at `:339-350`. Not an EditCommand commit producer. Image builder uses `hold`; video/audio builder omits explicit hold (`timeline-asset-plans:280-392`), so neither row can be blindly forwarded. Native image codec needs Agent/Viewing equivalence qualification; do not silently rewrite authored type or discard opaque fields. Video's explicit hold can be derived only from verified explicit source endpoints under the native rule, preserving all other fields. |
| Automatic target creation/snapping/free-track/top insertion: `planAssetDropTarget:205-273`. | Native ADD reads an existing track; ordinary track.create can compose, but App's collision/snap/top-order policy is not automatically recorded by ADD. First slice should use an already explicit compatible track/time. Do not call coverage complete by freezing an unrecorded mutable choice. |
| Prepared replacement/duplicate/group conversion: `commands/media.ts:462-715`, `useSwitchToFinalVideo.ts:82-153`, `useClipEditing.ts`; swap descriptor `commands/media.ts:213-434`. | `replaceClipId` preserves identity and existing row fields/window; removeClipIds and afterClipId also carry group/ripple behavior. Native ADD is birth only. Delete+ADD of the same ID violates reservations; assembled-target replaces the entire observed flat collection and is not this intent. Frozen occurrence swap is raw-child-only/same-kind; no parent swap in the frozen registry. Keep these writers/tests. |
| Standalone registration: `useAssetOperations:94-172`, facade `registerAsset:952-988`, Runtime `dataProvider.registerAsset:1147-1162`. | Still writes timeline registry via snapshot save, even without placing a clip. Native alias birth is internal to ADD and cannot replace standalone registration or arbitrary entry refresh. Keep media/catalog prep separate from canonical registration; no new upsert path is implied. |

## Next bounded implementation and actual acceptance test

1. **Agent/Runtime owners first:** review/freeze the exact native successor and
   generate/pair official artifacts normally, including the existing public
   verified-media read. Do not point frozen App types at b1ec code or bypass
   provider/schema compatibility. Qualify parent ADD through normal startup
   provider/Door, with real host-imported or settled registered media. The
   current proof2 fixture can supply existing-film preservation/tripwires but
   its legacy media seed cannot count as the ADD being tested.
2. **Small useful slice:** one explicit video row on an already explicit active
   visual parent track, with verified explicit endpoints and new reserved clip
   ID; either a native four-field already bound alias or a fresh alias whose
   entire requested binding is exactly the native binding. Capture through
   execute as above; port against the complete goldens, reuse App commit
   session/outbox, and keep the original basis/selection/IDs across dependent
   edits, exact retry and ACK. No claim that all existing import descriptors
   satisfy this slice. Preserve every authored row/registry field; if the
   caller requests more than the contract can carry, retain its draft and
   report the bounded owner gap rather than reducing it.
3. **Actual acceptance requirement:** use official selection+verified GETs;
   ADD -> reload exact full canonical document/manifest/history -> guarded
   inverse -> redo. Run both new-alias and exact-reuse cases; assert distinct
   created facts and alias survival/removal. Include existing opaque registry
   siblings/parent/track/rows, rational fps and trimmed source endpoints.
   Lose ACK, advance unrelated head, restart, resend byte-identical persisted
   body/key and verify one accepted result; changed key payload/catalog,
   lifecycle/authority, wrong project/origin, occupied and retired clip/alias,
   extra/null binding fields and unsupported timing must refuse atomically.
   Tripwire legacy writers/evaluator during edits. This requires the central
   test service; **not run/requested by this read-only review**.
4. **Remaining owner gaps:** lossless rich existing/new App registry entries,
   image hold codec/evaluation equivalence, audio, parent identity-preserving
   replacement, standalone registration and automatic placement/group policy.
   Resolve each against the actual caller positives before retirement; no new
   op/schema field is proposed here. Keep all current positive media/import/
   replacement tests and writers until their replacement qualifies.

## Review validation

Executed exactly:

```sh
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -B /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-parent-media-read-contract-review/notes/probe.py
```

**Exit 0:** exact permanent golden records/after bundle and deterministic replay;
29 isolated native diagnostic cases, **11 pure positives with exact inverse,
18 expected refusals**. Every input bundle/command/verified value remained
unchanged. Full diagnostics are [probe.py](../workers/app-m2-parent-media-read-contract-review/notes/probe.py)
and [probe-results.json](../workers/app-m2-parent-media-read-contract-review/notes/probe-results.json).
The script reads b1ec through git archive into a temporary notes directory,
cleans that source automatically, and never edits another worktree or environment.
No provider acceptance, durable reservations, actual Runtime ADD, App test suite,
browser/pixels/audio, install, build, tsc, sockets or full suite was run. This is
a source contract review with pure semantic probes, not writer retirement or
release evidence.
