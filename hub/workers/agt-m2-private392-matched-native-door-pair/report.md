Implemented the bounded private392 native/Door qualification.

- Added [test_commit_runtime_private392_native_door.py](/home/user/work/wt/agt-m2-private392-matched-native-door-pair/tests/editing_conformance/test_commit_runtime_private392_native_door.py).
- Added the named central suite `private392-native-door-integration`.
- Verified exact Agent/Runtime pins, health digest, authenticated Door startup, module paths/hashes, project-data roundtrip, inverse/redo, stale zero-write refusal, and opaque disjoint preservation.
- Existing shared-occurrence lost-ACK/retry/control passed.

Results:

- Project-data targeted tests: **17 passed**.
- Central explicit integration selection: **2 passed in 5.32s**.
- No full suite or excluded matrices run.

Reports and commit message are written; `DONE` marker created.