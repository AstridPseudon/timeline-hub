# P2/A2 parent12208 source disposition

## Result: PASS, bounded — `causeUNKNOWN`

Actual12208 safely proves only a pretransport boundary:

- Exact tuple: App `24865fa…`, Agent `6386c7…`, Runtime `6634a1…`, Composition `635f4d…`.
- Retained packet: 245 records, 22 POSTs, zero intended commit POSTs; only handshakes and 16 inspect requests, all HTTP 200.
- Runtime ordinals 1/2 are explicitly unattributed setup activity.
- The 90-second wait is a Playwright ceiling, not Runtime duration.

This does not identify the local guard, event, hit target, or capture substage. The historical 0511 fixture facts (`181→341`, `f2-app-clip`, refusal strings) are not actual12208 evidence and are excluded.

## Source comparison

- `lib/timeline-data.ts` and `hooks/useTimelinePersistence.ts` are byte-identical between actual `24865fa…` and current `2d25dc…`.
- Therefore ancestor `5e242c64e3` cannot establish actual12208 causality.
- The later reviewed `2d25dc…` change is isolated to `hooks/useTimelineCommit.ts`: it preserves authored clip extension fields during row materialization (`useTimelineCommit.ts:203–224,341–350`). This is the smallest source-linked repair proposal, but remains source inference; no actual12208 trace proves that path caused the failure or that this repair fixes it.
- Caller fidelity is otherwise intact: pointer basis (`useClipDrag.helpers.ts:344,369–385`) → move (`useTimelineTrackManagement.ts:468–541`) → `applyEdit`/save scheduling → persistence capture/defer (`useTimelinePersistence.ts:1013–1117,1335–1346`) → outbox dispatch (`commands/commitOutbox.ts:464–491`).

The same-tuple `5678` PASS proves the general A2/outbox/commit path for transition-clear, not parent-move attribution.

## Missing retained input

Before naming a substage, safely export from existing retained raw evidence, if available:

- pointer coordinates and DOM target;
- clip ID, track, duration, and canonical source identity;
- whether `applyEdit`, `localCommit`, scheduling, capture, handoff, intent reservation, and dispatch occurred;
- the exact safe capture/handoff outcome code/message.

No new collector, replay, body export, or product/test change was made.

## Verification

- `git diff --quiet 24865fa212 2d25dc460c -- lib/timeline-data.ts hooks/useTimelinePersistence.ts` — pass; identical.
- `git diff --check` — pass.
- No tests or browser/full suites run; this was a read-only bounded comparison.
- Worktree clean. `DONE` and commit message created.