# Handoff: AP2 P1 causal-unit review

Review of exact App commit `af13f581ddb18e183ff386dcc189d96aff9c512c` on parent `0cdc76782833d594776452e07706acb406c51553`.

**PASS:** independent no-weakening and causal-boundary unit review. The change is test-only and limited to `useTimelineSave.test.tsx` (+176/-2). Every prior test body/assertion is byte-identical (`cmp` exit 0, 642-line old-test tails). The three new mounted schedules pass with 13 closest existing guards (16/16), and scoped ESLint passes.

The schedules are genuine mounted `useTimelineSave`/`useClipEditing` → split ACK → poll → local handoff/session/outbox paths. They cover old-owner stale trim with mocked 409, held original verification causing local refusal/no second POST/draft retention, and verified replacement owner/new base POST. The fixture preserves the actual native Agent move fields (`at`, `app.astrid.fixed_start/for`) and checks exact patch/read/basis/base/mirror/new-ID/hold-6 properties; no executor, custody, or invented reads are present.

**Limit:** this is not recovery of exact live service failure `28486` and not a real Runtime 409 proof. The 409 is locally mocked, no browser/HTTP/Runtime/Agent/service/full suite ran, and the original live refusal cause remains unverified. The synthetic reply helper is not authoritative Runtime evidence. The internal `JSON.stringify` pending-body equality proves durable reuse, not independent expected-wire-byte equality; unchanged neighboring tests retain the exact retry-byte/key assertions and full v2 envelope controls.

`npm run typecheck:strict-islands` was attempted and failed on the pre-existing missing Astrid pack/virtual modules; no direct test-file typecheck was run. No production/browser/spec/ops/HTTP/build/service edits or runs were made. No policy/UX change is owed by this diagnostic alone.

For a future E2E, deterministically schedule: split ACK; Agent native move against the accepted split pin; controlled poll delivery before owner adoption; immediate real Source In capture against the still-verified App basis; then allow the real request and Runtime conflict classification. Do not force the old pair, bypass original verification, omit reads to manufacture atomic mode, or guess `atomic_scope_changed` versus field conflict. Assert whichever conflict details the actual request and Runtime return establish.
