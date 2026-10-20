# AP2-M2 private014 parent-swap reconciliation

## Result

The Runtime-positive is the existing private014 `clip.swap-media` v1 carrier:

```json
{
  "schema_version": 1,
  "op": "clip.swap-media",
  "version": "1",
  "select": "parent/clip:<raw-id>",
  "args": {"old_media": "<exact five-field selection>", "media": "<exact five-field selection>"},
  "intent": {"ownership": "parent"}
}
```

The authoritative proof is `runtime-ordinary014-a020-final-candidate.md`: final
candidate `fcf4c3d5` / tree `69abf4e2`, ordinary producer `a0dca169`, raw
schema `6ba7`, artifact `f021`, and the exact native lane reported 3 passed in
3.11s, including parent replacement and frozen public013 parent-ownership
refusal. The proof explicitly keeps public013 and the published tuple
unchanged.

The carrier matches the App use case. It snapshots the authored parent bundle,
local generation, outbox basis, and display head before the one producer read.
The staged App delta is therefore limited to the row-local pure helper:

- `parentClipMediaSelection` reads the target's original authored registry
  selection and refuses missing or conflicting mirrors.
- `captureParentClipSwapMedia` emits exactly `clip.swap-media`,
  `parent/clip:<raw-id>`, `old_media`, `media`, and parent ownership.
- `executeParentClipSwapMedia` records exact old/new media dependencies,
  collection/track/ownership/read guards, and only changes the raw `asset`
  field (including the authored mirror); unsupported timing/source/ownership
  shapes refuse without mutation.
- `finishParentClipSwapMedia` replays the detached capture after verification,
  preserving the command/record across JSON round-trip.

The shared session/Provider adapter remains an unactivated flat proposal. The
existing proposal is
`hub/design/ap2-m2-parent-swap-shared-adapter-packet.patch`, with its scope
recorded in `ap2-m2-parent-swap-shared-adapter-packet-REPORT.md`. No session,
Provider, dataProvider, command-service, schema, API, artifact, lock, or pin
change was made here.

## Verification

Passed in this App worktree:

```text
node node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/commands/parentClipSwapCapture.test.ts src/tools/video-editor/commands/parentClipAddCapture.test.ts
  2 files / 10 tests passed

node node_modules/eslint/bin/eslint.js --no-cache src/tools/video-editor/commands/parentClipAddCapture.ts src/tools/video-editor/commands/parentClipSwapCapture.ts src/tools/video-editor/commands/parentClipSwapCapture.test.ts
  passed

npm run typecheck:strict-islands -- --pretty false
  passed

git diff --check
  passed
```

The pure lane proves exact operation/selector/args/intent, capture record
dependencies and bindings, raw-only carrier preservation, guarded refusal,
JSON replay, and direct parent-media neighbors. The record contains the
before/after writes consumed by the existing guarded inverse machinery, but no
native/session/provider inverse journey was run or claimed.

Not run, per task: native/provider/Door/browser/full suites, local sockets,
dependency installation, Runtime/Agent qualification, actual App adapter
activation, or a repeat of the already passing native nodes. The next step is
to integrate and qualify the paired Agent/Runtime parent member, then apply the
flat shared adapter proposal and run the focused App session plus actual
lost-ack/restart/retry/undo and zero-legacy journey.
