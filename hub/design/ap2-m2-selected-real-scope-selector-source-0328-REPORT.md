# Selected real scope selector source repair

## What changed

Changed only `tests/e2e/local/three-products.selected-param-dev.spec.ts`.

The three readiness assertions that queried `getByTestId('video-editor-provider')`
now call `expectSelectedTimeline(page, selected)`. That helper uses the existing
visible `Select timeline` combobox and checks the exact `project` and `timeline`
URL parameters against `selected.projectId` and `selected.timelineId`. The exact
route identity is the product's real selection surface: `VideoEditorPage` reads
those parameters, validates them against normal project/timeline discovery, and
passes the verified timeline ID into the real provider. The exact selected clip
ID and P1 schema/document pin assertions remain unchanged.

The existing `#root > *` 20-second mount precondition, three boundary positions,
original reloads, and all P1/P2/removal/refusal/draft/lost-ack/restart/body+key/
undo/zero-legacy assertions remain unchanged.

No product hook, data attribute, navigation/recovery/retry/timeout, harness,
driver, pin, or shared dependency was changed.

## Actual-cause evidence

The retained actual0320 run passed the mount precondition and loaded the
`Selected PARAM` timeline and `selected-param-clip`, then failed first at the
provider selector:

```text
getByTestId('video-editor-provider')
Expected data-timeline-id: 4a16a443-05a2-48b1-bdd6-4a0e211151cb
Error: element(s) not found
```

Retained evidence:

- Report: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/ap2-m2-selected-restored-precondition-one-case-0320-REPORT.md`
- Error context: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-selected-draft-p1-review-gate/central-trace/three-products.selected-pa-e0e73-fusal-retry-reload-and-undo/error-context.md`
- Trace: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-selected-draft-p1-review-gate/central-trace/three-products.selected-pa-e0e73-fusal-retry-reload-and-undo/trace.zip`

Source review proves the rejected hook was not a real browser DOM contract:

- `src/tools/video-editor/pages/VideoEditorPage.tsx:800-826` renders the
  `VideoEditorProvider` React component but adds no `data-testid` or
  `data-timeline-id` to it.
- A repository search found no production `video-editor-provider` hook; the
  matching hook exists only in isolated `VideoEditorPage.test.tsx` mocks.
- `src/tools/video-editor/pages/VideoEditorPage.tsx:204-214,288-311,633-643`
  establishes the real identity path: URL IDs are read, matched against normal
  discovery data, and only a verified project/timeline mounts the provider.
- `src/shared/components/ProjectTimelineSelectors.tsx:143-162,346-362`
  defines the existing `Select timeline` combobox used by the loaded page.
- `src/app/main.tsx:42-45,102-124` and `src/app/bootLayer.ts:6-8,60-81`
  define the existing `#root` mount/first-frame path retained by
  `expectAppMounted`.

## One-to-one assertion mapping

| Previous readiness assertion | Replacement | Identity preserved |
| --- | --- | --- |
| First load: nonexistent provider test ID with `selected.timelineId` attribute | Visible existing `Select timeline` combobox + exact URL `project` and `timeline` IDs | Exact project/timeline IDs; following exact `selected.clipId` DOM assertion remains |
| After first reload: same nonexistent provider test ID | Same helper | Exact IDs; clip and retained `Amount=8` checks remain |
| After lost-ack reload: same nonexistent provider test ID | Same helper | Exact IDs; clip, selected parameter, recovery, retry body/key checks remain |

No new DOM query lacks a defining product path. The exact selected clip query
(`.clip-action[data-clip-id="..."]`) and existing parameter surface
(`astrid-element-params`, `Amount`) were not weakened or replaced.

## Verification

Passed:

- `./node_modules/.bin/eslint --no-cache --max-warnings 0 tests/e2e/local/three-products.selected-param-dev.spec.ts`
- `git diff --check`
- `./node_modules/.bin/playwright test --config playwright.three-products.config.ts tests/e2e/local/three-products.selected-param-dev.spec.ts --list`
  — exactly 1 test in 1 file.

Not run by instruction: browser execution, socket/localhost execution, central
test service, full suite, install, or a second run. The retained actual0320
failure remains the only browser evidence; this source repair is therefore not
claimed as an actual journey qualification.

## Decisions and next step

Decision: use the existing route-backed project/timeline selection surface,
not the absent provider test ID and not a new product attribute. This preserves
exact identity while respecting the instruction not to add a product hook.

Next step: the orchestrator may perform the single permitted new actual run
from this source when its conversion review is complete.
