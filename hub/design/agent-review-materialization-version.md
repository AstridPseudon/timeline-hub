**APPROVEPRIVATE** — independent read-only Agent source review complete, with no blocking Agent finding. **Runtime semantic ACK, both-owner review, generation/source freeze, actual matched native qualification and public adoption remain separate pending gates.**

Reviewed exact committed `tl/agt-m2-materialization-version-boundary` **`3730d0bd51686a1692450359482205df64dcc839`**, tree **`3892a10bcffa9bf520b4c79591637cf3259d6724`**, parent `9cab2ad36ff6c99c05b42d16d54dfa82e7e86d5e` / tree `216e67d6667ff34f1a192c7dc8326858243bf0f5`. Astrid/tests subtrees `2e79a7b63c78f483a371cfe34c8aea62f6cfb049` / `d3846e625aa0dceb9945ba38be5691658c2be083`; source schema SHA256 **`f80215f272bc2cf302d772d619cb8248108eb597a654e01ab89c3a332204d94f`**. This matches the implementation's proposed tree; the candidate is no longer a pending harness commit. The review worktree's unrelated current HEAD was not tested as the candidate.

Read PLAN first, owner version policy, design/worker report, original counterexamples, prior carrier review, all changed product/tests and Runtime proposal/refinements. The distinction is correct: the original public S2 v1 placement is complete at **103 reads / 3 selections**, while the obsolete private add has **25/3**, missing current owner/order safety facts. No blanket v1 rejection and no guessed legacy authority.

| Version/source | Verified result |
| --- | --- |
| Complete public S2 v1 placement/add/swap | Exact original commands/records/output; empty map; default source-aware engine and detached provider accept; SDK identity ACK passes |
| Ordinary public v1/nonmaterializing edits | Original M1/SDK retry goldens retained; additional original auto/shared/create/unplace/pool requests pass default source-aware execution |
| New obsolete private v1 placement/swap/add | Visible capture refusal, original claims preserved, explicit re-author pointer; durable draft/flight/key survive restart; equivalent current v2 succeeds |
| Current source-bound v2 | Same handlers/guards; exact original S/I, owner O, parent/source pin and D/J join; no new wire field/DTO/seed/framework or derived semantic births |
| Accepted historical private v1 | Authenticated provider-history path preserved; detached JSON-reloaded inverse/redo/restore pass; actual Runtime lifecycle remains unverified |
| Missing/malformed v2 proof or forged owner/source/map/history flag | Closed refusal; empty/identity-map SDK fallback rejected even with receipt echo |

Schema audit independently proves all **48 definitions / 22 operation clauses** and the record/envelope floor remain. Exactly twelve `then` clauses retain the complete old v1 branch and add an exact copy changing only the version constant to `2`; existing unversioned `track.create` args remain unchanged and semantic validation admits only 1/2. V2 inventory: clip.move, placement.move, track.create, clip.set, clip.set-element, track.set, shot.set, clip.set-params, occurrence.add-media, occurrence.swap-media, placement.create, placement.unplace, shot.pool. Parent-only clip add/delete/trim/split and occurrence delete/duplicate, producer guard, inverse/restore stay semantic v1. Reversing only those additive version branches and four inherited item-reference unions recovers byte-exact ordinary S2 **`a6f1aaa9dfcc31828bd04c908158fd7fd9a825df6c9f88f79b81779273a190ef`**. Full current S2 containment passes normally. **S3/text/next ordinary union is excluded and needs explicit later composition/review.**

All three retirement rows remain **HELD candidate**, with both exact test IDs rerun and PASSED:

| Row | Original-v1 refusal | Current-v2 success |
| --- | --- | --- |
| AG-MAT-V01 | `test_recipe_m2_placement.py::test_private_carrier_placement_v1_refuses_without_refreshing_original_claims` | `test_recipe_m2_placement.py::test_parent_and_occurrence_golden_capture_replay_reload_inverse_redo[fixture_path1]` |
| AG-MAT-V02 | `test_recipe_occurrence_media.py::test_private_carrier_swap_v1_refuses_without_refreshing_original_claims` | `test_recipe_occurrence_media.py::test_portable_goldens[swap-fixture_path2]` |
| AG-MAT-V03 | `test_recipe_occurrence_media.py::test_obsolete_carrier_add_v1_refuses_original_claims_with_draft_kept` | `test_recipe_occurrence_media.py::test_obsolete_carrier_add_equivalent_reauthored_v2_succeeds` |

All paths above are under `tests/editing_conformance/`. Original fixture blobs stay unchanged. Public `test_legacy_sealed_new_submission_preserves_original_claims` remains a passing NEW-request success. No guard was weakened or original claims refreshed. Changed provider fixture setup completes canonical publication before capture; changed legacy golden setup is supplemented by independent default-ingress probes.

Independent tests on an immutable candidate archive, shared deps read-only, private/no pytest cache:

| Lane | Result |
| --- | --- |
| Original public/M1 goldens, carrier/version/map/identity, dependent B after lost ACK/reload, stale siblings, undo/replay, SDK forgery/durability | **447 passed**, 55.22s |
| Complete schema containment/union/registry | **96 passed**, 185.86s |
| Ordinary golden/provider setup neighbors | **22 passed**, 164 deliberately deselected, 11.99s |
| Explicit six ledger-pair nodes + original public-v1 success | **7 passed**, 3.62s |
| Independent source/schema/counterexample/default-provider/SDK ACK/default-engine/forgery probes | **24 named PASS lines**, exit 0 |
| Candidate-parent whitespace and fixture diffs; worktree status | PASS; no fixture or worktree changes |

Counts overlap. No full/full* suite, localhost/browser/live run, normal private generation or public artifact/pin mutation. Prior implementation 866/1237 counts were not claimed as independent reruns; its eight integration cases remain unqualified here.

Runtime proposal documents still request the final 13-op version-only semantic ACK; no ACK found at final readback. Static peer inspected at **`3c917378a6dc2b48362fd1bc152cb13a5fd6b84a` / `853c122f2713fd6970164ff6c471550700257e8f`**: private captured closure/sealed-binding joins and ledger-first lookup are retained. This is not approval of the Runtime carrier; coordination separately identifies a secondary-ID over-refusal repair requiring its own reviewed successor. Detached accepted-history fixtures are Agent semantics evidence, not actual Runtime admission or authentication proof.

Next: obtain Runtime ACK and both-owner reviews on the exact Agent/Runtime sources, then normal PRIVATE generation and central targeted native admission/ACK, own-slot/retired/global-item occupancy, opaque/numeric preservation, original dependent captures, accepted retry/restart and inverse/redo/restore. Public adoption remains held. No policy decision was changed during review.

[Detailed report, exact commands, source identity and logs](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-review-materialization-version/notes/report.md).
