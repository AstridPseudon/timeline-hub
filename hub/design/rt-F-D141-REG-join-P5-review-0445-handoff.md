# D141h finite REG handoff

The exact join is complete and finite:

- `rt-F-D141-REG-upgrade-fix-next` owns the 13 upgrade REG fixes. The smallest disjoint file scope is `runtime_protocol/upgrade.py`; stage the missing `db_path` on the `_validate_candidate` RealmStore inspector before timeline integrity inspection. Preserve all tests, assertions, inputs, skips, and fixtures.
- `rt-F-D141-REG-typescript-fix-next` owns the 2 TypeScript-generator REG fixes. The smallest disjoint generated-output scope is `conformance/typescript/contract-metadata.ts` and `conformance/typescript/generated.ts`, regenerated with the existing generator. Do not alter test assertions or generator inputs.
- Luna is the default owner only after the proved join above; no broader root-cause investigation is authorized by this review.

The 38 `NEW_OURS` failures are not REG-eligible and remain outside these handoffs. No environment-type pristine failure exists.

After a Runtime fix, the new Runtime head must be qualified and reviewed, then normally merged, then actual normal tool-consumer pins may move. No speculative pin movement is authorized. The original P5 receipt remains the authentic `P5-service6934` cut proof used by production; source applicability after subsequent source changes is a separate owed check.

The C0v2 contract review recorded in this join requires request base pair (`base_revision_id`, `base_publication_id`), semantic/doc.patch commands, label, per-step patch, `merge=fields|atomic`, declared reads, `Idempotency-Key`, and `dry_run`. Replies must distinguish accepted, merged, conflict, invalid, and preview. Canonical closure must authenticate receipt bindings, effects, dependencies, history, and guarded undo; conflict includes reason/head; invalid includes code/path/hint/suggested command; preview must not mutate store/history/idempotency/head.
