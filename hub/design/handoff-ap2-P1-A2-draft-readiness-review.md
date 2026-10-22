# P1 App A2 draft-readiness review

Result: **FAIL for current P1 draft readiness; H3 remains no-go.** The existing
move-only outbox/restart leg passes, but the required real split → trim the
created ID → Agent edit → lost acknowledgement → restart chain is not runnable
on this draft. The required corpus command also has one baseline provenance
failure. No H3 GO, A2 acceptance, or provider acceptance is inferred from the
fixture assertions.

## Draft identity

- Repo: App, worktree branch `tl/ap2-P1-A2-draft-readiness-review`.
- Published baseline ref `hub/timeline/app/tl/app-A2-save-funnel` (also
  `hub/tl/integration`/`tl/integration`) resolves to
  `f9d5d0cdd666d4d68e5dfe6a2c29d513da92f8d9` (`Merge tl/app-U3b-eof-fix`).
- Worktree was clean; no tracked repository files were changed.
- This is the U3b-derived baseline with the existing outbox/session helpers,
  not an A2 implementation.

## Commands and results

1. `node node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --no-cache src/tools/video-editor/commands/p1FeasibilityCorpus.test.ts`
   - **FAIL**: 12 tests, 11 passed, 1 failed.
   - Log: `/tmp/ap2-p1-corpus.log`.
   - Failure is the exact-provenance case for
     `three-products-seed-and-recovery`: corpus expects SHA-256
     `2ba2164ba7fd2d76ccca94d0645e6b79236c85ab4e53e82e84ae1af250c7d815` for
     `tests/e2e/local/support/harness.ts`; actual is
     `b243b340177c2d905f841ec4c7307b03e7afd4f43f0096701c20bf132f202534`.
     The current file's last commit is
     `15d9df3ce299e9e672dffbbb5a300e3d59fbdbf2` (`test: repair U3c quick and
     journey harness`). This is baseline corpus/source drift, not a changed
     P1 behavior; the owning corpus worker should refresh or explain the pin.
2. `node node_modules/typescript/bin/tsc --noEmit`
   - **PASS**, exit 0. Log: `/tmp/ap2-p1-tsc.log`.
3. `node node_modules/eslint/bin/eslint.js src/tools/video-editor/commands/p1FeasibilityCorpus.test.ts --max-warnings 0`
   - **PASS**, exit 0. Log: `/tmp/ap2-p1-eslint.log`.
4. `git diff --check`
   - **PASS**, exit 0. Log: `/tmp/ap2-p1-diffcheck.log`.

No central test-service request was needed: the local targeted corpus run did
not refuse sockets or require a browser. No full/browser/heavy suite was run.

## Covered legs

- `p1FeasibilityCorpus.test.ts:51-71` runs the real App trim document through
  `authoringBundleFromDocument` and `executeClipTrim`, checking `from`, `to`,
  `hold`, intent clearing, and preserved speed/opaque data. It also reads the
  Agent split fixture and checks the requested `right_id`; it does not execute
  an App split or submit that command.
- `p1FeasibilityCorpus.test.ts:73-82` runs the real App move fixture through
  `executeClipMove` and checks disjoint authored-field preservation.
- `p1FeasibilityCorpus.test.ts:98-134` passes the available App outbox leg:
  two dependent `clip.move` intents, an external label mutation, a lost ACK,
  owner disposal, restart/recovery, exact replay of the first request, and
  dependent replay from the accepted `p1` head. This is a fake IndexedDB/fake
  transport test and covers accepted behavior only.
- `p1FeasibilityCorpus.test.ts:84-96` verifies that the corpus metadata names
  accepted/merged/refused and the required seams. It is a description check,
  not execution evidence for those dispositions.

## Missing or unexecuted H3 seams

- **App split capture/submit and created-ID binding:** missing. The current
  editor split path (`hooks/clip-editing/useClipSplitting.ts:18-81`) calls
  local `applyConfigEdit`; there is no session-owned `clip.split` capture port
  that allocates/persists `right_id` for the outbox.
- **Trim of the newly created split ID through the queue:** missing. A
  session-owned `clipTrimPort` exists, but the current corpus only calls the
  native executor directly; the fake transport has no `clip.trim` branch and
  would throw `Unsupported test command`.
- **Intervening Agent `track.set` against a real Runtime head:** missing. The
  fake transport can apply `track.set`, but the corpus chain never sends it and
  does not exercise a real Agent edit or Runtime merge.
- **Merged reply:** missing. The fixture says `runtime_wire: rebased`, but the
  current session transport maps every successful response to outbox outcome
  `accepted` (`commitSession.ts:213-225`); the fake transport emits no merged/
  rebased distinction.
- **Refused predecessor and dependent revalidation/rollback:** missing. The
  outbox marks a refused predecessor and dependent intents as conflicts and
  exposes `useLatest`/`keepLabelChanges`, but no P1 chain drives a refusal and
  proves dependent revalidation or rollback.
- **Lost ACK/restart for this mixed chain:** missing. Restart/replay is covered
  only for move→move, not split→trim-new-ID→Agent-edit.
- **R1 `doc.patch` execution and field-level previous-value conflict details:**
  missing on this App draft; no provider/runtime execution is present in this
  corpus.

## Callable interfaces for the A2 extension

- `createTimelineCommandSession(options)` (`commands/commitSession.ts:139-163`)
  requires a scope, initial basis, `send(request, key)`, preview/project/state
  callbacks, and returns the session ports plus `recover(ownerId)`, `retry()`,
  `flush()`, `observe(remote)`, `useLatest()`, and `keepLabelChanges()`.
- Existing trim seam: `ClipTrimCapturePort` in
  `commands/clipTrimGesture.ts:9-13`: `capture({clipId,current})`,
  `finish(basis,args)`, `submit({command,preview})`. The session exposes it as
  `session.clipTrimPort`; it requires a literal `parent/clip:<id>` identity.
- Existing track-label seam: `TrackLabelCapturePort` in
  `commands/trackLabelGesture.ts:21-29`: `capture({trackId,current})`,
  `finish(basis,args)`, `submit({command,preview})`. The session exposes it as
  `session.trackLabelPort`.
- Existing generic seam: `session.genericPatchPort` has
  `capture({patch,current})`, `finish(basis)`, and `submit({commands,preview})`
  (`commitSession.ts:1063-1121`). It captures App-native timeline patch
  operations and emits native commands; it is not v2 `doc.patch` execution.
- Durable chaining is already available through the session's internal
  `enqueue` and `commitOutbox.ts`: dependent appends use
  `basis: { after: predecessorId }`, `dispatch(build, transmit)`, and
  `recover(scope, ownerId, work)`. Recovery retries the persisted exact
  request/key; it does not create the missing split binding or merge semantics.
- Current request builder (`commitSession.ts:204-211`) sends only the ABI-1
  base pair, commands, and `source: { via: 'app' }`; it does not send v2
  `label`, `steps`, `merge`, or `reads`. A2 must extend this existing builder
  and preserve the outbox's original payload/key and dependent basis semantics.

## PASS/FAIL boundary and next commands

The bounded native fixture checks and the existing move lost-ACK/restart leg
are **PASS**. Overall P1 draft readiness is **FAIL** because the exact corpus
run is red and the H3 chain's real split, merged, refused, new-ID, and
`doc.patch` seams are unimplemented/unexecuted. Do not call H3 GO or accept A2
until those seams are wired to the real Runtime/Agent path and the three reply
dispositions are observed end to end.

After the A2 implementation and Runtime/Agent chain are available, rerun these
exact checks (and fix the stale harness provenance pin before calling the
corpus green):

```sh
node node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --no-cache src/tools/video-editor/commands/p1FeasibilityCorpus.test.ts
node node_modules/typescript/bin/tsc --noEmit
node node_modules/eslint/bin/eslint.js src/tools/video-editor/commands/p1FeasibilityCorpus.test.ts --max-warnings 0
git diff --check
```

Heavy integrated chain execution belongs to the central farm once the chain is
actually runnable.
