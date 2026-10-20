# Findings

- PASS is valid for the named standalone Chrome155 `getDisplayMedia({video:true,audio:true,preferCurrentTab:true})` capture capability only.
- The probe uses a real Playwright locator click, awaits ordered MediaRecorder chunks through `stop`, writes `whole-tab.webm`, runs ffprobe, decodes audio/video with ffmpeg, and asserts one live video track, one live tab-audio track, native monotonic PTS, and both declared decoded tones.
- The synthetic WAV is only the HTML-audio fixture source. The 1320 Hz and 880 Hz measurements above are from decoded Opus in the retained WebM; there is no synthetic replacement in the result.
- Native PTS are preserved and audited. The visual marker is explicitly diagnostic-only; no phase, offset, origin, alignment, normalization, resampling, or parity claim is made.
- Grant/preflight identity matches the result: App source `2b388e769d9e153122e43b16b5d21e6e1ddf5b71`, source tree `0124b608…`, Composition 0.0.12/77 files, private graph `4a54ed6f…`/32,382 entries, Node `v20.19.4` with the recorded executable SHA, and Chrome `155.0.8059.84` with the recorded executable/tree SHAs.
- The central scheduler was the Composition namespace only, with snapshot tree `23a994070b8e25aba18703af1c6a0c840df1ab62`; the command invoked the frozen App source by absolute path and its 5,835-file guard. No App, Runtime, Player, export-frame, or product source was changed.
- Short-temp static evidence is valid: old socket path 175 bytes, fresh `/tmp/timeline-tab-audio-*` path 85 bytes; UID/GID matched, mode was 0700, pre-existing directories were protected, and failure cleanup removed only the process-owned allocation. The run's current marker was created/consumed with the exact source and `POSTFLIGHT_OK`; no run-owned temp remains. An older empty discovery temp directory dated 13:21 remains and was not deleted as unrelated/pre-existing state.
- The retained central output contains the WebM and `.last-run.json`, but not the probe's attached JSON/raw RGB files. The small metrics JSON in this handoff is therefore an offline recomputation from the WebM, not a claim that those attachments were transported.

## Boundary

Do not promote this result to Player/export-frame/audio parity, Composition evaluator parity, or end-to-end App viewing evidence. Do not claim unsupported browser/backend behavior or a fallback path. The historical 1248 run remains failed. The source can be released after this artifact and metrics handoff is accepted.
