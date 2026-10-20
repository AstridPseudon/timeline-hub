# App canonicalTiming serialization boundary audit

**Audit complete; serialization isolation is NOT currently satisfied. No implementation or merge recommendation for a cap field.** General clip serializers, snapshot editing, recovery drafts and the legacy publication adapter retain the entire derived `clip.app.canonicalTiming` container. The popup's existing strip seam removes the complete container, including an injected candidate scalar, from its reconstructed child timeline, but still stores the unstripped config in its recovery slot. The seam also deletes same-named raw authored values indiscriminately. Native clip.move keeps projected view hints out of its raw command capture and persisted UNSENT intent; that separation must be retained.

Audited source: `/home/user/work/wt/app-m3-canonical-timing-serialization-audit`, HEAD **b1ef4b9b910ba72375c34cf319692f90d22edc25**. All source references below are relative to that worktree. Read `ORCH/PLAN.md` first, including the existing canonicalTiming scalar decision and stored4000 policy. Owner/Viewing carrier approval remains outside this audit; no new DTO, scalar declaration, field implementation, renderConfig authority, pair launch or policy change. Reports/probes exist only under the assigned ORCH design/worker paths. The repository remains clean.

## Proven findings

1. `lib/serialize.ts:22–89` calls `sanitizeTimelineClipSnapshot`, which allowlists clip fields but treats `app` as an opaque object. `lib/timeline-domain.ts:2444–2482` clones all app members. `serializeClipForDisk`, `serializeForDisk`, `serializeResolvedTimelineEdit`, `serializeTimelineConfigSnapshot` and `serializeTimelinePair` all retain existing timing fields **and** a private injected `__auditStoredOccurrenceCapMs: 4000`. No scalar-specific production field was added.
2. The smallest existing **whole-container strip** is `tools/travel-between-images/components/shotTimelineDataProvider.ts:135–150`, `createCanonicalTimeline`: `Object.fromEntries(Object.entries(clip.app).filter(([key]) => !['canonical', 'canonicalTiming'].includes(key)))`. It also removes `assetEntry` and reverses the occurrence ID prefix. The probe exercises it through exported `projectShotTimelineDraftComposition`, rather than duplicating its filtering code. Arbitrary contents, including the private scalar, are absent from the resulting child timeline. Other app entries, own `__proto__`, null and array order survive; original graph bytes remain unchanged.
3. That seam is **not** safe for arbitrary raw authored input: it unconditionally removes both names, even when they are unknown user data with no derived provenance. A private probe supplies such an app object, observes deletion in the child timeline, and verifies the original object is unchanged. Do not promote this implementation into a universal raw serializer blacklist.
4. Popup publication `shotTimelineDataProvider.ts:446–545` uses that strip for its candidate graph, then writes **`config: nextConfig`** at lines 510–516 into `astrid.timeline-drafts`. A real adapter path with an in-process rejecting publish callback proves: stored `draft.config` **contains** the candidate; stored `draft.canonicalPublication` **does not**. A sanitized publication candidate is insufficient evidence for sanitized recovery storage.
5. Runtime legacy scoped save `integrations/runtime/dataProvider.ts:907–1020` strips `output` only. `reconcileParentClips` at 1791 merges each submitted clip over its immutable base and preserves its whole app. The candidate supplied only in the edited config reaches **both** `parent_composition.clips` and `parent_composition.config.clips` at the generated transport boundary. The probe starts with a marker-free base and returns an in-process 409 after recording the request. Refusal is not payload sanitization and is not evidence of durable Runtime acceptance.
6. Native move uses retained raw bytes. A real session probe injects the candidate only into `env.current().resolvedConfig.clips[0].app.canonicalTiming`, captures/submits the move and disposes before dispatch. Its durable UNSENT intent has **no** candidate, no pending request, and no HTTP commit. Explicit recovery then sends one commit without the candidate. A separate raw-authored-input probe preserves same-named unknown values in the intent's before/after bundles and original display closure. Persisting those authored inputs is required crash recovery, not a derived-config leak.
7. Runtime command transport is not a sanitizer either. `RuntimeDataProvider.commitTimeline:678` checks scope/base, then forwards the request; `generated.ts:175` JSON-encodes it with a nonfinite-number guard. A private clip.set-shaped command containing `args.values.app.canonicalTiming` reaches transport intact before an injected 422. This demonstrates producer responsibility, **not** semantic acceptance of that command. Existing native move/label captures must continue to use raw bases rather than serialize projected app values.

`lib/` above means `src/tools/video-editor/lib/`; `commands/`, `hooks/`, `data/` below mean the same video-editor root unless prefixed otherwise.

## Actual flow and all relevant consumers

| Boundary / consumer | Current behavior and leak exposure |
|---|---|
| `data/shotCompositionProjection.ts:395–437` | Child view producer spreads raw `app`, then overwrites `canonical` and `canonicalTiming` with derived objects. Existing timing keys are sourceOffsetMs, speed, gain, muted, durationMs, occurrenceStartMs, occurrenceDurationMs. Raw same-named data remains in the pinned source graph, although hidden by the view overlay. Parent clips at 551–565 are forwarded separately and can retain genuinely authored same-named values. |
| `hooks/useTimelineCommandSession.ts:82–106,128–145` | Load, accepted ACK and recovery project verified raw closure/graph into ONE displayed config, run preview patches, attach the separate `TimelineData.editProjection` fact, then commit with `save:false`. That displayed config contains derived hints. The display/revision fact does not sanitize clip app. Initial/adopted and recovered command previews remain viewing consumers. |
| `lib/timeline-data.ts:201,227,271,351,377–401,428–473` | `configToRows` puts the app in ClipMeta; `rowsToConfig` copies it back; assembly keeps supplied config and resolvedConfig. A private row round-trip retains the candidate in the returned config. `TimelineData.config` is therefore not proof of raw authorship. Stable signatures can also include view hints copied here. |
| `lib/serialize.ts:22,34,77`; `lib/timeline-domain.ts:2444,2696,2721` | All five serialization entrypoints retain whole app. Disk removes output/assetEntry/closed-field extras; that does not strip derived timing. Domain snapshot serializers are also used for display and must not lose viewing hints through an indiscriminate fix. |
| `commands/runner.ts:223–290` | Resolved-config effects call serializeResolvedTimelineEdit; rows use rowsToConfig; config/data effects accept their config directly after validation. Derived metadata can become the next config through every route when supplied there; private resolved-effect and rows probes confirm retention. |
| `lib/timeline-mutation-engine.ts:86,141,210`; `hooks/useTimelineCommit.ts:300–339,416–548` | Row and resolved-config mutation paths share the above serializers; direct config/TimelineData paths bypass disk serialization. `commitData` removes stale editProjection facts, not canonicalTiming. Snapshot-write blocking during pending commands is a concurrency guard, not a metadata strip. |
| `hooks/useTimelineOps.ts:281–302` | Label-only updates use the raw command port. Other unmigrated operations still commit compiled snapshot data. Do not infer all editing paths are raw just because native move passes. |
| `hooks/useTimelinePersistence.ts:649–670,950–1009,1028,1474` | Actual snapshot save clones `scheduled.data.config` for provider calls; draft creation clones `nextData.config` or calls recoveryConfig.snapshot, then immediately schedules saveTimelineDraft before debounce/persistence checks. Save-as-copy/conflict recovery calls the same draft creator. Neither save nor draft creation sanitizes clip timing. |
| `hooks/useTimelineSave.draftConfig.ts:12–27` | Retains scoped opaque raw roots, then snapshots `{...config, ...sameBaseRoots}`. Clips/app are display fields and excluded from retained raw roots. It neither strips derived clip timing nor retains the overwritten raw app counterpart. Its private round-trip into the real draft store retains the candidate. |
| `data/timelineDraftIndexedDb.ts:111–230` | `createDraftRecord`, saveTimelineDraftIfOwner and saveTimelineDraft store supplied draft objects without field filtering. Load/reconcile/advance/clear operations are ownership/base mechanisms, not metadata stripping. Do not mutate this general store to guess which JSON keys are derived. |
| `hooks/useTimelineSave.ts:198–235,290–325` | Reloads persisted config into buildTimelineData, remembers roots and retries using the original base. A stored derived hint is not cleaned here. Sanitizing only the network adapter would leave the storage/recovery leak. |
| Popup `ShotTimelinePreview.tsx:56–120`; `shotTimelineDataProvider.ts:100–132,411–417` | Initial popup data takes projected clips as config; shot-local rebasing and preview-duration updates spread the whole timing object, so a future scalar would survive these view copies. They are not authored-output seams. |
| Popup `shotTimelineDataProvider.ts:219–253,446–545` | Draft composition and publication candidate both use createCanonicalTimeline: whole derived containers removed from reconstructed child timeline. Publication recovery still stores nextConfig unchanged. `loadTimeline:337–381` rehydrates that config. Raw same-name deletion risk applies at this seam. |
| `data/shotCompositionEditor.ts:223,466–480` | updateCanonicalShotTimeline/updateCanonicalShotRevision accept the supplied child timeline and embed it; no additional derived app strip. Popup currently cleans first; other callers cannot assume the editor function sanitizes them. Source-only inspection here. |
| `commands/authoringBundle.ts:108–124,222`; `commands/commitSession.ts:14,42,236,259,299,381–401` | Raw accepted closure is cloned into authoring bundles; original `_runtime_document` is retained. Durable intent includes commands, before/after, preview PATCH and displayBasis (raw closure/graph). displayBasis is not the derived resolved config, despite its name. Both move and track-label ports capture from retained bundle; label path is source-traced and covered by existing session tests, not separately injected in this audit. |
| `commands/commitOutbox.ts:67–104,211–225,255–285` | IndexedDB `astrid.command-outbox/owners` preserves finite JSON, including UNSENT payloads, and later exact pending body/key and accepted result. It strips no timing name. Correct native separation keeps view hints out; a contaminated producer would be durably contaminated. Never scrub historical intent/request bytes or change exact retry identity here. |
| `commands/commitSession.ts:143–158` → `integrations/runtime/dataProvider.ts:678` → `client.ts:614` → `generated.ts:175` | Wire picks **commands only**, not payload.before/after/preview/displayBasis. Captured move writes are positional, label writes are label-only. Generic transport forwards app if another producer explicitly includes it. No field-based sanitizer exists. |
| Legacy `integrations/runtime/dataProvider.ts:877–904,907–1020,1791–1842`; `generated.ts:161` | Numeric save refuses for provenance; scoped save reconciles clips, duplicates them coherently in config/top level, JSON-serializes and calls publication. Neither early provenance checks nor later tracked-timeline refusal prove sanitation. Private transport probe establishes both copies are contaminated before refusal. |
| `hooks/useTimelineHistory.ts:83–93,249–272`; `lib/browser-runtime.ts:112–158` | Snapshot undo/checkpoints clone the supplied config, and InMemoryDataProvider save/checkpoint stores it unfiltered. These are additional config recipients, not durable Runtime command history. RuntimeDataProvider implements no saveCheckpoint; no claim of a Runtime checkpoint leak. Source-inspected, not injected. |
| `lib/canonicalRenderBounds.ts:23–63`; `compositions/VisualClip.tsx:701`; `data/portableVisualSeamIntent.ts:69` | Read the existing view timing; bounds helper spreads clip/app. Viewing is allowed to retain derived hints. These are not sanitizers, storage or raw command producers. No cap semantics were changed. |
| `hooks/useRenderState.ts:889,1153`; `lib/renderRouter.ts:851–884,944–980` | Intermediate render payload contains the view timeline, and external/browser exporter receives it as evaluation input. The current managed Runtime admission builds selector/canonical pins and does **not** forward clip arrays. Thus no current managed-render clip wire leak is claimed. An external exporter serializing the provided timeline would need an explicit boundary review; not exercised here. Compile-only output snapshot at useRenderState:1303 contains counts/IDs/fps/resolution, not clips. |

`canonicalShotViewModel.ts:80` is a different value: raw shot revision timing copied onto a legacy Shot view model; not the clip app container. No other production reference to the literal `canonicalTiming` strips it (`rg` across `src`); the popup seam is the only exact-name strip found. Generic opaque structures nested elsewhere must not be recursively filtered by key name. The unused sync-ledger storage helper has no production saveKeepBothArtifact caller and is not an actual config recovery path here.

## Smallest later repair and permanent test targets

The exact reusable stripping behavior already exists at **`src/tools/travel-between-images/components/shotTimelineDataProvider.ts:135–150`**, inside createCanonicalTimeline. Remove the entire *known derived overlay* there/at equivalent projection-to-authored exits, never just the candidate member or today's list of timing keys. That behavior must cover both final authored payloads and recovery configs; sanitizing only the candidate graph leaves the proven popup storage leak.

There is **no already-safe universal raw strip seam**. `sanitizeTimelineClipSnapshot` is the central lexical serialization seam, but receives raw authored objects and display snapshots alike. `cloneAppExtension` deliberately preserves opaque data, and `serializeTimelineConfigSnapshot` also powers rows/display. Globally stripping these names there would both erase raw unknown data and risk removing the carrier during display/local preview updates. Shape matching on `app.canonical` is also insufficient: raw unknown data can use the exact same shape.

Use the existing verified raw closure/clip identity to distinguish the derived overlay and restore same-named raw authored app entries at a deliberate view-to-authored boundary. The existing optional `authoredConfig` argument to serializeResolvedTimelineEdit currently restores only the opaque registry root; callers often supply `current.config`, which can itself be a projected config. **Do not treat that parameter as automatically verified raw source.** Likewise recoveryConfig retains only opaque roots, so it cannot currently restore overwritten raw clip app data. Retained command bundles/pinned raw child graphs provide the real original bytes. This is a concrete input/provenance constraint for the later implementation, not a proposed new public DTO, side authority or storage layer.

Recommended permanent test changes (not implemented in this read-only task):

| Existing target | Required assertion for later implementation |
|---|---|
| `src/tools/video-editor/lib/serialize.test.ts` | Known projected clip → disk/edit boundary omits the entire derived container (with an injected unknown member); raw same-name authored object survives byte-for-byte. Existing closed clip/root validation, output/assetEntry removal, root registry restoration, null/order/prototype keys and explicit own transition:undefined remain unchanged. |
| `src/tools/video-editor/lib/timeline-data.test.ts`, `commands/runner.test.ts`, `lib/timeline-patch.test.ts`, `hooks/useTimelineCommit.test.tsx` | Rows/resolved/config/data paths retain timing for view evaluation but produce clean authored outputs using verified raw identity, preserving original same-name app values. Reorder/delete/add must use identities, not array indexes or occurrence-prefix heuristics alone. |
| `src/tools/video-editor/commands/commitSession.test.ts`, `commands/commitOutbox.test.ts`, `hooks/useTimelineCommandSession.projection.test.tsx` | Inject hint only in installed view; native move **and label** must exclude it from raw captures, UNSENT before/after/displayBasis and pending wire while preserving raw same-name unknown data. Cover dispose before send, lost ACK, A/B dependent suffix, exact retry, restart and recovery; never rewrite existing intent bytes. |
| `src/integrations/runtime/dataProvider.test.ts` | Record actual scoped legacy POST before a refusal; assert both clip copies sanitized only when derived. Numeric/head/tracked refusal alone is insufficient. Preserve unknown raw fields, coherent duplicate clips, authored order and explicit transition None. Also inspect actual generic command wire after producer sanitization. |
| `src/tools/video-editor/hooks/useTimelineSave.draftConfig.test.ts`, `hooks/useTimelineSave.recovery.persistence.test.tsx`, `hooks/useTimelinePersistence.test.tsx`, `data/timelineDraftIndexedDb.test.ts` | Verify the real scheduled durable draft, not only a helper return or network payload; raw unknown data/bundle/opaque roots retained at the original project/timeline/revision/publication pair. Retry/reload/save-as-copy reproduce intent without storing derived app timing. Generic store should preserve supplied authored JSON. |
| `src/tools/travel-between-images/components/ShotTimelinePreview.test.ts` | Spy publish AND inspect the real persisted draft while publish is rejected/ACK lost: both authored candidate and durable config must be clean; raw counterpart preserved. Keep current head/owner/ACK-race behavior and view-only local-duration timing positives. |
| `src/tools/video-editor/data/shotCompositionProjection.test.ts` | Pin original raw app collision, verify projection overlays it only for display, source graph is unchanged, and reconstruction preserves raw authored content. All projector entry paths continue to supply the viewing carrier coherently; carrier review is a separate gate. |

Future tests must assert the intended clean boundary. The private diagnostics below intentionally assert **current leak observations** and must not be copied as passing product acceptance expectations. No existing passing behavior test was changed, skipped, deleted or weakened.

## Exact commands and results

Working directory for every command: `/home/user/work/wt/app-m3-canonical-timing-serialization-audit`. Node **v22.22.0**, private Composition **0.0.12** at `/tmp/app-coherent-deps12/node_modules/@banodoco/timeline-composition`; existing dependency tree treated read-only. The private config imports this worktree's normal Vitest config, aliases public12/React peers to private12, adds the ORCH probe file, and points cacheDir under this worker's notes. All runs use runner config loading and no cache. No install, shared dependency/cache/venv mutation, build, tsc, browser, live socket, full suite or central pair launch.

For reproducibility below:

```sh
N=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-canonical-timing-serialization-audit/notes
```

Initial diagnostic run:

```sh
node /tmp/app-coherent-deps12/node_modules/vitest/vitest.mjs run \
  --config "$N/vitest.config.ts" --configLoader=runner --no-cache --maxWorkers=1 \
  "$N/serializationAudit.test.ts"
```

**Exit0, 1 file / 13 diagnostic tests passed, 2.81s**, `notes/probes.log` (before adding popup durable-publication and generic-command-wire probes).

Initial repository neighbors (worktree node_modules still pointed to shared App dependencies):

```sh
node /tmp/app-coherent-deps12/node_modules/vitest/vitest.mjs run \
  --config "$N/vitest.config.ts" --configLoader=runner --no-cache --maxWorkers=1 \
  src/tools/video-editor/lib/serialize.test.ts \
  src/tools/video-editor/lib/timeline-domain.test.ts \
  src/tools/video-editor/lib/timeline-data.test.ts \
  src/tools/video-editor/commands/commitOutbox.test.ts \
  src/tools/video-editor/commands/commitSession.test.ts \
  src/tools/video-editor/commands/authoringBundle.test.ts \
  src/tools/video-editor/hooks/useTimelineSave.draftConfig.test.ts \
  src/tools/video-editor/data/timelineDraftIndexedDb.test.ts \
  src/tools/video-editor/hooks/useTimelineSave.recovery.persistence.test.tsx \
  src/integrations/runtime/dataProvider.test.ts \
  src/tools/travel-between-images/components/ShotTimelinePreview.test.ts
```

**Exit1, 8 files passed / 2 failed; 283 tests passed / 20 failed, 22.00s**, `notes/targeted.log`. All 20 failures were invalid hook calls: tested code used private React while @testing-library's Node import used shared ReactDOM. `timeline-domain.test.ts` does not exist and selected no tests; no coverage is claimed for that selector.

Corrected private runtime setup changes ONLY this assigned worktree's root symlink temporarily, restoring it in an EXIT trap; it changes nothing inside either dependency tree:

```sh
original_deps=$(readlink node_modules)
trap 'ln -sfn "$original_deps" node_modules' EXIT
ln -sfn /tmp/app-coherent-deps12/node_modules node_modules
node /tmp/app-coherent-deps12/node_modules/vitest/vitest.mjs run \
  --config "$N/vitest.config.ts" --configLoader=runner --no-cache --maxWorkers=1 \
  "$N/serializationAudit.test.ts" \
  src/tools/video-editor/hooks/useTimelineSave.recovery.persistence.test.tsx \
  src/tools/travel-between-images/components/ShotTimelinePreview.test.ts
```

**Exit0, 3 files / 50 tests passed (15 diagnostics + 35 unchanged repository tests), 9.20s**, `notes/probes-and-react.log`. Both previously affected suites pass completely. The other 8 repository suites passed in the initial run; this establishes the selected 303 unique repository tests across corrected/initial runs, not one full-suite claim.

Finally strengthened the private legacy probe so its immutable base has no candidate and only the incoming edit has it; no product/test-repo changes. Using the same temporary root-symlink setup:

```sh
node /tmp/app-coherent-deps12/node_modules/vitest/vitest.mjs run \
  --config "$N/vitest.config.ts" --configLoader=runner --no-cache --maxWorkers=1 \
  "$N/serializationAudit.test.ts"
git diff --check
git status --short
readlink node_modules
```

**Exit0, 1 file / 15 diagnostic tests passed, 2.71s**, `notes/probes-final.log`; `git diff --check` and status confirm no repository changes; root link restored to `/home/user/work/app/node_modules`. No worktree build/temp output remains. The probes use repository fake IndexedDB and injected in-process transport, not a real Runtime, server or browser. These passes do not establish native pair acceptance, rendered pixels/audio, cap delivery or sanitization after a future repair.

## Disposition

No task blocker: the requested read-only audit is complete. Findings block claiming the conditional scalar is nonserializing today; they do not reverse the stored4000 decision. Orchestrator should send the concrete stripping/storage and raw-collision findings to App + Viewing before authorizing implementation. Later work should repair the explicit boundaries, add the permanent assertions above, retain raw command recovery exactly, then qualify the authorized carrier/pair separately. No KEEP marker or mergeable product patch is supplied.
