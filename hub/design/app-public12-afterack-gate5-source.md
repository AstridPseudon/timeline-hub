# Public12 after-ACK scheduling and Gate 5 source handoff

**HELD; source-only work complete.** Runtime 0.2.9 and the actual matching Agent/public12 pair remain **PENDING**. No browser or socket request was made. A prerequisite/source guard failure is not a semantic pass.

Worktree: `/home/user/work/wt/app-m2-public12-afterack-gate5-source`.
Base: `080a5743a` (`tl/app-m3-release12-current-safety-compose`).
Report and exact executed commands:
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-public12-afterack-gate5-source/notes/report.md`.

## Bounded delta

- Exact reviewed `5fe884946` ten-line session scheduling change: +8/-2, net **six product lines**. Appending B does not trigger automatic retransmission of uncertain A. Explicit retry/flush/recovery retains existing authority.
- Original +113 regression lines and 29-line helper recovery/preview delta, preserving current labels, loadLatest, inverse and external-edit behavior.
- Exact `bc8c2e3b6` new M2 case, with its support isolated into `prepareAfterAckLossMoves`. The original `faultFirstCommit`, `prepareDependentMoves`, all **21 existing helpers** and **six existing case bodies** are byte-identical. Copied new case differs only in the separate helper call.
- Existing strict relevant-conflict and preservation journeys remain unchanged. No new failure marker or weakened passing expectation.
- No package/root/generated/lock/runtime-pin change or native UI writer activation. The separate normal App 0.2.9 pin worker owns that adoption.

Four tracked files, +306/-13 overall. No report/build/temp output in the worktree. Integrate only the bounded logical delta; do not merge the entire candidate as qualified.

Source/test evidence: **15 files / 307 tests passed** under read-only private12 dependencies with `--maxWorkers=1 --configLoader=runner --no-cache`; scoped lint, exact source assertions and `git diff --check` passed. Playwright discovery listed **seven** cases, without running a browser. All 77 installed Composition 0.0.12 files match its immutable artifact; six peer manifests and shared cache metadata remained unchanged.

## Pending paired qualification

First compose the independently owned normal App 0.2.9 pin with this source. Publish the exact frozen Runtime and Agent source pair, with Agent on actual public Composition 0.0.12 and the same generated contract. Do not infer a final SHA from moving integration heads, reuse the old ordinary cohort, patch a digest or relax a guard. This branch still has the prior App 0.2.8 placeholder and does not itself match the required final pair.

The manager must register the following command on the existing central `app e2e-m1-gesture` lane **after** the pair is published. Replace each required environment value with the published value in the service-owned suite environment/definition; missing values must fail. The already-built hosted dist must come from the exact composed App source, with verified private12/six-peer dependencies; `ASTRID_APP_DIRECT_DIST` prevents global setup from making an implicit build. Build/normal-pin/settings qualification belongs to its separately authorized central work, not this worker.

The following is the exact future service command template, not a command executed here:

```sh
flock -w 600 /home/user/work/.app-m1-browser.lock env \
  TIMELINE_BUNDLE_AGENT_HEAD="${FINAL_AGENT_PUBLIC12_SHA:?published full 40-character Agent SHA required}" \
  TIMELINE_BUNDLE_RUNTIME_HEAD="${FINAL_RUNTIME029_SHA:?published full 40-character Runtime SHA required}" \
  ASTRID_CHECKOUT="${FINAL_AGENT_CHECKOUT:?frozen matching Agent checkout required}" \
  ASTRID_RUNTIME_CHECKOUT="${FINAL_RUNTIME_CHECKOUT:?frozen matching Runtime checkout required}" \
  ASTRID_PYTHON=/home/user/work/venv-agent/bin/python \
  ASTRID_RUNTIME_PYTHON=/home/user/work/venv-runtime/bin/python \
  ASTRID_APP_DIRECT_DIST="${PAIRED_HOSTED_DIST:?exact composed App hosted dist required}" \
  PWTEST_CACHE_DIR="$PWD/.gate5-playwright-cache" \
  PLAYWRIGHT_OUTPUT_DIR=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/browser-artifacts/${PWD##*/} \
  node node_modules/playwright/cli.js test --config playwright.three-products.config.ts --grep 'M1 real'
```

`M1 real` selects three cases: preserved M1 exact-retry/restart/undo, the new post-loss M2 Gate 5, and the preserved relevant dependency conflict. The new case uses the same mounted pointer capture, route.fetch/abort fault, native IndexedDB, reload/Runtime restart and recovery button; no fake acceptance or outbox injection. It asserts B stays unsent after A's durable acceptance/lost ACK, exact A request identity and receipt recovery, B's original guards/dependencies and new key at HA, disjoint C retention/rebase, raw closure, history, undo, opaque/transition retention, Agent show/native inputs, preview revision and zero legacy POSTs. Real semantic success requires the browser case to reach and pass these assertions.

Only after the service lane carries the published pair and exact build:

```sh
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test app-m2-public12-afterack-gate5-source e2e-m1-gesture) && \
  /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"
```

If waiting exits 124, wait on the same request again; never resubmit. Do not run browsers directly in the worker. The currently registered historical lane lacks the mandatory source pin environment and is not ready for this candidate.

After the same pair/build is registered for `e2e-m1-preserved`, the unchanged concurrent-edit/restart cases can be centrally requested separately:

```sh
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test app-m2-public12-afterack-gate5-source e2e-m1-preserved) && \
  /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"
```

Preserve real source-head, actor, realm, Runtime-instance, contract-digest, peer and secret-leak guards. Discovery/static checks do not execute or qualify those runtime guards. The full old ordinary cohort is not authorized. No full/browser/build/tsc/install/socket request was run here.
