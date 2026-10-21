# Parent 0547 result: first-cause diagnosis

## Result

The required same-original-result execution was consumed once. It is a real
FAIL, not a launch or setup failure. No App source, assertion, caller, helper,
selector, timeout, pin, option, or shared file was changed. No retry and no
legacy-writer cut were made.

The first boundary is the exact 404 response body for the deliberately wrong
verified media selection:

```text
GET /api/runtime/v1/projects/edb1507099a64ed7af9cd84eff22306b/media-selection/verified
  object_id=sha256:1d9fd75956a1fc3a7e57b0e26f0d2ea521b0f4e66286068025a077e9290b2350
HTTP 404
```

The observed body was:

```json
{"code":"not_found","message":"selected media is not a managed project generation/variant/object","request_id":"85fa632fa90f48f790f0cf4f55cebb20"}
```

The keeper assertion expects the same `code` and `message` but omits
`request_id`, and fails at
`tests/e2e/local/three-products.spec.ts:1505`. The 404 status and semantic
message are correct. The run did not reach ADD, raw/order, reload, lost-ACK,
restart, exact retry, undo, opaque/order, or zero-legacy assertions; all remain
unverified rather than failed.

## Exact result and source tuple

- Test ID: `ap2-m2-parent-promoted-current-one-case-0547-ap2-m2-parent-current-driver-durable-promotion-0535-actual-1021054752-6715`
- Result: FAIL, exit 1, 78 seconds; 1 collected, 1 executed, 1 failed, 0 passed
- App keeper commit: `a304dce02a185a4774ff5144d5aa451c9702aa46f`
- App keeper tree: `a3c82aa91f1336b86491191acf857d88c56179b2`
- Agent: `6efc81500a0e0688c2bb41e736503f0fc3e04abb`, tree `2ed2b8a12b5b3391ca221ba6ff05390f71a73556`
- Runtime/producer: `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`, tree `d3a290b407fa61e6ab2d476f50c068073f70df00`
- Shared schema digest: `sha256:7d4afa05962b8cd61643213fc79cdde41e16046c4e2a777bd299b48af0f31816`
- App source file hash in the keeper source worktree: `tests/e2e/local/three-products.spec.ts` = `sha256:f5a8ff14965504257a86832cff130777cb983b6d07fda46300d25c3aa28d3eff`
- Promoted driver hash: `sha256:34ee03d1ea6f25ae4f68b8965f5c9b050d8892214416ec3bf551dfa81b17a2d2`
- Gate hash: `sha256:2aebe7cce4aab7cbf2fb4292165687385edddb0351bab12c633537bfc09c7546`

## First-cause classification

This is a cross-repo contract mismatch exposed by the App assertion, not a
test-environment setup cause and not evidence of an App product-path defect.
Runtime 95bd’s `contract/schemas/common.json` declares `request_id` required
for every Error response. Its `runtime_protocol/server.py` `_error()` adds
the request ID to every `RuntimeErrorBase` error, and the captured service
returned that conforming envelope. The failure is therefore caused by the App
keeper’s exact two-field expectation being narrower than the current Runtime
contract.

The brief forbids changing assertions or changing Runtime/shared ownership in
this worker. A peer/orchestrator contract decision is required before any
assertion conversion or Runtime change, followed by a fresh approved actual;
no downstream gate may be inferred from this run.

## Evidence and commands

Central source preflight passed:

```text
test-ap2-m2-parent-current-driver-durable-promotion-0535-preflight-1021054051-11866
PASS, exit 0, 9 seconds
```

The approved actual was run exactly once with the pinned gate and driver:

```sh
test "$(sha256sum -- /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-current-driver-durable-promotion-0535/final-keeper-gate.sh | cut -d' ' -f1)" = '2aebe7cce4aab7cbf2fb4292165687385edddb0351bab12c633537bfc09c7546' && test "$(sha256sum -- /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-current-driver-durable-promotion-0535/run-parent-manual-drop-evidence.sh | cut -d' ' -f1)" = '34ee03d1ea6f25ae4f68b8965f5c9b050d8892214416ec3bf551dfa81b17a2d2' && env NORMAL014_PROFILE=final95 NORMAL014_APP_SOURCE=parent NORMAL014_USE_BASE_PYTHON=1 sh /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-current-driver-durable-promotion-0535/final-keeper-gate.sh run
```

Result: FAIL as recorded above. The retained exact failure packet is in the
central runner tail and error context under
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-central-keeper-command-preflight-0508/evidence-final95-parent-a304-central/run/`;
`result.txt` is `runner_status=1`, and the packet records the 201 import, 200
selection read, 404 wrong verified selection, and the extra `request_id`.
The durable actual report is
`design/ap2-m2-parent-promoted-current-one-case-0547-REPORT.md`.

Read-only local checks performed:

```sh
git status --porcelain=v1 --untracked-files=all
# PASS: empty

git -C /home/user/banodoco/banodoco-workspace-runtime show 95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c:contract/schemas/common.json
# PASS: Error.required includes code, message, request_id

git -C /home/user/banodoco/banodoco-workspace-runtime show 95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c:runtime_protocol/server.py
# PASS: _error() writes payload["request_id"] before sending
```

No local browser, full suite, install, live socket, or broad/targeted test was
run after the failure; there was no source change requiring one.

## Live callers

The live caller chain was unchanged in the actual:

```text
onTimelineDrop -> useExternalDrop.ts -> external-drop-utils.ts
-> useAssetManagement.placePreparedAsset -> createTimelineCommands.addClip
-> existing commit-session/outbox path
```

## Disposition

No dead writer/helper is physically proven removable because the first actual
stopped before the positive ADD and all downstream durability/undo controls.
The broad parent row remains open. Blocked on the App/Runtime owner decision
for the required `request_id` error-envelope field; do not retry or relabel
this result until that decision and a new approved source/result exist.

