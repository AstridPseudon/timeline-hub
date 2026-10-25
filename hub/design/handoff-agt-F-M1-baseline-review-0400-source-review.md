# F-D86 source review

Verdict: `PASS_SOURCE`.

## Scope and source identity

- Candidate: `11d043cd488283712082429652c46d05a730426c`
- Parent/base: `f51844083737a...` (`tl/integration` as captured by the dispatcher)
- Changed product file: `tests/editing_conformance/test_commit_runtime_m1.py` only.
- Candidate blob: `23451aa80279f47d126e5e5699f51272b8a6418402ba559617c243bcd6b15041`
- Parent blob: `aad40f65c3fec32468bbe99f4b328d02a4cd9497e59debdd138265bc0a042545`

The source fixture is the captured `precut-v31.tar.gz` film baseline, not a
synthesized or empty target. The archive hash is
`e304773208ff96cea0dca545c69cfa3fcb7ef605c01c306017ed8bcfc654a6b5`; its
manifest hash is `1ce7480bc157194730d1e9c937d99090cb8b21986428139f18d55cfc4fa988e4`.
`build_film_fixture` restores two independent captured roots and pins the
original project, timeline, parent revision/publication, media, transcript,
and text-binding IDs.

## Before/after setup trace

The pre-migration M1 setup read the parent composition from the same captured
film timeline and applied the following exact changes before publishing:

1. append track `music-other` (`kind: audio`);
2. set the first clip's `app` to the `word:word-1` anchor, `until_film_end`,
   `fixed_start: false`, `for: 5.5`, and opaque `[None, {"keep": True}]`;
3. append the `music-other` audio clip with `at: 0`, `hold: 5.5`, and the
   same opaque extension;
4. mirror `config.clips` from `clips`.

The candidate retains those mutations byte-for-byte in the same fixture
purpose. Its source call trace is:

`build_film_fixture` -> `RuntimeService(source_fixture.duplicate_root)` ->
registered `load_timeline_commit_provider("astrid")` ->
`_timeline_commits()[0].revision_closure(project_id, timeline_id,
parent_revision_id)` -> `bundle_from_document` -> `emit_document_commands`
against that same source bundle -> `get_project_timeline(project,
source_fixture.timeline_id)` -> `service.commit_timeline` with the exact
current base revision/publication, C0 `commands`/`steps`, `merge: atomic`,
`reads: []`, `dry_run: false`, `source: {"via": "python"}`, the existing
idempotency key, publisher `owner`, and the registered provider route.

The returned fixture changes only `parent_revision_id` to the accepted
revision. Root, project, timeline, media, transcript, text-binding, and all
other captured pins remain unchanged. This removes the failed intermediate's
empty `m1-journey` target and its synthetic ID remapping; it does not replace
the journey with unrelated input.

## History and assertion review

The only test-body assertion change is:

`base_history["items"][0]["intent"] == "bootstrap"` ->
`base_history["items"][0]["intent"] == "legacy_unknown"`.

The captured legacy publication actually stores `intent: legacy_unknown`,
with `records: None`; `bootstrap` is reserved for the exact empty bootstrap
installation. The candidate keeps the two-entry count, baseline receipt,
chronological item order, later `recorded` entry, and all subsequent exact
history/receipt predicates. This is source-backed and stronger than a
count-only or union assertion; no historical-source exemption is used.

All other test bodies, decorators, parameters, refusal expectations, retry
keys/bodies, inverse/redo predicates, and no-write/read-only guards are
unchanged. Static AST comparison found the three other test bodies identical
and the first body differing only at the literal above.

## Consumer accounting

The ten M1 selectors covered by this fixture are:

- `test_cli_python_outbox_restart_and_guarded_inverse[disjoint-rebase-undo]`
- `test_cli_python_outbox_restart_and_guarded_inverse[touched-basis-conflict]`
- `test_keyed_view_lost_ack_restart_and_fresh_head`
- `test_keyed_view_requires_write_but_inspection_remains_read_only`
- `test_normal_client_auto_placement_preview_restart_retry_inverse_and_redo`
  for `anchor-image`, `anchor-video`, `fallback-image`, `fallback-video`,
  `shared-image`, and `shared-video` (six selectors).

The required 23-consumer accounting is 10 M1 + 6 D87 frontend/checkout
selectors + 6 owned-move/publish selectors + 1 scalar family dependency.
The D87, owned, and scalar files are not changed by this candidate and are
not being claimed as newly qualified by it; their original predicates remain
outside this one-file setup migration. The candidate's M1 setup preserves the
shared scope/graph/physical roots, legacy reference, transcript and binding,
media IDs, opaque/timing values, durable history, retry/idempotency, refusal,
inverse/ABA, and no-write purposes relied on by the accounting.

## Static checks

- Candidate and parent Ruff via stdin: `All checks passed!` for each.
- Parent scoped mypy: `Success: no issues found in 1 source file`.
- Candidate AST parse/compile and in-memory body comparison: passed.
- `git diff --check 11d043cd48^ 11d043cd48`: passed.
- Candidate mypy was not run because mypy does not accept stdin and writing a
  candidate copy into the worktree was prohibited by the source-only brief.

No pytest, collection, helper/fixture/function execution, services, probes,
full suites, browsers, package installs, or render work was performed.

Non-blocking documentation note: the retained comment near the fixture still
mentions a “new bootstrap-created target”; the code now uses the captured
existing timeline. It does not change the source call trace or behavior.
