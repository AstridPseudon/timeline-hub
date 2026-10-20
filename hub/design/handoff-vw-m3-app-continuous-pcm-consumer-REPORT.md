# App continuous PCM consumer — BLOCKED on public source admission

App base **0ea988bdd2907c876b82fd2620820e3fb6d6ea84** (`public12root0ea`). **No product changes or actual consumer implementation.** The brief explicitly requires stopping if a required public source contract is missing; this is that case. `BLOCKED` and the harness commit message are written; no `DONE` is claimed.

## Concrete blocker and bounded proposal

Public Composition **0.0.12** exports `compileAudioEnvelope`, `computeMediaTrim`, `getSanitizedPlaybackRate`, `applyAudioEnvelope`, and `audioEnvelopeWav` from `/evaluation`. It does **not** export `encodedEnvelopeSource`, `envelopeKey`, or `useAudioEnvelopeSource` from either `/evaluation` or the root. The package export map forbids private `dist/lib/...` imports (`ERR_PACKAGE_PATH_NOT_EXPORTED`). The exact Node namespace/deep-import probe and output are adjacent `-public-source-seam.mjs` / `.log` artifacts.

The existing implementation of exact admission is bundled inside `dist/chunk-DMRW7SC3.js` (function at line 546), used internally by `dist/index.js`'s private preparation hook. Its declaration in `dist/lib/audio-envelope.d.ts` is **not an advertised import**. The earlier `app-preview-audio-seam.md` handoff's claim of a public admission API therefore does not hold for these exact public12 bytes. This is prerequisite evidence, not a proposed change to the settled continuous policy.

An App implementation must accept the existing matching prepared positive AND reject mismatched envelope identity, frame-rounded source origin, child rate and URL through the existing contract. App currently ignores `audio.render_source`. Copying the private validator would duplicate policy; refusing every prepared record would lose the valid positive; importing private bundle chunks would bypass the public boundary; substituting the public TimelineComposition audio implementation would replace App's readiness/retry owner. None meets this brief.

**Recommended minimal prerequisite, owned by Composition:** export the existing pure `encodedEnvelopeSource` plus its `EncodedEnvelopeSource` type through the existing `/evaluation` entry. No new validator, decoder architecture, store, hook lifecycle, source certificate, or DTO. An approved artifact/pin exception is required because this worker is expressly prohibited from a package bump. Do not expose/adopt the hook wholesale: keep App's existing `PreviewAudio` attempt lifetime. After that prerequisite, App's owner can review one consumer PR using the supplied public trim/rate clock adapter, real public apply/WAV, and the existing browser fetch/Web Audio pattern inside that attempt lifetime.

App's only local decode helpers (`audioAnalysisClient.ts` and `useWaveformData.ts`) are private fixed-rate analysis caches, not exported reusable full-source preparation lifetimes. The package has a private fetch/AudioContext/close/abort pattern. No new decoder architecture was introduced; the **public source-admission gap alone** is sufficient to block the required complete contract.

## Evidence

- Existing `AudioTrack.test.tsx`, `RemotionPreview.audioFailure.test.tsx`, and `TimelineComposition.media-conformance.test.tsx`: **91 passed, exit 0**, 5.87s. The last suite includes the public prepared-source positive and explicitly historical App callback behavior. This is existing behavior coverage, not continuous PCM qualification.
- New offline red harnesses: **19 passed / 5 failed, exit 1**, 2.77s. Eighteen passes replay the previous public clock adapter tests against the clean public12 graph; one pass uses real public compile/apply/WAV and exact full-source float bytes. The five failures are the matching prepared positive (App uses original URL instead) plus four forged variants (wrong envelope, raw `.05` instead of `2/30`, wrong rate, and blob URL). The red expectations remain desired behavior and are not inverted or xfailed.
- Namespace/deep-import probe: **exit 0**, confirms public source admission missing. No private function imported or executed by the new harness.
- Fresh graph comparison against its provisioning manifest: **35,545 node_modules entries checked; zero additions, missing entries, changed file contents or symlink targets**. `-graph-check.json`. No installs or shared dependency/cache writes.
- `git apply --check` on the **unapplied test-only** red proposal: exit 0. `git diff --check`: exit 0. Final `git status --short`: empty.

The new tests are outside product source and supplied as flat copies and an **UNAPPLIED `-red-proposal.patch`**. `-exact.patch` is empty because the actual product diff is empty. Original clock adapter/report/raw-from-negative controls and the historical frame-table RED records are untouched. No tolerance change.

## Exact commands

Cwd for all commands: `/home/user/work/wt/vw-m3-app-continuous-pcm-consumer`. During test runs, only this worktree's pre-existing `node_modules` symlink was temporarily pointed to the clean private graph below, then restored to its original target. The config uses the repo's actual admission plugin and source shims, aliases React/Remotion/Composition to that private graph, and places cacheDir in this worker directory. `--no-cache --configLoader=runner` avoids shared Vite caches. Node was v22.22.0; clean graph Vitest was v4.1.5.

```sh
W=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-app-continuous-pcm-consumer
N=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-app-private12-clean-install/clean-project/node_modules
D=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design
node "$N/vitest/vitest.mjs" run --no-cache --configLoader=runner --config "$W/vitest.config.mjs" src/tools/video-editor/compositions/AudioTrack.test.tsx src/tools/video-editor/components/PreviewPanel/RemotionPreview.audioFailure.test.tsx src/tools/video-editor/compositions/TimelineComposition.media-conformance.test.tsx > "$D/handoff-vw-m3-app-continuous-pcm-consumer-baseline.log" 2>&1
# exit 0: 91 passed
node "$N/vitest/vitest.mjs" run --no-cache --configLoader=runner --config "$W/vitest.config.mjs" "$W/continuousPCM.contract.test.tsx" "$W/compiledAudioSourceClock.test.ts" > "$D/handoff-vw-m3-app-continuous-pcm-consumer-red.log" 2>&1
# exit 1: 19 passed / 5 failed, concrete required consumer cases
node "$W/public-source-seam.mjs" > "$D/handoff-vw-m3-app-continuous-pcm-consumer-public-source-seam.log"
# exit 0: missing-public-contract probe

git apply --check "$D/handoff-vw-m3-app-continuous-pcm-consumer-red-proposal.patch"
git diff --check
git status --short
# all exit 0; status empty
```

Three earlier private test-config attempts failed before mounted assertions: missing explicit package/source aliases, missing admission plugin, and runner-loader incompatibility with the base config's `__dirname`. Their six `-setup-failed*.log` files are retained. Final config uses existing source/plugin imports with explicit paths; no test or product code was weakened to resolve setup.

## Limits and next step

No actual browser, render, listener, network, install, full suite or central request. No `.git` mutation, other-worktree edit, package/root change, authoring mutation, renderConfig/TimelineData field or Runtime DTO. No actual decode/cancellation/retry/Blob cleanup consumer was implemented or qualified; those remain required after the public admission prerequisite. Mute/half/boost exactly-once PCM consumption, occurrence/window preparation lifecycle, currentRoot activation, and physical Player/export parity are **unverified**. App owner review/merge and later real parity qualification remain necessary.
