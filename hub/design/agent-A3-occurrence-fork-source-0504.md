# R1-A3-occurrence-fork — source and consumer handoff

Provider source PASS; real Runtime service PASS; mounted App NOT PROVEN.

D15 implemented one registered Python semantic command; the 0445 optional marker proposal is not used. No schema, generated client, lock, pin, artifact or Runtime source changed. The 0445/0455 closed-carrier inference was wrong: frozen34e explicitly permits unknown operation envelopes pending registered schemas/handlers. Carrier finding: agent-A3-occurrence-fork-carrier-0504.md. Runtime retains the frozen34e tuple.

## Exact source identity

Worker agt-A3-occurrence-fork-0504; base Agent `9cf0fde2f57603813d81733ee8b0f7117ffd634c`; harness commit is pending (worker cannot commit). Exact source-set SHA256 (sorted compact JSON of path -> file SHA256): `e7c96edb911f6a1d89fb218cc951fea6094ee350f2ab62cbf039f951239e6830`. Per-file immutable hashes are in agent-A3-occurrence-fork-call-0504.json. Current tested Runtime source `be5848e17fbf68100286114883f5820fe4755911`, with unchanged schema SHA256 d106dfe8212500709b4072d7bc0486f83c27d5d8de33d215cb52b9ea7d46357d and normal frozen producer34e. No independent new producer tuple.

## App callable contract

Minimal command accepted by actual Runtime (replace fixture identities):

```json
{
  "schema_version": 1,
  "op": "occurrence.fork",
  "version": "1",
  "select": "occurrence:occ-0",
  "args": {
    "shot_id": "shot-fork"
  },
  "intent": {
    "ownership": "occurrence"
  },
  "created": [
    "shot:shot-fork"
  ]
}
```

Reserve shot_id once with the existing native ID allocator/outbox contract and retain the exact body/key across retries. The occurrence selector is the existing selected occurrence, never a new occurrence. The local registered parameter schema requires exactly shot_id, refusing extras/invalid IDs; no arbitrary new-op execution or schema exemption was added. Python callers may use `capture_occurrence_fork(bundle, owner, shot_id)` from native_occurrence_fork.py. The production provider registry invokes this handler through create_runtime_commit_service().commit; actual RuntimeService.commit_timeline with load_timeline_commit_provider('astrid') used it.

The created claim is REQUIRED on the Runtime request: only `shot:<reserved-shot-id>`. The provider record is `{ref:shot:<id>,kind:shot,owner:null}`. No created occurrence. New shot items receive the existing _copy_shot_for_placement deterministic IDs, based on project/timeline/selected occurrence/reserved shot/source raw item. Raw clip/track/asset IDs are preserved. Root/item reservation and collision checks remain native; id_map is the existing `{}` identity-allocation result, not a remapping instruction. Revision IDs and managed pins are provider/compiler outputs. Do not invent an App edge patch, another occurrence, duplicate/delete sequence, schema branch or tuple.

Full v2 request controls are unchanged. Supply label, steps(id,label,intent,tags,command_ordinals,patch,reads), merge, request reads, source/rationale/group_id and exact scope/base pair with stable idempotency. A semantic step can submit patch:[]; the provider returns the complete authoritative effects. Gesture read dependencies belong in request/step reads as D13 requires. The fixture request and complete native captured command/record/step shape are in agent-A3-occurrence-fork-call-0504.json; they are fixture fragments, NOT usable project IDs or HTTP credentials. The App may omit command recorder claims other than created; the provider reconstructs them. If supplied, claims must match exactly and forgery refuses.

Native captured reads (tagged state:present|absent) include parent.config.pinnedShotGroups, the complete selected occurrence row, selected /shot.shot_id, raw clip/track collection shape and membership/order, complete selected /source, complete authored /shot.payload, and absent destination shot root. Selections/bindings retain the selected owner. `fork.source` resolves the exact physical source internal image at the command boundary; v2 records retain authenticated physical bindings, full effect union and step dependencies. Fresh child and selected ownership are written through native recording/compiler paths. The fork is an ownership replacement; it does not grant global continuation/broadcast authority over a sibling's old physical image.

Occurrence ID/count/order/timing/map and opaque fields remain exact. Only selected shot ownership/pin changes. A shared shot and distinct shots sharing an internal image both retain the sibling's original shot and internal bytes. Complete internal payloads, raw windows and item opaque metadata survive. Subsequent native edits target only the new child.

Undo uses existing timeline.inverse publications (and existing optional steps). It restores the selected source using authenticated accepted boundaries, never current/latest guessed images. The helper also supplies those verified sources to immutable closure/timing compilation when the source no longer survives at the head. Created-child removal retains native surviving-consumer/ABA/history guards. Native redo that recreates the shot must claim created:[shot:<id>] as other native root births do; actual Runtime refuses a missing created claim. No guards were relaxed.

## Evidence and limits

- Frozen34e git-show semantic schema AND complete generated-bundle CommitRequest validated occurrence.fork; current Runtime request validator also passed. Generator source imports the same generic EditCommand. Unknown op without provider registration remains unsupported. No generation needed.
- Final scoped source tests: 244 PASS (fork/provider, duplicate/delete neighbours, step undo, V2 timing/validation, vendor parity/artifact baseline).
- Actual Runtime service: 1 PASS. Normal bootstrap/native create/duplicate seed, exact minimal fork envelope, disjoint v2 merged reply, selected identity and sibling preservation, immediate exact undo/redo, native shot edit, surviving-consumer refusal. No sockets/HTTP/browser/render/P5/full suite. This seed has distinct child images; shared physical-source fork->edit and undo were proved in direct provider/native tests, not mounted App or a shared Runtime HTTP seed.
- Scoped Ruff PASS; scoped mypy PASS10; normal Ruff ratchet 2149/2149; final mypy ratchet recorded in worker report. Diff check clean. Original existing V2 assertion remains unchanged, including its timing-adapter spy.

App next: wire the named semantic command into the existing persisted A2 outbox before shared ADD/SWAP/child placement, carry created claims/stable reservations and declared gesture reads, then qualify mounted behavior/reload/guarded undo. For a combined gesture use fork then media/placement in one commit with appropriate sequential steps; preparatory fork-step undo must refuse a surviving later edit. The provider-only and service proof does NOT close mounted A3/H3. Runtime needs no new tuple or schema release for this command.
