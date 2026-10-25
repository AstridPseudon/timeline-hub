# P2/A2/A3 Native Wholepath Source Report

## Result

Completed the independent read-only source map. No source, test, pin, metadata, or design files were changed. Worktree remains clean.

The production native Undo request is independently established as:

```json
{
  "api_version": 1,
  "project_id": "P",
  "timeline_id": "T",
  "base_revision_id": "rT",
  "base_publication_id": "pT",
  "commands": [{
    "schema_version": 1,
    "op": "timeline.inverse",
    "version": "1",
    "select": null,
    "args": { "publications": ["pT"] }
  }],
  "label": "Undo timeline",
  "steps": [{
    "id": "uStep",
    "label": "Undo timeline",
    "intent": "Undo timeline",
    "tags": [],
    "command_ordinals": [0],
    "patch": []
  }],
  "merge": "fields",
  "reads": [],
  "dry_run": false,
  "source": { "via": "app" }
}
```

`uStep` is the outbox intent UUID. The `Idempotency-Key` header is a separate UUID. `pT` is the target accepted publication/receipt ID, not the idempotency key.

Sources:

- App Undo command construction: `src/integrations/runtime/dataProvider.ts:770-800`
- Outbox request shape and native `fields` merge selection: `src/tools/video-editor/commands/commitSession.ts:176-236`
- Dynamic intent and idempotency IDs: `src/tools/video-editor/commands/commitOutbox.ts:146-149`, `464-529`

This exposes the concrete oracle mismatch: the current test helper expects `merge: "atomic"` at `tests/e2e/local/three-products.p2-elements-assets.spec.ts:179-210`, but native inverse production code emits `merge: "fields"` because it has no `doc.patch`.

## Wholepath

```text
App gesture
  -> commitSession undo intent
  -> persisted outbox / exact retry bytes and Idempotency-Key
  -> Runtime commit endpoint
  -> Agent timeline.inverse validation and inverse execution
  -> Runtime authoritative recorder/history publication
  -> App accepted response
  -> Runtime canonical revision + dependency readback
  -> independent canonical document/digest comparison
```

Runtime remains the sole writer. Agent supplies inverse semantics, guards, dependencies, and effect recording.

Sources:

- Runtime-only writer and Agent semantic provider: `/home/user/work/runtime/contract/commit-v2.md:1-5`
- Runtime execution and publish path: `/home/user/work/runtime/runtime_protocol/timeline_commit_execution.py:69-121`, `/home/user/work/runtime/runtime_protocol/timeline_commit_store.py:1522-1589`, `1732-1763`
- Agent inverse execution: `/home/user/work/agent/astrid/sdk/timeline/commands.py:201-308`, `/home/user/work/agent/astrid/sdk/timeline/commit.py:1238-1444`
- App canonical readback: `src/integrations/runtime/dataProvider.ts:885-988`

## Independently supported expectations

| Area | Expected relationship |
|---|---|
| Request command | `timeline.inverse`, version `1`, `select:null`, target publication in `args.publications`; no caller-supplied inverse writes |
| Request step | Submitted `patch:[]`; this is a claim boundary, not the authoritative effect patch |
| Request reads | Top-level `reads:[]`; step-level `reads` is omitted by the App builder |
| Merge | Native inverse is `fields`; `atomic` is reserved for `doc.patch` requests |
| Command `expect` | Agent-generated guards for each inverse write. For target `before = U0`, target `after = U1`, inverse expects current value `U1` before restoring `U0` |
| Absent/null | `ABSENT` is distinct from explicit null: `{"state":"absent"}` versus `{"state":"present","value":null}` |
| Authorship | Agent-generated direct authorship for restored writes; not supplied by App |
| Reads | Replayed/generated from accepted target records, semantic captures, and inverse validation; never copied from the final reply or synthesized from the final diff |
| Selections | Exact collection membership/order/boundary guards from target records and inverse replay |
| Bindings | Normalized command bindings plus physical record bindings carrying references, revisions, digests, evaluation boundaries, and paths |
| Created | Provider-generated created/restored identities from authenticated target history and materialization; not invented from canonical output |
| Writes | Full normalized before/after effect records, including root, collection, mirror, and materialization effects where applicable |
| Step patch | Provider-derived effect patch from inverse execution, not the submitted empty patch |
| Dependencies | Provider-only normalized union of inherited request reads, step reads, semantic captures/selections/bindings, compiler effects, materializations, and conservative scope dependencies |
| History | `records.undo_of: [pT]`; `undo_steps: null` for whole-commit Undo; authoritative records must match the accepted result |
| Receipt | Runtime-generated `receipt_id`, distinct from the request idempotency key |
| Canonical result | Accepted canonical document must equal independent post-Undo Runtime readback; digest must match that document |

Sources:

- Request/reply and absent/null contract: `/home/user/work/runtime/contract/commit-v2.md:60-155`, `458-505`
- Accepted dependency semantics: `/home/user/work/runtime/contract/commit-v2.md:112-155`
- Runtime authoritative metadata and validation: `/home/user/work/runtime/runtime_protocol/timeline_commit_store.py:81-109`, `1181-1255`
- Agent recording of writes, reads, bindings, created, dependencies, and guards: `/home/user/work/agent/astrid/sdk/timeline/_recording.py:71-287`
- Agent provider-derived effect and dependency construction: `/home/user/work/agent/astrid/sdk/timeline/_commit_patch.py:494-652`
- Inverse guards and restoration: `/home/user/work/agent/astrid/sdk/timeline/inverse.py:1027-1181`
- Whole-commit selection and `undo_steps:null`: `/home/user/work/agent/astrid/sdk/timeline/_step_undo.py:87-128`

## Worked fixture relationships

### Parameter edit

Let `O` be the original canonical document. The target commit changes:

```text
parent/clips/C/params: U0 -> U1
```

The target accepted publication is `pT`, revision `rT`.

Native Undo must use base `(rT, pT)` and target `pT`. The authoritative inverse effect restores:

```text
parent/clips/C/params: U1 -> U0
```

The inverse guard expects `U1`. If `U0` was absent, the inverse writes an absent state; if `U0` was explicit null, it writes present-null.

### Element creation

For original document `O`, the target creates dynamic clip `Cnew` plus its registry/manifest closure. Undo targets the accepted target publication, not the dynamic ID directly. The independent expected result is that `Cnew` and its dependent closure are removed while all original identities and digests in `O` remain intact.

### Asset registration

The target creates dynamic registry/manifest identities. Those IDs come from the accepted target records and must not be invented from the response. Undo restores the original registry/manifest closure and preserves unrelated canonical content.

### Placement

The target changes occurrence, shot, and internal-timeline closure. Undo must restore the original parent/shots/internals from `originalcanonicalbefore`. The placement publication is a separate Runtime receipt from the idempotency key.

## What is independently available

Available from `originalcanonicalbefore`, target request/source, accepted target history, and target step:

- Target publication and revision linkage.
- Exact inverse command and base pair.
- Original field/root values and absent/null states.
- Target writes, reads, selections, bindings, created identities, and dependencies when retained in accepted history.
- Expected inverse guards and restored effect relationships.
- Expected whole-commit `undo_of` and `undo_steps:null`.
- Expected canonical closure, subject to concurrent/merged changes.

Only the actual post-Undo Runtime readback independently proves the final canonical document and digest. App already reads the canonical revision and dependency closure through `canonicalAt` and validates the response against that readback (`src/integrations/runtime/dataProvider.ts:885-988`; test helper `tests/e2e/local/three-products.p2-elements-assets.spec.ts:268-274`).

## Finite limits

The following cannot be safely filled from the final reply or canonical document alone:

- Exact recorder reads/selections/bindings/dependencies for a target whose accepted records are unavailable.
- Exact composite inverse effect ordering and materialization records.
- Runtime-generated publisher, receipt ID, accepted revision, `id_map`, and digest before execution.
- A full expected canonical document when unrelated changes are merged concurrently; the contract requires preserving those other changes.
- Any metadata not established by C0, accepted history, or the authenticated Agent/Runtime source.

No fallback to `objectContaining`, type-only/nonempty checks, expected-copy from the reply, invented authority/full payloads, or product relaxation is justified.

P315493 was used only as the passing comparator requested. Its former tuple behavior was not imported as current native proof. The existing review failures remain valid against the current source.

## Verification

Tests were not run. The brief explicitly requires READONLY source mapping and says no test/tsc/lint duplication is required.

Completion marker created:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-P2-native-wholepath-0218/DONE`