# D127 finite READ-ONLY SWAP source recipe

## Custody and scope

- App base: `fe3309dba4520835a685f925468bff1acdc0506f`.
- App tree: `e55f0d65dca0c9f2ba3013df4cab999f314308b9`.
- Qualified original P2 source hash: `tests/e2e/local/three-products.p2-popup.spec.ts` SHA-256 `09f5e2c2ea2a207575534a88adf2847d68cdd389caa5d145580100f21302b2b9` (verified against the committed blob).
- Retained safe custody: D127 admitted submission `.../workers/app-D127-full-P2-admitted-resume-1407/evidence/facts.json`, `notes/submission.json`, `notes/terminal.json`; independent D125 custody `.../workers/app-D125-P2-Proof-GO-review/evidence/facts.json` and verdict.
- This is a source-level handoff only. No browser extraction, source edit, collector/probe, native execution, request replay, credential export, or Runtime run was performed.

This recipe is not an authentic replay of original3250. Dynamic project/timeline/head/media IDs and the original private provider closure are not retained in the safe custody; see `missing-components.md`.

## Deterministic source construction

1. Use the existing source fixture constructor `DirectHarness.seedThreeProducts` at `tests/e2e/local/support/harness.ts:1233-1290` with immutable inputs `referenceAt=15`, `transitions='native-none'`, and the default `occurrenceHostWindow=12`. It uses the existing `commitNativeSeed` receiver at `:870-1070`, not a new runner. The stable fixture identities are `f2-app-clip`, `f2-agent-clip`, `f2-transition-clip`, `f2-agent-clear-clip`, shot `f2-shot`, occurrence `f2-occurrence`, and marker key `f2-marker` (`:1269-1287`). The seed's parent reference clip is at 15 seconds; the target child is `f2-agent-clip` at 3 seconds on `V2`, initially `f2-placeholder` (`:930-936`, `:970-980`).
2. `preparePopupSeed` at `tests/e2e/local/three-products.p2-popup.spec.ts:254-313` reads the seeded canonical closure, reads the seeded image object, and imports those exact old bytes through `importMedia` (`:183-218`). It then appends, in order, two fixture commits through `commitFixtureCommand` (`:220-252`):
   - `occurrence.place-shared`, selected by `occurrence:f2-occurrence`, with `{ occurrence_id: 'f2-occurrence-copy', on: 12 }` (`:273-283`), creating the shared occurrence at `start_ms=12000`.
   - `doc.patch`, atomically setting parent `p2_popup_opaque` from absent, changing the target internal clip asset from its original value to the imported old asset, and adding the old asset registry entry from the authenticated selection (`:285-303`).
3. The new input is the real deterministic PNG `makePng(65, 49)`, filename `p2-popup-new.png`, MIME `image/png` (`preparePopupSeed:310-312`; generator `tests/e2e/local/support/harness.ts:368-384`). The old input is not guessed or recreated: it is the bytes read from `harness.seed.image.objectId`, imported as `p2-popup-old.png` (`:265-268`).

## Exact SWAP preconditions and order

The mounted test captures `before = history(...).head`, `beforeRaw`, and `original = canonicalAt(...before.head.revision_id)` before the gesture at `tests/e2e/local/three-products.p2-popup.spec.ts:920-938`. The operation is valid only if the popup has a unique physical occurrence/shot/internal-timeline closure, matching dependency-manifest pins and digests, and the displayed occurrence matches those pins. The production checks are `sharedPopupMediaCommands` at `src/tools/travel-between-images/components/shotTimelineDataProvider.ts:750-812`.

The source-level SWAP order is:

1. Select rendered clip `f2-occurrence-copy:f2-agent-clip`.
2. Click `Swap selected clip` and provide the new PNG (`three-products.p2-popup.spec.ts:949-954`; UI handlers `ShotTimelineMediaControls.tsx:157-199`, `:201-276`, buttons/input `:289-314`).
3. Import and resolve the new registered media selection. The producer must retain the old selection and resolve the new selection through the registered `getProjectMediaSelection` reader, validating asset/generation/variant identity (`shotTimelineDataProvider.ts:726-747`).
4. Detect one changed raw clip and one shared owner. Emit `occurrence.fork` first, with a newly allocated `shot-fork-*` ID, then `occurrence.swap-media` selected by `occurrence:f2-occurrence-copy/clip:f2-agent-clip`, with `{ old_media, media }` and an occurrence asset creation claim when the new asset is absent (`:813-871`). The shared-owner guard explicitly requires the fork carrier before media editing (`:807-809`, `:826-834`).
5. Persist those two semantic commands as one durable local intent. The capture path calls `sharedPopupMediaCommands` before any document-patch fallback (`shotTimelineDataProvider.ts:1071-1158`, especially `:1098-1113`). The expected command assertions are in `three-products.p2-popup.spec.ts:523-578`: command ordinals `[0,1]`, fork then SWAP; SWAP carries exact old/new media pins; no duplicate original body is implied.

## Supported production handoff to Runtime

The mounted production chain is:

`ShotTimelineMediaControls` → `useTimelineCommandsService.addClip` (`src/tools/video-editor/hooks/useTimelineCommandsService.ts:452-524`) → timeline persistence capture (`src/tools/video-editor/hooks/useTimelinePersistence.ts:966-1035`) → scoped popup binding (`ShotTimelinePreview.tsx:545-567`, `:611-685`) → `createLocalSaveSession` and existing IndexedDB outbox (`shotTimelineDataProvider.ts:1025-1049`; `commitOutbox.ts:1-111`) → exact persisted intent dispatch (`localSaveSession.ts:158-201`, `:269-321`) → registered `DataProvider.commitTimeline` (`src/integrations/runtime/dataProvider.ts:751-765`) → `WorkspaceClient.commitTimeline` (`src/integrations/runtime/client.ts:735-742`) → generated POST route (`src/integrations/runtime/generated.ts:202-204`).

The handoff preserves immutable inputs: the original verified `base_revision_id`/`base_publication_id` is loaded once and checked against the mounted composition (`shotTimelineDataProvider.ts:1025-1048`); outbox dispatch advances only the base pair while retaining original commands, steps, reads, and allocated IDs (`localSaveSession.ts:165-188`). The request is the existing C0 v2 shape with `source: { via: 'app' }`, `dry_run:false`, semantic commands `[occurrence.fork, occurrence.swap-media]`, one step, and the current accepted head returned by Runtime. Runtime/Agent must provide the actual dynamic values; this handoff does not invent them.

## Safe retained result

D127's sole original3250 body reached terminal failure with 5 PASS, 2 FAIL, and 1 serial NOTRUN. The SWAP public result was HTTP 409 with static tag `history_unavailable` at `three-products.p2-popup.spec.ts:495`; D125 and D127 both state that the lower private binding/cause and exact SWAP semantic test-to-namespace binding are `UNKNOWN`. No lower-guard or correlation attribution is made here.
