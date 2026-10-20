# Native extent + Root regression test unit

## Scope

- Base/source commit: `61f1a420f1f355ee0d16ffb0dbeb617b83b1b044`
  (`tl/vw-m3-native-layer-extent-fix`), after the harness producer commit; it
  is not `abd41eb2a`.
- Root-test reference: `cfb7d7c4e79dc6fbc25437430d124af77aa5547b` on
  `tl/vw-m3-root-extent-regressions`.
- Changed path: `remotion/tests/root-metadata.test.cjs` only.
- The added file is byte-identical to the reference file and to the
  root-regression final patch: 227 lines, blob
  `b7c49bbf35883de0e75d863fd84e7f96624ca138`, SHA-256
  `181950efa7e91f646d57496b33897e4e40ec6723c695f6bb6d8ffe940443b6cc`.
- No product files, Root implementation, DTOs, package pins, authority, or
  graph/runtime changes were made.

## Tests

1. `ROOT_SOURCE_DIR="$PWD/src" /tmp/vw-m3-agent-gate-node20.19.4/bin/node tests/root-metadata.test.cjs`
   — PASS, 7/7.
2. `ROOT_SOURCE_DIR="/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-native-extent-final-review/candidate/remotion/src" /tmp/vw-m3-agent-gate-node20.19.4/bin/node tests/root-metadata.test.cjs`
   — PASS, 7/7 against the frozen review candidate source.
3. `env -u PYTHONPATH -u NODE_OPTIONS -u NODE_PATH PYTHONDONTWRITEBYTECODE=1 ASTRID_NODE_EXECUTABLE=/tmp/vw-m3-agent-gate-node20.19.4/bin/node ASTRID_REMOTION_PROJECT_DIR=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-native-extent-final-review/audio-project /home/user/work/venv-agent/bin/python -B -m pytest -q -o addopts= -p no:cacheprovider --tb=short tests/packs/rendering/test_native_layer_extent.py tests/packs/rendering/test_remotion_native_window.py tests/packs/rendering/test_normal_audio_run.py tests/packs/rendering/test_normal_audio_sources.py tests/packs/rendering/test_normal_audio_source_phase.py`
   — PASS, 127 passed in 13.62s.

An initial combined Python invocation was intentionally not treated as
evidence: it omitted the approved Remotion project environment and retained
`PYTHONPATH`, producing 18 setup errors and 21 environment-related failures.
The corrected, cache-free command above passed all 127 tests.

## Review status and boundaries

- The independent final extent review’s producer checks and Root candidate
  checks are green; the original baseline Root regression cases were red as
  intended and the candidate Root unit is green.
- The separate `precision_for_render` change is preserved unchanged and is
  **HELD**, not approved by this extent test grant.
- Tail semantics, Runtime/public12 adoption, HTTP/MP4 behavior, graph
  qualification, render/browser/socket parity, and whole-unit merge readiness
  remain outside this unit and held. This report makes no such claims.
- No full, browser, socket, render, install, network, or git mutation command
  was run.

## Flat artifacts

- Report: this file.
- Test evidence: `handoff-vw-m3-native-extent-root-test-unit-tests.log`.
- Source state: `handoff-vw-m3-native-extent-root-test-unit-source.json`.
- New-test-only patch: `handoff-vw-m3-native-extent-root-test-unit-flat.patch`.

