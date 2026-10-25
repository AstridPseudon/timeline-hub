# D118d verdict: blocked outside authorized source scope

No repository files changed. The clean1623 source is still byte-exact with reviewed1616 (SHA-256 `6e41a5bba04666275b9e252d7aeb30247a145207da3f9ed14f06b338563a1436`).

## First causal seam

The retained actual1646 trace rejects the initial guarded physical-shot `items` replacement at fixture line 311, before source publication/reread or duplication. `_doc_patch.Closure.install` translates the physical revision reference into the owning occurrence's `payload.items`; `State.set` calls `project_shot_items`. The source has no items and its authenticated `item_id_map` is empty, so `shot_item_map` returns an empty correspondence. `_item_ids(value, set(mapping), ref)` then rejects the authored one-item list at `_command_state.py:369`. This is not a failed shot-revision lookup or a duplicated-item rebind.

The fixture comment cites Agent D100 `d3b5cfef76b4b3abef5db5f8288abc214a61354f`. That commit is not an ancestor of this frozen base (merge-base exit 1), and its physical-membership implementation is absent. Its diff authenticates the physical source image and distinguishes physical IDs from remapped placement aliases before allowing a guarded membership replacement. The current base still enforces exact membership against the original empty input. C0 §2 explicitly supports generic membership changes inside an existing payload root; this finding does not change that contract.

## Whole path and identity custody

The ordinary App caller persists intent/request state in `commitOutbox.ts`; `localSaveSession.ts:192` sends the stored request/key, `RuntimeDataProvider.commitTimeline` calls the Runtime client and validates/adopts the accepted canonical closure. The Runtime commit route validates scope/path and invokes the registered provider. `load_timeline_commit_provider("astrid")` loads `create_runtime_commit_service`; the provider executes and only Runtime acceptance can persist the result. The fixture uses that actual registration and commit boundary, not a manufactured accepted response.

The passing current capture caller (`test_capture_source_runtime.py`) genuinely creates and initializes the timeline, creates the occurrence/tracks and admits media, but leaves the shot's item list empty. Its canonical-read helper supplies only canonical image fields. That proves the source custody and projection route; it does not demonstrate the extra item-list birth requested here.

After a successful source commit, `_saved_document` rereads Runtime's physical closure; `open_authoring_bundle` preserves an un-copied shot's physical identities and empty alias map. `authoring_commit._read_base` authenticates the original revision/publication through history and compares the receipt's canonical closure with exact immutable reads. The existing source publish/reread block then ensures duplicate baselines would refer to an accepted source. `duplicate_authoring_shot` copies source provenance and reserves destination identities; `_materialize_duplicates` compares the copied baselines/source mapping with the authenticated source, executes the native duplicate and remaps to the native result. It does not authorize introducing an item into the original empty source. These later stages were not reached in actual1646 and remain behaviorally unverified.

## Unapplied owner seam

Owner must resolve the missing D100 production dependency in `astrid/sdk/timeline/_command_state.py` (`shot_item_map`, `_item_ids`, `project_shot_items`) against the frozen base and its normal suites. No cherry-pick, product edit, guard bypass, private authority, synthetic source map/history, altered input, assertion change or null normalization was applied here. The authorized test-file scope cannot supply that implementation. Further downstream failures are unknown; D100 adoption alone is not claimed to make all nine pass.

## Verification

Ruff, mypy with skipped imports/private cache, Python 3.11.17 compilation/private cache, and git diff whitespace check pass. AST/hash verification preserves all 43 original assertions, all 11 original test functions, and all 54 original fixture statements as an ordered subsequence. Goldens, authored values, pins, topology and input sequence are unchanged. The inherited upstream-absence proof was rechecked at upstream `92443771676ef2bbb547d0a103d708fa8bec4c63`; the test path remains absent. Runtime is clean at commit `5e9ad1c6f74241d8771d3284fdd2ce7a214fd344`, tree `de2954a0ceadb4455903d9abdfec3b773318a50f`.

Own9 NOTRUN: no causal source correction exists and the task prohibits an unchanged rerun. Capacity was below 5 GB initially and later exceeded it; that does not satisfy the independent corrected-source requirement. No full/family/pytest/browser/socket/service/native/recovery suite was run, and no held SWAP WIP was inspected. The retained actual1646 outcome remains 9 setup errors, 0 failures, 0 skipped; it is prior evidence, not this worker's execution.
