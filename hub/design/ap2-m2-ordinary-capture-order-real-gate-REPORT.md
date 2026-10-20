# Ordinary real capture-order gate

## Result

The one central run was submitted against the exact requested target tree and
failed in the later ordinary journey. This worker made no App source changes.

- Target: `tl/ap2-m2-ordinary-real-capture-contract-repair`
- App tree: `e1c9733e10aed927472aad455add65dd60b7621f`
- Required ancestors: `7d42fcd3a`, `8c0e1f799` (both ancestors)
- Agent: `8130a401bf44a518d5a40ae274d398b8c560be55`, tree `236c3e57e0265c52b81ba8085de3193026176bff`
- Runtime: `2c4ac180c2220bdad966bc01e95ad230e99ce26a`, tree `7ab412cc4bcbe517efcfa806e092336390312e18`
- Composition: `0.0.13`, artifact SHA256 `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`
- Locked graph archive SHA256: `895c628ab0727c8975247310fd0319b0f546a8d032a57072c9e364e20965ca30`
- Worktree: clean before and after the run; no source, lock, dependency, or wire changes.

## Central evidence

Submitted exactly once:

```sh
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test ap2-m2-ordinary-capture-order-real-gate e2e-m2-ordinary-committed-driver-gate) && /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"
```

Result directory:
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/ap2-m2-ordinary-capture-order-real-gate-e2e-m2-ordinary-committed-driver-gate-1020221052-23660/`

Result: exit 1, 1 test failed, 135 seconds.

The absolute approved driver passed Chromium smoke, hosted App build, and
pre-build collection of exactly one ordinary test (`Running 1 test using 1
worker`). The App/Agent/Runtime source tuple and schema digest were the pinned
values above. The ordinary ten-command capture progressed through the initial
batch and the Agent/local/restart path; the failure was at
`three-products.spec.ts:1241`, where the expected accepted local-label retry
returned HTTP 409:

```json
{"code":"conflict","details":{"base":{"publication_id":"txn-9535c6959bac4249aaf4650d2566b87e","revision_id":"authoring-parent-revision-874d84daad595b04fbc9859272c1a60040fc4351527084fc82ca8865eed2f7a4"},"conflicts":[{"base":{"state":"present","value":"V1"},"choices":[],"kind":"dependency_changed","ours":{"state":"absent"},"path":["label"],"ref":"parent/track:V1","theirs":{"state":"present","value":"F2 Agent ordinary sibling"}}],"current":{"publication_id":"txn-c472596830e34b95baf2e56c48d017b7","revision_id":"authoring-parent-revision-7f8e5a502bed10cbe02ab1160ec38f014c828f9cef5485c559070ce2e83c7e7a"},"reason":"dependency_changed","status":"conflict"},"message":"original authored guard changed","request_id":"bdebdd896d344241a10193a04e8b280c"}
```

This is evidence that the capture-order repair no longer stops the ordinary
batch at the earlier `capture_mismatch`; it does not qualify the full journey.
Atomic retry/restart/undo and zero-legacy remain unqualified because the test
stopped at this conflict.

The central log retains the actual response body and trace/error-context paths:

- [`summary`](<../tests/ap2-m2-ordinary-capture-order-real-gate-e2e-m2-ordinary-committed-driver-gate-1020221052-23660/summary>)
- [`log.txt`](<../tests/ap2-m2-ordinary-capture-order-real-gate-e2e-m2-ordinary-committed-driver-gate-1020221052-23660/log.txt>)

The disposable central snapshot was cleaned by the approved driver, so the
referenced Playwright `trace.zip` and `error-context.md` files are not
available after cleanup. The exact wire error above was retained in the
central log before cleanup; no rerun was made.

## Local checks

- `git status --porcelain=v1 --untracked-files=all`: PASS (clean)
- exact target ref, owner ancestry, pin/tree, lock, graph, and Composition checks: PASS
- `git diff --check`: PASS
- No full suite, local driver, browser, socket, dependency install, or source edit was run.

## Decision / next step

No decision was made to change the settled capture repair. The next owner/manager
action is to diagnose the 409 `dependency_changed` expectation or contract at
the local-label rebase point, then run a new explicitly authorized gate after
that decision. Do not claim the ordinary gate passed from this result.
