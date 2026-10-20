# Agent review of Runtime private392 counterpart

Date: 2026-10-20

## Decision

**APPROVE — bounded cross-area source/contract/security review.**

This approves Runtime commit `f8da4b6d46b0ec5ebeb7a42be47c5bf3438c5414`,
tree `8be43e13acb436120f8a63b1a178d64c49422461`, as the corrected private392
counterpart for the reciprocal review. It does not approve a normal Agent pin,
native392 qualification, public adoption, activation, release, or integration.

## Exact identities and inventory

- Runtime commit: `f8da4b6d46b0ec5ebeb7a42be47c5bf3438c5414`
- Runtime tree: `8be43e13acb436120f8a63b1a178d64c49422461`
- Runtime parent/base: `f0268d2b817de8b2d9917a1395b272e5f4c8ddbb`, tree
  `c24c0a5c06bb83622a038ec99a30401ca68eca0f`
- Agent source: `e010e6a3868e963471244491bb6672c3e4a5135e`, tree
  `70414cf6875d2c97c45f33e0a5158c80bd7391d9`
- Agent/Runtimeschema SHA-256:
  `39211e63a50b9fb495fdf3feb5beaf0e4d0b4eab9a7e13f4d5f769e0d317429d`

The exact Runtime commit is present in the Runtime object database; no
pending/prospective handoff identity was used. Its parent diff is exactly one
announced 39-line addition to `tests/test_timeline_clip_replacement.py`.
The corrected source-bound helper, port, and store are therefore present in
the committed parent and were not replaced by the incomplete e63 schema-only
candidate. Their committed blob hashes are:

```text
runtime_protocol/timeline_materialization.py  92ec9b7f105d5e0fd1c5f9e9f2a4602ee3dd005365a570e7ba91a573bb8b31fb
runtime_protocol/timeline_commit_port.py       00ecf62412b3e1a1339794d8229e048521cebb6f26ca3eca24d6e0517a2f3767
runtime_protocol/timeline_commit_store.py      c06fdc3d4d1ee0e2f1cdc00a41f6c094fe4c7ffbc649810d7c289ea88954862a
```

The real current integration `a020a1c77a07aa657efb60b0442450209e55e470`
versus `f026` has exactly the tuple's 24 changed paths and zero paths outside
the announced allowlist. Every current test function in those changed test
files is present in the committed candidate; the RT02 test file is byte-
identical to a020. The candidate itself has no non-test delta from f026.

## Contract and artifact checks

- Runtime artifact manifest contains **75 paths**; all 75 exist in the
  committed tree and match their declared hashes.
- Raw Runtime bundle:
  `sha256:fa7717e25c95126b18bb6f37b4c2d813d4a815456a06d438d52ef41c2cf1eab3`
- Runtime health/schema digest:
  `sha256:242d2bc193bf16b699eb87592736769aacd8fdb75a1bb859dff3255d83ea5042`
- Artifact manifest version:
  `sha256:52df520b8384c70dc10d0b15bdce00e758c153019d26ddb9e141f5840885ba2d`
- Contract metadata remains `0.2.13`; no new Runtime DTO, endpoint, table,
  schema version, pin, or generated artifact was introduced by f8da.
- The committed Agent schema and Runtime generated schema are byte-identical,
  with 56 `$defs`, the 30-operation inventory, and 12 explicit v2 operation
  branches: `track.set`, `shot.set`, `clip.set-params`, `clip.set-element`,
  `clip.move`, `occurrence.add-media`, `occurrence.swap-media`,
  `placement.move`, `placement.create`, `placement.unplace`, `shot.pool`,
  and `clip.set`.
- `ProjectDataWriteArgs` is present in the generated Runtime package root and
  is the closed Agent operation shape. Runtime carries the exact schema and
  does not create a second project-data authority or alter the Agent's
  original guards.

The private952/private613/ordinary-a0/public013 carrier bytes remain in the
current parent/source composition; f8da changes no carrier or artifact file.

## Source/security review

The exact committed source preserves the required custody boundaries:

1. `timeline_materialization.py:39-183` is a read-only provenance join. It
   authenticates project/timeline scope, parent and source content digests,
   source shot/internal revision closure, occurrence ownership, exact item
   maps, and the sealed source/owner bindings. It rejects derived destinations
   that appear in `created`, rejects duplicate occurrence owners and reused raw
   item identities within the request, and requires the prepared `id_map` to
   equal the authenticated source-bound mapping. It returns allocations; it
   does not grant write authority or perform allocation.

2. `timeline_commit_port.py:436-455` requires a private
   `RequestCommitPort`, exact request-context equality, and the command's
   sealed bindings at the matching ordinal. Source closure and media/text
   captures are re-read and compared before acceptance
   (`timeline_commit_port.py:387-434`). Thus a caller cannot supply an
   allocation map or source proof as authority; the installed Agent provider
   must produce the sealed, captured record.

3. `timeline_commit_store.py:662-850` keeps creation separate from
   materialization. Native `created` claims are validated against the frozen
   records and checked against project/global shot and item occupancy. Derived
   allocations are not converted into native birth claims. Current slot/head
   ownership, inverse restoration, retained history, C4/global-item
   reservations, and authenticated prior receipts are checked before mutable
   projection writes.

4. Retry safety is ledger-first. `timeline_commit_store.py:116-189` checks the
   exact idempotency row and request hash, authenticates its history/event
   record, and validates source-bound records on replay. The acceptance
   transaction invokes that lookup before head, destination, closure, or
   persistence checks (`timeline_commit_store.py:888-917`). A changed payload
   under the same key is refused; an exact retry returns the stored receipt.

5. Current safeguards remain in the parent carrier: history/publication
   ancestry and catalog-tail verification (`timeline_commit_store.py:227-260`,
   `runtime_protocol/timeline_catalog.py:28-98`), no overwritten newer catalog
   head, project-scoped revision/shot closure and CAS digest checks
   (`timeline_commit_store.py:473-589`), exact managed media/catalog/CAS
   checks (`timeline_commit_port.py:757-856`), and retained text ownership,
   size, MIME, UTF-8, and byte checks (`timeline_commit_port.py:607-652`).
   The committed RT02 test additionally preserves native shot replacement,
   restart, and exact retry behavior.

These checks cover the rejected e63 gap: the corrected counterpart contains
the authenticated source-bound allocation join and its port/store integration,
while retaining the current history, catalog, CAS, headless, text, C4, global
item, and RT02 protections.

## Evidence and limits

Read-only evidence used here:

- exact `git show`/`git diff` of the committed Runtime and Agent objects;
- 75-path manifest/hash verification;
- schema byte identity and 56/30/12 inventory checks;
- 24-path current-base allowlist check and test-function retention check;
- direct source inspection of the materialization, port, store, catalog, CAS,
  text, and RT02 paths;
- existing recorded Runtime evidence for the 319/199/246/43 lanes and the
  prior source-freeze/counterpart reports.

No Runtime suite, full suite, localhost/browser lane, native392 pair, pin,
generation, release, or adoption operation was run for this review. The
recorded 319/199/246/43 evidence remains the test evidence for those lanes;
this review adds no duplicate comprehensive run.

Next step is the orchestrator's reciprocal Agent review. Only after both
reviews approve may the normal private Agent pin and one matched native392
pair be prepared.
