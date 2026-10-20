# Handoff app → app2: resolved-edit-serializer — 2026-10-20 14:17 UTC
Owner: app2 now; no new App workers on this row. App keeps transition-none and shot-graph-settings.
Current reference root b1ef4b9b/tree8d8a normal013/public12; integration41fff still old pin pending gate.
Proof: Root safety helper integrated f845/cc4 and internal-boundary2d80; it preserves unknown roots but is NOT a retired writer.
Superseded: older 022/023/028/029 pins, pre-MAIN17 roots and old whole-cohort compositions are SOURCE ONLY.
Remaining deletion/gates: Delete serializeResolvedTimelineEdit with its three snapshot callers only after those consumers capture native commands. Retain generic opaque/null/order/proto positives.
Shared files: App currently owns door/outbox/commitSession/useTimelineCommandSession/useTimelineOps changes; send exact seam patch before concurrent edits.
Reference design docs: deletion-ledger.app.md D01-app-resolved-edit-serializer; app-writers.md. Core serializers currently also investigated for derived-cap stripping: coordinate shared seam.
Targeted command (own verified dependency graph and own cache config):
`node --require "$N/vitest-runner.cjs" "$V" run --config "$N/vitest.config.ts" --configLoader=runner --no-cache --maxWorkers=1 src/tools/video-editor/lib/serialize.test.ts src/tools/video-editor/commands/runner.test.ts src/tools/video-editor/hooks/useAssetManagement.assetDrop.test.tsx`
Use the actual test files on the named branch; inspect git tree if a historical filename was renamed. No source-proof is an actual browser/current tuple pass.
Before writer cut: normal actual acceptance → reload → guarded undo → exact retry and 0 legacy traffic; update row evidence through App until ledger ownership is split.
Remote reviewed merge requests receive LIGHT overlap/conflict check and prompt merge queue. No extra broad review imposed.
