# Runtime R2r created-child Sol review — FAIL

Reviewed final Sol1210 tree `9345cb58fe8c54f114d666929e167bbeb5899c6c`
(`1675bb7084786f55a4343b366782bc209ad9a1c4`) against cumulative base
`3b926efab2eed122d374540baee297d4cdcec62a`.

The prior two Luna failures are repaired. The exact 1204 equal-byte
future/foreign physical-ID promotion is accepted by old `7fbb89da` and
refused here by sequential allocation/provenance; the fresh real public
RuntimeService → managed media → Agent native birth/child-track/held-image →
complete-v2 commit/readback path passes with a new receipt. The mandated suite
passes 257/257, including all 52 collected integration nodes; Ruff, Pyright,
AST/original-test preservation, and frozen-client/schema checks pass.

Qualification remains **FAIL** because a fresh public probe appended this
schema-valid but forged dependency to an earlier command:

```json
{"key":"source.forged","kind":"source","policy":"exact","pin":{"document_id":"foreign-document","version":1,"content_digest":"sha256:1111111111111111111111111111111111111111111111111111111111111111"}}
```

The pin was not captured through the Runtime source-input APIs and was absent
from the candidate document manifest. Runtime nevertheless accepted the public
commit as receipt `txn-546924ab306d4c0eb8098789262d3fac` and persisted the
forged dependency in its history record. The durable probe is
`workers/rt-R2r-created-child-sol-review-1233/evidence/forged-source-dependency.md`.

Cause is the mismatch between `timeline_commit_auth.py:1361-1371` (only
`media`/`document` advance the per-command manifest) and
`timeline_commit_port.py:512-520` (candidate document pins must have a
recorded source/transcript dependency, but extra unconsumed source/transcript
dependencies are not rejected). Repair this boundary with exact captured
source/transcript pin authentication and unchanged-state refusal controls.

No code or tests were changed by this review. No full/browser suite was run.
