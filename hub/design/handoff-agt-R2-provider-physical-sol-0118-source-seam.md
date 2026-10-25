# R2/F-D86 physical provider source return

Verdict: **STOP_UNAPPLIED**. No repository source, test, fixture, helper, or Git metadata changed. There is no mergeable candidate or newly authored regression. Static checks are not functional qualification.

## Scope and identities

Read PLAN section 3, worker agt-F-provider-custody4-0100's report, worker agt-R2-provider4-source-seam-0107's report and absolute evidence/source-seam.md, and the D86-provider-custody4 section of the orchestrator's design/agt-D86-main-families.md (lines 220–228). Its exact scope is **three test functions / four parameterized nodes**, not an assumed eleven-node subset:

1. tests/sdk/test_timeline_commit_provider.py::test_restore_undo_redo_exact_full_closure_and_unknown_fields
2. tests/sdk/test_timeline_commit_provider_add_delete_runtime.py::test_native_add_delete_one_publication_inverse_redo_restart_reservations[net-zero]
3. tests/sdk/test_timeline_commit_provider_add_delete_runtime.py::test_native_add_delete_one_publication_inverse_redo_restart_reservations[replace-existing]
4. tests/sdk/test_timeline_semantic_reservations.py::test_aggregate_children_are_retired_in_their_occurrence_scope

Base HEAD: 219b9ca8b196bcf4ee6fda6e08c2e50ae251ae4b. Base and unchanged worktree tree: 9d26efc30836abb7ae3a19882e6e917405db2f89. Source-manifest.json contains SHA-256 hashes for the four scoped files and thirteen directly inspected dependencies, each compared byte-for-byte to HEAD. The three test hashes also equal both previous workers' hashes. The brief's abbreviated 7c48 was ambiguous; read-only comparison against the dated carrier merge 7c485e5b61 shows no inverse.py or commands.py difference. No refs were changed.

## Historical observations, corrected failure stage

Read the original rehearsal XML, without executing it:

/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-core-rehearsal-2234/evidence/OWN-REHEARSAL-SUITE.xml

Historical-targets-and-controls.json records its hash, the four exact failure texts, and sixteen passed comparator nodes. These are historical outcomes only. Current outcomes are unknown.

* Full-closure restore: **redo**, provider test line 1008, fails at inverse.py:1021. The restore, first undo and equality of the first undo's complete canonical document to `changed` already passed. The previous report's shorthand “restoreundo” must not be interpreted as failure of that first undo.
* Aggregate child retirement: **redo**, semantic-reservations test line 94, fails at the same guard. Equality of the first undo to the introduced complete canonical document already passed.
* Net-zero: the first undo's reload equality passed. The first inverse-record writes equality (line 148) failed because the actual first write is absent-to-present with the full literal row. The XML diff is truncated; it does not establish every returned field. The `created == []` assertion at line 149 was not reached.
* Replace-existing: first undo fails at the explicitly excluded Runtime native-write/effect-image auth boundary. No Runtime source was changed, no denied route was invoked, and no alternate admission path is proposed.

Passing comparator nodes in that XML: ordinary restore preview/digest/race (one), retained transcript/config restore inputs (two), native parent clip-delete reload/undo/redo with retained pins (six), retired native identity reuse refusal (two), seeded deletion retirement (two), aggregate removal retirement (two), and introduced-and-deleted child retirement (one). Their exact parameter spellings and outcomes are in historical-targets-and-controls.json. They do not qualify the four targets.

## Concrete Agent producer/verifier mismatch (source inference)

The two redo failures have different authored graphs. The shared source-level mismatch below does not depend on equating those graphs or inventing source images:

1. DetachedRealm.context at provider-test lines 88–101 submits native commands without label/steps/merge/reads. CommitPatch.__init__ at _commit_patch.py:262–263 therefore sets `v2` false. This is an existing supported native path, not evidence of a malformed physical fixture.
2. apply_inverse preserves native stage groups and appends their `inverse.stage` binding at inverse.py:1173–1181. CommitPatch.finish associates the corresponding `effect_range` at _commit_patch.py:559.
3. CommitPatch.finish at _commit_patch.py:595–611 emits `commit.effect` bindings for an inverse with stages **even when v2 is false**. At lines 617–622 it also emits input `commit.materialization` bindings for those same legacy inverse stages because `not self.v2` is true. Lines 658–675 show these bindings carry exact physical source/successor, owner, managed edges, step, and boundary.
4. On redo, _managed_boundaries at _commit_patch.py:752–764 identifies the stage's effect-range segment. _materialization_sites at lines 978–981 treats that segment as effect-bound because commit.effect exists. It verifies the exact effects and any materialization proof it encounters, but at lines 1119–1122 it **does not append stage transitions** unless `include_inverse_stages=True`.
5. _validate_materializations at inverse.py:1007–1010 uses the default false flag, so those stage transitions cannot enter `expected`. Lines 1013–1022 nevertheless require every persisted commit.materialization tuple to occur in that expected multiset. A legacy inverse containing both kinds of proof is consequently rejected on redo as unexpected. The retained traceback is consistent with precisely this producer/verifier disagreement.

This is a source-supported explanation, not a fresh behavioral reproduction or proof that no other issue remains. The XML's abbreviated record repr does not expose every actual binding tuple. The prior reports did not trace the producer's legacy/v2 conditions or the transition suppression; this return supplies that missing causal seam.

There is no justified fixture correction that changes a shared image, drops opaque data, replaces the native capture, or changes source authority. Adding v2 controls solely to avoid this legacy inverse path would change coverage and route around the failure; it is not proposed.

## Binding scope stop

The brief makes accepted-history verification/history integrity read-only, prohibits making generic fork validation more permissive, and ends with “no sourcefix.” Its conditional instruction is to stop unapplied if a repair would change that seam. The concrete repair choices reach that boundary:

* changing _commit_patch.py's emission/association of persisted materialization proofs widens beyond owned inverse.py and the three tests; or
* changing inverse.py:_validate_materializations or _commit_patch.py:_materialization_sites changes accepted-history verification.

Neither is applied. Merely setting `include_inverse_stages=True` at inverse.py:1008 is **not** a safe bounded correction: v2 inverse stages legitimately use effect proofs without an additional materialization binding, so unconditionally requiring all stage transitions as materializations could introduce the opposite incomplete-proof refusal. Dropping unexpected bindings, filtering accepted history, accepting equal payloads, or bypassing validation would weaken integrity. No such patch or workaround was authored.

The source-only follow-up needs orchestrator allocation of this exact producer/verifier boundary. The eventual owner must preserve exact sources, digests, ordered owners, owner/managed-edge provenance, boundary/step/ordinal association, uniqueness and missing-proof refusals. Keep Runtime, D88, ABI policy, accepted history data and source custody untouched.

## Net-zero expected recorder facts (unapplied proposal)

Source is more specific than the historical truncated diff. apply_inverse at inverse.py:1136–1190 deliberately executes reversed native commands and reversed writes; its comment distinguishes landing coalescing from execution. _restore_write at lines 919–940 restores the deleted row via Recording.create(restoring=True), then reverses the original creation via assign(ABSENT). Recording.assign at _recording.py:121–132 appends every edge. Recording.create at lines 155–179 retains a typed `created` fact even during historical restoration. Hence the source-supported expected **native** write list for net-zero undo is:

```python
[
    {'ref': ref, 'path': [], 'before': ABSENT, 'after': present(row)},
    {'ref': ref, 'path': [], 'before': present(row), 'after': ABSENT},
]
```

The native `created` fact is `[created]`, the same typed identity already asserted by this test at lines 104–105. This records historical restoration, not fresh ID allocation permission. The source predicts the same native pair for redo of that pair. This is an inference, not an observed current redo result.

A future D83-reviewed expectation correction should assert that exact full native list and typed restoration fact, **and** retain the original net-zero predicate as exact coalesced absent-to-absent equality. Preserve all existing identity-collision/refusal and no-history-change assertions so restoration never grants ordinary reuse. Do not project or truncate the native recorder to satisfy the old assertion. C0 at commit-v2.md:437 explicitly retains native allocation/restoration provenance alongside effects, and its undo section at lines 1595–1619 requires sequential stages and original authenticated allocation authority.

This replaces two existing predicates, so it must be presented explicitly for D83 same-or-stronger review rather than falsely claimed as identical AST conservation. This run did not obtain a full current authoritative record (test/fixture execution forbidden); it therefore does not invent an exact full-record equality, new acceptance corpus, bindings, receipt or source image. No expectation was changed.

## Predicate and fixture conservation

predicate-conservation.json inventories every original assertion and raises context in the three whole files, with source and AST, and all top-level decorators. Entire baseline/candidate module ASTs and bytes are identical, which also preserves fixture bodies, branches, opaque literals, imports, helper calls, parameters and original physical source identity.

For the exact three source functions: full closure has six assert statements; parameterized add/delete has twenty-eight assert statements and three raises contexts (including nested helpers); aggregate retirement has four assert statements. Add/delete retains both True/False inputs and the exact ids net-zero / replace-existing. These counts describe source statements, not separately executed assertions or collected tests.

Retained checks include full canonical closure equality, unknown parent/shot/internal/occurrence/registry/config/manifest values through the original unchanged fixtures, native command claims, publication cardinality/history prefix and immutable original records, exact idempotent retry, renderer/legacy-writer tripwires, no identity reuse before/after undo/redo/restart, intervening-write refusal with unchanged history, and retry tripwires forbidding re-execution/reservation checks. No passing behavior was changed into a refusal, xfail or skip.

No new regression was authored because the protected repair was stopped. The minimal future focused regression should use genuine provider output from the unchanged full-closure or aggregate fixture, explicitly prove the accepted legacy inverse carries both effect and materialization bindings, then assert preview/no-write and accepted redo closure equality; run it alongside the existing whole/step fork-proof tampering controls. This is a proposed regression requirement, not an existing selector or coverage claim. Existing selectors for the four originals are listed above; the independently existing protected controls are tests/sdk/test_timeline_inverse_fork_guard.py::test_fork_materializations_require_complete_unique_authenticated_edges and ::test_missing_fork_binding_fails_closed_before_equal_clear_inverse. Preserve their complete damage/whole/step/preview matrices.

## Static evidence and proposed existing-log entry

No pytest, collection, test/helper/fixture execution, test service, build, browser, render, probe, sockets, source custody or Runtime auth work ran. Only standard-library source/XML analysis and the explicitly allowed static tools ran.

* `python3 /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-provider-physical-sol-0118/evidence/check_static.py`: PASS baseline/candidate AST/bytes/in-memory compile, four scoped files.
* Ruff baseline/candidate: PASS, exit 0, four scoped files, repository pyproject configuration and `--no-cache`. Exact commands/output are in ruff-baseline.txt and ruff-candidate.txt.
* Mypy baseline/candidate: both exit 2 with byte-identical NumPy __init__.pyi:737 Python 3.12 syntax diagnostic under the repository's Python 3.11 target. Checking aborts before useful target checking; this is not a typecheck pass. Baseline uses actual HEAD source via --shadow-file; candidate uses the unchanged worktree; independent caches live only under TMPDIR. Exact commands/output are in mypy-baseline.txt and mypy-candidate.txt.
* `git diff --check`: PASS. `git status --short`: empty. No candidate patch or test result is claimed.

Proposed update to the **existing** D86-provider-custody4 entry (not written to a shared ledger): “R2 physical source return STOP_UNAPPLIED at Agent219b9ca8: two historical redo failures trace to legacy inverse dual proof emission vs stage-transition suppression; protected accepted-history verification boundary needs explicit allocation. Net-zero native recorder expectation is coalesced rather than sequential; exact correction proposal retained for D83 review. Replace-existing remains separate Runtime auth ownership/D88 STOP. Four original selectors and all predicates unchanged. Static AST/compile/Ruff PASS; mypy environment-blocked with identical baseline/candidate diagnostic. No current functional qualification; no mergeable candidate.”

Next steps: orchestrator reviews this exact stop finding and assigns the producer/verifier seam if permitted; a separately authorized source candidate then gets one independent protected review and MAIN candidate functional qualification before any core product merge. A fixture-only correction still requires fresh protected review and incremental proof. This worker dispatches neither review nor tests.
