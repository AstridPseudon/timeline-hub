# R-commit-response source call-map

Pinned revisions:

- Runtime `37eb6c7bdb79dcae2523883e66b5cea5be721ffd`
- App `66354161950d1e747965c095ea97b881d2592708`
- Agent `079580ca46af77e0292d49dc34386b25c8391f99`

## App element mutation

The pinned App element path captures and submits one native command and one
step: `commitSession.ts:760-792` calls `finishElementEdit`, stores
`commands: [result.command]`, and enqueues it. `commitSession.ts:218-236`
builds the POST request, preserving that command, one step, `merge: fields`,
and `reads: []` for a non-`doc.patch` command. `useTimelineSave.ts:776-788`
waits for `handoff.capture` and then `handoff.flush`; no response outcome is
visible in the retained App evidence.

## Static normal-path repetitions

For this one-command native request, the pinned Agent validates the same
command at least three times per execution attempt:

1. `astrid/sdk/timeline/commit.py:950-955` validates `execution_calls`.
2. `astrid/sdk/timeline/commands.py:210-211` validates each command in
   `execute`.
3. `astrid/sdk/timeline/commands.py:218-219` calls `_normalize`, which calls
   `validate_command` again at `commands.py:155-157`.

The Runtime request schema is separately validated at
`runtime_protocol/timeline_commit_port.py:60-65` / service
`service.py:2433-2446`; this is request-boundary validation, not the Agent
command validation above.

For a non-replay accepted mutation, accepted-record verification is repeated
across boundaries. Agent preflight reads the base closure, current head, and
base history at `commit.py:973-978`; `port.history_entry` reaches
`timeline_commit_store.py:433-451`, including `_verify_accepted`. Runtime
acceptance repeats base history verification in `_check_context`
(`timeline_commit_store.py:1184-1192`) and current-head verification in
`_check_head` (`1194-1203`); `head` calls `_head_entry`, which calls
`history_entry` (`395-451`). After acceptance, coordinator replay lookup
(`timeline_commit_execution.py:99-103`) calls store lookup and
`_verify_accepted` (`timeline_commit_store.py:172-200`).

The acceptance transaction also redoes candidate-level prepared/schema and
closure guards (`timeline_commit_store.py:1217-1220`, `866-940`), while the
port boundary checks prepared ownership/materialization (`timeline_commit_port.py:623-637`).
These are not safely removable from source evidence: provider preflight is
outside the acceptance lock, acceptance checks are the authoritative CAS and
current-owner guard, and post-accept replay verifies that the durable winner
is the response source.

Canonicalization is likewise repeated: request identity/hash at
`service.py:2474-2481`, `timeline_commit_execution.py:69-75`, and
`timeline_commit_store.py:1184-1192`; durable records/document/events are
digested during acceptance and post-accept verification
(`timeline_commit_store.py:872-873`, `1417-1423`, `202-295`). No timing or
daemon conclusion follows from these source calls.

## SHA-256 source hashes

Runtime:

- `runtime_protocol/service.py` `51cf343781cc79cb93831ec3b4a075025b6df47f73fc0184c8a43457453c9404`
- `runtime_protocol/timeline_commit_store.py` `4d975505c876731eefafc5c8bf8bb79783c2d5c151392163406b1e971004be99`
- `runtime_protocol/timeline_commit_execution.py` `2b0c256757f1bf0b3ab3124840250d2d8ef5dbec31a259c4b1e924e295619dd6`
- `runtime_protocol/timeline_commit_port.py` `0d44b5a5e1e0374239df461cb5094ff4fe5bb70761233efd4e3a65c2b29b0859`

App:

- `src/tools/video-editor/hooks/useTimelineSave.ts` `33e0ff6b26689e8af62b099557e8455f6ba87ad2b9bbbcbc69e42ac84918638a`
- `src/tools/video-editor/commands/commitSession.ts` `7bddb9c4adc28ff7d7079c4011ae965e65952570abe248f3d0247789a3532648`
- `src/tools/video-editor/commands/localSaveSession.ts` `08821033a3d764ef2305c157149f68eea621818602ea26558b4cb606b635856a`
- `src/tools/video-editor/commands/elementCapture.ts` `e7e1630a88abf5e8fa06f569bcc0000f7ebf9a43e15e1abba596865426fd76fc`
- `src/tools/video-editor/commands/elementGesture.ts` `7ab18452e1854038e27456369613eb0b0ac13f0fc3d4ffb44f512e10d39c3a5e`

Agent:

- `astrid/sdk/timeline/commit.py` `f4272228f5c663d2f586aa5cc4f8ef2486aad4e4d38ca99e9433b6a991e53dbd`
- `astrid/sdk/timeline/commands.py` `9858390bbced10eb2ca1112dcbd16d092a12c34f5a3eebcf2ed218fe087ff6a2`
- `astrid/sdk/timeline/validation.py` `dc3305e24bcad677c6573c5bdd8557e2a60d72dd9eedd03c307f8c8a78bf8fbc`

