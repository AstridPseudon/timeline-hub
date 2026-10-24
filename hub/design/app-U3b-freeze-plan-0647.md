# U3b freeze-plan report

Plan-only PASS. No product files, refs, merges, commits, or tests were changed/run. `DONE` marker created.

Refs verified:

- Current integration: `9b810408cc`
- Held draft: `7fc54e1f95ce`
- Draft/main base: `65c1771b78ab`
- Local `origin/main`: `2a288e629c47` — exact expected tip
- Live `ls-remote` refresh remains mandatory immediately before merge by the lead.

Upstream delta: 18 commits, 111 paths, `+3900/-1357`:

- 76 modified, 25 added, 9 deleted, 1 rename.
- Main areas: onboarding/reload flow, task panel, Runtime connection/restart handling, chat selector, tour cleanup, local workspace/service-worker behavior.
- No `supabase/**` changes and no extension implementation changes in this delta.
- Upstream deletes the four tour media assets, `tourFlag*`, `tourRecord*`, and renames `useEditorTourTrigger.ts` to `useIsDesktopEditor.ts`.

Merge previews:

- Held draft vs current integration: five overlapping paths:
  - `src/tools/video-editor/hooks/useTimelineCommit.ts`
  - `src/tools/video-editor/lib/timeline-data.ts`
  - `src/tools/video-editor/lib/timeline-data.test.ts`
  - `tests/e2e/local/support/app.ts`
  - `tests/e2e/local/support/harness.ts`
- Only one textual conflict appeared: `tests/e2e/local/support/harness.ts`.
- Current integration vs refreshed main: 22 changed-in-both paths plus added-in-both `supabase/functions/_tests/mocks/groqSdk.ts`; 10 conflict hunks across nine files, primarily package/test plumbing, AgentChat, `useTimelineCommit`, and the Runtime harness.

Recommended order:

1. After P2/P3 GO, lead refreshes all refs and verifies `ls-remote` equality.
2. Merge the held U3b draft onto current integration, retaining its reviewed diagnostic delta but not treating its stale editor tree as authoritative.
3. Merge refreshed App main last, so upstream editor/onboarding/tour behavior wins.
4. Resolve ordinary conflicts with Luna; escalate only actual semantic contradiction to Sol.
5. Preserve current outbox/transport, Runtime door lifecycle, prepared-media basis, raw/opaque clip preservation, reviewed caller fixes from `69099d6db7`, and dormant D31/D37 implementation/tests.
6. Re-vendor `astrid-browser` only after the actual merged Agent exists, through the normal provenance-generating tool. Bundle D39 client/schema/producer adoption once; do not churn pins.
7. Continue with Runtime final tuple, U4p, targeted checks, original P1–P3/F gates, then authorized full/browser Farm runs.

Cloud/dev-extension decisions remain unchanged: retain the current retirement of `ai-timeline-agent`, `timeline-import`, and `astridAppendService`; retain `complete_task`/billing compatibility. Do not resurrect deleted `NewChatMenu`, `TourChatPanel`, old tour manifests, or retired extension/test routes.

Proposed acceptance checks:

- Targeted Vitest for `timeline-data`, `useTimelineCommit`, `timelineLocalSaveHandoff`, `useTimelinePersistence`, `useTimelineSave`, diagnostics, outbox, Runtime client/data provider/operation host, bootstrap, and local adapter tests.
- Node lanes for `p1-diagnostic-safety`, `mounted-readiness-safety`, and the existing seven-file support cohort.
- App/Node/root `tsc --noEmit --incremental false`.
- Scoped ESLint with `--max-warnings 0`.
- `git diff --check`.
- Source checks for retired writers/routes, exact v2 request fields, `Idempotency-Key`, accepted/merged/rebased/preview/conflict/invalid replies, canonical document/digest/id-map/history/undo fields, and Runtime door authorization.
- Playwright discovery only before Farm execution: P1=2, P3=1, P2=8, mounted-readiness=1.
- Full/browser/live gates only through the authorized central service/Farm, one full suite at a time.

Unverified: actual merge resolution, live ref refresh, Agent vendoring/provenance, full suites, browser bodies, and Farm gates.