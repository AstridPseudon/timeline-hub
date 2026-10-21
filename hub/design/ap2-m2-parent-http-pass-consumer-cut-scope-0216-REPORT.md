# AP2-M2 parent HTTP pass consumer-cut scope

## Decision

**No App deletion is qualified.** The assigned worktree is unchanged. Result
`13087` is a Runtime/Agent HTTP/provider proof for parent media **swap**; it is
not proof that a mounted App prepared-File gesture reaches that operation, so it
does not make an App writer dead.

The candidate cut named by the executor report remains only a candidate: the
parent clip-swap branch that can reach the legacy whole-document
`saveTimelineAtHead` persistence path. I did not remove it, and I did not remove
the shared `saveTimelineAtHead` implementation. The deletion ledger remains
open for the parent-media row.

## What result13087 actually proves

The central request was:

```sh
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test \
  ap2-m2-parent-frozen-source-single-gate-0138 \
  normal014-integration-parent-media-accepted --no-cache)
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test \
  ap2-m2-parent-frozen-source-single-gate-0138-normal014-integration-parent-media-accepted-1021021211-13087 10
```

It ran:

```text
env NORMAL014_PROFILE=final95 NORMAL014_APP_SOURCE=parent \
  bash design/normal014-parent-media-central.sh run
```

Result: **1 passed in 1.41s; central run exit 0 in 146s** on App source
`25155ccb22728780a3ecd6379a929cad75cc1400` / tree
`972d2ed2e4f85f334eb9f2e6ca40d9bfbce9eac7`, with the approved final6ef Agent
and 95bd Runtime/producer tuple.

The executed test was
`tests/test_timeline_clip_replacement.py::test_native_parent_clip_swap_route_replaces_parent_media`.
Its actual command/request shape is:

- Agent captures `clip.swap-media` v1 with `select: parent/clip:<id>`,
  `args.old_media`, `args.media`, and `{ownership: parent}`.
- The Runtime test builds the native commit body and submits it through the
  parent-ownership commit helper (`_native_parent_ownership_commit`), not
  through a browser-mounted App or App `File`/`DataTransfer` event.
- It asserts only that the result is `accepted` or `rebased` and that the
  canonical parent clip asset becomes the new asset.

The source-level native assertions retained by the reviewed Agent/App swap
implementation include exact old/new five-field media dependencies, parent
clip/track/asset reads, fixed parent ownership, two writes, raw clip-field
replacement, mirror equality, JSON replay, and refusal for changed original
media, missing/mismatched verified media, duration/alias conflicts, unsupported
stand-ins, or conflicting registry mirrors. Those are native/provider semantics,
not mounted App caller evidence.

The result contains no App browser request trace. It does not prove App
`commands.addClip`, App `handleAssetDrop`, App `useExternalDrop`, App
`useTimelineState` wiring, or an App `parentClipSwapMediaPort` caller.

## Evidence not present in result13087

Result13087 does **not** establish any of the following for an App consumer:

- mounted File/DataTransfer gesture ingress;
- App request body/source assertions;
- client or Runtime restart/reload recovery;
- lost-ack exact retry and original key/body/receipt;
- guarded App undo/redo;
- duplicate prevention and opaque-data preservation through the mounted path;
- zero legacy snapshot/save traffic.

The executor report explicitly says no local browser, full suite, second central
run, pin adoption, or public activation was performed. The earlier mounted
prepared-File gate is a different operation and is not a substitute.

## Exact existing mounted driver and first blocker

The existing prepared-gesture driver is:

```text
tests/e2e/local/support/run-parent-manual-drop-evidence.sh
```

It selects this existing Playwright case in
`tests/e2e/local/three-products.spec.ts`:

```text
M2 real mounted manual video drop: Runtime selection refusal is closed, native ADD recovers exactly, and undo preserves opaque data
```

That journey is a **parent `clip.add-media`** File drop. Its retained assertions
inspect media-import, media-selection and verified-selection requests, the
`clip.add-media` commit body, selection identity, lost ACK, reload, Runtime
restart, exact retry, follow-up edit, guarded undo, opaque data, and
`wire.legacy === []`. It is therefore the correct existing driver for a future
mounted **ADD** qualification, but it cannot qualify result13087's **SWAP**
operation.

Its first recorded blocker, from the one allowed central run, was before the
positive native ADD path: the deliberately wrong verified selection returned
HTTP **422**, while the test expected **404 or 409** at
`three-products.spec.ts:1172`. The positive add, lost-ACK/restart/retry/reload,
undo, and zero-legacy assertions did not run. No rerun was made, and this task
does not rerun or modify that driver.

## App caller/source census

The reviewed prepared-ADD path has these live callers and wiring points:

- `src/tools/video-editor/hooks/useAssetManagement.ts` — `placePreparedAsset`
  routes qualified prepared video to native `commands.addClip`, visibly refuses
  missing selection/carrier/native refusal, and preserves placement/removal
  intent.
- `src/tools/video-editor/lib/external-drop-utils.ts` — `handleFileDrop` and
  generation/general asset helpers await and propagate the placement result.
- `src/tools/video-editor/hooks/useExternalDrop.ts` — dispatch and mounted drop
  callback await the result before seeking.
- `src/tools/video-editor/hooks/useTimelineState.ts` — supplies the existing
  provider-bound `parentMediaCommands` construction to the asset manager.
- `src/tools/video-editor/hooks/useTimelineCommandsService.ts` — constructs
  the provider-bound verified-media runtime and the native prepared-ADD facade.
- `src/tools/video-editor/commands/commitSession.ts` and
  `src/tools/video-editor/hooks/useTimelineCommandSession.ts` — own the
  prepared parent ADD/SWAP capture ports and durable submission plumbing.

For **SWAP**, the App source census finds only the port/plumbing and focused
tests (`parentClipSwapCapture.ts`, `commitSession.ts`,
`useTimelineCommandSession.ts`, and their tests). There is no production App
gesture caller that captures and submits `parentClipSwapMediaPort`. The
existing legacy whole-document writer remains live through
`useTimelinePersistence.ts:401-407` and the broader App writer families listed
in `design/app-writers.md`; popup `shotTimelineDataProvider.ts` is a separate
shot-graph writer and is not made dead by the parent HTTP swap proof.

The exact reviewed source pair needed for a future mounted ADD qualification is
`useAssetManagement.ts` plus its mounted construction in `useTimelineState.ts`,
with `external-drop-utils.ts`/`useExternalDrop.ts` as the required caller
neighbors. A future SWAP deletion needs a real existing mounted SWAP caller and
its reviewed source pair first; none exists in the current App tree, and this
task does not invent one or add a wrapper.

## Checks and changes

- `git status --short --branch` — clean; no App product files changed.
- No targeted test was run because this worker made no source/test change.
- Existing evidence consulted: executor-0210 central result **1 passed**;
  prepared-consumer focused source suite **4 files, 43 tests passed**;
  final row-local seam review **45 controls/types/lint/shell/diff passed**;
  prior mounted gate **failed at the 422-vs-404/409 first assertion**.
- No browser/socket/full/proof replay was run by this worker.

## Blocker / next step

The first blocker is operation and ingress mismatch: result13087 is native
parent SWAP, while the only existing mounted prepared-gesture driver is parent
ADD, and the App has no production SWAP caller. Resolve the existing mounted
ADD gate's settled 422 refusal expectation and obtain its complete acceptance,
reload/retry/undo, and zero-legacy evidence before cutting the ADD writer. For
the SWAP leaf, first provide an existing reviewed mounted SWAP caller/source
pair and its matching gesture proof; do not infer it from result13087.

