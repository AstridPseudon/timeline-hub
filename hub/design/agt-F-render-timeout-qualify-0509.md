## Report

Implemented read-only harness: [tools/run-render-timeout-qualify-0509.sh](/home/user/work/wt/agt-F-render-timeout-qualify-0509/tools/run-render-timeout-qualify-0509.sh).

Preflight passed:

- Current Agent: `9cd3dbe865`; installed child Agent: `ba8f0bc8be`; Runtime: `f3208b26b5`.
- Installed-only import origins verified; relevant rendering files byte-match installed child.
- Target body hash: `ca54f2d5…f3ded82`; 9 assertions; matches `ba8f`.
- Node `v20.19.4`, profile `819acf`, receipt verified.
- No product/test/runtime/profile changes.

Test command executed once:

```text
child/bin/python -P -m pytest -q --import-mode=importlib -o addopts= -p no:cacheprovider --timeout=45 tests/packs/rendering/test_threejs_backend.py::test_threejs_support_rejects_unsupported_timelines_with_clip_reasons
```

Result: **failed**, `1 failed in 45.65s`.

The actual production path reached `support → _support_report → CommandTransport.run`, then blocked in `process.communicate` during the second support probe. No Node, Remotion, browser, raster, or MP4 path was reached. Cause remains unknown; no registry-cause inference made.

Evidence is retained under the worker’s `evidence/` directory. No second body run was attempted. Qualification is marked `BLOCKED`; commit message is written to the requested path.