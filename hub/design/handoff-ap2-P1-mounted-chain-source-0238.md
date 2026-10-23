# P1 mounted mixed-chain source handoff

Status: **BLOCKED — corrected seam report; no fabricated chain spec.** H3
remains **NO-GO** and this is not P1 acceptance.

Base inspected: App `tl/ap2-P1-mounted-chain-source-0238` at exact
`9d6df77eac9a3e32854dcee79e1213c48feb9573` (`9d6df77ea`). This correction
incorporates independent review `handoff-ap2-P1-chain-seam-review-0242.md` and
the approved C0c contract sections 1–5 and 7.

## Correction to the earlier handoff

The earlier report was directionally right that the real mounted production
chain is unavailable, but it incorrectly demanded a new `clipSplitPort`,
`clipSplitCapture.ts`, or TypeScript split executor. C0c does not require any
of those. A2 may carry the upstream split as a guarded `doc.patch` identity-list
insert with a stable authored created ID. The existing contract-compatible
`documentPatchIntent.ts` path already describes that shape, including a
`created: ["parent/clip:<id>"]` effect.

The missing proof is narrower and unchanged in consequence: the mounted
production caller has not been shown to use that path. Do not replace the
required App split with an Agent-only split.

## Exact missing production seam

The current mounted UI still follows
`useClipSplitting.ts:28-33,46-51,70-80` → `applyConfigEdit` → the ordinary
snapshot persistence path. `useTimelineSave` does not construct or pass the
existing durable `localSaveSession`/handoff into `useTimelinePersistence`.
`createLocalSaveSession` currently has only test callers. Therefore the
mounted editor has not been proven to submit the captured split through the
persisted outbox, nor to expose its canonical created ID to the dependent trim.

The owner follow-up is to mount the existing durable handoff at
`useTimelineSave → useTimelinePersistence → persisted outbox`, join the
official v2 generated client and status types, and submit the captured
`documentIntent` as the approved guarded `doc.patch`. The production caller
must reserve and retain one stable authored right-hand clip ID, use the
canonical accepted/merged `id_map` and landed document to bind the dependent
trim, and retain the exact predecessor/dependent request bytes and keys across
lost acknowledgement and restart.

The outbox already has dependent intents of the form `{ after: predecessor }`
and retains exact pending request bytes/key. On predecessor acceptance, the
dependent base advances from the canonical landed pair. On predecessor
refusal, the implementation may either revalidate the dependent suffix against
the refusal head or roll the suffix back with a user-visible message; C0c does
not make revalidation mandatory when the permitted rollback-with-message path
is used. Neither permitted outcome is currently proven by the mounted
production caller.

## Required P1 chain, unchanged

The eventual source must drive the original mounted App scenario through the
real three-products fixture/harness:

1. **App split:** the mounted UI submits the split through A2 as a guarded
   `doc.patch` list insert, with the authored stable right-hand ID and the
   canonical created-ID effect.
2. **App dependent trim:** the mounted UI trims that newly created ID using the
   predecessor's canonical `id_map`/landed document; it must not recapture or
   invent a different ID.
3. **Intervening Agent edit:** an Agent edit lands while the App predecessor is
   pending, exercising disjoint merge behavior and the actual canonical head.
4. **Lost ACK and restart:** lose the durable acknowledgement, restart/reload,
   and retry the exact original request body with the exact original
   `Idempotency-Key`; there must be no duplicate history entry or re-execution.
5. Cover predecessor/dependent **accepted**, disjoint **merged** (preserving the
   Agent field), and **refused** outcomes. For refusal, prove either dependent
   revalidation at the returned head or the permitted suffix rollback with a
   clear message. A refusal must not overwrite the Agent edit or silently leave
   a stale dependent intent.

No Agent split substitute is acceptable, and no new split port/capture/executor
is required by this handoff.

## v2 request and outcome preservation

The mounted caller and generated client/status join must preserve the complete
v2 contract, not a reduced DTO. Every mutation request retains:

- `api_version: 1`;
- `project_id`, `timeline_id`, `base_revision_id`, and
  `base_publication_id`;
- ordered `commands` (native semantic commands or `doc.patch`), including
  `schema_version`, `op`, `version`, `select`, and `args.changes` with tagged
  `before` guards;
- nonempty `label`;
- complete ordered `steps`, each with stable `id`, `label`, `intent`, `tags`,
  `command_ordinals`, `patch`, and optional `reads`;
- `merge` (`fields` or `atomic`), request-level `reads`, `dry_run`, and the
  HTTP `Idempotency-Key`; and
- any existing `source`, `rationale`, or `group_id` annotations when supplied.

For accepted and merged success, preserve the full `{data, receipt}` envelope:
`status` (`accepted` or `merged`), base and previous head IDs,
`accepted_revision_id`, `rebased_onto`, canonical closure/document, document
digest, normalized commands, canonical `id_map`, provider/compiler versions,
authoritative `publisher`, complete authoritative `steps` including patches and
`dependencies`, effective `merge_mode`, and the durable receipt (including its
receipt ID/result and authenticated request identity). A merged canonical
document includes the intervening Agent change and must be adopted before
replaying still-pending local edits.

Preserve conflict/refusal replies with the returned `head` pair and structured
reason/details; preserve invalid replies with `code`, `path`, and `hint` (and
the complete invalid detail where supplied); preserve dry-run/preview replies,
including `would_status`, canonical preview data, steps/dependencies,
`merge_mode`, and no durable receipt/history entry. Exact retries after a lost
ACK or restart return the original accepted/merged envelope for the same body
and key; a changed body under the same key is `idempotency_mismatch`, not a
second edit.

The canonical closure and authoritative records must retain opaque, null,
absent, membership, and order data; resolved physical bindings; canonical
created-ID dependencies; receipt/request hash; complete command and step
records; dependencies; and merge mode. Do not reduce the proof to final bytes.

## Existing evidence and boundary

- Fixture `tests/fixtures/p1-feasibility/cases.json` remains explicitly
  `authored-not-go` for the missing mounted A2 handoff/created-ID binding and
  refusal handling.
- `tests/e2e/local/parent-split-command.spec.ts` proves only the standalone
  pre-A2 real-UI split path; it is not this mixed chain.
- The A2 draft's `originalLocalSaveBasis`/session staging does not prove that
  the mounted caller activates the handoff.
- Existing review evidence remains unchanged: `node
  node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts
  --no-cache src/tools/video-editor/commands/localSaveSession.test.ts` —
  **PASS, 15/15**; `node node_modules/typescript/bin/tsc --noEmit` —
  **PASS**; `node node_modules/eslint/bin/eslint.js
  src/tools/video-editor/commands/localSaveSession.ts
  src/tools/video-editor/hooks/clip-editing/useClipSplitting.ts
  --max-warnings 0` — **PASS**; and `git diff --check` — **PASS**. These
  checks were not repeated for this documentation correction.
- No browser, socket, Runtime/Agent chain, full suite, or heavy run was done.

This handoff changes no product, test, fixture, schema, generated-client,
pin, or launcher file. It adds no old route, rollback override, or executor
requirement. The next P1 attempt is unblocked only after the owning A2 seam is
mounted and the complete chain is executed; until then, report **BLOCKED** with
no P1 acceptance.
