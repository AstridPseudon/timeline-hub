# Mixed-source audio scope audit

## Finding

There is **no current ordinary public12/App audibility gap** caused by the
inactive normal PCM producer selecting audio-track clips only. That producer's
`audio.render_source` is consumed by the public12 `AudioTrack` envelope path;
visual video audio is carried by the visual clip's `<Video>` element and is not
supposed to be converted into an envelope source by the current contract.

There **is** a bounded omission if “continuous prepared fullmix” means a future
source-carry route that must prepare every audible sample into one external PCM
mix: visual-track video assets with embedded audio are not selected by the
normal producer. That is a source-inventory/ownership gap for that stronger
meaning of fullmix, not evidence that the existing normal public12 render is
silent. It needs an explicit source-owner decision and contract; no product
code or contract change was made here.

Custom dynamic elements are not a second currently declared audio source. The
public12 dynamic/effect path is visual; the App dynamic renderers receive clip,
params, theme/fps and optional asset data, but no audio-output declaration or
PCM source identity. The App test suite also preserves DB-stored sequence code
as migration-only and renders an unsupported placeholder. An extension could
arbitrarily emit media in its own React implementation, but that is not a
source the current compiler or normal PCM worker can safely infer.

## Exact source coverage

| Source | Existing audible behavior | Continuous prepared by normal PCM? | Audit result |
|---|---|---:|---|
| Audio-track audio/video clip with a compiled fade or explicit envelope | public12 `AudioTrack` computes an envelope, uses prepared `audio.render_source` outside Player, then applies constant `track.volume * clip.volume`; App `AudioTrack` uses the same scalar plus its frame/preview envelope adapter | Yes, when the prepared-source join is active | This is the producer's legitimate scope. `normal_audio.py:71-79` selects clips whose track kind is `audio`; `:123-129` writes the prepared source. |
| Visual-track video with embedded audio | public12 `VisualClip` renders `<Video>` with the original file, trim and playback rate; gain is `track.muted ? 0 : track.volume * clip.volume`, and non-positive gain also sets `muted`. App `VisualClip` has the same gain/mute behavior through `ReadinessVideo` | No | Still audible in the ordinary public12/App route. Not an envelope-bearing source under the settled audio contract. A true external fullmix would miss it unless visual media with an audio stream is added to source ownership. |
| Image visual clip | `<Img>`/image path; no audio stream | No | Not an audible source. |
| Built-in/public12 dynamic effect | Registered visual component output; no standard `<Audio>`/`<Video>` source contract in the public12 effect path | No | Not a current declared audible source. Do not invent PCM preparation for arbitrary effect output. |
| App DB-stored custom sequence | Deliberately not compiled/executed; loud unsupported placeholder | No | Not an audible source in the current App behavior. |
| App extension clip renderer | Arbitrary renderer receives visual `ClipRendererProps`; no declared audio source, gain/mute, or prepared-source contract | No | Potential future capability only. It cannot be safely included by source carry without a new explicit contract, which is outside this audit. |

## Behavior details

### Inactive normal producer

The reviewed producer is commit `ab935f77378ba5ea1df55ba775654f8bba233ebc`
(the implementation was introduced at `9fd669e481cf94ee641d9719f3ed7341910c2`).
In `astrid/packs/rendering/rendering/renderers/remotion/normal_audio.py`:

- lines 71-79 build the set of `kind == "audio"` track IDs and index only
  clips on those tracks;
- lines 97-100 resolve each selected managed asset, carrying an original clip
  only through the trusted source-owner seam;
- lines 123-129 attach `audio.render_source` with the envelope key,
  `source_from`, and `playback_rate`.

This matches the settled `audio-compile-contract.md`: continuous source-time
preparation is required for fade/envelope-bearing audio clips, while constant
gain is applied downstream. The contract's strict fade vectors are the
relevant prepared-source requirement; it does not define visual embedded audio
as an `audio.render_source` envelope input.

### Public12

The locked artifact is
`remotion/artifacts/banodoco-timeline-composition-0.0.12.tgz`. Its bundled
source is visible in `dist/index.js` and `dist/chunk-DMRW7SC3.js`:

- `dist/index.js:74-120` compiles an audio envelope and, in Player, decodes the
  raw source and applies `applyAudioEnvelope`; outside Player or with a
  prepared source it requires the exact prepared tuple through
  `encodedEnvelopeSource`.
- `dist/index.js:133-149` renders the audio-track `<Audio>` and applies
  `track.muted ? 0 : track.volume * clip.volume` as constant base gain.
- `dist/index.js:231-265` and `:313-323` render visual video with the source
  file, `computeMediaTrim`, playback rate, constant effective volume and mute.
  `useFadeOpacity` is visual opacity; it is not an audio envelope for the video
  element.
- `dist/chunk-DMRW7SC3.js:478-514` shows that only the compiled audio envelope
  is continuously baked into PCM, with source clock `(sample/sampleRate -
  sourceFrom) / playbackRate`; `:546-556` rejects a missing or mismatched
  prepared source.

The normal Agent root uses this public `TimelineComposition` at
`remotion/src/Root.tsx:83-100` and `:164-180`. Therefore a visual video with an
embedded stream remains a direct video-audio contribution in the ordinary
route, independent of the inactive audio-track PCM preparation.

### App current path

`/home/user/work/app/src/tools/video-editor/compositions/AudioTrack.tsx:223-351`
selects playable audio/video assets on audio tracks, computes
`track.muted ? 0 : track.volume * renderClip.volume` at lines 247-248, and
applies the authored fade through `getAudioFade`/`getAudioVolumeProp` at lines
299-323.

`/home/user/work/app/src/tools/video-editor/compositions/VisualClip.tsx:307-383`
and `:444-461` compute the same scalar gain and pass it to `ReadinessVideo`,
with `muted={effectiveVolume <= 0}`. Its video audio is not sent through
`AudioTrack` or a continuous envelope baker.

`TimelineRenderer.tsx:1598-1611` derives audio clips only from audio-track
IDs, and `:1753-1760` mounts `AudioTrack` only for those tracks. The dynamic
sequence paths at `:319-403` pass visual component props; the extension path at
`:1173-1259` passes only `ClipRendererProps` including `source`, `params`, and
`live`. `audioAnalysisDemand`/`AudioAnalysisProvider` concerns analysis of
audio-track input for visual reactions, not creation of an additional audible
source.

The existing App behavior test at
`src/tools/video-editor/compositions/TimelineRenderer.dynamic.test.tsx:103-129`
also verifies that DB-stored sequence code is not compiled and the custom clip
shows the unsupported placeholder. The sequence fixture at
`TimelineRenderer.sequence.test.tsx:412-435` is audio-reactive-colour: it
consumes analysis and changes visual colour; it does not produce audio.

## Existing fullmix/embedded-audio evidence

The Agent native FFmpeg path explicitly treats visual embedded audio as a
feature it would discard, not as an audio-track source to prepare:

- `tests/packs/rendering/_helpers.py:108-143` creates a real H.264 source with
  an AAC stream when `audio=True`.
- `tests/packs/rendering/test_ffmpeg_support.py:320-345` includes the
  `discarded_visual_audio` fail-closed case.
- `astrid/packs/rendering/rendering/renderers/ffmpeg/support.py:986-994`
  rejects a visual clip with an audio stream when effective gain is nonzero,
  reporting that FFmpeg would discard embedded audio.

This is important preservation evidence: the alternate FFmpeg backend must not
be used as proof that ordinary public12 video audio is intentionally absent.
The current public12 route preserves it through `<Video>`; a future true
fullmix route would need to extract/mix it deliberately rather than silently
reuse the FFmpeg discard rule.

## Pure checks run

- An inline Node assertion against the extracted public12 `dist/evaluation.js`
  passed. It checked a 1-second fade-in/fade-out envelope at 10 Hz, stereo
  `applyAudioEnvelope`, the `source_from` shift, float32 stereo WAV headers,
  and scalar gain composition (`track * clip`, including zero mute).
  Result: `public12 envelope/audio math OK: fade curve, source clock, stereo PCM, WAV encoding, scalar gain composition`.
- `PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -B -m pytest -q tests/packs/rendering/test_ffmpeg_support.py -k discarded_visual_audio`
  — PASS, `1 passed, 63 deselected`.
- `PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -B -m pytest -q tests/packs/rendering/test_composition_package.py -m 'not integration'`
  — PASS, `5 passed, 1 deselected`.

I also attempted `tests/packs/rendering/test_scene_host.py` without installing
anything. It first stopped because this worktree has no renderer peer
`esbuild`; retrying with the existing read-only peer tree at
`/home/user/work/composition/node_modules` reached the next prerequisite and
reported 15 setup errors because the pinned renderer requires Node `v20.19.4`
while this environment exposes only Node `v22.22.0`. No product code failed and
no dependency was installed or modified. Browser, socket, full-suite, and live
render tests were not run.

The assigned Agent worktree remains clean; no repo code, tests, markers, package
symlinks, or build output were added.

## Handoff decision

Keep the normal producer audio-track-only for the current prepared envelope
join. Preserve direct visual video audio in the ordinary public12/App path and
do not reinterpret visual opacity fades or arbitrary dynamic JSX as audio
envelopes.

If the orchestrator means “fullmix” literally as one continuous prepared PCM
mix, record a separate follow-up requirement: the trusted source owner must
inventory visual-track video assets with audio streams, apply their visual
track/clip mute and gain, and define their source trim/rate/overlap policy.
Dynamic audio would likewise need an explicit declared source contract. That
follow-up is not safely implementable by changing the current selector alone,
and no such change was made.
