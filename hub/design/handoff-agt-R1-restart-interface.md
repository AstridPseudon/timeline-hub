R1 COMMITTED DRAFT 2026-10-22T23:50:21Z
Harness source8a66b1ac88b88ee437e42ba4b7d14ad67930d360 on tl/agt-R1-restart (hub timeline/agent/tl/agt-R1-restart via hub-sync). Independent agt-R1-review now running; U2 merge-forward and Runtime adoption pending. Below is author interface progress with final326+27 test handoff appended; no real Runtime v2/ H3 claim.

# R1 early interface (work in progress)

Worktree `/home/user/work/wt/agt-R1-restart`, branch `tl/agt-R1-restart`.
No commits/pushes by worker. Harness/hub-sync must publish.

Implemented draft in commands.py, commit.py and narrow `_doc_patch*`/`_commit_patch.py` helpers. Authoritative operation schema definitions in `_doc_patch_schema.py`; regeneration: `PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m scripts.gen_doc_patch_schema`. No Runtime edits/pins.

`execute(..., commit_request=request, evaluated_head=head)` populates Plan.steps, Plan.label, Plan.merge_mode. Provider passes request and actual evaluated head and puts those fields under existing prepared.records (no new top-level prepared keys). Commands still have the existing ten recorder keys. Physical binding facts remain in records.commands[].bindings, with ref/physical_ref/revision_id/content_digest/boundary plus key/policy/dependencies; patch bindings additionally contain normalized path, submitted change, and write_range. `steps[].dependencies` is a normalized guard index. `steps[].patch` is provider output, including root turnover and managed edges for semantic/child edits.

Declared reads run at batch/step input. Explicit reads=[] permits field merge; omitted reads with doc.patch produces atomic scopes persisted per step. `rebase_patch` scans verified ancestry and maps native aliases to physical sites; the provider replays original submitted commands on the landing head, not widened generated recorder claims.

R2 integration: patch recorder writes remain ordinary native State addresses, with actual sequential before/after values; physical bindings identify authored sites even where list container writes/projected root turnover are broader. R2 owns inverse.py and step undo. New binding metadata needs its validation/inverse integration. Shared-image patching projects main's independent authoring clones back to one physical shared image, without altering native occurrence semantics.

Runtime home adoption still required: generated command schema/CommitRead definitions; prepared.records label/steps/merge_mode and enriched provider bindings; exposing accepted/preview/history metadata and new merged status; C0c successor/edge provenance authentication. Current Agent tests use DetachedPort (existing Runtime ABI stub), so they do not qualify Runtime adoption.

Initial legacy acceptance lane: 262 passed, 2 deselected, 2 failed (one provider step-metadata retry bug fixed; one missing ASTRID_RUNTIME_CHECKOUT env fixed for next run). Current added patch suite being iterated; no full suite requested.

Final handoff: report.md supersedes this progress note; acceptance 326 passed / 2 deselected, neighbours 27 passed / 21 deselected, scoped lint/type checks passed. Repository gate limitations and cross-lane dependencies are recorded there.
