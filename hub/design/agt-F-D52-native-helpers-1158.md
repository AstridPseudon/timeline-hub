## Report

Qualified all five live native/helper nodes using current authenticated source/publication fixtures. No product or shared-helper changes.

Tests:

- Five-node focused: `5 passed in 3.15s`
- Four affected files: `115 passed in 13.74s`
- Neighbor controls: `86 passed, 1 deselected in 13.01s`
- Ruff, mypy, AST parsing, and `git diff --check`: passed

The integration-marked `test_runtime_port_declares_exact_text_selection` was not run locally.

One structure test required migrating stale R4 publication assertions to current v2 canonical publication fields while preserving the music-duration behavior. Evidence is recorded at [native.xml](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D52-native-helpers-1158/evidence/native.xml).

Commit message and `DONE` marker are ready.