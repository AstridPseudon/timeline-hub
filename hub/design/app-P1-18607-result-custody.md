# App P1 result custody: run 18607

Result-custody repair completed for `app-P1-local-OPS-1830-ap2-P1-chain-h6-1023185313-18607`.

- Raw log restored from the retained worker deletion hunk at lines 3267–3328: exactly 26440 bytes, 62 lines, SHA-256 `a83cc89c1909877b7f01dfe4c83e994a31b8450afae80767a01e87781bf3728b`.
- The overwritten JSON replacement is preserved privately as a non-raw record: 18,661 bytes, SHA-256 `28f8c39b6587228a5cba3056e56a5a83ace6a7382a7269821da13c209ee372ec`.
- Run result remains `fail`, exit `1`, elapsed `744s`; no body, preflight, benchmark, network, browser, or test rerun was performed.
- Snapshot mode: `actual direct service snapshot; not synthetic/control`. App/Agent/Runtime/Composition heads and trees, source blobs, installed receipts/origins, and preflight evidence are retained in the safe JSON.
- Timing boundary: requested `2026-10-23T18:53:13Z`, observed end `2026-10-23T19:05:41.146658791Z`. Preflight says `D21 passed; actual body executed`.
- First case: PASS, line 9, 27.4s automatic exact retry. Second case: FAIL at the expected-post count boundary; Agent move, HTTP 409 refusal, and App rollback/message assertions were unreached.
- Priority/correlated safe records retain exact source ranges and line hashes for lines 10 and 11. The detailed line 12 record is capped at 16 KiB and unparseable; its state before the cap cannot be recovered and is not inferred.
- Allowlisted SourceIn, basis, displayed head, capture/adoption, outbox, UI, owner and error correlations remain available only in bounded/redacted form in the safe JSON. Full request bodies, success receipts, credentials, tokens, and raw packets were not copied.
- Cause remains UNKNOWN; no product, collector, or specification cause was assigned. Existing D25 triage ownership remains unchanged.

Safe artifact SHA-256: `97b088b687ec4779eb85dfc94c9ebb43d03bae30ae5ba96d608544d540e0c1e8`. The byte-identical copy is at the design packet path.
