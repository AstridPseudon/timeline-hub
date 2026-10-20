# READY — final current caller HTTP/WAV proof

Source cohort is the frozen current caller tree `303452fe7aa075d8451f641f577db7dcd0b74ca2`, represented in this worktree by the exact frozen scope patch
`handoff-vw-m3-pcm-caller-current-land-unit-scope.patch` (SHA-256
`3a2cde22fc6bb979e96bd64cd0efc958a626f9e7e223a00f57e3a6e51a7bd03e`). The frozen source JSON is
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-pcm-caller-current-land-unit-source.json`.

Private project (owned by this worker):
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-pcm-current-http-final-proof/audio-project`

The project was built from the current Agent tree's public 0.0.12 artifact and
the three current helper files, with real private package scopes and only
read-only leaf links to Composition peers. It must be passed explicitly as
`ASTRID_REMOTION_PROJECT_DIR`.

## Named-suite line for the manager

```text
agent integration-viewing-normal-pcm-http-final-current env -u NODE_OPTIONS -u NODE_PATH ASTRID_REMOTION_PROJECT_DIR=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-pcm-current-http-final-proof/audio-project PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" PATH=/tmp/vw-m3-agent-gate-node20.19.4/bin:$PATH /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/packs/rendering/test_normal_audio_http.py
```

This is the requested targeted environment-repair repeat of the already
authorized current-caller HTTP lane. Do not alter another suite line.

## Preflight fingerprint before request

- Node: `/tmp/vw-m3-agent-gate-node20.19.4/bin/node` (20.19.4)
- Python: `/home/user/work/venv-agent/bin/python`
- Artifact: `remotion/artifacts/banodoco-timeline-composition-0.0.12.tgz`, SHA-256 `0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`, 77 archive members
- Helper source files: `remotion/normal-audio-sources.mjs` (`dc260d6980f3fc6ff0340b364d810cd4310cc3c663db836ab9c84f6ee5dd14e4`), `remotion/attempt-envelope-pcm.mjs` (`db7bc06d2b3c9efecac015d59d965ef4dfa718e13f1ef303f190c3831bc95719`), and `remotion/compiled-audio-source-clock.mjs` (`6ce210e91547d8bca901dc23fe3b06eae0d463fa18d6e1cb79d23494f5145ffc`)
- Test: `tests/packs/rendering/test_normal_audio_http.py` (`468bbc3227dc32b4fa0f8d4f52e610757bb59b5007060957e032e837fb1ac05e`) is the unchanged portable 22-test source from the frozen current caller handoff
- No local socket test will run; the named central service is the only HTTP execution

Preflight command to run before requesting the named suite:

```sh
env -u NODE_OPTIONS -u NODE_PATH PATH=/tmp/vw-m3-agent-gate-node20.19.4/bin:$PATH node --input-type=module -e 'for (const name of ["attempt-envelope-pcm.mjs","compiled-audio-source-clock.mjs","normal-audio-sources.mjs"]) { await import(process.cwd()+"/remotion/"+name); }' && test "$(find /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-pcm-current-http-final-proof/audio-project/node_modules/@banodoco/timeline-composition -type f | wc -l)" -eq 77
```

