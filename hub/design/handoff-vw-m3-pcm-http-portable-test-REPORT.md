# Normal PCM HTTP portability cleanup

## Delivered

Only `tests/packs/rendering/test_normal_audio_http.py` changed. The hardcoded
orchestrator and worker project fallback is removed. `_project_dir()` now uses
the imported renderer's `remotion.REPO_ROOT / "remotion"` when
`ASTRID_REMOTION_PROJECT_DIR` is absent or empty, while preserving an explicit
override. Three pure tests cover default, empty, and explicit configuration.
The module docstring names the actual admission, registry, profile/theme/effect
staging, port, and final encoder doubles.

Final source SHA-256:

```text
468bbc3227dc32b4fa0f8d4f52e610757bb59b5007060957e032e837fb1ac05e  tests/packs/rendering/test_normal_audio_http.py
```

## Offline evidence

```text
AST parse: PASS
Ruff: PASS (`ruff check tests/packs/rendering/test_normal_audio_http.py`)
Pure path tests: 3 passed, 19 deselected
Collection: 22 tests collected
Serializer preflight: 3 modes passed (full, window, layer)
git diff --check: PASS
```

Private project:
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-pcm-http-portable-test/project`

The Composition 0.0.12 artifact is SHA-256
`0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`, with
exactly 77 archive members and 77 extracted package files. Its 22 peer links
are leaf links resolving under `/home/user/work/composition/node_modules`.
The private project includes the existing `normal-audio-sources.mjs`,
`attempt-envelope-pcm.mjs`, and `compiled-audio-source-clock.mjs` helpers.

## Central evidence

One central request was made, as required:

```text
vw-m3-pcm-http-portable-test-integration-viewing-normal-pcm-http-portable-1020095009-3822
```

The central command collected and executed all 22 tests: 3 pure tests passed,
but all 19 HTTP cases failed before consumption because the initial private
project build omitted `attempt-envelope-pcm.mjs`. The project was repaired
after that run. A second localhost request was not made because this task
allows one central request. Therefore the corrected 19-case HTTP behavior is
not claimed as centrally qualified.

Portable owner-configured command (set the project to the owner-approved
installed bundle):

```sh
env -u NODE_OPTIONS -u NODE_PATH \
  ASTRID_REMOTION_PROJECT_DIR=/absolute/path/to/owner/remotion-project \
  PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" \
  PATH=/tmp/vw-m3-agent-gate-node20.19.4/bin:$PATH \
  /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider \
  tests/packs/rendering/test_normal_audio_http.py
```

