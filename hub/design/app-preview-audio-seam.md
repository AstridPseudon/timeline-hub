# App preview PCM envelope seam

Status: source audit only. M3 integration remains held. This document follows
the settled 2026-10-20 decision: one continuous gain policy, with gain
evaluated at PCM source time, is shared by App preview and normal Agent export.
The old frame-step policy is retired deliberately; readiness, retry, mute,
amplify, and constant base gain remain App preview behavior.

Coordination status: the latest App STATUS records App M1 complete but the
global M1 record absent, with M2/M3 merges held. No standalone Viewing STATUS
file was present; the latest Viewing coordination report still records no
actual Player-vs-export PCM parity and acknowledges the App adapter/Agent
compiler split. Those status findings are why this handoff remains design-only.

## Findings

The audible main-preview path is:

```text
RemotionPreview
  -> @remotion/player <Player numberOfSharedAudioTags={0}>
  -> PreviewComposition
  -> TimelineRenderer
  -> AudioTrack (one Sequence per audio clip, premounted for 2 seconds)
  -> PreviewAudio
  -> Remotion Html5Audio
```

`RemotionPreview.tsx:91-96` mounts `TimelineRenderer` inside the Player
composition. `RemotionPreview.tsx:248-270` supplies the deferred, output-only
config and its compiled transitions; `:543-562` mounts the real Player with
zero shared audio tags and a one-second Player buffer delay. The preview
component's deferred-config and seek mailbox are not audio policy and should
not change for this seam.

`TimelineRenderer.tsx:1623-1629` derives audio tracks/clips and
`:1780-1787` mounts `AudioTrack`. `AudioTrack.tsx:293-307` currently computes
the track/clip base gain, trim, and playback rate. `:311-327` gives each clip
its own premounted Sequence and preserves the media-error boundary.

`AudioTrack.tsx:336-400` is the overlap seam. `ClipAudio` compiles the public
envelope once, then currently creates the old frame-time callback at
`:359-363`:

```ts
baseVolume * audioEnvelopeAt(envelope, (frame + frameOffset) / fps)
```

The callback is consumed by both `@remotion/media` in the render branch and
`PreviewAudio` in the browser branch. The browser branch keeps the lifecycle
at `:148-261`:

* a premounted `<audio preload="auto">` is held until it has future data;
* `buffer.delayPlayback()` holds the Player while an active element is not
  playable;
* progress resets the ten-second no-data hold limit rather than restarting a
  request;
* real errors remount a fresh element after 500/1000/2000 ms backoff;
* a retry gives up honestly and reports the clip through
  `PreviewAudioFailureProvider`;
* `useWebAudioApi` remains enabled for amplified playback, including the
  conservative authored-envelope-boost case; mute is represented by a zero
  base gain.

This is the behavior the PCM adapter must wrap. `RemotionPreview` should not
be changed to own audio preparation, and no second Player/audio scheduler is
needed.

## Public Composition 0.0.10 surface inspected

The reviewed artifact is
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/artifacts/banodoco-timeline-composition-0.0.10.tgz`,
SHA-256
`cd83b77f72ce436e25eef697b289d33adae2087d92035aa37a27a308975ddea7`.
It was inspected with `tar`; it was not installed or modified. App's current
installed package is still 0.0.8, and the tracked local vendor source is the
older 0.0.2 package.

The public declaration in `package/dist/evaluation.d.ts` exports:

```ts
compileAudioEnvelope(clip, fps): AudioEnvelope | undefined
audioEnvelopeAt(envelope, seconds): number
applyAudioEnvelope(
  channels: readonly Float32Array[],
  sampleRate: number,
  envelope: AudioEnvelope,
  sourceFrom?: number,
  playbackRate?: number,
): void
audioEnvelopeWav(channels, sampleRate): ArrayBuffer
encodedEnvelopeSource(prepared, envelope, sourceFrom, playbackRate): string
```

The inspected implementation validates the envelope and sample clock, checks
equal channel lengths, then multiplies every PCM sample by

```text
audioEnvelopeAt(envelope, (sample / sampleRate - sourceFrom) / playbackRate)
```

It does not quantize to video frames. `audioEnvelopeWav` writes the resulting
channels as an IEEE-float WAV. The public `useAudioEnvelopeSource` helper also
exists in the artifact, but it is not the App adapter: it owns a separate
decode/Player-buffer lifecycle and uses `Audio` with `pauseWhenBuffering`.
Using it wholesale would discard App's bounded retry, no-data hold, and fresh
element retry behavior.

The trusted prepared-source check is exact, not a hint. Public10's
`encodedEnvelopeSource` accepts only a prepared record with an HTTPS file,
matching canonical envelope identity, exact `source_from`, and exact
`playback_rate`; otherwise it throws `AudioEnvelopeError`. App must consume
that seam, never trust an arbitrary prepared URL, envelope key, or metadata
label. The `render_source` record is an additive compiled/runtime field; it is
not an authoring field and must not be created by App.

## Candidate App adapter handoff

The smallest App implementation is inside the existing explicit overlap seam:

1. Keep `AudioTrackComponent`'s base-gain calculation and `ClipAudio`'s
   authored-envelope compilation on the shared public Composition compiler.
   App may call the public `compileAudioEnvelope`; it must not duplicate fade,
   duck, curve, or envelope selection rules.
2. Replace only the browser-side callback path in `ClipAudio` with a
   `PreviewAudio` PCM-preparation adapter. The render branch remains the Agent
   export consumer until Agent publishes the shared compiled-clock contract.
3. For an envelope clip, prepare the source once per exact tuple
   `(source URL, compiled envelope identity, source clock, playback rate)`:

   * if a trusted `clip.audio.render_source` is present, validate/use it via
     the public exact-match API;
   * otherwise fetch the source with an abort signal, decode it in a temporary
     `AudioContext`, copy its channel views, call public `applyAudioEnvelope`
     with the Agent-provided source clock and playback rate, and make the
     result available through public `audioEnvelopeWav` and a blob URL;
   * put only the envelope-shaped gain into the prepared PCM. Pass the
     constant `baseVolume` to the media element/Web Audio graph separately;
   * revoke a blob URL on replacement, cancellation, or unmount.

   The source clock is a contract input, not an App inference. It must account
   for source trim, occurrence clipping/offset, and speed exactly as the Agent
   shared audio contract specifies. In particular, do not replace it with a
   video-frame index or silently use the current `frameOffset` callback as a
   PCM substitute. `applyAudioEnvelope`'s documented source-time equation is
   the qualification oracle for this adapter.

4. Keep `PreviewAudio` as the media/lifecycle owner. Preparation pending or
   retry backoff holds the Player; successful preparation then uses the same
   can-play/future-data readiness path; a failed fetch/decode is a fresh
   bounded attempt and reports through the existing failure provider. Do not
   use `pauseWhenBuffering` as a replacement for the existing hold policy.
5. Render the prepared URL with a constant volume prop. Preserve `muted` as a
   zero base gain, preserve `useWebAudioApi` for `baseVolume > 1` and the
   existing conservative envelope-boost admission, and preserve the current
   media remount key when source/clock/amplification inputs change. No
   per-frame `volume(frame)` callback remains on the prepared PCM path.

The likely product edit is one focused change to
`src/tools/video-editor/compositions/AudioTrack.tsx`, with a small adjacent
pure/hook helper only if keeping the preparation state out of the component
materially reduces risk. `RemotionPreview.tsx`, Player controls, output
projection policy, and render/player routing are out of scope.

### Data-shape prerequisite

The current App `TimelineClip` type (`src/tools/video-editor/types/index.ts:365-412`)
does not declare the public10 `audio` runtime field. More importantly,
`shotCompositionProjection.ts:390-434` copies the canonical child fields but
does not copy `audio` or `audio.render_source`. The current media-conformance
test fabricates a `render_source` only in its local fixture
(`TimelineComposition.media-conformance.test.tsx:178-182`); that is not a
production handoff.

Before implementation, Agent must publish the one compiled-clock/gain
contract and the trusted-host prepared-transform join. App then needs the
smallest reviewed projection/type preservation needed to carry that exact
runtime field to `AudioTrack`; it must not invent a new App DTO or turn
`render_source` into authored state. If the contract intentionally keeps the
field outside the App projection, the handoff must instead expose the
prepared source through an existing resolved-clip input with the same exact
identity checks. Until that source-based join exists, App can only qualify
its in-memory adapter shape, not actual prepared preview audio.

## Ownership split and evidence

| Area | Owner | Minimal responsibility |
|---|---|---|
| One compiler and source clock | Agent | Publish the reviewed compiled envelope/clock contract; apply the same policy to normal export and trusted prepared output. No App policy copy. |
| Preview adapter | App | `AudioTrack.tsx` browser branch: public PCM preparation, constant base gain, existing readiness/hold/retry/failure/mute/amplify behavior. Preserve ordinary no-envelope media path. |
| Player/render/PCM instrument | Viewing | Actual Player capture, actual final-export decode, waveform/source-time goldens, and the qualification instrument. No duplicate DSP/compiler. |
| Composition package | Composition/Viewing | The reviewed public10 package/API and its package qualification. App consumes the exact pinned bytes only after the coordinated M1/root adoption decision. |

The App unit tests should stay next to `AudioTrack.tsx` and prove:

* a 48 kHz (or other explicit) Float32 PCM fixture is multiplied at sample
  source times, including samples between video frames; the expected values
  come from `audioEnvelopeAt`, not a frame table;
* trim, occurrence/source offset, and playback-rate clock inputs use the
  shared contract tuple, with no frame-step approximation;
* prepared PCM receives envelope gain once and the media element receives one
  constant base gain (including `0.8 × 0.5 = 0.4` and boost cases);
* pending preparation holds the Player, can-play releases it, failed
  preparation retries with the existing delays, and cancellation revokes the
  old blob URL;
* mute produces zero output and amplify retains the Web Audio path; an
  ordinary no-envelope clip retains the current direct source path;
* a forged/mismatched `render_source` refuses through the public exact-match
  validation rather than being played.

The existing frame-step comparator in `AudioTrack.test.tsx` and the current
frame-table media-conformance assertions remain as historical RED baseline
evidence. They must not be relabelled as PCM qualification or widened. During
the implementation change, any expectations made intentionally obsolete by
the retired callback should remain named and become strict requirement-linked
expected failures, rather than being deleted or inverted.

Viewing's qualification must use actual Player PCM versus actual final-export
PCM with the same pinned media/closure and unchanged fail-closed timing,
channel, waveform, and gain bounds. Synthetic PCM proves only the adapter's
sample arithmetic; it is not an audio-parity claim. The currently retained
Player capture findings remain RED and do not qualify this seam.

## Proposed deletion-ledger row

The manager should apply this as the cross-owner row after review; this worker
does not edit the manager-owned ledger.

| id | what | contradicts | replaced by | owners | milestone/status | evidence/exit |
|---|---|---|---|---|---|---|
| VW-AUDIO-STEP (proposed handoff) | App `AudioTrack.tsx` per-frame `volume(frame)` envelope callback, including the old public `audioEnvelopeAt` frame-table comparator | One continuous PCM source-time gain policy | Public Composition `applyAudioEnvelope`/`audioEnvelopeWav` in App preview and the same Agent export compiler; constant base gain plus existing App lifecycle retained | App + Agent + Viewing | M3, in progress | Keep the existing frame-step RED record forever. Delete only after Agent's compiled-clock contract is published, App's real prepared/PCM adapter is live, both consumers use it, and Viewing's actual Player-vs-export PCM goldens pass without threshold widening. |

## Blockers and decision status

* The reviewed 0.0.10 artifact and public functions are present, but App still
  has 0.0.8 installed; no install or package/root edit is authorized in this
  audit.
* The Agent `audio-compile-contract.md` and published trusted prepared-source
  join are not present in the accessible source trees. The exact clock tuple
  and production `render_source` forwarding therefore remain unverified.
* Current App projection/types do not preserve the public10 runtime audio
  field, so no claim is made that an Agent-prepared WAV can reach the main
  preview today.
* No test, browser run, build, typecheck, export, or audio-parity claim was
  made for this audit. M3 integration remains held pending the coordinated
  M1/root adoption and the Agent/Viewing handoffs.
