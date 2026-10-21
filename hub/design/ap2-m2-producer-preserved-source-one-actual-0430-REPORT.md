# AP2 M2 producer preserved-source actual

## Result

The one authorized post-diagnosis actual was submitted exactly once against
source worker `ap2-m2-producer-final-external-hash-binding-0416` with
`--no-cache`.

Result: **FAIL**, central test ID
`ap2-m2-producer-final-external-hash-binding-0416-ap2-m2-producer-existing-graph-command-actual-e2e-integration-1021043055-14352`, exit 1, 61 seconds.

The current preflight was run once first and passed: test ID
`ap2-m2-producer-final-external-hash-binding-0416-ap2-m2-producer-existing-graph-command-preflight-1021043016-25757`, exit 0. It reported hosted resolver `0.0.13`, the pinned Composition tarball, Agent `8130a401bf44a518d5a40ae274d398b8c560be55`, Runtime `2c4ac180c2220bdad966bc01e95ad230e99ce26a`, public13 graph, private isolation, and `checks=10`.

The actual completed the hosted build (`built in 46.73s`) and reached the
single producer test. Its first failure was before the test body could run:
Playwright's Chromium launch at `tests/e2e/local/support/app.ts:43` exited
with `SIGTRAP`. The error was `browserType.launch: Target page, context or
browser has been closed`; Chromium pid 24169 launched, then exited with
`signal=SIGTRAP`.

The retained first-failure packet and trace are in:
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/ap2-m2-producer-final-external-hash-binding-0416-ap2-m2-producer-existing-graph-command-actual-e2e-integration-1021043055-14352/`

This run does not qualify producer behavior or any requested raw/order,
owned-removal/move/hold, reload, lost-ACK, restart, exact-body/key, retry,
undo, or zero-legacy assertions. No retry or repair was performed.

## Custody and prerequisites verified

- Keeper marker and lease were present:
  `workers/ap2-m2-producer-final-external-hash-binding-0416/KEEP` and
  `managers/app2/notes/producer-exact-source-keeper.lease`.
- Source keeper was clean at commit
  `97187ce3c1576559239f869067a9cef8ffb5f357`, tree
  `4acab858b0f12a1878fc231a33f3d06af9b0bdc0`, parent
  `00bbc22d63b4abe7275cfe9ad5f3762157d7394f`.
- Dependency link was exactly `node_modules -> /home/user/work/app/node_modules`;
  no install or shared dependency write occurred. The source keeper remained
  clean after the run.
- Wrapper SHA-256:
  `3069891ce3c1f56fd66d138ccd5be2960bfb0158b368209704fc215ed3761b48`.
- External runner SHA-256:
  `be59b3da5c01e0df22ec556cc84cd25a2a1a4304cf4542035829003eecb2e75b`.
- Protected graph matched: archive
  `895c628ab0727c8975247310fd0319b0f546a8d032a57072c9e364e20965ca30`,
  Composition package
  `7c806b078b00bba1593336c49a3d2953b3f8f7afc7fa9919f6d5d7ccc7c1aa61`,
  evaluation
  `e27ed545e9e0c28cf863e7bccd4a720f61e1002e04f2946dd3afca5e5f478155`,
  tarball
  `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`,
  version `0.0.13`, and 77 tarball files.
- Source pins and the exact `run`-mode argv guard were unchanged. Free disk
  was 15 GiB at completion, above the 10 GiB floor. No other producer case was
  running at submission.
- No local browser, local suite, build-only rerun, install, guard change, or
  writer cut was performed. No product or live-caller files changed. The
  assigned worktree is clean with no build output.

## Exact commands and results

Preflight command:
`request-test ap2-m2-producer-final-external-hash-binding-0416 ap2-m2-producer-existing-graph-command-preflight --no-cache`
followed by `wait-test ...-1021043016-25757`: PASS, exit 0, checks=10.

Actual command:
`request-test ap2-m2-producer-final-external-hash-binding-0416 ap2-m2-producer-existing-graph-command-actual-e2e-integration --no-cache`
followed by `wait-test ...-1021043055-14352`: FAIL, exit 1, one browser-launch
failure; no retry.

The registered actual command was:
`cd /home/user/work/wt/ap2-m2-producer-final-external-hash-binding-0416 && test "$(sha256sum -- /home/user/work/wt/ap2-m2-producer-final-external-hash-binding-0416/scripts/testing/run-producer-public13-list.sh | cut -d' ' -f1)" = 3069891ce3c1f56fd66d138ccd5be2960bfb0158b368209704fc215ed3761b48 && sh /home/user/work/wt/ap2-m2-producer-final-external-hash-binding-0416/scripts/testing/run-producer-public13-list.sh /home/user/work/wt/ap2-m2-producer-final-external-hash-binding-0416 run`

## Blocker and next steps

The settled plan and app2 `STATUS.md`/`INBOX.md` were followed. `HOME.md` was
not present in the coordination tree, so there was no HOME file to read. No
decision was changed.

The blocker is the central Chromium launch environment (`SIGTRAP`), not a
producer assertion or source/preflight prerequisite. Investigate the retained
error context and trace before any future actual is considered. Do not retry
this result blindly.
