## Report

Implemented one named test-service row and installed-child proof harness.

Tests:

- Preflight: passed; exact six-node collect passed.
- `3 passed, 3 errors in 52.14s`.
- Passed: startup identity, Remotion host session, selected generic-host node.
- D09 three nodes errored during setup at the existing installed-registry guard (`RemotionValidationError`), before test bodies.

Qualification evidence:

- Managed child: `child-c886d448...`
- Agent c36, Runtime abd47 via `rt-pin-8ea0766f`
- Installed origins, RECORD/direct_url, Node v20.19.4, schema path, and immutable819acf profile verified before/after.
- `PYTHONNOUSERSITE` and unsupported variables absent.
- Original test hashes unchanged; evidence is ~60 KB.

The D09 boundary is a harness/profile invocation incompatibility: installed mode rejects the fixture’s explicit source `PYTHONPATH`/pack roots. No retries were made. Full SAME25691 remained untouched.

Commit message and `DONE` marker recorded.