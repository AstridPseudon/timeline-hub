# Runtime speech WAV HTTP selected-media proof

Date (UTC): 2026-10-20T16:56:09Z

## Source and digest

- Runtime worktree: `/home/user/work/wt/rt-m2-speech615-http-selected-proof`
- Base/source commit: `615a95a63c2ae79c6a47400ffc79a72dedd0bc5f`
- Changed source: `tests/test_generation_publish_v1_settlement.py`
- Changed source SHA-256: `c98f7b1fc8f4c0386fe144b8908308c08efd8c4cfc5aea546a4207b7a7ad6db6`
- Final binary patch SHA-256: `c25a1013b237212b870977a70fbf152eaa3d762871139e58a624104500957ac4`
- Product-code changes: none.

## Proof

One case reuses the existing valid-WAV speech fixture: task admission with
`generation.generate_speech`, executor claim, `generation.publish_v1` settlement,
and Runtime-derived generation/variant/managed-output association. It settles a
real one-second, 8 kHz mono WAV, closes the fixture service, and restarts the
same persisted realm behind a loopback `RuntimeDaemon`.

The case provisions a normal `projects:read` credential and uses the generated
`WorkspaceClient` over HTTP for both public reads:

1. `get_project_media_selection` resolves the exact association/object/version.
2. `get_project_verified_media` consumes that exact selection.

Assertions require the returned object ID to equal the WAV's SHA-256 digest and
the verified response to equal the exact selection, `audio/wav`, byte size, and
`duration_seconds: 1.0`.

## Results

- Central socket-backed test service, exact final tree:
  `request-test rt-m2-speech615-http-selected-proof targeted --files
  "tests/test_generation_publish_v1_settlement.py"`
  - Executed command: `/home/user/work/venv-runtime/bin/python -m pytest -q
    tests/test_generation_publish_v1_settlement.py`
  - Result: **13 passed in 3.58s** (tree
    `5bcd1e7dbb7e0e91d8d3170b8d5a5cf51db7f70`).
- Local non-socket regression:
  `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD"
  /home/user/work/venv-runtime/bin/python -m pytest -q
  tests/test_generation_publish_v1_settlement.py -k
  'not exact_over_authenticated_http'`
  - Result: **12 passed, 1 deselected in 2.94s**.
- `git diff --check`: passed.

## Limits and non-claims

- No full suite, render, model call, or live Speech SDK run was performed.
- The actual Speech SDK does not yet send intent/effect; this proves only the
  Runtime managed-API settlement and generated public-read path.
- This is not a Voiceover or RIPPLE proof.
- No manual client duration, fake generation, latest/adoption lookup, or product
  code change was used.
