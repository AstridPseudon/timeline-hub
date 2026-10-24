Implemented in `tools/run-render-timeout-0137.sh`:

- Runs pytest with admitted child `d12c6f...`, installed profile, child-first PATH, and no source `PYTHONPATH`.
- Added durable pre/post custody reporting.
- No product, test, profile, bench, or timeout changes.

Checks:

- `bash -n`: PASS
- `git diff --check`: PASS
- Preflight: PASS
- Installed-child exact collect-only: PASS, 1 collected
- Wrong-tree guard: correctly refused

Preserved hashes: target `9efe493c`, body `ca54f2d5`, validator `361f759e`, Runtime `8ea0766f`, child Agent `521c8880`, Node `v20.19.4`, archive `819acf6b`.

The original 45-second body was not rerun in this worker; final invocation remains pending harness execution. Current script SHA: `7d8ac540...`; committed tree is pending harness commit.