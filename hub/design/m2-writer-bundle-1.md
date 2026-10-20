# M2 ordinary writer bundle 1 — branch qualification

Status: Runtime candidate READY; Agent-owned pin/registry tuple and App browser success/reload/undo qualification pending. Nothing merges into integration until PLAN records M1. Pins move as one coordinated change. Hub-sync publishes/fetches the branches; managers do not push upstream.

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
