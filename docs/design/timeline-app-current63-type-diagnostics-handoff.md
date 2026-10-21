# App CURRENT63 TypeScript diagnostics handoff

**Audience:** App2 and Viewing  
**Capture:** `app-m4-type-selflink-private-overlay-one-check-r8`  
**Status:** qualified current13 evidence; no compiler rerun in this handoff task

## Result

The qualified CURRENT63 capture produced **63 distinct App diagnostics in 10 files**, with compiler exit `2`, stdout length `13,144` bytes, and stderr length `0`. `TS2688` count is **0** and Composition `TS2305` count is **0**. The actual table matches the previously provisional **52 / 4 / 7** split exactly:

| Diagnostic group | Files | Count | Codes | Boundary/recipient |
| --- | ---: | ---: | --- | --- |
| App2 transcript helper (`transcriptAssociateCapture.ts`) | 1 | 52 | TS18046×3, TS18047×9, TS18048×5, TS18049×5, TS2322×4, TS2339×10, TS2345×5, TS2488×1, TS7006×7, TS7053×3 | App2 |
| HOME local narrowing/ES2020 | 2 | 4 | TS2339×2, TS2550×2 | HOME |
| Theme boundary | 7 | 7 | TS2345×7 | App/Viewing boundary; separate from HOME's four |
| **Total** | **10** | **63** |  |  |

### Existing file/code counts

| File | Count | Codes |
| --- | ---: | --- |
| `src/tools/travel-between-images/components/ShotTimelinePreview.tsx` | 1 | TS2345×1 |
| `src/tools/video-editor/commands/clipScalarGesture.ts` | 2 | TS2550×2 |
| `src/tools/video-editor/commands/transcriptAssociateCapture.ts` | 52 | TS18046×3, TS18047×9, TS18048×5, TS18049×5, TS2322×4, TS2339×10, TS2345×5, TS2488×1, TS7006×7, TS7053×3 |
| `src/tools/video-editor/components/CompactPreview.tsx` | 1 | TS2345×1 |
| `src/tools/video-editor/components/PropertiesPanel/VideoEditorAssetPanelSurface.tsx` | 1 | TS2345×1 |
| `src/tools/video-editor/components/TimelineEditorShellCore.tsx` | 1 | TS2345×1 |
| `src/tools/video-editor/compositions/TimelineRenderer.tsx` | 1 | TS2345×1 |
| `src/tools/video-editor/hooks/clip-editing/useClipDeletion.ts` | 2 | TS2339×2 |
| `src/tools/video-editor/hooks/useDerivedTimeline.ts` | 1 | TS2345×1 |
| `src/tools/video-editor/hooks/useRenderState.ts` | 1 | TS2345×1 |
| **Total** | **63** |  |

### Existing code totals

`TS18046×3`, `TS18047×9`, `TS18048×5`, `TS18049×5`, `TS2322×4`, `TS2339×12`, `TS2345×12`, `TS2488×1`, `TS2550×2`, `TS7006×7`, `TS7053×3`.

## Exact source, program, and graph metadata

- Source commit: `1a54d30521945c7ea1ab7148e840011c8893c78d`
- Source tree: `941ff4c78ea72a48f6e83f310e54a4258f45e24b`
- Compiler workdir at capture: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m4-type-selflink-private-overlay-one-check-r8/overlay/source` (removed after capture)
- Config: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m4-type-selflink-private-overlay-one-check-r8/overlay/source/tsconfig.app.json`
- TypeScript: `/home/user/work/app-m3-private13-normal-lock-install-units-r6-owned/node_modules/typescript/bin/tsc`, version `5.9.3`
- Node option: `--max-old-space-size=4096`
- Recorded argv: `/home/user/work/app-m3-private13-normal-lock-install-units-r6-owned/node_modules/typescript/bin/tsc -p tsconfig.app.json --noEmit`
- Preflight: `PASS`; program root names: `2549`; compiler invocations: `1`; exit: `2`
- Protected graph: `/home/user/work/app-m3-private13-normal-lock-install-units-r6-owned/node_modules`
- The default shared App worktree dependency graph is obsolete for this evidence (`10`); it was not used or treated as a source of diagnostics.
- Composition package: version `0.0.13`; declaration origin `/home/user/work/app-m3-private13-normal-lock-install-units-r6-owned/node_modules/@banodoco/timeline-composition/dist/evaluation.d.ts`; runtime origin `/home/user/work/app-m3-private13-normal-lock-install-units-r6-owned/node_modules/@banodoco/timeline-composition/dist/evaluation.js`
- Composition archive: `vendor/artifacts/banodoco-timeline-composition-0.0.13.tgz`, SHA-256 `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`; **77/77** regular archive members matched installed bytes
- Actual import-origin proof: the five checked App importers resolved the private13 declaration/runtime origins above; all four expected symbols were present in the declaration checker
- Owned thin overlay: `422` retained root links and `23` retained type links; no bad retained targets; the invalid nested `@types` self-alias was omitted only in the private overlay
- Protected graph manifest: **32,365 entries**, unchanged before/after. Before and after manifest SHA-256: `189c9cd8287f584b11872e3b0724630b32bf989d52622569776ecca65b5b9c00`
- Raw stdout SHA-256: `7ecb8f2c4c6b3c549fc438866a611c206ba2e5ecfb86465a3825afafdd486267`

Evidence files retained at:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m4-type-selflink-private-overlay-one-check-r8/notes/`

In particular: `tsc.stdout`, `tsc.stderr`, `preflight.txt`, `compiler-context.txt`, `overlay-proof.txt`, `composition-77-members.txt`, `diagnostic-file-code-counts.txt`, `protected-before.manifest.sha256`, `protected-after.manifest.sha256`, and `postmanifest.txt`.

## Withdrawn old71 evidence

The old 71-diagnostic output is **invalid for current13 and must not drive repairs**. Its source was the older commit `cd5080bdca2a4baae81b2546de739f4b44326a59` / tree `f6b21d70ce85529121cdf8f2092368c8b521eda3`; the capture omitted `cd` into the source directory and resolved shared Composition `0.0.10`. Its eight `TS2305` export errors are therefore not current evidence. The current13 qualified run has `TS2305=0` and uses the direct private13 origins recorded above.

## Raw compiler stdout (verbatim)

```text
src/tools/travel-between-images/components/ShotTimelinePreview.tsx(232,40): error TS2345: Argument of type 'ResolvedTimelineConfig' is not assignable to parameter of type 'TimelineConfig'.
  Types of property 'theme' are incompatible.
    Type 'string | undefined' is not assignable to type 'string'.
      Type 'undefined' is not assignable to type 'string'.
src/tools/video-editor/commands/clipScalarGesture.ts(24,32): error TS2550: Property 'hasOwn' does not exist on type 'ObjectConstructor'. Do you need to change your target library? Try changing the 'lib' compiler option to 'es2022' or later.
src/tools/video-editor/commands/clipScalarGesture.ts(24,76): error TS2550: Property 'hasOwn' does not exist on type 'ObjectConstructor'. Do you need to change your target library? Try changing the 'lib' compiler option to 'es2022' or later.
src/tools/video-editor/commands/transcriptAssociateCapture.ts(72,3): error TS2322: Type 'unknown' is not assignable to type 'ObjectValue'.
src/tools/video-editor/commands/transcriptAssociateCapture.ts(77,3): error TS2322: Type 'unknown' is not assignable to type 'string'.
src/tools/video-editor/commands/transcriptAssociateCapture.ts(88,18): error TS18046: 'value' is of type 'unknown'.
src/tools/video-editor/commands/transcriptAssociateCapture.ts(89,14): error TS18046: 'value' is of type 'unknown'.
src/tools/video-editor/commands/transcriptAssociateCapture.ts(90,21): error TS18046: 'value' is of type 'unknown'.
src/tools/video-editor/commands/transcriptAssociateCapture.ts(119,7): error TS18048: 'content' is possibly 'undefined'.
src/tools/video-editor/commands/transcriptAssociateCapture.ts(119,66): error TS18048: 'content' is possibly 'undefined'.
src/tools/video-editor/commands/transcriptAssociateCapture.ts(124,65): error TS18048: 'content' is possibly 'undefined'.
src/tools/video-editor/commands/transcriptAssociateCapture.ts(124,83): error TS18048: 'content' is possibly 'undefined'.
src/tools/video-editor/commands/transcriptAssociateCapture.ts(127,25): error TS18048: 'content' is possibly 'undefined'.
src/tools/video-editor/commands/transcriptAssociateCapture.ts(134,43): error TS2322: Type '{ schema: "media.transcript/v1"; media_id: string; source_id: string; segments: { id: string; start: number; end: number; text: string; speaker?: string | null | undefined; words?: { id: string; start: number; end: number; text: string; }[] | undefined; }[]; } | undefined' is not assignable to type '{ schema: "media.transcript/v1"; media_id: string; source_id: string; segments: { id: string; start: number; end: number; text: string; speaker?: string | null | undefined; words?: { id: string; start: number; end: number; text: string; }[] | undefined; }[]; }'.
  Type 'undefined' is not assignable to type '{ schema: "media.transcript/v1"; media_id: string; source_id: string; segments: { id: string; start: number; end: number; text: string; speaker?: string | null | undefined; words?: { id: string; start: number; end: number; text: string; }[] | undefined; }[]; }'.
src/tools/video-editor/commands/transcriptAssociateCapture.ts(192,27): error TS2345: Argument of type 'string | number | true | JSON[] | { [key: string]: JSON; }' is not assignable to parameter of type 'object'.
  Type 'string' is not assignable to type 'object'.
src/tools/video-editor/commands/transcriptAssociateCapture.ts(192,63): error TS2345: Argument of type 'string | number | true | JSON[] | { [key: string]: JSON; }' is not assignable to parameter of type 'object'.
  Type 'string' is not assignable to type 'object'.
src/tools/video-editor/commands/transcriptAssociateCapture.ts(293,30): error TS2345: Argument of type 'JSON' is not assignable to parameter of type 'string'.
  Type 'null' is not assignable to type 'string'.
src/tools/video-editor/commands/transcriptAssociateCapture.ts(295,18): error TS2345: Argument of type 'JSON' is not assignable to parameter of type 'string'.
  Type 'null' is not assignable to type 'string'.
src/tools/video-editor/commands/transcriptAssociateCapture.ts(300,23): error TS2488: Type 'string | number | boolean | JSON[] | { [key: string]: JSON; }' must have a '[Symbol.iterator]()' method that returns an iterator.
src/tools/video-editor/commands/transcriptAssociateCapture.ts(300,23): error TS18047: 'clips' is possibly 'null'.
src/tools/video-editor/commands/transcriptAssociateCapture.ts(304,28): error TS18047: 'clips' is possibly 'null'.
src/tools/video-editor/commands/transcriptAssociateCapture.ts(304,34): error TS2339: Property 'flatMap' does not exist on type 'string | number | boolean | JSON[] | { [key: string]: JSON; }'.
  Property 'flatMap' does not exist on type 'string'.
src/tools/video-editor/commands/transcriptAssociateCapture.ts(304,43): error TS7006: Parameter 'clip' implicitly has an 'any' type.
src/tools/video-editor/commands/transcriptAssociateCapture.ts(307,34): error TS18047: 'clips' is possibly 'null'.
src/tools/video-editor/commands/transcriptAssociateCapture.ts(307,40): error TS2339: Property 'entries' does not exist on type 'string | number | boolean | JSON[] | { [key: string]: JSON; }'.
  Property 'entries' does not exist on type 'string'.
src/tools/video-editor/commands/transcriptAssociateCapture.ts(330,22): error TS18047: 'nextClips' is possibly 'null'.
src/tools/video-editor/commands/transcriptAssociateCapture.ts(330,22): error TS7053: Element implicitly has an 'any' type because expression of type 'any' can't be used to index type 'string | number | boolean | JSON[] | { [key: string]: JSON; }'.
src/tools/video-editor/commands/transcriptAssociateCapture.ts(380,3): error TS2322: Type 'JSON | undefined' is not assignable to type 'ObjectValue'.
  Type 'undefined' is not assignable to type 'ObjectValue'.
src/tools/video-editor/commands/transcriptAssociateCapture.ts(438,24): error TS18047: 'refs' is possibly 'null'.
src/tools/video-editor/commands/transcriptAssociateCapture.ts(438,29): error TS2339: Property 'associations' does not exist on type 'string | number | boolean | JSON[] | { [key: string]: JSON; }'.
  Property 'associations' does not exist on type 'string'.
src/tools/video-editor/commands/transcriptAssociateCapture.ts(439,36): error TS7006: Parameter 'row' implicitly has an 'any' type.
src/tools/video-editor/commands/transcriptAssociateCapture.ts(440,20): error TS7006: Parameter 'owner' implicitly has an 'any' type.
src/tools/video-editor/commands/transcriptAssociateCapture.ts(441,24): error TS7006: Parameter 'row' implicitly has an 'any' type.
src/tools/video-editor/commands/transcriptAssociateCapture.ts(444,39): error TS7006: Parameter 'row' implicitly has an 'any' type.
src/tools/video-editor/commands/transcriptAssociateCapture.ts(455,20): error TS18047: 'sourceMap' is possibly 'null'.
src/tools/video-editor/commands/transcriptAssociateCapture.ts(455,20): error TS7053: Element implicitly has an 'any' type because expression of type '"astrid.transcript_segment/v1"' can't be used to index type 'string | number | boolean | JSON[] | { [key: string]: JSON; }'.
  Property 'astrid.transcript_segment/v1' does not exist on type 'string | number | boolean | JSON[] | { [key: string]: JSON; }'.
src/tools/video-editor/commands/transcriptAssociateCapture.ts(462,42): error TS2345: Argument of type 'JSON | undefined' is not assignable to parameter of type 'ObjectValue'.
  Type 'undefined' is not assignable to type 'ObjectValue'.
src/tools/video-editor/commands/transcriptAssociateCapture.ts(477,37): error TS7006: Parameter 'row' implicitly has an 'any' type.
src/tools/video-editor/commands/transcriptAssociateCapture.ts(484,3): error TS18047: 'nextRefs' is possibly 'null'.
src/tools/video-editor/commands/transcriptAssociateCapture.ts(484,12): error TS2339: Property 'associations' does not exist on type 'string | number | boolean | JSON[] | { [key: string]: JSON; }'.
  Property 'associations' does not exist on type 'string'.
src/tools/video-editor/commands/transcriptAssociateCapture.ts(484,48): error TS7006: Parameter 'row' implicitly has an 'any' type.
src/tools/video-editor/commands/transcriptAssociateCapture.ts(485,3): error TS18047: 'nextRefs' is possibly 'null'.
src/tools/video-editor/commands/transcriptAssociateCapture.ts(485,12): error TS2339: Property 'associations' does not exist on type 'string | number | boolean | JSON[] | { [key: string]: JSON; }'.
  Property 'associations' does not exist on type 'string'.
src/tools/video-editor/commands/transcriptAssociateCapture.ts(487,3): error TS18047: 'nextMap' is possibly 'null'.
src/tools/video-editor/commands/transcriptAssociateCapture.ts(487,3): error TS7053: Element implicitly has an 'any' type because expression of type '"astrid.transcript_segment/v1"' can't be used to index type 'string | number | boolean | JSON[] | { [key: string]: JSON; }'.
  Property 'astrid.transcript_segment/v1' does not exist on type 'string | number | boolean | JSON[] | { [key: string]: JSON; }'.
src/tools/video-editor/commands/transcriptAssociateCapture.ts(492,14): error TS18049: 'config' is possibly 'null' or 'undefined'.
src/tools/video-editor/commands/transcriptAssociateCapture.ts(492,21): error TS2339: Property 'clips' does not exist on type 'string | number | boolean | JSON[] | { [key: string]: JSON; }'.
  Property 'clips' does not exist on type 'string'.
src/tools/video-editor/commands/transcriptAssociateCapture.ts(494,82): error TS18049: 'config' is possibly 'null' or 'undefined'.
src/tools/video-editor/commands/transcriptAssociateCapture.ts(494,89): error TS2339: Property 'clips' does not exist on type 'string | number | boolean | JSON[] | { [key: string]: JSON; }'.
  Property 'clips' does not exist on type 'string'.
src/tools/video-editor/commands/transcriptAssociateCapture.ts(494,99): error TS18049: 'config' is possibly 'null' or 'undefined'.
src/tools/video-editor/commands/transcriptAssociateCapture.ts(494,106): error TS2339: Property 'clips' does not exist on type 'string | number | boolean | JSON[] | { [key: string]: JSON; }'.
  Property 'clips' does not exist on type 'string'.
src/tools/video-editor/commands/transcriptAssociateCapture.ts(498,31): error TS18049: 'config' is possibly 'null' or 'undefined'.
src/tools/video-editor/commands/transcriptAssociateCapture.ts(498,38): error TS2339: Property 'app' does not exist on type 'string | number | boolean | JSON[] | { [key: string]: JSON; }'.
  Property 'app' does not exist on type 'string'.
src/tools/video-editor/commands/transcriptAssociateCapture.ts(498,45): error TS18049: 'config' is possibly 'null' or 'undefined'.
src/tools/video-editor/commands/transcriptAssociateCapture.ts(498,52): error TS2339: Property 'app' does not exist on type 'string | number | boolean | JSON[] | { [key: string]: JSON; }'.
  Property 'app' does not exist on type 'string'.
src/tools/video-editor/components/CompactPreview.tsx(46,40): error TS2345: Argument of type 'ResolvedTimelineConfig' is not assignable to parameter of type 'TimelineConfig'.
  Types of property 'theme' are incompatible.
    Type 'string | undefined' is not assignable to type 'string'.
      Type 'undefined' is not assignable to type 'string'.
src/tools/video-editor/components/PropertiesPanel/VideoEditorAssetPanelSurface.tsx(47,40): error TS2345: Argument of type 'ResolvedTimelineConfig' is not assignable to parameter of type 'TimelineConfig'.
  Types of property 'theme' are incompatible.
    Type 'string | undefined' is not assignable to type 'string'.
      Type 'undefined' is not assignable to type 'string'.
src/tools/video-editor/components/TimelineEditorShellCore.tsx(578,40): error TS2345: Argument of type 'ResolvedTimelineConfig' is not assignable to parameter of type 'TimelineConfig'.
  Types of property 'theme' are incompatible.
    Type 'string | undefined' is not assignable to type 'string'.
      Type 'undefined' is not assignable to type 'string'.
src/tools/video-editor/compositions/TimelineRenderer.tsx(1625,75): error TS2345: Argument of type 'ResolvedTimelineConfig' is not assignable to parameter of type 'TimelineConfig'.
  Types of property 'theme' are incompatible.
    Type 'string | undefined' is not assignable to type 'string'.
      Type 'undefined' is not assignable to type 'string'.
src/tools/video-editor/hooks/clip-editing/useClipDeletion.ts(11,30): error TS2339: Property 'ownerRef' does not exist on type 'object'.
src/tools/video-editor/hooks/clip-editing/useClipDeletion.ts(12,29): error TS2339: Property 'clipRef' does not exist on type 'object'.
src/tools/video-editor/hooks/useDerivedTimeline.ts(71,9): error TS2345: Argument of type 'ResolvedTimelineConfig' is not assignable to parameter of type 'TimelineConfig'.
  Types of property 'theme' are incompatible.
    Type 'string | undefined' is not assignable to type 'string'.
      Type 'undefined' is not assignable to type 'string'.
src/tools/video-editor/hooks/useRenderState.ts(596,53): error TS2345: Argument of type 'ResolvedTimelineConfig' is not assignable to parameter of type 'TimelineConfig'.
  Types of property 'theme' are incompatible.
    Type 'string | undefined' is not assignable to type 'string'.
      Type 'undefined' is not assignable to type 'string'.
```

## Limits and next steps

- This is a diagnostic handoff, not a fix and not a clean typecheck claim.
- No App source, package, lockfile, test, compiler, build, install, browser, or full-suite change was made here.
- Do not re-run the compiler or reanalyze old71 as part of consuming this handoff. Use the raw CURRENT63 lines and the ownership/file counts above to scope the next repair review.
