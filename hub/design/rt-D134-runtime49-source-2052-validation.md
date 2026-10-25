# D134 Runtime source assessment

Scope: root-048 (35 legacy-word-anchor cases) and root-022 (14 selected-PARAM cases), exactly as retained by the 2022 root-clusters packet and independently checked by review-2029.

Disposition: 27 root-048 M1 cases are FIXTURE_SETUP; the remaining 8 root-048 retained-input cases and all 14 root-022 cases are UNKNOWN. No product contract gap is proved. No case is retired or blanket-deferred.

The frozen Runtime service boundary is `runtime_protocol/service.py:2546`, which delegates to the registered provider. The frozen Agent first frame is `astrid/sdk/timeline/validation.py:650` for root-048 and `astrid/sdk/timeline/commit.py:1331` for root-022. Frozen Agent source is commit `a4e016b6a9f91fbe372672bdcf382c630bf59186`; frozen Runtime source is commit `5e9ad1c6f74241d8771d3284fdd2ce7a214fd344`. The current Runtime helper/product tree is HEAD `e319fdbcd5` with product parent `ab1e4f6141`; it was used only to confirm the registered-provider call path, not as historical body proof.

Root-048 M1 setup proof: `test_commit_runtime_m1.py:72` publishes a fixture whose authored parent clip contains the exact legacy declaration `word:word-1` but supplies no transcript/source pin or binding. The same source blob is used by the native-checkout, frontend, parent-track, scalar, and owned-move cases. The first refusal is the frozen Agent timing-validation call, with Runtime only at the provider boundary. These 27 rows are fixture/setup, not a product finding.

Root-048 retained-input cases deliberately retain a transcript pin but clear the authored word choice before the measured commands (`test_timing_retained_inputs.py:129-146`). The source comments state that no binding is invented; accepted-history/caller request bodies and the missing raw XML/runner witness are unavailable. The first refusal therefore cannot be assigned to setup or product from source alone. D23/D14 relational-timing deferrals do not apply as a blanket disposition; each of these eight remains UNKNOWN.

Root-022 source shows explicit selected-PARAM setup in the selected-schema fixture (`test_timeline_selected_schema_runtime.py:219-220`) and explicit source selection in the element/numeric/schema callers. That makes a product-contract seam plausible, but the retained evidence does not include the exact authenticated request, hydrated selected-authority state, accepted record, or first failing command within the batch. The frozen exception at `commit.py:1331` alone is insufficient to prove a product gap. All 14 remain UNKNOWN and go to no implementation queue.

Comparator applicability: the prior selected-PARAM and bounded word/transcript passing packets prove only their explicit, bounded source-selection paths; they do not supply the missing D134 request/record/body witness. D12 preservation, D14/D23 deferred relational timing, and D16 earlier-refusal rules were applied per case, not as group-wide explanations.

Validation checks performed: exact member extraction from root-048/root-022; duplicate/disjointness check; frozen source inspection with `git show`; current Runtime registered-provider path inspection; JSON/TSV consistency checks. No Runtime/App/Agent tests, provider runs, socket/browser suites, source edits, or product/test edits were performed.
