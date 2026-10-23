# R2r/P1 independent review

**Runtime supported public handoff: PASS. Mounted normal App caller: FAIL.**

Runtime’s authenticated public endpoint already returns the exact pair:

```text
GET /v1/projects/{project_id}/timelines/{timeline_id}
get_project_timeline / getProjectTimeline
authorization: projects:read
```

Evidence:

- Route/auth: `runtime_protocol/server.py:539-544`
- Service projection: `runtime_protocol/service.py:2319-2329`
- Pair projection from one `parent_composition_heads` row: `runtime_protocol/timeline_catalog.py:12-25`
- Required schema fields: `contract/schemas/timeline.json:6-12`
- Python generated GET: `generators/python_client_template.py:999-1000`
- TS generated GET: App `cffa91c93…/src/integrations/runtime/generated.ts:183`
- App wrapper passthrough: `client.ts:667-669`

History is also pair-bearing:

```text
GET /v1/projects/{project_id}/timelines/{timeline_id}/commits
envelope: {items, next_cursor, head: {revision_id, publication_id}}
```

- Route/auth: `runtime_protocol/server.py:545-555`
- Fixed-head service binding: `runtime_protocol/service.py:2522-2549`
- Python client validation: `generators/python_client_template.py:967-973`
- TS client/wrapper passthrough: App `generated.ts:206`, `client.ts:696-703`

Independent authenticated daemon witness:

```text
legacy_null= {'head_revision_id': 'parent-1', 'head_publication_id': None}
verified_get= {
  'project_id': 'bd8fc963527149fab108866133951b7c',
  'timeline_id': 'main',
  'head_revision_id': 'parent-1',
  'head_publication_id': 'txn-bbfd3f02b0164e60a20d7aac2ebc1a1c'
}
history_head= {
  'publication_id': 'txn-bbfd3f02b0164e60a20d7aac2ebc1a1c',
  'revision_id': 'parent-1'
}
moved_get= {
  'revision_id': 'candidate-pair-witness-move',
  'publication_id': 'txn-cd45f84eb43a4af2ba4c042ca5268788'
}
captured_pair= {
  'revision_id': 'parent-1',
  'publication_id': 'txn-bbfd3f02b0164e60a20d7aac2ebc1a1c'
}
no_match_control= REFUSE stale inspected revision: public pair moved
client_envelope= preserved
accepted_move= candidate-pair-witness-move
```

The initial null publication is expected for the unverified legacy head. The verified public GET and history return the same pair. A later head move does not match the captured pair and correctly refuses.

## App gap

Frozen App commit `cffa91c93e80717cec1a4e740fae67140394eb88` already uses the pair-bearing GET in `restoreHistory` (`dataProvider.ts:239-255`), but normal `loadTimeline` does not:

```text
loadTimeline
  -> readTimeline
  -> inspectCanonicalTimelineHead
  -> inspection lacks head_publication_id
  -> App normalizes it to null
  -> timelineLocalSaveHandoff.checkHead refuses
```

Evidence:

- `loadTimeline`/read path: `dataProvider.ts:945-946, 1391-1399`
- Inspection request: `dataProvider.ts:563-569`
- Inspection schema has no publication field: frozen `timeline-inspection-result.json:7-14,35-42`
- Inspection producer emits revision only: `runtime_protocol/timeline_inspection.py:755-765`
- Null publication handling: `dataProvider.ts:1401-1407, 1438-1445`
- Fail-closed save check: `timelineLocalSaveHandoff.ts:53-59,92-106`

The App owner should mount the existing pair-bearing GET or fixed-head history into the displayed original basis, requiring project/timeline identity and exact revision equality. On mismatch, retry or refuse. Never attach the latest publication to another inspected revision. If the head moves after capture, retain the captured pair for outbox/CAS and let Runtime CAS handle the conflict.

No Runtime producer/schema/new tuple is required.

Existing request/reply wire shapes were untouched, including all requested request fields (`api_version`, scope IDs, base pair, commands, labels, steps, merge/read/dry-run/source/rationale/group/idempotency) and reply fields (accepted/merged/historical-rebased data, receipts, documents, heads, revisions, digests, records, effects, bindings, dependencies, history, undo steps, conflict/invalid details, and preview semantics). This review only re-qualified the public read envelope.

## Tests

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. /home/user/work/venv-runtime/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/test_timeline_commit_read_basis.py::test_generated_python_client_lists_commits_over_real_http tests/test_timeline_commit_read_basis.py::test_foreign_scope_and_consumer_reads_do_not_write_or_invoke_provider
```

Result: **2 passed in 1.77s**

Import origins:

```text
/home/user/work/wt/rt-R2r-head-pair-review-0637/packages/python/astrid_runtime_client/__init__.py
/home/user/work/wt/rt-R2r-head-pair-review-0637/runtime_protocol/__init__.py
/home/user/work/wt/rt-R2r-head-pair-review-0637/tests/baseline_fixture.py
```

`git diff --check` passed. No product/test/schema/generated/pin/manifest changes were made. No full/browser/native/crash/R5/original-P1 suite was run.

Artifacts:

- [report.md](/home/user/work/wt/rt-R2r-head-pair-review-0637/report.md)
- Commit message written to the required `commit-msg` path.
- Empty `DONE` marker created.