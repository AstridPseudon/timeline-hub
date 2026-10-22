Both original gaps are fixed at the contract level. **One blocking issue remains: closure-root addressing.**

Reviewed Runtime `0d4c71a3c` and Agent `a086cc6db` on local `tl/integration`. No edits, builds, tests, or network access.

1. **`steps[].reads`: fixed and implementable.** §1 now distinguishes batch-entry reads from sequential step-entry reads, preserves request reads conservatively for every step, and persists declared, captured, and fallback scope dependencies for undo. The two-patch scenario exercises the previously missing dependency and requires rejecting partial undo while accepting grouped undo. This fits the engine’s sequential command execution and separate input/observation captures in [commands.py](/home/user/work/agent/astrid/sdk/timeline/commands.py:193) and [_recording.py](/home/user/work/agent/astrid/sdk/timeline/_recording.py:71). Implementation must preserve those evaluation boundaries rather than flattening dependencies into batch-entry guards, as the amendment explicitly requires.

2. **Provider-generated effects: fixed and implementable, subject to addressing below.** §§2/5 correctly permit authoritative root creation/removal and managed-edge effects while forbidding those forms in submitted patches. They retain native provenance and require authenticated semantic restoration, including redo inheritance. This matches the existing restoration machinery and Runtime’s [inherited-allocation authentication](/home/user/work/runtime/runtime_protocol/timeline_commit_store.py:191). The creation/undo/redo scenario supplies the missing concrete coverage. These are implementation requirements, not claims that today’s provider already supports v2.

3. **Addressing ambiguity: real and blocking.** The [compiler](/home/user/work/agent/astrid/core/timeline/authoring_bundle.py:917) includes the shot identity when generating an internal revision ID, but assigns newly materialized children the parent’s `timeline_id`. Two created shots therefore produce distinct roots both named `internal:film-1`. [Runtime validation](/home/user/work/runtime/runtime_protocol/timeline_commit_store.py:489) requires unique revision IDs, not unique child timeline IDs. The single-child fixture does not expose this collision.

   Adopt this principle: **Every root address must resolve to exactly one physical closure image at its evaluation boundary; entity IDs are shorthand aliases, not sufficient physical identities.**

   Keep `parent` and existing unambiguous addresses unchanged. Permit `internal:<timeline_id>` only when it identifies exactly one reachable child; reject multiple matches with `ambiguous_ref`, never select or broadcast. Add an explicit revision-qualified form, such as `internal-revision:<revision_id>`, for ambiguous roots and provider effects. Apply the same uniqueness rule to `shot:<shot_id>`, since closures also permit multiple revisions of one shot ID.

   Persist resolved bindings, normalize aliases before overlap checks, and follow revision successors only through authenticated materialization/edge provenance during rebase and undo. Never silently retarget an alias. Effect records must distinguish roots across the verified before/after union. Add a two-child creation/edit/undo fixture.

I found no additional independent blocking issue. Historical receipt compatibility and compiler attribution are now explicitly addressed.

VERDICT: CHANGES REQUIRED