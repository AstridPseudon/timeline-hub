# P1 project-seed review handoff

## Verdict

PASS. The independent review accepts `ec8e8a25cf7ac29247d06bc5a224b94145ee71c3`
(`25140dfd23eeea6e731a4168fce10fa4bff87d8f`). No repo delta was made.

The one-line `seedOneClip` boundary correction reads the authoritative slug
from `(project.body.data ?? project.body).slug`. Runtime `34eac0041b0891e9011966b39bcbd26053fde5bc`
serves project GET as HTTP 200 with a top-level resource and serves project
creation as HTTP 201 with `data`; the DirectHarness binds all later reads to the
created `project_id`. No hardcoded/latest/fallback project identity was added.

The P1 spec SHA-256 is
`926cdadd0370f0648e03b4bba743b56c1e7c80f0ff3fa1887ba985e9bc772fd1`.
The exact two-test collection, suite ancestry guard, support environment
`38fbbc993`, Agent/runtime pins, and all original C0 v2 assertions are
preserved. The `ap2-P1-chain-h6` suite row points at this new spec hash.

Evidence passed: exact list (2 tests), `npm exec tsc -- --noEmit`, targeted
ESLint with zero warnings, `git diff --check`, and the offline recorded GET/POST
shape witness. No HTTP/socket/browser/build/full/service run was performed, so
the real two-case journey remains for the central service/manager.

See the full report at:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-P1-project-seed-review-0518/report.md`
