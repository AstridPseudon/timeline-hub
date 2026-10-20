# AP2 M2 parent exact-candidate central gate

## Result

Not qualified. The exact authored-hold/valid-digest candidate reached the
positive manual-drop path, but its first causal failure was zero native commit
POSTs. The test timed out with `wire.posts.length === 0` at
`tests/e2e/local/three-products.spec.ts:1208`; the later native add, retry,
restart, reload, undo, opaque, duplicate, and zero-legacy assertions did not
run.

## Candidate and pre-build proof

- App candidate: `9de0e009f5c50d45de402727b8eb889ee4cb7199`, tree
  `9afa27b7ba22074dce31d670970007a9eecd6920`; the worktree was clean.
- The candidate contains the valid mismatching-digest fixture: the wrong
  selection changes only the final hex digit of a valid `sha256:<64-hex>`
  `object_id`. The positive path checks the original five-field selection.
- The authored-hold fix is present in
  `useTimelineCommandsService.ts`: the detached native row receives
  `hold = to - from`; the local preview/document row is unchanged. Its focused
  regression asserts `from: 0`, `to: 2`, `hold: 2` and native submission.
- Central snapshot proof: `snap` records tree
  `9afa27b7ba22074dce31d670970007a9eecd6920`; `runner.log` lists exactly one
  mounted manual-drop test before the hosted build. The build then passed.

## Central command and result

```sh
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test ap2-m2-parent-positive-drop-first-post-fix ap2-m2-parent-drop-real-central-qualification) && printf '%s\n' "$R" && /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"
```

Run: `ap2-m2-parent-positive-drop-first-post-fix-ap2-m2-parent-drop-real-central-qualification-1020211823-32057`

Result: exit 1, 191s. The private014 guards passed: Agent
`3c4f6de4fa777323b3386c01c7266b619b86af6d`, Runtime
`202074110717146fc7f08af2306a8dd7f695b0b1`, producer `a0dca169`, artifact
`sha256:f021e7714c1b40011b69ba624d288c217749d58013b8adf0352d283854f20fa0`,
schema `6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`,
and Composition `0.0.13` locked archive. The central log records one listed
test, a successful hosted build, and the source tuple with snapshot App commit
`2aff048ddb82277ad738618a493e28a2f83de5ba` whose tree is the exact candidate
tree above.

First failure:

```text
tests/e2e/local/three-products.spec.ts:1208
Expected: 1
Received: 0
Timeout: 90000ms while waiting for wire.posts.length === 1
```

Before that failure, the wrong-selection refusal, import `201`, exact selected
five-field media, and verified-selection query checks passed. There is no
valid-input Runtime response, HTTP 422, response body, or commit request body
to report: `faultFirstCommit` observed no commit POST at all. The expected
native request shape remains the test's `clip.add-media`, `select: 'parent'`,
selected five-field `args.media`, and detached row; it was never sent.

## Scope and next step

No product edits, dirty-source test, local browser/socket/script, dependency
install, full suite, pin/adoption, or rerun was performed. The prior stale
target and cancelled runs are not used as evidence. The next investigation is
the live positive path between the verified selection response and native
submit, preserving the passed refusal/draft and source/cohort guards; do not
claim qualification until a real native POST and the remaining recovery tail
pass.
