# Runtime private392 final review

**Decision: APPROVE.** This is an independent source/contract approval of the
final committed private candidate for reciprocal review and later matched
private pin/native392 preparation. It is not public adoption, activation,
release, or native392 qualification.

## Exact candidate

- Commit: `f8da4b6d46b0ec5ebeb7a42be47c5bf3438c5414`
- Tree: `8be43e13acb436120f8a63b1a178d64c49422461`
- Parent/base: `f0268d2b817de8b2d9917a1395b272e5f4c8ddbb`
- Delta from f026: one file only, `tests/test_timeline_clip_replacement.py`,
  carrying the exact current `a020a1c` RT02 test addition (39 lines).
- Current a020 test file and final candidate test file are byte-identical.

The tuple and the f026 current-join report/log were read as the controlling
source and evidence records. The final candidate has no source, guard,
schema, generator, generated-client, artifact, or type delta beyond the
approved test forward.

## Contract and byte checks

- Current a020 versus f026 outside the 24-path allowlist: **0 mismatches**;
  no current test assertions are missing.
- Candidate artifact manifest: **75 paths**, all present, all declared hashes
  valid, and all byte-identical to e63. Manifest file SHA-256:
  `1c684f53582a44b12a7438b79ddeace8696768b4fb98f8f704d58a640fa6cd5f`.
- Agent e010 source was streamed directly from the frozen Agent checkout and
  is byte-identical to the candidate schema:
  `sha256:39211e63a50b9fb495fdf3feb5beaf0e4d0b4eab9a7e13f4d5f769e0d317429d`.
- The generated schema has 56 definitions, 30 operation clauses, and 12
  explicit v2 operation branches:
  `track.set`, `shot.set`, `clip.set-params`, `clip.set-element`, `clip.move`,
  `occurrence.add-media`, `occurrence.swap-media`, `placement.move`,
  `placement.create`, `placement.unplace`, `shot.pool`, and `clip.set`.
- `ProjectDataWriteArgs` is present in the generated Python package root and
  `__all__`; the generated Python and TypeScript command types contain the
  closed `project-data.write` argument shape.
- Removing only `ProjectDataWriteArgs` and the `project-data.write` operation
  clause from the candidate reproduces frozen private613 exactly:
  `sha256:613123b2760150f9f33e23485516d757359c3eaebfe02d552bc97155309aaad3`.
- From that result, removing the 12 v2 alternatives, the three additive
  item-reference alternatives (`ScopedId`, `EntityRef`, `TargetKey`), and the
  item form from `AnchorIdentity` reproduces ordinary6ba exactly:
  `sha256:6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`.
- Raw bundle SHA-256:
  `fa7717e25c95126b18bb6f37b4c2d813d4a815456a06d438d52ef41c2cf1eab3`.
- Runtime health/schema digest:
  `sha256:242d2bc193bf16b699eb87592736769aacd8fdb75a1bb859dff3255d83ea5042`.
- Artifact version digest:
  `sha256:52df520b8384c70dc10d0b15bdce00e758c153019d26ddb9e141f5840885ba2d`.

## Guard/source review

The f026 carrier remains unchanged in the final candidate. Read-only inspection
and the existing recorded 319/199/246/43 evidence support these boundaries:

- Acceptance performs the exact idempotency-ledger lookup before provider
  validation, and a matching retry returns the stored receipt; a changed
  request hash refuses. The source-bound v2 path is not an identity-only
  blanket admission.
- Retired unsafe private-v1/public legacy writers refuse before replay lookup
  and before writes. The current source-bound v2 path has the corresponding
  positive coverage, including the later RT02 restart/exact-retry test.
- Materialization proves scoped parent/source closure, occurrence owner,
  item membership, stable bindings, and inverse provenance. It does not grant
  caller authority or write mutable rows by itself.
- Existing owner admission, C4/global-item occupancy and reservation checks,
  catalog/history verification, CAS byte/digest ownership checks, headless
  overwrite refusal, and text-binding ownership/media checks remain present.

No new caller authority, Runtime request DTO, persistence table, or endpoint
was introduced by the f026 source join. The only new generated argument type
is the approved Agent command-schema `ProjectDataWriteArgs` above; it does not
expand Runtime authorization.

## Evidence and limits

Existing evidence read, not rerun: 319 acceptance/schema checks, 199
join/ownership checks, 246 safety/generated checks, and 43 client checks,
plus the recorded generator/artifact/TypeScript checks and the 3-case central
catalog/occupancy lane. No full suite, install, pin, Git mutation, or 952
native44 rerun was performed for this review. Native392 qualification, the
matched Agent/Runtime pin, and public adoption remain separate gates.
