# Parent 590 first-failure diagnosis

## Verdict

The exact historical cause is a harness lock timeout, not a Playwright/browser
failure and not product-native behavior.

The central command retained in the 590 summary wraps the whole gate with:

```sh
flock -n /home/user/work/.app-m1-browser.lock env -i ... sh .../final-keeper-gate.base.sh run
```

The immutable corrected runner then reaches
`normal014-app-central.bound.sh:160-162`:

```sh
flock -w 600 /home/user/work/.app-m1-browser.lock \
  node node_modules/playwright/cli.js test "$@"
normal014_playwright_exit_status=$?
```

The outer `flock -n` still owns the same lock while the gate and runner are
running. The inner `flock -w 600` therefore waits on the outer command, while
the outer command waits for the gate to finish: a self-contention timeout.
Util-linux `flock` returns status 1 on that timeout. The runner labels that
captured status “Playwright child exit” at lines 162-163, but the `node
playwright` process was not reached.

The timing is consistent with this boundary: hosted build success in 57.28s,
then approximately the inner 600s wait, and suite duration 668s. The retained
runner tail has no Playwright collection/test output, Runtime/frontend output,
or reporter output after the build; its next lines are the status 1 and the
missing-summary verifier error.

## First causal boundary

- **Boundary:** harness lock acquisition before Playwright process start.
- **File/lines:**
  `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-build-heap-corrected-one-central-1145/record/artifacts/normal014-app-central.bound.sh:160-163`.
- **Outer owner:** retained suite command in
  `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/ap2-m2-parent-build-heap-corrected-one-central-1145-ap2-m2-parent-build-heap-corrected-one-central-1145-e2e-integration-1021114743-590/summary`.
- **Classification:** harness/setup timeout; not child RC, browser timeout,
  retention loss, Runtime failure, frontend failure, or product-native failure.
- **Secondary failure:**
  `run-parent-manual-drop-evidence.sh:69-75` verifies
  `three-products-summary.json` after the lock command. Since Playwright did
  not start, the verifier reports ENOENT and preserves a synthetic bounded
  summary with empty requests/responses/console arrays. That is a consequence,
  not the cause.

## Retained packet and preservation

Fresh 590 packet:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-build-heap-corrected-one-central-1145/record/evidence-central-corrected/run/`

Its retained facts are `runner_status=1`,
`run_root_cleanup=after-evidence-copy`, and
`trace=false`, `error_context=false`,
`request_response_console_summary=false`. The 590 source manifest records the
central log hash `3467685311347af866c59aba9ae25fb4b57cc79498a3893af1506ac9df4443e5`
and summary hash
`c71bb8228c1947483ba0b04388b9c9501602ab2833bcb6ae7226ec693bbde6fa`.
The current retained packet hashes are:

```text
runner-tail.log              f04c9d1117a23eba84a99bffda51132b7d76fdccd9e04dc3961445ea31a204f0
bounded-browser-evidence.json 541e9140ccd10769da387f38baed4e060a2eccf63c85581f8279e2fc5f51aa0b
evidence-presence.json       4c12877acca2384c40551bd54d576b77066237771c425c5f176655f47776fee3
result.txt                   6afccb5b43a157a7f5bc8cdb2dce50e3f6c196db3420f6082169f13ce1775ae9
retention.log                c5410c8014ec39b4476d5918a05d6f147fda9a0cba263817dfc21553ab8f6149
sourceHASH-manifest.txt      d5162b53c008dc7bf2b6054e11b1c95f06b65e1aeb03ab4a0bd37bd8e968c7c3
source-identity.txt          ac6e278a580236a58372a03eb8daae5a35420f9d934044412c22fb0a52f5748b
```

The old 1384 packet was read-only checked and left unchanged. Its manifest
continues to record the old central log hash
`595b3ebcced1a549f72bb950f956195f58a04e82e3279c44e2a507bdf63ae31b`, summary
hash `54cf87e189df1a5b339391e6f29bbaf6bc8935be26ef6afe5f4064072c5793af`, and
packet manifest hash
`d0187c95e917f3d4be2e6d5919d657d3fc3da5a2d124e5f4aca71b3a347496be`.

The parent-owned disposable run root was removed after evidence copy, as
recorded by `retention.log`; no retained test-lock file was removed. The
retained aggregate preflight recorded the local-browser-lock probe as PASS,
and no other process, worktree, branch, or historical packet was killed or
removed by this diagnosis.

## Reached and unreached

Reached: source/keeper/hash guards; 76 locked Runtime artifacts; private graph
(532 packages/34 bins); hosted build of 5586 modules in 57.28s; post-build
runner status handling and evidence retention.

Unreached: Playwright CLI process; global setup; Runtime daemon/browser door;
Chromium; frontend; test reporter; any browser request/response/console; all
manual ADD, strict 404, raw/order/opaque, lost-ACK, restart, exact retry, undo,
and zero-legacy assertions. No product-native conclusion is supported.

## Smallest correction / peer request

Manager/orchestrator authorization is required for one successor. Keep the
frozen source, test body, assertions, pins, graph, credentials, and timeout
unchanged, but make lock ownership single-layered: remove the outer central
`flock -n /home/user/work/.app-m1-browser.lock` wrapper and let the existing
runner’s `flock -w 600` at lines 160-161 serialize the browser stage. Then run
the already-approved preflight and, only if authorized, one successor central
execution. Do not change product routes/selectors or infer browser evidence
from this failed run.

## Commands and results

Read-only commands used:

```sh
sed/nl/rg/find/sha256sum on PLAN.md, the 1145 report, the 590/1384 retained
packets, the frozen App tree, and the preserved runner/config sources
```

Results: source identity and all requested retained hashes were inspected;
590 and 1384 packets were preserved; no repository source was modified. No
test, build, browser, socket, service, registration, retry, or full-suite run
was performed, per task.
