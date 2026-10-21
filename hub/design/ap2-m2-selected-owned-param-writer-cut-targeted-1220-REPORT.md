# AP2 M2 selected owned PARAM writer cut — targeted review

## Result

No source change was made. The selected project-pack legacy snapshot writer is
already absent in the current `tl/integration` App source, so there is no
legitimate deletion to apply in this worker.

The current split is:

- `AstridElementParams.tsx:51-75`: an admitted/project-owned
  `elementRef.packId` takes the selected native carrier, resolves the exact
  accepted authority pin, performs the retained read, and submits
  `clip.set-params`. It returns before any snapshot callback.
- `selectedParamPort.ts`, `selectedParamAuthority.ts`, `clipParamsCapture.ts`,
  `commitSession.ts`, and `useTimelineCommandSession.ts`: live selected native
  capture, original-history authority, retained-read, command construction,
  session fencing, and outbox submission. These are not dead helpers.
- `AstridElementParams.tsx:77-81`: the remaining
  `!reference?.packId` literal/unowned `ElementCapturePort` path. Its positive
  test remains in `AstridElementParams.test.tsx`; removing it would drop a
  separate unsupported-family consumer and exceed the selected owned-pin cut.
- `AstridElementParams.tsx:83`: host `onChange(next)` compatibility fallback
  when the literal native port is unavailable. It is not reachable from the
  admitted/project-owned branch because that branch returns first.

Thus the supported branch is already isolated by the owned `packId` guard. The
hosted SYSTEM8e no-carrier decision is unchanged; no project pin, builtin
substitute, latest/P2/browser-hash authority, or save-time admission was added.
The retained ORIGINAL P1 `schema_source` and selected revision remain intact.

An independent prior review reached the same bounded disposition:
`ap2-m2-selected-exact-remaining-writer-cut-0059-REPORT.md` records that the
selected-pack writer was already absent and that the literal fallback remains
live. This worker made no claim that the whole App PARAM writer is retired.

## Verification

Shared dependency paths were checked read-only:

```text
realpath node_modules
/home/user/work/app/node_modules
realpath /home/user/work/app/node_modules
/home/user/work/app/node_modules
```

The protected install currently resolves `@banodoco/timeline-composition`
0.0.8, while this worktree's tracked `package.json` and lock pin the existing
0.0.13 tarball. No shared install, dependency, graph, or cache was changed.

Passed:

```bash
./node_modules/.bin/vitest run --no-cache --config config/testing/vitest.config.ts --maxWorkers=1 --no-file-parallelism \
  src/tools/video-editor/commands/clipParamsCapture.test.ts \
  src/tools/video-editor/commands/selectedParamPort.test.ts \
  src/tools/video-editor/commands/selectedParamAuthority.test.ts \
  src/tools/video-editor/commands/commitSession.test.ts \
  src/tools/video-editor/commands/commitOutbox.test.ts \
  src/tools/video-editor/hooks/useTimelineCommandSession.test.tsx \
  src/tools/video-editor/hooks/useTimelineCommandSession.projection.test.tsx \
  src/tools/video-editor/components/PropertiesPanel/AstridElementParams.test.tsx \
  src/tools/video-editor/components/PropertiesPanel/AstridElementParams.mounted.test.tsx \
  src/tools/video-editor/components/PropertiesPanel/PropertiesPanel.test.tsx
# 10 files, 233 tests passed

./node_modules/.bin/eslint --no-cache --max-warnings 0 \
  src/tools/video-editor/commands/clipParamsCapture.ts \
  src/tools/video-editor/commands/clipParamsCapture.test.ts \
  src/tools/video-editor/commands/selectedParamPort.ts \
  src/tools/video-editor/commands/selectedParamPort.test.ts \
  src/tools/video-editor/commands/selectedParamAuthority.ts \
  src/tools/video-editor/commands/selectedParamAuthority.test.ts \
  src/tools/video-editor/commands/commitSession.ts \
  src/tools/video-editor/commands/commitSession.test.ts \
  src/tools/video-editor/commands/commitOutbox.test.ts \
  src/tools/video-editor/hooks/useTimelineCommandSession.ts \
  src/tools/video-editor/hooks/useTimelineCommandSession.test.tsx \
  src/tools/video-editor/hooks/useTimelineCommandSession.projection.test.tsx \
  src/tools/video-editor/components/PropertiesPanel/AstridElementParams.tsx \
  src/tools/video-editor/components/PropertiesPanel/AstridElementParams.test.tsx \
  src/tools/video-editor/components/PropertiesPanel/AstridElementParams.mounted.test.tsx \
  src/tools/video-editor/components/PropertiesPanel/PropertiesPanel.test.tsx
# passed, zero warnings

git diff --check
# passed
```

Serialized typecheck command:

```bash
flock -w 600 /home/user/work/.app-tsc.lock env NODE_OPTIONS=--max-old-space-size=4096 ./node_modules/.bin/tsc --noEmit -p tsconfig.app.json --pretty false
```

Result: failed with 29 existing diagnostics, all outside this worker's
selected PARAM source/test paths. The diagnostics include Composition 0.0.8
missing 0.0.13 exports (`CompiledCanonicalTransitions`, `computeMediaTrim`,
`encodedEnvelopeSource`, `getSanitizedPlaybackRate`, `compileCanonicalTransitions`,
and `clipOpacity`), plus existing unrelated App type errors in preview,
timeline, scalar, and renderer files. Because the worktree is unchanged, this
is baseline/protected-package evidence, not a regression from this worker.

Not run: browser/localhost/live-socket, central/full suites, or any install or
shared dependency mutation. No generated/public API/pin/lock/source file was
edited. `git status --short` and `git diff --stat` were empty.

## Handoff

The orchestrator can treat the selected-pack legacy writer cut as already
present in this source tree, while keeping the literal/unowned element PARAM
consumer open. The next real selected browser journey remains checkpoint 18's
responsibility; it is not claimed here.
