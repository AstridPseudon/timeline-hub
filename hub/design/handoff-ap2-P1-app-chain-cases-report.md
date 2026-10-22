# Handoff: ap2-P1 App chain-cases review

## Result

`PASS` for the App case collection only, at author SHA
`898476b0e3ce8844717f9ea52edf9b7b4957e696`.

This is not an H3 GO and not a full-P1 pass. The corpus correctly records
`authored-not-go`; the real integrated chain remains pending A2/R1 and service
execution.

## Evidence

The corpus has real App, Agent, and e2e source paths. Independent provenance
checking found every declared commit object/path and every declared SHA-256
matching the committed bytes. The targeted test executes App trim/move capture
and the App outbox/session recovery APIs. It checks exact lost-ACK request
replay, stable first payload/key, a distinct dependent key, canonical `p1`
base, and preservation of the intervening head edit.

The mandated local checks all passed:

```bash
node node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --no-cache src/tools/video-editor/commands/p1FeasibilityCorpus.test.ts
# Test Files 1 passed; Tests 12 passed
node node_modules/typescript/bin/tsc --noEmit
# pass
node node_modules/eslint/bin/eslint.js src/tools/video-editor/commands/p1FeasibilityCorpus.test.ts --max-warnings 0
# pass
```

## Runnable farm command

Use the central targeted service for the same test when checking the worker
snapshot (do not request a full/browser suite for this review):

```bash
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test ap2-P1-app-chain-cases-review-r2 targeted --files "src/tools/video-editor/commands/p1FeasibilityCorpus.test.ts") && /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"
```

## Missing seams before H3

1. App split capture/submit and Runtime-created-ID binding for `right`.
2. App mixed-command queue trim against that newly created ID.
3. A real Agent `track.set` commit as the intervening edit. The current JSON
   labels the actor Agent but points to the App track-label fixture; the Agent
   fixture exists and is byte-identical at
   `fc6c1f2615b1b37ae6bc2121397e64ee9d8061f`.
4. Runtime v2 execution of accepted, merged, and refused replies, including
   canonical head and `id_map`; new v2 merged replies must use `merged`, while
   historical ABI replies may retain `rebased`.
5. A2 predecessor refusal handling: dependent revalidation against the actual
   canonical head or explicit rollback with a user-visible message.
6. R1 `doc.patch` execution, previous-value checks, field/collection conflict
   details, and real service execution of the chain. The current transport is a
   fake and directly mutates its server document; it is not H3 proof.
7. Keep C0b/undo out of this proof until its approval and implementation are
   complete.
