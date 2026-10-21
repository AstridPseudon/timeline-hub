# Agent source proposal: occurrence child deletion

Date: 2026-10-21 UTC

Status: dormant source proposal for Runtime and App acknowledgement. No App or
sheet caller was changed, no live caller changed, and PRIVATE017 remains
untouched.

## Closed shape

The existing "clip.delete" operation keeps its parent form as version 1:

    {
      "schema_version": 1,
      "op": "clip.delete",
      "version": "1",
      "select": "parent/clip:<raw>",
      "args": {},
      "intent": {}
    }

The one new dormant branch is version 2 of that same operation:

    {
      "schema_version": 1,
      "op": "clip.delete",
      "version": "2",
      "select": "occurrence:<raw>/clip:<raw>",
      "args": {},
      "intent": {"ownership": "occurrence"}
    }

The selector is the ownership declaration. Both identifiers are raw,
non-empty, and cannot contain "/" or "::". There is no new operation family,
argument alias, DTO, store, public export, or caller registration. The
existing operation entry remains the only registration.

## Source semantics

The v2 handler checks exclusive source ownership before any recorded read or
write. It rejects a source used by another occurrence with
"unsupported_ownership", atomically. It then records the complete occurrence
root, its source shot identity, the complete child collection selection
(membership and order), the complete selected child row, and the occurrence
internal source. It binds both the owner and target, and clears only the
selected child root.

The occurrence root, remaining child rows and order, child tracks, source
shot, materialized source linkage, registry/media bytes, and sibling
occurrences are not written. Opaque values, explicit nulls, and absent fields
are carried in the selected row's recorded before-state and are restored by
the normal guarded inverse. The existing materialization capture set includes
this operation so a source-bound v2 record retains the existing exact
allocation facts when a materialized source is present.

Parent "clip.delete@1", whole "occurrence.delete@1", and their existing
fixtures remain unchanged. Unsupported nested or legacy ownership remains
refused by the parent branch.

## Schema and stripping floor

The source schema adds one anyOf branch under the existing "clip.delete"
dispatch: v1 keeps the old empty ClipDeleteArgs and empty intent; v2 uses
the same empty ClipDeleteArgs, the explicit occurrence-child selector, and
the fixed occurrence intent. No generated Runtime schema or pin is claimed.

The source floor is the existing authored-bundle codec: the handler consumes
the raw child row and source collection directly, while document compilation
and JSON reload remain the compile boundary. The direct proof compiles the
deleted bundle, JSON-reloads it, undoes and redoes through the accepted
recorded boundaries, and checks the source document with existing
source-bundle recovery. This preserves opaque values, null, absence,
surviving child order, and the untouched sibling occurrence without adding a
fixture.

## Proof and limits

Added direct behavior proof covers:

- one occurrence child deletion with compile, JSON reload, exact inverse and
  redo;
- first surviving child, middle deletion, and sibling occurrence retention;
- changed child and changed collection order guard conflicts;
- shared-source zero-write refusal;
- schema closure through the existing operation.

The only changed live caller count is NONE. Runtime/App ACK, generated
schema/client proof, native or HTTP qualification, install, renderer, browser,
and full-suite evidence are intentionally not claimed.
