# AP2 M2 selected PARAM exact remaining writer cut

## Disposition

**HELD / UNMERGED.** The selected-pack legacy snapshot writer is already absent
from the current App integration tree. No physical deletion was made and no
`rowDELETED`, native-success, or current gate-pass claim is made.

The newest authorized gate, `ap2-m2-selected-cold-mount-approved-gate-0055`,
failed before selected P1 admission: the real Runtime connection status did
not become `connected` within 20 seconds. Its exact report is
`ap2-m2-selected-cold-mount-approved-gate-0055-REPORT.md`; no retry or repeat
gate was run.

## Source trace

The selected-pack PARAM publisher is the native command path:

- `src/tools/video-editor/components/PropertiesPanel/AstridElementParams.tsx:51-75`
  takes the `reference.packId` branch, keeps the draft, resolves the accepted
  authority pin, prefetches retained inputs, and submits `clip.set-params`.
  It returns before the panel snapshot callback.
- `src/tools/video-editor/commands/commitSession.ts:784-847` owns the live
  `clipParamsPort`, validates the captured basis, builds `selectedParamsCommand`,
  and submits the native command.
- `src/tools/video-editor/hooks/useTimelineCommandSession.ts:199-229` wraps
  the port with selected-authority and legacy-clean fences, preserving refusal
  when the basis or session changes.
- The selected-pack legacy `onChange(next)` snapshot branch is therefore not a
  selected-pack caller. `AstridElementParams.tsx:77-83` is the remaining
  unowned/literal fallback after the native literal-element branch; it is not
  this selected-pack row and remains live through `ClipPanel`/`PropertiesPanel`.
  Removing it would exceed this task and could remove an unmigrated literal
  path.

No selected-PARAM helper is dead:

| export | live production callers |
|---|---|
| `selectedParamsCommand` | `commitSession.ts:21,843` |
| `captureClipParamsEdit` / `submitClipParamsEdit` | `AstridElementParams.tsx:64,66` |
| `createSelectedParamPort` | `useTimelineCommandSession.ts:45` |
| `resolveSelectedParamAuthority` | `selectedParamPort.ts:4,56` |
| `ClipParamsCapturePort` / `clipParamsPort` | `commitSession.ts:784,1160`, threaded through `useTimelineSave`, `useTimelineState`, `VideoEditorProvider`, `PropertiesPanel`, and `ClipPanelBody` |

The exact selected-pack schema pin and accepted native history are preserved;
the client does not add local schema validation or infer a replacement pin.
The chosen draft/normal refusal behavior remains in place.

## Verification

Shared dependency realpaths were checked before testing; both worktree
`node_modules` and `/home/user/work/app/node_modules` resolve to the shared
install. Tests used an owned `TMPDIR` and Vitest `--no-cache`.

Command:

```sh
./node_modules/.bin/vitest run --no-cache --config config/testing/vitest.config.ts \
  --maxWorkers=1 --no-file-parallelism \
  src/tools/video-editor/commands/clipParamsCapture.test.ts \
  src/tools/video-editor/commands/selectedParamPort.test.ts \
  src/tools/video-editor/commands/selectedParamAuthority.test.ts \
  src/tools/video-editor/components/PropertiesPanel/AstridElementParams.test.tsx \
  src/tools/video-editor/components/PropertiesPanel/AstridElementParams.mounted.test.tsx \
  src/tools/video-editor/components/PropertiesPanel/PropertiesPanel.test.tsx
```

Result: **70 passed, 1 failed** across 6 files. The failure is the existing
mounted test `AstridElementParams.mounted.test.tsx` case “refuses a mounted
edit whose retained read completes after the command session is gone”; it
times out at line 210 waiting for `latest.current?.commands.clipParamsPort`.
The same failure reproduced in a single-file rerun. The first mounted case and
all other selected neighbors passed. No test was skipped, weakened, deleted,
or converted.

The latest central gate result was **exit 1 before P1**, as described above.
No browser, localhost/live socket, full suite, repeat gate, or build gate was
run by this worker.

## Candidate cut

- Current source: unchanged `HEAD ee6b809e6` on `tl/ap2-m2-selected-exact-remaining-writer-cut-0059`.
- Changed exports: none.
- Changed live callers: none.
- Physical product deletions: none; the selected-pack legacy writer was already
  gone in the integrated `8baef9869`/`db8ddd10e` plus shared `5a7144b55` source.
- Blocker: real Runtime connection readiness in gate 0055, followed by the
  focused mounted-session setup failure recorded above.

Recommended next step: resolve the authorized central Runtime readiness
failure, then re-audit this exact tree before any deletion or native-success
decision. Do not remove the remaining literal fallback or claim this row
closed from the source-only evidence.
