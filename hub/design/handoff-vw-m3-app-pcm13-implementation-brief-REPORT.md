# App public13 continuous PCM — concrete UNAPPLIED implementation unit

**Ready for App-owner port; not activated or integrated.** One App product leaf changes: `src/tools/video-editor/compositions/AudioTrack.tsx`, **+110/−34 (net +76), 405 → 481 lines**. Two direct test files add 24 cases. No App worktree was created, and no App source/pin/lock was written. PLAN, COMMON, current Viewing INBOX, prior 19-pass/5-RED report/tests, release13 handoff and App current-cohort report were read. No settled decision was changed.

## Artifacts and exact inputs

- [UNAPPLIED App patch](handoff-vw-m3-app-pcm13-implementation-brief-consumer.patch): one source file plus `continuousPCM.contract.test.tsx` and `continuousPCM.lifetime.test.tsx`.
- [Executed commands](handoff-vw-m3-app-pcm13-implementation-brief-commands.sh).
- Complete editable source/test/staging proposal: `/home/user/work/wt/vw-m3-app-pcm13-implementation-brief/proposals/app-continuous-pcm13/`. This is outside Composition product source and is not imported by its build.
- Exact App owner cohort: **`b1ef4b9b910ba72375c34cf319692f90d22edc25`**, tree **`8d8a10b057ed31fed69517e18a23b8ec3811447a`**, from `design/app-current013-corrected-public-browser-gate.md`. Read via `git show`, not the older local integration `41fff23` or prior consumer `0ea988` cohort.
- Actual public Composition **0.0.13**, archive `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/artifacts/banodoco-timeline-composition-0.0.13.tgz`, SHA256 **`9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`**. All **77 regular safe members** unpacked into this worker’s own real leaf. Version/export target checked before the final test run. No repack or export implementation copy.

The former `continuousPCM.contract.test.tsx`, `compiledAudioSourceClock.test.ts`, and clock helper remain byte-identical to the previous handoff. Only the contract test goes into the App patch; the other two remain offline test support, not an unused product abstraction.

## Implementation

`ClipAudio` uses only public `/evaluation` admission, compiler, trim, rate, apply and WAV APIs. `audio.render_source` participates in the existing semantic/reset identity. A matching prepared record supplies its admitted HTTP(S) attempt URL directly; the public validator rejects wrong envelope, raw fractional origin, child rate or blob URL. An export with an envelope requires that existing prepared source and never starts browser decoding. A prepared record without an envelope refuses rather than being silently ignored.

For ordinary preview envelope audio, a small effect inside **the existing PreviewAudio attempt** fetches/decode-prepares full source PCM. It calls the public sample envelope once at `computeMediaTrim(originalCompiledChild, fps).trimBefore / fps`, using the child’s sanitized rate, then writes the public full-source IEEE-float WAV. It does not slice or resample PCM itself. The native Audio retains the existing bounded trim, rate, sequence and premount. Its `volume` is the constant track×clip scalar (or zero), so neither gain nor rate is applied twice. Existing Web Audio amplification selection remains, including a compiled envelope above unity.

The same reducer owns retries and chrome Retry. Abort, stale completion suppression, AudioContext `finally` close and Blob URL revocation stay inside that attempt. Native failure after successful playback resets readiness before its replacement decode. The existing hold also covers preparation; source chunks renew its existing timer, starvation releases it without restarting the download, and late playable media can join. Native readiness, progress, teardown and premount handling are retained. No new decoder service, shared hook, source factory, protocol, store, compiler, DTO or authority field was needed. **No new cross-owner lifetime seam is requested.**

## Executed evidence

All tests below used the actual extracted public13 bytes and read-only unchanged dependency leaves from `vw-m3-app-private12-clean-install/clean-project/node_modules`. React/Remotion/native media, browser decoder/fetch and gateway identity are explicit offline host boundaries; public compile/admission/apply/WAV are real. Only eight App files were read; required function declarations were extracted verbatim with the TypeScript parser. The real error boundary and failure context were retained. There is no App repo copy or private Composition source import.

| Command/result | Evidence |
| --- | --- |
| Unchanged exact App leaf + prior direct contracts | **Exit 1: 19 passed / 5 failed**, 1.97s. Same desired prepared positive and four forged/mismatch REDs, now against public13. `workers/vw-m3-app-pcm13-implementation-brief/red.log`. |
| Final proposal + preserved contracts + lifetime tests | **Exit 0: 3 files / 42 passed**, 4.57s. Prior 24 cases all GREEN; 18 additional direct lifetime/behavior cases. `workers/vw-m3-app-pcm13-implementation-brief/green-final-public13.log`. |
| Scoped TypeScript/browser/React-hooks ESLint | **Exit 0**, no diagnostics, no cache. Uses the App’s relevant rules, not a claim that all App lint ran. |
| `git apply --check .../consumer.patch` in own tiny exact-base `port-check` directory | **Exit 0**. One modified product file/two added tests; nothing applied to App. |
| `git diff --check` | **Exit 0**. |

The full-source WAV tests compare exact bytes at **44.1/48 kHz**, two channels, >unity signed input, fractional trim and child rate. A between-frame sample explicitly differs from a planted step-held gain, so the retired callback cannot satisfy that assertion. Prepared sources retain half/zero/boost scalars without decoding. Other cases cover envelope edits, stale decode/source changes, failed decoder close, fetch backoff/exhaustion/chrome Retry, retry after a playable element fails, stalled preparation, source-chunk progress, premount readiness, ordinary native progress/retry/teardown, occurrence-end shortening and prepared export.

Development stops are retained honestly: initial Node child-process tar staging hit sandbox EPERM (replaced by safe Python archive/Git reads); initial AST staging parsed `.ts` as TSX (corrected); the first new bound-window fixture used a decimal half-frame and expected 8 instead of native floating-point result 7 (changed the new fixture to an exact 125-ms bound without touching production clock math); an attempted alias-free run had zero collected tests because this Composition repo’s package self-reference points to its own unbuilt dist. Final staging resolves the **advertised public13 export through its own export map**, then aliases exactly that public entry to avoid self-reference. No private chunk or admission/DSP copy. The preceding 41-pass result was superseded by the final 42-pass source-progress case. No old passing behavior test was rewritten, skipped or weakened.

## Reproduction and App-owner port

From `/home/user/work/wt/vw-m3-app-pcm13-implementation-brief`:

```sh
O=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch
W="$O/workers/vw-m3-app-pcm13-implementation-brief"
P=proposals/app-continuous-pcm13
N="$W/fixture/node_modules"
python "$P/stage.py"
PCM_BASELINE=1 node "$P/stage.mjs"
node "$N/vitest/vitest.mjs" run --no-cache --configLoader=runner --maxWorkers=1 --config "$W/fixture/vitest.config.mjs" continuousPCM.contract.test.tsx compiledAudioSourceClock.test.ts
# required RED: exit 1, 19 pass / 5 fail
node "$P/stage.mjs"
node "$N/vitest/vitest.mjs" run --no-cache --configLoader=runner --maxWorkers=1 --config "$W/fixture/vitest.config.mjs"
# GREEN: exit 0, 42 pass
node "$N/eslint/bin/eslint.js" --no-cache --no-config-lookup --config "$P/eslint.config.mjs" "$P/AudioTrack.tsx" "$P/"*.test.tsx "$P/"compiledAudioSourceClock*.ts
```

The 13:25 direction remains: **App owner first adopts immutable Composition 0.0.13 with normal pin + lock byte identity; only then port/activate this consumer; Agent follows App.** Runtime/client **0.2.13** in the current cohort is a separate version and is not Composition public13. The patch deliberately contains no pin/lock delta. On a newer App head, port only this leaf diff and two tests, preserving intervening owner edits.

The next App worker must run these 24 direct tests on its actual public13 installation, the existing `AudioTrack.test.tsx`, `RemotionPreview.audioFailure.test.tsx`, `TimelineComposition.media-conformance.test.tsx`, and normal owner checks using a private cache/config. Existing frame-callback assertions describe the deliberately retired gain policy: preserve their audible fade/mute/amplify positives as continuous-PCM equivalents, do not replace them with refusal expectations or disable the suite. This worker has not performed that App-suite migration and does not claim the current App suites green. Project typecheck and the known public12/public13 strict NodeNext declaration issue remain with the owner; this proposal does not change declarations.

## Limits and blocked work

The requested bounded proposal is complete; **no task blocker**. Activation is pending App-owner pin/lock adoption and port qualification. No full suite, central request, project build/typecheck, browser, rendering, socket, network or install ran. No shared dependency/cache/runtime/venv or parent directory was written; scope directories are real and only unchanged dependency leaves link out. The temporary proposal node_modules link and own cache are removed at completion; rerun staging recreates the owned overlay.

Actual AudioContext codec support/device resampling, HTTP/gateway authorization, Blob playback/amplification behavior, advanced-start occurrence/seek/window synchronization, full-source memory/startup cost, currentRoot delivery and physical Player/export PCM parity remain **unverified**. Mocks prove control flow and exact public PCM processing, not audible output. The previous App browser cohort’s Chromium-launch failure is neither repaired nor recounted as this unit’s failure. No deletion or Gate 6/consumer-release qualification is claimed.
