# Independent review: corrected normal PCM HTTP final gate

## Verdict

**APPROVE, narrowly scoped.** The corrected test-only gate has sufficient
evidence for the normal PCM HTTP/WAV component proof on the exact final source
tree. It does not certify Runtime admission, a native host, MP4, browser,
renderer/audio parity, installation/network setup, or product-wide adoption.

## Source and run identity

- Final harness commit: `8cef91fa8d2603d26403defae6c26118f0467cdf`
- Final source tree: `84461f34344977181d5ee3eeaf58c1e372e9b607`
- Passing central result: `.../tests/vw-m3-pcm-http-corrected-final-gate-targeted-1020093304-8154`
- Result: `19 passed in 23.37s`, exit 0.
- The passing snapshot tree is exactly `HEAD^{tree}` and the touched test
  hash is `2c0a2cfe3491a9cb9065aff4ee91141e8a94caa91f68725848cd499ad06ae602`.
- The reported product/source hashes match the checked-out final tree for
  `service.py`, `banodoco_composer.py`, `run.py`, `normal_audio.py`, the two
  Remotion helpers, and the public12 tarball.

The earlier pre-HTTP fixture run remains historical: tree `2f2ebbb…`, 19
failures before HTTP because the fixture used unsupported `clips[*].opaque`.
The later integration-named request at 09:31:27 used stale tree `4e19d…` and
failed 16/19 on derived `audio`-property comparison; it is not the final gate
result. The final targeted request at 09:33:04 used tree `84461f…` and passed.

## Independent source review

The final test invokes the real `_execute_remotion_locked` normal route. The
route uses the real `AssetMaterializer`, real `InvocationAssetServer`, real
native PCM preparation helper/Node 20.19.4 execution, managed staging, and
ExitStack cleanup. The test wraps the server lifecycle only to observe it and
replaces only the final encoder subprocess. The replacement performs direct,
proxy-free `urllib` GETs against every materialized asset URL and every
generated native-WAV `render_source` URL while the real server is live.

The 19 collected cases are exactly:

- 3 full/window/layer success cases;
- 9 encoder error/cancel/timeout cleanup cases;
- 3 retry cases;
- 1 reused materialized-root case; and
- 3 native-preparation-error cases.

The assertions verify final serialized Root props retain exact authored clip
and track fields, allowing only generated `audio`; check clip volume 3 and 0
(boost and mute) and track scalars 0.5 and 2; and validate native float-WAV
RIFF/fmt/data headers, stereo channels, 30,000 Hz rate, 60,000-frame length,
fade gain, and phase (`source_from == 0`, `playback_rate == 1`). They also
verify live server/file lifetime, server shutdown, derived-file removal,
retry staging separation, reused-root source retention, timeline/registry
byte immutability, and removal of props/runtime/staging leftovers.

Explicit doubles, as required: final encoder subprocess consumption;
`_validate_project_dir`; element-registry regeneration/effect validation;
canonical profile/theme/effect staging; and available-port selection. These
are clearly test doubles. The proof does not present them as native-host or
Runtime-admission evidence.

## Overlay and integrity review

The private overlay uses public12 package version 0.0.12. The archive SHA-256
is `0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`, and
all 77 regular archive members are byte-equal to the extracted package. The
helper hash is
`dc260d6980f3fc6ff0340b364d810cd4310cc3c663db836ab9c84f6ee5dd14e4`.
The six overlay links resolve only to the private package or read-only
Composition peers under `/home/user/work/composition/node_modules`; no App
node_modules or scenegraph source is imported.

## Checks run by this review

- Read-only AST/source identity audit: PASS.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -B -m pytest -p no:cacheprovider --collect-only -q tests/packs/rendering/test_normal_audio_http.py`: **19 collected**, PASS.
- `/home/user/work/venv-agent/bin/ruff check tests/packs/rendering/test_normal_audio_http.py`: PASS.
- `git diff --check`: PASS.
- No behavior suite was rerun; the unchanged-tree 19-case PASS was reviewed
  from the central result and source snapshot.

## Limitations and next step

Approve this component gate only. Preserve the distinction between the
passing final targeted central result and the stale failed integration-named
request in any aggregate report. Any broader claim requires separately
qualified Runtime/native-host, MP4, browser, parity, or adoption evidence.
