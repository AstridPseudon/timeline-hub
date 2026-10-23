# Runtime handoff: G5 source authority

**Disposition: FAIL for current cross-timeline source-copy support.**

Current Runtime supports:

- complete `revision_closure(revision_id)` only in the authenticated request's
  `(project_id, timeline_id)` scope;
- exact declared `shot_closure(shot_id, revision_id)`, which can resolve a
  child from another timeline but returns only the shot/internal/media/document
  closure;
- exact project-scoped transcript/config document pins and exact Runtime media
  selections/raw-media pins, all rechecked before acceptance;
- durable destination request hash/idempotency/head CAS, provider-record
  authentication, destination closure validation, identity reservations and
  atomic persistence.

Exact source:

- `runtime_protocol/timeline_commit_provider.py:34-59`: fixed provider ABI;
- `runtime_protocol/timeline_commit_port.py:223-296`: same-timeline revision,
  exact shot and media handback;
- `runtime_protocol/timeline_commit_port.py:316-465`: source document capture
  and request-private recheck;
- `runtime_protocol/timeline_commit_store.py:446-485,541-572`: complete
  same-scope closure and narrower child closure;
- `runtime_protocol/timeline_commit_store.py:743-814,839-1000,1070-1130`:
  closure, media/materialization, destination identity and acceptance guards;
- `runtime_protocol/service.py:1697-1742,2435-2510` and
  `runtime_protocol/server.py:294-319`: empty timeline bootstrap and the
  authenticated destination-scoped commit route;
- `packages/python/astrid_runtime_client/generated.py:846-856,963-965`:
  current generated create/commit client shapes.

Missing seam: no current registered source timeline selector/full source
closure import for an empty destination, and no current registered operation
for a fresh occurrence to attach to an existing shot created earlier in the
same duplicate. The current Agent G5 draft's known failures and R4 historical
source-copy code do not establish current support. See the detailed worker
report at
`workers/rt-G5-source-authority-0822/report.md`.

Bounded owner proposal: after an explicit contract decision, Runtime owns one
authenticated source-closure duplication semantic carrier, including exact
source revision/publication verification, full closure/media/document admission,
fresh destination identity allocation, repeated-shot sharing authorization and
negative controls. Agent owns only the caller mapping and canonical-state
consumption. No implementation was made here.

Evidence: the required authentication negative test passed 28 cases; `git diff
--check` passed; no full or known duplicate suite was run.
