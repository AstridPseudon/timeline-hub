Implemented OPS-D29 return artifact:

- Extended `request-runtime` for explicit eighth `NODE_BIN`, preserving legacy shapes.
- Preserved maker guards and added physical-directory rejection for symlinked toolchains.
- Added canonical patch, manifest, and committed finite carrier fixture.

Tests passed:

- `patch --batch --fuzz=0` + `cmp` for both scripts
- `bash -n`, Python compile, JSON validation, `git diff --check`
- Fixture: `PASS cases=14 ... store=0 build=0`
- Manifest hash verification

Actual approved Node/npm files remain absent in this sandbox, so production receipt qualification is unverified. Commit message and `DONE` marker created.