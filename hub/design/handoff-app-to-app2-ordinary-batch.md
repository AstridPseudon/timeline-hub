# Handoff app → app2: ordinary-batch — 2026-10-20 14:17 UTC
Owner: app2 now; no new App workers on this row. App keeps transition-none and shot-graph-settings.
Current reference root b1ef4b9b/tree8d8a normal013/public12; integration41fff still old pin pending gate.
Branch: timeline/app/tl/app-m2-ordinary028-current-safety-compose @ 55e7e217b4adc2c57315e22ce0bebfc36a436ffa
Branch: timeline/app/tl/app-m2-ordinary-session-compose-r1 @ f5e4386521d1ab3a26b9ef31d145c6185af68952
Proof: OLD028/S2 source units only; no current all-writer retirement. Never import older pins/root/cohort wholesale.
Superseded: older 022/023/028/029 pins, pre-MAIN17 roots and old whole-cohort compositions are SOURCE ONLY.
Remaining deletion/gates: Replace useTimelineOps snapshot ingresses atomically; no partial supported-patch submission, no sequential compiler canary, no fallback after capture.
Shared files: App currently owns door/outbox/commitSession/useTimelineCommandSession/useTimelineOps changes; send exact seam patch before concurrent edits.
Reference design docs: app-writers.md; deletion-ledger.app.md D01-app-ordinary-batch.
Targeted command (own verified dependency graph and own cache config):
`node --require "$N/vitest-runner.cjs" "$V" run --config "$N/vitest.config.ts" --configLoader=runner --no-cache --maxWorkers=1 src/tools/video-editor/hooks/useTimelineOps.test.ts src/tools/video-editor/commands/commitSession.test.ts`
Use the actual test files on the named branch; inspect git tree if a historical filename was renamed. No source-proof is an actual browser/current tuple pass.
Before writer cut: normal actual acceptance → reload → guarded undo → exact retry and 0 legacy traffic; update row evidence through App until ledger ownership is split.
Remote reviewed merge requests receive LIGHT overlap/conflict check and prompt merge queue. No extra broad review imposed.
