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


## agt-m2-materialization-union-compose — COMPLETE ordinary/item-ref generation freeze

This supersedes b3/schema10c as normal item-ref generation input. Old b3 remains feature provenance ONLY, withdrawn for generation. Exact reviewed deltas were composed onto current ordinary a31, without copying its old EditCommand/ClipSetParamsArgs. M2 integration remains HELD.

- Worktree `/home/user/work/wt/agt-m2-materialization-union-compose`, branch `tl/agt-m2-materialization-union-compose`.
- Observed HEAD/base `a31d712d4a5c9ad08f385e12d71d3f1f7cbfef83`, base tree `38aa664976e61ca50d2358c102c78c9a48e0f7ea`. Successor commit SHA is pending harness exit, so manager must publish actual SHA afterwards; no invented commit identity.
- **Final source tree `42c44bc62e2d2a31cae1c5d531438fa2eb68c5b5`**, product subtree `63bd90527c191264c2ff7e8f6863f746ed3ce8dc`, tests subtree `a66746f9872547ebf3189718e06d1ef7c425c77b` (computed from Git object encoding without writing .git).
- **NEW canonical schema SHA256 `8e0e80624909c31b4a07c956fe06389a1b711b67f46392772ae8b0ff430a56ce`**, source `astrid/core/timeline/schema/edit-command.schema.json`. Normal Runtime item-ref generation must use this COMPLETE union, never raw overrides or withdrawn10c.
- All35 ordinary definitions/14 conditionals (12native +inverse/restore) retained. Reversing ONLY EntityRef/ScopedId/AnchorIdentity/TargetKey item-ref pattern additions recovers frozen472622 source byte-for-byte, including asset refs, schema_source/DocumentPin/MediaSelection and every native closed args. Registry unchanged.
- Carrier remains exact flat allocation-ref→raw-ID, original parent/S/I/owner binding/dependency join, original D/J replay, physical facts separate from typed semantic births. One checked allocation join; shared current875 remapper; unchanged a610 alias/value guards. Current selected-object resolver, media provenance and native clip/scalar/trim/split/popup handlers retained. Approved3eae exact immutable-image comparisons composed; matching exact allocation detector avoids numeric-only materialization without a map. Product net+395, helper178lines.

Final focused evidence: reviewed lane **631PASS/7integration deselected (87.63s)**; current ordinary/provider/params/scalar/media/trim/split/golden lane **721PASS/1integration deselected/5strictXFAIL (95.08s)**. Scoped Ruff and diffcheckPASS; remote.py's122 lint diagnostics verified unchanged. ALL existing golden files byte-identical, new materialization v1 captures separate. Pure media reload/inverse fixtures now supply original verified source contexts, retaining all positive assertions.

**Generation/schema readiness is not complete product qualification.** Two ORIGINAL dependent-B positives fail capture_mismatch after A materializes and provider reloads D: original S/I allocation bindings are not reconstructed at native ingress. Kept strict xfails with original acceptance/unchanged-command assertions. Final Bundle2 ingress owner must hydrate authenticated original accepted allocation/source context (distinct from2590equal-stateABA); no frontend work imported. Three legacy M2 media/placement golden comparisons remain strict xfail for old sealed capture compatibility, with separate new captures positive. This evidence means a direct reviewed carrier port is NOT fully ordinary-compatible; do not silently remove/refresh those expectations or claim a releasable source.

**Actual Runtime admission remains PENDING.** Runtime owner must generate the official matched artifact normally from this schema, compose its source/private join +authenticated own-slot implementation, and qualify occupancy/retired/globalitem authority, stale sibling replay, inverse/redo/restore/retry and six positive opaque real-service requirements. No actual matched-pair run/override/pin mutation or acceptance qualification occurred here. App ACK/pins remain owned work. M2held.

Exact commands, provenance, five outstanding requirements and next steps: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-materialization-union-compose/notes/report.md`. Both commit-msg files ready; harness owns commit creation.


## agt-m2-materialization-superset-compose — guard PASS; successor freeze requires harness HEAD

This section supersedes the preceding 8e schema generation recommendation. Complete candidate `8e0e80624909c31b4a07c956fe06389a1b711b67f46392772ae8b0ff430a56ce` was NOT a release: its four regex rewrites fail the conservative public-floor guard. Withdrawn10c remains WITHDRAWN and is an exact negative fixture only.

Only the four canonical patterns changed in product: each keeps the complete anchored ordinary regex as an independent first alternative and adds a typed shot-item alternative. TargetKey retains the unchanged property-path suffix. Reversing ONLY these four pattern edits recovers the exact ordinary472622 bytes; all 35 ordinary definitions, 14 conditionals, schema_source, closed args and registry are retained. No State/recording/provider/SDK/client/Runtime or pin changes.

Imported the exact six-file tests-only delta from `ffa5325c69c575a883af25123f4d1c20a3706e4b`. Original fixture bytes, provenance and guard tests remain exact. One minimal helper correction distinguishes an absent keyword from an unknown keyword set to null: both adding and removing it now require review. New tests prove the four actual unions under an arbitrary definition name, reject old-branch changes/sibling restrictions/unknown changes, preserve arbitrary old IDs, accept typed new refs and reject malformed item refs. No sample-based containment or name allowlist; no general solver.

- Assigned source worktree: `/home/user/work/wt/agt-m2-materialization-superset-compose`, branch `tl/agt-m2-materialization-superset-compose`.
- Observed source HEAD / successor parent: `2ea37958c8e70ab56209f1c104976f8a198a6a85`; parent tree `42c44bc62e2d2a31cae1c5d531438fa2eb68c5b5`.
- **Exact NEW source tree including all seven new test files: `2a5f9267e6c5e6b924c77d88e8712f77d1ec446f`.** Product subtree `8e28d41e67aa0b54fd3d2fcf82fa5c111b8321ca`; tests subtree `17a9ea9f9d8a34db10fb3bf60fb5aef7985c1617`.
- **NEW canonical schema SHA256: `62a7a2ed1c7af34b90e6c38cda1f8fb725742077a3ac66051ca29dcf389750a6`**, source `astrid/core/timeline/schema/edit-command.schema.json`.
- Final successor source HEAD does not exist until the harness commits after worker exit. Manager must publish that actual commit SHA and verify its tree equals the NEW tree above before freezing a generation input. The observed parent HEAD is NOT the successor. No commit identity has been invented.

| Fixture | Published source | Raw SHA256 |
| --- | --- | --- |
| `runtime-0.2.2.json` | Runtime `6be970633cc82ab412428151e6bf42f3e7fc3081`, `contract/schemas/edit-command.json`, version 0.2.2 | `460e61c70702f1f6bfa5cd033c8da859c913c3c8839f2a5b928df7691e08a388` |
| `runtime-0.2.3.json` | Runtime `d691ddadb4ef3f5881a25fa893b4fb812211f102`, same path, version 0.2.3 | `472622c45fa6b5c7a425c949516a64a52d83192d3749e78a0f000decd088aee9` |
| `withdrawn-10c.json` | Agent `b3c0dbd7c69a369dee303640c2bd608f1d3b71c9`, canonical schema, withdrawn negative only | `10c1610b61ad151259149c97061493d9e36ae0a9220ba4983b45f22e8ac7e3b1` |

Commands run from the assigned source worktree AFTER the schema/helper changes:

```bash
PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q tests/sdk/test_timeline_materialization_schema_union.py tests/sdk/test_timeline_schema_superset.py tests/sdk/test_timeline_composed_schema.py tests/sdk/test_workspace_client_timeline_commit.py tests/sdk/test_runtime_response_conformance.py tests/stage1/test_vendored_workspace_client_parity_luna.py
```

**111 passed in 13.20s**, exit 0. The original five-file guard handoff command (omit only the new materialization-union test file above) also passed unchanged: **77 passed in 7.36s**, exit 0; the extra case versus the prior worker's 76 is the item-reference case already present on this materialization base. All original guard assertions remain.

```bash
PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q --tb=short tests/editing_conformance/test_materialization_map.py tests/editing_conformance/test_recipe_m1_commands.py tests/editing_conformance/test_parent_track_label.py
```

**185 passed in 11.10s**, exit 0. No xfails/skips/deselections in these two final lanes.

```bash
/home/user/work/venv-agent/bin/ruff check --no-force-exclude tests/sdk/command_schema_compatibility.py tests/sdk/test_timeline_schema_superset.py tests/sdk/test_timeline_materialization_schema_union.py
git diff --check
```

Both PASS, exit 0. Each of the seven new files also passed `git diff --no-index --check /dev/null <file>` (exit 0/1 with empty diagnostics, as appropriate for new files).

**Manager handoff after actual guard PASS:** harness commit -> publish exact successor HEAD/tree -> normal Runtime generation from schema62a7 -> apply the same published-floor guard to generated canonical bytes and retain exact Agent/artifact checks. No release/pin/adoption is authorized by this schema result. Historical 0.2.2->0.2.3 regex rewrites remain outside this conservative proof.

M2 integration remains HELD. Five preserved capture behavior requirements (two dependent-B captures and three legacy media/placement goldens) are owned by another worker and were not rerun or claimed resolved here. Runtime admission, own-slot/occupancy, opaque real-service requirements and coupled acceptance remain pending. No App-readiness claim. Full report and RED probes: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-materialization-superset-compose/notes/report.md`.
