# App M2 producer physical approved-one-actual — 0552

## Result: HOLD — no producer actual submitted

Worker 0551 returned a concrete **HOLD**, not the required custody
**APPROVE**. Per the task gate, dependent execution stops on that HOLD. I did
not submit the original producer case, browser, hosted build, local daemon,
full suite, install, retry, or any source/assertion/selector/timeout/pin
change.

The blocking review is
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/ap2-m2-producer-physical-startup-final-custody-0551-REPORT.md`.
It identifies three concrete qualification defects:

1. There is no authoritative central source-preflight/startup-only result for
   the final successor tuple.
2. `producer-startup-only-gate.sh` invokes the worker-owned probe and `tsx`
   without literal hashes binding those bytes before invocation.
3. No named central suite entry or literal command exists for the startup-only
   gate; the 0545 startup gate also does not rerun the successor's inherited
   drift/unknown-mode/zero-test/child-RC guards as a central result.

The 0545 worker still has a `running` marker and no report/result. Its artifact
existence is not treated as daemon-health evidence. The 0538 report explicitly
said startup proof was not run. No result was relabeled or reused.

## Frozen source and prerequisite audit

Read-only identity and cleanliness checks in this worktree:

```text
git rev-parse HEAD                                      b8cc7e1c79ec5516b9eee3832b5c33d62dac1aa7
git show -s --format=%T HEAD                            fd16d32fd3487e56c9fe1ff16582dba240f63b77
git status --porcelain --untracked-files=all             clean
scripts/testing/run-producer-public13-list.sh           329cfca7ff6fcc6764e5eaa6cb53ba77a40e6aa842361d0ed6795ca5b4398352
tests/e2e/local/producer-ownership-current-pin.spec.ts  d91d0c1cce22f68119cd30fcb0a288346474b0ad4b64c84dcee3b730fa468d89
tests/e2e/local/support/producer-ownership-current-pin.ts
                                                         50cbe5341f24c9a1ecc999018e2c6d975380a3440570abce151f9173c9752016
playwright.producer-ownership-current-pin.config.ts      5b880ceff883abce2575a3a85aaa4eda69d3bcb848768ff0e91f337d50cca4c0
Agent commit/tree                                          8130a401bf44a518d5a40ae274d398b8c560be55 /
                                                         236c3e57e0265c52b81ba8085de3193026176bff
Runtime commit/tree                                        2c4ac180c2220bdad966bc01e95ad230e99ce26a /
                                                         7ab412cc4bcbe517efcfa806e092336390312e18
```

The successor custody artifacts are present with the hashes reviewed by 0551,
but are not a PASS result:

```text
producer-physical-keeper-gate.sh                         c365641bdeca10b9d740d5968c9a1161db7b18f8bf49e9d8bd46f14aae60cfab
producer-startup-only-gate.sh                            8f3be0c8fcb18ab474b8d5b31c8b6a17b1cdc3d02324b4159d184c266357013c
producer-startup-only-probe.ts                           4beb7c22dfa06e04d28253dbab02f76ff2a9953f0accd4b12247514e4f0608f6
```

Additional read-only checks:

```text
App node_modules -> /home/user/work/app/node_modules                    PASS (normal link)
locked graph node_modules -> physical path                             PASS
locked graph source archive SHA-256 = 895c628ab0727c8975247310fd0319b0f546a8d032a57072c9e364e20965ca30
                                                                         PASS
df available = 13,686,976 KiB                                           PASS (> 10 GiB)
flock -n /home/user/work/.app-m1-browser.lock -c ':'                   PASS (AVAILABLE)
short tla-* run roots at audit time                                      none
0552 worker-owned run roots                                             none
```

No source copy, dependency, graph, lock, or shared-cache file was modified.
No local browser or daemon was launched.

## Original case, command, and callers

No final approved central actual command exists because 0551 did not approve
one, and no actual was submitted. Therefore the new central test ID and result
count are **N/A**; there is no new pass/fail and no first failure to capture.
The preserved original target is:

```text
test: tests/e2e/local/producer-ownership-current-pin.spec.ts:87:3
title: removes only stale owned transcript output and moves only owned scene output
collection contract: exactly 1 test in 1 file
```

The prior 0532 result (`1 collected, 0 passed, 1 failed`) was the old
`17d2518c`/`d63fe4f` tuple's Runtime symlink startup failure and was not
replayed or counted as evidence for this `b8cc7e1` candidate. Consequently none
of the original ownership, raw/order, reload/retry, undo, or zero-legacy
assertions ran in 0552.

Live source callers remain unchanged:

- `scripts/testing/run-producer-public13-list.sh` forwards the existing npm
  `run test:e2e:three-products -- --grep 'M2 ordinary extension batch'` shape
  and invokes the Playwright config/spec for list/run modes.
- `playwright.producer-ownership-current-pin.config.ts` selects
  `producer-ownership-current-pin.spec.ts`, one worker, 300-second timeout,
  and zero retries.
- `tests/e2e/local/producer-ownership-current-pin.spec.ts:87` is the sole
  original test case and imports the unchanged helper.
- `tests/e2e/local/support/producer-ownership-current-pin.ts` supplies the
  unchanged fixture/observation helpers.

## Exact commands and results

Executed read-only audit commands included:

```sh
git rev-parse HEAD
git show -s --format='%T %H %s' HEAD
git status --porcelain=v1 --untracked-files=all
sha256sum scripts/testing/run-producer-public13-list.sh \
  tests/e2e/local/producer-ownership-current-pin.spec.ts \
  tests/e2e/local/support/producer-ownership-current-pin.ts \
  playwright.producer-ownership-current-pin.config.ts
realpath node_modules
realpath "$LOCKED_GRAPH/node_modules"
git -C /home/user/peteromallet/astrid-agent show -s --format='%H %T' 8130a401bf44a518d5a40ae274d398b8c560be55
git -C /home/user/banodoco/banodoco-workspace-runtime show -s --format='%H %T' 2c4ac180c2220bdad966bc01e95ad230e99ce26a
df -Pk .
flock -n /home/user/work/.app-m1-browser.lock -c ':'
```

All listed checks passed. The producer wrapper, startup gate, source-only
preflight, central startup smoke, Playwright list, and actual run were **not**
executed by 0552 because the explicit 0551 HOLD makes dependent execution
unauthorized. There is no central actual result directory for this tuple.

## Required next step

The prerequisite owner must correct the 0551 custody defects by literal-binding
the startup gate, probe, and exact `tsx` bytes, registering one named central
source-preflight/startup-only suite that includes the successor's inherited
guards, and producing a central PASS with real daemon health and teardown,
zero producer body/case execution, and the exact frozen environment. A fresh
independent custody review must then explicitly say **APPROVE** before the one
original actual is considered.
