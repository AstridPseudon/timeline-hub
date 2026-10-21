# App parent 404 body-only exact-envelope correction

## Result

Changed only `tests/e2e/local/three-products.spec.ts` at the manual-drop
refusal expectation (lines 1505-1509). The final matcher keeps the exact 404,
`not_found` code, and full message, and matches the body `request_id` against
the pinned Runtime `Id` pattern inside a full `toEqual` object matcher. It does
not read or assert `X-Request-ID`, strip any body property, or use
`objectContaining`; missing/invalid IDs and unexpected body fields fail.

The original `a304dce02a185a4774ff514d5aa451c9702aa46f` expectation was an exact
two-field body (`code`, `message`). The final current conversion is one-to-one:
it adds exactly one `request_id` matcher field, producing the current exact
three-field matcher. The intermediate `86f765532d25181a1f3e953fb08f79587d328f85`
header-derived conversion was held by the 0559 review because the browser door
strips `X-Request-ID`; it is superseded and is not labelled approved here.

## Authority and retained evidence

Pinned Runtime 95 is commit `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`, tree
`d3a290b407fa61e6ab2d476f50c068073f70df00`:

- `runtime_protocol/server.py:90-102` defines the shared ID validation and
  request-ID creation; `:321-340` emits the internal response header; and
  `:394-400` adds the same ID to the error body.
- `contract/schemas/common.json:9` pins `Id` to
  `^[A-Za-z0-9][A-Za-z0-9._~-]{0,127}$`; `:30-38` makes `Error` require
  `code`, `message`, and `request_id` while disallowing extra top-level fields.
- `runtime_protocol/door.py:59-66` documents and implements the browser-door
  boundary: internal `X-Request-ID` is not forwarded and the response-header
  allowlist excludes it.

The retained actual `6715` body is recorded in
`design/ap2-m2-parent-promoted-current-one-case-0547-REPORT.md`: it contains
the 404, exact code/message, and `request_id`.
The 0559 report records the corresponding browser-facing response with no
`X-Request-ID` header. The offline proof used that retained body and the
headerless browser boundary: the valid body passed without a header; missing
ID, invalid ID, wrong code, wrong message, and an extra field were all refused.

## Hashes and source custody

- Current source base: commit `86f765532d25181a1f3e953fb08f79587d328f85`,
  tree `5f1d1d06432350eacbdd3d37ae8956b9fe2f756b`.
- Final file SHA-256:
  `5c12370fe8a14439f6c82ddbf088bcfcc2fcdcbfb8af90cbba4ec30e72bb1603`.
- Final file Git blob: `67934dbcd263d6dc52648e176c8401f94338bfc7`.
- Pre-edit file SHA-256 (header-derived base):
  `b1f28a7fe1e87635ed1d52602f43e663d3f4af19638aa061af4521fd85b0422a`.
- Working binary diff SHA-256 against current base:
  `dccd39844901fc0ba980c4131f58cd32ed804a5d508e5fd0b116538bb7d3a373`.
- Final binary diff SHA-256 against `a304dce02`:
  `e90f1888922315c4c9a26441937b3fd1ebaf7c756465810b116d0fabc750ac77`.
- Only changed source path: `tests/e2e/local/three-products.spec.ts`.
- Normal ignored dependency link verified unchanged:
  `node_modules -> /home/user/work/app/node_modules` (realpath matches).

## Checks

- `node -e "...esbuild.transformSync(...three-products.spec.ts...)"` — PASS
  (syntax).
- `node_modules/.bin/eslint tests/e2e/local/three-products.spec.ts --max-warnings 0` — PASS.
- `node_modules/.bin/playwright test --config playwright.three-products.config.ts tests/e2e/local/three-products.spec.ts --grep 'M2 real mounted manual video drop' --list` — PASS; exactly 1 test in 1 file.
- Offline exact-envelope proof — PASS; valid retained body accepted without
  `X-Request-ID`, and five invalid variants refused.
- `git diff --check` — PASS.

No actual/browser replay, build, full suite, install, transport mock, native
proof, source/helper binding edit, or product behavior edit was performed.

## Unchanged callers and assertions

The live caller chain remains unchanged:
`onTimelineDrop -> useExternalDrop.ts -> external-drop-utils.ts ->
useAssetManagement.placePreparedAsset -> createTimelineCommands.addClip ->
existing commit-session/outbox path`.

The original no-mutation and positive ADD/raw/order/reload/ACK/restart/
exact-retry/undo/zeroLegacy assertions remain byte-identical. The requested
`HOME.md` was not present in the orchestration tree; PLAN, manager STATUS,
manager INBOX, and the relevant 0556/0559/0600 and retained-6715 reports were
read.
