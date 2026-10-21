# M2 current-ops producer ownership safety case

## Result

The exact Runtime checkout was provisioned and all source, command, and cohort
guards passed. The one permitted central `--no-cache` run was submitted against
the source worker `ap2-m2-producer-current-proof-execution-stage-0320`, not this
checkout. It failed before browser launch, Runtime traffic, or any test-body
assertion because the hosted App build has a missing Composition export.

No retry or harness edit was made after that first actual run.

Central result:

```text
ap2-m2-producer-current-proof-execution-stage-0320-ap2-m2-producer-current-ops-e2e-integration-1021033441-19091
exit=1 in 23s
App tree 8c7393050ded32854503dfb7719a102b5dec94eb
```

First failure:

```text
src/tools/video-editor/compositions/playerEvaluation.ts:5
getSanitizedPlaybackRate is not exported by
@banodoco/timeline-composition/dist/evaluation.js
```

The failure occurred during `npm run build:hosted` from Playwright global setup.
The browser did not start, no Runtime commit packet was sent, and the producer
journey's accepted/refused behavior is unverified.

## Identity and custody checks

- Final source worker ref: App commit `4ef89267f00d193273441ff6dbb955f30d27d708`, tree `8c7393050ded32854503dfb7719a102b5dec94eb`. This was checked from the final Git ref, not copied from the earlier preparation report.
- Approved body: commit `36dd91257fd13dcad0d58b48c790caa5063b4c8c`, tree `d908845dbc8e5ebf96698d08621557e904f20c52`.
- Final delta against the approved body is exactly one added file: `playwright.producer-ownership-current-pin.config.ts`. No spec, helper, production, shared writer, DTO, authority, carrier, fresh-creation, or three-products file changed.
- Approved spec SHA-256: `d91d0c1cce22f68119cd30fcb0a288346474b0ad4b64c84dcee3b730fa468d89`.
- Approved helper SHA-256: `50cbe5341f24c9a1ecc999018e2c6d975380a3440570abce151f9173c9752016`.
- Final selector config SHA-256: `5b880ceff883abce2575a3a85aaa4eda69d3bcb848768ff0e91f337d50cca4c0`.
- Runtime checkout: HEAD `2c4ac180c2220bdad966bc01e95ad230e99ce26a`, tree `7ab412cc4bcbe517efcfa806e092336390312e18`, at `/home/user/work/wt/rt-pin-2c4ac180`.
- Agent cohort: HEAD `8130a401bf44a518d5a40ae274d398b8c560be55`, tree `236c3e57e0265c52b81ba8085de3193026176bff`.
- Composition public13 archive: SHA-256 `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`; 77 listed archive members.
- Runtime producer artifact version: `sha256:6f000bc615a9cb24fb00cc69a97af75eae71006ebfe87e3caa272fcdbbb1af56`; `contract/artifacts.json` contains 75 artifacts.

## Commands and evidence

Passed exact selector collection locally, with the named command's same config
and spec path plus `--list`:

```text
env ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-2c4ac180 \
TIMELINE_BUNDLE_AGENT_HEAD=8130a401bf44a518d5a40ae274d398b8c560be55 \
TIMELINE_BUNDLE_RUNTIME_HEAD=2c4ac180c2220bdad966bc01e95ad230e99ce26a \
TIMELINE_CURRENT013_AGENT_SHA=8130a401bf44a518d5a40ae274d398b8c560be55 \
TIMELINE_CURRENT013_RUNTIME_SHA=2c4ac180c2220bdad966bc01e95ad230e99ce26a \
TIMELINE_CURRENT013_PUBLIC_SOURCE_SHA256=9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738 \
TMPDIR=/tmp/tl-ap2-producer-current-ops-one-safety-case-0333 \
node_modules/.bin/playwright test --config playwright.producer-ownership-current-pin.config.ts \
tests/e2e/local/producer-ownership-current-pin.spec.ts --list
```

Result: exactly 1 test collected.

Passed targeted source checks:

```text
node_modules/.bin/eslint --no-cache --no-warn-ignored --max-warnings 0 \
  playwright.producer-ownership-current-pin.config.ts \
  tests/e2e/local/producer-ownership-current-pin.spec.ts \
  tests/e2e/local/support/producer-ownership-current-pin.ts
git diff --check 36dd91257fd13dcad0d58b48c790caa5063b4c8c..HEAD
```

The exact central suite command was:

```text
env ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-2c4ac180 TIMELINE_BUNDLE_AGENT_HEAD=8130a401bf44a518d5a40ae274d398b8c560be55 TIMELINE_BUNDLE_RUNTIME_HEAD=2c4ac180c2220bdad966bc01e95ad230e99ce26a TIMELINE_CURRENT013_AGENT_SHA=8130a401bf44a518d5a40ae274d398b8c560be55 TIMELINE_CURRENT013_RUNTIME_SHA=2c4ac180c2220bdad966bc01e95ad230e99ce26a TIMELINE_CURRENT013_PUBLIC_SOURCE_SHA256=9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738 TMPDIR=/tmp/tl-ap2-producer-current-ops node_modules/.bin/playwright test --config playwright.producer-ownership-current-pin.config.ts tests/e2e/local/producer-ownership-current-pin.spec.ts
```

## Scope and live callers

The safety case remains limited to existing-output ownership:

- Transcript actions → regenerate: existing owned stale output may be deleted; refusal is accepted as a visible, atomic outcome.
- Scene Phase Markers → move existing shots: existing owned output may move and receive its native hold update; refusal is accepted as a visible, atomic outcome.
- Protected foreign/user rows must retain complete raw objects and order through accepted/refused actions, reload, lost acknowledgement, exact retry, and undo.

The test calls the existing `appTest` direct harness, `compositionPublication`,
the Runtime composition-revision genesis/read endpoints, and the mounted
`/tools/video-editor` route. The production UI callers are the existing
`transcriptLaneExtension` / `buildTranscriptCaptionPatch` in
`src/tools/video-editor/dev/transcript-lane/extension.ts`, the existing
`scenePhaseMarkersExtension` / `moveExistingShotsToMarkers` in
`src/tools/video-editor/dev/scene-phase-markers/extension.ts`, and their
registration through `src/tools/video-editor/dev/localExtensions.ts`.

No fresh creation, native host-field writer, or whole-writer closure is claimed.

## Blocker and recommendation

The central run is blocked at the hosted build by the missing
`getSanitizedPlaybackRate` export in the installed Composition package. The
Viewing/App integration owner should repair or provision the exact compatible
Composition package for this App tree. Only after that external repair should
the orchestrator decide whether a new, separately authorized run is warranted;
this worker did not retry the failed case.
