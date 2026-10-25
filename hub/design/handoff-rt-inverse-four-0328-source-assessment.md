# R2r/R2 source-only inverse assessment

Scope: four exact selectors from `peer-agent-to-runtime-20261025T031422Z-inverse-four-auth-handback.md`.
This is a read-only source assessment. Historical `10077` outcomes are not treated as current behavior.
The two D14 equal-text positives are outside this handback.

## Exact source identities

| role | path | revision | tree | SHA-256 |
|---|---|---|---|---|
| Agent producer | `/home/user/work/agent` | `657bc2e8dba066df1c7d21851315bdb6b0f16a3a` | `9dee25d783fbb7d70a4eaf76e66de2db1743663f` | see per-file rows below |
| Runtime verifier | `/home/user/work/wt/rt-R2-inverse-four-source-0328` | `6634a17f3ffd885567ba3c91b6c7a560df7375a4` | `47b376717ce7a919a697c62133de3e74dc9f6d3a` | see per-file rows below |

Files read as exact bytes and parsed/compiled in memory:

- Agent `astrid/sdk/timeline/inverse.py`: `06bd41f404a40c17a1ec06b49c8443e0e755f622134822ede55fb3ca79234cee`
- Agent `astrid/sdk/timeline/_commit_patch.py`: `05a1ebc6b251c75f4d5dc272598adc295ce5bf5a8c4596ad08497de6676264be`
- Agent `astrid/sdk/timeline/capture.py`: `d96af5fb7b20e61671e17e23ac3c259c85c3c2da906b2af8751ad92ad7883af7`
- Runtime `runtime_protocol/timeline_commit_auth.py`: `4ac2b8792fe0389afb6eb710a348c35fa196131a13cab175bd3646f7d2cc0aeb`
- Runtime `runtime_protocol/timeline_commit_store.py`: `2a68990b180326585b7f0abaf1ee54c8ff9340e83663f17cd1efff1b2bd78a5c`
- Governing `contract/commit-v2.md` (same bytes as `/home/user/timeline-hub/hub/design/commit-v2.md`): `4581ea85aada0af405b1b1b9284e9938a6dba3ca4f6980b7c3c0be8f135f9bb7`

The frozen R4 candidate SDK ref contains `astrid/sdk/timeline/inverse.py`, but not `_commit_patch.py` or `capture.py`; it was not used as a producer comparator. No checkout or ref mutation occurred.

## Whole-path source comparison

Runtime's verifier derives the expected inverse stage from authenticated source history in `timeline_commit_auth.py:1230-1297`, then requires contiguous non-overlapping native/effect ranges, exact source-site membership, and complete coverage in `:1300-1394`. For timeline-root stages it requires the exact reverse source step patch in `:1473-1495`; for native/effect images it requires the final native image to equal the authenticated stage image and every effect to have the expected bindings in `:1737-1769`.

The current Agent producer matches those predicates at source level:

- `_step_undo.py:329-382` selects authenticated target stages and emits each native slice in reverse order, retaining `_inverse_effects = inverse_changes(source_step.patch[slice])`.
- `inverse.py:1053-1079` restores the source writes plus the authenticated clip-cache derived writes in reverse order; `:1132-1186` records one contiguous `native_write_range` per stage.
- `_doc_patch.py:537-566` reverses sequential set/remove/list effects; `_commit_patch.py:538-561` preserves captured inverse effects when their computed effect set agrees, and `:595-611` binds each exposed effect to its stage boundary and ordinal.
- `_commit_patch.py:152-226` computes the closure-union effect image, including root creation/removal; `capture.py:240-267` is only a command-capture wrapper and contains no inverse-stage or effect-image emission seam.

No source fact demonstrates that Agent emits an invalid range, a non-reversed timeline patch, or an incomplete effect image. Therefore no Agent seam is returned immediately.

## Per-selector handback

1. `tests/editing_conformance/test_word_binding_recipe.py::test_same_word_in_reused_cas_clips_retains_raw_source_through_undo[True]`

   Historical message: `inverse stage native ranges are missing, reordered, or overlapping`.

   Owner: Runtime `timeline_commit_auth._inverse_stage_ranges` (`:1355-1387`). Smallest demonstrated seam: Runtime's authenticated native-range length/start/membership predicate against `_inverse_stage_history` (`:1288-1296`), not Agent capture. Agent's current stage construction is the matching reverse source-write plus clip-cache order (`inverse.py:1074-1079`, `:1143-1186`). No current behavior is inferred.

2. `tests/editing_conformance/test_word_binding_recipe.py::test_last_write_clear_undo_restore_and_restore_inverse`

   Historical message: `inverse stage timeline effects differ from authenticated source history`.

   Owner: Runtime `timeline_commit_auth._inverse_stage_boundaries` (`:1473-1495`). Smallest demonstrated seam: exact equality between the stage patch and the ordered reverse of the authenticated source step patch. Agent retains that source-derived reverse in `_step_undo.py:377-382` and validates/reuses it in `_commit_patch.py:551-557`; no Agent emission mismatch is shown by source.

3. `tests/editing_conformance/test_word_binding_recipe.py::test_on_until_clear_preserves_other_reference_and_opaque_fields`

   Historical message: `inverse stage native ranges are missing, reordered, or overlapping`.

   Owner: Runtime `timeline_commit_auth._inverse_stage_ranges` (`:1357-1393`). Smallest demonstrated seam is the same contiguous range and exact native-site membership check as selector 1. The opaque/reference preservation is downstream of that authenticated stage; current Agent source still emits the complete reversed stage and does not authorize an extra or omitted native site.

4. `tests/editing_conformance/test_native_sheet_current_runtime.py::test_http_omitted_native_clip_row_delete_retries_rebases_and_refuses_changed_selection`

   Historical message: `inverse stage native writes do not cover its authenticated effect image`.

   Owner: Runtime `timeline_commit_auth._inverse_stage_boundaries` (`:1737-1769`). Smallest demonstrated seam: the final native-image equality plus per-effect `commit.effect` coverage. Agent's current `effect_diff` closure union (`_commit_patch.py:152-226`) and stage effect/binding emission (`:538-561`, `:595-611`) are source-complete for this predicate. Conditional follow-up only: if an allowed exact record comparison later shows the clip-delete root/effect omitted, return the minimal Agent seam at `effect_diff`/`finish`; this source review does not establish that omission.

## Governing contract

The comparison follows `contract/commit-v2.md` / `design/commit-v2.md`: provider-generated patches are complete closure-union effects (`:388-412`), inverses use authenticated sequential boundaries and preserve derived effects (`:1593-1610`), and all later writes/reads/dependencies remain guarded (`:1624-1636`). No guard, ABI, authority, or receipt behavior was relaxed.

## Checks

- In-memory `ast.parse` + `compile` for the five Python source files: PASS.
- Scoped Agent Ruff for `inverse.py`, `_commit_patch.py`, `capture.py`: PASS.
- Scoped Runtime Ruff for `timeline_commit_auth.py`: PASS.
- Scoped baseline Ruff including `timeline_commit_store.py`: FAIL with 11 pre-existing style/lint findings in the store; no files changed.
- Scoped mypy over the five Python source files with `--no-incremental --follow-imports=skip --ignore-missing-imports`: PASS.
- No pytest, collection, fixtures, helper execution, body/service run, socket run, attack tooling, or product edits.
