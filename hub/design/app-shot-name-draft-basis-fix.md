# App shot-name draft/basis fix

## Source and tree

- App worktree: `/home/user/work/wt/app-m2-shot-name-draft-basis-fix`
- Base `HEAD`: `a4fb4bbb00e8c0453fdce8d311cf6a63944fc7b9` (`feat(app): migrate embedded shot names to native session`)
- Review source: `/home/user/timeline-hub/hub/design/app-shot-name-native-independent-review.md`
- This report describes the uncommitted worker tree; no integration branch or other worktree was changed.
- Changed production files: `commitSession.ts`, `shotSetCapture.ts`, `shotSetGesture.ts`, `useTimelineCommandSession.ts`, `useNameEditing.ts`, `ShotEditorView.tsx`.
- Added focused tests: `shotSetSession.test.ts`, `useNameEditing.test.ts`.

## Resolutions

1. `commitSession` shot completion now keeps the original captured bundle as `before` and the captured-basis `finishShotSet` result as `after`. `captureShotSet` retains the true pre-placeholder bundle, so local projection/undo cannot restore the placeholder name. Submit compares the captured before bundle with the current session bundle and refuses after an observation changed it; it does not merge or rebase a stale graph. The accepted command retains its original guards/source pin/identity.

2. Native shot submission returns a completion tied to the same outbox intent ID and accepted receipt. The name form remains open while durable submission is pending, closes only after acceptance, and restores the exact untrimmed input after refusal. Refusal is presented through the existing error path. Scope and unmount guards prevent a late completion from updating a different shot; dispose still does not wait for a network acknowledgement.

## Evidence

Passed:

```text
node node_modules/vitest/vitest.mjs run --config vitest.config.ts --no-cache --maxWorkers=1 \
  src/tools/video-editor/commands/shotSetCapture.test.ts \
  src/tools/video-editor/commands/shotSetSession.test.ts \
  src/tools/video-editor/commands/commitSession.test.ts \
  src/tools/video-editor/hooks/useTimelineCommandSession.test.tsx \
  src/tools/travel-between-images/pages/ShotEditorView.test.tsx \
  src/tools/travel-between-images/components/ShotEditor/hooks/editor-state/useNameEditing.test.ts
PASS: 6 files, 119 tests.

npx eslint --max-warnings 0 [all touched source/test files]
PASS.

git diff --check
PASS.
```

The requested `--configLoader=runner` variant was attempted with `--no-cache` but the repository config fails before tests because `config/testing/vitest.config.ts` uses CommonJS `__dirname` while runner mode evaluates it as ESM (`ReferenceError: __dirname is not defined`). The passing run used the normal config with `--no-cache`; it did not write the shared Vite cache.

## Remaining gates / limits

- Actual Runtime HTTP acceptance/refusal for `shot.set`, browser form behavior, reload/restart recovery, lost-ACK exact retry, native undo/redo, and project/scope switch are still unverified here.
- The 0-legacy-name-writer gate is not achieved or claimed. Standalone/canonical fallback, ordinary legacy, gallery, and settings writers remain intentionally unchanged.
- No full suite, browser, localhost/socket journey, project typecheck, build, install, integration merge, or retirement claim was made.

Recommended next step: run the central Runtime/browser journey against this exact worker tree, covering acceptance, 409 draft retention, reload/exact retry, and native undo before review approval.
