## Report

- Added observational harness: [run-render-support-probe-0530.py](/home/user/work/wt/agt-F-render-support-probe-0530/tools/run-render-support-probe-0530.py).
- Ran exactly one synthetic transition probe through the production caller.
- Evidence: [diagnostic.json](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-render-support-probe-0530/evidence/diagnostic.json).

Result: one child completed normally:

- Spawned/owned child PID 19.
- Result absent initially, then present at 840 bytes.
- Return code: `0`.
- stdout/stderr: empty.
- Total caller time: `8.79s`.
- No Node/browser/real render/MP4 path reached.

Qualification remains blocked: `ASTRID_HOST_EXECUTION_PROFILE` was missing from the sanitized child environment, and the child fell back to the installed package’s nonexistent `remotion` path. This does not prove a registry cause.

Checks:

- Harness syntax compile: passed.
- `git diff --check`: passed.
- Original test body: intentionally not rerun.
- Full/broad suites: not run.

Smallest next step: authorize a narrow environment-policy fix to preserve the existing installed-profile selector, then repeat one bounded probe. Commit message and `DONE` marker were written.