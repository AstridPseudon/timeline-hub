## Report

- No code changes needed: the fix is already integrated in `c8e87e5e` and present in `tl/integration`.
- `native_host` is re-exported through the normal rendering conftest seam and imported by the RLE test.
- Scoped worktree is clean; test body/assertions unchanged.

Verified:

- Collection: 1 test collected.
- Setup plan: `host_project` → `native_host` resolved successfully; no fixture body ran.
- Initial collection without Runtime `PYTHONPATH` exposed the known missing `runtime_protocol` environment issue.

Not run: actual native host, renderer/helper/browser/runtime, full suite, or conformance nodes.

Artifacts: [report.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m4-rle-native-host-fixture-source-repair-0748/report.md), commit message, and `DONE` created.