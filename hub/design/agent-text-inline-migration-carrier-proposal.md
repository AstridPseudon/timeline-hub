# Agent O6 proposal: explicit Main inline text migration

Status: source-only proposal for reciprocal Agent/Runtime review, 2026-10-21.
This is the smallest extension to the existing `text-binding.set` command. It
does not change the Runtime port, API, DTO, store, writer, provenance
authority, or schema in this task, and it does not retire any Main caller.

## Closed command extension

Add one closed, versioned discriminator to the existing `text-binding.set`
args:

```json
"legacy_source": "main-inline-voiceover-v1"
```

The discriminator is legal only with the existing `binding` target
`{"kind":"voiceover_script","slot":null}` and the existing `text`
immutable descriptor. It is not legal with `clear`, any other binding, or any
additional argument. The normal native command remains unchanged: without the
discriminator an inline row is still `unsupported_shape` and is never treated
as text authority.

`main-inline-voiceover-v1` means exactly one row in the selected occurrence's
accepted shot payload has the legacy identity `slot == "voiceover"`, has no
canonical `kind`, and has a string `text`. The row's complete raw mapping is
the source; the literal `hello` is the current Main witness, not a second
caller-supplied authority. Empty strings and all UTF-8 bytes are valid. No
newline, whitespace, Unicode, or null normalization is allowed. Unknown
siblings, explicit `null` values, and the row's list ordinal are opaque and
must be retained.

## Normal-path acceptance

1. The existing caller opens the accepted project/film base and resolves the
   explicit `occurrence:<id>`. Existing project, base revision/publication,
   occurrence, shot-owner, and accepted-film guards remain the authority; the
   discriminator adds no identity or provenance field.
2. Before ingest or authored writes, the caller/recorder requires exclusive
   occurrence ownership (`text-binding.owners == [occurrence:<id>]`), one
   owner shot, and exactly one matching legacy row. A shared shot, missing or
   duplicate candidate, canonical `kind` mixed into the legacy row, non-string
   `text`, invalid UTF-8, or any other unknown/malformed target refuses with a
   visible error and performs no write. Unrelated opaque rows are not guessed
   or rewritten; an ambiguity that could make their preservation non-lossless
   also refuses.
3. The caller encodes only that row's `text` as UTF-8 and calls the existing
   `ingest_project_object(project_id, data, media_type="text/plain; charset=utf-8", ...)`.
   It checks the returned managed descriptor exactly (`object_id == digest`,
   SHA-256, byte size, and MIME). The idempotency key is derived from the
   existing project/occurrence/base identity and content digest. No inline
   bytes, caller hash, or new carrier is sent to Runtime.
4. The caller submits the existing `text-binding.set` with the returned
   descriptor and `legacy_source`. Existing Runtime `text_selection` performs
   its project-scoped CAS and UTF-8 acceptance recheck.
5. The existing text-binding recorder records the full raw `before` row, the
   exact collection membership/order selection, occurrence/shot reads, and
   the descriptor `after` row. The replacement occurs at the original list
   ordinal; it does not append or sort. The canonical after row is exactly:

   ```json
   {
     "kind": "voiceover_script",
     "slot": null,
     "media_id": "sha256:<text-digest>",
     "content_hash": "sha256:<text-digest>",
     "byte_size": 5,
     "mime_type": "text/plain; charset=utf-8"
   }
   ```

   for the Main witness `hello`; no `text` or Runtime-derived fields are
   authored. Existing opaque fields are copied exactly rather than interpreted.
6. The existing accepted inverse is guarded by the target after-state,
   occurrence/shot reads, and collection membership/order. It restores the
   complete inline `before` row at the same ordinal, including absent-vs-null,
   unknown siblings, and all opaque values. Any intervening write, reorder,
   owner change, or A→B→A state refuses before mutation. Redo is the existing
   guarded command path, not a snapshot shortcut.
7. Runtime's existing acceptance transaction projects the immutable descriptor
   and appends its existing binding event. Runtime neither reads nor migrates
   the inline row and adds no writer or authority.

The minimal witness is a project-owned, exclusive occurrence whose shot has
`text_bindings == [{"slot":"voiceover","text":"hello"}]` (possibly with
other rows before/after). Success replaces only that row with the canonical
descriptor above; inverse deep-equals the original list. A shared occurrence
refuses before ingest, preserving Main's existing positive behavior elsewhere.

## Boundaries

- Main inline/catalog positives and all legacy callers stay live/held until
  this migration is implemented and qualified. This proposal does not replace
  their behavior with refusal.
- Shared ownership is unsupported in this closed extension; cutting the Main
  positive to obtain shared migration is not authorized.
- The discriminator is intent/guard data only. It is not persisted provenance,
  a new source kind, a pin, or a second text authority.
- No new endpoint, port, DTO, table, store, writer, schema artifact,
  generation, pin, release, HTTP/body work, Runtime implementation, or tests
  are part of this proposal. Manager approval and reciprocal Runtime source
  agreement are required before implementation.

