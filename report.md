# Gate6 frozen export tuple preparation

## Result

Prepared a fail-closed invocation packet and source-guard checklist for the
current App owner controller. No product files, integration worktrees, grants,
markers, credentials, render jobs, or browser jobs were changed or launched.

Gate6 remains **HELD**. The current `/home/user/work/app` integration checkout
is at `157eef8cf1151db09310153c10856d45d8590c87` (tree
`1deb8b48fe1fbd26a97ff816084640be6bb358dc`) and does not yet contain the
approved controller successor `fabe262c01725faf28999f0e650c7dfe701925df`.
It also has pre-existing untracked vendor entries, so it is not a qualifying
clean App source for `--ready`.
That successor is the existing controller source whose guards separate Agent
server `d0a5072b`, Runtime server `8f105c26`, and official Runtime client
producer `2c4ac180`; the packet therefore does not silently claim the current
App checkout is ready.

The durable packet is exported as:

- `design/handoff-vw-m3-gate6-frozen-export-tuple-prep-invocation.md`
- `design/handoff-vw-m3-gate6-frozen-export-tuple-prep-guards.md`

## Existing evidence verified

The retained MP4 was read-only verified at:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-normal-three-media-public13-mp4/task-43b122b9d463400ba4cdecd779603914.mp4`

- SHA-256: `ba653c490689847a31033babc48dba64f6322549fa2b98b12e615ea58658bbc9`.
- H.264 High, 1920x1080, 30 fps, 165 frames, 5.5 s.
- AAC-LC, 48 kHz, stereo, 5.5 s.
- `ffmpeg -xerror -err_detect explode` video and audio null decodes passed.

This proves retained MP4 identity/decode only. It is not Player/export frame
parity, PCM parity, or Gate6 closure evidence.

## Checks

Passed:

```text
ASTRID_NODE_EXECUTABLE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node \
  node --check /home/user/work/app/tests/e2e/timeline/viewing-parity/tab-audio.controller.mjs
ASTRID_NODE_EXECUTABLE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node \
  node --test /home/user/work/app/tests/e2e/timeline/viewing-parity/tab-audio.controller.test.mjs
ASTRID_NODE_EXECUTABLE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node \
  node /home/user/work/app/tests/e2e/timeline/viewing-parity/tab-audio.controller.mjs --discover /home/user/work/app
git status --short --branch
ffprobe ... retained MP4
ffmpeg -xerror -err_detect explode ... -f null -  # video
ffmpeg -xerror -err_detect explode ... -f null -  # audio
sha256sum ... retained MP4
```

The controller checks passed; discovery reported exactly five current
`native-codec-chrome155` cases. The Composition direct TypeScript attempt was
not a valid test run. The exact attempts were:

```text
/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node --import ./typescript/tests/register-extensionless.mjs --test typescript/tests/scene-evaluation.test.ts typescript/tests/evaluation.test.ts typescript/tests/audio-envelope-admission.test.ts
  FAIL: Node reported ERR_UNKNOWN_FILE_EXTENSION for .ts.
npx tsc -p typescript/tsconfig.test.json --outDir <private /tmp staging>
  FAIL: this worktree has no local React/Remotion/@types/node dependencies.
```

The read-only shared App `node_modules` cannot be linked or modified by this
task. No build output remains in the worktree.
No install, browser, render, full suite, or central Gate6 suite was run.

## Decisions and limits

- The packet uses the existing `e2e-viewing-gate6-current-fivecase` suite and
  controller; no framework or new invocation machinery was added.
- The packet requires the actual owner-integrated App source/tree, a frozen
  `VIEWING_FRAME_SOURCE_TUPLE`, a fresh `TAB_AUDIO_GRANT_PATH`, and a fresh
  `TAB_AUDIO_RUN_MARKER`. None were minted or consumed here.
- The positive/negative contract is explicit: the four normal/fixture/frame/tab
  cases must complete, then the picture-only patch must fail the frame bound.
  Any physical audio claim must use decoded PCM with frequency/FFT-bin,
  timing/envelope, phase continuity, gain on both channels, and stereo checks;
  RMS-only comparison is insufficient.
- The existing five-case tab capture case records a native-PTS VP8/Opus stream
  but does not itself claim a physical mix. The packet keeps that claim held
  until the owner sequence supplies the approved full PCM comparison evidence.

Recommended next step: after the actual App owner merge lands, fill only the
four manager-owned packet inputs, rerun offline `--ready`, and let the manager
launch the named suite once under the central browser lock.
