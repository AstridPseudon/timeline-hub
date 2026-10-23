# A2 placement v2 independent review handoff — PASS

Reviewed App commit `0212bf3d18e26243afd594569794ee7dfbb2227c` on base
`1117c15f7e37a087a1175ea0e923958ce8a4132d`. The diff is exactly the four
allowed files in `commitSession.ts` and its placement/session/scalar tests.

The existing builder now emits the required v2 request metadata for automatic
placement, guarded inverse/Undo, and current semantic callers. Stable outbox
intent IDs are used for step IDs; command ordinals remain contiguous; native
captured reads/guards/created IDs remain in their original command envelopes and
evaluation boundaries. Unknown `doc.patch` uses its ordered actual changes as
the step patch, omits request reads, and forces conservative atomic mode. No
reads, annotations, dependencies, provider effects, executor, route, or reply
machinery were invented.

Independent evidence:

- Focused placement/session/scalar plus useTimelineSave recovery guards: 6 files /
  175 tests passed.
- Mounted A2 save guard `useTimelineCommit.test.tsx`: 16 tests passed.
- Private exact Composition archive
  `819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234`,
  package `0.0.14`: 8 files / 179 tests passed.
- Root/App/Node TypeScript checks, scoped ESLint, Runtime `34eac004` vendor
  lock, and `git diff --check`: passed.

No browser, live HTTP/socket/service, full suite, build, or central test-service
run was performed. No repository or shared dependency was modified by review.
The separate Proof1014 causal inverse matcher issue remains outside this task.
See the full report at
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-A2-placement-v2-review-1029/report.md`.
