## F/D69 core triage

Counts: **0 confirmed live regressions · 11 exact decision conflicts · 0 environment · 0 PASS**

Evidence: [evidence.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D69-failures-core-1646/evidence.md)

### Cases

- `tests.core.test_timeline_element_publication::test_d69_upstream_sameclip_exacthead_publication_preserves_closure_and_user_params` — FAIL, `AttributeError` for removed `astrid.sdk.timeline_elements.resolve_admitted_element`; upstream body unchanged, hash `dabf55…`.
- `...::test_d69_upstream_stale_head_and_concurrent_cas_reject_without_rebase` — same traceback; body hash `fa1ae7…`.
- `...::test_d69_upstream_bad_duration_never_publishes[0]` — same traceback; body hash `6cdb38…`.
- `...[-1]` — same traceback.
- `...[inf]` — same traceback.
- `...[nan]` — same traceback.
- `...::test_d69_upstream_unadmitted_owner_and_sourceclip_reject` — same traceback; body hash `a39f82…`.

Current production uses authenticated document reads plus `TimelineSession.submit()` in [timeline_elements.py](/home/user/work/wt/agt-F-D69-failures-core-1646/astrid/sdk/timeline_elements.py:271), not the old resolver/direct publisher. Keeping these exact bodies would require the retired writer, conflicting with D52, G5, and R5.

- `tests.timeline.test_authoring_bundle::test_d66_upstream_approval_is_bound_to_candidate_and_base_revision` — FAIL, `_Writer.__init__()` missing `document`; body hash `3290dd…`.
- `...::test_d66_upstream_frozen_render_restart_then_approval_promotion_is_single_generation` — same constructor failure; body hash `b1761d…`.

The exact bodies require deleted `promote_approved_authoring_candidate` and `publish_parent_composition`. Current authoring publication uses `commit_timeline()` at [authoring_bundle.py](/home/user/work/wt/agt-F-D69-failures-core-1646/astrid/core/timeline/authoring_bundle.py:1855). D52 explicitly retires this helper/writer path.

- `tests.v10.test_timelines_create::test_d66_upstream_remote_create_empty_creates_shell_then_empty_head` — FAIL before old-route assertions: canonical inspection input is absent from the fake writer; current caller invokes `TimelineSession.open()` at [remote.py](/home/user/work/wt/agt-F-D69-failures-core-1646/astrid/sdk/remote.py:537). If supplied, the body then requires retired `publish_parent_composition`.
- `...::test_d69_upstream_remote_create_empty_generates_ulid_when_no_id_given` — same failure; body hash `1411ac…`.

Runtime’s current `create_timeline()` bootstraps the empty head when the commit provider is installed, so this is not counted as environment or a confirmed live regression. The exact bodies still conflict with R5/G5 by requiring the old writer.

### Verification

- Read-only XML/AST comparison: **11 selected, 11 failures; restored bodies equal upstream-924 bodies**.
- `git diff --check HEAD`: **PASS**.
- `git status --short`: **clean**.
- No pytest, collection, HTTP, body, or service rerun performed.

No product or test files were changed. `commit-msg` and `DONE` were created.