# WC8 retained-parameter independent data-safety review

Verdict: **APPROVE** for Agent `c0671afddb34f4fe6b8ca66f511df9fc530cc344`, reviewed against parent `2ca0f9e94fc6dc4ab2ece608eae88e1e2ba50a57` and the settled design `runtime-wc8-retained-params-family.md`.

## Scope and diff

The commit changes only:

- `astrid/sdk/timeline_sheet.py` — retained native parameter-cell carrier and `_duration_sheet` translation.
- `tests/sdk/test_timeline_sheet_native.py` — presence/null/rename and opaque-parameter coverage.

No Runtime, schema, generated client, pin, store, or unrelated Agent writer changed. The live retained caller remains `astrid/sdk/timeline/checkout.py:564-601` (`_stage_sheet`), which loads the original outbox bundle/basis, translates the legacy edited text, previews against `NativeSheet`, and writes pending commands only after the complete preview succeeds.

## Safety review

- Author-time basis is retained and remains authoritative. `_stage_sheet` reconstructs `NativeSheet` from `state["sheet"]["bundle"]` and `state["sheet"]["basis"]`; it does not fetch or recapture a current head. Existing basis/project/timeline/pending checks remain in `NativeSheet.apply` and `TimelineSession`.
- The new allowlist at `astrid/sdk/timeline_sheet.py:798-803` is presence-based: every serialized cell must already have existed in the retained row, except the existing clip-level `asset`, `hold`, `transition`, and `trim` cells. Missing cells, added cells, duplicate/malformed cells, and structural changes refuse before any pending/outbox write. Explicit `key=clear` remains a presence-preserving delete instruction.
- Existing opaque parameter keys are deliberately permitted. Changed known declarations still go through the existing provider at `astrid/sdk/timeline/_scalar_commands.py:68-145`, whose schema validator checks changed declared properties while preserving unknown JSON values. Selected project-pack parameters still refuse at `timeline_sheet.py:820-821`; formula-bound params still refuse at `:822-823`.
- Expression/elision handling remains fail-closed for unquoted expression tokens and `ELIDED` values at `timeline_sheet.py:827-834`. A quoted string beginning with an expression glyph is treated as a literal JSON string, consistent with the literal-text policy.
- `_duration_sheet` translates changed legacy cells back into the retained native serialization (`:973-1002`) and leaves all other cells untouched. The command carrier records `values` and `clear` separately, so null, explicit delete, and rename retain presence semantics.
- No guard refresh, draft replacement, or silent filter was found. Refusals happen before `_stage_sheet` writes `state["pending"]`; the retained retry path continues to use the durable command/flight rather than rebuilding from a new head.

## Independent evidence

1. Targeted touched/neighbour lane:

   ```text
   PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/sdk/test_timeline_sheet_native.py
   73 passed in 8.32s
   ```

2. Refusal and preserved native behavior lane:

   ```text
   PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/editing_conformance/test_native_sheet_current.py -k 'unsupported_cells_refuse_whole_batch_before_queue or custom_pack_param_refuses_without_client_inputs or formula_bound_params_are_a_named_requirement_and_refuse_before_queue'
   17 passed, 21 deselected in 2.46s
   ```

3. An independent inline probe used the existing `Generated` `/v1` fake and real `TimelineSession`: `set-null`, explicit `clear` of an existing null, and text rename were each staged as one `clip.set-params`, committed, reloaded, and undone. Results were `pending_ops=['clip.set-params']` for all three and `restored_exact=True` for all three.

4. A direct retained translator probe showed: existing opaque JSON object replacement is accepted; an opaque expression-like value, a new parameter cell, and an elided value each raise `SheetError("unsupported retained sheet edit")` before staging. `git diff --check` passed.

No HTTP, full, browser, render, install, or live-socket suite was run, per task scope. This approves Agent-side data safety and does not claim live Runtime qualification.

## Evidence note

The changed test at `tests/sdk/test_timeline_sheet_native.py:343-346` appends `unknown=label` after the `# ref` suffix, so that particular assertion proves malformed-binding rejection rather than the retained semantic new-cell refusal. This is a test-witness weakness, not a product finding: the retained source guard is explicit at `timeline_sheet.py:798-803`, the direct retained probe exercised the semantic refusal, and the neighboring native no-write lane passed.

No allowlist deviation or blocking data-safety finding was found. Recommended next step is only to repair that test input if the orchestrator wants the test itself to witness the semantic branch; no product change is required for this review.
