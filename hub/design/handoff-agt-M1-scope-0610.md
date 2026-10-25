# F-D86 M1 / D100 source-scope return

Status: `RETURN`, source-only. This is a bounded proposal for the orchestrator; it is not a behavioral qualification, a ledger edit, or permission to change an authored test.

## Decision requested

Do not merge `de864e542aedc17df19200889bf80d3cceda6aa8` (M1 anchor migration). Keep the 0600 return's exact genuine `build_film_fixture(tmp_path)` baseline and the original M1 source unchanged. The safe disposition proposal is:

1. Keep all ten M1 selectors listed in `handoff-agt-M1-scope-0610-selectors.tsv` as one `M1-baseline10` legacy-only scope under the D72(1)/D52 rule, pending the orchestrator's ledger decision.
2. Do not use `variant="anchor"`, a different archive/head, a new music timing, a stripped word binding, a fabricated accepted history, or a new authority seam.
3. Preserve the original predicates and refusal purpose. No test, product, Runtime, schema, pin, or generated-file edit is made by this return.
4. Keep D100's independent inverse-materialization ten failures as a separate scope. They are not evidence for an M1 cure and are not folded into this disposition.

This is the narrowest supported proposal because the current source has no setup-only capture that adds the missing legacy word association while preserving the original authoritative source and head. If the orchestrator does not accept a legacy-only disposition, the honest result is `M1-baseline10: held / missing current supported capture`, not an anchor migration.

## Exact M1 selectors and shared caller audit

The canonical selectors are in the TSV companion. All ten share the same `film` fixture at `tests/editing_conformance/test_commit_runtime_m1.py:21-84`. The four test bodies are:

- `test_cli_python_outbox_restart_and_guarded_inverse`: two selectors, `disjoint-rebase-undo` and `touched-basis-conflict`.
- `test_keyed_view_lost_ack_restart_and_fresh_head`: one selector.
- `test_keyed_view_requires_write_but_inspection_remains_read_only`: one selector.
- `test_normal_client_auto_placement_preview_restart_retry_inverse_and_redo`: six selectors, the Cartesian product of `kind={image,video}` and `mode={anchor,fallback,shared}`.

The shared fixture call trace is static and unchanged:

1. `film` selects the paired Runtime, imports the registered provider, calls the genuine `build_film_fixture`, opens its duplicate root, and registers `load_timeline_commit_provider("astrid")` (`test_commit_runtime_m1.py:22-37`).
2. It reads the pinned source closure (`:38-41`), constructs the authored desired bundle (`:42-55`), and emits the guarded `doc.patch` commands (`:56`).
3. It submits the C0-shaped body through `RuntimeService.commit_timeline` with the exact project/timeline IDs, exact base revision/publication pair, `label`, `steps`, `merge="atomic"`, `reads=[]`, `dry_run`, source/rationale/group, idempotency key, publisher, canonical `/v1/projects/{project}/timelines/{timeline}/commit` path, and authorization callback (`:57-79`).
4. `renderer_off`, `wire`, and `auto_film` are downstream callers. `auto_film` adds only its own current setup commit and is consumed by the six auto-placement selectors; it does not create a second M1 source.

The actual 19214 packet selected exactly these ten M1 nodes and recorded all ten as setup errors: `RuntimeErrorBase`, `setup failure: legacy word anchor is missing`, with no durable traceback frame. That packet is an outcome export, not proof that the original accept path is green. The source trace below explains the refusal boundary.

## Immutable original source and authored contract

The original source is the default captured pre-cut fixture used by `build_film_fixture`, not the anchor variant. Preserve:

- the original `film-parent-v1` authoritative head and its one-parent-revision graph;
- original project/timeline, parent/child/shot/internal identities, physical image/media map, transcript document, text-binding identity, and authenticated pins;
- authored parent declaration and `word:word-1` binding, `until_film_end`, `until: None`, `fixed_start: False`, and `for: 5.5`;
- authored `music-bed` timing (`at: 0`, `hold: 5.5`) and the desired `music-other` timing (`at: 0`, `hold: 5.5`);
- opaque values, including `[None, {"keep": true}]`, list/order, request fields, and every original assertion.

The rejected anchor candidate instead selects `precut-anchor-v31`: its authoritative head is `input-anchor-baseline`; `music-bed.at` changes from `0` to `0.25`; it adds `film.config`, a config clip mirror, declaration/provenance data, and changed authority. The later desired-bundle assignment does not undo those source changes. That is source/authority substitution, not setup. The 0600 static verdict restored the genuine baseline and explicitly found no safe supported current capture preserving both the original source and the missing legacy association.

## Why setup-only capture is not currently possible

D100/D104 permit a setup-only migration only when the original input is invalid under a correct current guard and every authored input, timing, topology, opaque value, expected result, and assertion remains unchanged. D100 explicitly sends a case legacy-only when containment requires changing an authored input or the authored-first source.

The current Agent validation source gives the relevant C0 predicate at `astrid/sdk/timeline/validation.py:405-445`:

- a historical text binding is accepted only when the reference shape is valid (`:417-424`);
- the baseline declaration/reference must be unchanged (`:430-434`);
- the text-reference source basis must be byte-equivalent to the baseline (`:435-437`);
- otherwise it refuses with `historical text binding requires an unchanged declaration and source`.

The original M1 fixture is the genuine historical source and its desired current request must exercise the preserved word association through the registered commit provider. Adding the association to the source, changing its source/head, moving it to the anchor archive, or removing it from the authored candidate would each violate one of the preserved source/authority/binding predicates. Therefore there is no supported setup-only fixture capture in the reviewed sources. This is a source-bound limitation, not a Runtime defect and not permission to weaken the guard.

The current C0 route remains the intended route: Runtime validates the exact request scope and canonical route at `runtime_protocol/service.py:2448-2461`, and the provider is registered/validated at `:2391-2409`. The M1 fixture's request shape is therefore retained as the acceptance/refusal purpose even though the historical setup cannot currently reach acceptance.

## Predicate conservation

The returned source preserves, independently for every selector:

- accepted commit/readback and canonical document equality where the original expects acceptance;
- exact revision/publication base pairing and canonical `commitTimeline` route;
- idempotency key/body preservation after a lost acknowledgement and restart;
- disjoint-head rebase versus touched-basis conflict, with the pending command retained and no write on refusal;
- dry-run preview with null receipt and no durable head/history change;
- accepted retry after restart, exact response replay, and changed-body/idempotency refusal;
- guarded inverse/redo, ABA protection, later disjoint-edit preservation, history/receipt assertions, and no-write checks;
- read-only view refusal versus writer acceptance and identical inspection;
- auto-placement anchor/fallback/shared modes for both image and video, including exact media selection, provider request, preview/accept equality, restart retry, inverse, and redo.

No assertion is removed, weakened, xfailed, or rewritten. No current run is claimed green by this static return.

## Named replacement coverage and explicit gaps

These current tests cover portions of the same C0 foundation and are replacement evidence only for the named predicates, not for the original historical word-bound M1 fixture:

- request envelope, preview/null receipt, structured refusal, exact pair, and canonical commit route: `tests/sdk/test_workspace_client_timeline_commit.py::test_workspace_client_commit_preserves_accepted_envelope_and_key`, `::test_workspace_client_commit_preserves_preview_null_receipt`, `tests/sdk/test_timeline_commit_v2_errors.py::test_preview_projects_landing_head_without_durable_writes`, and `tests/editing_conformance/test_doc_patch_v2.py`'s atomic/ABA/no-write cases;
- restart, exact retry, inverse/redo and accepted-history boundaries: `tests/sdk/test_timeline_commit_provider_runtime.py::test_structural_reservations_and_receipt_retry_survive_runtime_restart`, `::test_restore_inverse_redo_and_exact_retry_survive_runtime_restart`, plus `tests/sdk/test_timeline_commit_provider.py::test_move_reload_and_inverse_import_no_renderer`;
- lost-ack/dependent batch/restart/undo: `tests/sdk/test_timeline_sheet_native.py::test_atomic_batch_commit_lost_ack_restart_and_undo`;
- current auto-placement command construction and its refusals: `tests/editing_conformance/test_recipe_auto_placement_reads.py`, `tests/editing_conformance/test_recipe_m2_auto_placement.py`, and `tests/editing_conformance/test_recipe_m2_shared_auto_placement.py`;
- current view write authority, exact-key retry, restart and read-only inspection: Runtime `tests/test_timeline_native_inspection.py::test_view_write_authority_and_key_before_any_persistence`, `::test_view_retry_keeps_original_revision_after_head_advances`, and `::test_daemon_generated_client_without_executor_catalog`.

Explicitly missing if M1 is legacy-only: one current end-to-end Agent/Runtime test that combines the original authored word-bound source, CLI/Python outbox, lost ACK, restart, disjoint/touched rebase branches, view read/write behavior, and all six auto-placement image/video modes in one preserved physical graph. The named replacement tests cover these capabilities in separate current inputs; they do not prove the missing historical word-bound combination. No claim should be made that they replace the original source identity.

## D100 separation

The exact D100 packet `handoff-rt-D100-30890-0543-per-id.json` reports 59 cases: 38 PASS, 16 FAIL, 5 ERROR. Its independent original-TEN selectors remain separate: five `original-third` inverse-materialization failures, four `authored-first` historical text-binding errors, and one `original-third` ABA control PASS. The first failure boundary for the new families is separately recorded as Agent `capture.py`'s internal `Fraction` conversion for `[at_ms]`, Agent authoring `authoring_bundle.py:849` for non-default `source_offset`, and Runtime closure admission for `chapter-1`. No common cure is inferred, and no Runtime defect is assigned from this source-only scope.

## Evidence and verification

The durable source evidence is in the worker evidence directory named in the final report. It records the 0600 static verdict, A/B/C source verdicts, 19214 and 30890 packet identities, the D100 whole-path trace, and this return's static call audit. The current M1 file was AST-parsed/compiled in memory, and scoped Ruff/mypy plus `git diff --check` passed. No pytest, import/collection, helper/fixture/function execution, probe, service, browser, render, package install, or full suite was run.
