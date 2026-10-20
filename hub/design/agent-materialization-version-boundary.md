# Agent materialization version boundary

**PRIVATE source candidate; not a source freeze or native qualification. Runtime ACK / both-owner review / matched private proof pending.**

```json
{
  "parent_commit": "9cab2ad36ff6c99c05b42d16d54dfa82e7e86d5e",
  "parent_tree": "216e67d6667ff34f1a192c7dc8326858243bf0f5",
  "candidate_commit": "PENDING_HARNESS_COMMIT",
  "candidate_tree": "3892a10bcffa9bf520b4c79591637cf3259d6724",
  "astrid_tree": "2e79a7b63c78f483a371cfe34c8aea62f6cfb049",
  "tests_tree": "d3846e625aa0dceb9945ba38be5691658c2be083",
  "schema_sha256": "f80215f272bc2cf302d772d619cb8248108eb597a654e01ab89c3a332204d94f"
}
```

## Exact version contract (PRIVATE proposal; Runtime ACK still pending)

Compatibility uses only existing EditCommand.version. NEW ordinary v1 commands use the unchanged public S2 record format. NEW v2 commands use the source-bound carrier. Both execute the SAME current handlers with the SAME owner, order, read, selection, producer and parameter guards. No submitted-binding-presence fallback selects semantics. The engine never changes a submitted version or refreshes its claims.

Native capture helpers select v2 only for a virtual occurrence shot in a bundle carrying its verified original source closure (destination shot differs from immutable source shot). Parent and nonmaterializing/legacy authoring keep v1. A sealed v2 command must contain all seven original capture fields: resolved, expect, authorship, reads, selections, bindings, created. Missing proof or a legacy bundle cannot authorize v2. Unsealed commands still run the authoritative recorder; the Runtime counterpart additionally requires the existing request-private sealed bindings before admitting a nonidentity map.

For v2 materialization the exact capture remains original S/I -> D/J, fixed materialization.owner binding, exact materialization.source:{shot ref} dependency pin (parent + source), existing flat id_map, and no semantic birth claim for derivation. No capture_version, DTO/argument field, store/table, endpoint, allocation seed, alias op or second interpreter/provider was added.

Affected operation inventory (v1 retained; v2 additive, identical closed args):

| Operation | Existing args definition (unchanged) |
| --- | --- |
| track.set | TrackSetArgs |
| shot.set | ShotSetArgs |
| clip.set-params | ClipSetParamsArgs |
| clip.set-element | ClipSetElementArgs |
| clip.move | ClipMoveArgs |
| occurrence.add-media | OccurrenceAddMediaArgs |
| occurrence.swap-media | OccurrenceSwapMediaArgs |
| placement.move | ClipMoveArgs |
| placement.create | PlacementCreateArgs |
| placement.unplace | PlacementUnplaceArgs |
| shot.pool | ShotPoolArgs |
| track.create | TrackCreateArgs |
| clip.set | ClipSetArgs |

All 48 definitions / 22 operation conditionals remain. Twelve then clauses now contain the complete unchanged old v1 branch and a copy changing ONLY version to 2. track.create already had an unversioned closed-args clause; it remains byte-identical and semantic validation accepts only 1/2. clip.add/delete/trim/split are parent-only and remain v1, as do occurrence.delete/duplicate, producer.guard, timeline.inverse and timeline.restore.

timeline.inverse v1 retains its existing authenticated accepted-history allocation facts, including private v1 records accepted before this boundary. Ordinary NEW private source-bound v1 captures refuse at exact recorder comparison with capture_mismatch and the message “keep the draft and explicitly re-author it against the current timeline.” The SDK keeps the exact pending draft, in-flight payload/key and visible conflict across restart. No accepted ledger or Runtime retry ordering was edited.

## Counterexamples and one-to-one version cases

Exact input: /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-materialization-current-recovery/legacy-capture-counterexamples.json
Raw SHA-256: f8a0227cd8dc90c9a042594b5db31f5fc9858a8417708d29771b9d65e2d4ef8e.

A direct equality probe verified old_sealed_placement.input/command/expected_records/expected_output equal the original repo fixture, and historical_carrier_add.input/original_command/original_output equal the original private add fixture. The new native add command equals historical_carrier_add.current_command with ONLY version changed to 2: 27 reads / 4 selections, not the obsolete 25/3 footprint.

Evidence requiring a distinction: old_sealed_placement.command is itself the complete public S2 v1 placement (103 reads / 3 selections), including the existing placement-owner guard. It is preserved unchanged, not retired merely for lacking NEW carrier bindings. test_legacy_sealed_new_submission_preserves_original_claims now passes its original success assertions and explicitly checks response id_map == {}; test_complete_public_s2_v1_keeps_original_capture_records_output_and_map covers placement/add/swap through default full closure opening. Forging only its version to 2 fails missing authoritative source bindings; explicit native v2 authoring gives the identical authored output. Runtime review of this distinction is requested; it is not a native acceptance claim.

The three pre-release private carrier v1 cases below retire only NEW submissions. All golden fixture bytes remain unchanged. Successful v2 placement/swap checks retain every old claim and record except the explicit operation version; the add equivalent preserves the original input/args/output and current 27/4 safety basis.

| Row / state | Retired private positive | Original-v1 refusal | Equivalent current-v2 success |
| --- | --- | --- | --- |
| AG-MAT-V01 — HELD candidate until merged | tests/editing_conformance/test_recipe_m2_placement.py::test_parent_and_occurrence_golden_capture_replay_reload_inverse_redo[fixture_path1] (occurrence case only; private carrier v1) | tests/editing_conformance/test_recipe_m2_placement.py::test_private_carrier_placement_v1_refuses_without_refreshing_original_claims | tests/editing_conformance/test_recipe_m2_placement.py::test_parent_and_occurrence_golden_capture_replay_reload_inverse_redo[fixture_path1] (native builder v2; parent remains v1) |
| AG-MAT-V02 — HELD candidate until merged | tests/editing_conformance/test_recipe_occurrence_media.py::test_portable_goldens[swap-fixture_path2] (private carrier v1) | tests/editing_conformance/test_recipe_occurrence_media.py::test_private_carrier_swap_v1_refuses_without_refreshing_original_claims | tests/editing_conformance/test_recipe_occurrence_media.py::test_portable_goldens[swap-fixture_path2] (native builder v2) |
| AG-MAT-V03 — HELD candidate until merged | tests/editing_conformance/test_recipe_occurrence_media.py::test_portable_goldens[add-fixture_path3] (historical carrier v1, 25 reads/3 selections; formerly strict xfail) | tests/editing_conformance/test_recipe_occurrence_media.py::test_obsolete_carrier_add_v1_refuses_original_claims_with_draft_kept | tests/editing_conformance/test_recipe_occurrence_media.py::test_obsolete_carrier_add_equivalent_reauthored_v2_succeeds |

These rows are appended to /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/deletion-ledger.agent.md as HELD candidate until merged. Accepted legacy placement/add/swap histories retain their exact original records through JSON reload, inverse, redo and restore (detached authenticated-port test, not a manufactured SQL publication). Ordinary public v1 captures and all current original safety tests remain positives.

Final targeted evidence: **866 PASS / 7 integration deselected**, **1237 PASS / 1 integration deselected**, **96 schema PASS**, plus explicit public-v1 response-map node **1 PASS**. Ruff and diff check PASS. Original dependent B after materialize A/reload, stale sibling D/J, original claims, inverse/redo/restore and accepted private v1 history JSON reload pass detached/engine lanes. No full/full* or live suite requested.

Runtime counterpart statically inspected at 3c917378a6dc2b48362fd1bc152cb13a5fd6b84a/tree853c122f2713fd6970164ff6c471550700257e8f: existing private capture join and ledger-first lookup retained. This is not actual Runtime acceptance. No normal private generation or public artifact/pin change occurred.

Exact commands/results, code refs, fixture setup distinctions, source identity, diagnostics and next steps: /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-materialization-version-boundary/notes/report.md.

Proposal and refinements are in /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/runtime-coordination.md and /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-m2-materialization-current-recovery/agent-coordination.md. No Runtime ACK at final readback. The whole task remains blocked on cross-review and exact-source normal PRIVATE joint qualification; source implementation is ready for review.
