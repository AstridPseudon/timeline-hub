# AP2 M2 literal element fallback cut

## Result

Deleted the literal PARAM legacy writer fallback in
`src/tools/video-editor/components/PropertiesPanel/AstridElementParams.tsx`.
Literal existing-clip PARAM edits now require the existing public014 native
element capture/session port. If the carrier is missing, the descriptor has
changed, or capture/submit refuses, the edited value stays in the local draft,
an inline error is shown, and `onChange` is not called. The existing selected-
pack refusal behavior remains intact.

Added direct tests for missing literal carrier and native capture refusal; the
existing native success, selected-pack refusal, stale-registration, overlay,
adapter, session, and command assertions were preserved.

## Scope decisions

- Only `AstridElementParams` and its direct test changed. `ElementsLibraryPanel`
  and `runtime/element-adapter.ts` were intentionally not deleted or broadly
  rewritten.
- The remaining exact direct-save/CAS caller is
  `ElementsLibraryPanel.tsx:121-156`, which sends transitions and non-literal
  element operations to `elementOperationAdapter.execute`; the corresponding
  direct read/apply/save boundary is `runtime/element-adapter.ts:497-524`.
  This remains live for literal animations, transitions, and owned/project-
  admitted routes, including the SYSTEM8e gap.
- No pin, inline authority, latest lookup, schema admission, capability drop,
  Provider/session/core, or active scalar gesture changes were made. No whole
  element row was marked deleted.

## Verification

```text
./node_modules/.bin/vitest run --config config/testing/vitest.config.ts --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/components/PropertiesPanel/AstridElementParams.test.tsx src/tools/video-editor/commands/elementCapture.test.ts src/tools/video-editor/commands/elementOverlayCapture.test.ts src/tools/video-editor/runtime/element-adapter.test.ts src/tools/video-editor/components/ElementsLibraryPanel.test.tsx src/tools/video-editor/commands/commitSession.test.ts src/tools/video-editor/hooks/useTimelineCommandSession.test.tsx src/tools/video-editor/hooks/useTimelineCommandSession.projection.test.tsx
PASS — 8 files, 164 tests

./node_modules/.bin/tsc --noEmit --pretty false --incremental false
PASS

./node_modules/.bin/eslint --no-cache --max-warnings 0 src/tools/video-editor/components/PropertiesPanel/AstridElementParams.tsx src/tools/video-editor/components/PropertiesPanel/AstridElementParams.test.tsx
PASS

git diff --check
PASS
```

No browser, localhost/live socket, full suite, Runtime Door, pin, generated
contract, installation, or shared-dependency mutation was run. Independent
review before merge remains for the orchestrator/merge queue; this worker did
not claim that review or browser proof.
