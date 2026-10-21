# Runtime source ACK — WC8 future occurrence trim/delete carrier

## Verdict

**SOURCE ACK** for Agent source `d9d3d7f4885fff515c251cad50475dc10f69f4e5`, tree
`697d985139bdb015a22a15c2ea93a54cf5262e06`, covering the reviewed occurrence
trim `9c35f4a...` and child-delete `d2be6511...` composition. The independent
Agent approval and the named shared review were reused; no new Runtime port,
field, DTO, endpoint, store, registration, caller, pin, release, or activation
change is needed.

The source-only activation hold remains unchanged. This ACK is semantic carrier
fit only; it does not qualify a live caller or native/HTTP path.

## Carrier fit

- **Media.** The composed trim reads the existing verified media descriptor and
  uses its intrinsic video duration; it does not add a media argument or new
  media identity. Runtime ABI 1 already carries the exact five-field
  `MediaSelection` (`contract/schemas/edit-command.json:1912-1940`). The
  request port captures declared selections through `selected_media()` and
  re-reads them during validation (`runtime_protocol/timeline_commit_port.py:268-275,`
  `421-424`). Its existing managed generation/variant/object, MIME, size,
  intrinsic-duration, catalog-digest, and CAS checks are in
  `runtime_protocol/timeline_commit_port.py:788-887`. Child delete changes no
  media identity, so the existing closure manifest checks remain sufficient.

- **Source and owner.** Agent trim uses the existing occurrence `_owner` and
  `_exclusive` guards, then records `trim.source` as an ordinary `entity`
  dependency and binds `trim.target`; child delete checks exclusivity first,
  reads the occurrence, source shot, target child, and scoped source, then
  binds owner/target and clears only the child (`d9d3d7f...:astrid/sdk/timeline/`
  `_trim_commands.py:181-267`, `_delete_commands.py:56-85`). Runtime already
  accepts entity dependencies with finite JSON pins and generic bindings,
  reads, and writes (`runtime_protocol/schemas/timeline-commit-bundle.json:`
  `3572-3636`; `contract/schemas/edit-command.json:57-69,362-398`). The existing
  canonical closure still authenticates each occurrence's project, shot, and
  shot-revision linkage (`runtime_protocol/timeline_commit_baseline.py:157-185`;
  `runtime_protocol/timeline_commit_store.py:533-547`).

- **Order and retention.** The child delete's `collection.clips` selection
  records membership/order in the existing `AgentSelection`; no positional or
  new order carrier is required. Runtime already enforces occurrence row order,
  complete closure membership, sorted shot/internal/media manifests, and exact
  dependency-row ordinals (`runtime_protocol/timeline_commit_baseline.py:157-218`;
  `runtime_protocol/timeline_commit_store.py:444-467,549-589`). Accepted
  `CommandRecord`s, including reads, selections, bindings, dependencies, and
  writes, are retained verbatim in `timeline_commit_history.records_json`
  (`runtime_protocol/timeline_commit_store.py:1083-1108`) and replay integrity
  checks compare the stored command sequence and records (`runtime_protocol/`
  `timeline_commit_store.py:130-189`).

- **`id_map`.** Neither reviewed operation creates an ID: trim writes only the
  existing child `from`/`to`/`hold` (and its existing intent cleanup), while
  delete clears the selected child root. The composition leaves the frozen
  thirteen-operation `SOURCE_BOUND_OPERATIONS` set intact and adds only the
  separate `clip.delete` v2 source-bound addition (`d9d3d7f...:astrid/sdk/`
  `timeline/_materialization.py:8-18`). The existing Runtime `id_map` envelope
  is an open string-to-ID map (`runtime_protocol/schemas/timeline-commit-bundle.json:`
  `3505-3525`); for materialized source edits, `materialization_join` already
  validates the authenticated source/item map and exact `id_map`
  (`runtime_protocol/timeline_materialization.py:100-182`). No new mapping or
  retention table is implied.

- **Transaction guards.** Runtime's existing acceptance transaction performs
  authorization, replay lookup, head/context checks, closure/destination
  checks, provider validation, persistence, publication, and input persistence
  as one transaction (`runtime_protocol/timeline_commit_store.py:888-939`).
  The store's `BEGIN IMMEDIATE`/savepoint wrapper rolls back the whole mutation
  on failure (`runtime_protocol/store.py:841-866`), while the execution
  coordinator preserves exact-request idempotency and rechecks the durable
  result around provider execution (`runtime_protocol/timeline_commit_execution.py:`
  `69-115`). The reviewed owner/source/order/ABA/inverse claims therefore fit
  the existing guarded record path; no new transaction guard is inferred.

## Public schema boundary

The current public014 Runtime projection still has only v1 dispatch for
`clip.delete` and `clip.trim` (the installed schema is the frozen
`6ba7b51e...` artifact; `contract/schemas/edit-command.json:929-955,1487-1514`).
The future source's absence there is the expected unpublished generation
dependency called out by the request, not a semantic carrier mismatch. No
schema generation or public014 mutation was performed.

## Verification

No tests were run. The brief explicitly prohibited running old selectors or any
test body and requested a source-only carrier review. No source files, schemas,
generated clients, pins, callers, or activation state were changed.
