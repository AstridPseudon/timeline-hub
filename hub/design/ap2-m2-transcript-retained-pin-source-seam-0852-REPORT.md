# App2 M2 retained transcript-source seam — 2026-10-21

## Result

Prepared one dormant, row-local App adapter in
`src/tools/video-editor/commands/transcriptAssociateCapture.ts:44-126`:
`readRetainedTranscriptSources`. It uses the existing authenticated
`getProjectVerifiedDocument` read for caller-supplied exact new and optional
prior transcript pins, returns the Runtime carrier unchanged as
`{ pin, document }`, and refuses a returned carrier whose pin differs from the
requested exact pin. It does not derive authority from browser/project-document
content, authored snapshots, or latest/version guesses.

The focused regression at
`src/tools/video-editor/commands/transcriptAssociateCapture.test.ts:163-182`
proves both exact new/prior pin passthrough and mismatched-carrier refusal.
The adapter remains dormant: live callers **NONE**.

## Existing producer and carrier trace

The normal App project-transcript response is not a complete source pin:

- `src/tools/video-editor/data/typed/projectTranscript.ts:53-80` defines
  `ProjectTranscriptDocument` with `document_id` and `version`, but no
  `content_digest`.
- The ordinary repository `get/create/update` path is
  `projectTranscript.ts:103-118`; identity/schema checks are
  `projectTranscript.ts:137-158`.
- The live host selection/import/promotion responses converge on `associate`
  at `src/tools/video-editor/lib/project-transcript-host.ts:747-857`.
  `associate` still projects and calls the snapshot writer
  `commitData(next, { save: true, semantic: true })` at `:600-652`.

The authoritative existing retained source is already complete:

- Runtime’s transcript identity/source validation and managed-media binding are
  `runtime/runtime_protocol/timeline_commit_inputs.py:29-35,162-194`.
- Retained bindings reconstruct the exact `{pin, document}` carrier at
  `runtime/runtime_protocol/timeline_commit_inputs.py:334-367`; exact live
  capture also checks version and digest at `:378-419`.
- The Runtime commit-port transcript resolver is
  `runtime/runtime_protocol/timeline_commit_port.py:300-321`; its public exact
  source resolver is `:534-548`, using the retained binding closure and
  `capture_document_input`.
- The service handoff is
  `runtime/runtime_protocol/service.py:2562-2565`, exposed by the existing
  `GET /v1/projects/:/document-inputs/verified` door entry at
  `runtime/runtime_protocol/door.py:166-172` and generated App client method
  `src/integrations/runtime/generated.ts:183`.
- App already carries that authenticated read seam as
  `src/tools/video-editor/data/DataProvider.ts:448-452`, implemented by
  `src/integrations/runtime/dataProvider.ts:345-353`.
- Agent’s matching exact retained transcript reader is
  `agent/astrid/sdk/timeline/native_source_inputs.py:80-104`; it confirms the
  same exact pin, scoped document, canonical content digest, and transcript
  shape. It was used as a compatibility reference only; no Agent files changed.

Therefore the existing source producer/handoff is complete for an exact pin.
The remaining live caller gap is concrete: the host’s `projectTranscripts.get`
result has no digest, so the host cannot yet request the retained read for a
new or prior source without an upstream exact-pin handoff. This worker did not
invent one or activate the adapter.

## Scope and preservation

Only the dormant adapter and its focused test changed. No host, repository/
CRUD, Provider, dataProvider, door, commit session, schema, pin activation,
writer deletion, or live associate cutover changed. Existing snapshot behavior,
ordinary positives, refusal boundaries, and draft preservation remain covered
by the existing transcript neighbor tests.

Suggested PEER REQUEST draft for the App2 owner (future live-consumer work):

> Adapt the dormant associate consumer to obtain the exact new/prior
> `DocumentPin` from the existing Runtime retained-read carrier before calling
> `readRetainedTranscriptSources`. `projectTranscripts.get` currently returns
> only `document_id`/`version` at `projectTranscript.ts:53-63`; do not hash its
> browser body or infer a digest/version. Keep the snapshot writer until the
> exact-pin consumer is qualified.

## Evidence

- `TMPDIR=/tmp/ap2-m2-transcript-seam-0852-tmp npx vitest run --config config/testing/vitest.config.ts --cache=false --no-file-parallelism --maxWorkers=1 src/tools/video-editor/commands/transcriptAssociateCapture.test.ts`
  — PASS, 1 file / 8 tests.
- `TMPDIR=/tmp/ap2-m2-transcript-seam-0852-tmp npx vitest run --config config/testing/vitest.config.ts --cache=false --no-file-parallelism --maxWorkers=1 src/tools/video-editor/commands/transcriptAssociateCapture.test.ts src/tools/video-editor/data/typed/importTranscriptIdentity.test.tsx src/tools/video-editor/lib/project-transcript-host.test.ts src/tools/video-editor/data/typed/timelineBundle.test.ts src/tools/video-editor/lib/transcript-panel-binding.test.ts`
  — PASS, 5 files / 60 tests.
- `npx eslint src/tools/video-editor/commands/transcriptAssociateCapture.ts src/tools/video-editor/commands/transcriptAssociateCapture.test.ts --ext ts,tsx --max-warnings 0`
  — PASS.
- `npm run typecheck:strict-islands`
  — PASS.
- `git diff --check`
  — PASS.
- Caller/scope scan: no callers of `readRetainedTranscriptSources` outside its
  focused test; changed paths are only the two dormant helper/test files.

No full, browser, native, build, daemon, socket, HTTP, install, or broad matrix
suite was run, per task limits. The live App2 consumer remains unverified and
must be qualified by the App owner after an exact-pin handoff exists.
