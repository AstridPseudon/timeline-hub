# App MAIN574/public13 parent-delete zero-post diagnosis

## Source and disposition

The starting App source was commit `1981ce9801b661a9a335201b0ebd4fcdf1d8aad1`,
tree `a4cc5140cb19f6d4414150d22ac579bce90bb08a`. The only change in this
worker is a test-fixture correction in
`tests/e2e/local/clip-delete-command.spec.ts`; no App product source, protocol,
Runtime, Agent, dependency, or integration worktree was changed. The harness
must commit this change before the strict central browser guard can run it, so
the post-harness commit/tree is not yet known here.

## Actual UI cause

The failed run's retained evidence was only the zero-post timeout; its wrapper
removed private browser artifacts, so it did not preserve a pre-fix
`document.activeElement` value. Source inspection of the actual active UI path
identified the fixture failure: `.clip-action` is a production
`div[role="button"][tabindex="0"]`, while the new Inspector also renders a
production Track name `<input>`. The keyboard hook intentionally ignores
editable targets and events outside the editor shell. The old fixture clicked
the clip and then sent a page-level `Delete` without asserting either
`data-selected` or focus. Thus the zero `wire.posts` result was not evidence
of a backend/port failure.

The fixture now asserts the selected clip, explicitly focuses that production
clip action, asserts it is the active element, and only then sends the real
`Delete` key. It does not inject an operation, bypass a readiness/port guard,
or replace the keyboard path. The same correction is applied to both the
success and conflict cases.

## Checks run

- `git diff --check` — passed.
- `npx eslint tests/e2e/local/clip-delete-command.spec.ts` — passed.
- `npx playwright test --config playwright.clip-delete.config.ts --list` —
  passed; exactly the two required tests were discovered.
- `npx vitest run --config .vitest-zero-post.config.ts src/tools/video-editor/hooks/useKeyboardShortcuts.test.tsx src/tools/video-editor/commands/clipDeleteGesture.test.ts src/tools/video-editor/hooks/useTimelineOps.clipDelete.test.ts` — passed; 3 files and 48 tests. The temporary config used a private `/tmp` cache and was removed.
- The prior central exact two-case run on the uncorrected tree exited 1 after
  the success case timed out with `wire.posts.length === 0`; the conflict case
  was consequently not run. No full suite, install, or typecheck was run.

## Remaining proof

The post-correction browser proof is pending the harness commit and a new
central exact two-case run. That run must prove both success and conflict
flows, including the existing owner-aware routing, opaque/proto/receipt,
idempotency/conflict metadata, and zero legacy-writer assertions. No claim is
made here that either browser case, Runtime acceptance, undo, or legacy-zero
proof has passed on the corrected source yet.
