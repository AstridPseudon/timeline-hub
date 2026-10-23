# R2r/P1 independent head-pair handoff review

## Result

**PASS for the supported existing Runtime public handoff; FAIL for the
currently mounted normal App caller.** Runtime already exposes and preserves
an authenticated `(head_revision_id, head_publication_id)` pair. The frozen
App adapter does not mount that read into displayed `loadTimeline`: it uses
inspection, whose public result has no `head_publication_id`, so the adapter
turns it into `null` and `timelineLocalSaveHandoff.checkHead` fail-closes.
This is an App integration gap, not a Runtime producer/schema/tuple defect.

No product, test, generated-client, schema, pin, or manifest files were
changed.

## Existing Runtime public path

The supported authenticated route is:

```text
GET /v1/projects/{project_id}/timelines/{timeline_id}
client methods: get_project_timeline / getProjectTimeline
authorization: projects:read
```

The HTTP handler authorizes `projects:read` and dispatches the route to
`RuntimeService.get_project_timeline` (`runtime_protocol/server.py:539-544` in
this worktree; the frozen 34eac reference has the same route at
`server.py:539-544`). The service validates the project-scoped timeline and
returns `_timeline_public_resource` (`runtime_protocol/service.py:2319-2329`).
The catalog projection reads `revision_id, publication_id` from the same
`parent_composition_heads` row and emits both fields
(`runtime_protocol/timeline_catalog.py:12-25`; frozen 34eac:
`timeline_catalog.py:12-25`). Therefore the public envelope includes, among
the normal timeline fields:

```json
{
  "project_id": "…",
  "timeline_id": "main",
  "head_revision_id": "parent-1",
  "head_publication_id": "txn-…"
}
```

The contract requires the pair, with nullable values for an unverified or
empty head (`contract/schemas/timeline.json:6-12`). The frozen 34eac schema
also requires both fields (`contract/schemas/timeline.json:6-12`).

The other existing pair-bearing read is:

```text
GET /v1/projects/{project_id}/timelines/{timeline_id}/commits
client methods: list_timeline_commits / listTimelineCommits
authorization: projects:read
envelope: {items, next_cursor, head: {revision_id, publication_id}}
```

Its route and authorization are in `runtime_protocol/server.py:545-555`; the
service binds history pages to one fixed head
(`runtime_protocol/service.py:2522-2549`). The generated Python client keeps
the JSON envelope and rejects a missing head object
(`generators/python_client_template.py:967-973`). The TS generated client
returns the JSON response unchanged (`App cffa91c93…/src/integrations/runtime/generated.ts:206`),
and its session wrapper passes the `HistoryPage` through
(`App cffa91c93…/src/integrations/runtime/client.ts:696-703`).
The generated Python `get_project_timeline` is also a direct JSON-preserving
GET (`generators/python_client_template.py:999-1000`; generated copy
`packages/python/astrid_runtime_client/generated.py:999-1000`).

## Independent authenticated witness

I ran a fresh `RuntimeDaemon` witness using the existing authenticated
`WorkspaceClient`, with the legacy baseline first unverified, then installed
through the existing verified-baseline path, then advanced by one accepted
revision. No SQL or App/private route was used for the public reads.

Observed output:

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

This proves the initial null publication is an expected legacy/unverified
condition, not evidence that the public verified handoff lacks a publication.
It also proves the bounded control rejects a public pair that no longer
matches the inspected revision.

The import-origin diagnostic, run with the worktree packages explicitly
visible, resolved to:

```text
astrid_runtime_client = /home/user/work/wt/rt-R2r-head-pair-review-0637/packages/python/astrid_runtime_client/__init__.py
runtime_protocol = /home/user/work/wt/rt-R2r-head-pair-review-0637/runtime_protocol/__init__.py
baseline_fixture = /home/user/work/wt/rt-R2r-head-pair-review-0637/tests/baseline_fixture.py
```

## Mounted App gap

Frozen App commit `cffa91c93e80717cec1a4e740fae67140394eb88` has the pair
source available: generated `getProjectTimeline` makes the public GET
(`src/integrations/runtime/generated.ts:183`), and the session wrapper passes
it through without projection (`src/integrations/runtime/client.ts:667-669`).
`restoreHistory` already uses this pair-bearing GET and requires both IDs
(`src/integrations/runtime/dataProvider.ts:239-255`).

The normal displayed path is different:

1. `loadTimeline` calls `readTimeline`
   (`src/integrations/runtime/dataProvider.ts:945-946, 1391-1399`).
2. `readTimelineInOrder` calls only `inspectCanonicalTimelineHead`, which
   invokes `POST .../inspect` (`dataProvider.ts:563-569`).
3. The inspection checks and reads `head_revision_id`, but the frozen Runtime
   inspection schema requires no `head_publication_id` and defines no such
   property (`candidate-runtime` frozen
   `contract/schemas/timeline-inspection-result.json:7-14,35-42`; producer
   `runtime_protocol/timeline_inspection.py:755-765` emits
   `head_revision_id` at the result construction and no publication field).
4. The App then parses the absent optional publication as null and returns it
   in the displayed record (`dataProvider.ts:1401-1407, 1438-1445`).
5. The save assembly loads the command basis and
   `timelineLocalSaveHandoff.checkHead` requires a non-null exact revision and
   publication match (`src/tools/video-editor/hooks/timelineLocalSaveHandoff.ts:53-59,92-106`).

Thus the current normal path is:

```text
loadTimeline -> inspect only -> missing publication -> null
            -> checkHead refuses original verified save basis
```

The App should mount the existing pair-bearing GET or fixed-head history into
the displayed original basis, requiring project/timeline identity and exact
revision equality before retaining the pair. On mismatch it must retry or
refuse; it must never attach the latest publication to a different inspected
revision. If the head moves after a successful exact capture, retain the
captured pair for outbox/CAS and let the normal Runtime conflict path handle
it; do not reload latest to rewrite a stale displayed source.

Immutable inspection, closure, and history must continue to agree on the same
exact root. No SQL/private route from App, read-import, guessed pin, or
`checkHead` waiver is acceptable.

## Wire-shape preservation

This review made no wire-shape changes. Existing request/reply fields remain
owned by the frozen clients/manifests: request `api_version`, project/timeline
IDs, base revision/publication, commands (semantic and `doc.patch`), label,
steps and their IDs/labels/intents/tags/ordinals/patch/reads, merge mode,
reads, `dry_run`, source, rationale, group and idempotency; replies retain
accepted/merged/historical-rebased complete data, receipt, document/head/
revision/digests, records/effects/bindings/dependencies/history/undo steps,
conflict reason/head, invalid code/path/hint/suggested command, and preview
without a receipt with `would_status` accepted or merged. This audit only
exercised the public read envelope, so those broader commit fields are
reported as untouched rather than re-qualified here.

## Tests and hygiene

Required targeted command:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. /home/user/work/venv-runtime/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/test_timeline_commit_read_basis.py::test_generated_python_client_lists_commits_over_real_http tests/test_timeline_commit_read_basis.py::test_foreign_scope_and_consumer_reads_do_not_write_or_invoke_provider
```

Result: **2 passed in 1.77s**.

The independent daemon witness above also completed successfully. No full,
browser, native, crash, R5, original P1, or other prohibited suite was run.
`git diff --check` passed; worktree status is clean at
`85dafdf46742b02ae5e4a300656cd6f5d68f0d4d` before the required report
artifact; the only current untracked worktree file is this `report.md`.

## Handoff

Runtime supported-path result: **PASS**.

Mounted App caller result: **FAIL**, bounded to the App owner. The next step
is to mount the existing pair-bearing read into the displayed original basis
with exact-match retry/fail-closed behavior, then re-run the App-owned
targeted handoff proof. Do not claim the current mount or P1 end-to-end pass.
