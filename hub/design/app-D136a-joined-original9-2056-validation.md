# D136a/D100 joined validation

## Source receiving

- Runtime review `rt-D136a-fps-final-review-2034`: PASS_SOURCE_SECURITY, candidate `c99214a227154df5fbaf681c2e0fc52c54500025`, tree `515fca228e943e35ef2d58b5de1300aedbd9fc60`.
- Exactly three reviewed blobs were received onto base `3082cad490ce1cee764ff137f99cb791a67ddd08`; all modes are `100644` and Git blob/SHA-256 identities match the reviewed manifest.
- Worktree scope check: PASS. Only the two tracked source paths and the one reviewed additive test are changed.
- `git diff --check`: PASS.
- D100 product, D100 boundary test, and approved projection test remain byte-exact. Projection SHA-256 is `6e41a5bba04666275b9e252d7aeb30247a145207da3f9ed14f06b338563a1436`; its retained census is 43 predicates, 11 test bodies, and 54 fixture statements.

## Narrow controls

- `python -m pytest ... tests/sdk/test_d136_fps_upstream_compat.py`: 45 passed in 2.56s.
- `python -m compileall -q -f ...`: PASS.
- `ruff check` on the three received paths: PASS.
- `mypy` on the three received paths: no issues found.
- Registered-provider and immutable Runtime pin custody were retained from the qualified review; the actual run used Runtime `ab1e4f6141987706132916e2da16477f5a019464`, tree `7d8e77b2f5a4af79305c9212ce5174d3ea9fd657`.

## Actual original9

The exact unchanged nine-selector command was run once at a real pre-run free-space reading of 5,039,394,816 bytes. It returned exit 1 after 11.977741395 seconds wall time. The private XML reports 9 tests, 9 errors, 0 failures, 0 skipped, and 0 passes. Every selector failed during setup at the same first seam:

`candidate: all authored fps declarations must retain their typed locations`

No retry, adaptation, fixture migration, alternate Runtime, or substitute selector was used. Raw XML/log/metadata remain private mode 0600.

## Held scope

No full, browser, socket, native, collector, acquisition, batch, old-27, unchanged-prior9, or release run was performed.
