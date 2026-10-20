# Agent D13 current014 consumer compose handoff

## Composition

Composed the reviewed registered-native producer/requester series from
`tl/agt-m2-d13-runtime-fixture-no-skip` (parent
`tl/agt-m2-d13-real-native-preservation`, review
`tl/agt-review-d13-real-native-final`) onto staged014 Agent pin
`e86f44d04e0a5f183d82d4d1ac307951dd32c44e`.

The port keeps the distinct `rendering.assemble_timeline` family and settled
proposal artifact, freezes the original target and exact child associations in
the requesting client's durable outbox, and commits through the requester's
own authority. GenericHost now rejects legacy assembler admissions, stages
producer identity and verified child reads for native assembly, and no longer
performs the old pre-settlement assembled publication hook. The existing
`publish_timeline_render` client operation remains as a facade for other
consumers; it was not replaced wholesale.

The donor's only fixture correction is present: the native final-render test
uses `tests.helpers.runtime.use_runtime()` instead of an unapproved
environment-based skip. No new skip/xfail was added. P1 authority, F1 staged
inverse, WC4/WC9, Scene/save-core, Root/service, and sprite/plate paths were
not touched.

## Evidence

- `PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m pytest -q tests/sdk/test_timeline_assembly.py tests/sdk/test_timeline_sync.py tests/sdk/test_timeline_sync_native.py tests/packs/rendering/test_assemble_timeline.py tests/packs/video_editing/test_runtime_publication_chain.py -m 'not integration'`
  — **111 passed, 2 deselected**.
- Focused Ruff on the D13 contract/assembly/sync/client files and new tests —
  **passed**. `git diff --check` — **passed**.
- Central `targeted --files tests/packs/video_editing/test_runtime_publication_chain.py`
  — **1 passed, 2 deselected** (default non-integration lane).
- Central `registered-native-render-integration` on this compose tree reached
  both integration tests but failed the Runtime health handshake before test
  logic: Runtime reports schema `sha256:8de823011a121359b9ad021e283b45afb6baeabc8a154a02bd086d1260a8b8f4`,
  while the staged client expects
  `sha256:ce3781c282564b650890456f6c257f3faabe2de3898a84363fecd47e48b30d59`.
- Central `ordinary014-consumer-integration` used exact Runtime
  `/home/user/work/wt/rt-pin-a0dca169` (`a0dca16975dfe8f5e762703b99d9791a16cf7fd7`):
  **1 passed, 1 failed, 1 deselected**. The canonical proposal positive
  passed; the real render/undo positive stopped at the suite bootstrap because
  that lane does not provide `ASTRID_REMOTION_PROJECT_DIR`. No skip or weakened
  assertion was introduced.

The required two-positive real MP4/decode, lost-ACK/restart/exact-retry,
revision-pinned render, and undo proof is therefore **not fully verified on
this composed tree**. It was previously green on the reviewed donor tuple,
but that donor result is not substituted for current-tree evidence.

## Product diff size

Tracked D13 delta: **528 additions / 240 deletions** across 8 files. Two new
files add **293 lines**, for **821 additions / 240 deletions** including the
native assembly module and unit tests. This is a bounded D13 port; no unrelated
current014 paths changed.

## Handoff

The worktree remains uncommitted for the harness. D13 must remain held until
the integration merge and a compatible exact-runtime registered-native lane
re-runs both positive IDs. Recommended next step: align the central suite's
Runtime/client schema and inject the pinned Remotion tuple into the a0 lane,
then rerun the two exact integration IDs before recording D13 as DELETED.
