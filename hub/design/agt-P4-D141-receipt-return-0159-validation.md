# P4 D141 immutable receipt return validation

Status: `PASS_READ_ONLY_CORRECTION_RETURN`.

This return is a same-author-lineage, finite metadata correction from base
`tl/agt-P4-D141-immutable-receipt-0151` at `5d11fec5ccf3ce1b314ef5c24216a1d802d56ffd`.  The only new semantic
field is provenance for the prior 39-character serialization of
`frozen_tuple.agent.tree`; the omitted final character `a` is restored to the
40-character Git tree `2ebe2ddf5a61f013953ab1e21d51ebaab746e58a`.  No body or kit work
was performed.

Independent post-write checks read `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-P4-D141-receipt-return-0159/evidence/correction.json` and
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-P4-D141-receipt-return-0159/evidence/source-manifest.json` back from disk.  They passed:

- all four pinned commit/tree pairs were recomputed with read-only `git show`:
  Agent `28e56cacb42d3da85b02e5b3543895b44f3d0f70` / `2ebe2ddf5a61f013953ab1e21d51ebaab746e58a`, Runtime `6a011d58e69173d70e2e9bb3ac434ac8f9e87d8d` / `ac5b862744bece65b2e30565db1777bacd60da28`, App `867cb2737af1b46dc608c7cd37c349e920fe9422` / `2b44a46ca51d880c6a00da4c19aa8629b55eb7dd`, and Composition `635f4de06fda22a85fc2e4cfc764d0153a4c9f40` / `5ab5191a296980a0a6bcd1178ab6902d6478a148`;
- 28 path-bound SHA-256 records in the emitted JSON were independently recomputed against their actual files;
- the retained 0055 manifest and runmanifest remained `67ef4348b4b77eb02b74abe20ad6fefdb075f980dc8ca563c0a3c79d1f0e5b9f` and `86595e66a6739d9d6c9cdaa5fe583c4b7eff50a5f2ba5aec4e620df91104dc71`; their declared 0047 XML path remains absent;
- the emitted receipt binds the actual effective XML `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-P4-D141-operational-return-0055/evidence/body-evidence/p4-d141c.xml` with SHA-256 `afca45b778f118b22f30e2cac08654a902dd86241b76442f146ae0ad8623316d`;
- `shlex` parsed the retained production argv, finding exactly three concrete selectors and the effective XML destination;
- stdlib XML parsing found 3 tests, 3 passes, 0 failures, 0 errors, 0 skips, and exact time `23.668` seconds;
- original 10086 remains distinct from historical 1347, and queued 19479 remains queued/unstarted with no exit or XML, as recorded by the retained source receipts;
- the original 0151 evidence files, retained 10086 inputs/artifacts, and original 0114 custody review were byte-identical before and after output creation (26 originals hashed).

No pytest/import/collection/body/control/typecheck/lint/installation/network or
product operation was run.  This packet does not convert the original 0114
custody `FAIL`, does not substitute the later 0119/95f5 manifest, and does not
claim a P4 GO; App owns the cumulative verdict.
