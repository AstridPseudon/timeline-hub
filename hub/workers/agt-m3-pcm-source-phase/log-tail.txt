The Agent side is done, but only part of the task: the four forced PCM regressions stay strict xfail. Nothing in this tree can serve or consume a prepared WAV.

**Why the four stay xfail:** the proposal's tests import `astrid.packs.rendering.rendering.renderers.remotion.normal_audio.prepare_normal_audio_sources`, which doesn't exist here. Its `AssetMaterializer` / `resolved_registry` / asset-server API doesn't match this tree either. `regressions.patch` therefore can't be applied as written. I didn't mock a host. A mock would be false authority, and the handoff says not to.

**What I changed:**
- **Slicer:** `RenderService._window_clip` (`astrid/core/rendering/service.py`) now records `app.astrid_slice_origin = {id, at, from, to}` on clips with `fadeIn` or `fadeOut`. Any authored value is dropped, so the host owns it. Clips without fades are unchanged.
- **Why it's needed:** the slicer rewrites `at`/`from`/`to`, so two different originals can slice to the same clip. For example, `at=0,from=0` and `at=.5,from=.5` give identical slices, but the original gain at source 0.5 is 1 versus 0. Recording the origin is the "carry the original clip identity through the existing trusted producer" step.
- **`tests/packs/rendering/test_normal_audio_source_phase.py`:**
  - Two slicer tests pass: the origin is recorded and distinguishes the two originals, and it is host-owned and fading-only.
  - Four PCM tests are strict xfail with `raises=ImportError`. They cover the 0..2 s clip sliced at 0.5 s with `fadeIn` 0.5, for both overlapping assets, in window and layer mode. The expectation is that the slice keeps (.25, -.125) at source 0.5.
  - The PCM test bodies are stubs: they only attempt the missing import. I did not carry over the patch's comparison bodies.
- **`design/audio-compile-contract.md`:** new "Slice phase" section with the translation the future producer must apply: compile E0 once, take q0/q1 from the public `computeMediaTrim` of the original and sliced clip, and shift every envelope keyframe by `-(q1-q0)/r`.

**Tests:** I ran them through the central service, not directly.
- **Command:** `request-test agt-m3-pcm-source-phase targeted --files "tests/packs/rendering/test_normal_audio_source_phase.py tests/core/rendering/test_service.py tests/packs/rendering/test_live_scene_boundary.py tests/editing_conformance/test_compile_contracts.py"`
- **Result:** 99 passed, 8 xfailed. The 8 are my 4 plus the 4 existing `audio_compile_contract` xfails.
- **Not run:** no full suite, and none of the patch's JS or vitest tests, because that is Viewing's `remotion/` package.

**Next step:** the Agent prepared-source producer needs to read `astrid_slice_origin` and apply the envelope translation. When it can serve a real WAV, replace the PCM stubs with the patch's comparison bodies and remove the xfail markers.

The commit message is written and the `DONE` file is created.
