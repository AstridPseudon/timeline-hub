# Runtime disposition: AG-MAT-V01, AG-MAT-V02, AG-MAT-V03

Date: 2026-10-21  
Scope: the three old-private-v1/current-v2 materialization mappings only.

## Decision

All three rows are **current pin pending (historical preservation qualified)**.
The candidate Agent source has the required refusal and equivalent-v2 success
assertions, and the reviewed Runtime source has no requested product delta. The
remaining blocker is one normal, matched current private pair from the exact
candidate tree, exercising each row through Runtime admission and the
ledger-first retry/undo/redo/reload path. There is no missing assertion node.

This is not a deletion decision. Keep all three Agent ledger rows
`HELD candidate until merged`; do not mark any row `DELETED` from the refusal
tests. The separate public `old_sealed_placement` v1 counterexample remains a
positive 103-read/3-selection case and is outside these three private rows.

## Evidence boundary

The exact candidate under disposition is Agent commit
`3730d0bd51686a1692450359482205df64dcc839`, tree
`3892a10bcffa9bf520b4c79591637cf3259d6724`, private schema
`f80215f272bc2cf302d772d619cb8248108eb597a654e01ab89c3a332204d94f`. Its
recorded Agent lanes were `866 passed, 7 integration deselected`, `1237
passed, 1 integration deselected`, `96 passed`, and the public-v1 preservation
test `1 passed`; lint and `git diff --check` passed. The recorded focused
Runtime/Agent materialization review also reports `34 passed in 8.31s`.
These are recorded results from the Agent/review workers, not runs performed
in this Runtime worker.

Runtime source review approved the bounded counterparts at:

- `83fe4a1cc8e79ba6db2f06271097a96ff2e7c59a`, tree
  `2d9d740ef22eea3b9ec4899bb8e400251bd6d444`;
- `7b8d6d9afe963e2b7a6c6b32fd4e3797451090da`, tree
  `d20b745c26a33c2ea4e20863f846335c8cf33e1e`.

Those are source/contract approvals, not native qualification or a current
pin. They confirm that existing `EditCommand.version` selects the recording
format, that source/owner/order/closure guards remain authoritative, and that
the private resource union must admit both v1 and v2 so accepted-history retry
can reach the ledger before live validation.

The matched private `952` and `392` results are qualified historical evidence,
not evidence for this `3892a10b` current pin:

- private952 (`909bfad8f9ae22d3e4b0dbb83fdcc07bcf1169c` with Runtime
  `95202c2b`) recorded the actual HTTP pair as `44 passed in 55.07s`; it is a
  v1 workspace path and does not qualify these row-specific v2 placement,
  swap, or add mappings;
- private392 (`1303ce6be32e7bd96ed5c6b35afcb15819e81b50` with Runtime
  `f8da4b6d46b0`) recorded the native door as `2 passed in 5.32s` plus a
  `17 passed` project-data lane; it covers shared-occurrence controls, not the
  three AG-MAT row-specific nodes.

The `016` materialization candidate is superseded and is not evidence. The
reviewed `017/42a` artifacts establish source identity only; its native node
was collected but unexecuted. Neither may be substituted for the required
current pair.

## Row dispositions

| Row | Original behavior / test | Obsolete-v1 refusal test | Equivalent current-v2 success test | Exact evidence and remaining blocker | Disposition and Agent ledger action |
| --- | --- | --- | --- | --- | --- |
| **AG-MAT-V01** | `tests/editing_conformance/test_recipe_m2_placement.py::test_parent_and_occurrence_golden_capture_replay_reload_inverse_redo[fixture_path1]` — occurrence case, private carrier v1; parent remains v1. | `tests/editing_conformance/test_recipe_m2_placement.py::test_private_carrier_placement_v1_refuses_without_refreshing_original_claims` — refusal preserves the original claims/draft. | The same parametrized golden test, using the native builder v2. | Candidate `3730d0bd`/`3892a10b` has both nodes; the recorded focused lane was `34 passed in 8.31s`, and the broader Agent lanes were `866/1237/96 passed` as listed above. Runtime `83fe`/`7b8` source reviews are approvals only. Remaining blocker: execute this exact placement pair on one current matched pin, including ledger-first retry, reload, inverse, and redo. | **Current pin pending; historical preservation qualified.** Keep `HELD candidate until merged`; append that the row assertions and source review are complete, while current matched native qualification is pending. Do not mark `DELETED`. |
| **AG-MAT-V02** | `tests/editing_conformance/test_recipe_occurrence_media.py::test_portable_goldens[swap-fixture_path2]` — private carrier v1. | `tests/editing_conformance/test_recipe_occurrence_media.py::test_private_carrier_swap_v1_refuses_without_refreshing_original_claims` — original claims are not refreshed. | `tests/editing_conformance/test_recipe_occurrence_media.py::test_portable_goldens[swap-fixture_path2]` — native builder v2. | Same exact candidate commit/tree/schema and recorded lanes. Historical952/392 native evidence does not execute this row on the `3892a10b` source identity. Remaining blocker: execute the exact swap refusal/current-v2 pair on the current matched pin, with ledger-first retry, reload, inverse, and redo. | **Current pin pending; historical preservation qualified.** Keep `HELD candidate until merged` and record the matched current pair as the only remaining qualification. Do not mark `DELETED`. |
| **AG-MAT-V03** | `tests/editing_conformance/test_recipe_occurrence_media.py::test_portable_goldens[add-fixture_path3]` — historical carrier v1, 25 reads/3 selections; formerly strict xfail. | `tests/editing_conformance/test_recipe_occurrence_media.py::test_obsolete_carrier_add_v1_refuses_original_claims_with_draft_kept` — draft is retained. | `tests/editing_conformance/test_recipe_occurrence_media.py::test_obsolete_carrier_add_equivalent_reauthored_v2_succeeds`. | Candidate source has both nodes and the recorded focused lane passed. The precise safety delta is old `25 reads/3 selections` versus current `27 reads/4 selections`: current proof adds `occurrence:occ-a/source::app.astrid.pool`, `parent::config.pinnedShotGroups`, and `placement.owners` membership/order/boundary data. Remaining blocker: execute the current v2 add through the matched Runtime pin and confirm ledger-first retry, reload, inverse, redo, and draft preservation. | **Current pin pending; historical preservation qualified.** Keep `HELD candidate until merged`; no assertion is missing, and the 25-to-27/4 proof must not be inferred from refusal alone. Do not mark `DELETED`. |

## Corrected next action

The `3730d0bd`/`3892a10b`/schema `f802…d94f` tuple is historical provenance
only. It is never the next generation or pin target. The sole current private
candidate is PRIVATE017 with Runtime `42a7203f` / tree `1f220b3d`, paired
with canonical Agent `ed5fd33c` / tree `f4a632e4`, raw schema
`6dd2b082…`, canonical schema `9f5612ff…`, and 65 definitions / 37
clauses. A future reviewed normal current Agent pin is still required; this
disposition authorizes neither a new private line nor native execution.

Use one bounded matched current pair from the existing nodes, with
unchanged-byte evidence for the preserved public-v1 positive and exact
source/owner/order/closure assertion mappings, plus the named refusal/current-v2
rows. Do not run three redundant full retry/undo/redo/reload matrices.
Runtime’s new ordered project-data lifecycle node alone is not a materialization
mapping proof.

The Agent ledger owner should leave the three rows held and add the note
“source pair complete; current matched pin/native qualification pending.” Only
after that bounded matched result should the rows move out of `HELD candidate
until merged`. No minimal new test node is required, and no Agent ledger was
modified by this Runtime disposition.

