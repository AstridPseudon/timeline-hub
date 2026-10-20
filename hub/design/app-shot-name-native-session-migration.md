# App shot name native-session migration

## Scope

This change migrates only the embedded canonical `ShotEditorView` name edit. It uses the mounted parent timeline command session and its existing durable outbox. Settings persistence, standalone canonical routes, legacy shots, wire DTOs, and pin/reader contracts remain unchanged.

The UI continues to trim and require a non-empty name. The native command helper intentionally preserves the Agent contract, including acceptance of an empty string; Runtime payload validation remains the separate authority for that discrepancy.

## Source and ownership

- Agent reference: `d8749a9ce12a699672faf3ad96b4e4cbea9245c2`, `_shot_commands.py`, `ShotSetArgs`, and `test_recipe_shot_set.py`.
- App basis: current `TimelineCommandBasis` / `authoringBundleFromDocument` from the mounted `useTimelineCommandSession`.
- Target identity: `occurrence:<raw-occurrence-id>/shot`, captured from the explicit embedded occurrence. No projected clip/group ID or default timeline is used.
- The capture records the raw occurrence read, raw source shot pin, exact root-name guard, occurrence binding, and direct payload write. It mutates only `payload.name`; `settings`, `provenance`, unknown fields, and source mapping remain untouched.

## Tree and binding

`createTimelineCommandSession` owns `shotSetPort`, alongside the existing clip and track ports. `useTimelineCommandSession` applies the same legacy-clean fence. The port is exposed through `TimelineEditorOpsContextValue`, selected by the mounted `AstridTimelineEditor`, and passed through `LocalTimelineShotBrowser` to `ShotEditorView`.

Name editing captures before the inline editor opens. Finish uses the original capture and the normalized UI string, then submits to the same session/outbox. Missing or stale authority refuses visibly and leaves the editor draft in place. The old canonical name publisher remains only for routes without this mounted port; it is not called by the migrated embedded consumer.

## Verification

Targeted checks run on this branch:

```text
node node_modules/vitest/vitest.mjs run --config vitest.config.ts --no-cache --maxWorkers=1 \
  src/tools/video-editor/commands/shotSetCapture.test.ts \
  src/tools/video-editor/commands/commitSession.test.ts \
  src/tools/video-editor/hooks/useTimelineCommandSession.test.tsx \
  src/tools/travel-between-images/pages/ShotEditorView.test.tsx
```

Result: 4 files, 115 tests passed. ESLint passed for all touched source and test files, and `git diff --check` passed.

Not run by this bounded task: Runtime HTTP acceptance, browser/reload/undo/retry journeys, localhost/socket tests, full suites, build, and project-wide typecheck. Those are required before removing the remaining legacy standalone name writer or declaring the zero-legacy-traffic gate complete.

Exact harness source a4fb4bbb00e8c0453fdce8d311cf6a63944fc7b9. Source only; independent review and actual qualification pending.
