# AP2 M2 selected reviewed current delivery and DEV gate

## Result

Delivered the reviewed selected row-local consumer onto the assigned current App
head `ce6deafa32593f3791cf64b67b7b67fe9f64fe96`, plus the approved one-file
assertion conversion.

The source packet is byte-for-byte identical to
`tl/ap2-m2-selected-fallback-assertion-conversion` for all nine row-local
donor paths and the converted test file. The donor source was
`tl/ap2-m2-selected-row-local-current-clean-source`
(`251f3a5b6f83b0d12b0863d3e602b10fc1d12d2e`); the approved conversion was
`713e5936bab4d5669826c6e40a5ec79312c120ce`.

The merge-forward was attempted from donor parent
`e9d04f4bf0b9c06d184541655f20a4ca832d0370` onto current `ce6deafa`.
Current Viewing alias-removal changes remain intact, including
`config/vite/vite.config.ts`; no older config or retired fallback file was
ported. Both retired fallback files remain absent.

## Delivered paths

- `playwright.three-products.config.ts`
- `src/tools/video-editor/components/PropertiesPanel/AstridElementParams.mounted.test.tsx`
- `src/tools/video-editor/components/PropertiesPanel/AstridElementParams.test.tsx`
- `src/tools/video-editor/components/PropertiesPanel/AstridElementParams.tsx`
- `src/tools/video-editor/components/PropertiesPanel/ClipPanelBody.tsx`
- `src/tools/video-editor/components/PropertiesPanel/PropertiesPanel.test.tsx`
- `src/tools/video-editor/components/PropertiesPanel/PropertiesPanel.tsx`
- `tests/e2e/local/support/harness.ts`
- `tests/e2e/local/three-products.selected-param-dev.spec.ts`

No schema, pin, dependency, shared file, fallback, or built-in-catalog
substitution was added.

## Assertion conversion

The old selected fallback assertion for `selectedSegmentIndex: 2 -> 1`
maps one-to-one to active assertions:

- Native success preserves `futureParam: "keep-me"`, asserts
  `values.selectedSegmentIndex: 1`, `clear: []`, exact `schema_source`,
  exact `{ command, preview: null }` submission, and no legacy `onChange`.
- Missing carrier visibly refuses while retaining dirty input `"1"`; capture,
  finish, submit, and legacy `onChange` are all not called, and the retained
  read/carrier error is asserted in the DOM.

No assertion was deleted or weakened; this conversion adds no `it.fails`,
skip, or xfail.

## Verification

All passed:

```text
./node_modules/.bin/vitest run --no-cache --config config/testing/vitest.config.ts --maxWorkers=1 --no-file-parallelism src/tools/video-editor/commands/clipParamsCapture.test.ts src/tools/video-editor/commands/selectedParamPort.test.ts src/tools/video-editor/commands/selectedParamAuthority.test.ts src/tools/video-editor/components/PropertiesPanel/AstridElementParams.test.tsx src/tools/video-editor/components/PropertiesPanel/AstridElementParams.mounted.test.tsx src/tools/video-editor/components/PropertiesPanel/PropertiesPanel.test.tsx
6 files, 71 passed, 0 expected failures

./node_modules/.bin/eslint --no-cache --max-warnings 0 playwright.three-products.config.ts tests/e2e/local/support/harness.ts tests/e2e/local/three-products.selected-param-dev.spec.ts src/tools/video-editor/components/PropertiesPanel/AstridElementParams.tsx src/tools/video-editor/components/PropertiesPanel/AstridElementParams.test.tsx src/tools/video-editor/components/PropertiesPanel/AstridElementParams.mounted.test.tsx src/tools/video-editor/components/PropertiesPanel/ClipPanelBody.tsx src/tools/video-editor/components/PropertiesPanel/PropertiesPanel.tsx src/tools/video-editor/components/PropertiesPanel/PropertiesPanel.test.tsx
PASS

./node_modules/.bin/tsc --noEmit --pretty false
PASS

./node_modules/.bin/playwright test --config playwright.three-products.config.ts tests/e2e/local/three-products.selected-param-dev.spec.ts --list
PASS — exactly 1 selected test:
local DEV selected PARAM uses admitted P1 through P2 removal, refusal, retry, reload and undo

git diff --check
PASS
```

The normal DEV fixture retains the genuine provenance: initial `draft-1`
carrier has no `packId`; Agent `timelines update-element` establishes P1
through accepted `clip.set-element` then `clip.set-params`; later P2 is
admitted through the normal project-pack path.

## One authorized central DEV gate

The existing wrapper was verified with `sh -n` and its exact source guards.
It pins this tuple:

- Agent `8130a401bf44a518d5a40ae274d398b8c560be55`, tree
  `236c3e57e0265c52b81ba8085de3193026176bff`
- Runtime `2c4ac180c2220bdad966bc01e95ad230e99ce26a`, tree
  `7ab412cc4bcbe517efcfa806e092336390312e18`
- locked App graph archive
  `895c628ab0727c8975247310fd0319b0f546a8d032a57072c9e364e20965ca30`
- Composition tarball
  `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`

Exactly one named, cache-disabled gate was submitted:

```sh
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test ap2-m2-selected-reviewed-current-delivery-and-gate ap2-m2-selected-real-p1-history-fixture-fix --no-cache) && /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"
```

Result ID:
`ap2-m2-selected-reviewed-current-delivery-and-gate-ap2-m2-selected-real-p1-history-fixture-fix-1020230919-12657`

Result: **exit 1; not qualified**. Collection selected exactly one test and
the hosted build passed (`5577 modules transformed; built in 58.86s`). The
browser journey reached genuine P1 setup, then Agent bootstrap failed before
P1 admission because its frozen runtime reported:

```text
neutral runtime bootstrap was not ready: No workspace is configured;
run astrid-runtime workspace create or workspace attach.
```

This is an environment/wrapper setup failure, not a selected assertion failure.
No retry or second gate was submitted. Bounded sanitized evidence is retained at:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/ap2-m2-selected-reviewed-current-delivery-and-gate-ap2-m2-selected-real-p1-history-fixture-fix-1020230919-12657/log.txt`

and the wrapper's bounded central trace directory:
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-selected-draft-p1-review-gate/central-trace`.

## Cleanup and handoff

The wrapper's temporary run root was removed; no `/tmp/ap2-m2-selected-p1.*`
directories remain. Disk check: 19G free on `/tmp`. The worktree contains
only the nine reviewed donor paths plus the one approved converted test.

Recommended next step: repair/provision the existing wrapper's Agent workspace
create/attach prerequisite, then let the manager decide whether to run the
same named gate once. No App source change is indicated by this failure.

