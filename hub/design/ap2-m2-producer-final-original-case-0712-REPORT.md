# App M2 producer final original case — 0712

## Verdict

Custody closure: **APPROVE**, using the independent 0703 approval and the
unchanged startup evidence. The one authorized original producer actual then
**FAILED before producer behavior**. Per the first-failure rule, I retained the
exact central packet and did not retry or delete any writer.

## Exact command and identity

Target source was the required `ap2-m2-producer-realm-physical-path-diagnosis-0538`
snapshot, never this checkout or an integration worktree:

```text
App b8cc7e1c79ec5516b9eee3832b5c33d62dac1aa7 / fd16d32fd3487e56c9fe1ff16582dba240f63b77
Agent 8130a401bf44a518d5a40ae274d398b8c560be55 / 236c3e57e0265c52b81ba8085de3193026176bff
Runtime 2c4ac180c2220bdad966bc01e95ad230e99ce26a / 7ab412cc4bcbe517efcfa806e092336390312e18
custody gate ffeaa34c944b931a0e2f393156dd3dc78cb39318bf24c64bb4073e2b6b3d5a20
source gate c365641bdeca10b9d740d5968c9a1161db7b18f8bf49e9d8bd46f14aae60cfab
wrapper 329cfca7ff6fcc6764e5eaa6cb53ba77a40e6aa842361d0ed6795ca5b4398352
```

Registered and submitted once, with `--no-cache`, as:

```sh
test "$(sha256sum -- /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-health-conversion-review-0703/artifacts/producer-startup-custody-gate-owned.sh | cut -d' ' -f1)" = ffeaa34c944b931a0e2f393156dd3dc78cb39318bf24c64bb4073e2b6b3d5a20 && sh /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-health-conversion-review-0703/artifacts/producer-startup-custody-gate-owned.sh run
```

Suite: `ap2-m2-producer-final-original-case-0712-actual-ffeaa34c-integration`

Test ID:
`ap2-m2-producer-realm-physical-path-diagnosis-0538-ap2-m2-producer-final-original-case-0712-actual-ffeaa34c-integration-1021071230-18664`

Result packet (retained):
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/ap2-m2-producer-realm-physical-path-diagnosis-0538-ap2-m2-producer-final-original-case-0712-actual-ffeaa34c-integration-1021071230-18664/`

## Counts and first cause

```text
exit 1, fail, 81s
1 test collected / 0 passed / 1 failed
test: tests/e2e/local/producer-ownership-current-pin.spec.ts:87:3
title: removes only stale owned transcript output and moves only owned scene output
```

The first failure was:

```text
ReferenceError: expect is not defined
at support/producer-ownership-current-pin.ts:229
await expect(firstTrackName(page)).toBeVisible();
```

This is the unchanged helper and occurred in `openCurrentPinTimeline`, before
the transcript regeneration or scene move producer actions. No producer commit
request/body was observed; no writer deletion occurred.

The original foreign/user ownership, raw/order preservation, reload/retry,
lost-acknowledgement, undo, and zero-legacy assertions were therefore
unreached. The exact Playwright error context and trace remain in the retained
central result packet. No retry or second central submission was made.

## Closure checks and reused evidence

Reused without replaying unchanged smoke:

- 0703 independent custody APPROVE, offline review 22/22.
- Startup preflight test ID `...health-conversion-review-0703-preflight-1021070615-7825`, PASS.
- Startup-only test ID `...health-conversion-review-0703-startup-1021070652-30920`, PASS, including physical TMPDIR Runtime startup, planted symlink refusal, direct/door identity, teardown, and zero producer/body execution.

Before the actual, read-only checks passed for the literal gate/probe/tsx,
source/body/helper/config/graph hashes; service tree versus protected keeper
HEAD/tree; frozen Agent/Runtime pins; intended original selector and one-test
list/run guard; physical TMPDIR guard; clean keeper with 5,912 regular files
and 2 symlinks; no keeper scratch artifacts; nonblocking browser lock; and
12,790,744 KiB free (>10 GiB). The final source and protected keeper were both
clean at the App tuple above. The one-line central suite registration was the
only orchestration change; no App report or `.gitignore` was edited.

The literal custody values were:

```text
startup gate 4963a1eb47f84c58ed51f271a581604339eda61547a817019e0e273eee668e41
startup probe a062cab11ea3a86ef75ece5a86584d0555040336032ced515d6ac50de9481d8f
format probe d4eeaeb74a582fe9ccb94c1cfba7f66c41ec50eef7823db34f61ed7185e12af3
tsx bin/cli 8729ecfb90d9d568939e4190e6f1d3317c946583b7d37a776e0c23a21c021cf8
tsx loader 0b1c5b86192772fe9257710e739959cee5947c11ae1f93b61abfaa9b80c6def1
tsx package 6e764b21991c21595441f82387c1451ccd10a3e7a3f0973cc5e3649a12dea7d2
body commit/tree 36dd91257fd13dcad0d58b48c790caa5063b4c8c / d908845dbc8e5ebf96698d08621557e904f20c52
spec d91d0c1cce22f68119cd30fcb0a288346474b0ad4b64c84dcee3b730fa468d89
helper 50cbe5341f24c9a1ecc999018e2c6d975380a3440570abce151f9173c9752016
config 5b880ceff883abce2575a3a85aaa4eda69d3bcb848768ff0e91f337d50cca4c0
graph archive 895c628ab0727c8975247310fd0319b0f546a8d032a57072c9e364e20965ca30
```

The retained selector is the existing wrapper path
`run test:e2e:three-products -- --grep 'M2 ordinary extension batch'`, which
forwards `playwright test --config playwright.producer-ownership-current-pin.config.ts
tests/e2e/local/producer-ownership-current-pin.spec.ts`; its unchanged list
branch requires `Total: 1 test in 1 file`, while this one-submit actual used
the corresponding `run` branch.

Executed by the actual: existing wrapped hosted build and browser, Playwright
collection of exactly one test, page navigation/connection setup, and the
first helper visibility call. Unreached by design or first failure: producer
actions, Runtime commit traffic, ownership mutation, reload/retry, undo, and
all remaining assertions. No local socket, install, full suite, or startup
smoke replay was run.

Recommended next step: fix or explicitly qualify the missing Playwright
`expect` import in the existing helper through the normal review path, then
obtain a new custody decision before any future actual. Do not treat this
run as producer ownership behavior evidence.
