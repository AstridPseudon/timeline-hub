Ask: use the bounded duplicate-registry proposal in the existing render row; retain unknown historical cause / Owner: Agent source/qualification; Runtime assessment complete / By: 2026-10-24T03:20Z

Assigned read-only Luna rt-F-render-21-source-review-0303 is complete; full D30 design/runtime-render-21-source-review-0303.md. No code/tests/body/bench/installation runs. Current relevant files equal retained521c source.

Exact current seam: validate_timeline→is_visual_clip_element loads a default ElementRegistry, then resolve_clip_to_artifact_type calls catalog.list_element_ids for effect/animation/transition, which obtains a separate cached registry. Raw registry data cache does not prevent repeated capability assembly. Existing lazy transition guard remains present; emptytimeline0catalog calls, media path incurs duplicate assembly.

Smallest source proposal: derive IDs from the already-supplied ElementRegistry inside resolve_clip_to_artifact_type, preserving exact type/admission semantics and eliminating second assembly. No new cache/guard/trust bypass or pack-authority change is needed by that proposal. This is a current source seam, not established original timeout cause.

Retained original45.005s timeout is in CommandTransport.process.communicate, no Node/npx/Remotion/predicate execution observed; later installed run failed missing runtime_protocol in4.65s, not reproduced timeout. Separate cProfile12.37s _transition_ids probe cannot stand for timed-out call. Original cause stays UNKNOWN. Agent owns any authorized implementation and meaningful installed qualification; no original21/full/renderer repeat is queued from Runtime.
