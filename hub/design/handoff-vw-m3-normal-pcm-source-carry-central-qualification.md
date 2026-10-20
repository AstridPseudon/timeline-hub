# Central qualification preparation — BLOCKED, DO NOT RUN

Source base ce2510034 plus exact 0a8c75772..ab935 prerequisite only. Await the
harness commit SHA; this document does not certify source carry or a caller.
No central request was made. No suite was registered or altered.

The existing whole-source HTTP controller and seven-case fixture are at:

- /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-pcm-served-whole-ready-controller.py
- /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-pcm-served-whole-ready-test_normal_audio_served_sources.py
- /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-pcm-served-whole-ready-ORCHREPORT.md

Read-only references, not copied, edited, rerun or relabelled. Their source-SHA
and peer graph are a DIFFERENT frozen source; their previous readiness must
not be transferred to this tree. In particular the same-106-cycle peer graph
hold in manager records is not resolved by this worker's different direct-test
graph. This worker's unchanged 2056-entry graph proves only no mutation by
these local tests. A normal-route controller needs a fresh exact source freeze
and before/after manifests of the entire graph it will actually use. Any drift
blocks central execution; do not accept a new baseline silently.

After Agent supplies the existing admitted unsliced/transformed binding and
the permitted callsite is implemented, prepare one bounded named suite (not
full) against that exact committed source. It must exercise the real normal
render caller, not call the inactive helper as its only entry. Required cases:

1. Original unsliced compiled timeline and registry are admitted together.
   Altering/swapping either before source consumption fails admission without
   publishing output. Forged app stamps/IDs confer no authority.
2. Whole, host window and layer exports retain exact original compiled clips
   through _segment_request and Timeline.for_render, including overlapping
   distinct stereo sources. The .5s cut of a 0..2s .5s fade retains (.25,-.125)
   at the original source .5s. Include explicit recursive envelopes, original
   exit fades, rational fps and child rate; no alignment or wider tolerance.
3. Actual HTTP GET of each prepared URL yields its own exact full native WAV
   bytes/sample count, unchanged channel count/rate, public12 applyAudioEnvelope
   once and public rounded trim/rate. Distinct source bytes under identical
   envelope/clock produce distinct correct URLs/WAVs. Swapped/forged WAVs and
   already-prepared render_source cannot substitute for admitted media.
4. Perform consumption during the actual normal invocation. Attempt WAVs and
   the server remain live until export finishes, then close/remove on success,
   cancellation, native error, registration failure and retry. Only disposable
   props/attempt outputs change; original compiled input/media/registry remain.
5. Check scalar/occurrence/track gain once, mute/amplification, no-envelope
   normal behavior, default routes/cache and source errors. Independently prove
   existing two compiler requirements green before dropping their xfails.

Current blocker: ce251 has no inherited compiled-source binding, mint or
transformed-pair validator. Building the above trusted fixture without the
real contract would require a test-only authority and would not qualify the
product. The exact blocked paths and owner recommendation are in the sibling
REPORT.md. Resume fixture implementation only after that contract exists.
