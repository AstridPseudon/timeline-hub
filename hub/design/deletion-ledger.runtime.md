# Deletion ledger — RUNTIME rows (ONLY the runtime manager edits this file)
See deletion-ledger.md for the rules. Add rows here for contradicting code your area must delete; keep status/evidence current.

| id | what (paths) | contradicts | replaced by | owner | ms | status | evidence |
|---|---|---|---|---|---|---|---|
| D04 | Runtime legacy publish route for canonical timelines (config publish on tracked timelines) | one edit path | /v1 commit only; direct legacy calls fail (gate6) | runtime | M2 | held | 3a6b3a5→859c751/c751ef4 removes old publisher body; test_timeline_legacy_authority.py65PASS +test_timeline_authority_door.py12PASS; combined42actual+845defaultPASS. Integration9f9b25c stillunchanged; consumer/M1hold. |
| D11 | R4 docs (docs/projects/timeline-r4/) | ceremony | one architecture page | runtime (delivery) | M4 | planned | |
