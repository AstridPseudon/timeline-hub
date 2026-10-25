# R2 three-body profile/route review

## Result

**PASS — source facts are sufficient.** The authentic D108b Composition `0.0.14` profile is exact and genuine on the Agent venue, but its required directory is absent on MAIN. The existing local `0.0.13` profile is a different lock/archive/registry tuple and cannot substitute. The three ordinary cases do not need Composition, Node, rendering, or a profile; their profile requirement was inherited from the full-core D73 harness.

This is not a D73 full-core execution clearance. D108b's MAIN waiver covers one full-core run only. The owner must choose the venue for these three cases.

## Exact current path and inputs

The existing production route is:

```text
POST /v1/projects/{project_id}/timelines/{timeline_id}/commit
Idempotency-Key: <scenario key>
```

The server passes the exact route path to Runtime `commit_timeline`; Runtime checks the path, scope, schema, authorization, and existing commit engine. The Agent client targets the same route and header. The source-proven direct non-render fixture uses `RuntimeService.commit_timeline(..., invocation_path=route_path(...), authorize=...)` after registering `agent.create_runtime_commit_service()`.

Use the exact ordinary source tuple: Agent rebound `44cfb2884e9ee918ba3ea19e354aeba31dfd2347` and Runtime `1daca2a33f6d7b10053e07c539a54843e3984e19`, with these selectors:

1. `tests/editing_conformance/test_word_binding_recipe.py::test_last_write_clear_undo_restore_and_restore_inverse`
2. `tests/editing_conformance/test_word_binding_recipe.py::test_follow_rebases_original_choice_after_source_move_and_reorder[True]`
3. `tests/editing_conformance/test_word_binding_recipe.py::test_stale_anchor_refuses_when_intervening_window_excludes_selected_word`

The current central suite has no exact-three row/body. Adding or selecting an owner-authorized existing venue is outside reviewer permission; no new framework or automatic gate is proposed.

## Profile facts and true input limit

D108b records the genuine full-core profile as directory `agent-remotion-v3-819acf-1110`, installed Composition `0.0.14`, profile lock SHA-256 `f4fc0a32a8822e956dfa21ff35d19c0c83d147c754cdb3546f91c84e330be18d`, selected archive SHA-256 `819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234`, and registry-state SHA-256 `d609b44b37d724358a33405e9d8539008fd1ac30bc2f0d9746575c3fbadaac96`. That directory is absent on MAIN. The existing `agent-remotion-0013` tuple is not equivalent, and no renamed or partial profile was accepted.

For the exact three ordinary cases, the true input limit is the exact Agent/Runtime pair and the normal Python/schema environment; no Composition profile is an input. For a D73 full-core run, the existing launcher still requires the authentic profile directory, `node_modules`, lock/archive/registry hashes, Node version, schema, and Composition version. Those declared guards remain unchanged.

## C0 request/reply preservation

The owner-run request must retain the existing C0 fields and semantics: exact project/timeline scope, exact base revision/publication pair, non-empty ordered commands, producer label, steps with IDs/labels/intent/tags/command ordinals/patch and reads where applicable, merge mode, reads, dry-run, and source. Accepted/merged replies must remain canonical and include the existing receipt/head, effects, bindings, dependencies, normalized commands, steps, merge, and publisher data. Conflict, invalid, and dry-run behavior remain unchanged.

## Reviewed options

- Owner-approved ordinary venue: run only the three selectors on the existing normal Agent/Runtime commit path above, retaining all existing guards. This is the preferred exact input route if the owner authorizes an existing central row.
- Existing D73 venue: first provide the authentic profile tuple through the normal approved provisioning path, then run the unchanged D73 launcher.
- Do not initialize or resize bench storage, copy/rebind environments, use `0.0.13`, use a partial/renamed profile, alter source, or add a collector/probe/service/body workaround.

No service/body/test run was made in this review. The profile absence blocks only the existing D73 full-core route on MAIN; it does not establish a profile requirement for the three ordinary production paths.
