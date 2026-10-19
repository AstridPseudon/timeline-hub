# App M0 contract review — current position
2026-10-19. App manager. Design review only; no Checkpoint A or product gate approval claimed.

App accepts Runtime commit-contract.md §4.1/§5 and Agent edit-command.schema.json / command-schema-handoff.md as the sole consumer contracts. Runtime owns wire/closure/port/bootstrap DTOs; Agent owns command arguments, recorder leaves and schemas. App introduces no alternate schema or request/session/rebase protocol. Full writer/deletion coverage is app-writers.md; source-to-projection and durable outbox details are app-contract-consumption.md.

## Accepted seams
- Ordinary /v1 commit, immutable media selection and publication history through main AstridRuntimeClient/door. Main receipt_id is accepted publication identity; retain revision+publication pins even when revision content repeats.
- Full CanonicalDocument (parent_revision, exact shot/internal images and dependency_manifest) provides raw accepted state for existing runtimeGraphToContract and popup projections. Display rows never reconstruct acceptance or unknown fields; no latest-child substitution. Separate accepted, current-head and local optimistic display labels.
- Initial slim provider ABI 1, exact generated digest, schema_version:1 distinct from string operation version, rationale only. Consume the generated projection of Agent's byte-identical packaged command schema.
- Minimal M1 clip.move version "1" uses `{on:<absolute timeline seconds>}`, fixed/non-ripple, preserving authored duration. Capture original guards before preview changes the row. App captures the exact Agent-published guard contract at gesture time, including occurrence/time-map dependencies and clearing an existing follow relation. M1 verifies sequential/dependent gestures through the real App capture path; the fixture adapter is insufficient. Cross-track/ripple/relative authoring stays outside this narrow M1 operation.
- Accepted inverse uses `timeline.inverse`, args `{publications:[<receipt_id>,...]}` with ordered unique explicit targets; server reconstructs guards. Historical restore is separate, sole `timeline.restore`, args `{revision_id,content_digest}`; main adapter requires both observed head guards and returns CommitAccepted. Runtime history/ABA/created-entity dependency safeguards remain required.
- Runtime verifies fresh bootstrap and existing-main baseline provenance. Null publication is readable but not an editable base; surface history_unavailable and preserve local work rather than invent provenance.

The Checkpoint A cheap wins are adopted: one authoritative recorder with executed commands derived from records, owner-defined legacy path normalization at ingress, and empty/identity-only id_map. App does not remap IDs. Runtime retains exact consumed transcript/config content; App consumes the resulting pinned inputs/capture contract rather than reading mutable latest content for replay.

Gate 6 now requires direct authenticated legacy-endpoint rejection with unchanged head/history/bytes, in addition to zero App traffic. The explicit App/Runtime M2 disposition matrix is in app-writers.md; bootstrap is atomic inside constrained empty/new createTimeline; external publishParentComposition is rejected even for first publication. Restore is a guarded command adapter; canonical snapshot/replace/render-coupled and shot/reference/item/text-binding bypasses are rejected under Runtime's complete matrix.

## Outbox and suffix decision
Reserve exact canonical route/body/key, allocated IDs and covered prefix atomically in IndexedDB before sending. ACK removes only its matched prefix; preserve newer suffix, stable realm/actor/project/timeline scope and durable independent-tab fencing. Main changed-instance fence remains until relaunch; afterward origin/credential/process instance may change while realm, actor, path/body/key remain fixed. Do not persist credentials or infer acceptance from equal current content. Storage failure blocks transmission while retaining visible local work.

Orchestrator's dependent-suffix rule is adopted: B authored on optimistic A stays unsent until A ACK; then submit B at HA with its ORIGINAL commands/value+identity/read/selection guards and a fresh request identity. The provider verifies guards at HA and alone rebases over later C. Failed guards/rejected A retain B as a conflict. Independent B on H0 stays unchanged. Relative B retains its read basis; absolute B retains its target. No new field/base_view. Equal-state ABA is allowed for this forward-suffix handoff by decision; accepted history and PLAN's guarded-undo ABA checks are preserved. Agent owns the required conformance experiment; the live App lost-ACK/restart journey remains M1 evidence.

## Remaining proof and environment
Reviewed Agent suffix experiment source/limits and final result: `PYTHONPATH=$PWD PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/m0_suffix` in agt-m0-suffix-conformance: 35 passed in 675.05s, no skips/warnings. Actual frozen R4 runner/rebase/inverse APIs are exercised; publication/idempotency/outbox storage are reduced models and JSON reload is not a browser restart. This closes App's M0 semantic review; canonical product schema/recorder implementation, real local storage/fencing/UI and live journey remain M1+ work after Checkpoint A. No outstanding App request for a Runtime DTO change.

Shared App node_modules is installed once at /home/user/work/app/node_modules. Contracts: 1/1 passed. Original npm test was interrupted without totals; completed 2-worker default baseline is 17,954 passed / 56 failed / 24 unhandled errors in 1,447 files (2,384.29s, exit1). The --net rerun of eleven permission-dependent files passed all 115 tests in 18.33s with zero unhandled errors on the reviewed listener-fix branch; all 50 selected failures recover. Six unrelated assertions in four files remain separately recorded and were not rerun. Full command/limits are in app-baseline.md. Preinstalled Chromium 141 passed explicit launch/page evaluation. tests/e2e/local/support/app.ts:22–29 already resolves it via PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers or PLAYWRIGHT_CHROMIUM_EXECUTABLE; raw default lookup alone expects absent revision 1223. No browser installation is needed. Full journey requires coordinated production build and Runtime/Agent paths; Runtime owns feasibility. No real journey or macOS result claimed.

Extension design App seams reviewed: reuse panels/inspectors/proposal review, replace numeric baseVersion/patch acceptance with command receipts, preserve unknown payloads, label findings/preview by revision. M5 registration/examples stay behind the hard stop; no new UI framework or automatic edit trigger is needed for the foundation.

## 2026-10-19 App review of first M2 ownership audit (design only; decision reconciled 22:33Z)
Reviewed m2-group-ownership.md against App dd376d5e0 and the preserved three original success tests. The fixtures start as raw parent clips with authored parent config.pinnedShotGroups rows. Orchestrator's DECIDED option A supersedes App's earlier parent-soft-tag recommendation: canonical shot ownership is the single editable representation; pinnedShotGroups is migration-only input. Migration must be recorded, guarded and lossless through the sole command path. Preserve full metadata, order, identities and unknown fields; refuse unsupported interleaving/reordering or duplicate shotId-derived identities without touching them. Existing converter and UI clone assumptions are not proof of losslessness.

App consumes a derived legacy-shaped group view with explicit canonical ownership bindings from the same accepted/local raw authoring image. Never infer ownership from display IDs or (shotId, trackId), and never persist that compatibility view as another group store. Whole-group temporal move targets occurrence placement; retrack atomically updates occurrence-owned child tracks. Stable property refs and membership/dependency guards must permit independent groups to rebase; no whole-parent/whole-array replacement for ongoing edits. Free parent/occurrence clip movement uses explicit scoped members; shared-shot edits require explicit shared intent.

Within the group slice (global priority superseded by AUDIT2216 all-writer migration): migrate one existing two-clip fixture, move to an existing lane, derive the App group view, prove preserved visible outcomes/accepted reload/exact guarded undo/independent-group concurrency. Track creation follows, then free multi-clip. Shared ordered restoration and track.create + own-move composed inverse stay Agent dependencies, retaining external-dependent and ABA protection and original allocated IDs. Preserve fixed source windows, simultaneous original reads, common row offsets, half-open contact and explicit blocked-placement refusal pending any reviewed routing policy.

All three original it.fails success expectations and exact quality-gate exceptions remain until their respective production capture→preview→commit→readback→guarded inverse behavior passes. Remove all three by M2 completion; don't claim the entire surface complete after the first existing-lane slice. Agent owns final migration/occurrence command and query schemas; App consumes the official handoff. Orchestrator22:35 authorizes M2 implementation branches; merging still waits for recorded M1. Actual M2 migration/publication/browser proof is unrun; source audit/probes are design evidence only.

## M2 priority 1: ordinary track rename ingress (App groundwork, 2026-10-19)

Audited App `9d0a383a1`, Agent `b63a89aad`, and read-only M1 safety branch
`5bec7785d`. This task is design-only; M2 merges remain held by the recorded gates.
Detailed paths, verification and the Agent fixture request are in
[the worker report](../workers/app-m2-ordinary-edit-ingress/report.md) and
[Agent handoff](../workers/app-m2-ordinary-edit-ingress/agent-handoff.md).

**Actual ingress:** desktop/touch `components/TimelineEditor/TrackLabel.tsx:230,475`
emits `{label:string}` through `TrackListRenderer` → `TimelineCanvas` →
`TimelineEditorCore` / `TimelineEditorCoreBody` → ops exposed by
`hooks/useTimelineState.ts` → `useTimelineTrackManagement.ts:900`
`handleTrackPopoverChange` → `applyEdit({type:'config',resolvedConfig})` →
`useTimelineCommit.ts:533` → `commitData` / `scheduleSave` →
`useTimelinePersistence.ts:399` → `RuntimeDataProvider.saveTimelineAtHead` →
`publishParentComposition` (`dataProvider.ts:1008`, legacy composition-revisions).
There is no `localTimelineCommand` symbol or rename method in
`useTimelineCommandsService` on this base; the shell toolbar supplies undo/redo,
not rename. A second ingress is public `TimelineOps.apply` with local
`track.update`, compiled by `lib/timeline-patch.ts:1483` and saved by
`useTimelineOps.ts:276`. Local command history is not an EditCommand attachment.

**Smallest conversion:** add one typed rename service adapter, redirect the
label-only popover branch and label-only merge-mode public patch ingress to it, and attach
Agent's captured command plus the local preview patch at the command-session
submission seam (`commands/commitSession.ts:222`, existing move pattern).
Capture before either config/patch preview mutates data; persist original reads,
identity/bindings and local predecessor with the command. Extend the session with
this bounded operation; keep `clip.move` and its capture unchanged. Preview uses
`useTimelineCommandSession`'s `save:false,skipHistory:true` path. Remove rename's
config-save branch and public patch's rename `commitData(save:true)` branch once
both emit commands. Reject unsupported mixed patch batches atomically with draft
preserved until their own operations land (replace mode also clears other fields);
never translate arbitrary patches or
drop the remaining operations. The common snapshot publisher remains OPEN for
other writers and is deleted only when the writer census reaches zero.

**Canonical target:** string `label` on an explicit `parent/track:<raw-id>`;
occurrence-local tracks require `occurrence:<id>/track:<raw-id>` and exact child
pins. The merged display track list deduplicates IDs (`shotCompositionProjection.ts:279`)
and cannot establish ownership. Start with the proven parent-owned mixed-journey
lane; require explicit bindings before child/shared cases. `displayLabel` such as
“· nested shots”, drag text and missing-label display defaults are cosmetic;
they must never become authored names. The immutable original basis comes from
`loadTimelineCommandBasis` → `authoringBundleFromDocument`, retained by the session
and advanced by recorded local commands, never reconstructed from display config.

**Agent dependency:** current native registry admits `clip.move`, `track.create`,
`timeline.inverse`, `timeline.restore`; generic envelope `op:string` admits no
additional handler. R4 `timeline.set`/`set_track(values,clear)` is donor code only.
Agent must publish the canonical operation/version, closed args/default/clear
rules, exact singleton selection/owner guards, original tagged label expectation,
recorded unchanged writes and browser/Python capture vectors. Rename is an
absolute string assignment, including empty string; null/omission/deletion are
not synonyms. Label-clear policy needs Agent confirmation (R4 refuses it), while
inverse must restore originally absent labels exactly. No created IDs, timing
intent or invented operation name is needed from App.

**Qualification:** retain the ordinary positive rename in
`useTimelineCommit.test.tsx:317` and all three `useClipDrag.test.tsx` `it.fails`
success expectations. M1 `three-products.spec.ts:1017` on `5bec7785d` currently
specifies visible refusal + exact recoverable draft (browser result unverified
here). M2 replaces that temporary endpoint-specific expectation with accepted
rename → reload retaining moved clip/opaque closure → `timeline.inverse` of the
rename publication restoring the previous label without undoing the move;
concurrent same-property/ABA writes must block inverse and keep local work.
Keep separate refusal/recovery coverage for genuinely unsupported edits. No
passing behavior is rewritten to require refusal. Same-pattern later families:
track properties/create/remove/reorder and clip scalar/clear/params/look,
then trim/split/delete/add/swap with their own Agent captures; none is widened here.

The portable cross-machine fixture is now shared at [app-track-rename-fixture-request.json](app-track-rename-fixture-request.json), byte-identical to the worker artifact. It preserves the existing parent-only App bundle/immutable document, originally ABSENT label, semantic Unicode-label input and expected tagged presence; it is NOT a new command/DTO schema or executable proof. Agent should return the official command/record/after golden in the existing recipe fixture format. Disjoint move+rename must preserve both; same label/target-owner changes conflict; inverse restores absent/present exactly and blocks intervening unchanged/ABA writes. No new IDs for this parent rename.
