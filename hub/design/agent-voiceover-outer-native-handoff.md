# Agent outer voiceover native handoff

2026-10-20. Bounded result: **BLOCKED by missing authored command carriers**.
No Runtime contract decision is reopened. No product code, pack declaration,
schema, permission, generation intent, pin, endpoint or requester implementation
was changed. The original outer authoring test double remains, explicitly
unqualified. No outer settlement/requester success or WC5 retirement is claimed.

## Source

Worker: `agt-m2-voiceover-outer-native-producer`.
Base commit `9c8a38e067ce5ba14612c2179abc89fb5487ddb3`, base tree
`83f16e907286f0a33b92a15a9df42277b4188264`, inherited from
`tl/agt-m2-speech-claim-fixture-repair`.
Only added source file:
`tests/packs/video_editing/test_outer_voiceover_native.py`.

Required tuple retained without overrides:

- Normal generated client contract `0.2.14`, schema
  `sha256:ce3781c282564b650890456f6c257f3faabe2de3898a84363fecd47e48b30d59`.
- `runtime.lock.json` source `a0dca16975dfe8f5e762703b99d9791a16cf7fd7`,
  producer `sha256:f021e7714c1b40011b69ba624d288c217749d58013b8adf0352d283854f20fa0`.
- Integration daemon explicitly uses `ad97e16effc53fa13f91c43f076f6edb3c38985f`
  through the existing Runtime archive locator.
- Shared environments were read-only. No dependency installs or cache writes
  into shared environments. No full suite and no duplicate inner WAV cases.

## Actual fixture counterexample

The new bounded probe imports the existing `fixture` and `synthesis` from
`tests/packs/video_editing/test_draft_voiceover.py`; it does not replace their
expectations or add a snapshot writer. With changed first script text
`Long new narration`, `prepare_draft_voiceover(..., timing_policy='ripple',
padding_seconds=.15)` produces the original successful intent:

| Existing original assertion | Exact required outcome |
| --- | --- |
| First placement duration | 3000 -> 4150 ms |
| Second placement start | 3000 -> 4150 ms |
| First still hold | 3 -> 4.15 seconds |
| Narration source end | 2 -> 4 seconds |
| Spanning parent hold | 6 -> 7.15 seconds |
| Parent config duration | 6 -> 7.15 seconds |
| Shot draft provenance | text/digest/settings/new audio/run/task/base-head record at `payload.metadata.draft_voiceover` |
| Detached safety | Original first placement remains 3000 ms |

The strict positive xfail attempts `capture_shot_set` using the exact prepared
provenance. Existing `ShotSetArgs.values` accepts only `name` and bounded
`settings`, with `additionalProperties:false`; it rejects `metadata` before
execution. The test retains the intended successful capture and resulting
metadata assertion, with `xfail(strict=True, raises=CommandError)` naming WC5.
No original passing behavior test was changed, skipped, weakened or removed.

This is a decisive missing carrier even for preserve timing. Further existing
source limits prevent a complete lowering:

- `astrid/sdk/timeline/_media_inputs.py:_verified` accepts only image/video;
  exact Runtime-verified `audio/wav` is rejected. A readable WAV and five-field
  media selection do not themselves authorize an edit.
- `native_occurrence_media_commands.py:_clip` requires a visual child track;
  the fixture's narration is on an audio track. `clip.add` only admits parent,
  non-media clips. Neither is an audio insertion workaround.
- `clip.set` exposes only hold set and bounded clears; it cannot replace the
  existing direct-media selector or set the source window.
- `shot.set` cannot write the required draft provenance, payload asset/item
  mirrors, or an internal registry binding. `clip.set-params` targets clip
  params and cannot serve as shot metadata.
- No installed command writes the existing occurrence's duration or the parent
  config duration. `placement.move` moves a raw clip inside its owner, not the
  occurrence's parent placement. Duplicate/delete cannot preserve the exact
  existing occurrence identities while changing those fields.
- `timeline.inverse`/`timeline.restore` consume accepted history/revisions;
  they cannot import a newly synthesized candidate. `producer.guard` records
  verified authority and has no authored writes.

Changing the five-field pin, using a bare digest/latest lookup, dropping
provenance, moving metadata to params, relabelling audio as visual, inventing
accepted history, or comparing snapshots to emit arbitrary writes would not
preserve this authored result. All are excluded by the settled brief.

## Identities, custody and authority

Outer: registered executor **`video_editing.sync_draft_voiceover`** from the
actual video_editing pack and GenericPackHost discovery/preflight/registration.
Inner: **`generation.generate_speech`** remains a separate executor identity.
There is no declared child_delegation/local_orchestrator relation on the outer
action; call nesting does not establish a Runtime parent-child relation.

The existing outer action returns only report/receipt and currently calls the
legacy bound authoring interface. It has no declared file output
`authoring_proposal` and does not settle the closed six-field D13 artifact.
Adding that declaration alone cannot produce missing command meaning.

The admission test records ordinary SDK `invoke(..., kind='executor',wait=False)`
and its actual retained spec. It then separately exercises the existing open
spec target carrier through normal `client.tasks.create`, with exactly
`runtime_dependencies.publication.admitted_target` containing project, timeline,
original revision and original publication, and exactly ordered
`execution_request.inputs` / `input_object_ids`. This second task is a queued
carrier-retention diagnostic, not a native producer result. Its ingested
script.txt bytes prove managed object custody only, not authoritative timeline
script selection. No new `script_pins` field is introduced.

Neither diagnostic task is executed, claimed or settled; both are cancelled
through the normal owner API. There is no outer attempt pin or settled proposal,
and no inner task is started by this investigation. The previously qualified
inner managed WAV/selection/provenance tests are unchanged and are not rerun.
Their success cannot stand in for an outer producer pin.

The integration negative submits to the existing commit door with the real
worker credential and asserts HTTP 403 plus unchanged accepted history. No
requester credential is lent to a worker. The request's empty command suffix is
intentional: authorization must refuse before edit validation, and it cannot
masquerade as a substitute voiceover proposal.

Once a carrier is authorized and implemented, use only the existing D13 codec:
`commit._digest` over the full proposal minus its own digest, declared durable
`authoring_proposal` artifact, exact outer five-field attempt identity and
original four-field target. Requester `TimelineSession.queue_proposal` owns the
outbox and commit. Producer output never gains commit authority. This worker
adds none of those product steps because the mandatory command lowering is not
available within its allowed scope.

## Validation

Local bounded command (no sockets):

```sh
env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/packs/video_editing/test_outer_voiceover_native.py::test_outer_fixture_still_requires_audio_provenance_and_ripple tests/packs/video_editing/test_outer_voiceover_native.py::test_outer_fixture_provenance_can_be_captured_without_a_snapshot_writer tests/packs/video_editing/test_draft_voiceover.py tests/sdk/test_timeline_producer_guard.py
```

Result: **41 passed, 1 xfailed**, 4.85 seconds. The entire existing voiceover
unit file is unchanged, including all original22 readable-audio/RIPPLE positives
and the inherited speech-admission addition. Existing producer guard/outbox
neighbors pass. A focused `-rx` rerun confirms the strict xfail reason above.

```sh
env PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m ruff check --no-cache tests/packs/video_editing/test_outer_voiceover_native.py
git diff --check
```

Result: PASS.

Central admission/authority result and snapshot tree: pending. The initial test
request `1020202335-31688` was rejected by the service before pytest because
`--files` forbids `-s`; it executed no tests. The replacement uses only one
explicit node, with captured trace output enabled by the test fixture.

## Next bounded decision for the orchestrator

Authorize the owner of the existing command registry to supply the missing
lossless audio/provenance/ripple carrier, or explicitly keep WC5 blocked.
There is no evidence that the settled D13 custody/authority design is wrong.
Do not restore a legacy writer or broaden this worker into a new framework.
After a real exact lowering exists, declare the proposal output, implement the
owned producer/session adapter, place the worker authority negative first,
freeze source, then run one real outer settlement -> requester/outbox case on
the exact tuple above. Keep original22 expectations and verified WAV selection.
