# D100 source boundary disposition

## Result

Finite result: **fixture/setup disposition; source remains HELD**.

The current production behavior is the registered Runtime path:

`RuntimeService.commit_timeline` → registered Astrid provider → `commands.execute` → `doc.patch` → `State.set`/`State.project_shot_items`.

The exact registered-provider comparator `test_registered_runtime_first_source_item_birth_and_no_write_refusal` is the meaningful RED→PASS: parent 23/27 with the first physical item refused at the old correspondence guard; candidate 24/27 accepts the physical item and still refuses the wrong-previous retry without changing the Runtime head. This is the existing source path after real qualification, using the C0 request envelope and `Idempotency-Key`; it does not call `occurrence.place-shared` with a non-default trim.

The remaining shared-owner failure is authored setup in the additive D100 test (`tests/sdk/test_d100_item_birth_boundary.py:156-170`). It starts from `document_fixture(shared=False)`, whose authored occurrence has `source_offset: {start: 0, end: 10000}` (`tests/sdk/test_timeline_commit_provider_document.py:40-44`), then directly executes `occurrence.place-shared`. The existing compiler guard deliberately rejects that non-default placement at `astrid/core/timeline/authoring_bundle.py:829-849`: non-default `source_offset` requires an explicit internal clip source trim. Parent and candidate fail at the same pre-`doc.patch` boundary, so this is not a candidate regression and does not establish a product requirement.

The smallest next path is therefore the one additive test file only: give that direct shared-owner setup an already admitted default `source_offset` (`0` or the canonical zero spelling) and update its authored parent digest. Do not change the compiler guard or silently retrofit non-default trim semantics. Existing protected shared-placement comparators already normalize source offsets to `0` before exercising the path (`tests/sdk/test_timeline_commit_provider.py:719-749`). If the product later wants D100 to certify shared placement with a non-default trim, that needs a separate explicit product question and semantic implementation/qualification; it is outside this source disposition.

## Custody/cache boundary

The two custody failures are compiler-only expectation mismatches. `doc.patch` records the physical closure and calls `_doc_patch_materialize.remember` (`astrid/sdk/timeline/_doc_patch.py:478-531`); `remember` adds `source_mapping._doc_patch_images` (`astrid/sdk/timeline/_doc_patch_materialize.py:13-45`). `_common.py:9-16` defines `source_mapping` as provenance and underscore-prefixed entries as derived helpers. The cache must not be treated as historical/source authority.

The custody assertions that must remain exact are:

- `source_mapping.shots`, including shot/revision/content/internal digests and the empty `item_id_map`;
- `source_mapping.placements`;
- `source_mapping._runtime_document` and its immutable shot/internal payloads;
- physical item identity and opaque item payload survive into the canonical document;
- wrong custody, duplicate/empty IDs, previous-value mismatch, and no-write refusal remain fail-closed.

An equal-strength test shape is to compare those three authoritative regions exactly to `before`, assert that the only extra top-level mapping key is `_doc_patch_images`, and then assert the cache separately: owner `occurrence:occ-a`, source shot/internal revision IDs, shot/internal IDs, cached payload equal to the authored replacement, and cached internal timeline equal to the original internal payload. Keep the existing `item_id_map == {}`, canonical-document, internal-revision, and original-bundle-immutability assertions. This separates an allowed compiler projection cache from custody without removing any live guard or predicate.

## Contract/callgraph/hash custody

- Agent candidate: `9486cbb06e2ab53402086772e6c2bc18bc4849fc`, tree `0919e511bd28b3d3af76bb18155efda12c3e94f6`.
- Runtime source: `ab1e4f6141987706132916e2da16477f5a019464`, tree `7d8e77b2f5a4af79305c9212ce5174d3ea9fd657`.
- C0 integration contract: `e319fdbcd512bd5fc9bc5b2c43abfa4d749c34d9`, tree `d5cb9335a03bf4764548e379ce180a66bf966910`.
- C0 request semantics are at `contract/commit-v2.md:60-110`: exact base IDs, commands, steps, `merge: fields|atomic`, reads, and whole-batch failure. `doc.patch` closure/previous-value semantics are at `:276-293`; conflict rules at `:595-612`; reply shapes at `:703-715`.
- Runtime's immutable caller is `runtime_protocol/service.py:2468-2483`; provider registration is `:2412-2424`, with the Astrid factory in `runtime_protocol/timeline_commit_provider.py:16-18,72-88`.
- The Agent provider executes the authenticated calls at `astrid/sdk/timeline/commit.py:1165-1335`, with the bounded CAS/replay and Runtime `preview`/`accept` handoff at `:1336-1444`; the source qualification helper registers the same provider and invokes `commit_timeline` at `tests/sdk/test_capture_source_runtime.py:155-160,216-260`.
- Candidate physical-source branch is `astrid/sdk/timeline/_command_state.py:316-422`; direct shared setup is `astrid/sdk/timeline/native_occurrence_shared.py:300-325`.

The full hashes and blob identities are in `source-manifest.json`. No product/test/fixture/pin file was edited; no test, lint, type, full, browser, socket, provider/native, own9, TEN, P4, collector, or acquisition run was performed by this worker.

## Durable evidence correspondence

This disposition consumes the immutable receiver1837 packet and independent review1843 packet exactly as supplied. Their retained results are parent 23/27 (4 failed) and candidate 24/27 (3 failed); App projection9/own9 and fixture receiving were not run/applied. The D100 source1742 and security1803 packets remain source-only/HELD evidence, not a semantic release.
