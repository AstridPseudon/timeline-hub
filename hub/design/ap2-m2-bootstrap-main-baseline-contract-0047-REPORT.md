# App2 M2 bootstrap Main-baseline contract proposal

## Result

Main behavior wins. The two-entry history is intentional, not an unintended
publisher, and the smallest App-owned change is a test expectation correction.
No bootstrap product path was edited or activated, and no browser gate was run.

## Main evidence

The Main014 Runtime source reviewed here is commit
`95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c` in
`/home/user/banodoco/banodoco-workspace-runtime`.

- `runtime_protocol/service.py:1698` defines `create_timeline()`.
- `service.py:1718-1729` creates the timeline and its ordinary timeline-created
  receipt/event.
- `service.py:1730-1734` then calls `TimelineCommitStore.bootstrap()` in the
  same create transaction.
- `runtime_protocol/timeline_commit_store.py:989-1022` creates the empty
  canonical parent, installs `parent.composition.published`, and records the
  real `parent_composition.publish` receipt with key
  `bootstrap:<timeline_id>`, `previous: null`, and the exact project/timeline
  scope.
- Main's `tests/test_timeline_commit_port.py:111-118` explicitly expects the
  post-create history entry to be that real bootstrap publication. Its
  `:121-137` neighbor also expects the create and publication receipts/events
  as separate ordered records.

Therefore the normal Main invariant is one bootstrap parent publication before
the first native `timeline.commit`; the native commit is not a replacement for
the baseline publication.

## App change

Changed only `tests/e2e/local/three-products.spec.ts:1729-1769`.

The former `items.toHaveLength(1)` assertion is mapped one-to-one to:

1. exactly two raw accepted entries in order: one
   `parent_composition.publish` baseline and one `timeline.commit` native
   initialization;
2. the baseline's exact `bootstrap:<timeline_id>` receipt key, null predecessor,
   `bootstrap` intent, null records, and project/timeline result scope;
3. the native entry's exact predecessor pair (the baseline revision/publication),
   `recorded` intent, `timeline.commit` receipt, and canonical-document
   project/timeline scope;
4. the ordered command sequence
   `timeline.init`, `track.create`, `track.create`, each version `1` and
   selected against `parent`; and
5. the returned history head being the native entry.

The existing create-before-init, zero-legacy, retry, reload, Runtime restart,
exact retry body/key, guarded undo, opaque-data, and post-commit assertions are
unchanged. No history entry is filtered out or deleted. The exact command-kind
array proves the native-initialization count is exactly one while retaining the
normal baseline count exactly one.

## Current App callers

The assigned App tree is on the published013 rollback state. Its current live
callers are:

- `src/shared/hooks/projects/useProjectCRUD.ts:154` calls
  `ensureProjectHasTimeline()` after project creation.
- `src/tools/video-editor/pages/VideoEditorPage.tsx:461` calls
  `ensureProjectHasTimeline()` for an empty selected project.
- `VideoEditorPage.tsx:551` calls `createCanonicalTimeline()` for an additional
  timeline.
- `src/integrations/runtime/createDefaultTimeline.ts:93-99` and `:121-126`
  route those current callers through the existing `publishEmptyTimeline()` /
  `publishParentComposition` path.

`RuntimeDataProvider.initializeNativeBootstrapTimeline()` at
`src/integrations/runtime/dataProvider.ts:498-513` and
`initializeBootstrapTimeline()` remain dormant exports in this assigned tree;
`rg` found no production caller. This proposal does not activate that path.
The historical f487 candidate described by the preceding two-entry triage had
the native initializer caller chain; that candidate's live qualification remains
separate and unqualified.

## Verification

- `./node_modules/.bin/eslint tests/e2e/local/three-products.spec.ts --report-unused-disable-directives --max-warnings 0` — PASS.
- `NODE_OPTIONS='--require=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-bootstrap-transport-assertion-repair/notes/vitest-runner.cjs' node node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism src/integrations/runtime/bootstrapInitialization.test.ts src/integrations/runtime/createDefaultTimeline.test.ts src/tools/video-editor/commands/bootstrapCapture.test.ts src/tools/video-editor/commands/commitOutbox.test.ts` — PASS, 4 files / 128 tests.
- `git diff --check` — PASS.
- No browser, localhost/socket, full suite, activation, pin/adoption, or repeat of gate 14046 was run.

An independent conversion reviewer must approve this test-only correction
before it is landed or used for a gate. No Runtime redesign is proposed here.
