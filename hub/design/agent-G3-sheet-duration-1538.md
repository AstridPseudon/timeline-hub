# G3/G5 detached duration staging handback

This worker found no genuine production staging defect on source
`cc8be25d4ad46fae3f7d0889aaee88f85ab6a9c6`. The current CLI regression fixture
does not retain `sheet.detached`: its local `base_parent` lacks
`publication_id`, while connected hydration adds `pub0`, so `_retain_sheet`
rejects it before `_stage_sheet` can run. The exact target then falls through
to `_apply_parsed`; changing production on that evidence would be speculative.

With the expected `pub0` metadata and donor history shape supplied, the exact
target passes (`1 passed in 1.15s`) and verifies the existing
`_stage_sheet` → `_duration_sheet` → `NativeSheet.preview` → normal commit
route. Pure local duration control also passes (`1 passed in 1.73s`).

Exact details, red/green commands, hashes, and the seven pre-existing Ruff
findings are in the worker report:
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-G3-sheet-duration-1538/report.md`.

Handback: repair/reassign the G5 fixture/history/publication metadata or the
retention comparison before reopening a production change. No product files,
tests, schemas, clients, inverse code, or CLI files were modified.
