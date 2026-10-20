# AP2 M2 ordinary proposal consumer native source

Date: 2026-10-20

## Result

The exact live proposal acceptance ingress is:

`ProposalPanel → ProposalRuntime.accept → TimelineOps.apply → useTimelineOps`

The current source already has the approved migration at that door. `useTimelineOps.apply` classifies the complete `TimelinePatch`; supported and mixed patches use the existing `genericPatchPort` capture/finish/submit path, while an all-unsupported patch retains the central snapshot fallback required by the qualified-writer report. No separate proposal snapshot writer exists to delete safely: `ProposalRuntime.accept` delegates exclusively to `TimelineOps.apply` and marks the proposal accepted only after that call succeeds.

This worker added two focused live-ingress regressions in
`src/tools/video-editor/hooks/useTimelineOps.test.ts`:

- A supported two-member proposal preserves its source/meta/order and is submitted as one native batch; `commitData` receives zero calls and the proposal becomes accepted.
- A mixed `clip.update` + `project-data.write` proposal is refused at native capture; finish/submit and `commitData` receive zero calls, and the proposal remains pending.

Literal unsupported counterexample: `project-data.write` targeting `com.example.producer` is not a native film command. It must remain on the central fallback until the paired Agent/Runtime project-data contract exists. The test deliberately uses this operation beside a supported clip hold to prove atomic mixed refusal and draft preservation.

No HOME-owned shared session/provider/store seam was changed. No Main behavior was removed. No DTO, store, framework, schema, pin, activation, private operation, browser/socket test, or full suite was added.

## Assertion mapping

The existing proposal lifecycle positive at
`src/tools/video-editor/lib/proposal-runtime.test.ts` (`accepts a pending proposal with matching baseVersion`) remains unchanged. Its mock `TimelineOps.apply`/accepted-state assertion is mapped one-to-one by the new live-adapter positive at
`src/tools/video-editor/hooks/useTimelineOps.test.ts` (`accepts a supported proposal through one native batch without snapshot traffic`). The new assertion adds the production adapter boundary and zero-snapshot-traffic proof; no old assertion was removed, skipped, weakened, or converted to a fake deletion row.

## Tests

Passed:

```text
./node_modules/.bin/vitest run --config config/testing/vitest.config.ts --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/hooks/useTimelineOps.test.ts src/tools/video-editor/commands/genericPatchCapture.test.ts src/tools/video-editor/lib/proposal-runtime.test.ts
# 3 files, 156 tests passed

./node_modules/.bin/vitest run --config config/testing/vitest.config.ts --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/commands/commitSession.genericPatch.test.ts src/tools/video-editor/hooks/useTimelineCommandSession.test.ts src/tools/video-editor/hooks/useTimelineCommandSession.projection.test.tsx
# 3 files, 53 tests passed

./node_modules/.bin/eslint src/tools/video-editor/hooks/useTimelineOps.ts src/tools/video-editor/hooks/useTimelineOps.test.ts src/tools/video-editor/commands/genericPatchCapture.ts src/tools/video-editor/commands/genericPatchCapture.test.ts src/tools/video-editor/lib/proposal-runtime.ts src/tools/video-editor/lib/proposal-runtime.test.ts --max-warnings 0
# passed

./node_modules/.bin/tsc --noEmit --pretty false
# passed

git diff --check
# passed
```

Not run: browser, localhost, live sockets, request-test, full suite, build, or Runtime HTTP. The neighboring command-session suite uses its existing fake transport and passed; no claim is made here about a live Runtime door.

## Blockers / next steps

No implementation blocker for this proposal ingress. The remaining central fallback is intentionally live for fully unsupported proposals and other artifact/config families named in `ap2-m2-ordinary-qualified-writer-deletion-v2-REPORT.md`. It should only be removed by the shared owner after those families have native recipes and independent one-to-one assertion review.
