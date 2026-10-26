# P4 D141 receipt check

Result: **PASS** for receipt validity only.

Read-only validation performed against the final serialized correction JSON, not its narrative:

- `correction.json` SHA256 is `b7be6965be0ac87e37ba139dcc621745ac84fb20796b78d2d03fea9d46aeeee5`.
- Service identity is `agent-p4-current-becfe-http-3legs-1026011042-10086`; the retained status is `pass`.
- The effective XML path is the retained 0055 output, and its SHA256 is `afca45b778f118b22f30e2cac08654a902dd86241b76442f146ae0ad8623316d`.
- XML parsed successfully: 3 testcases, 3 passed, 0 failures, 0 errors, 0 skipped, total `23.668` seconds. The three XML selectors match the command selectors exactly.
- The retained 0055 manifest and runmanifest still declare the absent 0047 path. The effective 0055 XML exists; the stale 0047 XML does not. No path substitution or original rewrite was performed.
- The controller-0105 source manifest SHA256 is `a97be375458fdb08c7c5041f64cd7097a8408a9175e1ac653345785dbf0734cb`. `sources.before`, `sources.after`, and `sources.final` match the correction receipt's recorded hashes.
- Direct read-only Git checks in the four source repositories confirm each requested commit object and tree exactly: Agent `28e56cac…f70` / `2ebe2ddf…e58a`; Runtime `6a011d58…7d8d` / `ac5b8627…da28`; App `867cb273…9422` / `2b44a46c…e7dd`; Composition `635f4de0…9f40` / `5ab5191a…a148`.
- The 0151 receipt remains exact (`949923e1…e11e`) and records the prior 39-character Agent tree. The correction restores the final `a`; the correction scope is metadata only. The 0114 `FAIL` receipt remains preserved.
- Service 19479 remains queued/unstarted with no exit or XML; service 1347 remains the distinct historical zero-selector failure. Neither was altered.

No pytest, imports, collection, product execution, acquisition, source/control rerun, kit/registry change, or code change was performed. This check does not grant an independent P4 GO.
