# Commands and results

All commands were read-only/offline unless noted. No browser, listener, render, network, install, permission, grant, or full-suite command was run by this auditor.

1. Central result inspection:

   `sed -n '1,260p' /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/composition-e2e-viewing-tab-short-owned-temp-capability-chrome155-1020133821-14480/summary`

   Result: PASS, exit 0, 44s; 1 passed, body 5.2s, total 7.4s. Log contained `READY_GRANTED`, `RUN_STARTED`, and `POSTFLIGHT_OK`, all source `2b388e769d9e153122e43b16b5d21e6e1ddf5b71`.

2. Artifact inventory and digest:

   `find /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-tab-short-owned-tmp-fix/capability-1340-output -type f -printf '%s %p\\n'`

   `sha256sum /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-tab-short-owned-tmp-fix/capability-1340-output/tab-audio-capture.probe.ts-8ea9e-rome155-MediaRecorder-clock-native-codec-chrome155-tab-audio/whole-tab.webm`

   Result: retained WebM is 80,477 bytes, SHA-256 `f35483bab8f4992489ccd617ca4c2375599dc9337f1fbc7b37c2e3d0820eb6c8`.

3. Offline container/PTS check:

   `ffprobe -v error -show_streams -show_packets -of json <whole-tab.webm>`

   Result: exactly one VP8 video stream (index 1, 5 packets, native time base `1/1000`, PTS 42..3487, monotonic) and one Opus audio stream (index 0, 66 packets, native time base `1/1000`, PTS 0..3900, monotonic).

4. Offline decode:

   `ffmpeg -v error -i <whole-tab.webm> -map 0:0 -f f32le <auditor-scratch>/audio.f32`

   `ffmpeg -v error -i <whole-tab.webm> -map 0:1 -vf 'crop=500:110:940:790,format=rgb24' -f rawvideo <auditor-scratch>/marker.rgb24`

   Result: decoded audio is 48 kHz mono, 190,080 samples. DFT measurements are 880 Hz amplitude `0.04818113852883244` and 1320 Hz amplitude `0.041814309247712324`. Visual decode is 62 frames; exact pre-event RGB count 0 and event RGB count 42, retained as diagnostic only.

5. Frozen source identity:

   `git -C /home/user/work/wt/vw-m3-tab-short-owned-tmp-fix status --short --untracked-files=all`

   `git -C /home/user/work/wt/vw-m3-tab-short-owned-tmp-fix show -s --format='%H%n%T%n%s' 2b388e769d9e153122e43b16b5d21e6e1ddf5b71`

   `git ls-files -z | node --input-type=module -e '<hash tracked paths and bytes>'`

   Result: clean source; commit `2b388e…`, tree `0124b608…`, 5,835 tracked files, full tracked hash `bd586630…`.

6. Frozen graph identity:

   `node --input-type=module -e 'import {hashTree} from <controller>; console.log(hashTree(<private graph>)); console.log(hashTree(<Composition package>))'`

   Result: private graph `4a54ed6f…`, 32,382 files/symlinks; `@banodoco/timeline-composition` `71b44e67…`, 77 files. Both match grant and preflight JSON.

7. Historical negative control:

   `sed -n '1,220p' /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/vw-m3-tab-clean-install-source-compose-e2e-viewing-tab-clean-install-capability-chrome155-1020124802-7076/summary`

   Result: remains failed exit 1 before recording with Chrome singleton socket path too long; postflight was OK. It is not relabeled as unsupported or fallback evidence.
