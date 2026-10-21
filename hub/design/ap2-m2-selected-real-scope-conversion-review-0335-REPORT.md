# M2 selected real-scope selector conversion review

## Verdict

APPROVE the exact candidate commit `8e9975005d18c6278000ab4c8cc8b18291d03e12`
with tree `87d2350417a876e14b81c58b64da29f1a30b35b6`.

The candidate changes only
`tests/e2e/local/three-products.selected-param-dev.spec.ts` (9 additions, 3
deletions). It replaces the nonexistent `video-editor-provider` DOM query at
the same three readiness positions with the existing visible `Select timeline`
combobox plus exact `project` and `timeline` URL parameters.

## Evidence and source mapping

The retained actual 0320 trace shows the old assertion failed after the real
page had already displayed the project, `Selected PARAM` timeline, and
`selected-param-clip`:

- Error context:
  `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-selected-draft-p1-review-gate/central-trace/three-products.selected-pa-e0e73-fusal-retry-reload-and-undo/error-context.md`
- Trace:
  `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-selected-draft-p1-review-gate/central-trace/three-products.selected-pa-e0e73-fusal-retry-reload-and-undo/trace.zip`

The replacement is backed by product source, not a test-only hook:

- `src/shared/components/ProjectTimelineSelectors.tsx:143-162,346-362`
  declares the real `role="combobox"` / `Select timeline` surface.
- `src/tools/video-editor/pages/VideoEditorPage.tsx:204-214` reads the route
  IDs and matches the discovered timeline; lines 288-310 require verified
  project/timeline identity before creating provider selection; lines 800-826
  pass that verified selection to the real provider.
- `src/app/main.tsx:42-45,102-124` and `src/app/bootLayer.ts:60-81` support the
  retained real `#root > *` 20-second startup mount check.
- `src/tools/video-editor/lib/timeline-dom.ts:18-24,77-84,130-134` and
  `src/tools/video-editor/components/TimelineEditor/ClipAction.tsx:572` declare
  the existing `.clip-action[data-clip-id]` surface.
- `src/tools/video-editor/components/PropertiesPanel/AstridElementParams.tsx:91-95`
  declares the retained `astrid-element-params` P1 surface.

The old `video-editor-provider` match exists only in
`src/tools/video-editor/pages/VideoEditorPage.test.tsx` mocks; it is absent from
the production page source. The candidate adds no attribute, private React
state read, response fabrication, navigation, retry/recovery, product,
harness, pin, or new timeout budget.

## Assertion mapping

- All three original 20-second `expectAppMounted` positions remain unchanged.
- The three old provider assertions become the same real timeline UI plus exact
  route identity checks for `selected.projectId` and `selected.timelineId`.
- The exact displayed clip locator, click, `astrid-element-params`, and
  `Amount` assertions remain. The selected P1 `schema_source` and exact clip
  selection body checks remain.
- Both original reloads remain.
- P1 success, P2 admission, authored-source removal, retained-P1 refusal,
  dirty draft, lost acknowledgement, restart/reload recovery, exact retry body
  and idempotency key, undo/inverse, and zero-legacy checks remain unchanged.
- No browser run is claimed; the retained actual evidence only proves the old
  locator's failure point and the real UI surface reached before it.

## Live callers

- The sole collected test is
  `tests/e2e/local/three-products.selected-param-dev.spec.ts:39`.
- Its fixtures are `tests/e2e/local/support/app.ts` (`appTest`,
  `openSeededTimeline`) and `tests/e2e/local/support/harness.ts`
  (`seedSelectedParamDev`, `advanceSelectedParamAndRemoveSource`, and
  `startSelectedParamDevServer`).
- The central wrapper named by prior evidence is
  `workers/ap2-m2-selected-draft-p1-review-gate/run-central-selected-p1.sh`.
  No other selected test or live caller was found in the App tree.

## Checks

Run against an archived private copy of the exact candidate tree, with the
shared `node_modules` read-only:

- `./node_modules/.bin/eslint --no-cache --max-warnings 0 tests/e2e/local/three-products.selected-param-dev.spec.ts` — passed.
- `git diff --check 8e9975005^ 8e9975005` — passed.
- `./node_modules/.bin/playwright test --config playwright.three-products.config.ts tests/e2e/local/three-products.selected-param-dev.spec.ts --list` — exactly 1 test in 1 file.
- `git diff --name-status 8e9975005^ 8e9975005` — only the selected journey file changed.

Not run by instruction: browser execution, localhost/socket execution, central
actual run, full suite, install, or any source mutation. A separate HOME
manager status file was not present; the available app2 STATUS/INBOX were read,
including their HOME pin/publication notes.

## Next step

Use this exact candidate/tree for the single newly authorized central selected
actual run. Do not claim P1/P2/recovery qualification from this review alone;
the full journey remains unverified until that run completes.
