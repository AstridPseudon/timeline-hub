# D141 P2 placement history binding classification

## Verdict

`INTENDED_CONTRACT`, source-bounded; Main owns the final gate. This is not a rerun and does not independently inspect raw run3118.

The smallest source explanation is a stale exact expected shape. Mounted child placement changes an unchanged occurrence's authenticated shot/internal-revision endpoints without authoring the occurrence root. Agent deliberately retains those endpoint transitions as `commit.materialization` bindings. The App `nativeUndoExpected()` oracle models `collection.owner:*`, `inverse.stage`, and `commit.effect`, but does not construct `commit.materialization`; `assertNativeHistoryEntry()` compares the complete entry with `toEqual`, so a provider-authoritative binding is a direct mismatch.

## Source trace

Agent `28e56cacb42d3da85b02e5b3543895b44f3d0f70`:

- `_commit_patch.py:700-718` pairs old/new `shot-revision:` and `internal-revision:` images for unchanged occurrences and appends `key: "commit.materialization"` with `ref`, `physical_ref`, `revision_id`, `content_digest`, `boundary`, `owners`, `policy`, `dependencies`, `successor`, `owner`, `edge_before`, `edge_after`, and `step_id`.
- `_commit_patch.py:620-635` appends `commit.effect` bindings for each authenticated before/after physical effect image.
- `inverse.py:1130-1187` reverses trusted accepted records and appends `inverse.stage` with publication/step/ordinal/write-range data.
- `_doc_patch.py:176-183` supplies the physical identity tuple and owners used by these bindings.

The placement test itself requires original shot/internal revision arrays after Undo (`tests/e2e/local/three-products.p2-elements-assets.spec.ts:1280-1290`), so the physical endpoint turnover is applicable to this boundary.

Runtime `6a011d58e69173d70e2e9bb3ac434ac8f9e87d8d` validates rather than strips the fields. `timeline_commit_auth.py:490-555` checks physical binding boundaries, image revision/digest, and step attribution; `commit.materialization` is evaluated against the authenticated step input, while `commit.effect` is tied to a step patch/effect ordinal. `timeline_commit_store.py:1021-1068` re-verifies history reads, `:1482-1495` supplies only authenticated `undo_of` history, and `:2061-2085` stores `canonical_json(records)` in `timeline_commit_history`. This is durable provider output, not an App reconstruction.

The App expected shape is at `three-products.p2-elements-assets.spec.ts:297-410`; its bindings array adds collection-owner captures, `inverse.stage`, and `commit.effect`, but no `commit.materialization`. The final whole-entry comparison is at `:748-761` and the placement Undo reaches it at `:1280-1290`.

## Introducing commits

The original binding writer is `8a66b1ac88b88ee437e42ba4b7d14ad67930d360`, parent `a086cc6db7928dc4a3516d304dd9a472b050f1cf`, “feat(timeline): implement R1 guarded document patches”; it introduced `_commit_patch.py`, including `commit.effect` and `commit.materialization`. R2 inverse-stage recording is `b5b8110667cb96723061dabb16fe81d74ac432d8`, parent `a086cc6db7928dc4a3516d304dd9a472b050f1cf`; provider integration is merge `61ceebce84bd6ae0b162477a343e9e184ea77a19`, parents `28b9b966206d7f19c8fc2212d662797e7024ea1c` and `b5b8110667cb96723061dabb16fe81d74ac432d8`.

The requested suspects are not this writer: D100 `9486cbb06e2ab53402086772e6c2bc18bc4849fc` changes `_command_state.py` item-birth custody; D100 test `42040a9c05ae7105cf88459cad5f0b8b9bf56fd1` is test-only; D136a `20dbfdef45f71fa28a63f5382c154f5cca50b83a` changes typed FPS validation; D139 `d133a14838a4e607947893408bc34ba2742a19c6` joins D100/D136a source deltas; D100a `bbeea9ddf750b1d67d08e848c20262d748e6ff03` carries item-birth changes. None adds the history binding family.

This matches C0 §2 (`design/commit-v2.md:324-350`): persist physical ref, revision/digest, evaluation boundary and verified edge/materialization provenance; undo/replay may follow only authenticated successors. Filtering these fields would weaken the contract and is not authorized.

## Evidence limits

Authorized ORCH/design and normal hub paths contain the placement3118 status/handoff, but no raw run3118 history JSON/assertion diff, safe pre-cut placement receipt/publication tuple, or immutable pre-cut test blob. The exact names above are source-derived and must not be presented as a captured raw payload.
