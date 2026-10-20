# Normal export envelope PCM join — UNAPPLIED

**Hold: no trusted transformed prepared-source factory is available.** This is a
bounded asset-stage proposal, not producer qualification or export activation.
Current Agent integration/base is `33b0a8385f2cd184f0e79544f78678bc0dbee0d7`.
No product, core, source/capture/provider, Runtime, package or lock file changes.

## Inputs and existing seams

- Agent domain review: `hub/tl/agt-reviews-audio-mouth-scanner`,
  `2c094da6f1e2d601e9433044d942865171a75294`, files
  `design/audio-compile-contract.md`, `design/agent-review-viewing-20261020b.md`,
  and `tests/editing_conformance/fixtures/audio_compile_contract.json`. This is
  the updated contract, superseding the draft `fd82c36c7` offset/clock prose.
  Offset **350 is milliseconds**, retained verbatim as metadata; never rescale it
  to .35. Occurrence speed is metadata; child speed controls playback. Gain is
  child volume times occurrence gain in the Agent projector, then track gain
  downstream. Do not multiply occurrence gain again. Curves are honoured.
- `d2ad2ff82`: existing inactive `remotion/attempt-envelope-pcm.mjs` and
  `compiled-audio-source-clock.mjs`, with 22 reported passes. The latter calls
  public11 `computeMediaTrim` / `getSanitizedPlaybackRate`; the kernel calls
  public `compileAudioEnvelope` / `applyAudioEnvelope` / `audioEnvelopeWav` once
  per prepared clip. This proposal does not copy or replace those helpers.
- `3aa4c526b`: codec-origin characterization, 27 reported passes including those
  unchanged 22. Reconciliation report/flat handoff
  `handoff-vw-m3-audio-compile-vector-reconcile-ORCHREPORT.md`: 22 actual compiled
  outputs, 138 PASS / 5 RED. These are prior results, not reruns by this worker.
- Reviewed source candidate `435357aec` (`hub/tl/agt-m3-source-consumer-compose`)
  carries the existing `VerifiedTimelineSource`, `mint_prepared_source`,
  `inherited_source`, `source_for_timeline`, and Python-only
  `RenderRequest.verified_source`. The host mints after admitted materialization;
  the inherited environment anchors the binding. No public JSON grants trust.
  This source module is **absent** on the current integration base. In the
  candidate it only validates an exact original timeline/registry path+digest
  pair; there is no transformed-pair operation. Do not invent one here.

## Actual lifetime and insertion point

Normal render action `astrid/packs/rendering/actions/render/run.py:render` passes
materialized paths through `RenderService`. Its `_segment_request` writes
`segment-inputs/NNNN-timeline.json` for layered/full-timeline-only windows, using
`_window_timeline` / `_window_clip`. `replace(request, timeline_path=..., window=None)`
retains the original Python source binding in the reviewed candidate. That new
path cannot pass the original binding's `validate` check. Native window-aware,
unlayered requests keep the original pair.

Both normal 2D/Three.js paths reach
`astrid/packs/rendering/rendering/renderers/remotion/run.py:_execute_remotion_locked`.
The existing lock surrounds the complete operation. `AssetMaterializer` verifies
managed bytes and supplies `assets[key].local_path`; it refuses wrong digests.
`InvocationAssetServer(materializer.serving_root)` serves those local paths.
`resolved_registry(asset_server)` clones the registry with invocation URLs.
Root props contain that registry, serialized timeline and resolved theme.
In candidate `435357aec`, the existing `if source is not None` block validates
the pair and runs `compile_canonical_root_props`; its public result supplies the
resolved `compiledTransitions.fps`. Insert audio preparation **after** that
compile and **before** `props_path.write_text`, only for existing `not frame_mode`.

Use an `ExitStack`-owned `TemporaryDirectory` **under `materializer.serving_root`**.
The other `.remotion-runtime-*` directory may be outside the server root and its
files cannot be registered. `InvocationAssetServer.local_url(wav_path)` is the
existing registration operation; no new registry entry or object ID is needed.
`audio.render_source` belongs only to the copied Root-props clip. It carries
exact `{file, envelope_key, source_from, playback_rate}`. Keep the original asset
key and original managed source. The server and WAV directory survive CLI render
and stitching/response; the stack cleans them on success/error. The existing
finally removes `.remotion-props.json`. Authored files/snapshots stay unchanged.

## Concrete patch

1. [normal-audio-source-join.patch](normal-audio-source-join.patch), checked against
   current `33b0a8385`: four **new, inactive** proposed files:
   `astrid/packs/rendering/rendering/renderers/remotion/normal_audio.py`,
   `remotion/normal-audio-sources.mjs`,
   `tests/packs/rendering/test_normal_audio_sources.py`,
   `remotion/tests/normal-audio-sources.test.mjs`. The Python adapter binds sources
   from the existing materializer and checks exact resolved-registry encoding;
   Node receives private subprocess data, not authority or a public request DTO.
   It derives clocks itself and calls the existing kernel. Python registers the
   WAV through the supplied existing resolver. Neither helper mints a source.
2. [normal-audio-source-wiring.patch](normal-audio-source-wiring.patch) is the exact
   14-line insertion into the existing verified block on **`435357aec`**, not a
   patch that applies independently to current integration. It changes only the
   owned Remotion backend. It deliberately names no nonexistent transform API.
   Rebase this insertion onto the coordinator's actual final prepared-source
   composition; do not apply it until the following holds are discharged.

The source passed to the kernel is always the verified **original**, never a
prepared WAV. Full decoded sample count, original rate and channel count survive
into float WAV. No trim, resampling, normalization, scalar gain, mute, tempo,
padding or per-clip alignment is baked. Public trim/rate and constant gains stay
downstream. Missing envelopes leave clips unchanged. Invalid preparations fail;
there is no silence or frame-step fallback. No caches, flags, providers or DSP
policy are added. Existing package8/package10 artifacts/pins remain immutable;
the proposed helpers require later coordinated public11 adoption (artifact
SHA256 `dfa824a475737598477d98a2be2c2ad6ab9c3e6c8b0f967fad22e154afd74601`).

## Owner work required before applying the wiring

The coordinator must compose the existing host mint/validation path through
`RenderRequest.verified_source`, `RenderService._segment_request`, inherited
source transport and the shared serializer. Preserve original authority and
bind the **actual** transformed pair as a trusted derivation, with original
envelope phase. Do not remint from caller labels, set the environment in an
adapter, override `validate`, add a DTO, or relax the exact-pair check. This
proposal contains no implementation/signature for that absent factory.

Path rebinding alone is insufficient. Code-derived counterexample: a 0..2s
clip with .5s fade-in sliced to [.5,1.5) gets `from=.5,to=1.5,at=0` while retaining
`params.fadeIn=.5`. Recompiling that slice and using its new source clock starts
the fade at source .5 (gain 0), whereas the original envelope there has gain 1.
Prove full-film/window/layer equivalence using the original public policy; do
not declare transformed films unsupported or add a second fade compiler.

Decoder-origin debt also blocks activation: existing kernel's nonzero-start
check falsely refuses the characterized MP3 (1105 skip samples, origin retained),
while absent/zero start does not prove safety (ADTS AAC is 1024 samples late).
Offset AAC also shifted 1024; M4A/normal-video AAC retained onset with trailing
frames retained. Neither deleting the check nor adding a codec refusal closes
compatibility. Keep the kernel unchanged and qualify an owner-approved compatible
decoder join without shifts, padding, trimming or fallback silence.

## Acceptance and present evidence

Isolated proposal tests ran using extracted proposed files plus unchanged
`d2ad2ff82` helpers and the existing read-only public11 extraction/peers: **6
pytest PASS / 4 vitest PASS**. Actual stereo PCM16 decoding produces full 30000
frame float WAVs at 30000 Hz; `.05` origin is exactly `2/30` vs
`1/(30000/1001)`, child rate 1.5; scalar gain/metadata and inputs are unchanged.
Wrong Root asset URL, wrong managed bytes and double preparation are rejected;
public TimelineComposition/AudioTrack rejects forged origin/rate/envelope.
The URL resolver in Python is containment-only, and Remotion media primitives
in vitest are mocked. **No HTTP fetch, real normal producer or export is proven.**
Public `encodedEnvelopeSource` checks envelope/clock/HTTP syntax, not source
content. A matching key/clock on the wrong WAV can pass that public check.
Source binding must therefore be proven at the real host/materializer join,
never claimed from these metadata-only consumer controls.

After owner composition and coordinated dependencies, run the proposed main-suite
files directly (pure/no sockets), then the real normal-path tests centrally:

```sh
env -u NODE_OPTIONS -u NODE_PATH PYTHONPATH="$PWD" \
  /home/user/work/venv-agent/bin/python -B -m pytest -q \
  tests/packs/rendering/test_normal_audio_sources.py
# Use the installed, coordinated public11 package; no private source aliases.
/home/user/work/app/node_modules/.bin/vitest run --root remotion \
  tests/normal-audio-sources.test.mjs tests/attempt-envelope-pcm.test.mjs \
  tests/compiled-audio-source-clock.test.mjs tests/attempt-envelope-pcm.codec-origin.test.mjs
# After adding the real host/normal-producer acceptance file to this same suite:
R=$("$ORCH/bin/request-test" <owner-worker-name> targeted --files \
  "tests/packs/rendering/test_normal_audio_sources.py tests/editing_conformance/test_compile_contracts.py tests/packs/rendering/test_verified_source.py tests/core/rendering/test_verified_canonical_preparation.py")
"$ORCH/bin/wait-test" "$R"
```

Mandatory real-producer additions to `test_normal_audio_sources.py`: admitted
WAV through normal `_execute_remotion_locked`, GET the exact registered WAV
while Root consumes it, compare non-silent samples/envelope and downstream
trim/rate/gains, then verify cleanup and unchanged authored bytes. Use both
original corpora, resolved rational clocks, curves and occurrence clipping.
Negatives: same envelope+clock but **wrong managed asset/WAV**, forged clock,
forged caller render_source/source authority, and attempt to prepare an already
prepared clip. Add whole/window/layer fade-phase preservation and compatible
AAC/MP3/video cases; do not convert those behavior requirements to refusals.

The existing App ordinary `ENVELOPE_UNRENDERED` RED and Agent's two existing
strict-xfail requirements remain untouched. Only an actual trusted normal
producer positive permits removing those existing markers/failures. Four App
adapter mismatches remain separate owner work. No full, browser, socket,
export, install, network, service or physical parity run was requested here.
