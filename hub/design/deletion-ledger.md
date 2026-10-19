# Deletion ledger: everything that contradicts the end state (orchestrator-owned; managers keep their rows current)
A milestone exits only when every row tagged with it is DELETED. Exceptions are the orchestrator's explicit deferrals, recorded in the Note.
Columns: id | what (paths) | contradicts | replaced by | owner | milestone | status (planned / in-progress / held / DELETED) | evidence (commit + proving test)

| id | what (paths) | contradicts | replaced by | owner | ms | status | evidence |
|---|---|---|---|---|---|---|---|
| D01 | App snapshot/whole-document savers, saveTimeline compat branch, useTimelinePersistence whole-doc fallback, timeline-save-utils reconstruction, every fallback writer in design/app-writers.md | one edit path | EditCommands via the durable command session | app | M2 | in-progress | |
| D02 | App local durable inverse history | Runtime is the only history | Runtime history/undo | app | M2 | planned | |
| D03 | Supabase canonical writers: ai-timeline-agent, timeline-import, complete_task append + registry upsert, _shared/astridAppendService.ts | one edit path (owner: purge) | none, retired | app | M2 | in-progress | |
| D04 | Runtime legacy publish route for canonical timelines (config publish on tracked timelines) | one edit path | /v1 commit only; a direct legacy call must fail (gate 6) | runtime | M2 | planned | |
| D05 | Agent astrid/core/timeline/inverses.py | duplicate inverse logic | registry guarded inverses | agent | M2 | planned | |
| D06 | Agent astrid/core/extensions/ | old extension model | M5 extension model (seams only before then) | agent | M2 | planned | |
| D07 | Agent deprecated retime helpers in astrid/sdk/timeline_editing.py | duplicate timing math | the one timing compiler | agent | M2 | planned | |
| D08 | App duplicate "what's on screen" math (playerEvaluation/TimelineRenderer private math, old audio fade evaluator) | one evaluator | Composition public evaluator | viewing+app | M3 | in-progress | |
| D09 | Agent visualize private copies (fast_lane, motion/model, sweep duplicates), core/onscreen.py, scene_answers duplicates | one evaluator | Composition public evaluator via thin scene_answers | viewing | M3 | in-progress | |
| D10 | Vendored timeline-composition copies (Agent remotion/vendor, App vendor/timeline-composition) and old App vendor theme/effect copies | one package | the exact built Composition tarball (0.0.8 → 0.0.9) | viewing+app | M3 | in-progress | |
| D11 | R4 docs (docs/projects/timeline-r4/) | ceremony | one architecture page | runtime (delivery) | M4 | planned | |
| D12 | Composition stale dist + `|| true` build masking | honest build | real build/tests | viewing | M0 | DELETED | ee22449 |
