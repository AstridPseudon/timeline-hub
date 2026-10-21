# Runtime D04/WC10 Main95 consumer handoff

Status: **HELD; no Runtime-owned migration exists on this slice.**

## Source tuple reviewed

- Runtime candidate: `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3`, tree
  `d3a290b407fa61e6ab2d476f50c068073f70df00`.
- Agent normal candidate: `6efc81500a0e0688c2bb41e736503f0fc3e04abb`, tree
  `2ed2b8a12b5b3391ca221ba6ff05390f71a73556`.
- Current App integration source: `780c502368cb6eb379cf3848af7009067c7cd744`,
  tree `8eed52bb7f8555c7765a8b485e00920bbf906639`.
- App’s independently qualified normal pin remains `10fa2ff9a8216604aa39e3584f89dc9e7a09080a`,
  tree `01fd2a04ff0c383ec5281043c7e5a4c843d1d835`; that pin is not silently
  treated as integration adoption.

## Caller result

Runtime95bd has no non-test Runtime product caller of
`publish_parent_composition`. The Runtime references are the route/server
entrypoint (`runtime_protocol/service.py:2779`, `runtime_protocol/server.py:582-584`),
generated client surfaces, conformance/recording fixtures, and Runtime tests.
The fixture calls are not product consumers and do not authorize a route cut.

The live callers are peer-owned:

- Agent6ef `astrid/sdk/remote.py:482-551`, with the direct operation call at
  line 536 in `RemoteTimelines.create_empty`. Agent’s authoring and migration
  adapters also retain the writer seam at
  `astrid/core/timeline/authoring_bundle.py:43-53,1591-1617` and
  `astrid/core/timeline/shot_composition_migration.py:151,1030-1033`.
  The existing replacement capability is `WorkspaceClient.commit_timeline`
  (`astrid/sdk/workspace_client.py:484-499`) with the existing
  `timeline.init` command/capture (`astrid/sdk/timeline/native_initialize.py:25-35`).
  Preserve the Runtime-created bootstrap head, exact command guards, receipt,
  replay, payload, and source/CAS checks. Required original positives are
  `tests/stage1/test_runtime_client_cutover.py::test_empty_timeline_opens_as_composition_on_real_daemon`
  and
  `tests/editing_conformance/test_commit_runtime_first_clip.py::test_empty_bootstrap_first_clip_client_commit_exact_reload_inverse_redo`.

- App current source `src/integrations/runtime/createDefaultTimeline.ts:51-81`
  publishes at line 60; the shot-composition provider’s legacy publication
  path is `src/integrations/runtime/dataProvider.ts:260-301`. App already has
  the normal replacement in `src/integrations/runtime/bootstrapInitialization.ts:177-185`,
  which sends the captured initialization commands to `/commit` through the
  existing `commitTimeline` port and durable owner/outbox. Required original
  positives are the bootstrap and headless-shell cases in
  `src/integrations/runtime/createDefaultTimeline.test.ts` (especially the
  atomic new-timeline, headless repair, and lost-ack replay cases), plus the
  existing `bootstrapInitialization.test.ts` init retry/restart case.

`astrid/core/dev/reference_realm.py:99` in Agent6ef is a dev/test fixture and
is intentionally not counted as a product consumer.

## Cut decision

Do not retire or widen `publish_parent_composition` on Runtime95bd. D04/WC10
require both peer consumer migrations to qualify first. This handoff does not
change Runtime product code, generated artifacts, published pins, fixtures, or
positive expectations.
