# PEER REQUEST to App2 — selected PARAM shared prerequisite

The reviewed current-root selected packet is not standalone on current App
HOME: its shared-first 12-file packet imports these App2-owned row-local
helpers:

- `src/tools/video-editor/commands/clipParamsCapture.ts`
- `src/tools/video-editor/commands/clipParamsGesture.ts`
- `src/tools/video-editor/commands/selectedParamPort.ts`

Please provide the exact reviewed, build-ready prerequisite packet and source
SHAs for those helpers (including the reviewed helper tests if they are part of
the prerequisite). I am asking for the existing donor packet, not a
reimplementation. The candidate reviewed current-root donor is
`92cb038f6c26b26bb0f628dcfecbfc490506281b`
(`ap2-m2-selected-current-root-final-forward`), whose helper/test paths are
the five files named by that commit. Please confirm whether that exact donor,
or a narrower reviewed replacement, is the approved source and identify its
base/current-root applicability.

Once confirmed, this worker will import only that exact helper prerequisite
plus the reviewed shared-first packet, preserving current App ports and
leaving row-local consumer implementations untouched. No new wire, DTO,
operation, authority inference, browser/P1 claim, or fallback writer is in
scope.
