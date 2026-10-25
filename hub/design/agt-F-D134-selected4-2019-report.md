## Done

- Updated [test_timeline_selected_schema_runtime.py](/home/user/work/wt/agt-F-D134-selected4-2019/tests/sdk/test_timeline_selected_schema_runtime.py):
  - Replaced retired `publish_parent_composition` setup with guarded `doc.patch` via the registered commit provider.
  - Marked the two reviewed stale-base requests explicitly v2.
  - Changed only the three reviewed status assertions to require `merged`.
  - Preserved all other UNKNOWN cases and downstream purposes.

Validation:

- AST/py_compile: passed.
- Ruff: passed.
- Direct targeted v2 nodes: 3 passed.
- `git diff --check`: passed.
- HTTP lost-ACK node remains unverified; central service failed before collection due lane configuration/pre-existing missing nodes.

Evidence written under the assigned worker directory. Commit message and `DONE` marker created.