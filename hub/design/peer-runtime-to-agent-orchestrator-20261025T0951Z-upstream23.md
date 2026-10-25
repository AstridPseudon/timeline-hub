Ask: Treat the 23-node D54a upstream proof as the replacement for only this scope; do not relabel the historical 924 runtime isolation.
Owner: Runtime worker rt-D118-upstream23-0951 for the actual run; Agent for the seven source-absent counterparts.
By: 2026-10-25T09:51Z requested handoff, completed 2026-10-25T09:56Z.

Pristine Agent: 08e6b905114a3ee2b05c3e7980421f26b4abf15c, tree 2694ae8d2709526b40fa037bda8b159cf412769d, clean.
Pristine Runtime: d4f496ec4fbcae7a1f3a51d47ed5147c561117ad, tree 1d3e06f4d59ed6d459646d24ab185c36eb5be075, clean.

Source AST/body matching verified 23 requested nodes: 16 runnable upstream counterparts and 7 absent (timeline script, four authoring-media rows, forced-caption render, D13 native preflight). The exact central targeted run was rt-D118-upstream23-0951-d118-upstream23-targeted-1025095559-19404: 15 PASS, 1 FAIL, 0 ERROR. The one failure is `test_render_export_adapter_writes_real_mp4_and_is_callable`; after private provenance isolation it reaches the renderer and reports `renderer command exited with status 1`. It is `UNKN`, not same failure, because D54a requires matching exception type and location. Fifteen current failures are `NEW-OURS` against upstream PASS. Absent nodes are not run and remain `NEW-OURS`/absent.

Evidence is under the worker evidence directory and linked by the manifest. The run used the normal upstream test route, exact original pytest arguments, timeout 45, and durable JUnit XML. No integrated Runtime was run in the upstream process, and no production or test files were changed.
