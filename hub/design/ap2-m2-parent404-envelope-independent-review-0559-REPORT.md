# App2 parent 404 envelope independent review

## Verdict

**HOLD — smallest concrete defect:** the strict conversion in frozen App
`86f765532d25181a1f3e953fb08f79587d328f85` / tree
`5f1d1d06432350eacbdd3d37ae8956b9fe2f756b` cannot pass on the existing mounted
App browser door. The assertion reads
`wrongVerified.headers()['x-request-id']`, but the pinned door strips
`X-Request-ID` before sending the response to the browser. Therefore the new
format assertion receives `undefined`; body/header correlation is not a valid
contract on this path.

This is not a reason to weaken the matcher or change the body expectation in
this review. The one-to-one conversion needs either the existing door/header
contract reconciled by its owner or a fixture/assertion shape that matches the
Main-visible response. No App product edit was made here.

## Candidate and delta integrity

- Candidate commit: `86f765532d25181a1f3e953fb08f79587d328f85`
- Candidate tree: `5f1d1d06432350eacbdd3d37ae8956b9fe2f756b`
- Prior source: `a304dce02a185a4774ff514d5aa451c9702aa46f`
- Only changed path: `tests/e2e/local/three-products.spec.ts`
- Prior file blob: `107589c135ac4a3067fc565842e60b043b5ca8e7`
- Candidate file blob: `b47bb4ad8e615679b2311a52222b152cf3946cd0`
- `git diff --check a304dce02 86f765532`: PASS

The exact diff is the reported three-line assertion addition: capture the
response header, validate the shared ID pattern, and add that captured value
to the exact `toEqual` body. The original 404 status/code/message/refusal and
the later positive ADD/raw/order/ACK/restart/exact-retry/undo/zeroLegacy
assertions remain unchanged in the candidate diff. No caller, helper,
selector, timeout, pin, source, field stripping, `objectContaining`, or
expected failure was added.

## Runtime producer and schema

Pinned Runtime source is commit
`95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`, tree
`d3a290b407fa61e6ab2d476f50c068073f70df00`.

- `runtime_protocol/server.py` blob
  `3aa8797055db6d7778d29dc2f220d6e01afc872a`: `_request_id()` accepts a
  valid incoming ID or creates one; `_send()` emits it as `X-Request-ID`; and
  `_error()` adds the same value to the error body.
- `contract/schemas/common.json` blob
  `6a6a4f11f4af435ba464b002d1c263509fa97bc1`: `Error` requires exactly
  `code`, `message`, and `request_id` at the top level (with `details` the
  only optional property), and `request_id` uses the shared ID pattern.

The producer-side evidence supports the proposed three-field envelope. It is
not sufficient for this assertion because the browser door is an additional
response boundary.

## Door/proxy forwarding check

The actual mounted test path is the Runtime browser door, as the App harness
documents (`tests/e2e/local/support/harness.ts`: hosted page -> Runtime door ->
Runtime daemon). The pinned door is `runtime_protocol/door.py`, blob
`8176af12d1d3dd41744b0c348187d8689054c13c`, at the same Runtime commit.

The door source is explicit:

- The comment above `REQUEST_HEADERS`/`RESPONSE_HEADERS` says internal
  `X-Request-ID` headers “never cross the door.”
- `RESPONSE_HEADERS` contains only content/media headers; it does not contain
  `x-request-id`.
- `send_header()` drops every response header not in that allowlist.
- `end_headers()` exposes only that same allowlist through
  `Access-Control-Expose-Headers`.

The retained actual 6715 trace independently confirms the source behavior.
In `0-trace.network`, the 404 response for the wrong
`/api/runtime/.../media-selection/verified` request has status 404 and body
`{"code":"not_found", ... ,"request_id":"85fa632fa90f48f790f0cf4f55cebb20"}`,
but its raw browser-facing response headers contain cache/content/CORS/date
headers and **no `X-Request-ID`**. The retained bounded evidence records the
same body, and the runner failure is the original two-field assertion mismatch.

The App Vite proxy source is permissive for ordinary upstream response
headers, but that does not override the pinned door's allowlist on the actual
mounted route. Consequently, approval based only on `server.py` would miss
the demonstrated door stripping.

## Offline controls

- `node -e "... esbuild.transformSync(...three-products.spec.ts...)"` — PASS
  (TypeScript syntax).
- `node_modules/.bin/eslint tests/e2e/local/three-products.spec.ts --max-warnings 0` — PASS.
- `node_modules/.bin/playwright test --config playwright.three-products.config.ts tests/e2e/local/three-products.spec.ts --grep 'M2 real mounted manual video drop' --list` — PASS; exactly 1 test collected.
- Compact exact matcher probe — PASS: one valid envelope accepted; missing
  ID, wrong ID, wrong code, wrong message, and extra field all refused.
- `git diff --check a304dce02 86f765532` — PASS.

No browser replay, actual rerun, broad suite, build, install, or product edit
was performed. Live callers remain unchanged. The downstream ADD/raw/order/
ACK/restart/exact-retry/undo/zeroLegacy behavior remains unverified by the
original 6715 run because it stopped at the old envelope assertion.

## Recommended next step

The Runtime-door owner should make an explicit contract decision about whether
`X-Request-ID` is intended to cross the browser door. If it remains stripped,
the candidate conversion is not landable as written and the strict test must
assert only the Main-visible body shape with a separately justified exact
correlation rule. If forwarding is intended, a door-owned source/test change
must land and be independently qualified before this App assertion can be
approved.
