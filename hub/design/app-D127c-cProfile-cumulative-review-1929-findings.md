# D127c cumulative protected review

## Verdict

SOURCE FAIL. The candidate remains unapplied and the actual mounted element body remains unqualified. The central targeted Runtime test passed, but its helper-shaped fixtures do not establish the App whole path.

## Blocking findings

### D127C-SEL-1 — first protected POST cannot be selected

The candidate predicate in `tests/helpers/p2_commit_phase_capture.py:P2CommitPhaseCapture._profile_body:449`, `_has_element_command:476`, and `_is_element_request:485` requires `commands[0].op == "clip.set-element"` for the exact one-command request. The real mounted path is:

`ElementsLibraryPanel.applyElement` → `element-adapter` → `useTimelineSave` → `commitSession` outbox → `dataProvider.commitTimeline` → Runtime `RuntimeHandler._dispatch` → `RuntimeHandler._timeline_commit`.

The protected App test at `app/tests/e2e/local/three-products.p2-elements-assets.spec.ts:1038-1056` asserts that the first element Apply POST has `commands[0].op == "doc.patch"` and includes a `list.insert`. The same test asserts the later params edit is also `doc.patch` at line 1084, while Undo is `timeline.inverse` at line 1105. Therefore the candidate selector never arms on the intended first element POST. The author and first-return tests use synthetic `clip.set-element` bodies and are not evidence of this mounted seam.

Required minimum diagnostic change: derive the predicate from the actual produced `doc.patch` shape at the first mounted element Apply POST, using only source-backed structural facts (the qualifying single command and its element insertion shape), then consume the one-shot selection there. It must separately reject params edits, Undo, setup, mixed batches, and retries without raw public IDs. No product or request-schema change was made by this review.

### D127C-PROV-2 — handler type and prefetched bytes are insufficient provenance

`P2CommitPhaseCapture._trace_inner:1254-1270` creates a request at `handler_entry` when no dispatch-bound request exists. `_profile_body:449-473` then accepts the handler class, method, route, and manually populated `_prefetched_body`. The candidate test `tests/test_p2_commit_phase_capture.py:test_element_profile_disables_on_handler_exception_without_exporting_exception_text:486-507` directly calls `_timeline_commit` after assigning `_prefetched_body`; it does not enter `_dispatch`.

This can profile a direct handler call that has no actual mounted `_dispatch` prefetch provenance. The required minimum is to require the request state established by the real `_dispatch` path before profiling; the handler-only fallback must not make a synthetic direct call eligible. This is a helper/test seam issue, not a product hook request.

### D127C-TYPE-3 — new scoped mypy diagnostic

`mypy --follow-imports=skip tests/helpers/p2_commit_phase_capture.py tests/test_p2_commit_phase_capture.py` reports a candidate error at `tests/helpers/p2_commit_phase_capture.py:704` because `stats_data.get(callee_key)` is inferred as optional before indexing. It also reports the two pre-existing test-environment import diagnostics for `pytest` and `test_timeline_commit_port`; no other new scoped error was found. The source gate therefore fails the required zero-new-diagnostic rule.

### D127C-APP-4 — strict App validator and activation identity are incompatible

The candidate adds `summary["cprofile"]` in `P2CommitPhaseCapture._summary:1014-1086`. The strict reviewed-new validator in `app/tests/e2e/local/support/p2-runtime-phase-bootstrap.test.ts:304-378` uses an exact summary-key set that has no `cprofile` entry, and its unknown-summary-field control rejects extras. The same validator allows only the existing helper identities; the normal Runtime helper is the prior reviewed hash, not the candidate hash. The D66 source guards in `app/scripts/testing/d66-plain-stack.mjs:226-256` and the App harness require an absolute regular non-symlink helper plus an exact SHA-256.

Consequently there is no App activation credit for this candidate. Accommodating the new summary field and pinning the candidate would require a separate App contract/source change, which is outside this source-only task. The candidate is STOP_UNAPPLIED.

## Independent recheck of earlier findings

- The raw pstats path guard is materially improved: the parent must be a private child of the temporary root, existing parents must be owner-only `0700` non-symlink directories, the profile file uses exclusive creation and no-follow semantics, and the file mode is `0600`; the parent is not chmodded.
- Partial profile enable failure restores the prior `sys.getprofile()` binding in `_start_profile:500-539`; normal return, exception, and `stop()` paths call `_stop_profile:542-560` in `finally`-style cleanup.
- The projection preserves pstats meanings for `ncalls`, primitive calls, `tottime`, and `cumtime`, ranks by descending cumulative time, bounds functions at 40 and edges at 1600, carries dropped counters, and emits sanitized relative file/function fields only. The timing note explicitly says cProfile overhead is not original budget time.
- Added negative controls cover method/path/query, dry-run, unselected handlers, mixed commands, retry consumption, partial enable, symlink/overwrite/private-mode output, and caller-edge counts. They remain synthetic `clip.set-element` controls and therefore do not repair D127C-SEL-1 or D127C-PROV-2.
- The diff contains no product/source/provider/schema edits, no removed parent test functions, and no raw request payload, keys, URLs, locals, exception text, identifiers, or raw stacks in the cProfile projection.

