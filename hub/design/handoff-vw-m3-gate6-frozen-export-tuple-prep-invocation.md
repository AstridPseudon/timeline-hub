# Gate6 frozen export tuple invocation packet

Status: **prepared / fail-closed / not launched**.

This is the single current-owner invocation. It is valid only after the
approved App owner controller successor `fabe262c01725faf28999f0e650c7dfe701925df`
(`2ff17e39f3a01b4a98350d0b0d257d13a0b37a67` tree) is integrated over the
actual current App owner base. Do not use the older controller constants in
the current App checkout, and do not substitute a self-selected App SHA/tree.

## Exact existing suite/controller

- Suite registration: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/suites.conf`, entry `app e2e-viewing-gate6-current-fivecase`.
- Controller: `tests/e2e/timeline/viewing-parity/tab-audio.controller.mjs`.
- Controller unit: `tests/e2e/timeline/viewing-parity/tab-audio.controller.test.mjs`.
- Playwright config: `playwright.viewing-parity.normal-profile-native1920.config.ts`, project `native-codec-chrome155`, one worker.
- Offline discovery command: `NODE tests/e2e/timeline/viewing-parity/tab-audio.controller.mjs --discover "$APP_ROOT"`.
- Readiness command inside the suite: `NODE tests/e2e/timeline/viewing-parity/tab-audio.controller.mjs --ready "$APP_ROOT" "$AGENT_ROOT" "$RUNTIME_ROOT"`.

The registered suite is launched only by the manager:

```sh
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test \
  integration:app e2e-viewing-gate6-current-fivecase) \
  && /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"
```

Run it once, after all inputs below are present. This packet does not authorize
this worker to submit it.

## Invocation inputs

The suite already supplies these fixed values:

```text
ASTRID_CHECKOUT=/home/user/work/wt/agt-pin-d0a5072b
ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-8f105c26
ASTRID_REMOTION_PROJECT_DIR=/home/user/work/runtimes/agent-remotion-viewing13-d0a5072b
ASTRID_REMOTION_BROWSER_EXECUTABLE=/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell
ASTRID_NODE_EXECUTABLE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node
TIMELINE_COMPOSITION_CHECKOUT=/home/user/work/composition
VIEWING_BROWSER_FLOCK_HELD=1
```

The manager must supply these exact, currently missing inputs:

```text
TIMELINE_VIEWING_APP_SOURCE=<actual 40-char SHA of owner-integrated App>
TIMELINE_VIEWING_APP_TREE=<actual 40-char tree of that same App commit>
VIEWING_FRAME_SOURCE_TUPLE=<path to manager-frozen next-five-case/v1 JSON>
TAB_AUDIO_GRANT_PATH=<path to a fresh approved grant JSON>
TAB_AUDIO_RUN_MARKER=<path to a fresh one-shot marker JSON>
```

The App source and tree must identify the same actual owner-integrated commit;
the controller's leaf/ancestor checks must pass. The tuple, grant, and marker
must be created by the manager/owner sequence, not this packet.

## Five current cases and result contract

Discovery must report exactly these five cases, in this order:

1. `normal App Render action downloads a valid native-size MP4 without a parity comparison`
2. `fixture readiness seeks actual managed Player video and captures native frames without export`
3. `compares native-size actual Player frames with decoded real CPU Remotion task output`
4. `captures the actual Player page as one native-PTS VP8/Opus tab stream without a physical-mix claim`
5. `picture-only one-host patch is reported as a mismatch after the full passing baseline`

Positive requirements are the first four cases, including real App Render
admission/download, managed Player frame capture, decoded export frame
comparison, no legacy write traffic, and one native-PTS tab stream. Case 5 is
the planted-negative: it must first establish the complete passing frame
baseline, then inject only the picture patch and reject the frame bound. A
negative result is not allowed to replace the positive baseline.

Any physical audio parity result attached to this run must compare decoded
stereo PCM from the same Player capture/export pair with one stream-wide offset
only. It must prove all of:

- full PCM decode at 48 kHz stereo;
- per-window frequency/FFT-bin identity and amplitude admission;
- timing/envelope activity identity for every compared block/window;
- phase continuity for capture and export;
- gain agreement on left and right channels;
- stereo stream/channel identity.

An aggregate RMS-only match, mono downmix, independent channel shift, resample,
padding, filtering, or threshold widening is not Gate6 evidence.

## Explicit non-claims

The retained MP4 is already verified separately (SHA-256
`ba653c490689847a31033babc48dba64f6322549fa2b98b12e615ea58658bbc9`, H.264
1920x1080/30 fps/165 frames, AAC 48 kHz stereo, strict decode). Do not render
it again or relabel that identity/decode proof as Player/export parity.

No grant, marker, App source/tree, browser capture, physical PCM result, or Gate6
pass exists until the owner supplies the missing inputs and the named suite
completes.
