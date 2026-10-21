# AP2-M2 current95 parent File/media gate

## Source approval

The required 0138 custody review approved the exact frozen parent source and
helpers in `ap2-m2-final95-frozen-source-custody-review-0138-REPORT.md`.

- App parent source: `25155ccb22728780a3ecd6379a929cad75cc1400`, tree
  `972d2ed2e4f85f334eb9f2e6ca40d9bfbce9eac7`.
- App pin bytes: unchanged from approved `10fa2ff9a8216604aa39e3584f89dc9e7a09080a`.
- Agent: `6efc81500a0e0688c2bb41e736503f0fc3e04abb`, tree
  `2ed2b8a12b5b3391ca221ba6ff05390f71a73556`.
- Runtime/producer: `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`, tree
  `d3a290b407fa61e6ab2d476f50c068073f70df00`.
- Runtime artifact: `sha256:54205b3ecb55038e416b31af936c9af26afa30dc1b05da16157ee4d861fe05ac`;
  76 manifest entries.
- Raw schema: `sha256:6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`.
- Public13 archive: `sha256:895c628ab0727c8975247310fd0319b0f546a8d032a57072c9e364e20965ca30`;
  all 77 guards retained.
- Approved helper hashes: `normal014-source-common.sh`
  `3b2018de1fbc123135590c37d4b17e995fd194fc39089b793e3f1b82e742bd56`,
  `normal014-parent-media-central.sh`
  `1d2ebce742bab9a20a911baedab8e7e318e82d6f1043f7f554949855acf646fd`,
  `normal014-app-central.sh`
  `c18d79205ca3b6af4a679ecef9cba0c11a1c3afee23b1daa56d95f109bedbf20`,
  and `tests/suites.conf`
  `9bb3b11d4e7292adb4ca9ca40203a86eeb815911a5896c1a23ccca2a3f39fbc7`.

## Single central request

Submitted exactly once, after approval:

```sh
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test ap2-m2-parent-frozen-source-single-gate-0138 normal014-integration-parent-media-accepted --no-cache) && /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"
```

Result directory:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/ap2-m2-parent-frozen-source-single-gate-0138-normal014-integration-parent-media-accepted-1021014332-27865`

Result: **FAIL, exit 1, 1 second**. The central summary recorded App tree
`972d2ed2e4f85f334eb9f2e6ca40d9bfbce9eac7` and the exact command with
`NORMAL014_PROFILE=final95 NORMAL014_APP_SOURCE=parent`. The retained
`log.txt` and `runner.log` are empty and the summary reports no test counts;
therefore no parent case reached execution and no structured required-case
verdict was available. The failure cause is not exposed by the sanitized
central result, so it is reported as a pre-case runner failure rather than a
product assertion.

The gate is **not qualified**. Genuine File input, raw/order preservation,
reload, undo, lost-ACK/restart, exact retry, and zero-legacy behavior have no
central case evidence from this run. No retry, local browser, full suite,
bootstrap case, source change, pin adoption, or public activation was done.

## Local state

The worker worktree remained clean at the approved source root. Shared
dependencies, artifacts, runtimes, and virtualenvs were not modified.
