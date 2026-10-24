## Report

Implemented harness-only identity fix in [tools/run-render-wire-0124.sh](/home/user/work/wt/agt-F-render-wire-return-0129/tools/run-render-wire-0124.sh).

- Requires manager-supplied exact snapshot tree; no `HEAD`/parent assumption.
- Locks canonical 19-file source manifest and six test-body hashes.
- Wrong source-tree expectations refuse.
- No product/test bodies changed.

Updated suite row:

```text
agent render-wire-0124 test "$(git rev-parse HEAD^{tree})" = abc038fadf8f6ee1b995ff1325c19fb1ab940adc && test "$(sha256sum tools/run-render-wire-0124.sh | awk '{print $1}')" = d1df6818a3db6ae9aa426cfc8b3e5560b43116a11333241156117428c6665aad && env -i HOME=/root LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONDONTWRITEBYTECODE=1 EXPECTED_SOURCE_TREE=abc038fadf8f6ee1b995ff1325c19fb1ab940adc PYTHONPATH="$PWD:/home/user/work/wt/rt-pin-8ea0766f" PATH=/home/user/work/bench-store/entries/child-c886d448c07fe72421bfbc708db0dc9399c2833a66b7dadc67625a3df0d4da0e/bin:/usr/bin:/bin ASTRID_HOST_EXECUTION_PROFILE=installed ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-8ea0766f ASTRID_RUNTIME_SOURCE_ROOT=/home/user/work/wt/rt-pin-8ea0766f ASTRID_REMOTION_PROJECT_DIR=/home/user/work/runtimes/agent-remotion-v3-819acf-1110 ASTRID_NODE_EXECUTABLE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node ASTRID_TEST_NODE_MODULES=/home/user/work/runtimes/agent-remotion-v3-819acf-1110/node_modules ASTRID_TIMELINE_SCHEMA_PYTHONPATH=/home/user/work/venv-agent/lib/python3.13/site-packages bash tools/run-render-wire-0124.sh
```

Evidence:

- Old 4492: failed only Agent identity (`HEAD=64489…`, parent `f550…`, tree `e45…`); all other preflight checks passed.
- New metadata-only preflight: `PASSED`, 19 source files and 6 bodies byte-identical.
- Wrong-tree control: refused with `FAIL Agent source identity`.
- `bash -n tools/run-render-wire-0124.sh`: PASS
- `git diff --check`: PASS
- Six render bodies were not executed, as required; central manager should queue one original six-case run.

Current source: `HEAD=f550018b…`, tree `e45ec8dc…`; finalized snapshot tree: `abc038fadf…`.

Commit message written and `DONE` marker created.