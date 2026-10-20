# M2 ordinary writer bundle 1 — branch qualification

Status: Runtime candidate READY; Agent final candidate3bf9e536 PUBLISHED and exact-pair qualification PASS; App browser success/reload/undo qualification pending. Nothing merges into integration until PLAN records M1. Pins move as one coordinated change. Hub-sync publishes/fetches the branches; managers do not push upstream.

## Runtime — reviewed candidate 2026-10-20T00:00Z

| Field | Exact value |
|---|---|
| Branch / commit | `tl/rt-m2-track-public-export` / `6be970633cc82ab412428151e6bf42f3e7fc3081` |
| Tree | `3fc266c2f8a576a8851c72fe36a21b8f475cd972` |
| Client version | `0.2.2` (provisional until coordinated release) |
| Schema digest | `sha256:89a396aaa10a5ab6c29fb5f053bf12dd031be4a259c33ebc6a53489fcd5878d3` |
| Artifact manifest | `sha256:3b805d6946fd73c44144009021f44153b78ceeb5e5b1298cd2397a1f2dc19730` |
| Copied Agent schema | `tl/agt-m2-parent-label-proof` / `86bfe1860cd2b4fe661bde88051ed4b690b94ce1` (owner CONFIRMED label-only first in runtime-coordination.md) |
| EditCommand file SHA256 | `460e61c70702f1f6bfa5cd033c8da859c913c3c8839f2a5b928df7691e08a388` |

This slice adds the official parent `track.set` label/clear schema. No roots/group draft, ABI/envelope/endpoint/table expansion or authority-cut cohort is included. Its Runtime product base includes the qualified M1 destination-occupancy guard. Agent decides whether later reviewed operations enter a later bundle; do not silently mix schemas.

`TrackSetArgs` requires BOTH `values` and `clear`; additive `anyOf` requires a nonempty set or clear. The generic generator now retains shared/nested fields and refinements, and the TypeScript package public root exports `TrackSetArgs`. Wire command arrays are unchanged; improved TypeScript minItems typing makes command batches/inverse publications nonempty tuples, so builders may need truthful narrowing.

Evidence: generator/artifact/conformance checks and TS typecheck PASS; focused contracts/schema/client/release115PASS (all19 label cases included); central generated clients/second-client/release80PASS/1existing deselection. Actual isolated0.2.2 Python wheel imports/metadata/forwardrefs PASS; packed TS consumer positive/negative compile PASS. Root export descendant separately rebuilt/packed and compiled through `@astrid/runtime-client`, with public negative guards; artifact/schema parity checks PASS. Literal package `npm test` has existing global TypeScript6 TS5112 config-discovery behavior; equivalent explicit build/typecheck/client-node tests ran. No full suite or updated-pin cross-product label semantics claimed.

Agent next: import official Python artifacts from EXACT6be9706 into the confirmed registry candidate, refresh `runtime.lock.json`, check byte parity and real provider compatibility. App next: build/pin the TypeScript package from the SAME6be9706 and use the paired Agent candidate for actual browser label success/reload/undo. Previous946bdff/fe0dd04 and artifact9ab13c/8612 are superseded; do not pin them.

Agent capture/golden source for this slice: `tests/editing_conformance/fixtures/recipe_m2_app_track_label.json` on86bfe186. Agent owns final registry/pin/capture exports and its tuple section below; App owns qualification results.

## Agent — published bundle 1 source (2026-10-20, agt-m2-bundle1-pin)

Status: source READY; focused tests, normal generator/vendor checks and exact-pair real-door qualification PASS (306 direct + 48 central, no skips/xfails). Harness commit is3bf9e5368a956ef562c77e1beb0a745addf23daf; its tree exactly matches the tested tree below.

| Field | Exact value |
|---|---|
| Candidate branch | `tl/agt-m2-bundle1-pin` |
| Base commit | `fc324e838fd668fc06cae906e8bcfccace86ad62` |
| Prepared/tested Agent tree | `b6e56b9fd8453d81d14f6449ab9ee167557d1808` |
| Agent candidate commit | `3bf9e5368a956ef562c77e1beb0a745addf23daf` |
| Approved overlay | Exact additive `2b8f2caa..7f01fcd75c090bbe7d02fd7908f31b615be1ca96`, all 13 files byte-equal to the approved descendant |
| Canonical schema | `astrid/core/timeline/schema/edit-command.schema.json` |
| EditCommand file SHA256 | `460e61c70702f1f6bfa5cd033c8da859c913c3c8839f2a5b928df7691e08a388` — byte-equal to Agent `86bfe186` and final Runtime `contract/schemas/edit-command.json` |
| Portable App golden | `tests/editing_conformance/fixtures/recipe_m2_app_track_label.json` |
| Golden SHA256 | `5aa9aed23a9764e4a9fb0d56fd5efc47368711933adbfaa224f2f725a766ed00` |
| Runtime branch / commit | `tl/rt-m2-track-public-export` / `6be970633cc82ab412428151e6bf42f3e7fc3081` |
| Runtime tree | `3fc266c2f8a576a8851c72fe36a21b8f475cd972` |
| Client / schema / artifact | `0.2.2` / `sha256:89a396aaa10a5ab6c29fb5f053bf12dd031be4a259c33ebc6a53489fcd5878d3` / `sha256:3b805d6946fd73c44144009021f44153b78ceeb5e5b1298cd2397a1f2dc19730` |
| Runtime lock SHA256 | `76509204d81fdeb25dcf3b621a52f0f3ac919c4e53bfe64f0e6c261dbf23ec08` |

Capture/ingress exports: `astrid.sdk.timeline._track_commands.capture_track_set(bundle, select, *, values=None, clear=())`; registry `astrid.sdk.timeline.commands.operations()['track.set']`; `astrid.sdk.timeline.sync.TimelineSession.queue(command)` / `.commit(command, ...)`; CLI `astrid timelines edit track-label TL --track parent/track:ID --set LABEL` or `--clear`. Empty string remains present; clear removes the field. Supplied capture claims are verified, never refreshed. JSON booleans stay distinct from numbers on pending-flight matching; numeric equivalence and default-intent subsets retain their approved behavior.

Scope: parent label only plus corrected native ingress, official Runtime vendor/pin files and their tests. No root/group/params/add/delete/trim/split widening. Permanent `c8010022` M1 identity/occupancy test is unchanged. No Runtime/App writes, install, full suite, merge or push.

Qualification: direct focused tests **306 passed in 16.20s** (parent label, M1 recipe, provider/document, sync/native sync, facade, native CLI, vendored client). Runtime `generators/generate.py --check`, Runtime `scripts/artifact_manifest.py --check`, Agent `scripts/vendor_lock.py check runtime.lock.json --producer /home/user/work/wt/rt-m2-track-public-export`, canonical byte parity and Agent `scripts/gen_cli_surface.py --check` all PASS. Central suite `bundle1-runtime6be9706-integration`: **48 passed in 67.32s**, service exit 0 / 70s, no skips/xfails. It asserts the actual Runtime HEAD before selecting it with `ASTRID_RUNTIME_CHECKOUT`; result path `tests/agt-m2-bundle1-pin-bundle1-runtime6be9706-integration-1020000846-9027/`.

Known inherited limits: Agent `scripts/artifact_manifest.py --check` reports only `astrid/packs/rendering/elements/catalog.ts`; both the stale manifest entry and catalog bytes are unchanged from `fc324e83`. Focused Ruff reports 15 pre-existing CLI findings, byte-for-byte equivalent diagnostics against HEAD, zero new findings across six touched product files. No claim of App browser qualification or a full/make-check pass. App must use this paired Agent tree and the exact same Runtime6be9706 for success/reload/undo. M2 integration remains held until PLAN records M1.

## Agent 2026-10-20T00:10Z selected subset and producer ACK
Bundle1 is LABEL-ONLY FIRST plus native Python/CLI ingress with its reviewed JSON-identity correction. Canonical schema stays byte-identical86bfe186; no roots/groups/otherops included. Other ordinary operations go in bundle2 after composed review. This explicitly confirms using FINAL Runtime6be9706/client0.2.2/schema89a396/artifacts3b805d, not946/fe0.
Agent-owned candidate worker agt-m2-bundle1-pin is composing7f01fcd7 label+ingress onto currentM1fc324, preserving permanentprojection regression, normally vendoring exact6be artifacts/runtime.lock and qualifying real pairedprovider/label/reload/undo. Exact finalAgentcommit/tree/export/pin section follows worker completion/harness commit; do not treat uncommittedsource as a finaltuple. App may build the finalRuntime TSpackage now and preparefrozenexistingparentlabelgolden, thenqualify againstpairedAgentcandidatewhenpublished. ALL integrationmerges HELD forPLANM1record.

## Agent FINAL CANDIDATE PUBLISHED — 2026-10-20T00:17Z
- Branch: tl/agt-m2-bundle1-pin
- Commit: 3bf9e5368a956ef562c77e1beb0a745addf23daf
- Tree: b6e56b9fd8453d81d14f6449ab9ee167557d1808 (EXACT centrally tested tree)
- Paired Runtime: tl/rt-m2-track-public-export /6be970633cc82ab412428151e6bf42f3e7fc3081
- Version/schema/artifact:0.2.2 /89a396aaa10a5ab6c29fb5f053bf12dd031be4a259c33ebc6a53489fcd5878d3 /3b805d6946fd73c44144009021f44153b78ceeb5e5b1298cd2397a1f2dc19730 (sha256 prefixes as above)
- Schema SHA256:460e61c70702f1f6bfa5cd033c8da859c913c3c8839f2a5b928df7691e08a388; runtime.lock SHA25676509204d81fdeb25dcf3b621a52f0f3ac919c4e53bfe64f0e6c261dbf23ec08
- Exports: astrid.sdk.timeline._track_commands.capture_track_set; commands.operations()['track.set']; TimelineSession.queue/commit. CLI edit track-label TL --track parent/track:ID --set LABEL or --clear.
- Golden: tests/editing_conformance/fixtures/recipe_m2_app_track_label.json SHA2565aa9aed23a9764e4a9fb0d56fd5efc47368711933adbfaa224f2f725a766ed00
- Qualification:306focusedPASS/16.20s +48actualexactRuntimePASS/67.32s (agt-m2-bundle1-pin-bundle1-runtime6be9706-integration-1020000846-9027), no skips/xfails. Includes label success/reload/undo, CLI lostACK/restart/exactretry/Python suffixclear/disjoint, M1renderertripwire+permanentoccupancy andclientcutover. Normalgenerator/vendorlock/schema byteparity checksPASS.
- Limits: parentlabel+correctednativeingress only; no additional clipops/root/group/authoritycut cohort. App browser qualification pending. Source inherited renderingcatalog manifest entry stale (actualcatalogfreshness isfixed, manifestchecksumneedsnormal ownerrefresh),15verifiedoldRufffindings; no newlint orfullsuiteclaim. Product source/captures/pins qualified; no additional old-compatdigest bypass.
Manager reviewed boundedparent/ingress/equalitychanges andofficialvendor/tuple diff; commit/tree matchescentralresult. App can FETCH NOW viahub-sync andqualify ordinarylabelsuccess/reload/undo onbranches. Keep this qualified tuple frozen; report candidate progresshere. All integrationmerges held untilPLANM1record.
