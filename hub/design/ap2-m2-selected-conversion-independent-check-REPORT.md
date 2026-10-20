# AP2 M2 selected conversion independent review

## Verdict

**APPROVE** for the requested one-file test conversion.

Reviewed candidate:

- branch: `tl/ap2-m2-selected-fallback-assertion-conversion`
- head: `713e5936bab4d5669826c6e40a5ec79312c120ce`
- donor: `tl/ap2-m2-selected-row-local-current-clean-source` at
  `251f3a5b6f83b0d12b0863d3e602b10fc1d12d2e`
- requested base: `hub/tl/integration` at
  `ce6deafa32593f3791cf64b67b7b67fe9f64fe96`

The candidate delta over the donor is exactly one file:

`src/tools/video-editor/components/PropertiesPanel/AstridElementParams.test.tsx`

No product source or App copy was added by the conversion.

## Assertion review

The original `selectedSegmentIndex: 2 -> 1` intent is represented in both
required outcomes:

- Native success retains `futureParam: "keep-me"`, asserts
  `values.selectedSegmentIndex: 1`, `clear: []`, and the exact
  `schema_source` pin passed to `finish`; it also asserts the exact submitted
  `{ command, preview: null }` payload and no legacy `onChange` call.
- Missing carrier refuses visibly while retaining the dirty input value `"1"`.
  `capture`, `finish`, `submit`, and legacy `onChange` are all asserted not to
  be called, and the retained-read/carrier error is asserted in the DOM.

The old source assertions map one-to-one to those active assertions. The
converted test contains no `it.fails`, `skip`, or `xfail`; the candidate-wide
`it.fails` inventory is the same three pre-existing drag exceptions as the
donor. No assertion was deleted or weakened.

## Scope and source checks

`git diff --name-status 251f3a5b6..713e5936b` reports only the test file above.
The donor commit’s own nine changed paths contain no
`theme-api.fallback.tsx`, `registry.generated.fallback.ts`, `config/vite`,
preview, render, or Composition path. Both retired fallback files are absent
from the candidate tree.

The donor branch was based on `e9d04f4bf0b9c06d184541655f20a4ca832d0370`,
while current `hub/tl/integration` is `ce6deafa32593f3791cf64b67b7b67fe9f64fe96`
and contains later Viewing alias-removal commits. This is a donor refresh/
merge concern, not a defect in the reviewed conversion delta; refresh the
source onto current integration before delivery.

## Verification evidence

Inspected the candidate worker’s recorded bounded run:

```sh
./node_modules/.bin/vitest run --no-cache --config config/testing/vitest.config.ts --maxWorkers=1 --no-file-parallelism \
  src/tools/video-editor/commands/clipParamsCapture.test.ts \
  src/tools/video-editor/commands/selectedParamPort.test.ts \
  src/tools/video-editor/commands/selectedParamAuthority.test.ts \
  src/tools/video-editor/components/PropertiesPanel/AstridElementParams.test.tsx \
  src/tools/video-editor/components/PropertiesPanel/AstridElementParams.mounted.test.tsx \
  src/tools/video-editor/components/PropertiesPanel/PropertiesPanel.test.tsx
```

PASS — 6 files, 71 passed, 0 expected failures.

Also recorded PASS: targeted ESLint, `tsc --noEmit --pretty false`, and
`git diff --check`. No browser, socket, full suite, `request-test`, build, or
pin/adoption gate was run. I did not rerun tests in another worker worktree or
create an App copy; this was a read-only source review.
