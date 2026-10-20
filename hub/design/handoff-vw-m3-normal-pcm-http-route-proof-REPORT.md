# Normal PCM HTTP route proof — fixture delivered, central rerun blocked

## Scope

Added only the test-owned `tests/packs/rendering/test_normal_audio_http.py`.
No product files were changed. The test enters the actual
`_execute_remotion_locked` normal caller, uses the real `AssetMaterializer` and
real `InvocationAssetServer`, and mocks only the final encoder subprocess.
During mocked consumption it performs proxy-free `urllib` GETs for both
materialized asset URLs and every generated `render_source` URL.

The cases cover full, native window, and native layer requests; complete
native float-WAV headers/data/sample count/channel/rate and phase; two distinct
stereo sources; scalar volume remaining in props (including mute and boost);
authored timeline/registry immutability; live server/derived files during
consumption; success, encoder error, cancellation, timeout, retry, native
preparation error, and reused materialized-root cleanup.

No browser, render/export, MP4, native-host substitute, fabricated source
certificate, helper-only substitute, or shared App/scenegraph import is used.
Empty/sparse-layer cases are not added.

## Exact checks

From `/home/user/work/wt/vw-m3-normal-pcm-http-route-proof`:

```text
/home/user/work/venv-agent/bin/ruff check tests/packs/rendering/test_normal_audio_http.py
PASS

python3 -B -c 'import ast, pathlib; ast.parse(pathlib.Path("tests/packs/rendering/test_normal_audio_http.py").read_text())'
PASS

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD \
  /home/user/work/venv-agent/bin/python -B -m pytest -p no:cacheprovider \
  --collect-only -q tests/packs/rendering/test_normal_audio_http.py
19 tests collected, PASS

git diff --check
PASS
```

The required one central request was made exactly once, before the final
fixture-only correction:

```text
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test \
  vw-m3-normal-pcm-http-route-proof integration-viewing-normal-pcm-http) && \
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test $R
FAIL: 19 failed in 1.84s
```

Central log:
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/vw-m3-normal-pcm-http-route-proof-integration-viewing-normal-pcm-http-1020092606-26925/log.txt`

That run stopped at timeline schema validation: the fixture's two audio clips
contained an invalid `opaque` clip property. Those two fixture-only fields were
removed afterward. The corrected file has static checks and collection green,
but its real HTTP behavior is unverified because the orchestration rule allows
only one central socket-backed request and forbids local socket runs.

The neighboring socket-free `test_normal_audio_run.py` was attempted once
without the required `ASTRID_NODE_EXECUTABLE` (setup failure), then with it;
the latter was rejected by that existing fixture's `PYTHONPYCACHEPREFIX` launch
environment policy. It was not modified.

## Private overlay

Overlay root:
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-normal-pcm-http-route-proof/checks/remotion`

- public12 package: exactly 77 regular files, version `0.0.12`;
- artifact SHA256: `0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`;
- overlay `normal-audio-sources.mjs` SHA256:
  `dc260d6980f3fc6ff0340b364d810cd4310cc3c663db836ab9c84f6ee5dd14e4`;
- peer links are only `@remotion/layout-utils`, `@remotion/media`, `react`,
  `react-dom`, and `remotion`, all leaf links to `/home/user/work/composition`;
- no App node_modules or scenegraph source is imported.

Final test source SHA256:
`b979046c16100f67bae871a6487fa70e96762fefde7dd04388c49b80515e31a7`

## Limitation / next step

This worker is blocked only on post-correction central evidence. Do not treat
the failed central run as HTTP/WAV qualification. The orchestrator should run
the corrected named suite only if it explicitly authorizes an exception to the
one-request rule; otherwise review the fixture correction and schedule the
qualification in the next permitted central slot.
