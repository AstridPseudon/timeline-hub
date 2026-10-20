# Normal PCM HTTP corrected final gate

## Result

PASS. The corrected normal-route proof executed all 19 collected cases in the
central test service. The final central source snapshot tree was
`84461f34344977181d5ee3eeaf58c1e372e9b607`.

Final result directory:
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/vw-m3-pcm-http-corrected-final-gate-targeted-1020093304-8154`

```text
test vw-m3-pcm-http-corrected-final-gate-targeted-1020093304-8154: pass exit=0
cmd: /home/user/work/venv-agent/bin/python -m pytest -q tests/packs/rendering/test_normal_audio_http.py
counts: 19 passed in 23.37s
```

The 19 cases are three full/window/layer success cases, nine encoder
error/cancel/timeout cases, three retry cases, one reused-materialized-root
case, and three native-preparation-error cases. Real HTTP GETs are performed
with proxy-free `urllib` against every materialized asset URL and generated
native-WAV `render_source` URL during mocked encoder consumption. The test
checks live server/derived-file lifetime, native float-WAV headers/channels/
sample count/phase, fade gain, clip mute/boost and track scalar handling,
source/registry immutability, retry, cancellation/error cleanup, and reused
root retention.

## Fixture and overlay preflight

Before the final central request, socket-free validation passed for the
corrected fixture through `Timeline.load(...).for_render(default_theme=
"banodoco-default").to_json_data()` and `_serialize_timeline` for full,
window, and layer requests. Collection reported 19 tests. Ruff and
`git diff --check` passed.

The test now uses the readonly producer-owned project overlay:
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-normal-pcm-producer-current/checks/remotion`.
Its public12 package is version 0.0.12, exactly 77 files, and every extracted
file is byte-equal to
`remotion/artifacts/banodoco-timeline-composition-0.0.12.tgz` with SHA-256
`0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`.
The six leaf links resolve only to that private package or
`/home/user/work/composition/node_modules` peers. The producer helper
`normal-audio-sources.mjs` is byte-equal to the repository source:
`dc260d6980f3fc6ff0340b364d810cd4310cc3c663db836ab9c84f6ee5dd14e4`.
No App node_modules or scenegraph source is imported.

## Real components versus doubles

Real: normal `_execute_remotion_locked` route, `AssetMaterializer`,
`InvocationAssetServer`, native PCM preparation helper, managed staging and
cleanup, loopback HTTP serving, and independent HTTP GET consumers.

Explicit doubles: final encoder subprocess consumption; project/runtime
admission (`_validate_project_dir`), element-registry regeneration/effect
validation, canonical profile/theme/effect staging, and available-port
selection. The test uses real Node 20.19.4 helper execution; it does not claim
native host admission for the mocked encoder.

## Corrections and limitations

The earlier central run failed before HTTP because the pre-correction fixture
had unsupported `clips[*].opaque` fields. The corrected fixture passed
serializer validation. The first post-correction run then exposed two
test-only issues: derived `audio` props were compared as authored clips, and
the route-proof overlay had a broken relative package link. The test now
asserts exact authored fields while allowing only generated `audio`, and uses
the valid readonly producer overlay. A subsequent central run exposed
inherited forbidden loader variables; the test explicitly removes those
variables before exercising the real preparation validator. No product files
or semantic expectations were weakened.

This is a normal PCM HTTP/WAV component proof only. It makes no MP4,
renderer parity, browser, native-host, full-suite, or installation/network
claim. No empty/sparse-layer extent proof was added.

## Source hashes

```text
tests/packs/rendering/test_normal_audio_http.py 2c0a2cfe3491a9cb9065aff4ee91141e8a94caa91f68725848cd499ad06ae602
astrid/core/rendering/service.py 930f7d6914bc4cb36d65e266e7fbaf83e625e6ed9466ce6426551631f477ec22
astrid/core/timeline/banodoco_composer.py 5cf8139312e813143adaf84c5a9a9e45d9ad6ce6be9a5dabd667df0048203a4f
astrid/packs/rendering/rendering/renderers/remotion/run.py 37a43a6bfcc2806d09f0b9149c9301c2c833cd6a807c624c77e19076151b284a
astrid/packs/rendering/rendering/renderers/remotion/normal_audio.py 00e46437f1199488260fa6b3409297eddbb2b827ec7a1d0be1b6fff3fbf2b74a
remotion/normal-audio-sources.mjs dc260d6980f3fc6ff0340b364d810cd4310cc3c663db836ab9c84f6ee5dd14e4
remotion/compiled-audio-source-clock.mjs 6ce210e91547d8bca901dc23fe3b06eae0d463fa18d6e1cb79d23494f5145ffc
remotion/artifacts/banodoco-timeline-composition-0.0.12.tgz 0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3
```

