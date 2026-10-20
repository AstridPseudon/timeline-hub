# APPROVE — inactive PCM helper unit only

Reviewed `tl/vw-m3-pcm-current-landing-batch` / `ab935f77378ba5ea1df55ba775654f8bba233ebc`, against ancestor `0a8c7577` and destination Agent `ed60bf15` (corrected Composition consumer `5f6c8130`). No blocking defect for the bounded inactive port. Normal-route activation, original-source transport and HTTP/Player/export qualification remain open. This approval does not close M3.

Read PLAN, `handoff-vw-m3-pcm-final-landing-review-REPORT.md`, `handoff-vw-m3-pcm-current-landing-batch-REPORT.md`, its complete patch, `agent-pcm-source-carry.md`, and `agent-pcm-compile-idempotence.md`. The complete patch matches the branch delta; its only byte differences from local `git diff` are abbreviated index hashes. Inspected actual product, tests, current render call sites, materializer lifecycle and released public consumer.

## Scope and behaviour

- Exactly **10 files**, **319 product lines**: Python adapter 135; JS kernel 114; public clock adapter 13; normal adapter 57. Remaining changes are tests. No changes to compiler, service, protocol, renderer entrypoint, pins, manifests, ledger, or integration.
- All envelope compilation, PCM gain application, WAV encoding, media trim and playback-rate policy use public `@banodoco/timeline-composition/evaluation` exports. Local recursive envelope time translation preserves keyframe/curve/multiply/minimum structure; it introduces no second gain evaluator or DSP implementation. Native FFmpeg decode retains sample rate, channel count and whole-source samples. No resampling, alignment, padding or normalization was added. Clip/track scalar gain stays downstream, with public mute/amplification behaviour.
- Public12 AudioTrack already knows how to consume prepared PCM and validates its envelope/clock; Player prepares PCM with the same public `applyAudioEnvelope`. Its scalar gain runs once. The Agent normal render entrypoint has **no call** to the new producer, and no new activation flag exists. There is public consumer capability, but no active Agent prepared-source producer/consumer join.
- Root asset registry must exactly equal the materializer's resolved registry. Selected managed bytes are SHA256-checked before decode. Incoming `audio.render_source` is refused; malformed envelopes/unsupported curves fail through public compilation; bad source clocks, non-finite PCM, unexpected subprocess response fields and escaping WAV paths refuse. Failed batches/registration remove their own scratch and preserve unrelated files and authored data. Tests cover corrupted/staged/swapped bytes and forged/double preparation.
- `original_clips` is an internal Python argument; it is never populated from caller JSON. The `window=` helper path retains deep copies before invoking the existing host slicer. The JS seam checks matching asset, track and sanitized rate. Neither helper reconstructs originals from `app.astrid_slice_origin`, shot metadata, or ID suffix parsing. The forged-stamp controls pass. Four former import-only strict xfails now compare actual full stereo PCM at the original **1e-7** tolerance for both assets and both slice modes. The two active-join compiler-vector strict xfails remain unchanged.

## Concrete holds before activation

These are incomplete integration obligations, acceptable only while the unit remains inactive:

1. **Source pair validation is external.** The helper does not prove that a supplied original is the actual original of a transformed clip: matching asset/track/rate alone cannot establish `at/from/to/params` closure. It lacks the window-fps comparison and re-derivation check. The source owner must validate the actual serialized, compiled pair before calling. No caller JSON field may become an authority toggle.
2. **Malformed trusted-map diagnostics are incomplete.** Missing original keys currently raise `KeyError`; absent managed digests can raise `AttributeError`; duplicate IDs overwrite entries in the helper's retention dictionary. Missing keys/digests fail closed, but duplicate-map retention requires validation of the actual compiled input. I independently confirmed normal timeline compilation refuses duplicate IDs (`clips[1].id 'sound' is not unique`). Activation must preserve that validation and add explicit map/digest/fps checks from the source-carry design, with clean refusal tests.
3. **Successful WAV lifetime belongs to the caller.** Containment is checked under `materializer.serving_root`, but successful output lives until its attempt owner removes it. Reused materializations can have a shared serving root. The separate caller join must register attempt cleanup in the existing ExitStack, and keep materializer/server/attempt alive through consumption. These local URL tests prove containment and explicit caller cleanup only; HTTP GET, server close, 404 and thread cleanup remain unverified.
4. **Compile and slice do not commute.** I reproduced the actual fixture: compiled original `at=0.123`; current `compile(slice(raw))` gives `from=0.5016`; `compile(slice(compile(raw)))` gives `from=0.502`, consistent with the full unwindowed source clock. The difference is **0.4 ms**, correcting the earlier documents' “1.6 ms” arithmetic. The corpus report independently found 6,432/9,023 synthetic mismatches, up to 1 ms at speed 2, and 14 membership differences; compile idempotence alone does not solve this. The source-carry document's §6 expectation of 0.5016 for the compiled slice is stale. Its re-derivation check must account for renderer recompilation of sliced `at`. Compiler-domain repair stays in the separately granted source-carry task; no compiler/slicer change belongs in this port.

Original fade phase is therefore **not solved by the app stamp**. The helper positives qualify retained unsliced compiled input, including the internal map seam. They do not qualify the existing already-sliced service route. Preserve its sample-exact requirements and the continuous public gain decision; no tolerance relaxation, behaviour refusal rewrite or route activation is warranted here.

## Independent tests

All direct tests used this exact branch's Python code and byte-identical copies of its seven JS helper/test files in a private worker overlay. The overlay's Composition package was extracted from the exact archive in `ed60bf15`: SHA256 `0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`; all **77** package members equal the shared 0.0.12 package. Peer links are read-only, Node 20.19.4 / Remotion 4.0.509 / React 18.3.1. No install or shared dependency mutation.

Exact commands (cwd = assigned worktree; variables below expand to absolute paths):

```sh
O=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch
W=$O/workers/agt-review-pcm-unit-current
P=$W/checks/remotion
N=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node

env -u NODE_OPTIONS -u NODE_PATH PATH=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin:$PATH \
  PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD ASTRID_REMOTION_PROJECT_DIR=$P \
  /home/user/work/venv-agent/bin/python -B -m pytest -p no:cacheprovider -q \
  tests/packs/rendering/test_normal_audio_sources.py \
  tests/packs/rendering/test_normal_audio_source_phase.py \
  tests/editing_conformance/test_compile_contracts.py tests/core/rendering/test_service.py
# 103 passed, 2 existing xfailed in 85.32s; exit 0; no deselections.

env -u NODE_OPTIONS -u NODE_PATH PATH=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin:$PATH \
  $N --expose-gc $P/tests/normal-audio-native-sources.test.mjs
# 5 passed; exit 0.
env -u NODE_OPTIONS -u NODE_PATH PATH=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin:$PATH \
  $N $P/tests/normal-audio-sources.test.mjs
# 8 passed; exit 0.
env -u NODE_OPTIONS -u NODE_PATH PATH=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin:$PATH \
  $N $P/tests/gapless-mp3-source-origin.test.mjs
# 4 passed; exit 0.
env -u NODE_OPTIONS -u NODE_PATH PATH=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin:$PATH \
  TIMELINE_HEAVY=1 $N --expose-gc $P/tests/long-audio-source.test.mjs
# 2 passed; exit 0.

/home/user/work/venv-agent/bin/ruff check \
  astrid/packs/rendering/rendering/renderers/remotion/normal_audio.py \
  tests/packs/rendering/test_normal_audio_sources.py tests/packs/rendering/test_normal_audio_source_phase.py
# All checks passed; exit 0.
git diff --check 0a8c7577 ab935f77
# exit 0.

$O/bin/request-test agt-review-pcm-unit-current remotion-0012-nodes --files \
  'tests/packs/rendering/test_normal_audio_sources.py tests/packs/rendering/test_normal_audio_source_phase.py tests/editing_conformance/test_compile_contracts.py tests/core/rendering/test_service.py'
$O/bin/wait-test agt-review-pcm-unit-current-remotion-0012-nodes-1020093822-21417 1
# 19 failed, 84 passed, 2 xfailed; exit 1. Every failure is FileNotFoundError
# for shared-runtime normal-audio-sources.mjs, which is not installed there.
```

Central run source tree: `16c18d6db01fa330d497ff9147786e65e01e54c8`. This is a genuine named-lane environment failure, not a green claim or PCM mismatch. The successful private-overlay run executes all the same 105 nodes. The shared runtime was left untouched. Recommend a dedicated named helper lane that selects a private overlay containing the exact snapshot's helpers and public12 package. No integration-marker deselection occurred in these files. `composition12-owner-integration` was unnecessary for this unit: no presenter/default-theme/archive changes are included, and running its obsolete package assertions from this pre-consumer branch would mix cohorts. That corrected cohort belongs to `5f6c8130`.

Raw logs and archive qualification are under `$W/{helper-pytest,native-node,normal-node,gapless-node,long-node}.log` and `$W/overlay-qualification.json`. No full suite, sockets, browser, Remotion normal export, served HTTP or Player/export parity was run. The existing generic-service targeted tests include FFmpeg renders; those are not evidence of an activated normal Remotion route.

## Exact safe port and conflict

Port only these ten paths from `ab935f77`:

```text
astrid/packs/rendering/rendering/renderers/remotion/normal_audio.py
remotion/attempt-envelope-pcm.mjs
remotion/compiled-audio-source-clock.mjs
remotion/normal-audio-sources.mjs
remotion/tests/gapless-mp3-source-origin.test.mjs
remotion/tests/long-audio-source.test.mjs
remotion/tests/normal-audio-native-sources.test.mjs
remotion/tests/normal-audio-sources.test.mjs
tests/packs/rendering/test_normal_audio_source_phase.py
tests/packs/rendering/test_normal_audio_sources.py
```

Nine paths are new in `ed60bf15`. The only overlapping path is `test_normal_audio_source_phase.py`: integration corrected the old docstring reference from `design/` to `docs/design/`, while this unit replaces that paragraph and the four import-only xfails. A private baseline export of affected paths from `ed60bf15` confirmed raw complete-patch `git apply --check` fails at its first hunk. Updating only that removed-context reference makes the complete patch check pass. Resolve by keeping the unit's new scoped docstring and substantive PCM positives; preserve current documentation locations if any reference survives. No pin, compiler, source-carry, renderer entrypoint or ledger should be restored from this old branch. Integration advanced to `efb96034` during review; its intervening changes touch none of these ten paths.

Only this shared report and the requested worker completion files were written as deliverables. Repository status remains clean. No product/test edit, git commit/merge/rebase/checkout/push, shared dependency change or decision deviation. Next: port this inactive unit, qualify the private helper lane, then land and review the separately granted compile-domain/source-carry join before requesting served-source and normal-route parity qualification.
