# D105 audit report

Decision: **normative occurrence-prefixed DOM-ID requirement: NOTFOUND.**

C0/C0b/C0c defines physical closure identity, bindings, occurrence addressing, and native entity spelling, but no DOM-ID or selector requirement. Relevant text:

- [`commit-v2.md:287`](/home/user/work/runtime/contract/commit-v2.md:287): closure-root identity is physical, not payload/array-order based.
- [`commit-v2.md:309`](/home/user/work/runtime/contract/commit-v2.md:309): native unambiguous addresses retain spelling and behavior.
- [`commit-v2.md:369`](/home/user/work/runtime/contract/commit-v2.md:369): occurrence rows use occurrence-scoped addresses.
- [`commit-v2.md:378`](/home/user/work/runtime/contract/commit-v2.md:378): native entity address normalization.

The deletion ledger and approved placement decisions document the current occurrence-qualified implementation and its tests, but do not establish a normative DOM requirement:

- [`deletion-ledger.app.md:346`](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/deletion-ledger.app.md:346)
- [`deletion-ledger.app.md:416`](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/deletion-ledger.app.md:416)
- Source-return and whole-path reports document the observed selector failure, not an approved requirement.

## D69 reverse-diff

Exact frozen D69 upstream: `3881e9440688f774878e18806da2dc5c993a9b00`, tree `210e5739b838ef7655f87238c711704301d12846`.

Upstream behavior:

- `timeline-dom.ts` passes the supplied ID unchanged as `data-clip-id`.
- `ClipAction.tsx` passes `action.id` unchanged.
- Frozen upstream `shotCompositionProjection.ts` creates `action.id = "${occurrenceId}:${rawClipId}"`.

Therefore embedded upstream did **not** expose raw `data-clip-id="clip-0"`; it exposed the occurrence-prefixed ID. Raw `clip-0` remained authored child identity. Current App preserves that projection behavior at [`shotCompositionProjection.ts:336-348`](/home/user/work/wt/app-P2-D105-placement-identity-citation-0552/src/tools/video-editor/data/shotCompositionProjection.ts:336).

The current failing raw selector is therefore not a regression against frozen upstream. It is an oracle/legacy-selector mismatch. However, because no approved C0 requirement mandates the prefix, D105’s settled rule directs a product-side compatibility fix, not an oracle merge.

## Correct next owner

**Product owner**, while preserving the origin allocator and internal occurrence identity.

Candidate source-only locus: the `ClipAction`/`timeline-dom.ts` attribute boundary, using the already-projected raw canonical ID only for the justified legacy locator while retaining the occurrence-prefixed `action.id` for internal identity, selection, drag, resize, history, and command targeting.

The owner must audit:

- `ClipAction`, timeline DOM readers, gesture/selection/resize/context-menu callers.
- `data-action-id` and other internal targeting attributes.
- Multiple occurrences sharing the same raw child ID; raw DOM IDs cannot be globally unique.
- Existing wrong-occurrence, sibling, same-asset, reload, undo, and placement selectors.

No predicate was dropped, no arbitrary retarget was made, and no tests were rewritten.

## Verification

- `git show -s --format='%H%n%T%n%s' 3881e944...`: exact frozen upstream confirmed.
- `git status --short --branch && git diff --check`: clean assigned worktree.
- Tests/build/lint/browser suites: **not run**, per the read-only audit brief.

Commit message and `DONE` marker were created.