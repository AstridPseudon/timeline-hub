# AP2 M2 parent mounted ADD result and cut

## Result

No mounted ADD result exists to analyze. The prerequisite worker
`ap2-m2-parent-corrected-existing-driver-one-run-0230` finished with exit 0,
but its exact-source review returned **HOLD**, so it correctly submitted no
central run. Its worktree was recycled after producing the no-run report.

There is therefore no first failure packet, no service pass, and no consumer
qualification. I did not retry, run a gate, run a browser/socket/full suite,
or delete any App code.

## Precise blocker

The exact-source conversion review reports:

- The final committed corrected source was unavailable.
- The only inspectable source was App commit
  `7e85d89120227f336a2e8dbf8e0ea44d98311da0` with tree
  `20bf7411c9ebbcbbb7a3fc10846e66cb0573b0f3`.
- The source-only preflight still expected the stale frozen App tree
  `972d2ed2e4f85f334eb9f2e6ca40d9bfbce9eac7`, so it failed before any case
  execution.
- The provisional source contained `REPLACE_AFTER_COMMIT_TREE` and
  `REPLACE_AFTER_COMMIT_SHA` placeholders. Filling those with a guessed value
  would make the source guard self-referential, so no value was substituted.

The source-finish report identified the intended corrected two-file consumer
tree as `6809757f93ca5e166b24b8bc0160ca09005e984a`, but it also requires the
harness-created clean commit before the shared source binding can be
finalized. That finalization and the required explicit approval did not exist
when the parent worker completed.

## Evidence status

The required cohort remains only a source-level reference, not run evidence:

- Agent `6efc81500a0e0688c2bb41e736503f0fc3e04abb`, tree
  `2ed2b8a12b5b3391ca221ba6ff05390f71a73556`.
- Runtime/producer `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`, tree
  `d3a290b407fa61e6ab2d476f50c068073f70df00`.
- App pin `10fa2ff9a8216604aa39e3584f89dc9e7a09080a`.
- Public13 archive SHA-256
  `895c628ab0727c8975247310fd0319b0f546a8d032a57072c9e364e20965ca30`.

Because the central run never started, these remain unverified here: actual
mounted File ingress, native ADD request, accepted revision, exact 404
negative, raw/opaque preservation, reload, undo, lost acknowledgement,
restart, exact retry, and zero legacy traffic. No first failure packet exists.

The parent’s offline checks passed before the HOLD (shell syntax, driver
probe, ESLint, one-case Playwright collection, and `git diff --check`), but
they do not qualify the mounted journey.

## Live ADD callers

The live mounted chain is unchanged:

`onTimelineDrop` in `src/tools/video-editor/hooks/useExternalDrop.ts:630`
calls `dispatchTimelineDrop` at `:62`, which calls `handleFileDrop` at
`src/tools/video-editor/lib/external-drop-utils.ts:275`.

For a prepared video, the mounted path is wired as follows:

- `useTimelineState` creates `parentMediaCommands` and passes them to
  `useAssetManagement` (`src/tools/video-editor/hooks/useTimelineState.ts:949-969`).
- `useAssetManagement.placePreparedAsset` calls the native `commands.addClip`
  (`src/tools/video-editor/hooks/useAssetManagement.ts:274-309`).
- `createTimelineCommands.addClip` performs the native parent-media capture,
  Runtime verification, finish, and submit (`src/tools/video-editor/hooks/useTimelineCommandsService.ts:474-539`).
- The durable command-session/outbox neighbor is
  `src/tools/video-editor/hooks/useTimelineCommandSession.ts:271-283`; its
  parent `clip.add-media` port is also exposed from `useTimelineState.ts:1263`.

These callers, shared persistence/serializer code, and duplicate-generation
consumers remain live and were not changed. Since the ADD consumer was not
qualified, no legacy ADD leaf is dead yet and no focused deletion was
prepared.

## Checks and environment

- `git status --short --branch` — clean on
  `tl/ap2-m2-parent-mounted-result-and-cut-0232`.
- Central named suite `ap2-m2-parent-retained-evidence-real-gate` — **not
  submitted**, because the exact-source review was HOLD.
- Browser, localhost/live socket, full suite, retry, and product cutover — not
  run.
- Available disk at completion: 17 GB; above the 10 GB floor.

## Required next step

HOME must finalize the harness-created clean App source binding using the
actual commit SHA and literal tree `6809757f...`, preserve the ancestry,
clean-state, pin, artifact, import, and postflight guards, and obtain a fresh
explicit source-review approval. Only then may one central no-cache run use
the existing driver command:

```sh
sh tests/e2e/local/support/run-parent-manual-drop-evidence.sh run "$PWD"
```

No ADD deletion or cutover should be attempted before that run contains every
required case assertion and the correct source/cohort evidence.
