# AP2 M2 ordinary real Scene Phase UI first-failure fix

## Result

Restored admission of the existing reviewed App-owned Scene Phase Markers
extension to the normal editor extension list. The current main migration made
`devLocalExtensions` contain only the generated Astrid pack catalog, while the
App-owned `scenePhaseMarkersExtension` and its panel/producer remained in the
repository and in the production reviewed-ID allowlist. The seed already
contained the two markers, so the first central failure was UI admission before
the producer action.

Changed only:

- `src/tools/video-editor/dev/localExtensions.ts`
- `src/tools/video-editor/dev/localExtensions.catalog.test.ts`

The generated pack entries remain first and unchanged. The existing
Scene Phase Markers extension is appended to the normal host list; production
selection already admits its reviewed ID. No new product feature, command,
producer, test callback, direct Runtime request, or App-owned group UI was
added.

## Before / after UI path

Before, the central hosted run used the normal `/tools/video-editor` route and
seeded `config.app['haus.astrid.scene-phase-markers']` with
`ordinary-marker-a` at 1 and `ordinary-marker-b` at 6. The DOM had no
`[data-testid="scene-markers-summary"]` before the producer action because the
extension was not in `devLocalExtensions`; the panel registration itself was
valid. Central test ID
`ap2-m2-chromium-launch-private-environment-fix-e2e-m2-ordinary-integration-1020191951-23822`
failed at `tests/e2e/local/three-products.spec.ts:1216` before
`buildAlignShotsPatch` could run. Chromium smoke and hosted build passed.

After this source change, the same normal route admits the existing extension,
so its registered status-bar panel is expected to render `2 markers`, the
playhead/tail input, and `scene-markers-move-shots`. The required next browser
run must click that real UI action once and qualify the resulting
`buildAlignShotsPatch` -> native generic capture path.

The central result referenced an error-context DOM report and `trace.zip`; those
artifacts were not retained in the accessible central result directory for this
worker, so no additional screenshot/trace claim is made here. The accessible
central log and source audit establish the missing DOM element and its
registration cause.

## Validation

Passed:

```text
node_modules/.bin/vitest run --no-cache --maxWorkers=1 --no-file-parallelism \
  src/tools/video-editor/dev/scene-phase-markers/__tests__/patch-building.test.ts \
  src/tools/video-editor/dev/scene-phase-markers/__tests__/panel-transition.test.tsx \
  src/tools/video-editor/dev/scene-phase-markers/__tests__/ScenePhaseMarkersOverlay.test.tsx
3 files, 53 tests passed

ASTRID_CHECKOUT=/home/user/work/agent VITEST_LANE=checkout \
  node_modules/.bin/vitest run --config config/testing/vitest.config.ts --no-cache \
  --maxWorkers=1 --no-file-parallelism \
  src/tools/video-editor/dev/localExtensions.catalog.test.ts
1 file, 2 tests passed

node_modules/.bin/eslint \
  src/tools/video-editor/dev/localExtensions.ts \
  src/tools/video-editor/dev/localExtensions.catalog.test.ts --max-warnings 0
passed

git diff --check
passed
```

Not run, per task rules: local browser, localhost/live sockets, full suite,
dependency installation, graph/source-floor checks, or a second central run.
The next request is blocked only on the harness committing this clean source
change; then request exactly one existing central suite:

```sh
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test \
  ap2-m2-ordinary-real-scene-ui-first-failure-fix e2e-m2-ordinary-integration) && \
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"
```

That run must retain the locked Composition 0.0.13 / Agent
8130a401bf44a518d5a40ae274d398b8c560be55 / Runtime
2c4ac180c2220bdad966bc01e95ad230e99ce26a tuple and report the existing
ordinary test ID, exact four-command batch, lost ACK, disjoint Agent edit,
newer local edit, exact retry after restart, guarded undos, opaque preservation,
and zero legacy traffic.

## Decisions and disposition

- Scene Phase Markers is not a fabricated fallback: its panel, registration,
  feature allowlist, seed shape, and `buildAlignShotsPatch` producer already
  exist in current App source and tests. Restoring its admission is the
  smallest normal-host fix.
- No alternate producer was substituted, and no group UI was touched.
- No blocker remains for this worker. Central post-commit browser qualification
  is unverified and is the recommended next step.
