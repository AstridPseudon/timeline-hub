# AP2 M2 parent authored-hold central qualification

## Result

The clean committed authored-hold candidate was run once through the unique
central App integration/e2e suite. The run reached the mounted manual video
drop test, but stopped at its first causal assertion: the deliberately wrong
verified media selection returned HTTP 422 while the test requires 404 or
409. This is not a qualification pass. The positive native `clip.add-media`
path, lost-ACK/restart/retry/reload recovery, opaque-field preservation,
duplicate prevention, undo, and zero-legacy-save assertions did not run.

No product source was changed and no rerun was made.

## Candidate and guards

- App HEAD: `9de0e009f5c50d45de402727b8eb889ee4cb7199`, clean before request.
- Central App tree: `3e3b71683d4a9fb582ddf965106b0adf4218b447`.
- Private cohort guards passed: Agent `3c4f6de4`, Runtime `202074110717`,
  producer `a0dca169`, artifact `sha256:f021e7714c1b40011b69ba624d288c217749d58013b8adf0352d283854f20fa0`,
  shared schema `6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`,
  and the locked Composition13 graph. The runner also reported
  `manifest=ecda762ebe682f266395161af055921c3db33ee9914fb00860626e7e4852d815`.
- Playwright collection found exactly one test, the mounted manual-drop test,
  before the hosted build. The hosted build passed.

## Central command and result

```sh
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test ap2-m2-parent-drop-real-central-qualification ap2-m2-parent-drop-real-central-qualification) && printf '%s\n' "$R" && /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"
```

Result: `ap2-m2-parent-drop-real-central-qualification-ap2-m2-parent-drop-real-central-qualification-1020210735-23889`, exit 1, 128s, one failed test.

Log:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/ap2-m2-parent-drop-real-central-qualification-ap2-m2-parent-drop-real-central-qualification-1020210735-23889/log.txt`

Failure: `tests/e2e/local/three-products.spec.ts:1172`, assertion
`expect([404, 409]).toContain(wrongVerified.status())`; received status 422.

## Local checks and scope

- `git status --short --branch` — clean at the candidate commit.
- No local browser, localhost, live socket, dependency install,
  API/DTO/schema/pin change, public/integration adoption, or product edit.
- The central wrapper performed the required mounted browser/build work
  outside this sandbox.

## Blocker and next candidate

The next candidate should resolve the settled private014 wrong-selection
refusal contract: determine whether the mounted fixture must assert the
Runtime's established 422 validation refusal or inject a syntactically valid
but semantically mismatching selection that returns the intended 404/409
refusal. Preserve the no-write/refusal guards and do not loosen them blindly.
Only after that is committed should the authored-hold candidate be centrally
qualified again; this worker did not test dirty source.

Note: an accidental generic `full` request was enqueued before the named
request. It is not qualification evidence; the named run above is the only
result used for this task.
