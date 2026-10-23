# P1 live-cause review handoff — 2026-10-23

Independent review of Sol0614 is complete against App `f98a5060e`, frozen Agent `f894c3c9…`, and frozen Runtime `34eac004…`.

## Findings

1. **A — PASS.** The original order enables the Agent authoring profile before `seedOneClip`. Runtime’s verified legacy import is startup-only, so the newly seeded legacy publication is outside the import set. The later history read invokes `_ensure_timeline_commit_baseline`, which calls `TimelineCommitStore.head` for the null publication and refuses the request. Frozen source identifies the refusal class as `history_unavailable`; live 19451 retained only the 409 status, so this is a source-established explanation, not a captured live response reason.
2. **B — PASS.** Frozen Runtime inspection emits `head_revision_id` but omits `head_publication_id`. App `RuntimeDataProvider.readTimelineInOrder` maps the absent optional field to null, while the original-basis/local-save production check requires a matching revision/publication pair. That mismatch refuses before owner creation.
3. **Selection — not a product finding.** The false selection boolean comes from querying `video-editor-provider`/`data-timeline-id`, a marker present in the test mock but absent from production. It cannot establish wrong timeline selection.

## Live limits

Both original 19451 cases failed before split at the unchanged 90-second owner wait. No claim is made about displayed error text, the exact live 409 reason, or downstream chain assertions. The offline witness source/log named by Sol (`/tmp/w-0ff1a2012c/cause.test.tsx`, `witness-final.log`) had been cleaned up and was unavailable for rerun; Sol’s retained packet reports its four real-hook tests PASS. No browser, HTTP/socket/service/build/full-suite rerun occurred.

## Owner packets

- **A → App2/P1 fixture owner + Runtime review:** exact reproduction is `enableTimelineAuthoring → seedOneClip` legacy publish → `openChain` → `loadTimelineCommandBasis` → history list → `_ensure_timeline_commit_baseline` → `TimelineCommitStore.head`, using Agent `f894c3c9…` and Runtime `34eac004…`. Preserve the scenario and do not synthesize a publication or move import into a read.
- **B → App lane + Runtime contract coordination:** exact reproduction is App `loadTimeline → readTimelineInOrder → inspectCanonicalTimelineHead` with the frozen Runtime inspection shape, followed by `readTimelineOriginalSaveBasis` and the head-pair check. App consumes the pair; Runtime owns any producer-contract change.

No H3/P1 behavioral credit is earned. All original positive assertions and the complete v2 scope/base/commands/label/steps/reads/merge/dry-run/key, accepted/merged/canonical/head/digest/receipt/effects/bindings/dependencies/history, conflict/invalid, owner wait, lost-ACK/restart/retry, guards, raw/opaque/order, rollback, and undo coverage remain untouched.
