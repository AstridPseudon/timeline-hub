# Historical render admission — proposed, owner decision required

Runtime base `9f9b25c`; Agent tested from integration (exact refs/results in worker report).
Companion: [render-commit-handoff.md](render-commit-handoff.md), D13; no implementation or wire change here.
First admission of accepted A after C/restart is distinct from retrying an already admitted A.

## Smallest selector on the existing render spec

Authenticated `POST /v1/tasks` (door `/api/runtime/v1/tasks`), existing `tasks:write`, project checks,
and required `Idempotency-Key: <durable-render-key>`; normal task request, with:
```json
{"project":"P","capability_id":"rendering.render","capability_digest":"sha256:<registered>",
 "input_object_ids":[],"spec":{"family":"render","params":{"timeline_ref":"T",
 "selector":"rendering.remotion","canonical_revision":{"project_id":"P","timeline_id":"T",
 "revision_id":"A","publication_id":"<accepted receipt_id>","content_digest":"sha256:<A payload>"}}}}
```
`canonical_revision` is optional, closed, and all five fields are required nonempty strings;
digest is exactly `sha256:[0-9a-f]{64}`. Null, partial objects, extra fields and wrong types refuse.
P/T must equal resolved outer project/timeline identities; these are selectors, never credentials.
`canonical_head_revision_id` remains an optional CURRENT-head expectation, never A's selector.
Other existing canonical expectations and `expected_version`, if supplied, still guard CURRENT state;
the durable historical handoff should omit mutable expectations so later C cannot strand A.
Omitting `canonical_revision` preserves existing current-head/legacy admission semantics.

## Runtime source validation and atomicity

Inside existing admission mutex/transaction, authorize project and unarchived timeline first.
Resolve exact scoped publication via `TimelineCommitStore.history_entry`, verifying the real receipt,
accepted result, history edge and revision binding; receipt identity alone is insufficient.
Require the selected revision's stored parent digest and receipt canonical image to agree exactly.
Load retained A via `revision_closure`; verify parent/shot/internal images and retained Document pins.
Its existing `_verify_inputs` verifies Documents, not all media bytes: explicitly verify each media,
scene package/entry/asset and narration dependency's retained bytes, size, digest and project custody.
Use existing verified legacy-source path only for real retained legacy publications; invent no history.
Do not read mutable child Documents or substitute C/latest input versions when resolving A.
Apply existing render projection, locator/injection rejection, budget and capability/readiness checks.
Validate everything before CAS snapshot publication, journal/object registration, receipt/task/run writes;
failure leaves database, CAS and staging unchanged. Recovery must not heal corrupt dependencies.
Publish the Runtime-built A snapshot through existing CAS snapshot machinery, in the admission transaction.
Retain original spec/key across restart; exact replay returns original admission after current authority
checks, before head-dependent freezing; changed selector/body under that key refuses with existing 409.

## Response and errors

Keep HTTP 201 `{data: Task, receipt: CommittedMutation}`; service retains its existing task/run envelope.
Task `spec.spec.inputs.timeline_authority` binds verified `project_id`, `timeline_id`,
`parent_revision_id`, `parent_content_digest`, NEW `publication_id`, dependency/input/snapshot digests.
Existing `timeline_snapshot_ref` binds A's revision/digest/project/timeline and `source_kind: revision`;
exact input object order includes verified A dependencies then snapshot digest. One task/run/receipt.
Use existing errors: 422 `validation_error` for malformed selector; 409 `conflict` details
`{reason: render_revision_mismatch, field: <selector field>}` for any scoped tuple mismatch,
including unavailable scoped revision/publication (no foreign identity disclosure).
Missing/corrupt retained inputs: 409 `conflict`, details `{reason: render_revision_integrity,
dependency_id: <selected dependency>}`; missing/corrupt closure uses selected revision as dependency_id.
Existing authentication, project membership, archived timeline, readiness and idempotency errors stay.

## Compatibility and coupled handoff

Open task spec objects currently accept/IGNORE unknown params: old Runtime silently freezes C when
given this proposed selector. Never deploy a caller relying on it against an old Runtime.
Publish explicit handshake feature support plus coordinated Runtime/client contract version before use;
Agent/App require support and verify returned A tuple or keep the pending intent visibly blocked.
After owner approval, define selector/authority schemas, OpenAPI/conformance fixtures and regenerate
Python/TypeScript clients/manifests with normal generators/release flow; no hand edits or new endpoint.
Agent's authorized coordinator persists A receipt + exact render spec/key before clearing commit flight;
Viewing consumes Runtime snapshot/object bindings. Renderer scopes never gain edit/task authority.
Permanent tests: `tests/test_render_historical_admission.py` uses real Agent commits, host storage,
restart, first admission, authenticated door, five tuple mismatches and corrupt media, with zero-write
checks. Success assertions remain RED without skips/xfails; current C is a passing byte-exact control.
D13/old publication 410 remains HELD pending approval and the separate producer-fence/replay journeys.
