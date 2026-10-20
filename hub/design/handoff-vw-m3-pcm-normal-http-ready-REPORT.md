# Normal-path PCM HTTP/WAV qualification — blocked

Status: **BLOCKED; no central run requested.** The assigned tree does not
contain the source-carry/call-site prerequisite needed to write an honest
normal-path served-WAV test.

## Evidence

- Assigned `HEAD` is `2019d7e69ceb9b10f18cc311e570d635b16c15d8`
  (`ce2510034f3edebef7430dd018c566101ea298fb` parent), the approved inactive
  normal-PCM prerequisite only. The `tl/vw-m3-normal-pcm-source-carry` ref
  points at the same commit; its delta is the ten-file inactive producer/test
  prerequisite, not source carry.
- `astrid/core/rendering/service.py::_segment_request` still writes an
  invocation-private sliced timeline and returns a replacement `RenderRequest`;
  it does not retain or transport an admitted unsliced/transformed compiled
  pair.
- `Timeline.for_render()` still only constructs `TimelineRenderView`; no
  original-clip association crosses that serializer boundary.
- `astrid/packs/rendering/rendering/renderers/remotion/run.py::_execute_remotion_locked`
  still serializes `merged_props`, starts the existing materializer/server,
  and launches the final Remotion CLI. There is no
  `prepare_normal_audio_sources` call site in the normal path. The only
  repository call is the direct helper fixture in
  `tests/packs/rendering/test_normal_audio_sources.py`.

Consequently, the existing served whole/phase fixture cannot be relabelled as
normal-route evidence. Calling the inactive helper directly would violate the
requested provenance boundary; adding a test-only source factory, authority
grant, handler stub, or invented transport would hide the missing admission
fixture.

## Specific missing fixture

The source owner must first land the approved source-carry join on this exact
cohort and expose a real invocation path that:

1. admits and validates the unsliced compiled request and its deterministic
   host transform together;
2. retains the original compiled occurrence clips through
   `_segment_request` and `Timeline.for_render()` for whole/window/layer
   requests, without reading authored `astrid_slice_origin`, IDs, or other
   caller metadata as authority;
3. calls the owned `normal_audio.py` preparation inside the existing
   `AssetMaterializer`/`InvocationAssetServer` `ExitStack`, before props are
   written for the final encoder, and keeps the attempt/server alive through
   consumption; and
4. preserves the existing normal admission, retry/cancel/error, gain/mute/
   amplify, registry, and cleanup behavior.

Only after that join exists can the ordinary repo test proposal be applied.
It should drive that real `RenderService` → `_segment_request` →
`for_render` → owned Remotion backend path, intercept only the final browser/
CLI encoder subprocess after prepared props exist, independently GET each
prepared URL with `urllib`, and assert native WAV bytes, exact source phase,
gain-once, window/layer original retention, digest/asset binding, forgery and
double-apply rejection, batch cleanup, 404 after attempt cleanup, and server
thread/port closure. The existing whole/phase fixture remains the reference
oracle; it must not be copied as a direct-helper-only substitute.

No unapplied repo test patch is emitted because there is no legitimate normal
entry point to exercise on this tree. This is the requested specific missing
fixture report, rather than an invented entry.

The two compiler strict xfails remain unchanged. They must stay until an
active normal producer supplies `audio.render_source` and the actual intent
passes; no xfail was added, removed, or weakened here.

## Checks run

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD \
  /home/user/work/venv-agent/bin/python -B -m pytest -p no:cacheprovider -q \
  tests/core/rendering/test_service.py -k 'window_timeline or segment_request'
5 passed, 47 deselected

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD \
  /home/user/work/venv-agent/bin/python -B -m pytest -p no:cacheprovider -q \
  tests/editing_conformance/test_compile_contracts.py
27 passed, 2 xfailed
```

No listener, socket-backed test, browser, CLI render, full suite, install,
central request, or grant was run. The shared-graph 106-cycle hold remains in
force; no borrowed graph was approved.

