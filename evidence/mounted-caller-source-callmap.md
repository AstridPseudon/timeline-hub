# R-commit-response mounted-caller source call-map

Read-only correction against the selected sources. No product, test, pin, or
generated source was changed.

## Verdict

- **Prior mounted-caller citation: FAIL.** `commitSession.ts` is dormant D37
  protocol code and cannot prove the mounted catalog/element save path.
- **Corrected mounted-caller citation: PASS, qualified to a non-empty element
  edit.** The mounted chain is:
  `useTimelineSave.ts:776-788` ->
  `hooks/timelineLocalSaveHandoff.ts:257-590,598-617` ->
  `commands/localSaveSession.ts:304-311,158-200` ->
  `integrations/runtime/dataProvider.ts:751-768` ->
  `integrations/runtime/client.ts:687-694` ->
  `integrations/runtime/generated.ts:202-204`.

## Mounted request shape

The element branch captures the operation and calls the mounted handoff at
`useTimelineSave.ts:782-788`. The handoff records the element's collection
and field reads at `timelineLocalSaveHandoff.ts:337-381`, then calls
`appendDocument` with `merge: "atomic"`, one generated step, and the element
operation name at `:565-577`. `localSaveSession.ts:304-311` invokes the
document-patch encoder; a no-op returns without creating an intent.

For a non-empty element diff under the official full-v2 digest,
`localSaveSession.ts:168-185` emits one `doc.patch` command with the encoded
`created` list (normally `[]` for this edit), `args.changes`, one step with
`command_ordinals: [0]` and the same patch changes, top-level `merge:
"atomic"`, top-level `reads`, `label: "Edit timeline"`, `dry_run: false`, and
`source: { via: "app" }`. The request carries the exact outbox head's
`base_revision_id` and `base_publication_id`; `rationale` and `group_id` are
not supplied by this element document-intent branch. The route is the
canonical project/timeline `/commit` path at `:186-188`.

The outbox allocates a random UUID request key after durable reservation at
`commitOutbox.ts:464-491`; retries reuse that stored request/key. Generated
transport serializes the request with a finite-number guard and sends the
same key as `Idempotency-Key` at `generated.ts:202-204`.

This is not a universal one-command claim: prepared-media can take the
native-command branch at `timelineLocalSaveHandoff.ts:385-461`, and a
no-change document intent sends no commit.

## Control-source comparison

The real-provider routed control source is App commit
`2056c7c0b21b5d5fa9ee2711897833f2deadf95d` (0707), merged by
`38b29b5e295f0ef0c6cee6af598812021d7105aa` (0724); the 0717 review accepted
that same control source. Its request assertion at
`VideoEditorProvider.runtime-elements.test.tsx:183-188` matches the mounted
shape: exact base pair, `merge: "atomic"`, `dry_run: false`, App source, a
`doc.patch` command, one step with ordinal `[0]` and intent
`timeline.apply_element`, a reads array, and step patch equal to command
changes. Its pending-outbox assertion at `:171-177` confirms persisted body,
key, and original head basis. This is source/test control evidence, not a
live Runtime receipt.

## Preserved independent facts

Agent command validation remains three call sites on initial execution and
two on each CAS retry: outer `commit.py:945-955` is outside the
`commit.py:1082-1196` retry loop; retries re-enter `execute` at `:1122` and
repeat `commands.py:210-211` plus `_normalize` -> `commands.py:155-157`.
Runtime preflight, locked acceptance/CAS/current-owner checks, and
post-accept winner replay remain separate authority boundaries. Their static
repetition does not establish cost or justify removing guards.

The actual POST terminal outcome and daemon attachment remain unknown. The
14.35/15.47-second resource durations are not server-processing measurements,
and the unrelated ACP 503 is not timeline-commit evidence. Missing evidence
is a handler-side trace or durable receipt attribution linking the observed
POST/key to a terminal Runtime outcome. C0 request/reply fields and D47
deferral are unchanged.

## Pinned revisions and source hashes

- App `66354161950d1e747965c095ea97b881d2592708`:
  - `useTimelineSave.ts` `33e0ff6b26689e8af62b099557e8455f6ba87ad2b9bbbcbc69e42ac84918638a`
  - `timelineLocalSaveHandoff.ts` `33b7a69528014bb91263fa42a79a08e75f9b33ea679baad8a7870839bb51bb58`
  - `localSaveSession.ts` `08821033a3d764ef2305c157149f68eea621818602ea26558b4cb606b635856a`
  - `dataProvider.ts` `9213ed6694cef931fe84fa3c83fda0b06ed02532c1b9b6271ef48c32d38f8988`
  - `client.ts` `d72e551f409112cd8b7c8fe9a716fe79ac1b1542699b867d87d367ef4177fc08`
  - `generated.ts` `7be7f351d485fdb24a7ebb0329fea7c65037675b11a96c581d33e60a14a581a4`
  - `commitOutbox.ts` `dc497f0676b72abee0736abe19f0c33848a059776440db507375847a12160b21`
  - `documentPatchIntent.ts` `732473c05b7709b8a4bb95160df3f40679caca9e7fe26384fe0a2ec4d80d08b6`
- Runtime `37eb6c7bdb79dcae2523883e66b5cea5be721ffd`; prior source hashes for
  `service.py`, `timeline_commit_store.py`, `timeline_commit_execution.py`,
  and `timeline_commit_port.py` remain verified in the independent review.
- Agent/sdk `079580ca46af77e0292d49dc34386b25c8391f99`.
