# App proxy response-header regression final review

## Verdict

**APPROVE** `tl/app-m2-proxy-response-header-regression` at source commit
`ad05c5bd3554cc7b86c2ba3e7b8c0fb7a38e69ca`, tree
`79b2cd8160075ced69e90a3c5891a4e425fe3d45`.

This closes the prior coupled review's response-header test HOLD. The candidate
is exactly one test-only commit on prior coupled source commit
`79c2ad29a1ce04756a3887201209812c1c99ad96` (prior tree
`7e1ba6f2c485705bec39b51074b9a2f510fc63cf`). The only changed path is
`scripts/runtime-discovery-proxy-operation.test.mjs` (`+5/-2`).

## Closure evidence

The permanent actual-Vite test's synthetic raw upstream now sends
`Authorization`, `Proxy-Authorization`, `Cookie`,
`X-Astrid-Operation-Handle`, and `Set-Cookie`, in addition to the existing
connection-nominated leak headers. The browser-facing `call(appPort, ...)`
response is asserted to have all five credential/private headers absent.
The same actual-hop case retains and asserts:

- `status === 200`, body `kept`, and `Content-Type: text/plain`;
- upstream `Authorization === Bearer pinned-token`;
- browser/request-side credentials and operation handle absent at Runtime;
- existing `X-First`/`X-Second` Connection nomination stripping,
  `ETag`/`X-Reply-Leak`/CORS negatives, and `Cache-Control: no-store`.

This is not mock-only coverage: it creates the production Vite server and
admission/proxy options, traverses Vite into the real operation proxy, and
reads the raw browser-facing Node response headers. The following mixed-case
nomination/`Expect` test remains present.

The product bytes are unchanged from the frozen inputs: browser host/provider
paths match `be27b45066947e920cda8da67991976b432ccb33`; proxy/server paths
match `66fc28fafabcc074c688e7a7b50b296df41fc70f`; shared media CORS paths are
also unchanged. The pre-existing coupled fixture is unchanged.

## Verification

- Central exact-tree suite
  `app-m2-proxy-response-header-regression-proxy-browser-host-coupled-integration-1020111126-7621`:
  **exit 0**, 90 Node + 12 chat + 261 Vitest = **363 passing**, zero
  failures/skips/cancellations. Snapshot records the exact candidate tree
  above.
- `git diff --check 79c2ad29a1ce04756a3887201209812c1c99ad96..ad05c5bd3554cc7b86c2ba3e7b8c0fb7a38e69ca`:
  clean.
- Existing pure proxy test was previously recorded as **1 pass** in the
  response-regression worker report. The central 363-case run was not
  duplicated for this read-only review.

## Limits

No Chrome/browser qualification, actual Runtime command acceptance, Runtime
restart/outbox recovery, native capture, outbox/restart activation, owner
activation, full suite, build, socket rerun, TypeScript check, install, or
shared dependency/cache write is claimed. The synthetic upstream proves the
browser-facing HTTP/Vite/proxy response-header contract only.

No KEEP. Recommended next step is to carry this test-only closure into the
orchestrator's inactive proxy composition; activation and the Runtime/native
gates remain separately held as documented by the prior coupled review.
