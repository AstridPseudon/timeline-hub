Implemented F-D09 source-profile invocation harness and one named test-service row.

Tests:

- `bash -n run-d09-current-invocation-2255.sh` — passed.
- `git diff --check` — passed.
- Final service run: `3 passed in 510.58s`.
- Exact original three D09 nodeids collected and passed.
- Final profile: `source`; pinned child interpreter, Runtime `8ea0766f`, Node `v20.19.4`.
- Source/test hashes, origins, manifest receipt, stderr, and no-write evidence recorded under the worker evidence directory (96 KB).

Two bounded corrections were required: Runtime imports are source-owned in source mode, and the Node toolchain must be on PATH for registry probing. No product code or guards changed. Full suite remained untouched.

Commit message and `DONE` marker created.