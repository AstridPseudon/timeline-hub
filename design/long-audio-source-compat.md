# Long audio source compatibility — UNAPPLIED

Status: offline proposal only, based on Agent `384918908` and the inactive
`d2ad2ff8290c8b11d8f97ccc7d669bd7a451daf5` helpers. No producer, provider,
core, pins, normal route or authenticated source changes. Public11 future
adoption remains coordinated separately. This is not normal PCM qualification.

The PLAN keeps existing films' music beds. A valid source just over a decoded
stdout buffer limit must remain playable; no layer, window, codec or size cut
is approved. The old helper's `maxDecodedBytes = 64 * 1024 * 1024` makes an
ordinary 174.7626875-second, 48 kHz stereo float decode fail with ENOBUFS.

## Exact inputs and patch base

- `fd9f50f490aaa47465eee947d9fb370a9387c1ac`, completed
  `tl/vw-m3-attempt-envelope-pcm-prep`: original 70-line PCM kernel and tests.
- `d2ad2ff8290c8b11d8f97ccc7d669bd7a451daf5`, completed
  `tl/vw-m3-envelope-public-clock-join`: same kernel with updated clock comment,
  plus the 13-line `compiled-audio-source-clock.mjs` public adapter. This is the
  patch's exact base. The helper also appears in the earlier flat
  `handoff-vw-m3-audio-normal-source-join-plan-proposal.patch`; do not add a
  second copy when composing those proposals.
- Completed codec-origin ORCHREPORT: MP3 has a concrete false refusal;
  timestamped AAC and absent-start ADTS demonstrate why simply deleting the
  start-time test is unsafe. No codec/origin repair or new refusal is proposed.
- `design/audio-compile-contract.md`: public trim rounding, child playback
  rate, continuous source-time envelopes; occurrence source_offset/speed are
  metadata, scalar gain stays downstream, authored curves are honoured.

`long-audio-source-compat.patch` changes only the proposed inactive kernel and
adds `remotion/tests/long-audio-source.test.mjs`. It is a delta atop d2ad,
not an integration-applicable standalone addition. It was checked/applied only
in a disposable ORCH directory; the resulting two files equal the tested files.
Neither helper nor regression is installed in the product tree by this task.

## Smallest demonstrated decode change

Send the existing synchronous FFmpeg stdout to an exclusive attempt-local
`decoded.f32` descriptor, instead of collecting its PCM in execFileSync's
maxBuffer. Existing normal rendering already redirects subprocess stdout to a
file (`renderers/remotion/run.py`, the `stdout_log` subprocess.run call); use
that same OS primitive, with no new dependency, DSP, decoder or framework.

Read this file in frame-aligned ~64 KiB blocks into the full-source planar
Float32Arrays required by public apply. Handle short reads without dropping
bytes. Keep public `applyAudioEnvelope` and `audioEnvelopeWav` unchanged, with
exactly the original source clock. Delete decoded scratch before publishing
`source.wav`; delete the newly allocated directory on failure. Never touch an
unrelated attempt file or the original source. The only remaining maxBuffer
values bound probe JSON/diagnostics, not PCM stdout. No replacement size ceiling.

This removes the decoded pipe copy and arbitrary 64 MiB default; it does
**not** bound RAM independently of duration. For D decoded bytes, the live
channel arrays plus public WAV require approximately 2D, plus fixed I/O buffers
and runtime overhead. Memory allocation, FFmpeg/IO and public-envelope failures
propagate; they are not reclassified as valid-source refusal or silent fallback.

## Exact bounded-memory owner seam — still required

There is no file-backed Float32Array in the existing Node path. Public11
`applyAudioEnvelope(channels, sampleRate, envelope, sourceFrom, playbackRate)`
uses `(sample / sampleRate - sourceFrom) / playbackRate` from sample zero.
Calling it on blocks with `sourceFrom - offset/sampleRate` changes floating
operation order; shifting keyframes changes the policy. Neither is a byte-exact
reuse of the existing clock. Public `audioEnvelopeWav` allocates the whole file.

Return this specific seam to the Composition audio owner, rather than creating
another gain implementation or pretending the file-backed patch is bounded:

1. Extend that existing public apply function with a default-zero absolute
   `sourceSampleOffset`. Evaluate
   `((sourceSampleOffset + sample) / sampleRate - sourceFrom) / playbackRate`.
   Offset zero preserves existing calls exactly; frame-aligned block offsets
   reproduce each whole-source sample's original arithmetic. Validate safe
   integer offset/count. No second curve/envelope evaluator.
2. Supply a file/sink WAV path using the existing public float WAV serialization,
   bounded blocks, and one full-source header. Test identical IEEE float bytes
   against current `audioEnvelopeWav` for RIFF-sized sources. The existing
   public writer uses 32-bit RIFF sizes and would wrap beyond that format's
   range; the owner must support long-file WAV representation (e.g. RF64) with
   the real consumer, rather than imposing a new size refusal. No such format
   or public API change is made here.
3. The Agent attempt/asset-stage owner then composes the existing decoder stdout
   file with those public block APIs. Preserve native rate/channel layout,
   exact source clock, original gain/trim/rate/mute downstream, honest process
   failures and attempt cleanup. No new producer/framework is needed. The
   inherited 30-second process timeout is also not evidence of arbitrary-length
   compatibility; lifecycle/time-budget handling belongs at that existing seam.

Until these owner seams are proven, this patch is an illustrative compatibility
proposal for the 64 MiB regression, **held from adoption as a bounded-memory or
all-size solution**. No valid film is declared unsupported. Codec origins,
original fade phase across layers/windows, transformed prepared-source binding,
trusted served-WAV admission and coordinated public11 adoption remain separate
unresolved dependencies from the earlier handoff.

## Ordinary positive regression

One native Node test process, sequential local subprocesses, one large fixture
at a time; `TIMELINE_HEAVY=1` explicitly required (dispatch metadata heavy=1).
Independently write a 48 kHz stereo IEEE-float WAV in small blocks: 8,388,609
frames = 67,108,872 decoded bytes, exactly 64 MiB plus one stereo frame. Unequal
channels, unequal tail impulses, public rounded rational-fps trim origin and
1.5x child rate expose truncation, channel loss and clock changes. Constant clip
volume 7 must not be baked. No resampling, normalization, alignment, timestamp
adjustment, trimming, padding or final codec is used.

The same ordinary positive test fails against d2ad with ENOBUFS and passes with
the proposal. It compares the entire WAV SHA256 against independent whole-source
channels passed through unchanged public apply/WAV, checks native headers/full
count, metadata, source/graph immutability, scratch deletion and tail boost,
and decodes the result with real FFmpeg to confirm count and tail samples.
A second small test checks nonfinite and empty/truncated-source cleanup while
preserving an unrelated attempt file. No existing test is edited or weakened;
no xfail, skip or new validity refusal is added.

Exact commands/results and limits are in the worker's `ORCHREPORT.md` and flat
ORCH handoff. Final positive run: 2 pass / 0 fail / 0 skipped, 3.416 seconds;
peak process RSS 193,308 KiB (~188.8 MiB). This is measured fixture use, not a
memory ceiling. No full suite, install, network, browser, socket or export run.
