# AP2 M2 selected service-tree registration — 0920

## Result

Corrected the registration-only mistake from 18044 and submitted exactly one
central actual run. The App worktree and the approved runner/source/spec/helper
bytes were not edited.

The only registration correction was removing the service/PWD `HEAD` equality
and retaining full service `HEAD^{tree}` equality. The protected real keeper
checks remain separate and exact.

## Registration evidence

- Service snapshot: full tree `92391f9a57dd38ce327b0a63990725053ea34601`.
- Protected keeper `/home/user/work/wt/app-pin-a50ca4a0`: exact HEAD
  `a50ca4a0172cce9c73ce3c040290bf9479098b0f`, tree
  `92391f9a57dd38ce327b0a63990725053ea34601`, clean, zero-byte `KEEP`.
- Normal keeper dependency link resolves to `/home/user/work/app/node_modules`.
- Approved runner bytes: SHA-256
  `4459f2c9acd7ce411f92beab33c216e549c98fe1fad996706998e6c5aaab85a3`.
- Stored registration body was read and validated programmatically: no
  unqualified service/PWD `rev-parse HEAD` comparison; the exact keeper `-C`
  `rev-parse HEAD` guard remains; SHA-256 fields are full lowercase 64-hex
  values and Git object IDs are full 40-hex values.
- Parent 25174 was terminal before submission and the local browser lock was
  free. Disk availability was 13G.

## Central actual

Command:

```sh
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test ap2-m2-selected-service-tree-registration-once-0920 ap2-m2-selected-retention-custody-one-original-0911-actual --no-cache
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test ap2-m2-selected-service-tree-registration-once-0920-ap2-m2-selected-retention-custody-one-original-0911-actual-1021091823-13522
```

Run ID:
`ap2-m2-selected-service-tree-registration-once-0920-ap2-m2-selected-retention-custody-one-original-0911-actual-1021091823-13522`

Result: FAIL, exit 1, 77 seconds. Registration and all runner guards through
artifact, graph, and exact list-1 passed. Hosted build passed. Playwright
collected and executed exactly one test in one file/worker.

First retained causal failure:

```text
tests/e2e/local/three-products.selected-param-dev.spec.ts:39:1
local DEV selected PARAM uses admitted P1 through P2 removal, refusal, retry, reload and undo
selected PARAM timeline: 409 {"code":"conflict","details":{"reason":"timeline_commit_required","status":"refused"},"message":"tracked timeline publication requires a timeline command","request_id":"c66e522a6d0c4bc5a2aaa085b63a14cb"}
```

This occurred in existing seed setup at `support/harness.ts:698`, before the
selected test's P1/P2 behavior assertions. The durable retention directory has
the child log (`aae8ddd5aff54f34b6664e3814f9db29bbea3226719f6421de9545f003ab52dc`)
but no identity/SHA manifest or DOM: the existing approved retention guard
refused because Playwright produced error-context and trace but no DOM, then
cleaned the temporary run root. The central log preserved the exact refusal;
the complete durable trace/DOM/log/identity/SHA packet was therefore not
available.

Unreached: P1/P2 continuation, removal, refusal behavior assertions, dirty
draft preservation, lost-ack retry, restart/reload, inverse/undo, and
`zeroLegacy` assertions. No writer cut was made. No second actual was run.

## Verification

- `sh -n <approved runner>` — PASS.
- Programmatic stored-body validation and `bash -n` — PASS.
- Local service tree/keeper HEAD+tree/clean/KEEP/link/lock checks — PASS.
- Central `request-test ... --no-cache` + `wait-test ...` — FAIL at the
  existing selected seed refusal and approved missing-DOM retention guard.
- No local browser, socket, install, full suite, broad preflight, or retry was
  run.

Recommended next step: diagnose the existing `timeline_commit_required`
response in selected seed setup under a separately authorized run; do not
reinterpret this run as evidence that the later selected behavior path passed.
