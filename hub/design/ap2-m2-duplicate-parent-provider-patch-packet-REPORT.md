# App provider-forwarding patch packet

Prepared two independent, unapplied flat diffs. No product source was changed on the worker branch; `git status --short` is clean.

## Packets

1. [occurrence duplicate provider patch](handoff-ap2-m2-duplicate-parent-provider-occurrence.patch)
   - Applies to source candidate `4006b673b3edaef2db2df8ade2012d644319df7e` (`tl/ap2-m2-duplicate-final-actual-gate`).
   - Forwards `editor.occurrenceDuplicate` into the public `editorOps` join.
   - Adds a mounted native-port marker to the existing `VideoEditorProvider` mock and asserts it through the mounted consumer.

2. [parent clip add-media provider patch](handoff-ap2-m2-duplicate-parent-provider-parent-media.patch)
   - Applies to source candidate `5ae77819ead824ea2bdd6041010142b8d055feb4` (`tl/ap2-m2-parent-real-prepared-caller-repair`).
   - Forwards `editor.parentClipAddMedia` into the public `editorOps` join.
   - Adds a mounted native-port marker to the existing `VideoEditorProvider` mock and asserts it through the mounted consumer.

The packets intentionally do not include the already-queued `ea82d7a3581ec97e9e3e31d06bfda481529ab1f3` element-provider line, generic dispatcher/API/lifecycle work, catalog changes, or lifetime changes.

## Evidence

Each packet was applied with `git apply --check` and then `git apply` to a fresh archived private copy of its paired source candidate. Before forwarding, the new mounted-port assertion was red (`Received: missing`, one failed provider test). With the forwarding line, it was green.

Occurrence candidate, after patch:

```text
npx vitest run --no-cache --config config/testing/vitest.config.ts src/tools/video-editor/contexts/VideoEditorProvider.test.tsx src/tools/video-editor/commands/occurrenceDuplicateCapture.test.ts src/tools/video-editor/commands/occurrenceDuplicateGesture.test.ts
Test Files  3 passed (3); Tests 107 passed (107)
npx eslint --no-cache src/tools/video-editor/contexts/VideoEditorProvider.tsx src/tools/video-editor/contexts/VideoEditorProvider.test.tsx src/tools/video-editor/hooks/useTimelineState.ts src/tools/video-editor/hooks/useTimelineState.types.ts
PASS
npx tsc --noEmit --pretty false
PASS
```

Parent candidate, after patch:

```text
npx vitest run --no-cache --config config/testing/vitest.config.ts src/tools/video-editor/contexts/VideoEditorProvider.test.tsx src/tools/video-editor/commands/parentClipAddCapture.test.ts src/tools/video-editor/hooks/useTimelineCommandSession.test.tsx
Test Files  3 passed (3); Tests 94 passed (94)
npx eslint --no-cache src/tools/video-editor/contexts/VideoEditorProvider.tsx src/tools/video-editor/contexts/VideoEditorProvider.test.tsx src/tools/video-editor/hooks/useTimelineState.ts src/tools/video-editor/hooks/useTimelineState.types.ts
PASS
npx tsc --noEmit --pretty false
PASS
```

No full suite, browser, localhost/socket, dependency, commit, push, or ledger work was performed.

## Next step

HOME final join should apply each packet only after its paired source candidate is present, then retain the provider mounted-port assertions. The two packet files are separate because their native port types arrive with different source branches.
