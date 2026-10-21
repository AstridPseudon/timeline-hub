# AP2-M2 current repaired parent-consumer join

## Result

Joined the two repaired, non-overlapping donor final states onto current
`hub/tl/integration`:

- `src/tools/video-editor/hooks/useAssetManagement.ts`
- `src/tools/video-editor/hooks/useAssetManagement.mediaImport.test.tsx`
- `src/tools/video-editor/hooks/useExternalDrop.ts`
- `src/tools/video-editor/hooks/useExternalDrop.test.tsx`
- `src/tools/video-editor/lib/external-drop-utils.ts`
- `tests/e2e/local/support/run-parent-manual-drop-evidence.sh`

The five tracked source/test files match their respective donor branch heads
byte-for-byte, and the evidence wrapper matches the video donor. The wrapper's
tracked executable mode is preserved.

The video donor includes the approved b4d native prepared-video consumer carrier.
It is reused as-is; no new consumer implementation was added. Prepared video
without selection, without its native carrier, or refused by native addClip now
remains a visible false/refusal with no local applyEdit fallback. Existing image,
audio, catalog, bootstrap, selected, trim, and ordinary assertions remain in
place. External-drop file, multi-generation, single-generation, and general
asset callers await and propagate false/rejection; seek occurs only after
accepted placement.

No `useTimelineState`, Provider, session, store, API/schema, pin, or new
shared source file was edited.

## Shared construction proposal

Regenerated the inactive current-HOME proposal:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/ap2-m2-parent-current-repaired-consumer-join-shared-proposal.patch`

It is a tiny one-file proposal using the existing `createTimelineCommands`
carrier, provider-bound `getProjectVerifiedMedia`, and the existing
`useAssetManagement` construction point. It is not applied pending combined
approval.

Static applicability:

```text
git apply --check --whitespace=error /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/ap2-m2-parent-current-repaired-consumer-join-shared-proposal.patch
PASS (worker HOME snapshot)

git -C /home/user/work/app apply --check --whitespace=error /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/ap2-m2-parent-current-repaired-consumer-join-shared-proposal.patch
PASS (shared HOME)
```

## Verification

```text
node --import 'data:text/javascript,globalThis.__dirname=process.cwd()+"/config/testing"' node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/hooks/useExternalDrop.test.tsx src/tools/video-editor/hooks/useAssetManagement.assetDrop.test.ts src/tools/video-editor/hooks/useAssetManagement.mediaImport.test.tsx src/tools/video-editor/lib/timeline-asset-plans.test.ts
PASS: 4 files, 43 tests

./node_modules/.bin/eslint --no-cache --max-warnings 0 src/tools/video-editor/hooks/useAssetManagement.ts src/tools/video-editor/hooks/useAssetManagement.mediaImport.test.tsx src/tools/video-editor/hooks/useExternalDrop.ts src/tools/video-editor/hooks/useExternalDrop.test.tsx src/tools/video-editor/lib/external-drop-utils.ts
PASS

npm run typecheck:strict-islands -- --pretty false
PASS

git diff --check
PASS

bash -n tests/e2e/local/support/run-parent-manual-drop-evidence.sh
PASS

tests/e2e/local/support/run-parent-manual-drop-evidence.sh probe
PASS: failuretrap probe copied evidence before disposable-root cleanup
```

The initial bare Vitest invocation failed only during config loading because its
ESM runner did not define `__dirname`; the established runner command above
passed.

Static donor/scope checks passed:

- each owned source/test file equals its named donor branch head;
- the wrapper equals the video donor;
- the final diff contains only the five owned row-local source/test paths plus
  the wrapper;
- the reviewed fixes 1–3 are visible in source: unconditional prepared-video
  refusal, preserved placement/removal intent, and awaited boolean propagation;
- the existing command service captures the prepared media selection before its
  sole verified-media await.

## Not run / handoff

No browser, localhost, live socket, request-test, full suite, gate source pin,
or HOME proposal application was run. Required next step is seam review and
combined approval, followed by applying the inactive shared proposal in HOME
and running the manager-controlled current gate.

