# Agent private successor: owner-pinned built-in overlay contract

Status: source contract implemented and directly qualified in the Agent
worktree. App D01 remains the remaining consumer/legacy-writer decision; this
handoff does not activate App.

## Smallest carrier

The existing `clip.add` operation keeps its public operation, version, and
Runtime request shape. Its closed `args` object has one new optional field:

```json
"schema_source": {
  "document_id": "<exact admitted document id>",
  "version": 1,
  "content_digest": "sha256:<exact document content digest>"
}
```

This is the existing `DocumentPin` definition already used by
`clip.set-params` and `clip.set-element`; there is no new DTO, endpoint, store,
operation, or browser validator. The field is only authoritative when the row
also carries the exact existing owner-qualified `elementRef`:

```json
{
  "packId": "<exact catalog/admission owner>",
  "kind": "effect",
  "id": "<exact effect id>",
  "revision": "sha256:<full 64-hex revision>"
}
```

With `schema_source`, Agent resolves the retained admitted snapshot for the
full `(packId, kind, id, revision)` tuple, validates known params against that
immutable definition, and preserves unknown JSON exactly. The bounded overlay
recipe additionally requires `row.clipType == elementRef.id` and an active
visual output track. Legacy unpinned `clip.add` remains unchanged.

## Apply / update / remove

App2 should emit the existing native carriers as follows:

1. `clip.add` with one complete parent row, the owner-qualified
   `elementRef`, literal `at`/`hold`, params, opaque siblings, and the exact
   `args.schema_source` pin.
2. `clip.set-params` with literal top-level `values` and `clear`, retaining the
   original element owner/id/kind/revision and carrying the same exact
   `schema_source` pin. Null is a value; `clear` removes presence; unmentioned
   params and row fields survive.
3. `clip.delete` on `parent/clip:<id>` for removal. It already records the
   complete original row and stable membership/order; inverse restores that
   original owner-qualified ref and does not re-resolve a newer catalog row.

The accepted authority-bearing add is now recognized by the existing selected
PARAM history resolver, so a subsequent set/clear can prove its source without
inventing a new selection event. Add records `params.schema` and
`params.snapshot` exact dependencies plus a fixed `params.element` binding.

## Guards proven

The direct Agent proof covers exact row/opaque preservation, null and clear,
set/delete/inverse, disjoint rebase, and atomic refusal before writes for wrong
owner, wrong revision, or changed pin. Existing neighbor tests preserve the
public 0.2.13 carrier and ordinary/private392 `ClipSetParamsArgs` and
`ClipSetElementArgs` definitions; the only successor delta is optional
`ClipAddArgs.schema_source`.

## Activation boundary

The catalog descriptor is not itself save authority. App2/Viewing must provide
the complete source-owned tuple and a legitimate retained `DocumentPin` from
the existing admission/provider path. Do not use a bare id, a revision prefix,
the hosted browser catalog as a substitute, a guessed owner, a fabricated pin,
or latest-catalog fallback. If the normal built-in has no retained pin, keep
the legacy writer and visible refusal in place; this contract does not claim
that system/builtin admission has been qualified.

