# P2/A3 D78 retained element request handoff

- Parent label: App-owned.
- Status: retained-and-authorized.
- Same-ID run: `app-pin-587316e3-d73-p2-current-1747-1024175319-22847`.
- Authorization: exact retained element `doc.patch` request under the owner/ORCH D78 authorization relayed at INBOX18:16. This packet uses no new browser, endpoint, extractor, replay, or body.
- Runtime ownership: replay, stackdump, and source-cause diagnosis.

## Request

The JSON packet contains the exact retained `POST` URL, header names/values, idempotency key, and raw UTF-8 request body. The body is 4,459 bytes, parses as JSON, and its raw bytes were preserved exactly. Its SHA-256 is `e58a09dcafa9fc499448d216d48a1e17f6ee326123e0a3281c169b20ab92b992`.

The request is the C0 v2 shape: `api_version`, project/timeline scope and base pair, one `doc.patch` command with op/version/select/args, label, one full step, merge, reads, dry-run, source, project_id, and timeline_id.

The retained request timestamp is `2026-10-24T17:55:58.603Z`; the HAR has no retained response status or response timestamp. The packet keeps the exact idempotency key because D78 authorizes this retained request key; it is not an authentication credential.

## Redaction

Credential, token, cookie, and secret header values are redacted explicitly as `[REDACTED]` with SHA-256 of the original value while preserving header names. The retained request has no auth/cookie header and no cookies; the body has no sensitive field names. No raw credential is included in this report or in the handoff markdown.

## Provenance

- HAR source: `trace.zip!0-trace.network`, anchor `record[111].snapshot`, request node `snapshot.request`.
- Body source: `trace.zip!resources/5e0a670f95cdaf127a07a4111aac1c6389a35f67.json`, referenced by `snapshot.request.postData._sha1`.
- Trace ZIP SHA-256: `2bb5f1c8db39d67fc6e359bbb91942ff3caff90e3385855b8cfe9709584b25c7`.
- Extracted network SHA-256: `bc5c36c5fbdd183d0a423a209df4826462aa1821ba4c57edfb8a5349700b06bb`.
- Retained body SHA-256: `e58a09dcafa9fc499448d216d48a1e17f6ee326123e0a3281c169b20ab92b992`.
- Retained diagnostic SHA-256: `d751a7d9236eaaeb2b42fac723391f1f4fe4da378feb6e16704bdd4eff0ae824`; its request-start anchor is `diagnostic.events[1]`, correlation `apply-1`, terminal `pending` at page-close.

## Explicit gaps

No response/receipt, accepted/merged/conflict/invalid result, or Runtime safe-phase output was retained. The source element case failed after the request remained pending; this packet does not claim execution or acceptance.

