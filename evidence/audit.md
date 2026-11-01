# M-T-07 Agent Timeline test-deletion audit

## Scope and method

Compared Agent base `3dba04a52a` to released source `2beaa36a` using `git diff --name-status`. The requested filename filter is case-insensitive path contains `timeline` or `skill`, and `test` or `fixture`; it yields **127 deleted paths**. The complete list is in [deleted-paths.txt](deleted-paths.txt); row-by-row mapping and rationale are in [deleted-test-mapping.csv](deleted-test-mapping.csv).

This is a source comparison, not a test run. For representative files, I read the deleted base assertions with `git show 3dba04a52a:path` and retained assertions with `git show 2beaa36a:path`. A candidate is called partial when released tests cover the same broad subsystem but not the removed assertion contract. “Unclear” means a neighboring test exists, but the source assertions/API differ enough that equivalent coverage cannot be established. Fixture-only deletions are no replacement absent a same-purpose retained fixture. **No direct equivalent was established** by the source review.

## Assessment

| Assessment | Count |
|---|---:|
| Direct equivalent | 0 |
| Partial | 52 |
| Unclear | 73 |
| No replacement | 2 |
| **Total** | **127** |

The largest deletion cluster is `tests/sdk/` (89 files). Released SDK tests now exercise a different checkout/transaction API. The retained tree has broad Timeline authoring, editing, CLI, inverse, visualization, and skill coverage, but the removed remote provider/runtime/conformance assertions are not shown to survive as equivalent tests. This is material coverage loss under the project rule against deleting or weakening tests.

## Representative assertion checks

- **Remote commit provider:** deleted `tests/sdk/test_timeline_commit_provider.py` tests `test_provider_accepts_trim_after_move_and_undoes_only_trim`, asserting a trim-after-move commit and undo returning exactly to the moved canonical document; it also tests legacy rebase step metadata. Retained `tests/sdk/test_timeline_transaction.py` instead asserts local checkout edits form a single undo step and exception rollback restores the local document. These are related but do not cover remote provider acceptance/rebase semantics. Assessment: unclear.
- **Public commit session:** deleted `tests/sdk/test_timeline_open_commit_v2.py` describes real native command execution, durable transport, conflict reruns and outbox behavior. Retained `tests/sdk/test_timeline_checkout.py` checks pinned base envelopes and local edit diffs, while `tests/sdk/test_timeline_journal.py` checks journal records/digests. Neither proves the removed transport/conflict/outbox journey. Assessment: unclear.
- **Arrange/occurrences:** deleted `tests/sdk/test_timeline_arrange.py` explicitly preserves shared-shot aliases and exact occurrence ordering/timing, rejects unknown duration and overlap without mutation, and keeps fractional adjacency. Released `tests/sdk/test_timeline_structure.py` tests chapter walls and clip time preservation; it is related structure coverage, not the occurrence arrange contract. Assessment: partial.
- **Native CLI and lost ack:** deleted `tests/packs/timeline/test_cli_native.py` asserts exact native command body, receipt identity, dry-run no-publication, and retry sends identical request after lost ack. Retained `tests/packs/timeline/test_cli_edit_flags.py` covers current edit flags and local checkout editing. It does not assert the removed native wire/receipt/retry contract. Assessment: partial.
- **Runtime clash-back:** deleted `tests/editing_conformance/test_timeline_clash_back_acceptance_runtime.py` exercises a real Runtime peer clash, pending record closure, and publication identity. Released `tests/editing_conformance/test_conformance.py` is only a parameterized scenario runner; the released conformance directory has no named clash-back acceptance journey. Assessment: unclear.
- **Authoring continuation:** deleted `tests/timeline/test_authoring_semantic_continuation.py` checks that a selected-item edit emits `occurrence.fork`, accepts publication, and preserves the sibling/source revisions. Retained `tests/timeline/test_authoring_bundle.py` checks lossless opening/compilation and untouched content preservation, but not the specific fork continuation route. Assessment: partial.
- **Installed skill lifecycle:** deleted `tests/reshape/test_timeline_installed_skills.py` tests installed-wheel skill selection, sync/update/uninstall, idempotence and broken-link scope. Retained `tests/test_skills_sync_registry.py` tests general registry sync/idempotence/foreign-link preservation, and `tests/test_skills_package_data.py` checks default/package behavior. Neither is an installed Timeline skill lifecycle equivalent. Assessment: partial.

## Conclusion

The released line retains substantial adjacent Timeline test code, but the diff removes 127 Timeline/skill-named tests and fixtures without assertion-equivalent successors identified in the reviewed cases. The clearest gaps are remote commit/runtime transport and clash-back journeys, native/sheet command and lost-ack behavior, exact occurrence arrangement, provider undo/rebase, and installed Timeline skill lifecycle. This is a coverage-loss finding for the manager’s merge judgment; no files or refs were changed.
