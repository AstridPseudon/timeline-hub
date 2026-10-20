# App D08 continuous PCM consumer

Implemented the prepared public13 consumer on the exact requested App owner base `b1ef4b9b910ba72375c34cf319692f90d22edc25` (tree `8d8a10b057ed31fed69517e18a23b8ec3811447a`). No package, lockfile, pin, store, DTO, clock/compiler, or source-factory files changed.

## Product delta

- `AudioTrack.tsx` now uses the public Composition evaluation APIs for prepared-source admission, full-source decode, continuous PCM envelope application, WAV creation, media trim, and sanitized rate.
- Ordinary envelope preview preparation stays inside the existing retry/abort/stale/lifetime attempt. It closes `AudioContext`, revokes Blob URLs, renews the existing hold from source chunks, bounds starvation, and preserves native readiness/retry/teardown.
- Native playback receives one constant track×clip gain. Rendering requires an already matching prepared source and never browser-decodes. Ordinary native audio without an envelope remains native.
- Added the two prepared-source/lifetime direct suites. Existing audio and media-conformance assertions were migrated from the retired frame-volume callback to continuous-PCM source identity and constant downstream gain; native lifecycle, mute, boost, retry, export, and failure positives remain.

## Qualification

Public Composition 0.0.13 was extracted privately from the provided artifact (SHA256 `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`). The normal App installation remains public12 because the owner-held public13 package/lock pin is not approved in this branch. Therefore this is overlay qualification only, not consumer-release qualification.

Exact targeted command: see the sibling `.COMMAND` file. Result: **5 files, 83 tests passed**, 10.31s. This includes the two direct suites (24 tests), `AudioTrack.test.tsx`, `RemotionPreview.audioFailure.test.tsx`, and `TimelineComposition.media-conformance.test.tsx`. The pre-migration 91-case neighbor run exposed 41 policy-mismatch failures (38 AudioTrack cases and 3 conformance cases); callback-only matrices were replaced by focused continuous-PCM assertions, so the qualified post-migration total is 83 rather than a claim that 91 unchanged cases remain.

Targeted ESLint over all touched App/test files: **exit 0**, no diagnostics. `git diff --check`: **exit 0**.

## Not run / pending

No full suite, browser, rendering, live socket, network, install, project typecheck, normal-root public13 run, physical Player/export PCM capture, or central Gate 6 positive/planted-negative was run. App owner must first adopt the immutable public13 package and lock bytes, then independently review/merge this leaf and run the owner typecheck plus the central physical Player/export qualification. The consumer remains held pending that pin and review.

## Artifacts

- Sibling `.patch` contains the applied tracked and untracked source/test delta.
- Sibling `.files` lists the five changed App files.
- Sibling `.COMMAND` records the exact targeted commands.
