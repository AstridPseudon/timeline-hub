# Normal PCM HTTP repaired-gate qualification

Result: PASS. The repaired portable normal PCM HTTP proof executed all 22
collected tests centrally, with 22 passed and 0 failed in 28.41 seconds.

## Exact source and environment

- Commit: `e5a636d5927aa31375723aa85f40bd32127a7db7`
- Source tree: `5817551647f3cee72e8f5ed2355334cfd8de0f1a`
- Test source SHA-256:
  `468bbc3227dc32b4fa0f8d4f52e610757bb59b5007060957e032e837fb1ac05e`
- Node: `v20.19.4`
- Python: `3.11.17` from `/home/user/work/venv-agent`
- Frozen candidate Composition artifact:
  `remotion/artifacts/banodoco-timeline-composition-0.0.12.tgz`
- Artifact SHA-256:
  `0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`
- Helper SHA-256 values:
  - `normal-audio-sources.mjs`:
    `dc260d6980f3fc6ff0340b364d810cd4310cc3c663db836ab9c84f6ee5dd14e4`
  - `attempt-envelope-pcm.mjs`:
    `db7bc06d2b3c9efecac015d59d965ef4dfa718e13f1ef303f190c3831bc95719`
  - `compiled-audio-source-clock.mjs`:
    `6ce210e91547d8bca901dc23fe3b06eae0d463fa18d6e1cb79d23494f5145ffc`

The frozen R4 refs do not contain these public-12 helper paths. The candidate
identity used here is therefore the exact checked-in public-12 artifact and
helper source set above, at the exact Agent commit/tree above.

## Preflight

Borrowed project:
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-pcm-http-portable-test/project`

- All 77 archive members were compared byte-for-byte with the borrowed
  `@banodoco/timeline-composition` package: PASS.
- All three actual helper copies in the borrowed project were byte-equal to
  the candidate sources: PASS.
- Actual Node ESM imports of all three helpers passed; import created zero new
  `Socket` or `Server` handles relative to the process baseline: PASS.
- The borrowed project remained unchanged after the central run: 77 package
  files and all helper hashes still matched.
- No shared dependency, cache, product source, or worktree file was changed.

## Central evidence

Request/result:
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/vw-m3-http-portable-repaired-gate-integration-viewing-normal-pcm-http-portable-1020100202-7165`

Exact command:

```text
env -u NODE_OPTIONS -u NODE_PATH ASTRID_REMOTION_PROJECT_DIR=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-pcm-http-portable-test/project PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" PATH=/tmp/vw-m3-agent-gate-node20.19.4/bin:$PATH /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/packs/rendering/test_normal_audio_http.py
```

Result: `22 passed in 28.41s`. The request was submitted with `--no-cache`.

The prior stale-environment run was
`vw-m3-pcm-http-portable-test-integration-viewing-normal-pcm-http-portable-1020095009-3822`:
3 pure path tests passed and 19 HTTP cases failed before consumption because
the borrowed project lacked `attempt-envelope-pcm.mjs`. After the project was
repaired, this fresh central run was authorized and completed all 22 cases.

No local HTTP qualification, full suite, browser, render, install, or network
claim is made. Central localhost HTTP is the only socket-backed test evidence.
