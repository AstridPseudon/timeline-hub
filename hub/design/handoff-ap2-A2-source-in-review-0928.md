# A2/P1 source-review handoff

Verdict: PASS.

Reviewed final candidate `94b19e363047c1446608ff42ee11b0f34c906c69` (tree `c3752a0ff4978f400feb22e45f65b976188c7807`) against provenance `e90090991aa6d3f18a97b3cf51ae908e81404f0e` and current integration `ff2d3c1d76c454f0402e48a42335d466a853cfe1`. Final commit scope is exactly the four allowed files. The original spec is unchanged, SHA-256 `d72798b2301973bfdabcf3b07c2746896e9ec5cd6188bebeda53733c070647a8`.

The production caller chain remains inspector source input → `useClipEditing` → `rowsToConfig` → `withHeldClipSourceFields` → mounted handoff/outbox. The bounded materialization fix restores explicit held `from`/`to`/`speed` without defaults or mutation and leaves bare `rowsToConfig`, provenance, opaque/null/absent fields, unknown fields, and dependent canonical/base-pair/new-ID/read guards stable. No shim bypass was found.

The old tree `679efb0b0fdb3b542edb210d15991784a51cf3f4` independently reproduced the mounted regression (`persists an inspector trim`: expected two intents, received one). The final candidate passed the corresponding focused lane and the exact private dependency-graph lane (9 files / 174 tests). TypeScript, scoped ESLint, diff checks, and serializer neighbours passed. No full/browser/socket/service suite was run.

The split full-raw-equality versus later `SPLIT_AT` expectation is a separate original-spec test-oracle inconsistency. No spec edit or contract question was made. Current integration contains extra mounted Undo tests not in the candidate; manager must port only the four reviewed files onto fresh current integration and preserve those tests before owner merge/OPS/original-chain.
