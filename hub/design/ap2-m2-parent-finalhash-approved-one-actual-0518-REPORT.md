# App2 M2 parent finalhash actual 0518

## Result

The one authorized `ap2-m2-parent-finalhash-actual-0517` submission was made
exactly once through the central test service. It failed in 2 seconds with
exit 1 after the custody gate passed and before any browser/request evidence
was produced. This is an execution/setup failure, not evidence of a product
failure.

Central test ID:

```text
ap2-m2-parent-complete-current-proof-source-0455-ap2-m2-parent-finalhash-actual-0517-1021052152-26621
```

The service captured App tree `a3c82aa91f1336b86491191acf857d88c56179b2`.
The exact source worker used was
`ap2-m2-parent-complete-current-proof-source-0455`.

## Exact commands and results

Approval and source preflight were retained from the 0517 report:

```text
test ap2-m2-parent-literal-digest-delta-review-0517-ap2-m2-parent-finalhash-preflight-0517-1021051812-12544: pass exit=0
```

It verified 76 artifacts, the expected manifest/schema, the frozen tree and
keeper identity, helper/driver hashes, all four negative guards, and exactly
one collected test: `three-products.spec.ts:1440`.

Final local prerequisite checks passed:

- source HEAD `a304dce02a185a4774ff514d5aa451c9702aa46f`, tree
  `a3c82aa91f1336b86491191acf857d88c56179b2`, clean;
- `KEEP` present and `node_modules` resolves to
  `/home/user/work/app/node_modules`;
- skeleton `5d36b0e53ff0d17ef045e226a6e6ca7584322858` and forwarding
  `968bbad09449f419ab63782fca49cad805068333` are ancestors;
- helper `af83e829f73ebcf9613e67808f81cab06c2e78f70c21bc850550cde1b5885fa4`;
- driver `40c7b57b6f327bafa82f26daaa4053f405e89f7bd48b5aacdadd21b2393867f0`;
- external gate `2fe1bf06d796d1342870a02a06a0d0f10057ba20bc2a29e0cad8a43deaaf16e1`;
- 14.5 GB available and the shared browser lock was idle.

The fresh local list-only command was:

```sh
(cd /home/user/work/wt/ap2-m2-parent-complete-current-proof-source-0455 && \
 PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers TMPDIR=<private-mktemp-dir> \
 node node_modules/playwright/cli.js test \
 --config playwright.three-products.config.ts \
 --grep 'M2 real mounted manual video drop' --list)
```

Result: `Total: 1 test in 1 file`, `three-products.spec.ts:1440`.
An initial local attempt used the worker's `tmpdir` marker file as a
directory and failed with `ENOTDIR` before collection; it was corrected with
a private temporary directory and passed. No product or shared dependency was
changed.

The one central submission was:

```sh
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test \
  ap2-m2-parent-complete-current-proof-source-0455 \
  ap2-m2-parent-finalhash-actual-0517)
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test \
  ap2-m2-parent-complete-current-proof-source-0455-ap2-m2-parent-finalhash-actual-0517-1021052152-26621
```

The registered command was unchanged and hash-pinned:

```sh
test "$(sha256sum -- <final-keeper-gate.sh> | cut -d' ' -f1)" = '2fe1bf06d796d1342870a02a06a0d0f10057ba20bc2a29e0cad8a43deaaf16e1' && <final-keeper-gate.sh> run
```

Central output reached:

```text
captured service tree guard passed
protected keeper guard passed
helper and driver hash guards passed
```

Then the existing durable driver returned exit 1. Its retained evidence says
`runner_status=1`; `runner-tail.log` says the runner log was not retained;
`bounded-browser-evidence.json` contains `requests:[]`, `responses:[]`, and
`console:[]`; and `evidence-presence.json` reports no trace, error context, or
request/response summary. Therefore zero browser tests, HTTP requests, ADD
bodies, or product assertions are evidenced. The first failing boundary is
the existing driver before its disposable runner log was retained; no first
request/body path exists to report.

## Preserved scope and decisions

The complete 404, ADD, raw/opaque/order, reload, lost-ACK, restart, exact
body/key, retry, undo, and `zeroLegacy` assertions were not altered. The
existing mounted live chain remains:

`TimelineEditorCore.tsx:onDrop` → `useExternalDrop.ts` →
`external-drop-utils.ts:handleFileDrop` → `useAssetManagement.ts:placePreparedAsset`
→ `useTimelineCommandsService.ts:commands.addClip` →
`useTimelineCommandSession.ts` durable parent-media session/outbox.

No deletion, source, assertion, option, timeout, pin, dependency, wrapper,
or harness change was made. The private graph archive `895c...` remains
distinct from official Composition 13 archive `9412...` (77 files), and the
final6ef/95bd cohort remains unchanged.

I did not retry: the task authorized one actual only, and this result did not
reach product behavior. No full suite, local browser/socket, install, or
source/pin change was run.

Recommended next step: the orchestrator should diagnose the unchanged durable
driver's pre-run exit from the retained execution environment before granting
any new actual authorization. No writer cut or behavior conclusion is
justified by this result.
