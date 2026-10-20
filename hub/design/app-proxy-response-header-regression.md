# App proxy response-header regression

## Source

- Base: `tl/app-m2-proxy-browser-server-coupled-stage` at `79c2ad29a1ce04756a3887201209812c1c99ad96`.
- Final central snapshot: `79b2cd8160075ced69e90a3c5891a4e425fe3d45`.
- Changed source: `scripts/runtime-discovery-proxy-operation.test.mjs` only.
- Product leak finding: none; no product code changed.

## Missing-test closure

Extended the existing permanent actual Vite → operation proxy → synthetic upstream test. The upstream now sends synthetic `Authorization`, `Proxy-Authorization`, `Cookie`, `X-Astrid-Operation-Handle`, and existing `Set-Cookie` response headers. The browser-facing response asserts all credential/handle headers are absent while preserving `Content-Type: text/plain`, the valid body, `Cache-Control: no-store`, the pinned Runtime bearer on the upstream request, and existing request-side stripping/normal-read positives.

All tokens are synthetic test labels; no real credentials are used. Existing repeated/mixed-case `Connection` nomination, `Expect`, private-handle, and request credential-negative coverage was retained.

## Verification

- `git diff --check`: pass.
- `node --check scripts/runtime-discovery-proxy-operation.test.mjs`: pass.
- `node --test --test-concurrency=1 --test-name-pattern='^pure:' scripts/runtime-discovery-proxy-operation.test.mjs`: 1 pass.
- Central `proxy-browser-host-coupled-integration`, request ID `app-m2-proxy-response-header-regression-proxy-browser-host-coupled-integration-1020111126-7621`: pass, 90 Node + 12 chat + 261 Vitest = 363 tests, 0 failures.

A direct worker-shell live-Vite invocation produced Node's generic top-level `test failed` for both the changed live case and the pre-existing live-Vite case; it was not used as evidence. The central isolated snapshot is authoritative for the live chain.

## Limits and next steps

This proves the supported same-origin HTTP/Vite/proxy/fixture transport path and browser-facing raw response headers. It does not claim Chrome qualification, requester activation, native Runtime acceptance, Runtime restart/outbox recovery, or owner activation. No KEEP; no blocker.
