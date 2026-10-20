# App M2 popup add/swap/placement command handoff

Status: popup/placement design and fixture request only. A separate standalone
parent literal-add capture is recorded below; it does not close this popup gap.
No App popup, provider, session, outbox,
`DataProvider`, or placement implementation was changed. The App branch remains
the M1 base `9c074972cea65c3a8352a0d0fc8672b609846ecc`.

This handoff is for the App manager and Agent manager. It deliberately does not
install an App-local opcode or copy the frozen R4 popup helper: the exact native
popup operation is not published yet.

## Source and contract pins checked

| Area | Ref/commit | Result |
| --- | --- | --- |
| App base | `tl/app-m2-popup-command-handoff` / `9c074972c` | M1 opaque-root recovery guards are present; popup still has the whole-graph save path. |
| App immutable media read | `tl/app-m2-media-selection-port` / `3368b73fe` | Reviewed `DataProvider.getProjectMediaSelection` read and validation are available. |
| Agent integrated baseline | `tl/integration` / `fc324e838` | Current native command registry baseline. |
| Agent parent clip creation | `tl/agt-m2-first-clip` / `0ace5c0bd` | Exact `clip.add` golden exists, but it is parent-only, non-media, and literal. |
| Agent parent media swap | `tl/agt-m2-media-swap` / `e8f7c2c89` | Exact `clip.swap-media` golden exists, but it is parent-only and preserves an existing registry slot. |
| Agent scalar commands | `tl/agt-m2-scalar-commands` / `ceb2ab67b` | `track.set` and `clip.set-params` support parent/occurrence scalar targets; neither creates media/registry state or placement. |
| Runtime media-selection parity | `tl/rt-m2-media-parity` / `cd4c21e`, proof `tl/rt-m2-media-proof` / `c709100` | The Runtime read returns the immutable selection identity used by the command provider. |
| Frozen App R4 reference | `origin/codex/handover-timeline-r4-20261019-candidate-app-qualified` / `8f0c2484` | Contains old `timeline.add`/`clip.swap-asset` occurrence helpers; those are not current Agent opnames and must not be ported. |

The current reviewed App read is `src/integrations/runtime/dataProvider.ts:733`
and its `DataProvider` capability is `src/tools/video-editor/data/DataProvider.ts:458`.
It validates and returns exactly:

```text
(asset, generation_id, variant_id, object_id, catalog_digest)
```

The provider must retain this tuple as captured input. It must not derive
`object_id` or `catalog_digest` from a display URL, registry `file`, generation
display ID, or a newer gallery row. For a replacement's old media, the App may
query the same Runtime read using the canonical asset/generation/variant pins
already present in the child registry; it must refuse if those pins are absent or
ambiguous. The old R4 check that compared `object_id` with an asset key is not a
valid substitute for this read.

## Exact App ownership and current write path

The popup is an occurrence/internal-track editor, not a parent-track editor:

* `src/tools/travel-between-images/components/ShotTimelinePreview.tsx:514-521`
  constructs `createShotTimelineDataProvider` for one `occurrenceId`.
* `src/tools/travel-between-images/components/shotTimelineDataProvider.ts:135-155`
  removes the projected `${occurrenceId}:` clip prefix before writing the child
  timeline back into the canonical occurrence revision.
* `src/tools/video-editor/data/shotCompositionProjection.ts:326-347` maps a raw
  child clip to a projected display row, but its authoritative identity is the
  occurrence plus raw child ID. A display ID or a tuple must never be used as
  ownership proof.
* `shotTimelineDataProvider.ts:390-434` reloads the canonical parent closure,
  selects the exact occurrence, and projects its internal timeline and registry.
* `shotTimelineDataProvider.ts:435-593` is still the compatibility writer:
  `saveTimeline` builds a whole canonical graph, persists a recovery draft, calls
  `updateCanonicalShotTimeline`, and finally calls
  `shotCompositionAdapter.publish`. The generic persistence funnel reaches it
  through `useTimelinePersistence.ts:401-405`.

For the future command producer, the ownership split is therefore:

| State | Authoritative owner | Command target shape to capture (semantic shape, not a new wire name) |
| --- | --- | --- |
| Popup child track | occurrence internal timeline | occurrence + raw child track identity; projected `occurrence:O:track:T` is not sufficient by itself. |
| Popup child clip | occurrence internal timeline | occurrence + raw child clip identity; preserve the raw `id`, not the prefixed display ID. |
| Popup child registry | same occurrence internal timeline | exact asset-key binding and its old/new immutable media tuple. Do not repair or upsert it as a side effect. |
| Parent lanes/clips | parent timeline | untouched by popup add/swap unless a separately captured parent command explicitly owns them. |
| Occurrence placement | parent canonical occurrence geometry | separate parent placement/occurrence command; do not encode it as a child clip `at`. |

This distinction is important because the popup-local `at` is relative to the
occurrence, while the canonical child revision stores child timing and the
parent occurrence stores its own `atMs`/duration/track placement. The future
command must state which coordinate it owns and record the conversion once.

## Native coverage result

There are exact native goldens for two related parent operations, but no exact
native golden for this popup slice:

* Agent `0ace5c0bd` registers `clip.add` with `select: "parent"`. Its handler
  rejects `occurrence:*`, rejects media clip types and all asset/media selectors,
  and creates only a complete literal parent row with a preallocated clip ID.
  It cannot represent popup media add.
* Agent `e8f7c2c89` registers `clip.swap-media` with a
  `parent/clip:<id>` selector. It reads both parent registry codecs, requires
  existing registry bindings, verifies Runtime-selected media metadata, preserves
  literal timing/source windows/clip identity/opaque fields, and writes only the
  authored asset key. Its inverse has no created IDs. It cannot target a child
  occurrence or create a missing child registry slot.
* Agent `ceb2ab67b` supplies occurrence-capable scalar writes only. It does not
  provide media selection, registry creation, child clip creation, child media
  replacement, or placement semantics.

Consequently, no popup App capture/parity helper is added here. Porting the
parent fixtures as if they proved popup semantics would either invent ownership
or silently fall back to a whole-graph write.

## Missing Agent contract to publish

Agent should publish the exact operation name/version and schema for the
following two semantic operations. The labels below are descriptive only; they
are **not** proposed wire opnames.

### Occurrence-owned media add

Required capture and recorder facts:

1. Exact parent head pair and occurrence closure: project, parent timeline,
   occurrence ID, shot ID/revision, internal timeline revision/content digest,
   and the child track's raw ID/kind/active/output role.
2. The selected five-field media tuple from Runtime, plus the Runtime-verified
   media kind/size/intrinsic duration at acceptance. App args must carry the
   tuple, not a guessed media descriptor.
3. Relative child `at` and intended duration/hold in the operation's declared
   units, with the occurrence boundary check. The operation must say whether
   video source windows/speed are supported; unsupported timing must refuse.
4. A clip ID reserved before the outbox request is sealed. The same ID must be
   reused after lost acknowledgement, restart, exact retry, and server rebase.
   The command must record the created child clip and every dependency that can
   consume it.
5. The exact child registry state for the selected asset key. The contract must
   explicitly choose one of these behaviors: (a) an existing exact registry
   binding is required, or (b) the command creates the binding from the
   Runtime-verified selection. If (b), registry creation and clip creation must
   be one atomic command with reserved identity and inverse order; no hidden
   registry upsert is acceptable.
6. Full ordered membership/selection, absence guards for the new clip and any
   new registry key, exact track ownership, and all reads needed to reject a
   concurrent child/occurrence replacement. A sibling occurrence and all parent
   state must be proven untouched.

### Occurrence-owned media replacement

Required capture and recorder facts:

1. Exact occurrence + raw child clip identity and the complete old immutable
   media tuple captured before local preview. Do not select by projected/display
   ID and do not refresh the old tuple after authoring.
2. Exact new immutable media tuple from the reviewed Runtime read. Old and new
   selection records must be independently verified at commit; missing,
   mismatched, foreign, or changed catalog pins refuse atomically.
3. Exact old child registry binding and exact new binding. The handler must not
   repair an absent/mismatched slot or search another owner for a matching object.
4. Preservation proof for clip ID, owner/track, relative start, hold/duration,
   source windows, speed, app intent, params, and opaque JSON. The only ordinary
   authored change should be the media binding defined by the published schema.
5. No created ID for the bounded existing-slot form. If the contract allows a
   new registry slot, it must publish its reservation and inverse dependency
   rules explicitly; otherwise refuse that shape rather than allocating during
   replay.
6. Guarded inverse that restores the old tuple/binding and refuses after a
   dependent consumer write or changed child registry state. Same-value writes
   remain recorded where the native recipe requires them.

Both operations must compose with the existing command session/outbox and use
the normal Runtime commit path. The command must be replayable from the
recorded canonical closure; App must not send a local `TimelineCommand`,
`TimelinePatch`, `timeline.add`, `clip.swap-asset`, or snapshot graph as a
compatibility payload.

## Smallest portable fixture request for Agent

Please publish two small raw-bundle/conformance fixtures plus their strict
capture/parity tests. They can share one bundle shape and differ only in the
child timeline/selection state:

* parent: one unrelated visual track/clip sentinel;
* occurrence `occ-a`: shot/revision/internal-revision pins, one visual child
  track, and the target child state;
* sibling occurrence `occ-b`: one unrelated child and registry binding;
* child registry and parent registry are distinct and both retained in the
  output;
* parent occurrence placement has non-zero `atMs` and a finite duration, so
  the fixture catches accidental conversion of child-relative time into parent
  time;
* opaque fields on parent, occurrence, track, registry entries and clips are
  nontrivial JSON and must byte-round-trip.

Fixture A, `popup_occurrence_media_add_v1`: `occ-a` has an existing output
track, no target child, and no selected asset binding; command input contains
one image selection tuple and a preallocated child ID. Assert one child add,
the contract's explicit registry behavior, sibling/parent preservation,
reload, inverse, redo, lost-ACK exact retry, and stable created ID.

Fixture B, `popup_occurrence_media_swap_v1`: `occ-a` has one existing media
child with an old asset binding and literal image timing; command input contains
the old and replacement selection tuples. Assert only the replacement media
binding changes, all timing/opaque fields and child ID survive, registry
bindings are not silently repaired, and inverse/replay restore the old binding.

The fixture should also include refusal cases for a parent selector, a
projected/display selector, missing old tuple, changed catalog digest, missing
occurrence/internal revision, duplicate child ID, missing track, sibling-owner
substitution, and a child registry collision. A combined add+swap batch is not
needed until each independent operation has a native golden.

## Placement boundary and next split

`src/shared/lib/placement/placementService.ts` is a separate open writer:

* `placeGeneration` at `:172-192` resolves media, mutates parent config and
  registry, then uses the snapshot CAS cycle;
* `unplaceGeneration` at `:208-224` removes or pools the parent clip;
* `batchUpdatePlacementFrames` at `:234-239` mutates parent placement frames;
* callers include `src/shared/hooks/shots/useShotGenerationMutations.ts`,
  `src/shared/lib/timelineFrameBatchPersist.ts`, and the reference/upload and
  generation-backfill flows.

No placement command is published on the checked Agent refs. Do not wire this
service to the parent clip-add or popup child-media command. Agent must publish
the exact canonical placement operation(s), including generation/media identity,
parent clip/registry ownership, frame collision policy, pooled state, created
IDs, and inverse ordering, before this App lane can capture them. The relational
`shot_generations.timeline_frame` and `metadata.end_frame` effects remain outside
canonical M2 scope per PLAN and must not be smuggled into that command.

## App implementation split after Agent publication

1. Add a narrow popup capture adapter beside the existing command capture code;
   feed it the published schema/recorder and the reviewed
   `getProjectMediaSelection` read. Capture synchronously before preview and
   retain the original command/guards in the existing outbox.
2. Add strict byte-parity tests against the published Agent add/swap fixtures,
   plus popup provider tests proving occurrence ownership, exact old/new media
   tuple use, created-ID reuse, and no parent/sibling mutation.
3. Route both add and swap through the same `commitTimeline`/command-session
   outbox path. Keep draft recovery only for unsent command recovery.
4. Only after independent accepted reload, inverse, lost-ACK/restart retry and
   zero-legacy-traffic tests pass, delete popup `saveTimeline`,
   `shotCompositionAdapter.publish`, and its whole-graph fallback. Placement is
   a later independent command slice.

This report is the current readiness boundary: App can consume the reviewed
media-selection read, but popup add/swap and placement are not ready for App
capture or live-writer deletion until Agent publishes the occurrence-scoped
native artifacts above.

## Standalone parent literal add (2026-10-20)

`tl/app-m2-parent-add-capture`, based on M1 opaque-root base
`9c074972cea65c3a8352a0d0fc8672b609846ecc`, adds only
`commands/parentClipAddCapture.ts`, its unit test, and
`commands/fixtures/recipe_m2_parent_clip_add.json`. It reuses `AuthoredState`
and `MoveRecording`; shared M1 primitives, root preservation, all guards, and
the original three `it.fails` are unchanged. This is branch-only M2 work.

Native authority is Agent `tl/agt-m2-first-clip`, exact commit
`0ace5c0bd06562aac31ed84f92e8bc6e54ade834`, not the frozen R4 popup helpers.
The exported fixture contains nine exact native command/record/after-bundle
cases and 51 native refusal kinds. The first case also matches the original
Agent `tests/editing_conformance/fixtures/recipe_m2_clip_add.json` add command
and record, with standalone ordinal/cause zero. The fixture includes the
SHA-256 of that original Agent golden. It was generated and reverified using
an archive of this exact commit, with the shared Agent dependency venv and
`PYTHONPATH` pointing only at that archive.

`captureParentClipAdd(bundle, 'parent', row)` consumes a complete caller-authored
row with an already allocated explicit ID and freezes the original bundle and
command. `finishParentClipAdd(basis)` accepts only that capture (including after
JSON roundtrip); no head refresh, row override or ID allocator enters finish.
The local executor verifies original destination-track fields, collection
shape/membership/order, new-ID absence and every supplied recorder claim. It
retains unrelated row values, opaque state, absent/null secondary codecs and
retained source/transcript dependencies, and synchronizes originally equal
clip mirrors including empty mirrors. Repeated local retries preserve the same
ID; executing against an occupied ID refuses. A subsequent explicit creation
records only its own created identity and guards the preceding ordered members.

Support is **existing active parent output track, nonmedia literal row only**.
Authored `at`/`hold` seconds are not rounded. Media selector keys (even null),
media clip kinds, source windows, follow relations, occurrence owners and
unsupported timing refuse as native. No registry, media read, placement, new
track, popup, session, provider, UI, root, pin, schema or Runtime artifact was
changed. Undo/redo and accepted retry/rebase remain Runtime/Agent authority;
this does not prove live acceptance, history, popup/media/occurrence creation,
writer deletion or any broader M2 gate. Native explicit-null-speed storage
parity is retained; Runtime inspection support is not claimed.

Validation on this branch:

* `node_modules/.bin/vitest run --config config/testing/vitest.config.ts src/tools/video-editor/commands/parentClipAddCapture.test.ts src/tools/video-editor/commands/clipMoveCapture.test.ts src/tools/video-editor/commands/authoringBundle.test.ts src/tools/video-editor/hooks/useTimelineSave.draftConfig.test.ts src/tools/video-editor/hooks/useClipDrag.test.tsx --pool=threads --maxWorkers=1`: **215 passed, 3 original expected failures, 5 files passed**.
* `node_modules/.bin/eslint src/tools/video-editor/commands/parentClipAddCapture.ts src/tools/video-editor/commands/parentClipAddCapture.test.ts --max-warnings 0`: **passed**.
* `node scripts/quality/check-known-failures.mjs` and `node scripts/quality/check-no-smoke-tests.mjs`: **passed**, exactly three authorized and zero forbidden markers.
* `node_modules/.bin/tsc -p tsconfig.app.json`: **exit 2, exactly two documented baseline errors**, `RuntimeConnectionProvider.tsx:90` TS7053 and `AgentChatNewChatButton.tsx:80` TS2550; no new diagnostics.
* Native export: `PYTHONPATH=/tmp/app-parent-add-agent /home/user/work/venv-agent/bin/python /tmp/app-parent-add-fixture.py`: **nine exact native captures/records/after-bundles and 51 refusal kinds passed**. Independent supplied-command verification also passed; original native golden SHA-256 is `5e9a54e75a0901724dedd3e62c0f37f78840a8edee001f30b92306383800479b`. The temporary exact-source archive and export script were removed after verification.
* Full/browser/socket/external-service suites and installation were not run.

Earlier attempts remain diagnostic failures: a three-file default-fork run
passed 23 tests but had two worker-start timeouts; a threads retry passed the
101 neighboring tests but had one worker-start timeout; an isolated run then
exposed a BigInt `%j` test-title serialization error before collection. The
title now uses a plain text label, and the final complete targeted run above
passed without unhandled errors. No behavior expectation was weakened.

Next: retain this bounded parent adapter on its branch. The occurrence-owned
media add/swap and placement fixture requests above remain open; do not route
those writers through this operation or merge this branch into integration
without the orchestrator's M2 integration decision.

## Agent00:29 — occurrence contract delayed by reproduced shared inverse gap
Newmedia absentfromoriginalmanifest exposes converter provenance issue: afteracceptedreload+undo newpin survives althoughregistry+lastconsumerremoved, soexactoriginaldocument/revisionnotrestored. c3da1535 preserves2desiredpositiveassertionsasstrictxfails; noAppwirecapturepublishedyet. agt-m2-media-manifest-provenance fixesgenericaccepted-boundaryprovenance NOW, preservinglegacyunselectedsourcepins/newerdependents. No globalprune/preseedworkaround. Parentexistingbinding9eb24realPASS doesnotcoverthisnewcase. Appmayprepareownedrawtiming/ownerselectors butmustwaitofficialnewcapture/goldens. Bundle1labelreadyunchanged.
