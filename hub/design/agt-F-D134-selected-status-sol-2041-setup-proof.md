# Setup conservation

The first-return HTTP fixture is inherited without changes. AST comparison against original base a30e74e901a28b39c28facba3deb00d76f186e23 proves the replacement parent literal equals the retired parent_composition literal:

```json
{"config":{"tracks":[]},"registry":{},"clips":[],"occurrences":[]}
```

config.clips is absent; top-level clips is an empty array. The registered real provider receives a guarded root doc.patch followed by the existing explicit top-level clips restoration. Its accepted canonical payload must equal the exact authored literal. This assertion is inherited, not weakened.

The HTTP behavioral test is byte-for-byte identical to original. Its durable pending pin, no pre-publish head advance, original schema rejection after re-admission/removal, removed source/artifact paths, lost acknowledgement, exact serialized flight body/key, rationale, same-port restart, exact retry observation, retained seed and guarded undo predicates are all preserved. The fixture's selection/admission/capture/session code after the retired bootstrap is unchanged. The bootstrap keeps idempotency key selected-http-baseline and now gets a real commit receipt through the supported provider.

No new controls, fake receipts or injected history were added. Current ab1e HTTP behavior is UNVERIFIED: the no-heavy prerequisite refused before any selected body ran. The prior return's mutable-Runtime probe is not current behavior credit.

