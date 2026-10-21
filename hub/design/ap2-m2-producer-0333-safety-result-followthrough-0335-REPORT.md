# M2 producer safety result follow-through — case0333

## Decision

Do not deliver the reviewed producer ownership guard repair `9a5e9ed6c`.
The only authorized current-ops run failed before the browser, Runtime door,
producer packet, or any route assertion. Therefore there is no actual evidence
to qualify accepted transcript removal, accepted Scene move-plus-hold, or an
explicit unsupported refusal, and no evidence that protected IDs, raw objects,
or order survived reload, lost acknowledgement, exact retry, or undo.

The source/draft safety boundary is preserved. No executor chain was started,
no retry was submitted, and no App source, DTO, field, pin, or fixture was
changed by this worker.

## Actual case0333 result

The single permitted central run was:

```text
env ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-2c4ac180 TIMELINE_BUNDLE_AGENT_HEAD=8130a401bf44a518d5a40ae274d398b8c560be55 TIMELINE_BUNDLE_RUNTIME_HEAD=2c4ac180c2220bdad966bc01e95ad230e99ce26a TIMELINE_CURRENT013_AGENT_SHA=8130a401bf44a518d5a40ae274d398b8c560be55 TIMELINE_CURRENT013_RUNTIME_SHA=2c4ac180c2220bdad966bc01e95ad230e99ce26a TIMELINE_CURRENT013_PUBLIC_SOURCE_SHA256=9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738 TMPDIR=/tmp/tl-ap2-producer-current-ops node_modules/.bin/playwright test --config playwright.producer-ownership-current-pin.config.ts tests/e2e/local/producer-ownership-current-pin.spec.ts
```

Result: exit 1 in 23 seconds. The first failure was during hosted build setup:

```text
src/tools/video-editor/compositions/playerEvaluation.ts:5
getSanitizedPlaybackRate is not exported by
@banodoco/timeline-composition/dist/evaluation.js
```

This is the first packet/assertion/fixture boundary: module loading in
`npm run build:hosted`, before browser launch. No Runtime request was sent and
no test-body assertion ran. The run was not retried.

The local dependency check supports a provisioning mismatch diagnosis, without
changing it: the shared installed package reports version `0.0.8` and has no
`getSanitizedPlaybackRate` export, while the App repository's vendored archive
is `0.0.13` with SHA-256
`9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`.
Shared dependencies are read-only, so this worker did not repair or replace
them.

## What is and is not qualified

| Route/outcome | Actual case0333 status |
| --- | --- |
| Existing owned transcript output removed | Unverified; no route execution |
| Existing owned Scene output moved and held | Unverified; no route execution |
| Explicit unsupported refusal | Unverified in the actual case; do not relabel the build failure as a product refusal |
| Future fresh creation | Not covered by this case and remains unverified |
| Protected IDs present, full raw objects unchanged, order unchanged through body/key/reload/retry/undo | Unverified; none of those assertions ran |

The live production callers remain the existing
`transcriptLaneExtension`/`buildTranscriptCaptionPatch` path in
`src/tools/video-editor/dev/transcript-lane/extension.ts`, and the existing
`scenePhaseMarkersExtension`/`moveExistingShotsToMarkers` path in
`src/tools/video-editor/dev/scene-phase-markers/extension.ts`, registered by
`src/tools/video-editor/dev/localExtensions.ts`.

## Separate source-only evidence and open gaps

The reviewed `9a5e9ed6c` repair has source-only evidence from its own report:
494 focused tests passed, including compiler -> reload -> reader ownership
checks and protected foreign/user deep comparisons. That evidence is not an
actual mounted current-path acceptance proof and is insufficient for delivery
after case0333 stopped at build setup.

The same source report records a separate carrier limitation: the active
generic capture path supports structural `clip.add` but not the app-bearing
`clip.update`, so a mixed producer batch can be explicitly refused. That
future carrier gap is not repaired or bypassed here. Fresh `managedBy`
compiler/reload evidence and the carrier gap remain separately labeled; broad
ordinary editing remains OPEN.

## Commands run by this worker

No browser, socket, localhost, full suite, or unchanged behavioral test replay
was run. Read-only checks were:

```text
git status --short --branch
git log -1 --format='%H%n%T%n%s'
node -e "const p=require('./node_modules/@banodoco/timeline-composition/package.json'); console.log(JSON.stringify({version:p.version,exports:p.exports},null,2))"
node - <<'NODE'
import('@banodoco/timeline-composition/evaluation').then(m => console.log({hasSanitized: typeof m.getSanitizedPlaybackRate, keys: Object.keys(m).filter(k => k.toLowerCase().includes('playback') || k.toLowerCase().includes('sanitize')).sort()}))
NODE
sha256sum vendor/artifacts/banodoco-timeline-composition-0.0.13.tgz
tar -xOf vendor/artifacts/banodoco-timeline-composition-0.0.13.tgz package/package.json
```

Results: clean worktree; installed package `0.0.8`, missing export; vendored
archive `0.0.13` with the digest above. No code tests were run because the
task explicitly forbids replaying unchanged tests after the actual case
failure.

## Next step

Viewing/App integration should provision the exact compatible Composition
package in the central test environment. Only after that external repair and a
newly authorized run should the orchestrator reconsider the 9a5e9ed6c source
delivery. This worker does not request or submit that run.
