# Actual App joint stored-cap See-domain gate commands

## Source proof

```sh
APP=/home/user/banodoco/reigh-app
git -C "$APP" show -s --format='%H%n%P%n%s' 4720a864c81dc7002a9e95dbacf10cec8df5da81
git -C "$APP" show -s --format='%H%n%P%n%s' 1fe351b9847d35db66ab294a6edf631447fa78ce
git -C "$APP" merge-base --is-ancestor \
  4720a864c81dc7002a9e95dbacf10cec8df5da81 \
  1fe351b9847d35db66ab294a6edf631447fa78ce
```

Result: producer is the direct parent of the ES2020-labelled descendant; ancestry passed.

```sh
git -C /home/user/banodoco/reigh-app grep -n 'Object\.hasOwn\|hasOwnProperty\.call' \
  1fe351b9847d35db66ab294a6edf631447fa78ce -- \
  src/tools/video-editor/lib/serialize.ts \
  src/tools/travel-between-images/components/shotTimelineDataProvider.ts
```

Result: serializer uses `hasOwnProperty.call` at line 43; producer still uses `Object.hasOwn` at line 146.

## Exact App mounted regression

The exact `1fe351b98` tree was archived to an owned temporary directory. Its tracked `vendor/artifacts/banodoco-timeline-composition-0.0.12.tgz` was mounted read-only through an owned extracted package directory; peers came from the shared read-only `/home/user/work/app/node_modules`; Vitest used `--configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism`.

```sh
node /home/user/work/app/node_modules/vitest/vitest.mjs run \
  --config <owned-candidate>/candidate.vitest.config.ts \
  --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism \
  src/tools/video-editor/lib/serialize.test.ts \
  src/tools/video-editor/hooks/useTimelineSave.draftConfig.test.ts \
  src/tools/video-editor/hooks/useTimelinePersistence.test.tsx \
  src/tools/video-editor/hooks/useTimelineCommandSession.projection.test.tsx \
  src/tools/travel-between-images/components/ShotTimelinePreview.test.ts \
  src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewSurface.storedCap.test.tsx \
  src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewSurface.test.tsx \
  src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewSurface.lifecycle.test.tsx \
  src/tools/video-editor/data/canonicalCompositionState.mainImageCap.test.ts
```

Result: **9 files, 200 passed, exit 0**.

## Exact candidate typecheck blocker

```sh
node /home/user/work/app/node_modules/typescript/bin/tsc \
  -p <owned-candidate>/tsconfig.app.json --noEmit --pretty false
```

Result: **exit 2** with:

```text
src/tools/travel-between-images/components/shotTimelineDataProvider.ts(146,30):
error TS2550: Property 'hasOwn' does not exist on type 'ObjectConstructor'.
```

## Composition source and exact artifacts

```sh
node /home/user/work/composition/node_modules/typescript/bin/tsc \
  -p typescript/tsconfig.test.json --outDir <owned-temp>/test-dist
node --import ./typescript/tests/register-extensionless.mjs --test \
  <owned-temp>/test-dist/tests/scene-evaluation.test.js \
  <owned-temp>/test-dist/tests/transition-spans.test.js \
  <owned-temp>/test-dist/tests/transition-policy.test.js
```

Result: **3 files passed, exit 0**.

The exact read-only public12 and public13 tarballs were independently extracted and probed against the shared pinned peers. Both passed: capped `4000ms → 120`, capped `4500ms → 135`, uncapped `→ 150`.

No browser, render, socket, network, install, or full suite was run.
