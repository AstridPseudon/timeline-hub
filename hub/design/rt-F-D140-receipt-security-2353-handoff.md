# D140 review handoff

`FAIL_SOURCE` / `NOT_READY` for candidate `0634ea013b29ba2ab02f619a99328b1f5ca81c7a`.

Blocking follow-up is limited to the existing receipt admission boundary:

1. Admit the actual Farm distribution/dependency producer format
   `timeline.farm-distribution-inputs/v1` and its `.farm-receipt.json` raw-byte,
   component-identity, source and custody closure. Do not promote the old
   D137 installed-kit summary.
2. Tie the D73 retained receipt to the launcher-created request-scoped
   manifest, request-id and runmanifest/exit evidence under the bound KEEP
   root. A detached byte-identical copy is insufficient.
3. Supply and verify the real Farm-owner authenticated digest handoff. Until
   those inputs exist, return the complete census as `NOT_READY`.

Do not change C0 request/reply shapes, introduce a new trust protocol, accept
unknown `timeline.*` schemas, recursively search tuples, create/reuse
terminal receipts, or run a safety-denied alternative route.
