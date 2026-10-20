# AP2 M2 element overlay mounted journey source

## Result

Blocked; no test/e2e source changes were made.

The requested positive journey cannot be authored against the current normal
catalog without creating a false-positive surface. The migrated
`ElementsLibraryPanel` ingress is deliberately narrow:

- `ElementsLibraryPanel.tsx` enters the native `elementOverlay` path only for
  an effect with no `packId` (`ElementsLibraryPanel.tsx:84`).
- The normal generated Astrid catalog entries used by the App carry an owner
  (`local` or `rendering`). The checked-in catalog includes the requested
  overlay-capable built-ins such as `end-spanning-layer`, `frame-overlay`, and
  `audio-reactive-colour`, all with a `packId`.
- The native delete ingress has the same literal-only contract: it requires an
  existing effect reference without `packId` and a matching literal clip type
  (`PropertiesPanelBody.tsx:241`).

Therefore an actual `ElementsLibraryPanel` click on a normal built-in follows
the still-legacy owner-pinned adapter path, not the already-migrated literal
overlay session. Making a normal entry eligible by stripping its owner,
injecting an unowned catalog item, or using a test capture port would violate
the task's exact public13/normal-catalog and real-door requirements. The
remaining dependency is an App/Agent authority decision or consumer seam that
accepts the exact owner-pinned built-in reference through the native overlay
command contract; this worker does not change that product contract.

## Verification

Focused unit lane passed:

```sh
env TMPDIR=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-element-overlay-mounted-journey-source/tmp \
  NODE_OPTIONS=--require=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-bootstrap-transport-assertion-repair/notes/vitest-runner.cjs \
  node /home/user/work/app/node_modules/vitest/vitest.mjs run \
  --config config/testing/vitest.config.ts --configLoader=runner --no-cache \
  --maxWorkers=1 --no-file-parallelism \
  src/tools/video-editor/components/ElementsLibraryPanel.test.tsx \
  src/tools/video-editor/commands/elementOverlayCapture.test.ts \
  src/tools/video-editor/commands/commitSession.test.ts \
  src/tools/video-editor/runtime/element-adapter.test.ts
```

Result: **4 files, 97 tests passed**.

The initial direct Vitest invocation was not evidence: it failed at startup
because this repository's config needs the established `__dirname` preload.
The corrected command above used the existing read-only runner and a private
worker temp directory. No browser, localhost, socket, full, Runtime-door, or
central suite was run.

## Next step for the orchestrator

Keep D01-app-element-routes open. Once the normal public13 catalog/authority
seam makes one owner-pinned built-in eligible for the migrated overlay
producer, add one case to `tests/e2e/local/three-products.spec.ts` using the
actual Elements Library click and mounted Properties Panel delete. The case
should then use the existing real-door helpers to assert the `clip.add` /
`clip.delete` command records, opaque and selection preservation, lost-ACK /
restart / reload / exact-retry / guarded-undo, and zero legacy snapshot POSTs.
The central targeted request should be issued only after that source exists:

```sh
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test \
  ap2-m2-element-overlay-mounted-journey-source \
  'targeted --files "tests/e2e/local/three-products.spec.ts tests/e2e/local/support/harness.ts"') \
  && /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"
```

