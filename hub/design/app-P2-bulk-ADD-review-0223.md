## A — FAIL

Reviewed exact source `24c9ba0d0e` (`PropertiesPanel.mounted.test.tsx`, blob `cbb4b598...`).

The production callback path is real through selection, `BulkClipPanel`, edit persistence, outbox, and held `commitTimeline`. However, the fixture is not the retained canonical fixture:

- `native-none` includes opaque/source fields omitted by the test.
- `f2-app-clip` has extra transition fields; the test replaces them with a simple transition.
- `f2-transition-clip` is canonical `crossfade/.5`; the test changes it to `fade/.75`.
- Tracks, registry metadata, and sibling opaque fields also differ.

This violates the exact-fixture requirement. I did not apply the delta, run acceptance, or request merge. Normal receipt: not requested; A failed before application.

Checks:

- `git -C /home/user/banodoco/reigh-app diff --check 24c9ba0d0e^ 24c9ba0d0e -- .../PropertiesPanel.mounted.test.tsx` — pass.
- Own worktree remains clean.
- No tests run because the source gate failed; no browser/full suite requested.

## B — Readonly investigation

Retained run `app-pin-24865fa2-p2-d88b-add-0213-1025021543-3964`: readiness passed; original failed at popup assertion line 892 after the 5-second wait.

The expected projected label is source-derived. `ShotTimelineMediaControls.tsx` reads `useTimelineMultiSelect(runtime.agentSelectionOwner)`, and the mounted pointer-selection producer in `useClipDrag.ts` also uses that owner.

No causal divergence is independently proven from the retained DOM/evidence. The unavailable fact is the post-click owner-scoped selection state/identity; no live rerun was performed. Therefore I recommend no source remedy from this review.

`design/commit-v2.md` was absent from the searched repositories; no substitute was modified. Commit message and `DONE` marker were created.