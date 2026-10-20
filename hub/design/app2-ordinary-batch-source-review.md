# D01-app-ordinary-batch — source handoff review

## Verdict

**Handoff is actionable but held for one upstream contract prerequisite.** The
ordinary row is still OPEN; no now-live ordinary App row was found. D01
transition-none and D01 shot-graph-settings are live/retained by App and are
outside this handoff. The shared `useTimelineOps`/command-session seam remains
App-owned and must be integrated by agreement.

Reviewed source identities:

- App base `hub/timeline/app/tl/app-m2-ordinary028-current-safety-compose`,
  commit `55e7e217b4adc2c57315e22ce0bebfc36a436ffa`, tree
  `1976a2f180b9927fe4679822aac2413f7be37ca8`.
- Reviewed current-root candidate `b1ef4b9b910ba72375c34cf319692f90d22edc25`,
  tree `8d8a10b057ed31fed69517e18a23b8ec3811447a`.
- Old staged generic helper only: branch
  `hub/timeline/app/tl/app-m2-generic-ops-native-batch-stage`, commit
  `3c8e2f347dfd1cc9e174196a0d75e44f7e6049e4`. This is a source pattern, not an
  adoption pin/cohort.
- Fixed producer pair checked read-only: Agent `d8749a9ce12a699672faf3ad96b4e4cbea9245c2`,
  tree `75354d38c898729bac09619679f5421faba319ed`; Runtime
  `2c4ac180c2220bdad966bc01e95ad230e99ce26a`, tree
  `7ab412cc4bcbe517efcfa806e092336390312e18`.

## Current live path

`src/tools/video-editor/hooks/useTimelineOps.ts:226-307` does the complete
local stale/version check and full-batch validation, then compiles with
`compileTimelinePatch`. A single label-only `track.update` is routed through
`trackLabelPort` (`:283-295`); every other valid patch still calls
`commitData(compiled.nextData, { save: true, semantic: true })` (`:298-303`).
That is the D01 snapshot ingress.

The same `TimelineOps.apply` is used by proposal acceptance
(`src/tools/video-editor/lib/proposal-runtime.ts:503-566`) and by the compiler
canary. `compiler-canary.ts:421-442` deliberately builds all DSL/source-map
`project-data.write` operations into one `dataPatch` and calls `timeline.apply`
once. It then creates a separate clip proposal (`:444-475`). Do not turn the
first batch into one submission per source-map entry.

Additional durable ordinary callers remain outside `useTimelineOps`: project
transcript association/import (`src/tools/video-editor/lib/project-transcript-host.ts:628-652`)
and persisted data-kind replacement (`src/tools/video-editor/data-kinds/dataKindItems.ts:50-58`).
They still build `TimelineData` with `buildDataFromCurrentRegistry` and call
`commitData`; they are not covered by a label/hold-only cut.

## Reusable source and limits

The old staged `genericPatchCapture.ts` contains the useful shape:

- `captureGenericPatch` freezes the original patch, resolves every owner before
  submission, executes members sequentially against one local authored bundle,
  and raises `GenericPatchRefusal` for the complete batch when any member is
  unsupported or fails.
- `GenericPatchCapturePort` separates `capture`, `finish`, and `submit`.
  The staged `commitSession.ts` stores the complete command list in the
  existing `prepared` map and calls the existing `enqueue` once, so one
  outbox intent/commit/inverse is retained.
- `projectGenericPatchPreview` is the right local-only projection seam for
  preserving displayed values and unrelated opaque state.

Do not copy that helper unchanged. It is hard-coded to exactly parent label
`track.update` and positive `clip.update {hold}`; it imports the old
`clipScalarCapture` path, which is absent from reviewed root `b1ef4b9b`. Its
golden fixture and “027” parity claims are historical only.

The fixed Agent/Runtime pair has native `track.set`, `clip.set`,
`clip.set-params`, `clip.set-element`, `clip.move`, `clip.add`, `clip.trim`,
and related commands. It has **no** native `project-data.write`, transcript,
data-kind, or seam operation. Therefore the old helper cannot close this row,
and no App-only mapper can honestly make the source-map/transcript families
native.

## Exact minimal seam for App integration

Keep the seam private to the existing App command/session files; do not add a
DTO, endpoint, second writer, or public SDK method.

1. Add a `GenericPatchCapturePort`-shaped port to the existing
   `TimelineCommandSession` return object in `src/tools/video-editor/commands/commitSession.ts`.
   Its implementation must use the current `prepared` map and `enqueue`, with
   one `Payload.commands` array and one local authored-bundle execution. Map
   only operations covered by the fixed Agent producer contract. Capture all
   members before owner resolution has any side effect; preserve patch order
   (including the public `order` semantics) and refuse the whole input if any
   member is unsupported.
2. Expose that port through
   `src/tools/video-editor/hooks/useTimelineCommandSession.ts`, with the same
   `legacyClean` gate currently applied to the label port. Pass it from
   `useTimelineState.ts` into `useTimelineOps` as one optional host seam.
3. In `useTimelineOps.apply`, retain the existing editable check, stale-base
   check, and full `validateTimelinePatch` call. When the generic port is
   available, capture/finish/submit the **complete patch** and return its
   native local diff. A mixed supported/unsupported patch must raise one
   refusal before preview, outbox append, or `commitData`; never filter the
   supported members or submit them independently. Keep
   `previewTimelinePatch`/`compileTimelinePatch` as pure diagnostic/preview
   utilities until every ordinary operation family has a native producer.
4. Leave `compiler-canary.ts` unchanged. Its source/source-map `dataPatch`
   must remain one `TimelineOps.apply` batch, and its main clip proposal must
   remain one proposal accepted through the same seam. If the current fixed
   producer pair cannot accept the data batch, fail the whole batch visibly and
   retain the proposal/draft; do not split it into per-key submissions.

Local-vs-App boundary: capture/execute/preview are pure App command helpers;
the App session owns the outbox, retry identity, local projection, and one
`/v1` request. Runtime receives the existing `commands[]` request unchanged.
The only cross-repo prerequisite is a reviewed Agent producer revision plus
matching Runtime registration for the missing project-data/transcript/data-kind
ordinary operation(s). Do not add a new wire field until that producer design
has an executable requirement.

## Deletion boundary

After all ordinary operation families have native producers and the mixed-batch
acceptance proof is green:

- Delete the label-only special case in
  `src/tools/video-editor/hooks/useTimelineOps.ts:283-295` and its now-unused
  `captureTrackLabelEdit`/`submitTrackLabelEdit` imports from this adapter.
- Delete the legacy snapshot branch in
  `src/tools/video-editor/hooks/useTimelineOps.ts:298-303`.
- Retain `validateTimelinePatch`, pure preview/diagnostic compilation, and the
  compiler-canary producer. Do not delete `project-transcript-host.ts`,
  `dataKindItems.ts`, or `timeline-save-utils.ts` until their missing native
  producer contracts and callers are separately covered; deleting them now
  would lose required transcript/data-kind behavior.

## Acceptance commands

1. App local targeted lane (no browser/socket):

   `node_modules/.bin/vitest run --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/hooks/useTimelineOps.test.ts src/tools/video-editor/hooks/useTimelineOps.trackLabel.test.ts src/tools/video-editor/lib/compiler-canary.test.ts src/tools/video-editor/commands/genericPatchCapture.test.ts src/tools/video-editor/commands/commitSession.genericPatch.test.ts`

   Required assertions: whole mixed refusal has no preview/outbox/commit,
   supported members become one command array/one outbox intent, lost-ACK
   retry reuses exact body/key, and compiler-canary source-map writes remain
   one batch.

2. Agent fixed-pair conformance in a private Agent archive:

   `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$AGENT_D874" /home/user/work/venv-agent/bin/python -m pytest -q tests/editing_conformance/test_recipe_scalar_commands.py tests/editing_conformance/test_recipe_clip_scalar_fields.py tests/editing_conformance/test_commit_runtime_clip_scalar_fields.py`

3. Runtime fixed-pair contract/ordinary acceptance:

   `PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python -m pytest -q tests/test_timeline_commit_validation.py tests/test_timeline_ordinary_http.py`

No browser, localhost, live socket, full suite, install, pin change, or
generated-contract change is part of this source handoff.

## Evidence run and blocker

Current App focused neighbors passed with the root-config form:

`node_modules/.bin/vitest run --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/hooks/useTimelineOps.test.ts src/tools/video-editor/hooks/useTimelineOps.trackLabel.test.ts src/tools/video-editor/lib/compiler-canary.test.ts`

Result: **3 files, 122 tests passed**.

The requested `--config config/testing/vitest.config.ts --configLoader=runner`
variant could not start because the repository config evaluates `__dirname`
under the runner loader (`ReferenceError: __dirname is not defined`). No
dependency was installed or modified.

Actual blocker: the fixed Agent `d8749a9c` / Runtime `2c4ac180` contract has no
native command for `project-data.write` or the transcript/data-kind/seam
ordinary families. App can stage the generic session seam for existing native
commands, but D01 cannot close, and compiler-canary source persistence cannot
be moved off snapshot writes, until that producer revision is reviewed and
paired.
