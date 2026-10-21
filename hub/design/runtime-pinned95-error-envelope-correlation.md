# Runtime95 pinned error-envelope and request correlation

Source authority: Runtime commit `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`,
tree `d3a290b407fa61e6ab2d476f50c068073f70df00`.

## Answer for the App2 parent404 observation

The strict body mismatch is expected: Runtime error bodies include a required
`request_id`. For the actual wrong verified-media selection used by the App2
manual-drop case, the complete direct-Runtime 404 body is:

```json
{
  "code": "not_found",
  "message": "selected media is not a managed project generation/variant/object",
  "request_id": "<same Runtime request ID>"
}
```

There is no `details` member for this case. The producer is
`runtime_protocol/timeline_commit_port.py:734-755`: a missing managed
generation/variant/object row raises `NotFoundError` with only that message.
`NotFoundError` is `code = "not_found"`, `status = 404`
(`runtime_protocol/errors.py:45-47`), and `RuntimeErrorBase.as_dict()` only
adds `details` when supplied (`runtime_protocol/errors.py:1-14`).

For the literal direct Runtime route that reads a missing parent composition
revision,
`GET /v1/projects/{project_id}/timelines/{timeline_id}/composition-revisions/{revision}`,
the complete body instead includes the route's supplied details:

```json
{
  "code": "not_found",
  "message": "parent composition revision not found",
  "details": {
    "timeline_id": "<timeline_id>",
    "revision": "<revision>"
  },
  "request_id": "<same Runtime request ID>"
}
```

The route dispatch is `runtime_protocol/server.py:600-602`; the producer is
`runtime_protocol/service.py:2332-2337`. Do not use this second message/details
shape for the App2 wrong-selection fixture; it is a different Runtime route.

## ID production and direct Runtime correlation

`runtime_protocol/server.py:95-102` is the only Runtime HTTP request-ID
producer. It caches one value on the handler. An inbound `X-Request-ID` is
accepted only when it matches
`^[A-Za-z0-9][A-Za-z0-9._~-]{0,127}$`; otherwise Runtime generates
`uuid.uuid4().hex`. The type is therefore a string satisfying the shared
`Id` pattern, not an integer and not an App command/request identity.

For a Runtime error, `server.py:394-400` obtains the cached value, adds it as
the body's `request_id`, and sends the error. `_send` emits the same cached
value as the `X-Request-ID` response header (`server.py:321-340`). Thus a
direct Runtime response has exact body/header equality:

```text
body.request_id == response.headers["X-Request-ID"]
```

This is correlation only. It is not the App edit `request_id` or the
`Idempotency-Key`, and it does not authorize a retry, undo, or any other
follow-up.

The pinned contract independently requires the same body field:
`contract/schemas/common.json:30-38` defines a closed `Error` object with
required `code`, `message`, and `request_id`; `request_id` uses the shared
`Id` format. No new DTO or schema field is needed.

## Door and App proxy seam

The hosted browser door runs the same Runtime handler/dispatch, but it has a
different header policy. `runtime_protocol/door.py:59-66` explicitly excludes
`X-Request-ID` from request and response header allowlists;
`door.py:654-666` drops it and exposes only the listed browser-safe response
headers. The door therefore preserves the Runtime error body (including
`request_id`) but does **not** expose a normal response-header copy of that ID.
The door's own admission refusals (`door.py:611-623`) are separate
`{"error": "..."}` responses and are not the Runtime parent404 envelope.

The normal App `/api/runtime` proxy is different from the door. The Vite
ordinary proxy rewrites the prefix and injects the bearer but does not remove
`X-Request-ID` (`config/vite/runtimeProxy.ts:25-43`). The discovery proxy
copies upstream response headers and streams the upstream body
(`scripts/runtime-discovery-proxy.mjs:429-449`). Therefore an actual Runtime
404 through that ordinary proxy retains the Runtime body and header. If the
proxy cannot resolve/reach Runtime, its own failure body is
`{code: "runtime_unavailable", message: ...}` without `request_id`
(`scripts/runtime-discovery-proxy.mjs:17-22`); that is proxy decoration, not
the pinned Runtime parent404.

## Generated-client exposure

The pinned Python generated client stores `ApiError.request_id` and decodes
`value.request_id`, falling back to the client-generated outbound
`X-Request-ID` only when the body has no ID
(`generators/python_client_template.py:119-123,572-577,621-660`). The normal
Python path therefore exposes the Runtime body ID on `ApiError.request_id`.

The pinned TypeScript generated client also exposes `ApiError.request_id`, but
its decoder reads the body only (`packages/typescript/src/generated.ts:72-91`);
it does not use a response-header fallback. The App's normal generated-client
seam is therefore the body `request_id`. A caller that needs to assert direct
header/body correlation may inspect the raw response headers, but it must not
invent a header ID when using the door, where that header is deliberately
absent.

## Existing evidence consulted

- `tests/test_generated_client.py:467-499` checks body `request_id` preservation
  and Python transport correlation/fallback behavior.
- `tests/test_door_transport.py:117-135` checks that the door hides
  `x-request-id` while exposing only the allowlisted headers.
- Existing App2 source report
  `design/ap2-m2-parent404-current-envelope-exact-source-0556-REPORT.md`
  records the same three-field wrong-selection body and the strict pattern
  check; its later ADD/retry/undo assertions remain outside this source answer.

No Runtime/App source, contract, pin, fixture, caller, or test was changed.
