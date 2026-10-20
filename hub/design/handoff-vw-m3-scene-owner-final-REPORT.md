# Scene-only executor and artifact handoff

## Result

APPROVE the existing managed `scene_only` executor and its actual artifact
contract for Agent review/landing. The landable source is the bounded patch
`handoff-vw-m3-scene-owner-final-executor-and-artifact-contract.patch`; it
contains the executor/source-binding guard, its focused unit tests, and the
existing real artifact-contract test. It does not add a Runtime route, DTO,
provider, factory, source-ref field, certificate field, or ordinary SDK claim.

The packet is
`handoff-vw-m3-scene-owner-final-examples/` (17 files, 26,205 bytes): saved
(`committed`), candidate, stale, and unavailable scene answers, each with the
existing managed/nested manifests and bundle, plus the packet manifest.

## Contract to land

- Keep the existing managed invocation: `mode: scene_only`, existing
  `capture_snapshot`/`filmstrip_snapshot`, and existing `filmstrip_bundle`.
- The executor binds labels and `scene_clips` to the verified source that
  prepared Root. It never copies the outer authority metadata map.
- It requests every frame in `range(duration_frames)`, validates exact ordered
  extent and projected compiled IDs, and emits no PNGs or sampled frames.
- Missing, malformed, stale, forged, incomplete, or unavailable binding/query
  produces `snapshot_label.status: unavailable`, label `revision unavailable`,
  empty `answers`, and empty `scene_clips`. The action may still return
  `returncode: 0`: that means the advisory action completed, not that Scene
  answers are usable.
- The ordinary SDK caller must check status, complete frame extent, and map
  binding before invoking `_scene_problems`; it must refuse unavailable,
  incomplete, or stale data even when managed action exit is 0.

Agent should land the executor small unit and implement the already-owned
ordinary SDK caller using the existing managed invocation. Do not introduce a
new DTO, factory, endpoint, or manual tuple activation.

## Evidence boundaries

The two central results are explicitly labeled below. They are admission
doubles using a private copied graph and public Composition 0.0.12 artifact;
they are not live Runtime or ordinary SDK proof.

1. `vw-m3-d1-ready-scene-node-requal-scene-central-owned-suite-retarget-1020175337-12836` — **3 passed in 13.03s**. It covers exactly:
   - `tests/packs/rendering/test_scene_answers.py::test_prepared_host_query_replaces_named_occluder_semantic_presence_positive`
   - `tests/packs/rendering/test_scene_answers.py::test_prepared_host_query_refuses_missing_or_stale_source_pair_and_cleans` (two parametrized cases, hence 3 total).
   It also verified the repaired 21,495-entry graph, pinned Node
   `v20.19.4` (`43d6cf…`), Runtime source `2c4ac180`, and 77-file public12
   extraction before/after.

2. `vw-m3-scene-central-final-venv-run-scene-central-owned-suite-retarget-1020174637-32679` — **18 passed in 76.77s**. It is the same two selected test functions above, with the full bounded scene-central wrapper lane around them (source graph, Root preparation, saved/candidate/forged/stale/unavailable controls, full extent, map/source-label checks, and cleanup). It used the preserved Agent venv interpreter and the same pinned Node/Runtime/public12 graph. The central wrapper is qualification machinery, not an SDK claim.

The artifact-contract qualification is separate and local: pinned Node/read-only
peer graph, `tests/packs/rendering/test_scene_artifact_contract.py::test_scene_only_bundle_is_real_node_artifact_for_saved_candidate_and_unavailable` — **1 passed in 7.68s**. This is UNIT-REAL-NODE with admission fixtures, not live Runtime, ordinary CLI, browser, or full-suite proof.

## D09 status

D09 remains **in-progress**. This evidence qualifies the existing scene-only
executor/source-binding and artifact handoff only. It does not authorize broad
private evaluator/geometry/pixel/statistics deletion, nor does it prove live
Runtime, ordinary SDK, owner-film, or physical parity behavior.
