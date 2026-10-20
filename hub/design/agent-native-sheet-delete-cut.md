# AG03 / Gate 1 — bounded native sheet clip-row deletion

Status: in progress, exact parent-clip omission slice only.

## Decision

`NativeSheet.preview` treats omission of a bound `parent/clip:<id>` row as one
existing `capture_clip_delete` command. The row's `# ref` is the only target
binding. The command is captured against the retained export bundle and is
then sent through the existing `TimelineSession.commit_many` / outbox path.

No operation, schema, DTO, API route, second writer, or client-side three-way
merge was added.

## Boundaries

- Added parent clip omission only; omitted track rows, occurrence-owned rows,
  additions, rebinding, row edits that alter the grammar, and changed basis
  remain visible refusals before queueing.
- Deletion uses the native executor, so source/opaque fields on the addressed
  row are consumed by the recorded write, sibling rows and collection order
  remain intact, and normal inverse/rebase/selection guards apply.
- The legacy detached `apply_sheet` / `_apply_parsed` omission consumer remains
  in place, including its existing positive tests. It must be identified as a
  remaining consumer before any duplicate legacy deletion branch is removed.
- Native `clip.delete` is intentionally parent-only. Occurrence/group/legacy
  shot ownership is not inferred from display name or row position and remains
  outside this slice.

## Evidence

Focused SDK and CLI tests cover exact target deletion, opaque/sibling/order
preservation, lost-ack immutable retry without refetch, guarded undo and
command-level redo, disjoint row rebase, membership conflict with no accepted
write, and the actual native CLI entrypoint. The local targeted neighborhood
passed 120 tests. Runtime HTTP integration was not run locally; it is queued
through the central test service separately. The central Agent targeted request
completed with 9 integration tests deselected (exit 5), and no available named
Agent lane runs these exact native-sheet HTTP files, so HTTP remains unverified.
