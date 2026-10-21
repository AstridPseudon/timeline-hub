# Private392 visual-seam carrier review

Date: 2026-10-21 UTC

## Decision

**APPROVE — dormant App source only.** The candidate fits the existing
private392 `project-data.write` carrier at
`parent.config.app.visualSeamContract[key]`. This review does not approve
activation, pinning, generation, adoption, fallback removal, or a native
provider/Door gate.

## Candidate and scope

- Candidate commit: `bce8bab72d03e12d2cbfb055d76a5ea04f474f68`
- Candidate tree: `f9bc16ce6b08c830cac814feee7b20e9d659fd6e`
- Base parent: `780c502368cb6eb379cf3848af7009067c7cd744`
- Exact delta: two added files only:
  - `src/tools/video-editor/commands/visualSeamProjectDataMember.ts`
  - `src/tools/video-editor/commands/visualSeamProjectDataMember.test.ts`
- `useTimelineState`, `useTimelineOps`, the existing project-data member,
  generic dispatch, Runtime types, schema, provider, session, outbox, and
  wire surfaces are untouched.

## Semantic review

The exact e010 Agent source is tree `70414cf6875d2c97c45f33e0a5158c80bd7391d9`
with schema digest
`39211e63a50b9fb495fdf3feb5beaf0e4d0b4eab9a7e13f4d5f769e0d317429d`. Its
closed operation is `project-data.write`, `select: parent`, with exactly
`target`, `key`, `value`, and `mode: replace`; it writes one leaf at
`parent.config.app[target][key]`. The exact Runtime private392 counterpart is
tree `8be43e13acb436120f8a63b1a178d64c49422461` and exposes the same closed
`ProjectDataWriteArgs` shape.

The candidate maps the existing authored seam object as follows:

```text
target = visualSeamContract
key    = each changed top-level authored contract key
value  = acknowledged authored value
mode   = replace
path   = parent.config.app.visualSeamContract[key]
```

Specific safety properties verified:

- `report` is excluded as a derived field. A report-only change returns no
  patch, while an already stored report remains an opaque sibling untouched by
  the native capture.
- Authored key order comes from the acknowledged object and is carried as
  explicit operation order. The existing native member retains that order
  through capture and replay; absent/null namespace births are handled by the
  existing container capture.
- The builder refuses malformed array namespaces and refuses an authored key
  disappearing from the current namespace because the private carrier has no
  delete member. Its object/array guard remains as narrow as the existing App
  seam snapshot guard; it does not broaden accepted values or normalize keys.
- The existing native member, not the dormant builder, supplies stable
  references and the old-presence guard. `MoveRecording` records config/app/
  namespace reads and the requested leaf expectation; `replaceGeneratedClaims`
  preserves the exact prior leaf state for stale-head, same-leaf, inverse, and
  redo checks. The candidate's capture/replay test exercises this unchanged
  carrier.
- Existing capture validates every operation before materializing the local
  result and reports a `ProjectDataMemberRefusal` for the whole patch. The
  retained mixed-batch test proves no partial write. The candidate emits only
  the already-valid `replace` mode; the native member rejects merge or any
  other mode at its closed command boundary.
- No derived report becomes authored data, and no new DTO, field, authority
  path, endpoint, store, or live pin is introduced.

## Evidence

Read-only cross-area evidence:

- Agent e010/392 source and Runtime f8/392 generated operation were inspected
  directly; the source/schema/operation identities above match the prior
  bounded reviews.
- Prior exact evidence remains valid and was not relabeled: App reported
  `16 passed` focused tests and Agent reported `17 passed` in
  `tests/editing_conformance/test_recipe_m2_project_data.py` against the
  private392 source. Those reports also include the exact opaque-report,
  order, absence, inverse, and namespace probes.
- Current App HOME snapshot was `ee6b809e680ab54ded4199ef51d9ab4c8d416835`;
  only pre-existing untracked vendor symlinks were present. No HOME product
  files were changed by this review.

Commands run in this review:

```text
node_modules/.bin/vitest run --config config/testing/vitest.config.ts --no-cache \
  --maxWorkers=1 --no-file-parallelism \
  src/tools/video-editor/commands/visualSeamProjectDataMember.test.ts \
  src/tools/video-editor/commands/projectDataMember.test.ts \
  src/tools/video-editor/hooks/useTimelineState.visual-seam.test.ts
=> 3 files passed, 16 tests passed

node_modules/.bin/eslint \
  src/tools/video-editor/commands/visualSeamProjectDataMember.ts \
  src/tools/video-editor/commands/visualSeamProjectDataMember.test.ts \
  --ext ts --max-warnings 0
=> passed

node_modules/.bin/tsc --noEmit --pretty false
=> passed

git diff --check HEAD^ HEAD
=> passed
```

No product edits, full suite, browser, localhost/live-socket gate, generation,
pin, or Runtime/App native qualification was run. The exact Agent 17-test lane
was inspected from the prior report rather than rerun in this App worktree.

## Recommended next step

Keep this builder unregistered and inert. Wire it only after the exact matched
private392 Agent/Runtime/App lifecycle is qualified; retain the current
snapshot fallback until that separate decision.
