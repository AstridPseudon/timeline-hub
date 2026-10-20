# RT07/D13 native historical render admission

Date: 2026-10-20

## Source tuple

- Runtime product base: commit `16acbb6ef94a6d8e226ccdc351ba0d96e0b09ea5`,
  tree `6a6ba82cb05200bb822669c19fab2aed40a73076`.
- Central targeted snapshot (includes the 125-line test below): tree
  `6c8a1f6ec4bd38a977b9c40fbf9d0ee23cf13fed`.
- Frozen ordinary Agent: commit `310e54840fa5fb8eb7e51bb64ed2c34b7a1063b3`,
  tree `c5a8a3ec7e9e01c61c5ae31834da53bed4be406a`.
- Agent normal request builder: `astrid/core/dev/journey.py`,
  `build_app_render_admission` (the approved App-shaped `rendering.render`
  builder).
- Runtime test: `tests/test_render_native_historical_retry.py`.
- Media/bootstrap source: the existing committed
  `tests/fixtures/precut-music-documents-v31.tar.gz` fixture. No fixture JSON,
  schema, Runtime API, or shared dependency was changed.

## Exact body and receipt identity

The test uses the Agent builder for the request body and transport key. For the
measured fixture run, the Runtime project was
`7b6f2bae8ffe42bf925216c38249ed79`, timeline `film`, and the render capability
digest was `sha256:dfe0363cbd511725f0a693c8d26e00c9f10dbe7a97cf88f2c74fef52e236c867`.
The exact idempotency key was:

```text
astrid.render:v1:film:head:download:native-a.mp4
```

The builder supplied the normal `rendering.render` body with
`family=rendering.render`, `timeline_ref=film`, selector
`rendering.remotion`, `output_name=native-a.mp4`, empty caller input objects,
the capability-derived output policy/storage estimate, and no inline snapshot.
The test then adds the existing closed `spec.params.canonical_revision`
selector, with exactly these fields: project ID, timeline ID, accepted A
revision ID, accepted A publication receipt ID, and accepted A parent content
digest. It does not add `timeline_snapshot`, `timeline_authority`, provenance,
or a renderer-worker authority field.

Observed native identities in the measured run:

- A revision: `authoring-parent-revision-1cdd30385109bb6cfe48e7fc550fdd5eb356213abda633f0480e8dac2bc7732f`
- A receipt: `txn-6e817be6b617473f92414101f15d7299`
- A parent digest: `sha256:654f4ee6d6adef53de657c6a3469d7202877bb2478cd1f7961d56eb2503ce36c`
- C revision: `authoring-parent-revision-9ba40fe0ae0615c666445c93105457f3e3687e62e164f7951ab10622bd23673b`
- C receipt: `txn-7758ba9d39fb4b0fb43d2b9b288fb3c8`

## Durable proof

1. A is accepted through `capture_move`/`bundle_from_document` and the real
   Runtime-loaded Agent provider.
2. The normal authorized render admission is accepted while A is current.
   Runtime resolves the canonical revision selector, verifies A's receipt and
   digest, and creates one task with a retained CAS snapshot. The task
   authority asserts A's revision, receipt, and parent digest.
3. The admission response is discarded at the caller boundary to model a lost
   acknowledgement. The exact original body/key remains available for retry.
4. A second real Agent-provider move commits C.
5. Runtime is closed and reopened. The exact original `create_task` body/key
   returns the byte-for-byte original admission result: same task, run, spec,
   receipt, and retained A snapshot. The current head is C, and the durable
   store still has exactly one task and one run.

The test keeps `rendering.render` separate from
`rendering.assemble_timeline`; it does not claim a worker claim, decoded
pixels/PCM, export, decoder behavior, or registered-completion restoration.

## Limits and ownership

The existing Agent normal builder does not itself expose the historical
`canonical_revision` selector; the test composes that already-approved
Runtime selector onto the builder's normal body. The remaining RenderRequest
propagation/requester ownership gap is therefore Agent/App requester work,
not a reason to invent a new wire field or inline snapshot. This test uses a
direct Runtime service call and discards its durable response; it does not
claim a real TCP connection drop or browser/outbox integration.

Qualification was bounded and explicit only:

```text
python -m pytest -q tests/test_render_native_historical_retry.py \
  tests/test_render_historical_admission.py tests/test_render_admission_exact_retry.py
```

Central result: **33 passed, 47 deselected in 17.32s**. A local focused run of
the new integration test passed (`1 passed in 1.00s`), and `git diff --check`
passed. No full/broad suite, renderer execution, pixel/audio decode, browser,
schema/API/pin generation, merge, or publication was performed.
