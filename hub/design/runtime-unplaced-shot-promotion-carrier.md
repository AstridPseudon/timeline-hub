# RT02 unplaced project-shot promotion carrier review

Status: **PROPOSED, NOT FROZEN**. This is a review result, not a product or
contract change.

## Decision

No existing authorized acceptance/projection carrier can safely represent
promotion of an **unplaced** project-shot head.

The smallest existing data owner is the project-scoped catalog (`project_shots`
and `shot_items`, with project ownership and a mutable version). That owner is
not the accepted film/timeline document. Runtime's current integration has
retired the catalog's direct shot writers, and the normal Agent provider has no
recorded operation for this mutation. Therefore RT02 needs an explicit,
bounded Runtime/Agent cross-contract decision before any native operation is
frozen or generated:

1. Preserve candidate promotion as a project-catalog mutation, outside the
   accepted film edit path, with its existing project owner, exact candidate
   and superseded item identities, candidate provenance/CAS digest checks,
   version CAS, atomic status transition, transitive invalidation result, and
   durable exact retry receipt; or
2. Explicitly retire the old unplaced-candidate behavior.

Recommendation: choose (1) only if the owners agree that a project-catalog
mutation is an authorized non-timeline seam. Do not encode it as a
`CanonicalDocument` edit, do not attach it to an arbitrary timeline, and do
not silently allow an orphan shot. Until that agreement exists, keep the
original positive behavior tests strict xfail with the RT02 requirement named.

## Evidence and source IDs

- Settled plan: `PLAN.md`, sections 2.4, 3, 4.1, plus the 2026-10-20
  project-reference-catalog and C4 decisions. The plan keeps project-scoped
  catalog infrastructure outside timeline state; film placement/selection is
  an explicit guarded edit; historical reuse must not repoint a newer global
  shot head.
- Runtime current tree `7f6dd892`:
  - `runtime_protocol/service.py:3138-3147` routes project-shot create/update,
    item, reorder, and promotion writes to `_refuse_direct_shot_write`.
  - `runtime_protocol/store.py:1498-1499` makes
    `RealmStore.promote_shot_items` fail closed.
  - `runtime_protocol/timeline_commit_port.py:250-265` makes `shot_closure`
    a read-only exact declared/pinned read; an undeclared shot is refused.
  - `runtime_protocol/timeline_commit_port.py:391-396` rechecks every
    captured shot closure against the immutable store value before acceptance.
  - `runtime_protocol/timeline_commit_store.py:357-388` requires a shot
    revision to be reachable from an accepted parent occurrence and derives
    its media/documents from that parent closure.
  - `runtime_protocol/timeline_commit_store.py:479-494` rejects an
    incomplete or extraneous shot closure: its shot set must equal the
    parent's occurrence shot set.
- Agent current tree `04c24768`:
  - `astrid/sdk/timeline/commands.py:29-72` registers 20 native operations;
    there is no candidate-promotion operation.
  - The direct operation inventory probe reports
    `candidate-promotion=unexpressible`.
  - `astrid/sdk/timeline/_shot_commands.py:12-41` only edits an explicit
    `occurrence:<id>/shot` name/settings projection.
  - `astrid/sdk/timeline/commit.py:730-738` builds the normal saved provider
    projection by visiting parent occurrences and retaining only their shot
    and internal revisions. This is the exact normal-provider blocker for an
    unplaced shot.
- Main archive commit `29d0954b6d78a7d7937d81bc36567b6dee7ca976`:
  - `runtime_protocol/service.py:3644-3751` verifies project/shot/candidate
    identity, candidate provenance, project-owned media and CAS bytes;
    atomically changes primary/candidate state; records a legacy shot
    revision; and returns the invalidation report through the durable receipt.
  - `runtime_protocol/store.py:1479-1492` performs the old atomic item
    metadata + project-shot-version update.
  - `packages/python/astrid_runtime_client/generated.py:979-983` carries the
    old generated-client request shape.

## Why the proposed Agent carrier is not sufficient for an unplaced head

An occurrence-owned `shot.promote-candidate` command could preserve a placed
occurrence's authored projection only if its source shot and all dependencies
were already part of the accepted closure. It cannot authorize a project-shot
head that has no occurrence in the selected timeline:

- `CanonicalDocument` contains the parent plus occurrence-reachable shot and
  internal images; it has no project-catalog head or shot-item collection.
- `shot_closure` is an immutable read, not a writer, and refuses an exact shot
  pin unless it is declared or already pinned by a closure.
- Adding an unplaced shot to the document would violate the complete-closure
  equality check, or would invent a parent/root/timeline ownership relation.
- Reusing a historical occurrence closure would be unsafe: C4 explicitly
  preserves the newer project-global head rather than repointing it.

`media_relations` and immutable media selection can prove source bytes and
dependencies, but neither is a carrier for mutable shot-item status or the
project-shot version. They must remain supporting evidence, not a substitute
catalog journal.

## Main witness

The exact two original positive flows were replayed against a private archive
of Main commit `29d0954b6d78a7d7937d81bc36567b6dee7ca976`, using that archive's
own generated Python `WorkspaceClient` and its documented injectable transport
against the archived `RuntimeService` (no product source or shared dependency
was changed):

- `main-generated-client-positive=PASS`: primary/candidate status transition,
  superseded item identity, and atomic project-shot update.
- `main-generated-client-replay=PASS`: exact idempotent replay.
- `main-generated-client-invalidation=PASS`: plate, proxy, and timeline asset
  fixed-point invalidation.
- `main-generated-client-provenance-negative=PASS`: foreign project
  provenance refused with unchanged shot version.

The unmodified original HTTP test file was also attempted directly from the
private archive, but the worker sandbox rejects socket creation with
`PermissionError: [Errno 1] Operation not permitted`; the generated-client
in-process witness above is the bounded no-socket replacement.

## Current Runtime evidence

Central targeted lane (socket-capable test service):

```text
request-test rt-m2-unplaced-shot-promotion-carrier targeted --files "tests/test_shot_candidate_promotion.py tests/test_timeline_shot_authority.py"
```

Result: **131 passed, 2 strict xfailed, exit 0**. The two xfails are exactly
the original promotion positives, with reason that the retired endpoint is
held until recorded-command candidate promotion exists. All shot-authority
neighbors passed.

No full suite was requested. No Runtime/Agent product code, endpoint, DTO,
schema, public pin, fallback writer, SQL history path, or generated client was
changed by this review.
