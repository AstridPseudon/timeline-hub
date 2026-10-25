# F-D86 D107 source-qualified receipt — 0721

Status: `SOURCE-QUALIFIED / BEHAVIOR-PENDING`. This handoff records the one
authorized D107 source receipt. It does not authorize a merge, a test run, an
effective retirement, or behavior closure.

## Scope and decision

- D107 is the exact original M1 baseline ten (`M1-baseline10`) from
  `handoff-agt-M1-scope-0610-selectors.tsv`. All ten original selectors and
  `tests/editing_conformance/test_commit_runtime_m1.py` remain untouched.
- The original source is legacy-only because its historical word association
  and source/head cannot be recreated by current setup without changing
  authoritative inputs. The current equivalent is a separate NEW-OURS source
  candidate, not an edit or reclassification of the original ten.
- This receipt does **not** retire the ten original tests, close D107, or
  confer functional proof. Final effective retirement/closure awaits release
  of current dependency `2154168d308bdf5b0903d150cd3855765685f92f` and
  meaningful MAIN outcomes, including the independent D108 full-core
  terminal. Product `2154168d` remains HELD; candidate `2e3331ee…` must not
  merge or run before that release and terminal gate.
- The original M1 source has no ABA tail. Genuine separate ABA tests remain
  unchanged and are not claimed as combination proof. D100 and D110 remain
  separate scopes.

## Exact original ten and replacement mapping

The following membership and purpose mapping is copied from the authorized
`handoff-agt-M1-scope-0610-selectors.tsv`; no alias or new original selector
is introduced.

| Scope | Exact original selector | Original source outcome | Purpose preserved | Replacement/current source mapping | Disposition |
| --- | --- | --- | --- | --- | --- |
| M1-baseline10 | `tests/editing_conformance/test_commit_runtime_m1.py::test_cli_python_outbox_restart_and_guarded_inverse[disjoint-rebase-undo]` | `ERROR setup: legacy word anchor is missing` | accept CLI move; lost ACK; dependent outbox; restart; exact idempotent retry; disjoint rebase; inverse; history/readback/no-write | Current equivalent: `tests/editing_conformance/test_m1_current_equivalent.py::test_new_ours_current_equivalent_preserves_m1_commit_journey[disjoint-rebase-undo]`; current provider/runtime restart/retry/undo are statically mapped, not executed | Original remains unchanged; source mapping held pending behavior |
| M1-baseline10 | `tests/editing_conformance/test_commit_runtime_m1.py::test_cli_python_outbox_restart_and_guarded_inverse[touched-basis-conflict]` | `ERROR setup: legacy word anchor is missing` | preserve touched-basis conflict; pending command; exact base pair; refusal and no-write | Current equivalent: `tests/editing_conformance/test_m1_current_equivalent.py::test_new_ours_current_equivalent_preserves_m1_commit_journey[touched-basis-conflict]`; current doc.patch/C0 conflict and ABA tests remain separate | Original remains unchanged; source mapping held pending behavior |
| M1-baseline10 | `tests/editing_conformance/test_commit_runtime_m1.py::test_keyed_view_lost_ack_restart_and_fresh_head` | `ERROR setup: legacy word anchor is missing` | view lost ACK; restart; exact key replay; changed-body idempotency conflict; fresh head | Partial current selectors: `tests/test_timeline_native_inspection.py::test_view_write_authority_and_key_before_any_persistence`; `tests/test_timeline_native_inspection.py::test_view_retry_keeps_original_revision_after_head_advances`; `tests/test_timeline_native_inspection.py::test_daemon_generated_client_without_executor_catalog` | Partial foundation only; exact historical combination remains pending |
| M1-baseline10 | `tests/editing_conformance/test_commit_runtime_m1.py::test_keyed_view_requires_write_but_inspection_remains_read_only` | `ERROR setup: legacy word anchor is missing` | read-only view refuses without persistence; inspection remains readable; writer accepts same view | Same exact Runtime view selectors above; no combined M1 claim | Partial foundation only; original remains unchanged |
| M1-baseline10 | `tests/editing_conformance/test_commit_runtime_m1.py::test_normal_client_auto_placement_preview_restart_retry_inverse_and_redo[anchor-image]` | `ERROR setup: legacy word anchor is missing` | image anchor auto-placement; dry-run null receipt/no write; accepted canonical equals preview; restart retry; inverse/redo | Current source families: `tests/editing_conformance/test_recipe_auto_placement_reads.py`; `tests/editing_conformance/test_recipe_m2_auto_placement.py` | Partial recipe coverage only; full M1 combination remains pending |
| M1-baseline10 | `tests/editing_conformance/test_commit_runtime_m1.py::test_normal_client_auto_placement_preview_restart_retry_inverse_and_redo[anchor-video]` | `ERROR setup: legacy word anchor is missing` | video anchor auto-placement; duration/output media selection; dry-run; retry; inverse/redo | Current source families: `tests/editing_conformance/test_recipe_auto_placement_reads.py`; `tests/editing_conformance/test_recipe_m2_auto_placement.py` | Partial recipe coverage only; full M1 combination remains pending |
| M1-baseline10 | `tests/editing_conformance/test_commit_runtime_m1.py::test_normal_client_auto_placement_preview_restart_retry_inverse_and_redo[fallback-image]` | `ERROR setup: legacy word anchor is missing` | image fallback placement at `fallback_at=1`; dry-run; accepted/retry; inverse/redo | Current source families: `tests/editing_conformance/test_recipe_auto_placement_reads.py`; `tests/editing_conformance/test_recipe_m2_auto_placement.py` | Partial recipe coverage only; full M1 combination remains pending |
| M1-baseline10 | `tests/editing_conformance/test_commit_runtime_m1.py::test_normal_client_auto_placement_preview_restart_retry_inverse_and_redo[fallback-video]` | `ERROR setup: legacy word anchor is missing` | video fallback placement at `fallback_at=1`; duration/output media selection; dry-run; accepted/retry; inverse/redo | Current source families: `tests/editing_conformance/test_recipe_auto_placement_reads.py`; `tests/editing_conformance/test_recipe_m2_auto_placement.py` | Partial recipe coverage only; full M1 combination remains pending |
| M1-baseline10 | `tests/editing_conformance/test_commit_runtime_m1.py::test_normal_client_auto_placement_preview_restart_retry_inverse_and_redo[shared-image]` | `ERROR setup: legacy word anchor is missing` | image shared placement with `frame=24`; dry-run; accepted/retry; inverse/redo | Current source families: `tests/editing_conformance/test_recipe_auto_placement_reads.py`; `tests/editing_conformance/test_recipe_m2_shared_auto_placement.py` | Partial recipe coverage only; full M1 combination remains pending |
| M1-baseline10 | `tests/editing_conformance/test_commit_runtime_m1.py::test_normal_client_auto_placement_preview_restart_retry_inverse_and_redo[shared-video]` | `ERROR setup: legacy word anchor is missing` | video shared placement with `frame=24`; duration/output media selection; dry-run; accepted/retry; inverse/redo | Current source families: `tests/editing_conformance/test_recipe_auto_placement_reads.py`; `tests/editing_conformance/test_recipe_m2_shared_auto_placement.py` | Partial recipe coverage only; full M1 combination remains pending |

The exact current-equivalent source selector is parameterized with IDs
`disjoint-rebase-undo` and `touched-basis-conflict`; those are the only two
current-equivalent nodes claimed here. The source does not claim that the
separate view or auto-placement families close the historical combination.

## Separate authentic archive read

The authentic normal archive-read `79c94` is recorded separately from the
current equivalent:

- Selector:
  `tests/editing_conformance/test_m1_legacy_archive_read.py::test_explicit_held_baseline_then_current_word_bound_read_is_closure_exact`
- Archive SHA-256:
  `2915bd4ac0d46954d19c30f87a517b82074218699978e650fab03fcba81b72d3`
- Held baseline pair: project `7b6f2bae8ffe42bf925216c38249ed79`, timeline
  `film`, revision `film-parent-v1`, publication
  `txn-55c0651b2cd64255ae06e73f9708220a`.
- Advanced current pair read separately: revision
  `a3e671256f1c42b8837d3e118c97b21b`, publication
  `txn-11c90075be6c4c8bb9e2627366f0fe4f`.
- Source review: `agt-F-D107-read-rereview-0647/report.md`, `PASS_SOURCE`;
  handoff `handoff-agt-D107-read-return-0639.md`.

This read proves authenticated closure/read identity only. It is not the M1
combination proof and is not counted as such.

## Separate held current-equivalent source review

- Candidate commit: `2e3331ee2f035e302f5ca52488832cd0e22bb3aa`.
- Candidate source file SHA-256:
  `7c8a4cc3a0383542999d95762ae77b6ce9468414e3313562b09f0f4c9018cbfc`.
- Independent review: `handoff-agt-D107-sol-review-0715.md`, `PASS_SOURCE`.
- Protected original file SHA-256, unchanged:
  `23451aa80279f47d126e5e5699f51272b8a6418402ba559617c243bcd6b15041`.
- The original file has 87 `assert` nodes and eight `pytest.raises` contexts;
  the review records 111 predicate-map rows. No pytest, import/collection,
  fixture/helper execution, service, browser, render, probe, install, or full
  suite ran for this source receipt.
- The candidate's separate current native-bound target refusal
  (`tests/editing_conformance/test_native_word_anchor.py::test_native_move_refuses_anchor_basis_until_explicit_clear`)
  is not substituted for the M1 combination and is not claimed as ABA proof.

## Contract and non-claims

The production caller remains the unchanged registered `commitTimeline`
provider. The C0 v2 request shape is `api_version=1`, exact
`project_id`/`timeline_id`/`base_revision_id`/`base_publication_id`,
`commands[{schema_version,op,version,select,args}]`, `label`,
`steps[{id,label,intent,tags,command_ordinals,patch,optional reads}]`,
`merge=fields|atomic`, optional reads, `Idempotency-Key`, `dry_run`, `source`,
`rationale`, and `group_id`. Accepted/merged replies retain canonical
document, base/landing pair, merge mode, receipt, records/bindings/effects/
dependencies/steps/history/undo_steps; conflicts retain reason/head;
invalid replies retain code/path/hint/suggested command; preview retains
`would_status` and null receipt. Historical rebased retries remain exact.
No guard, policy, authority, schema, or client change is made or implied.

This receipt is source-qualified and behavior-pending only. It does not retire
the ten original tests, close D107, confer functional proof, or count the
archive read as combination proof. Final effective retirement/closure awaits
current dependency release and meaningful MAIN outcomes. No original/test/
product/pin edit is part of this receipt.
