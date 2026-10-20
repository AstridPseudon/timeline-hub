# Normal PCM source proposal: one Agent owner handoff, UNAPPLIED

Review base `6b108a8ef5b8a658bae26de59b373342dec40c71`. Reviewed the PLAN,
`design/audio-compile-contract.md`, source-join worker ORCHREPORT, and all three
`design/normal-audio-source-*` artifacts at
`tl/vw-m3-audio-normal-source-join-plan`. Source candidate inspected at
`435357aec`; inactive kernels at `d2ad2ff82`; existing public11 built exports
read from the prior worker's immutable extraction. No activation is qualified.

**Next owner: Agent's existing normal-source/capture coordinator.** Complete one
trusted segment derivation through the existing Python source transport, carrying
both original clip phase and exact asset identity to disposable Root props.
Do not apply the proposed 14-line wiring insertion independently. Its adapter
has no original-clip input and cannot repair phase from sliced props alone.
No new factory, provider, public DTO, environment setter or authority bypass is
proposed. Core/provider/pins are read-only in this review.

## Why the current proposal is insufficient

`RenderService._segment_request` reads the original timeline, then calls
`_window_timeline` / `_window_clip`. A layered request always takes this path;
an unlayered full-timeline-only renderer also takes it. The replacement request
changes `timeline_path` and clears `window`. Candidate `435357aec` retains the
original `verified_source`; `validate`, `inherited_source` and serializer
`source_for_timeline` demand the exact original path and digest. Revalidating
the original object after PCM preparation does not qualify a transformed pair.
The source candidate has original-pair minting/validation, no implemented
transformed-pair composition. This is an Agent owner dependency.

The slicer preserves `metadata.source_window_start_seconds` and end seconds,
but overwrites each intersecting clip's `at`, `from`, `to`, ID and sometimes
`hold`. It leaves fade parameters intact. A 0..2s clip with fadeIn=.5, sliced
to [.5,1.5), becomes at=0/from=.5/to=1.5. Public envelope recompilation starts
its fade again: at source sample 15000/30000, original stereo PCM is
(.25,-.125), proposed slice PCM is (0,-0). Fade-out also moves prematurely.
The added regression repeats this with a second overlapping source and the
layer track filter; it checks each WAV independently, avoiding mix cancellation.

The retained window metadata is insufficient: original clip
`at=0,from=0,to=2` and original clip `at=.5,from=.5,to=2`, otherwise identical,
produce identical sliced clips and metadata for that window. Their original
gains at source .5 are respectively 1 and 0. The new passing test proves this
using the actual slicer. Do not reconstruct original time from the suffixed ID,
new `at`, new `from`, or source_offset metadata.

## Exact correction at the existing producer

At the original-input stage of `_segment_request`, retain the admitted original
pair and deterministic window/track transform through the existing source
owner's private composition. The original compiled occurrence clips are
available in that pair, and in the retained admitted snapshot/projector inputs.
Use the existing ONE projector/serializer, including occurrence caps and gain;
never re-project raw children with a different duration policy. Keep the mapping
while iterating original clips, before IDs/bounds are replaced. Validate the
actual transformed pair in the existing source flow, including inherited
transport and serializer. Caller labels cannot supply that mapping or authority.
The source owner must implement that missing composition; this review invents
no callable API for it.

At disposable Root-props preparation, use the resolved public fps and the
original compiled occurrence clip `c0`, paired with its sliced clip `c1`:

```text
W = FrameWindow.start_frame / Fraction(*FrameWindow.fps_rational)
visible_start = max(original_clip.at, W)         # actual existing slicer
c1.from = c0.from + (visible_start - c0.at) * child_rate
q0 = computeMediaTrim(c0, fps).trimBefore / fps
q1 = computeMediaTrim(c1, fps).trimBefore / fps
r  = getSanitizedPlaybackRate(c0.speed)           # unchanged on c1
E0 = compileAudioEnvelope(c0, fps)                # original fade-out duration too
delta = (q1 - q0) / r
E1(t) = E0(t + delta)
```

Represent `E1` using existing `clip.audio.envelope`: subtract delta from EVERY
keyframe's `at`, recursively through multiply/minimum, preserving values,
curves and other envelope fields. Negative keyframe times are already valid in
public11. This translates the public result; it adds no fade compiler or DSP
policy. The unchanged public helper prefers the derived envelope over params.
Then the unchanged kernel applies it once using `q1,r`; public AudioTrack admits
the same envelope/clock and applies sliced trim/rate once. For any source time s,
`E1((s-q1)/r) = E0((s-q0)/r)`. It preserves original fade-in AND fade-out.

Use the difference of rounded origins, not simply W, W-original_at, or raw trim
difference. Example: from=.05, rate=1.5, W=.5 at 30fps gives q0=2/30, q1=24/30,
delta=22/45, not .5. The proposed public-helper tests cover this and 30000/1001
fps, linear/equal-power/s-curve. No sample shift, trim, padding or alignment.

Keep derived audio data ONLY in disposable compiled props, after canonical
validation. Do not write it into authored snapshots or trust caller-supplied
`audio.envelope` / `render_source` as a prepared-source grant. The real serializer
must demonstrably preserve the owner's derived result at that boundary.
Occurrence source_offset **350 milliseconds** and occurrence speed stay metadata;
child speed sets r. Occurrence gain is already in clip.volume; keep track gain,
mute and amplify downstream, without multiplying occurrence gain again.

## Asset URL and byte identity are the same handoff

Root's actual original source URL is `assets.assets[clip.asset].file`, passed as
AudioTrack's asset entry. There is no new `clip.assetURL` field to authorize.
The adapter's comparison with `materializer.resolved_registry(asset_server)` is
useful, and materialization checks managed digests. Preserve that exact pairing:
original registry key -> verified local_path -> decoded original bytes -> this
clip's prepared WAV -> `asset_server.local_url(path)` -> Root render_source.file.
Keep the original registry unchanged. Use the existing server and ExitStack
lifetime, with WAVs under materializer.serving_root through consumption/cleanup.

Public11's encodedEnvelopeSource validates envelope/clock and HTTP syntax; it
cannot distinguish swapped WAVs with matching metadata, or establish original
asset identity. Do not widen that public API or claim consumer admission proves
source authority. The new two-asset control uses identical envelopes/clocks and
unequal independently written stereo PCM; resolving each returned URL to its
actual file proves the private adapter preserves the pairing. It would detect
WAV/URL swaps and source aliasing. Existing wrong-registry-URL, wrong-managed-byte
and double-apply negatives still pass. This remains a containment-only resolver,
not a real served-asset or trusted normal-producer positive.

## Regression patch and owner acceptance

[normal-audio-source-regressions.patch](normal-audio-source-regressions.patch)
adds two files to main's existing pytest/vitest test directories. Apply AFTER
the original UNAPPLIED join patch plus unchanged d2ad helper prerequisites;
this patch itself applies cleanly to review base. No product changes are in it.
Four new positive slice expectations are strict xfails, naming the restoring
Agent source requirement. `--runxfail` proves all four fail at PCM comparison.
No passing test is rewritten, skipped or weakened. Existing contract xfails and
ordinary ENVELOPE_UNRENDERED requirements stay unchanged.

The test-only JS translation demonstrates an existing representation; do not
copy it into tests to manufacture a producer positive. The owner must carry the
same expectations through the actual `_segment_request` -> source validation ->
serializer -> `_execute_remotion_locked` path, then remove the four markers when
the genuine path restores them. A direct sliced-props helper test cannot certify
that transport. Central targeted acceptance must read the exact served WAV
while Root consumes it; assert both overlapping sources, whole/window/layer
samples, trim/rate/gain, same-envelope/clock different assets, forged authority,
wrong managed bytes/URL/WAV, double apply, cleanup and authored immutability.

Reported here: extracted proposal pytest **8 pass / 4 strict xfail**; forced
requirements **2 pass / 4 fail**; public11 vitest **8 pass**; existing service
window/segment tests **5 pass**; compile contracts **27 pass / 4 existing xfail**.
Exact commands and logs are in this worker's ORCHREPORT.md. Tests use actual
native decode/public11 exports; media primitives in existing vitest are mocked.

This completes the bounded review, not normal-export activation. Decoder-origin
compatibility debt (including characterized MP3 false refusal and AAC +1024)
and coordinated public11 adoption remain the existing separate activation holds;
no kernel, tolerance, codec rule or pin changes. No browser, export, full suite,
network, socket, install or central service was run. Layer/window behavior must
be restored through the owner composition; valid films are not newly refused.
