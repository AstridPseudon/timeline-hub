# D127 submission checkpoint

Status: **SUBMITTED_WAITING_TERMINAL**.

The frozen D66 `p2 --submit` route completed its single source preflight
(`pass`) and queued exactly one original full-P2 body. The same normal ID is
being awaited; no second request was made.

- Target: `app-pin-fe3309db`
- Preflight ID: `app-pin-fe3309db-d73-p2-fe3309db-submit-preflight-1025140913-15235`
- Normal ID: `app-pin-fe3309db-d73-p2-fe3309db-submit-1025140943-3250`
- Durable plan SHA-256: `36fc0caa325e5a262a587c6342e329bca0929d49fe21e0a9f0c3bde3b9ad9a81`
- Exact original admission: `5311045632` bytes
- Recheck: `5133033472` bytes; D89c same-body admission applies, and the
  `4000000000`-byte stop line was not approached.

The four pinned source identities, checkout receipt hashes, source hashes,
Node 20.19.4 binary hash, and actual launch-root `tsx` resolution are in the
JSON packet. Raw payloads, authentication material, private URLs, stacks, and
opaque service details are not published.
