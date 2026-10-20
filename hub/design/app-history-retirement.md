# App D02 history retirement recipe

Status: audit of `tl/integration` (`2bfde69ea`), plus held `d35266528`/`4cdf2b87`,
`24b9b8ede` (track-label session), and `818f24c75` (clip-delete session).
D02 remains **in-progress** until the local accepted snapshot/checkpoint path is
gone. This is a deletion recipe, not authorization to change the settled plan.

## Authority split

Keep Runtime accepted history/navigation: `useTimelineHistory.refreshCanonicalHistory`
and `restoreCanonicalRevision` (`hooks/useTimelineHistory.ts:553-609`) call
`shotComposition.listHistory/restoreHistory`; the held history UI maps
`RuntimeDataProvider.listTimelineCommits` to `GET /v1/projects/:p/timelines/:t/commits`
and strict restore to `POST .../composition-revisions/:revision/restore` with the
current revision+publication pair (`integrations/runtime/dataProvider.ts:196-247`,
`client.ts:623-672`). Keep repeated-publication identity and exact-head tests from
`d35266528`/`4cdf2b87` and the real UI journey branch.

Keep `commands/commitSession.ts:306-329`: unsent intent undo cancels only the
outbox tail and reprojects in memory; accepted undo emits `timeline.inverse` with
accepted publication IDs through the same `/v1/.../commit` outbox. Keep
`commands/commitOutbox.ts` durable pending A/B, exact request/key, recovery and
guards. Keep IndexedDB recovery drafts as crash recovery for unsent/conflicted
work, not accepted history.

## Delete after the last ordinary writer converts

1. Remove the snapshot/checkpoint branch from `hooks/useTimelineHistory.ts`:
   `persistCheckpoint` (249-280), checkpoint trim/labels/retention (96-121),
   checkpoint state/append/load (`219`, `233-238`, `527-551`), trigger counters
   and `onBeforeCommit` checkpoint scheduling (`215`, `346-367`),
   `jumpToCheckpoint`/`createManualCheckpoint` (488-525), and the toolbar fallback
   (`TimelineEditorShellToolbar.tsx:171-204`). Do not remove canonical-history
   state/effects or strict restore.
2. Remove the local accepted snapshot restore publication: the old
   `restoreHistoryEntry` path (`useTimelineHistory.ts:303-321`) must not call
   `commitData(..., { save: true })` for an accepted edit; accepted undo is the
   command session. Retain only the minimum native snapshot needed to cancel an
   unsent gesture B in memory; it must be bounded to unsent state and must never
   POST a snapshot or represent accepted history.
3. Remove the legacy command-history bridge once every producer uses the command
   session: `useTimelineState.ts:1022-1032` (`commandHistory`), the matching
   `CommitDataOptions`/event payload, and `useTimelineHistory.ts:123-201`
   (`buildCommandHistoryEntry`, collapse/merge, and snapshot-backed accepted
   undo). Do **not** delete command-runner inverse generation until its remaining
   unsent-preview consumers are replaced; any retained inverse is memory-only.
4. Remove checkpoint plumbing from `DataProvider.ts:496-497`,
   `useTimelineOps.ts:39-45,70-77,122-141,287-375`, and App history state
   wiring (`useTimelineState.ts:421,464-466,499-501,746-771,1265-1267`,
   `useTimelineState.types.ts:252-254`, `timeline-state-types.ts:73-75`,
   `timelineStore.ts:398-400`). Update the public SDK TimelineOps contract only
   in its owning task; do not leave a second checkpoint stack in App.
5. Remove checkpoint fields/methods from the browser/in-memory provider only
   after its tests are converted (`lib/browser-runtime.ts:64,76,93,148-167`).
   The Runtime compatibility test already records the intended absence
   (`testing/__tests__/providerCompatibility.runtime.test.ts:121-132`). Do not
   confuse Runtime recovery `checkpointAttempt` with timeline history.
6. The old Supabase schema (`supabase/migrations/20260326100500...`) has no
   current caller/RPC. Do not rewrite the applied migration; after zero-traffic
   proof, add the normal forward migration to drop `timeline_checkpoints` and its
   policies/index. This is cleanup of the old durable store, not a new history API.

## Dependencies and replacement proof

Do this only after ordinary editor, media add/swap, popup, placement, transcript,
element, visual-seam, and remaining producer paths have accepted command coverage
or are deleted. Before the cut, each migrated producer must fail if it calls
`saveTimeline`, `saveTimelineAtHead`, snapshot `publishParentComposition`, or a
Supabase config-replaced route; popup add and swap need separate zero-traffic tests.

Replace old checkpoint/snapshot positives with: (a) unsent A/B cancel/reproject
does not call a save or Runtime publication; (b) accepted A undo sends exactly one
guarded `timeline.inverse`, survives reload, and refuses after an intervening
accepted write; (c) Runtime history shows repeated revision IDs by distinct
publication IDs and marks exactly one exact current pair; (d) strict restore uses
the Runtime adapter and readback closure. Preserve all existing positive journey
assertions by changing their expectation to accepted Runtime behavior; do not
delete or weaken them.

Static cut estimate: about **340 App product lines** are directly checkpoint/
accepted-snapshot plumbing across the hook, TimelineOps adapter, state/UI wiring,
provider contract, and browser test provider, excluding tests and the retained
native unsent snapshot/outbox. Exact line ranges above are the cut inventory;
the applied migration is not counted as deletable history.
