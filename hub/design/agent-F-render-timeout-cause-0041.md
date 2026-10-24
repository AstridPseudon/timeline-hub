## Report

Inspected the settled plan, retained longrepr, source hashes, subprocess path, process graph, runtime, and profile custody.

Classification: harness/transport timing, not Node resolution, Remotion rendering, or a Three.js predicate failure.

- Original 21-node run: 16 passed / 5 failed; four failures were missing Node/Npx from PATH.
- PATH-qualified service `10359`: 4 passed / 1 timeout.
- Remaining timeout: `test_threejs_support_rejects_unsupported_timelines_with_clip_reasons`, 45.005s, blocked in `CommandTransport.process.communicate`.
- Exact child preflight: 15.386s, valid `supported: true`, empty stdout/stderr; Node `v20.19.4`, npx `10.8.2`.
- Child graph is Python support process only; this path does not launch Node, npx, or Remotion.
- Source/test bodies, Runtime `8ea0766f`, profile archive `819acf`, registry, and Node 20 custody remained unchanged.
- No unchanged test-body rerun; no product, timeout, test, dependency, or backend changes made.

Checks:

- `bash -n tools/run-render-cohort-0013.sh` — passed.
- `git diff --check` — passed.
- Worktree remains clean.

Blocked owner: rendering transport/qualification harness. Fixing this requires authorized child-process reuse/startup optimization or timeout-policy restructuring, both outside this task’s permitted scope.