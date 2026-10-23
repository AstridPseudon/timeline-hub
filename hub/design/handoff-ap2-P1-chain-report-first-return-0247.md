# P1 chain report — first return after independent review

Result: **BLOCKED — H3 NO-GO; no P1 acceptance.** This is a corrected design
handoff, not a product or test implementation.

## Reviewed basis

The source is App `tl/ap2-P1-mounted-chain-source-0238` at exact
`9d6df77eac9a3e32854dcee79e1213c48feb9573` (`9d6df77ea`). The independent
review is `handoff-ap2-P1-chain-seam-review-0242.md`. C0c sections 1–5 and 7
were read from the approved `commit-v2.md` contract.

The independent review correctly rejects the previous handoff's unsupported
demand for `clipSplitPort`, split capture/finish code, and a TypeScript
executor. A guarded `doc.patch` identity-list `list.insert` with a stable
authored created ID fits the contract. The reviewed production caller using
that route remains unproved.

## Corrected blocker

The missing seam is the production mount of the existing durable
`localSaveSession`/handoff through
`useTimelineSave → useTimelinePersistence → persisted outbox`, plus the
official v2 generated client/status join. The mounted editor still routes
`useClipSplitting` through `applyConfigEdit` and ordinary snapshot persistence;
`useTimelineSave` does not activate the durable handoff, and
`createLocalSaveSession` has only test callers.

Before P1 can run, that seam must submit the captured guarded `doc.patch`,
reserve one stable authored right-hand clip ID, and make canonical created-ID
dependents consume the predecessor's accepted/merged `id_map` and landed
document. The outbox must retain exact request bytes and key across a lost ACK
and restart. On refusal it may either revalidate the dependent suffix against
the returned head or use the permitted suffix rollback with a user-visible
message; revalidation is not mandatory if the rollback path is correctly
implemented. Neither outcome is currently proven.

## Required chain and wire contract

The original scenario remains mandatory: **App split → trim the new ID →
intervening Agent edit → lost ACK → restart**, with accepted, merged, and
refused outcomes. The merged case must preserve the Agent field. Refusal must
not overwrite it or leave a stale dependent intent. No Agent split substitute
is acceptable.

The request must retain `api_version: 1`, `project_id`, `timeline_id`, both
base IDs, ordered commands, `label`, complete step patches and reads, `merge`,
request-level `reads`, `dry_run`, and the HTTP `Idempotency-Key`. The command
envelope and guarded changes retain `schema_version`, `op`, `version`,
`select`, `args`, and tagged `before` values.

Accepted/merged replies must retain the full `{data, receipt}` result:
canonical closure/document, digest, normalized commands, canonical `id_map`,
receipt, complete authoritative steps and dependencies, and effective
`merge_mode`, alongside status, base/previous/accepted IDs, `rebased_onto`,
provider/compiler versions, and publisher. Conflict/refusal retains the head;
invalid retains code/path/hint; preview retains `would_status`. Exact retry
after lost ACK returns the original envelope without duplicate history or
execution; a changed body under the same key is `idempotency_mismatch`.

## Evidence and limits

Existing review evidence is unchanged: `node
node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts
--no-cache src/tools/video-editor/commands/localSaveSession.test.ts` — **PASS,
15/15**; `node node_modules/typescript/bin/tsc --noEmit` — **PASS**; `node
node_modules/eslint/bin/eslint.js
src/tools/video-editor/commands/localSaveSession.ts
src/tools/video-editor/hooks/clip-editing/useClipSplitting.ts --max-warnings 0`
— **PASS**; and `git diff --check` — **PASS**. Those checks were not repeated
for this documentation-only correction. No browser, socket, Runtime/Agent
chain, full suite, product test, fixture, schema, generated-client, pin,
launcher, or repository edit was made.

The authoritative status is therefore **corrected BLOCKED**, with **no P1
acceptance**. The next action belongs to App A2 production integration; after
that seam lands, rerun the real three-products chain and reassess H3.
