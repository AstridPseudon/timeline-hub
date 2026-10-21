# AP2-M2 bootstrap live-caller report correction

## Result

**Corrected; public disposition HELD.** The prior
`ap2-m2-bootstrap-only-current-home-port-REPORT.md:47` statement that there
was “no ... public activation change” was false. The source packet changed a
live initializer call path. HOME owns the already-directed revert; this worker
changed no App source, call path, pin, generated contract, or test.

## Actual diff and activation effect

The relevant source diff is the second-parent delivery of `b69c85ea7`
(`b69c85ea7^1..b69c85ea7^2`):

- `src/integrations/runtime/createDefaultTimeline.ts` replaced the live
  `publishEmptyTimeline`/`client.publishParentComposition` initializer with
  `RuntimeDataProvider.initializeNativeBootstrapTimeline`. Both exported
  `createCanonicalTimeline` and `ensureProjectHasTimeline` consequently use
  native create/init/commit.
- `src/integrations/runtime/dataProvider.ts` added the provider method and
  wires the configured `AstridRuntimeClient` to create, history, immutable
  parent reads, basis loading, and commit.
- `src/integrations/runtime/client.ts` added the live `createTimeline` wrapper.
- `src/integrations/runtime/bootstrapInitialization.ts` added the durable
  create/init boundary and its recovery path. It reserves the create request,
  then captures a native command batch and posts `/commit`.
- `src/tools/video-editor/commands/bootstrapCapture.ts` emits
  `timeline.init@1` followed by `track.create@1` records.
- `src/tools/video-editor/commands/commitOutbox.ts` added the create-owner and
  initialization retention surfaces used by the live initializer.

This is not an inert source-only helper: a live initializer invokes the helper
chain and reaches the incompatible command.

## Changed exports/surfaces and live product callers

The following is the required caller inventory. The grep excluded tests,
`tests/**`, `__tests__/**`, and vendor trees.

| Changed export/surface | Live product caller(s) | Live effect |
| --- | --- | --- |
| `createCanonicalTimeline` | `src/tools/video-editor/pages/VideoEditorPage.tsx:551`; internal call from `createDefaultTimeline.ts:108` | Additional timeline creation enters native bootstrap. |
| `ensureProjectHasTimeline` | `src/shared/hooks/projects/useProjectCRUD.ts:154`; `src/tools/video-editor/pages/VideoEditorPage.tsx:461`; internal call from `createDefaultTimeline.ts:108` | Project creation and first/headless repair enter native bootstrap. |
| `RuntimeDataProvider.initializeNativeBootstrapTimeline` | `src/integrations/runtime/createDefaultTimeline.ts:64` | Configured provider invokes the native owner. |
| `initializeBootstrapTimeline` | `src/integrations/runtime/dataProvider.ts:78,503` | Live durable create/init/recovery boundary. |
| `reserveBootstrapInitialization` / `resumeBootstrapInitialization` | `src/integrations/runtime/bootstrapInitialization.ts:213,216-217` | Live reservation and recovery; `reserveBootstrapInitialization` calls `reserveCreate` at `:34`. |
| `captureBootstrap` | `src/integrations/runtime/bootstrapInitialization.ts:170` | Live command capture emits `timeline.init@1`. |
| `AstridRuntimeClient.createTimeline` | `src/integrations/runtime/dataProvider.ts:508` | Live create request before native commit. |
| `createCommitOutbox` / `reserveCreate` | `src/tools/video-editor/commands/commitSession.ts:133`; `src/integrations/runtime/bootstrapInitialization.ts:209` | Shared live outbox; bootstrap uses it directly. |

## Required operation versus exact pinned schema

The bootstrap packet requires this command cohort:

```text
timeline.init@1 (select=parent; args=name, slug, output)
track.create@1 ...
```

The App's exact public013 pin is recorded in `runtime.lock.json`:

```text
contract:       0.2.13
producer source: 2c4ac180c2220bdad966bc01e95ad230e99ce26a
producer:       sha256:6f000bc615a9cb24fb00cc69a97af75eae71006ebfe87e3caa272fcdbbb1af56
schema:         sha256:8de823011a121359b9ad021e283b45afb6baeabc8a154a02bd086d1260a8b8f4
server:         8f105c26e3b62f9c2683f717a9773a12bc775a8e
```

Its exact `contract/schemas/edit-command.json` contains `track.create` but
does not contain `timeline.init`; its generated TypeScript types contain no
`TimelineInitArgs`. The public HTTP operations `createTimeline` and
`commitTimeline` are transport methods, not evidence that the command
operation `timeline.init` is accepted. Therefore the native packet is not
compatible with the currently pinned public013 Runtime.

The private202 overlay is a separate cohort:

```text
Runtime server: 202074110717146fc7f08af2306a8dd7f695b0b1
producer:      a0dca16975dfe8f5e762703b99d9791a16cf7fd7
contract:      0.2.14
schema:        sha256:ce3781c282564b650890456f6c257f3faabe2de3898a84363fecd47e48b30d59
```

Its exact edit-command schema adds `timeline.init@1` and `TimelineInitArgs`.
A private202 activation overlay can qualify only that private pair; it is not
public013 readiness evidence and must remain explicitly labelled separately.

## Disposition

Source-only bootstrap evidence may remain privately qualified against the
matched private202 Agent/Runtime pair. Public use is **HELD** until HOME's
public call-path revert is in place and a matched Main014 Agent/Runtime/App
cohort is adopted with real create/init/restart proof. Do not claim public
activation, public writer retirement, or a public bootstrap gate from b69 or
its derived delivery reports.

## Checks and limits

Read-only evidence checks completed:

- `git -C /home/user/work/app diff b69c85ea7^1 b69c85ea7^2 -- <bootstrap source paths>` — PASS; confirmed the initializer replacement and added native surfaces.
- `rg` over App `src` excluding tests/vendor for every changed export listed above — PASS; caller inventory recorded here.
- `git -C /home/user/banodoco/banodoco-workspace-runtime show 2c4ac180...:contract/schemas/edit-command.json` and the corresponding generated metadata — PASS; public013 has no `timeline.init`/`TimelineInitArgs`.
- The corresponding `202074110717...` Runtime schema inspection — PASS; private202 has `timeline.init@1`/`TimelineInitArgs`.

Per the task boundary, no product tests, browser, socket, `request-test`, full
suite, pin/adoption, or new audit ceremony was run. The report correction is
documentation-only.
