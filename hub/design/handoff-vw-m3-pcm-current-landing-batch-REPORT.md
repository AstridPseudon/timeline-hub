# PCM current landing batch

Prepared on `tl/vw-m3-pcm-current-landing-batch` at base `d65471fd0d34d1e87c26486e56a39b8c40289ad5`, which is the requested `tl/vw-m3-pcm-producer-red-fix` head.

## Change

Added only `remotion/tests/normal-audio-native-sources.test.mjs`, copied byte-for-byte from donor commit `27b53e155` (git blob `3704149629089239afb26f1a3b720ea49cf49ed1`). It is 278 lines. No donor merge and no product/source changes were made.

The reviewed inactive producer fixes were left unchanged. The concurrent final landing review completed with approval for this inactive prerequisite; its normal-route activation, public12 adoption, and served-HTTP qualification holds remain open.

## Focused qualification

All commands ran without installs, sockets, browsers, renderer activation, or full-suite execution, using the shared Agent venv, Node `v20.19.4`, public12 Composition `0.0.12`, and shared read-only peer links (Remotion `4.0.509`, React/React DOM `18.3.1`, Remotion media/layout `4.0.509`). Public12 artifact SHA256 and all 77 package members were independently verified.

- Python lane: `51 passed, 2 xfailed` (the existing compiler xfails), exit 0.
- Native Node lane: `5 passed`, exit 0.
- Normal Node lane: `8 passed`, exit 0.
- Long Node lane: `2 passed`, exit 0.

The native/long lanes retained 8,388,609 stereo 48 kHz frames (67,108,872 decoded bytes) and produced the expected WAV SHA256 `8592a32de5b2c4f46fd176ac2129edfcea2ab9489aa0b0e178c8049b2e4681a2`; the gapless MP3 case retained 86,400 frames and native float bytes.

Exact focused commands:

```sh
cd /home/user/work/wt/vw-m3-pcm-current-landing-batch

env -u NODE_OPTIONS -u NODE_PATH PATH=/tmp/vw-m3-agent-gate-node20.19.4/bin:$PATH \
  PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD \
  ASTRID_REMOTION_PROJECT_DIR=/tmp/vw-m3-pcm-current-landing-batch-check/remotion \
  /home/user/work/venv-agent/bin/python -B -m pytest -p no:cacheprovider -q \
  tests/packs/rendering/test_normal_audio_sources.py \
  tests/packs/rendering/test_normal_audio_source_phase.py \
  tests/editing_conformance/test_compile_contracts.py

cd /tmp/vw-m3-pcm-current-landing-batch-check/remotion

env -u NODE_OPTIONS -u NODE_PATH PATH=/tmp/vw-m3-agent-gate-node20.19.4/bin:$PATH \
  /tmp/vw-m3-agent-gate-node20.19.4/bin/node --expose-gc \
  tests/normal-audio-native-sources.test.mjs

env -u NODE_OPTIONS -u NODE_PATH PATH=/tmp/vw-m3-agent-gate-node20.19.4/bin:$PATH \
  /tmp/vw-m3-agent-gate-node20.19.4/bin/node tests/normal-audio-sources.test.mjs

env -u NODE_OPTIONS -u NODE_PATH PATH=/tmp/vw-m3-agent-gate-node20.19.4/bin:$PATH \
  TIMELINE_HEAVY=1 /tmp/vw-m3-agent-gate-node20.19.4/bin/node --expose-gc \
  tests/long-audio-source.test.mjs
```

## Scope audit

- Worktree status: exactly one untracked path, the requested test file.
- `git diff --check` and Node syntax check passed; new-file whitespace check passed.
- Protected-path scan found zero changes to provider, core, compiler, `run.py`, activation, or root-pin paths.
- HEAD branch census: 2,911 tracked files plus the one requested untracked test; top-level counts and product LOC are unchanged from base.
- Product LOC census (tracked authored Python under `astrid` plus non-test/non-script Remotion JS/MJS/TS/TSX): 902 files / 290,334 lines (`astrid` 287,411; `remotion` 2,923).
- No build/cache/temp residue remains in the worktree.

## Limits

No normal-route activation, source validation/serialization, HTTP serving lifecycle, Player/export parity, browser, socket, full suite, or install was run or claimed. No decision deviation or blocker.
