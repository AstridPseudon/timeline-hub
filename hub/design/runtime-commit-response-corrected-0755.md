# R-commit-response corrected source call-map

Successor to the author0745 source call-map. The original artifact is
preserved unchanged at the author worker path. This successor incorporates the
narrow independent0750 correction below.

## Scope and pinned revisions

This is a source-only call-map for the existing commitTimeline path. It does
not change product code, tests, generated clients, kits, pins, the D47 memo or
any authority backend. Static repetitions are not measured cost and are not a
deletion recommendation.

Pinned revisions:

- Runtime `37eb6c7bdb79dcae2523883e66b5cea5be721ffd`
- App `66354161950d1e747965c095ea97b881d2592708`
- Agent/sdk `079580ca46af77e0292d49dc34386b25c8391f99`

## Correction to the prior cardinality claim

The author0745 wording “three command validations per execution attempt” is
withdrawn. It is not correct for a CAS retry.

For one native command on the normal initial provider execution, the source
has three validation call sites:

1. `astrid/sdk/timeline/commit.py:945-955` validates each copied command in
   `execution_calls` before the provider's initial `execute`.
2. `astrid/sdk/timeline/commands.py:189-211` validates each supplied command
   inside `execute`.
3. `commands.py:218-219` calls `_normalize`, and
   `commands.py:155-157` validates the command again.

The CAS loop is `commit.py:1082-1196` (`for attempt in range(3)`), with stale
head handling continuing at `1191-1196`. Its replay path re-enters
`execute` at `commit.py:1122`. The outer `commit.py:945-955` validation is
outside that loop, so each CAS retry redoes only two command-validation call
sites: `commands.py:210-211` and `_normalize`→`155-157`. Thus the exact
static cardinality is three on the initial execution and two on each CAS retry
(up to the source loop's bounded retries), per command. This is a call-site
count, not an execution-time or measured-cost claim.

## App element mutation

The pinned App element path captures and submits one native command and one
step: `commitSession.ts:760-792` calls `finishElementEdit`, stores
`commands: [result.command]`, and enqueues it. `commitSession.ts:218-236`
builds the POST request, preserving that command, one step, `merge: fields`,
and `reads: []` for a non-`doc.patch` command. The outbox allocates the
request key at `commitOutbox.ts:464-483`; generated transport puts it in the
`Idempotency-Key` header at `generated.ts:202-204`.

The separate local-save handoff can emit a `doc.patch` request
(`timelineLocalSaveHandoff.ts:337-377, 566-577`); the one-command native
cardinality above is scoped to the `commitSession` element port. The retained
App evidence has no response outcome, abort, completion, or daemon identity.

## Static normal-path repetitions and authority boundaries

The Runtime request schema is separately validated at
`runtime_protocol/timeline_commit_port.py:60-65` / service
`service.py:2433-2446`; that is request-boundary validation, not the Agent
command validation counted above.

For a non-replay accepted mutation, accepted-record verification spans
distinct authority phases. Agent preflight reads the base closure, current
head, and base history at `commit.py:973-978`; the port history path reaches
`timeline_commit_store.py:433-451`, including `_verify_accepted`. Runtime
acceptance repeats base-history verification in `_check_context`
(`timeline_commit_store.py:1184-1192`) and current-head verification in
`_check_head` (`1194-1203`); `head` reaches `_head_entry`, which reaches
`history_entry` (`395-451`). After acceptance, coordinator replay lookup
(`timeline_commit_execution.py:99-103`) calls store lookup and
`_verify_accepted` (`timeline_commit_store.py:172-200`).

The acceptance transaction also redoes candidate-level prepared/schema and
closure guards (`timeline_commit_store.py:1217-1220`, `866-940`), while the
port boundary checks prepared ownership/materialization
(`timeline_commit_port.py:623-637`). These checks are not safely removable
from this source evidence: provider preflight is outside the acceptance lock,
acceptance checks are the authoritative CAS and current-owner guard, and
post-accept replay verifies that the durable winner is the response source.

Canonicalization is likewise repeated: request identity/hash at
`service.py:2474-2481`, `timeline_commit_execution.py:69-75`, and
`timeline_commit_store.py:1184-1192`; durable records/document/events are
digested during acceptance and post-accept verification
(`timeline_commit_store.py:872-873`, `1417-1423`, `202-295`). No timing or
daemon conclusion follows from these source calls. Same-mutation proof reuse
is only a future research seam, not a D47 exception or implementation basis.

## Causal limits and precise missing evidence

- The actual App element POST outcome and daemon attachment remain unknown.
- Resource durations `14.35s` and `15.47s` are client/resource durations, not
  Runtime server-processing times.
- ACP `503` is an unrelated chat GET, not evidence of a timeline commit
  failure.
- The precise missing evidence is a handler-side trace or durable receipt
  attribution linking the observed App POST/`Idempotency-Key` to the terminal
  Runtime handler outcome (`accepted`, `merged`, `conflict`, `invalid`, or
  unknown). No such trace/attribution is present.

No implementation is justified by this call-map. Existing request/reply and
authority scope remain unchanged.

## C0 contract boundary retained

The production caller's request remains: `api_version`, `project_id`,
`timeline_id`, exact `base_revision_id`/`base_publication_id`, nonempty
`commands`, `label`, `steps` (`id`, `label`, `intent`, `tags`,
`command_ordinals`, `patch`, `reads`), `merge` (`fields` or `atomic`),
`reads`, `dry_run`, `source`, `rationale`, `group_id`, and
`Idempotency-Key`.

Replies remain:

- accepted/merged: canonical document, head/revision/digests, records,
  effects, bindings, dependencies, history, undo steps, and full receipt;
- preview: `would_status` and null receipt;
- conflict: reason, head, and current;
- invalid: code, path, hint, and suggested command.

No new fields, rules or backends are proposed here; nothing is deleted.

## SHA-256 source hashes

Runtime:

- `runtime_protocol/service.py`
  `51cf343781cc79cb93831ec3b4a075025b6df47f73fc0184c8a43457453c9404`
- `runtime_protocol/timeline_commit_store.py`
  `4d975505c876731eefafc5c8bf8bb79783c2d5c151392163406b1e971004be99`
- `runtime_protocol/timeline_commit_execution.py`
  `2b0c256757f1bf0b3ab3124840250d2d8ef5dbec31a259c4b1e924e295619dd6`
- `runtime_protocol/timeline_commit_port.py`
  `0d44b5a5e1e0374239df461cb5094ff4fe5bb70761233efd4e3a65c2b29b0859`

App:

- `src/tools/video-editor/hooks/useTimelineSave.ts`
  `33e0ff6b26689e8af62b099557e8455f6ba87ad2b9bbbcbc69e42ac84918638a`
- `src/tools/video-editor/commands/commitSession.ts`
  `7bddb9c4adc28ff7d7079c4011ae965e65952570abe248f3d0247789a3532648`
- `src/tools/video-editor/commands/localSaveSession.ts`
  `08821033a3d764ef2305c157149f68eea621818602ea26558b4cb606b635856a`
- `src/tools/video-editor/commands/elementCapture.ts`
  `e7e1630a88abf5e8fa06f569bcc0000f7ebf9a43e15e1abba596865426fd76fc`
- `src/tools/video-editor/commands/elementGesture.ts`
  `7ab18452e1854038e27456369613eb0b0ac13f0fc3d4ffb44f512e10d39c3a5e`
- `src/tools/video-editor/hooks/timelineLocalSaveHandoff.ts`
  `33b7a69528014bb91263fa42a79a08e75f9b33ea679baad8a7870839bb51bb58`
- `src/integrations/runtime/generated.ts`
  `7be7f351d485fdb24a7ebb0329fea7c65037675b11a96c581d33e60a14a581a4`
- `src/tools/video-editor/commands/commitOutbox.ts`
  `dc497f0676b72abee0736abe19f0c33848a059776440db507375847a12160b21`

Agent/sdk:

- `astrid/sdk/timeline/commit.py`
  `f4272228f5c663d2f586aa5cc4f8ef2486aad4e4d38ca99e9433b6a991e53dbd`
- `astrid/sdk/timeline/commands.py`
  `9858390bbced10eb2ca1112dcbd16d092a12c34f5a3eebcf2ed218fe087ff6a2`
- `astrid/sdk/timeline/validation.py`
  `dc3305e24bcad677c6573c5bdd8557e2a60d72dd9eedd03c307f8c8a78bf8fbc`
