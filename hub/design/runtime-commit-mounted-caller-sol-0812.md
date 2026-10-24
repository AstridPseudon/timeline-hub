# R-commit-response mounted-caller corrected source call-map

Successor to corrected0755, retaining independent0750/0756 Agent and Runtime
findings and applying App peer0802 mounted-caller correction. Original0745,
corrected0755 and independent0756 remain immutable. Their App citation is
superseded below; their source-only causal limits remain in force.

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

## Mounted App caller correction (supersedes 0745, 0755 and App portion of 0756)

The claim that `commitSession.ts:760-792` proves the mounted catalog save
emits one native command, one step, `merge: fields`, and `reads: []` is
withdrawn. That is a retained D37 dormant protocol module. Its internal
one-command element port (`760-792`) and request builder (`218-236`) are
source facts about that module only. They do not establish the production
caller, its command kind, its metadata, or the observed POST payload.
No original artifact has been edited.

All App paths/lines below refer to exact selected App
`66354161950d1e747965c095ea97b881d2592708`, tree
`9a37265f0286128df7e6240a9df9877d959474af`, not current integration.

### Actual mounted chain

- `src/tools/video-editor/pages/VideoEditorPage.tsx:138-141` constructs the
  concrete `RuntimeDataProvider`. `hooks/useTimelineSave.ts:134-137` selects
  local document saving by the provider's three capabilities.
- The mounted element save at `hooks/useTimelineSave.ts:776-788` awaits the
  owner, calls `handoff.capture` with `kind: 'element'`, adopts the local preview,
  then awaits `handoff.flush()`. It does not call the dormant element port.
- `hooks/timelineLocalSaveHandoff.ts:337-380` checks the causal element edit
  and declares its original collection/field reads. `566-577` routes this
  element branch to `session.appendDocument`, with label `Edit timeline`,
  a UUID step ID, intent equal to the element operation name, empty tags,
  explicit `merge: 'atomic'`, and reads on both the intent and step.
  The `commands` alternative at `382-462` is populated for prepared media,
  not this element branch.
- `commands/localSaveSession.ts:304-311` encodes the document intent using
  `documentPatchIntent`; `documentPatchIntent.ts:130-215` computes guarded
  changes and allocated clip/track IDs. Its `216` returns null on no change;
  `219-222` retains the supplied step/merge/reads. Thus an unchanged document
  does not append an intent or prove a new POST.
- `commands/localSaveSession.ts:166-188` builds the request for the first
  retained intent, then `192` forwards its persisted body/key to `options.send`.
  `hooks/useTimelineSave.ts:319-323` binds that callback to the provider's
  `commitTimeline`.
- The concrete implementation `src/integrations/runtime/dataProvider.ts:751-767`
  checks identity and exact base presence, then passes the request and key
  unchanged to the client. `client.ts:687-694` wraps the generated call in
  `withMutation`. `generated.ts:202-204` serializes the request and performs
  POST to the scoped `/commit` route with `Idempotency-Key`; `78-90` uses the
  injected transport if supplied, otherwise HTTP `fetch` and response bytes.
  This is source wiring, not a new HTTP observation or daemon attribution.

### Source-derived request shape and cardinality

For a nonempty document intent from THIS mounted element capture, the builder
emits exactly one command:

`{ schema_version: 1, op: 'doc.patch', version: '1', select: null,
created: patch.created, args: { changes: patch.changes } }`.

This is proved by the active fallback array at `localSaveSession.ts:168-169`,
not by the dormant module. The number and values of patch changes, created IDs,
and reads depend on the authored edit/document. No concrete historical request
body or exact field/read count is inferred here.

`localSaveSession.ts:172-185` supplies:

- `api_version: 1`, scope project/timeline IDs, the outbox-ready exact
  `base_revision_id`/`base_publication_id`, and the nonempty command array;
- `label: 'Edit timeline'`, `dry_run: false`, `source: { via: 'app' }`;
- one step from `patch.step`, preserving its UUID `id`, label, operation-name
  intent, `tags: []`, and declared reads, with `command_ordinals: [0]` and
  `patch: patch.changes`;
- request `reads: patch.reads` and `merge: 'atomic'` for this element branch;
- optional `rationale`/`group_id` only when stored on the original save
  (`183-184`). This element `appendDocument` path stores before/after/label
  plus documentIntent (`311`), so these optional request properties are omitted.

The `fullV2` guard (`159-162`, `185`) is true for the selected source:
`generated-contract-metadata.ts:6` has the exact required schema digest
`sha256:35c2d9c5e0b51ab8d8b7a4f4dbafbdfcb13d232d7bd22fff21cf73e250398d4c`.
There is no inferred loss of metadata through the older-contract branch.

The element reads start with the selected parent clip collection's membership
and order (`timelineLocalSaveHandoff.ts:344-346`); field reads carry explicit
present/value or absent state (`347-350`). IDs, selected element/timing/params,
track and transition inputs vary with operation (`351-380`). Paths select
`['clips']` or `['config','clips']` according to authored layout. These are
not the dormant module's empty request reads.

Do not generalize one command/step to every save or every queued flush.
The same active session accepts `original.commands` and `original.steps`
(`localSaveSession.ts:168,176-178`), otherwise creates a default step covering
all command ordinals; it retains supplied reads rather than inventing `[]`.
For a document intent, the generic merge fallback is explicit patch.merge,
otherwise atomic for omitted reads or fields for supplied reads (`174-175`).
The pump processes retained intents sequentially (`130-158,203-208`).
One source-derived element intent is not a count of historical POSTs or retries.

The shared outbox allocates a UUID key once when reserving a new pending
request at `commands/commitOutbox.ts:474-483`; existing pending requests are
returned unchanged at `470-472`. It persists the exact serialized request
before invoking transmit (`485-491`). Local session `192`, provider `758-763`,
client `693`, and generated transport `204` propagate that key. Retry can reuse
the same pending body/key; source alone does not show whether it happened.

### Retained App source qualification, not rerun

Read the existing A4 census0438 and independent0444: both qualify shipped
production mounts on exact `c0fe88994405fd517b58473c14678a0d1b73056d`, tree
`8e3ef15ee5f7c08381d8dc9efb38b5c98845466d`. They separate D31/D37 dormant
custody and in-memory/dev fallback from production v2 callers. These are older
source qualifications, not a claim that their line numbers equal selected663.
The selected663 mounted chain above was inspected directly.

Read existing real-provider controls0707, independent0717, integrated0724:
0707 uses genuine RuntimeDataProvider/save lifecycle/adapter/outbox with
synthetic document and controlled fetch; 108 tests/7 files, three typechecks,
and scoped lint were reported passing. Independent0717 confirms that scope.
Integrated0724 reports source-tree equality and three controls passing.
These source/control facts qualify the production wiring and exact pending
body/key retention under controlled stalls. They are not original-fixture
Runtime completion, backend timing, browser GO, or historical cause proof.
No test, probe, benchmark, body export, browser, daemon or HTTP request was run.

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

## Additional exact-source hashes (SHA-256)

Hashes below are over `git show <revision>:<path>` bytes; repository revisions
are the pinned revisions above. No worktree or installed package substitutes.

- `src/tools/video-editor/pages/VideoEditorPage.tsx`
  `e80539d0ca6a450b774488c482449f858a1fc9f606b27ca8db0901bbaf1427df`
- `src/tools/video-editor/commands/documentPatchIntent.ts`
  `732473c05b7709b8a4bb95160df3f40679caca9e7fe26384fe0a2ec4d80d08b6`
- `src/integrations/runtime/dataProvider.ts`
  `9213ed6694cef931fe84fa3c83fda0b06ed02532c1b9b6271ef48c32d38f8988`
- `src/integrations/runtime/client.ts`
  `d72e551f409112cd8b7c8fe9a716fe79ac1b1542699b867d87d367ef4177fc08`
- `src/integrations/runtime/generated-contract-metadata.ts`
  `001186de18c627be1930c3b77b78afb1b15a3eea4bd8401931e251643f33c972`

## Immutable consumed artifacts (ORCH-relative paths; SHA-256)

- `workers/rt-R-commit-response-source-0745/evidence/source-callmap.md`
  `3109c0f51b6e83d0f47dabb222b5d142df5c4347142263ef576a5690da768f44`
- `workers/rt-R-commit-response-return-0755/evidence/source-callmap.md`
  `5c3871377f2fa9aff58a4aebcec8cb3abd3a71ab0a55190a297faa9f824f6ccb`
- `workers/rt-R-commit-response-final-review-0756/report.md`
  `dffb3ce4e16dbd293715be70bd54e69e283ffab6a66a0aeb273ac8794787b8c8`
- `design/app-A4-current-final-census-0438.md`
  `5c318b7c8182e551933389ec9e7c81489783a1e20a37aa1070c48b3a4cb4b344`
- `design/app-A4-final-census-review-0444.md`
  `c3c0ae2b6a1fc4322c8028f3b50270245b27f931d28ad7dc7ffcd25917fecc7d`
- `design/app-P2-current-causes-sol-0707.md`
  `989de834c02c826a136ef74beea6712d888065e9c6d13d347014c0af613ee1f3`
- `design/app-A3-real-provider-controls-review-0717.md`
  `f14e220c0eaf6436fd18aa8378e7aca1b2840251b0e653dc10e4078e53119562`
- `design/app-A3-provider-integrated-0724.md`
  `fc2832a52bce5117d32a9c6a819e31f23f0e8733fc39e0530b25921a47bedeb6`
- `design/peer-app-to-runtime-app2-orchestrator-20261024T0802-source-caller-correction.md`
  `a0e70966121d81bc3ce268ed610704084db37239466acdda8e86181de4625199`

## Verification and disposition

Read-only commands used: `git -C <repo> show <pinned revision>:<path>` with
`nl -ba | sed -n '<ranges>p'` for the exact line ranges cited above;
`git -C <repo> rev-parse '<pinned revision>^{tree}'` for all three pins;
Python `hashlib.sha256(subprocess.check_output(['git','-C',repo,'show',
revision+':'+path])).hexdigest()` for each selected source hash. All reads
succeeded. The existing 0755 source hashes matched re-read App/Runtime/Agent
blobs. Selected Agent tree is `2deab1a1494fbccfce5e9235412bacb8a949c0cd`;
Runtime tree is `be4114705127f9ee9e86b26cd6de3f467e771c01`.

No tests or existing controls were rerun, as required by this source-only brief.
No implementation, guard removal, pin adoption, or D47 exception is justified.
The missing handler-side trace or durable receipt correlation for the observed
POST/key remains the precise input needed for historical outcome attribution.
Independent whole-mounted-path worker0812 is separate; its verdict is not
assumed or claimed by this successor.
