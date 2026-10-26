# P2 D141 independent history source review

## Result

Source findings are PASS except for two exact-record defects in 0149's evidence metadata. The source-intent label `INTENDED_CONTRACT` is supportable only at source scope. The actual 3118 extra-field family, its array position, and its cause remain `UNKNOWN_CAUSAL_ATTRIBUTION`; no App actual packet was supplied and none is manufactured here. No product release or gate verdict is made.

## Findings

1. **C0 full v2 request/reply/history shapes — PASS.** C0 §1 requires the exact base pair, commands, label, steps, merge, reads, idempotency and provider-derived step records (`contract/commit-v2.md:60-155`). C0 §2 requires physical ref, revision, digest, evaluation boundary and verified edge provenance in authenticated command/step records (`:314-350`), and complete physical materialization effects (`:388-438`). C0 §4 retains the `{data, receipt}` success envelope and `accepted`/`merged` status semantics (`:703-715`), with structured conflict/invalid replies (`:1265-1315`). C0 §5 requires ordinary-commit undo, persisted target bindings, authenticated materialization provenance and later-history scanning (`:1563-1642`). These shapes remain unchanged by this source-only review.

2. **C0 source intent — PASS, source-only.** The contract expressly requires authoritative physical/materialization bindings for the history and inverse boundary. Therefore an authenticated provider binding can be contract-required in principle. This does not prove that any particular extra record was emitted by run 3118, nor that an App exact-object expectation is stale.

3. **D124 complete-stage emission — PASS with metadata correction.** Agent D124 `16bbd56dbf016bcddeafa891291129efcfa87196` changes `_commit_patch.py` so active inverse stages compute `complete_stage`; for one exact before/after stage it calls `materializations()` into a proposed binding record and appends the proposed bindings only after exclusive, single-owner, successor/edge and shot-identity predicates pass. The passing Agent source has the older `if not self.v2 or not segments` path and no `complete_stage` branch; the cut source has the new branch. Agent pass `070dfc…` is an ancestor of D124, D124 is an ancestor of cut `28e56cac…`, and the reviewed blob IDs in 0149 match the frozen pass/cut source. However, 0149's `candidate_activation.parent` is not exact: D124's direct parent is `5caa12bda353cc46143d3125bce60f8019cf839d`, not `070dfc…`. This is a metadata FAIL, not a failure of the D124 source-delta finding.

4. **D100 item mapping — PASS as non-serializer finding.** D100 `9486cbb06e2ab53402086772e6c2bc18bc4849fc` / D100a `bbeea9ddf750b1d67d08e848c20262d748e6ff03` modify Agent `_command_state.py`: shared placement reopens an exact physical image, permits physical item membership changes without extending an alias map, and adjusts item correspondence/projection. The diff does not add `commit.materialization` serialization. It can change the physical input/image state supplied to a producer predicate, but source alone cannot establish that it made `complete_stage` true for run 3118.

5. **Runtime history validation/projection/persistence — PASS.** On cut Runtime `6a011d58…`, `timeline_commit_auth.py:490-605` validates physical bindings, boundaries, image revision/digest, owners and authenticated successor edges; `timeline_commit_store.py:712-797` verifies accepted records, materialization joins and closure identity; `:1021-1072` exposes verified history entries and preserves records/steps; and `:2061-2092` persists `canonical_json(records)` in `timeline_commit_history`. The pass-to-cut Runtime delta adds validation/projection/history diagnostics and replay safeguards, but the inspected Runtime files contain no new producer-side writer that invents the Agent binding family. Runtime’s role here is validation, replay/projection and durable storage of provider records.

6. **Historical passing placement receipt — PASS, bounded.** Existing D118 evidence records the original automatic child placement case as PASS in 88.780s on the immutable tuple App `96d4754b…` / tree `3f9da34c…`, Agent `070dfc5…` / tree `60564143…`, Runtime `d23a8e0…` / tree `6283b5f…`, Composition `635f4de…` / tree `5ab5191…`. This is case-level historical evidence only; D118 explicitly says the overall eight-case P2 run was NO-GO. It does not contain the raw 3118 actual records.

7. **Peer 0138 and D141d boundary — PASS.** The peer 0138 note says the cut placement failed at `assertNativeHistoryEntry` via guarded Undo and reports only “additional authenticated binding fields” without enumerating them or assigning a product cause. BOARD-HEADER D141d directs Runtime to classify source intent versus product REG and does not itself decide the gate. The evidence therefore supports a finite source review, not a run-level family/cause claim.

8. **0149 evidence metadata — FAIL in two places.** Its verdict/source-manifest correctly preserves the missing actual-3118 packet and correctly records pass/cut trees and most source blobs, but (a) the D124 `parent` field is wrong as an exact direct-parent claim, and (b) `source-manifest.json` says the safe passing receipt is missing even though the D118 receipt cited in the same 0149 findings is present. These are corrected in this review's manifest; neither defect authorizes a product or expectation edit.

## Attribution limit

The source proves a plausible newly reachable producer branch in D124 and a separate D100 item-mapping change. It does not prove that the 3118 request exercised that branch, that the actual extra fields were `commit.materialization`, that D100a supplied the triggering image state, that Runtime caused the difference, or that App's expected shape is stale. Source-derived field names must not be presented as a captured 3118 payload. The safe App actual-vs-expected packet remains absent; no request for it is made here.

## Scope discipline

No source, test, fixture, expectation, request/reply shape, production caller, generated client, kit, hub, network, body, import, collection or cleanup action was performed. The worktree remains unchanged.
