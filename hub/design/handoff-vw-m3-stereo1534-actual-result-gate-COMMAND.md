# Stereo 1534 actual-result gate commands

## Central run (recorded result; not rerun by this worker)

```text
composition-e2e-viewing-tab-stereo-grantpath-chrome155-1020153403-18318
```

Result: **failed, exit 1**. The central log shows `READY_GRANTED`,
`RUN_STARTED`, one browser test, native `ffprobe` audio channel refusal at
`channels=1`, and `POSTFLIGHT_OK`.

## Read-only artifact audit run by this worker

```bash
ffprobe -v error \
  -show_entries format=filename,format_name,format_long_name,duration,size,bit_rate:stream=index,codec_type,codec_name,codec_long_name,profile,width,height,pix_fmt,r_frame_rate,avg_frame_rate,time_base,start_pts,start_time,duration,channels,channel_layout,sample_rate,nb_frames \
  -of json \
  /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-stereo-owned-state-guard-fix/stereo-1534-output/tab-audio-capture.probe.ts-8ea9e-rome155-MediaRecorder-clock-native-codec-chrome155-tab-audio/whole-tab.webm
```

Result: WebM; VP8 1440x900; Opus 48 kHz mono; native time base `1/1000`;
video start PTS 45 and audio start PTS 0.

```bash
ARTIFACT=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-stereo-owned-state-guard-fix/stereo-1534-output/tab-audio-capture.probe.ts-8ea9e-rome155-MediaRecorder-clock-native-codec-chrome155-tab-audio/whole-tab.webm
ffprobe -v error -select_streams v:0 \
  -show_entries packet=pts,pts_time,dts,dts_time,duration,duration_time,size \
  -of csv=p=0 "$ARTIFACT"
ffprobe -v error -select_streams a:0 \
  -show_entries packet=pts,pts_time,dts,dts_time,duration,duration_time,size \
  -of csv=p=0 "$ARTIFACT"
```

Result: 5 nonempty video packets and 66 nonempty audio packets; PTS were
monotonic. No decode was performed by this audit, matching the required
pre-decode mono refusal.

```bash
sha256sum "$ARTIFACT"
```

Result:
`07fc9b7278eb449068c4b4ddb6cb1d8da05c5741c77e09698446fc0f2abede50`.

Compact handoff bundle:

```text
handoff-vw-m3-stereo1534-actual-result-gate-artifact.tgz
sha256: ab15c111b52b1a98453bdbb09f792ef8ab30323e8765a2b81a65e9b9186f4ff2
```

No browser, render, network, install, live socket, full suite, retry, grant,
or product test was run by this worker.
