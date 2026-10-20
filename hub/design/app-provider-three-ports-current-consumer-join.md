# App Provider three-port current-consumer join

Status: source join complete; harness commit and the actual mounted App2 gate remain pending.

## Exact source identities

- App worker base: `180d2aaeaa7b330ca5677e0e11f985e2d00d9116`.
- Candidate working-tree tree, computed in memory without Git object/index/ref writes: `97e9698040c7f10079f43038ebb4a2e8d83113d3` (5,853 tracked files plus 1 untracked test file).
- App2 occurrence-duplicate reviewed source: `d3792aabdc8592be5f72321faa7143e9b76d1c26`.
- App2 element reviewed source: `ea82d7a3581ec97e9e3e31d06bfda481529ab1f3`.
- App2 parent-media current-root consumer: `c97a64d68d0bd318249034250633fa486ba14495`.
- Parent exact prerequisites: legacy-clean fence `c9d1fb88022853febd3740c0f404c56f22da03d9`; prepared-caller repair `5ae77819ead824ea2bdd6041010142b8d055feb4`.

The eventual commit SHA is intentionally left to the harness.

## Composition

The existing command-session/outbox path now exposes the reviewed `occurrenceDuplicatePort` and `parentClipAddMediaPort`, including the existing readiness, generation, head, bundle, preview, exact-command, and legacy-clean fences. The reviewed occurrence duplicate and prepared parent-media callers use those ports; prepared-media verification uses the already-landed Runtime facade. Existing element capture remains on the current session path.

`VideoEditorProvider` now forwards exactly these three editor operations in its memo:

- `element: editor.element`
- `occurrenceDuplicate: editor.occurrenceDuplicate`
- `parentClipAddMedia: editor.parentClipAddMedia`

The Provider consumer assertion confirms all three are mounted. Existing `None`, shot, move, label, automatic, and lifetime/host wiring remains present and unchanged in the Provider memo.

No framework, DTO, pin, direct POST, generic serializer, or legacy writer retirement was added. The existing root read facade `0096ba86d` and recovery fix `9b14bf9f7` were retained.

## Local evidence

Passed targeted Vitest runs:

```text
5 files, 154 tests passed
  commitSession.occurrenceDuplicate.test.ts
  commitSession.test.ts
  parentClipAddCapture.test.ts
  VideoEditorProvider.test.tsx
  AstridTimelineEditor.document-shots.test.tsx

5 files, 72 tests passed
  elementCapture.test.ts
  useTimelineCommandSession.test.tsx
  useTimelineCommandSession.projection.test.tsx
  useAddVariantAsGeneration.test.tsx
  useClipEditing.test.ts
  useSwitchToFinalVideo.test.tsx

1 file, 22 tests passed
  useTimelineCommandSession.test.tsx (including the added parent-media legacy-save fence)
```

Targeted ESLint passed with `--no-cache --max-warnings 0`; `git diff --check` passed. No full suite, project TypeScript check, install, browser, or shared-cache write was run.

## Open gate

The exact App2 source identities and this candidate tree are ready for the central actual mounted gate. That gate must still establish native mounted reload/undo/lost-ACK/restart/exact-retry behavior and zero legacy traffic. These source and targeted-test results do not retire or activate any writer.
