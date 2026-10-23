# P1 mounted mixed-chain source handoff

Status: **BLOCKED — no fabricated chain spec**. H3 remains no-go.

Base inspected: `tl/integration` / App `9d6df77eac9a3e32854dcee79e1213c48feb9573` (`9d6df77ea`).

## Concrete missing production seam

The mounted editor can express a visible split, but the current production caller does not express it as the required A2 command/outbox intent:

- `src/tools/video-editor/hooks/clip-editing/useClipSplitting.ts:28-33` and `:46-51` call `splitClipAtPlayhead(...)` and pass the resulting full snapshot to `applyConfigEdit(...)`.
- `src/tools/video-editor/commands/commitSession.ts` exposes `clipTrimPort`, but no `clipSplitPort`; the production session has no `clip.split` capture/finish/submit path that reserves and persists the created right-hand ID.
- `src/tools/video-editor/commands/clipSplitCapture.ts` and `clipSplitGesture.ts` are absent on this base.
- `src/tools/video-editor/commands/localSaveSession.ts` exists as the A2 boundary, but `createLocalSaveSession` has no production caller in `src/`; its only current callers are tests. The mounted editor still reaches `useTimelinePersistence` through the snapshot save path.

Therefore a new `tests/e2e/local/three-products.p1-chain.spec.ts` cannot honestly drive the requested sequence through “actual mounted upstream editor → A2 persisted outbox → Runtime → Python Agent.” Importing or copying the existing `parent-split-command.spec.ts` would only prove the separate pre-A2 split path and would fabricate the missing created-ID handoff. Per the task decision, no new spec was added.

Owning caller: App A2 production integration, specifically the mounted editor split caller/session wiring (`useClipSplitting` → command-session/A2 outbox). The seam must reserve the right ID, submit `clip.split`, expose the canonical `id_map`, and let the dependent trim target that mapped ID without recapture. A2 must also revalidate or roll back dependent intents after predecessor refusal.

## Required follow-up before source can be prepared

After the App A2 production caller is integrated with the split port, this test should use the existing three-products fixture/harness and CLI helpers to cover:

1. Agent `clip.split` with an explicit reserved right ID.
2. Mounted App trim of that newly created ID via the real UI entrypoint.
3. Agent `track.set` while the App predecessor is pending.
4. Lost durable ACK, reload/Runtime restart, and exact request body/key retry.
5. Accepted, disjoint merged (Agent field preserved), and refused predecessor/dependent preservation without overwrite.

The future source must assert raw/opaque/null/absence/membership preservation, canonical closure and digest/head/receipt/commands/authoritative steps/dependencies/merge mode, created-ID handoff, exact retry bytes and key, no duplicate history, Runtime `/commits`, and zero old-route/network writes. New v2 requests must retain `api_version: 1`, project/timeline IDs, both base IDs, semantic or `doc.patch` commands, label, complete steps, merge, reads, dry-run, and `Idempotency-Key`; accepted/merged/conflict/invalid/preview replies must retain the complete v2 fields from `contract/commit-v2.md`.

## Evidence and acceptance

- Fixture `tests/fixtures/p1-feasibility/cases.json` is explicitly `authored-not-go` and names the missing “App split capture/submit port for `clip.split` and created-id binding” plus A2 dependent revalidation/rollback.
- Existing `tests/e2e/local/parent-split-command.spec.ts` is a standalone real-UI split proof, not the requested mixed A2 chain; its current production source still targets the pre-A2 path above.
- A2 draft branch inspected read-only: `tl/ap2-P1-A2-chain-draft-proof` at `e739d880e`; it adds the local-save session boundary but does not mount the split caller into production.
- No browser, socket, Runtime, or full suite was run. The requested chain source is not source-ready until the owning seam lands.
