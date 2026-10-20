# App PCM public clock — absent-consumer fallback complete

No active App prepared-PCM consumer exists in either assigned App `1be0efdde` or the selected public10 cohort `9d9101fef15470c813d060ed0169676fa7206c2e`. **No product bug fix or active playback qualification is claimed.** Product worktree is unchanged. Delivered only the task-authorized **UNAPPLIED** tiny clock adapter and direct tests, in flat ORCH design files.

- Proposal: [handoff-vw-m3-app-pcm-public-clock-proposal.patch](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-app-pcm-public-clock-proposal.patch) — adds `compositions/compiledAudioSourceClock.ts` (12 lines) and its direct test (97 lines); imports only the existing public evaluation API. No new hook, source factory, lifecycle, DTO or activation.
- Adapter: [handoff-vw-m3-app-pcm-public-clock-adapter.ts](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-app-pcm-public-clock-adapter.ts).
- Tests: [handoff-vw-m3-app-pcm-public-clock.test.ts](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-app-pcm-public-clock.test.ts).
- Coordination: [handoff-vw-m3-app-pcm-public-clock-coordination.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-app-pcm-public-clock-coordination.md), explicitly aligned with pending App12 pin-prep.

Existing seam: current `src/tools/video-editor/compositions/AudioTrack.tsx:295-326` still derives frame-volume with local `getAudioFade` / `getAudioVolumeProp`. Selected public10 `AudioTrack.tsx:348-399` compiles the public envelope (`:355`) and passes a per-frame callback (`:360-364`) into render/PreviewAudio (`:398`). `git grep` for apply/WAV/useAudioEnvelope/source_from in that cohort's compositions finds only the existing media-conformance test's prepared-source fixture, not a producer. The package's own private preparation hook already uses public trim/rate, but it is not this App consumer and must not replace App's retry lifecycle wholesale.

The proposed adapter consumes an **already compiled** clip and resolved fps. `source_from = computeMediaTrim(clip, fps).trimBefore / fps`; `playback_rate = getSanitizedPlaybackRate(clip.speed)`. The only extra guard rejects invalid resolved fps. It never reads occurrence offset/speed/gain and never repairs projection behavior. `.05` produces frame 2 at 30 fps and frame 1 at 30000/1001 fps. The selected child rates 2 and .5 remain unchanged. This is a source-clock proposal, not an implementation of PCM preparation or trust admission.

## Targeted offline evidence

Exact immutable public12 artifact: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-app12-pin-prep-artifact.tgz`, version 0.0.12, 58,444 bytes, 77 files, SHA256 `0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`. Extracted privately under this worker's ORCH directory. Config resolves the advertised `/evaluation` export from these built artifact bytes. All77 extracted-file hashes, advertised export, shared installed Composition files and App root package/lock hashes were verified unchanged after tests. Shared peers are read-only; no install or shared package mutation.

Exact final test command (same command for red and green, stdout redirected respectively to the flat design `-red.log` / `-green.log`):

```sh
/home/user/work/app/node_modules/.bin/vitest run --config /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-app-pcm-public-clock/vitest.config.mjs --reporter=verbose
```

- **Raw-from control:** exit 1, **9 failed / 9 passed**. Control is the proposed adapter with only its source origin replaced by `clip.from ?? 0` (saved as `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-app-pcm-public-clock-raw-from-control.ts`). This is an intentionally wrong candidate control, **not a claim of an existing App PCM consumer failing**.
- **Correct public trim/rate adapter:** exit 0, **18 passed**, 387ms. Exact same final tests (SHA256 `50d11e41a111cd06cf9671a2d2b1349cc2616a876393fb6ae12c91b9eca5df37`). No xfail/skip/tolerance change.
- Four real public compile/apply/WAV cases use .05 trim, 30/rational fps, 2x/.5x child rate, stereo 44.1/48kHz, all original source samples. Every interleaved float WAV sample is compared byte-exactly against public source-time envelope gain with the independently pinned frame-rounded origin. WAV format/rate/channel/count assertions pass. Positive and negative samples beyond unity survive. The test calls public compile/apply/WAV once each; scalar gain stays outside.
- Literal already-compiled `volume=.4` with occurrence metadata `source_offset=350`, `speed=1.5`, `gain=.5` is preserved byte-for-byte. Separate volume 0/.5/3 and changed occurrence metadata do not affect clock or compiled envelope. This proves adapter neutrality, **not canonical projection correctness or compiler-gain provenance**.
- Defaults/invalid child rates delegate to the public sanitizer; invalid resolved-fps cases reject.

```sh
/home/user/work/app/node_modules/.bin/tsc -p /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-app-pcm-public-clock/tsconfig.json
```

Exit 0: strict, no-emit targeted adapter/test typecheck against exact public12 declarations. No App-wide typecheck claim.

```sh
git apply --check /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-app-pcm-public-clock-proposal.patch
git diff --check
git status --short
```

All exit 0; final status empty. The patch also passes `git apply --check` from an isolated archive of the selected public10 cohort's compositions directory. Temporary archive extraction and Vite cache were removed. No build output/temp files in product worktree.

Development checks: the first raw-control run was interrupted (130) while Vitest formatted large typed-array diffs; the final comparison uses byte-exact Buffer equality with compact diagnostics. A first corrected-clock run had 17 pass / 1 fail because a .15-second unity witness fell inside the rational-fps 2x fade-out. Moved that witness to .115 seconds, inside the true unity plateau, and reran both final controls. The all-source byte-exact WAV assertion was unchanged; no tolerance widened. Initial corrected run is retained in `-green-initial.log`.

## Limits and next step

Absence of an actual preparation consumer triggers the explicit fallback, so there is no small App product PR to merge now. This is not a new broad inventory and does not close the active audio join. The owner can apply the two-file proposal alongside the eventual owned preparation consumer after the pending public12 pair. That consumer must use the same compiled clip/envelope phase and constant base gain; preserve full native rate/channel/source duration; preserve existing PreviewAudio readiness, bounded retries/no-data hold, volume .5/mute/amplify, abort/cancellation and Blob URL revocation; and consume trusted prepared metadata through the package's exact admission. The adapter contains none of that lifecycle and proves none of it.

No App data/shotProjection/core/provider/root package/pin edits; no projection RED compensation; no normalization/resampling/clip alignment/scalar-gain bake; no authoring bytes changed. No browser, render, socket, network, full suite, install, physical Player/export PCM parity or actual trusted source join was run/claimed. No git commit/checkout/merge/rebase/push or other worktree writes.
