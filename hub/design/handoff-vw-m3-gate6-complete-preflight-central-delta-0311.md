# Gate6 complete preflight handoff

The reusable read-only aggregator is:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-gate6-complete-preflight-central-delta-0311/preflight-only.mjs`

It reuses the reviewed controller guards, catches every independent failure,
records `statfs` before/after each step, and has no grant/marker/browser/
Runtime/service side effect. Final result: 16 checks passed; failures were
Runtime physical isolation, its 21,421 shared-file census, the dependent
frozen-graph guard, and current disk before/after-stage headroom. Current
free bytes were `10,704,015,360`; exact needed bytes to meet the measured
minimum were `348,073,984`.

The 0258 snapshot measurement remains exact: `314,671,104` allocated bytes,
requiring `11,052,089,344` bytes before staging for a 10 GiB after-stage
floor. 0304 had only `24,231,936` bytes above that minimum at pre-request;
its later post-failure observation fell by `86,974,464`. Central failure-time
free bytes for 32009 and 16444 were not emitted and remain unknown. The
retained App909 source/tree and ignored `dist`/`node_modules` paths are
unchanged; no protected path was touched. See the worker REPORT for exact
paths and commands. No third physical request is authorized.
