# App2 parent 404 exact-envelope assertion conversion

## Result

Completed the one-to-one test-only correction in
`tests/e2e/local/three-products.spec.ts` at the manual-drop refusal case.
The prior strict two-field expectation (`code`, `message`) is now a strict
current Runtime95 three-field expectation (`code`, `message`, `request_id`).
The existing HTTP 404 assertion, exact `not_found` code, full original
message, no-mutation checks, and all later positive ADD/raw/order/ACK/restart/
retry/undo/zeroLegacy assertions are unchanged. No App product source,
Runtime source, pin, selector, timeout, helper, driver, or suite registration
was changed.

## Source authority

The pinned Runtime producer is commit
`95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`, tree
`d3a290b407fa61e6ab2d476f50c068073f70df00`.

- `runtime_protocol/server.py:95-102` accepts/preserves a valid `X-Request-ID`
  or creates the Runtime request ID using the pinned ID format.
- `runtime_protocol/server.py:321-340` emits that same value as the
  `X-Request-ID` response header.
- `runtime_protocol/server.py:394-400` puts that same value in the error
  body's `request_id` field.
- `contract/schemas/common.json:30-38` defines the closed `Error` object,
  requires `code`, `message`, and `request_id`, disallows extra top-level
  fields, and uses the shared `Id` format.

The test now captures `wrongVerified.headers()['x-request-id']`, checks the
source-pinned ID pattern, and uses it in `toEqual`. This preserves header/body
correlation while rejecting a missing or wrong ID and any unexpected body
field.

Before:

```ts
await expect(wrongVerified.json()).resolves.toEqual({
  code: 'not_found',
  message: 'selected media is not a managed project generation/variant/object',
});
```

After:

```ts
const wrongVerifiedRequestId = wrongVerified.headers()['x-request-id'];
expect(wrongVerifiedRequestId).toMatch(/^[A-Za-z0-9][A-Za-z0-9._~-]{0,127}$/);
await expect(wrongVerified.json()).resolves.toEqual({
  code: 'not_found',
  message: 'selected media is not a managed project generation/variant/object',
  request_id: wrongVerifiedRequestId,
});
```

This is the approved one-to-one assertion conversion under the Main-visible-
behavior decision recorded in the prior first-cause report. The existing 404
refusal remains strict. All positive ADD controls remain unchanged. The
independent assertion-conversion review precedes any next actual.

## Checks

All checks were offline and targeted; no browser, actual, build, full suite,
install, live socket, Runtime/App source, or pin change was run.

- `node -e "const fs=require('node:fs'); const esbuild=require('esbuild'); esbuild.transformSync(fs.readFileSync('tests/e2e/local/three-products.spec.ts','utf8'), {loader:'ts', format:'esm'});"` — PASS (syntax).
- `node_modules/.bin/eslint tests/e2e/local/three-products.spec.ts --max-warnings 0` — PASS.
- `node_modules/.bin/playwright test --config playwright.three-products.config.ts tests/e2e/local/three-products.spec.ts --grep 'M2 real mounted manual video drop' --list` — PASS; exactly 1 original case listed at line 1440.
- Compact exact-matcher proof — PASS: the observed real three-field envelope passed; missing `request_id`, wrong code, wrong message, and an extra field each refused (1 pass, 4 refusals).
- `git diff --check` — PASS.

## Integrity and callers

Only `tests/e2e/local/three-products.spec.ts` is modified. Before/after/diff
hashes:

- Before file SHA-256: `f5a8ff14965504257a86832cff130777cb983b6d07fda46300d25c3aa28d3eff`
- After file SHA-256: `b1f28a7fe1e87635ed1d52602f43e663d3f4af19638aa061af4521fd85b0422a`
- Binary diff SHA-256 against `tl/ap2-m2-parent-complete-current-proof-source-0455`:
  `4c98d728c019beb2c47740148124aac7fa128372ac76ea948852a05e4a33f88b`

The live caller chain remains unchanged:
`onTimelineDrop -> useExternalDrop.ts -> external-drop-utils.ts ->
useAssetManagement.placePreparedAsset -> createTimelineCommands.addClip ->
existing commit-session/outbox path`.

The normal ignored dependency link remains unchanged:
`node_modules -> /home/user/work/app/node_modules`.

Commit message written to the required path:
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent404-current-envelope-exact-source-0556/commit-msg`.

`KEEP` and `DONE` markers are present in the required worker directory.
