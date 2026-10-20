## Report: agt-m3-fade-join

**I did not build the join, so ENVELOPE_UNRENDERED vectors 10-11 and the slice PCM tests are still strict xfail.** There is no real prepared-WAV host path in this tree, and your brief said to record what's missing instead of adding mocks. The only change is a "Join status" paragraph in `design/audio-compile-contract.md`.

**What's missing:**
- **No `applyAudioEnvelope` to join to.** The Composition package installed for hosts (`/home/user/work/app/node_modules/@banodoco/timeline-composition`) has no `applyAudioEnvelope`. The 0.0.10 source in `/home/user/work/composition` does export it, along with `audioEnvelopeWav` and `encodedEnvelopeSource`, but no installed build carries them.
- **No prepare-and-serve step.** The Remotion render route (`remotion/run.py`) never decodes a source, writes an envelope WAV, or serves it. `encodedEnvelopeSource` only accepts an `http(s)` URL, so this step is needed.
- **No `render_source` from the compiler.** The compiler can't set `audio.render_source`, which vectors 10-11 expect, because it has no file to name.
- **No Python port.** A Python port of the envelope would duplicate the public Composition policy, so I didn't add one.

**Test result:** targeted run through the test service (cached tree `deffff75…`, no full suite requested):
`python -m pytest -q tests/editing_conformance/test_compile_contracts.py tests/packs/rendering/test_normal_audio_source_phase.py tests/core/rendering/test_service.py`
This gave 81 passed, 6 xfailed in 47s, exit 0. The six xfails are the two fade vectors and the four slice PCM tests.

**Next step:** install a Composition build that exports the 0.0.10 audio-envelope functions into the Remotion project. Then add the prepare step to the render route as planned, including the slice-origin keyframe translation in the "Slice phase" section. That step should write the `audio.render_source` field the vectors expect.

I wrote the commit message to `commit-msg` and created `DONE`. I didn't create `BLOCKED`, since the documentation part is complete.
