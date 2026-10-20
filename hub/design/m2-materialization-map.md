# Exact source-bound materialization map — Agent candidate

Worker: agt-m2-materialization-map-impl, base 1b52391e. Runtime peer: rt-m2-materialization-own-slot. Both exact manager ACKs are in commit-contract.md (Runtime 01:18, Agent 01:22). This coordination page was published before product wiring. No Runtime files, generated artifact, SDK/App dependency pin, seed, ABI or default timing activation changed.

## Source and schema exports

- Canonical schema: `astrid/core/timeline/schema/edit-command.schema.json`. The four existing patterns ScopedId, EntityRef, TargetKey and AnchorIdentity now admit closed `shot:D/item:J` addresses. Generate from this source normally; this worker generated no release artifact.
- `astrid.sdk.timeline._command_state.item_identity(ref)` returns `(shot_ref, raw_item_id)` only for a canonical shot-owned item. `State.entity/get/set` use actual `item_id` with `id` fallback; logical aliases connect item rows to their authored shot aggregate. No writable fallback resolves immutable source shots or items.
- `open_authoring_bundle(..., capture_sources=True)` retains deep-copied verified parent/shot/internal inputs in private `source_mapping._source_closure`. The default stays false for frozen M1 bundles/goldens. One necessary Agent SDK read-boundary line in `RemoteTimelines.open_bundle` enables it. Without this line, the real SDK would seal legacy commands while the provider reconstructed new bindings; the parity test proves the corrected SDK and provider captures agree. `bundle_from_document` already retains the verified complete `_runtime_document`.
- `_copy_shot_for_placement` keeps its exact seeds and remaps `item_id`, raw `id` fallback and equal identity mirrors; distinct secondary ids and opaque children survive.

## Exact capture exports

`Plan.id_map: dict[str, str]` is copied to provider PreparedCommit.id_map and therefore Runtime result/receipt by the existing port. For each destination D, source S, owner O and original source item map `{I: J}`:

```json
{"shot:D":"D","shot:D/item:J":"J"}
```

Authoritative records retain:

```json
{
  "bindings": [
    {"key":"shot:D","ref":"shot:S","policy":"fixed","dependencies":["materialization.source:shot:D"]},
    {"key":"shot:D/item:J","ref":"shot:S/item:I","policy":"fixed","dependencies":["materialization.source:shot:D"]},
    {"key":"materialization.owner:shot:D","ref":"occurrence:O","policy":"fixed","dependencies":["materialization.source:shot:D"]}
  ],
  "dependencies": [{"key":"materialization.source:shot:D","kind":"entity","policy":"exact","pin":{"parent":"ORIGINAL base_parent object","source":"ORIGINAL source_mapping.shots[D] object, including item_id_map"}}]
}
```

The strings describing parent/source above stand for the full existing objects, not new wire types. `Recording.finish(capture=True)` retains these source and owner binding refs in command.bindings before sealing. No command args field is added; no created fact or absent authored root is fabricated for materialization. Semantic item births use typed create_entity, absent reads and actual writes; raw aggregate writes cannot smuggle a new item identity. Shot aggregate births retain their existing typed root primitive. Provider item reservations use raw item ids separately from project-shot identities; cross-project/global physical admission remains Runtime-owned.

`_materialization.id_map(records)` joins exact complete recorder facts; `_materialization.verify_sources(State, records)` verifies original scope, owner, source and parent against retained immutable input. `_materialization.source_entity(State, ref, pin)` returns a detached raw S/I value only from those verified inputs. It never supplies a writable State entity.

`_materialization.consume(bundle, records, closures=...)` installs only captured D/J, with unchanged allocator seeds, when a sibling or undo makes S unshared. Rebase retains original materialization pins; it does not refresh them from the head. Ordinary authoritative reads still observe their execution head, while command claims remain original. Provider inverse source contexts load the original parent named by authenticated records in addition to accepted before/after boundaries, so undo can recover S and redo consumes the same D/J after reload.

**Inverse detail for Runtime review:** inverse records and their Plan/result id_map retain the original allocation bindings/dependency even when undo's output closure returns O to S/I. Thus a map is provenance of an already captured allocation, not a claim that output still contains D, or that any SQL row is absent. Redo returns the original map. Restore remains the existing verified whole-closure operation and emits no new allocation; later materialization captures the same scoped destinations. The provider tests cover sibling-first rebase -> undo -> redo with exact closure recovery.

## SDK ACK and release boundary

SDK sync reconstructs known native commands against the exact original source bundle and checks the entire returned commands list, derived map, scoped output owner/items, closure hashes and receipt identity. A missing map on a typed request fails too. For inverse results with a nonidentity map, SDK fetches the referenced accepted history and original source contexts, cross-checks returned commands/maps against that history, then validates the reversed source/output closure. Arbitrary nonidentity maps remain refused, leaving the flight intact. App owns its corresponding validator.

No compatibility refresh of old sealed command claims was implemented. Frozen M1 bundles and identity maps retain their old captures; old accepted records/retry authority stay on the existing path. Any additional old-sealed-command migration needs joint Runtime review rather than dropping claims.

Runtime must review the source candidate (including inverse provenance above), generate the four item-ref patterns through the official paired release, refresh pins/ACK validators under their owners, then run actual coupled admission/occupancy/own-slot/retry tests. Existing installed generated contracts are deliberately untouched; no schema override or claimed actual Runtime qualification. M2 integration remains held per PLAN.

## Size and evidence

The 150–220 line target is exceeded. Before implementation this page recorded the concrete reasons: sibling-first installation before guard verification and accepted-reload inverse require a read-only source resolver separate from State. Additional executable counterexamples required retaining inverse allocation provenance across unshared-source undo/redo, typed raw-item birth/reservations, and checking SDK ACKs against original commands and accepted inverse history. These are bounded functions over existing envelopes; no new framework, table, endpoint, DTO, receipt ledger or allocator was introduced. Exact final counts and test commands are in the worker report.

Final status: **Agent source/schema/capture contract ready for joint Runtime/App review and official paired generation.** Targeted final source: 584 passed, 1 default-marker deselection in 44.55s; focused Ruff and git diff --check passed. Product net +397 lines (+425/-28). The shared `_remap_shot_items` raw-codec helper applies recorded I->J on replay; the allocator is used only for original opening/verification, with unchanged seeds. Actual Runtime occupancy/own-slot qualification remains unverified.
