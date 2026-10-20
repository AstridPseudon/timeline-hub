# Final current-caller PCM HTTP/WAV proof

## Source and setup

Applied the exact frozen current caller scope from
`handoff-vw-m3-pcm-caller-current-land-unit-scope.patch` to current
integration `43d567f9d`. The frozen caller tree is
`303452fe7aa075d8451f641f577db7dcd0b74ca2`; the patch SHA-256 is
`3a2cde22fc6bb979e96bd64cd0efc958a626f9e7e223a00f57e3a6e51a7bd03e`.

Private project setup completed at:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-pcm-current-http-final-proof/audio-project`

It contains the exact public 0.0.12 Composition archive (77 regular files,
SHA-256 `0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`),
three helper copies byte-identical to current source, real private scopes, and
read-only leaf links to the shared Composition peer graph. No shared graph,
runtime, venv, node_modules, cache, or other worktree was changed.

The pre-request Node probe imported all three actual project helper modules,
verified all three source/project hashes, counted all 77 package files, and
observed zero new socket/server handles.

## Evidence

- Caller component tests with the private project environment: **29 passed**.
- Frozen caller worker targeted component suite: **266 passed, 1 deselected**;
  its six serialized Root clock goldens and failure/cleanup/retry cases passed.
- Frozen caller central HTTP lane without explicit project override: **22
  passed in 25.19s** (`vw-m3-pcm-caller-current-land-unit-integration-viewing-normal-pcm-http-1020104047-30462`). This is retained evidence only; it is not the requested private-project-env repeat.
- `git diff --check`: **pass**.
- Ruff: **13 inherited diagnostics** in the frozen service/runner cohort,
  matching the caller worker's unchanged-lint fingerprint; no diagnostics were
  introduced or fixed.

## Blocker

The required new named central suite line for this worker's explicit
`ASTRID_REMOTION_PROJECT_DIR` has not been added to
`scratchpad/orch/tests/suites.conf`. I wrote the exact command and environment
fingerprint first in
`handoff-vw-m3-pcm-current-http-final-proof-READY.md`, as required. I did not
edit the shared suite file or reuse another worker's project directory, so the
authorized environment-repair repeat was not submitted.

No local socket/HTTP run, browser, render, MP4, native-host, parity, Runtime
certificate, install, network, or full suite was run.

Next step: manager registers the READY command as a named suite, then submit
that one explicit-project-env repeat and record its result here.
