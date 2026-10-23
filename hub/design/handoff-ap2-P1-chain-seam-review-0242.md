# P1 mounted chain seam review

Result: **FAIL — the reviewed blocker report needs correction; H3 remains NO-GO.**

Reviewed App `tl/ap2-P1-mounted-chain-source-0238` at `9d6df77ea` against
`design/commit-v2.md` §§1–5/7. Also inspected the current local A2 draft
`hub/timeline/app/tl/app-A2-production-v2-mount-r4` at `18f338e6b`, including
the production-handoff work at `a5cd83f5d` / `02a161cae`.

The original mounted-chain handoff is directionally right that the real
production chain is unavailable, but it overstates one requirement: C0c does
not require a new `clipSplitPort`, `clipSplitCapture.ts`, or a TypeScript split
executor. The A2 route may carry the upstream split as a guarded `doc.patch`
with an identity-list insert and stable created ID. That old-port demand is
rejected and is the reason this review is FAIL rather than an accurate PASS.

## Confirmed blockers

- The mounted UI still does `useClipSplitting.ts:28-33,46-51,70-80` →
  `applyConfigEdit` → the ordinary persistence path. There is no production
  session caller for `createLocalSaveSession`; the latest A2 draft only stages
  `originalLocalSaveBasis` and leaves activation explicitly pending.
- The current A2 handoff/session is opt-in. `useTimelinePersistence` accepts
  `localDocumentSave`, but `useTimelineSave` never constructs or passes it.
  The staged handoff can map raw parent edits and preserve opaque/null/absent
  data, but it cannot submit anything from the mounted editor yet.
- `documentPatchIntent.ts:161-220` already supplies the contract-compatible
  generic path: identity collections yield `list.insert`/move/remove with
  guards and `created: ["parent/clip:<id>"]`. This is not sent today because
  `localSaveSession.ts:141-153` blocks document intents until the generated v2
  join exists.
- The outbox does have the needed predecessor mechanism: dependent intents
  use `{ after: predecessor }`, exact pending request bytes/key are retained,
  and an accepted predecessor advances the dependent `readyBase`. Refusal
  currently marks the dependent suffix conflicted and the local session
  reloads/rolls back the visible draft; it does not implement C0c’s required
  dependent revalidation against the refusal head.
- The reviewed integration’s request DTO omits `steps`, `merge`, and `reads`;
  accepted/reply DTOs omit `merged`, authoritative steps/dependencies and
  `merge_mode`; preview omits `would_status`; failures omit `invalid` detail
  fields; history omits merge/read/step projection. The generated parser still
  rejects `merged` and only accepts `accepted`/`rebased`. The separate U4p
  draft adds type fields but still has that generated parser gap, so it is not
  complete v2 evidence.
- The existing `localSaveSession.test.ts` run is only synthetic transport and
  fake canonical results. It does not prove Runtime/Agent acceptance, merged
  canonical adoption, refusal revalidation, `id_map`, or durable history.

## Minimal owner follow-up

App A2 should join the official generated v2 client, instantiate the durable
session/handoff from the ready original verified read, pass it to the mounted
persistence hook, and encode the captured `documentIntent` as the approved
guarded `doc.patch` request/step. It must preserve all C0c request fields and
reply fields, stable split-created IDs, exact retry bytes/key, and canonical
accepted/merged adoption. On refusal it must revalidate the dependent trim
against the returned head or roll back the suffix with a message.

Do not add a split port just for P1. Keep the original required scenario
unchanged: App split → trim the newly-created ID → intervening Agent edit →
lost ACK → restart, covering accepted, merged, and refused replies. No
Agent-only split substitution is acceptable.

## Checks

- `node node_modules/typescript/bin/tsc --noEmit` — **PASS**.
- `node node_modules/eslint/bin/eslint.js src/tools/video-editor/commands/localSaveSession.ts src/tools/video-editor/hooks/clip-editing/useClipSplitting.ts --max-warnings 0` — **PASS**.
- `node node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --no-cache src/tools/video-editor/commands/localSaveSession.test.ts` — **PASS**, 15/15.
- `git diff --check` — **PASS**.

No repository edits, browser/socket/full/heavy runs, or real Runtime/Agent
chain execution were performed. This review is not P1 acceptance.
