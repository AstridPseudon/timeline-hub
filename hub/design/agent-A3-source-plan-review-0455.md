# A3 source-plan review — 0455

**Independent design readiness: PASS.** Production acceptance remains **FAIL / NO-CARRIER / not done**; the production caller uses it is **NOT MET**.

## Scope and identities

Reviewed `design/agent-A3-same-owner-source-plan-0445.md` against PLAN §3, `design/commit-v2.md` §§1–5, BOARD-HEADER, and the current Agent integration source at `f95f1e1691b82dce74a49eb7ca444f97eb364037`.

The source plan retains the exact frozen tuple: Runtime source commit `34eac0041b0891e9011966b39bcbd26053fde5bc` in `runtime.lock.json`, and the approved closed edit-command schema SHA-256 `d106dfe8212500709b4072d7bc0486f83c27d5d8de33d215cb52b9ea7d46357d`. Runtime 34e's `contract/schemas/edit-command.json` has the same `d106…` digest. No product, schema, generated artifact, producer, lock, or pin was changed by this review.

## Findings

1. **NO-CARRIER is source-supported.** Current `astrid/sdk/timeline/commands.py:66–82` registers `occurrence.duplicate`, occurrence media, and placement families, but no selected-owner fork/materialization operation. `native_occurrence_duplicate.py:42–55` creates both `shot:<new>` and `occurrence:<new>` entities. The reused independent 0422 witness recorded duplicate count **2 → 3**, order `[occ-0, occ-1, occ-copy]`, with `shot:shot-copy` and `occurrence:occ-copy`; it is explicitly prior evidence and was not rerun. This is not same-owner isolation.

2. **Current guards do not supply the missing carrier.** `native_occurrence_media_commands.py:42–44` rejects shared authored placement for ADD; `native_placement_commands.py:31–33` has the same shared-placement refusal for move. `_swap()` does not itself call `_exclusive()` in this source, and the source plan correctly avoids claiming an unobserved SWAP rejection or positive shared SWAP witness. Neither fact provides physical same-owner isolation.

3. **The proposed surface is exact and unapplied.** The plan proposes only an optional `args.materialize: "selected-occurrence"` marker on existing `occurrence.add-media`, `occurrence.swap-media`, `placement.create`, and occurrence-selected `placement.move` families. It keeps `schema_version: 1`, `version: "1"`, existing intents/guards, and closed argument schemas; it explicitly keeps parent `clip.swap-media` from accepting the marker (or splits that shared args definition). It does not claim an existing supported option, new op, standalone fork transaction, doc.patch edge write, or current producer capability.

4. **The Runtime exception is explicit and required.** Current Agent and frozen Runtime schemas omit `materialize` and use `additionalProperties: false`; current `placement.move` is registered with shared `ClipMoveArgs`. Therefore the marker cannot be sent to the frozen `34e` producer. The plan correctly makes Runtime `contract/schemas/edit-command.json` and generated client/type adoption an authorized-after-freeze exception, with no generation or pin advancement authorized in this document. It also correctly calls out that the old `timeline_materialization.materialization_join` requires a different destination shot and remapped item allocations, so same-shot revision turnover must use authenticated `commit.materialization` lineage and preserve the old join unchanged.

5. **Physical-owner, identity, closure, read, effect, replay, and undo reasoning has no fatal design gap.** The proposed boundary is consistent with C0c and the current source:

   - resolve the selected occurrence to one verified physical shot/internal image and retain the complete owner set; never choose the first equal alias or broadcast a shared-root edit;
   - derive fresh physical revisions while preserving occurrence count/order, occurrence IDs, shot/entity IDs, raw clip/track/item/asset IDs, timing/maps, source windows, and opaque/authored fields; do not report provider-derived revisions as caller-created entities;
   - leave managed closure edges provider-only and update only the selected occurrence's physical pin, retaining old images while any sibling reaches them;
   - capture exact selected row/pin, source payloads, full physical owners, consulted collections/order, media/registry/timing inputs, and exact pins; keep conservative whole-source dependencies and never fabricate `reads: []` from a byte diff;
   - record complete authored and derived effects plus `commit.materialization` source/successor, owner, edge-before/after, evaluation boundary, step, and command ordinals;
   - rebase only through authenticated unique same-owner successors, refusing ambiguous aliases, missing provenance, unrelated reattachment, unknown history, and ABA; preserve exact-key retry without duplicate effects/history;
   - make whole and per-step undo restore only the selected owner, retain surviving roots, scan later reads/writes/consumers and ABA, and preserve merged landing before-values. The plan explicitly prevents the existing all-owner `remember()` behavior from broadcasting selected-owner inverse.

These are implementation obligations, not evidence that the current source already implements them. The known Runtime store/schema/materialization limitations are concrete implementation blockers and are already named in the plan; they are not a fatal flaw in the document-only proposal.

## Acceptance boundary

The plan preserves the complete v2 request (`api_version`, both scope IDs, both base IDs, `commands`, `label`, `steps` with `id/label/intent/tags/command_ordinals/patch/reads`, `merge`, `reads`, `dry_run`, `source`, `rationale`, `group_id`, and stable scoped idempotency) and full `{data, receipt}` reply/effect/history/undo fields, including authentic historical `rebased` replay and preview `would_status: accepted|merged`. It also explicitly states that the mounted App caller and full v2 producer adoption are not met. A provider-only unit result cannot close A3.

No source-plan correction was required. The smallest safe disposition is to keep this as an unapplied proposal pending orchestrator authorization of the named semantic/schema/producer tuple and cross-lane adoption. Do not treat `materialize` as current or authoritative, and do not claim production acceptance.

## Verification

- `git diff --exit-code` — PASS before report writes; Agent worktree was clean at `f95f1e169…`.
- Import-free source assertions over current registry/schema — PASS: all named operation families present; proposed marker absent from the current closed Agent schema.
- `sha256sum astrid/core/timeline/schema/edit-command.schema.json` — `d106dfe8212500709b4072d7bc0486f83c27d5d8de33d215cb52b9ea7d46357d`.
- `git -C /home/user/work/runtime show 34eac004…:contract/schemas/edit-command.json | sha256sum` — same `d106…` digest.
- Read-only `git show` checks of the frozen R4 Agent/Runtime refs — PASS; no checkout or ref mutation.
- No duplicate probe, HTTP, browser, full, native14, or other heavy suite was run.

