# Parent final body actual report

## Result

**FAIL — first real native failure; no rerun.** The exact centrally submitted
actual lane collected and executed one test, but native ADD qualification did
not reach its first ADD post.

- Test ID: `ap2-m2-parent-final-body-approved-one-case-0629-ap2-m2-parent-pin-final-acb-explicit-0617-actual-1021062952-11497`
- Suite: `ap2-m2-parent-pin-final-acb-explicit-0617-actual`
- Source/target: `ap2-m2-parent404-door-body-exact-correction-0604`
- App HEAD/tree: `acb582c2c3b08481d43853b8526894ac60d074bc` /
  `141724b56736be40a269f60aa8bfc060914ebd29`
- Outcome: exit 1, 171 seconds; `1 failed`, `0 passed`
- Collection/execution: `1` collected, `1` executed; no zero-test condition

## Exact command

```sh
request-test ap2-m2-parent-final-body-approved-one-case-0629 \
  ap2-m2-parent-pin-final-acb-explicit-0617-actual
wait-test ap2-m2-parent-final-body-approved-one-case-0629-ap2-m2-parent-pin-final-acb-explicit-0617-actual-1021062952-11497
```

The registered command retained gate
`515931b8700aba3bf7b1a98e5013ecbe3c5769925b9ce21e44f4fb03b1a4a1e5`, helper
`d9a691dcaafd7d544a467445a3a020a9ad3d02afc1d527870f00be6948fea848`, driver
`34ee03d1ea6f25ae4f68b8965f5c9b050d8892214416ec3bf551dfa81b17a2d2`,
`NORMAL014_PROFILE=final95`, `NORMAL014_APP_SOURCE=parent`, and
`NORMAL014_USE_BASE_PYTHON=1`. The preflight and four refusal controls passed.
The accepted preflight `…-1021062025-31285` also retained the 76-artifact
manifest/schema, locked graph, clean keeper/KEEP/normal dependency link and
ancestry, local resource/copy guards, wrong-argv refusal, and list count 1;
the actual run rechecked the captured tree, keeper tuple, and helper/driver
hashes before entering the browser phase.

## First real failure and scope

The required case was `tests/e2e/local/three-products.spec.ts:1440`.
The 404 refusal/body phase passed: the wrong verified selection returned 404
with `code=not_found`, the exact message, and the reviewed `request_id`
pattern. The normal import/selection phase also reached POST 201, selection
200, and verified 200.

The first failure was at line 1557, while waiting 90 seconds for recovery:

```text
Expected: attempts: 1
Received: attempts: 0
```

Therefore ADD/raw/opaque/order/reload/lostACK/restart/exactbody/key/retry/
undo/zeroLegacy were not executed or qualified. In particular, no native ADD
post or ADD request body was produced; startup/refusal evidence is not native
ADD qualification.

Evidence:

- Central result: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/ap2-m2-parent-final-body-approved-one-case-0629-ap2-m2-parent-pin-final-acb-explicit-0617-actual-1021062952-11497/`
- Failure packet: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-central-keeper-command-preflight-0508/evidence-final95-parent-a304-central/run/error-context.md`
- Sanitized request/response evidence: same `run/bounded-browser-evidence.json`
- Trace: same `run/playwright-trace.zip`

The live caller chain remains unchanged:
`onTimelineDrop -> useExternalDrop.ts -> external-drop-utils.ts ->
useAssetManagement.placePreparedAsset -> createTimelineCommands.addClip ->
existing commit-session/outbox path`.

No App worktree files were changed. No local browser, second run, alternate
target, guard bypass, source/assertion/header/selector/timeout/pin/options
change, install, or full suite was performed.
