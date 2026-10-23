# Handoff: P4 G3 draft readiness

Base `b0a169a51a88c0f71e69cee894316a2450549856` remains clean. The existing G3 emitter is ready for structural translation: one scalar edit emits one guarded `set`; ten pre-existing note slots emit ten ordered absent-value changes. The P4 case-shape tests, emitter conformance, and seven narrow CLI/Python/sheet/show/history facade tests pass. Ruff, mypy, and `git diff --check` pass.

Execution is **not ready for P4 acceptance**. `astrid/sdk/timeline/commands.py:29-92,106-117` has no `doc.patch` operation, so validation/execution rejects it. `astrid/sdk/timeline/commit_session.py:57-74` reaches the emitter but intentionally stops at the R1 provider seam; `astrid/sdk/timeline/sync.py:307-328` only submits registered native commands. `TimelineSession.undo()` (`sync.py:405-414`) supports whole-publication inverse only, not the contract's per-step map. Current CLI/sheet paths (`astrid/packs/timeline/cli_native.py:197-213`, `astrid/sdk/timeline_sheet.py:720-889`) remain native-command paths.

Per requirement: single native front doors **partial pass**; emitter translation **pass**; ten-note accepted commit **blocked on Agent R1/G2 integration**; per-step undo/history step patches **blocked on Agent R2 and Runtime R2r**; conflict/rerun **native boundary only**, generic patch unexecuted; show/history **facade-only**, authoritative v2 records unexecuted. Generated-transport tests were not counted as real provider acceptance. No new P4 test was added and no full/live suite was run.

Logs: `/tmp/p4-g3-baseline.log`, `/tmp/p4-g3-cases.log`, `/tmp/p4-g3-facades.log`, `/tmp/p4-g3-emitter-boundary.log`, `/tmp/p4-g3-ruff.log`, `/tmp/p4-g3-mypy.log`, `/tmp/p4-g3-diffcheck.log`.
