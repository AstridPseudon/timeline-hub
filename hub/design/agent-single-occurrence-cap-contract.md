Merged Agent tl/integration140e84cc (source5bf1731a), 2026-10-20 12:44 UTC. Independent ACCEPT152targeted/2oldaudioxfails, exact fixture hash and no production changes verified.

# Exact single-occurrence cap contract

Agent preparation/evaluation is resolved with **no product change**. The stored occurrence `duration_ms=4000` is already the normal Agent render cap for the exact original MAIN closure. Authored image hold5/fade_out1 is preserved in the pinned child, while the ordinary projected/serialized clip is hold4/fade_out1 and public12 evaluates f105 to opacity0.5. No next occurrence is present or added.

## Exact inputs and App handoff

Worktree: `/home/user/work/wt/agt-m3-single-occurrence-cap-contract`, base `d8749a9c` (Agent). Candidate6749e542's editor/read and raw diagnostic vectors are retained; its purported production strict xfail is replaced by a real normal-pipeline regression. That xfail sent raw hold5 straight to public `clipOpacity`, bypassing the cap-owning projector, so it was not production join evidence.

The byte-identical captured closure is now:

- Agent `tests/editing_conformance/fixtures/main_image_cap_raw_closure.json`.
- SHA256 **`ad3d0ad35876665489080703c2323a8840c9187428dbe28a913e8ab4ada53f04`**.
- Source: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-main-image-cap-source-vector-raw-closure.json`.
- One `image-occurrence`, shot pin `image-shot/image-shot-revision`, internal pin `image-internal`, parent `image-cap-parent`. Placement start0, duration4000ms, speed1, source_offset0. Child `image`: at0, hold5, fade_out1. No next occurrence, extra cap field, DTO, renderConfig, altered asset or pin.

The complete shared corpus is `tests/editing_conformance/fixtures/visual_compile_contract.json`, schema5, SHA256 **`43783e0f40ef1922b54af855379c8538074c8b1df3a7abd4472a8db93877a484`**. App should copy/compare the raw fixture by its exact byte hash and consume key `single_occurrence_cap_closure`, containing the full actual projected_config, registry, serialized_timeline and expected public observations. No fields are filtered. `cap_fade_closure` remains the explicitly different prepared-editor analog (stored2000ms plus next cut4000ms); it is not evidence for deriving this single-occurrence cap. Existing native A8/B10, overhang, rational30000/1001 and editor projection values are preserved.

## Existing authority and normal path

1. `astrid/packs/rendering/actions/render/managed_timeline.py:1012` `resolve_managed_render_snapshot` resolves an immutable canonical head. `_project_exact_parent_head` at893 reads the pinned parent/shot/internal records and calls the existing `project_runtime_parent_composition` at963.
2. `astrid/core/timeline/shot_composition_projection.py:272` `_occurrence_window` reads placement.start_ms and occurrence.duration_ms. For these exact bytes the occurrence window is [0,4)s. It does not infer duration from child content or another occurrence.
3. The same module's `project_runtime_parent_composition` at454 passes that end into `_project_clip` at291. `_project_clip` uses `clipped_end=min(child end, occurrence end)` and writes hold=visible_duration*child_speed on its detached copy. Here min(5,4)=4, speed1. Effects remain fade_out1; authored hold5 stays intact. The provider also uses this same projector in `astrid/sdk/timeline/commit.py:739`.
4. Normal `validate_managed_render_snapshot` and `materialize_managed_render_snapshot` (at1168) accept/write this snapshot in a private test directory. `_serialize_timeline` in `astrid/packs/rendering/shared/rendering_backend/__init__.py:52` calls `Timeline.load(...).for_render(...).to_json_data()`. Serialized hold remains4; metadata output fps remains numeric30.
5. The actual serialized clips and managed registry enter pinned public Composition0.0.12 `prepareScene`, `queryTrackFrame`, `clipOpacity`. This one-clip/no-transition closure needs no synthesized incoming transition/cap metadata. No second compiler or private fade equation is introduced.

| Public12 result from actual normal serialized output | Value |
| --- | --- |
| own duration / draw duration | 120 / 120 frames |
| frame90 clip opacity | 1 |
| frame105 clip opacity | **0.5** |
| frame119 | layer0 present, clip opacity1/30 |
| frame120 | no layers |
| raw hold5 direct clipOpacity at105 | 1, diagnostic only |

Executable proof: `tests/editing_conformance/test_compile_contracts.py::test_single_occurrence_cap_through_normal_managed_projection`. It starts with the exact hash-checked closure, uses existing `_Runtime` in-process exact reads, executes the real helpers above, compares full direct/managed projections and serialization with the shared fixture, asserts input bytes/objects unchanged, then evaluates those actual output clips using public12 extracted privately. It asserts ordinary success, with no xfail. Existing prepared-editor positive stays positive. The SDK timing compiler needs no change for this defect question; this does not claim the entire one-compiler migration is complete.

## Evidence and limits

Targeted compile/projector/managed/timing/golden neighbors: **152 passed, 2 xfailed**, 9.83s. The only xfails are the existing audio vectors10–11. Public12 normal-host neighbors: **15 passed**, 26.19s. Ruff on the touched Python file: pass. `git diff --check`: pass. Exact commands and preservation checks are in the worker report at `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m3-single-occurrence-cap-contract/notes/report.md`.

MAIN pixels are cited, **not rerun**: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/viewing-main-image-cap-actual-reference.md`, central operation `vw-m3-main-cap-locked-theme-stage-e2e-viewing-main6-locked-theme-image-cap-three-stills-1020115023-5447`, original MAINa411628f, locked Composition0.0.6. Frame90 RGB240 PNG SHA256 `7640face10c33eb4c8682b890ddcc6faacaf0e57c0810e9438e4b2df8a88444a`; frame105 RGB122/124/130 PNG SHA256 `c0b0adc7856e2750137315451a9657661925436746d0da1e9cd6a2527d14431b`; background5/8/20 gives median source-over fraction0.5. Frame119 PNG SHA256 `128017371420be346796916879dc2e5faac0f2761d5025018e392913abea63be` is a quantized near-end control. MAIN metadata duration120 excludes frame120; no nonexistent frame120 PNG is claimed. PNG alpha255 is not layer opacity. The media fixture/reference is a static-public executable analog, not an owner film.

No full suite requested or run; no browser/render/socket/server or live Runtime acceptance. No unified pixel/audio parity or Gate6 closure. Public pure evaluation and host neighbors do not establish render-source admission. Shared dependencies/caches untouched; no installs, git mutation or writes to integration/other worker worktrees.

## Cross-owner App question

`app-main-cap-half-golden.md` reports the exact App counterexample: `shotCompositionTiming.ts:135–143` `timelineOccurrenceEffectiveDurationMs` derives content extent capped only by the next same-lane occurrence. For this one-occurrence closure it replaces stored4000ms with5000ms, producing hold5/f1051/frame120 present. Agent's normal path above instead uses the existing stored4000ms authority. That difference is established by the App report plus executable Agent proof, not a reason to invent a cap in Agent or activate renderConfig.

Orchestrator was asked to assign App policy reconciliation against these exact bytes while preserving its original stored2000ms/content5000ms/next4000ms → effective4000ms editor positive. A blanket min(stored,content) change would violate that original positive. No cross-owner App edit or policy guess was made here. Agent task is complete; App reconciliation remains an external follow-up unless already assigned by the orchestrator.
