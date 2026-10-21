# Runtime O6 explicit inline migration carrier review

Date: 2026-10-21

Verdict: **concrete existing Runtime carrier mismatch; no bounded SOURCE ACK**.

The proposal is correctly scoped in one respect: the legacy inline row remains
Agent-owned migration input, while the resulting descriptor is an ordinary
project-managed text object selected through the existing `text_selection`
seam. Runtime must not read inline text as authority or auto-migrate it. The
current Runtime source nevertheless cannot carry the proposed migration as
written.

## Mismatches

### 1. The current commit carrier rejects `legacy_source`

`runtime_protocol/timeline_commit_port.py:60-62` validates every commit request
against the installed `CommitRequest` schema. The installed
`TextBindingSetArgs` definition at
`runtime_protocol/schemas/timeline-commit-bundle.json:2642-2733` has
`additionalProperties: false`; its allowed operation-level keys are the
existing `binding`, `text`, and `clear`. `legacy_source` is not one of them.

Therefore a `text-binding.set` request carrying
`legacy_source: "main-inline-voiceover-v1"` is refused at request validation,
before the request-scoped port can call `text_selection` or acceptance can run
the binding projection. This is a real current-source carrier mismatch, not a
request to add a new Runtime endpoint or DTO. No schema or generated artifact
was changed in this review.

### 2. A raw inline `before` state is incompatible with the existing projection

Even if the discriminator were admitted by a future coordinated contract,
`timeline_commit_store.py:743-764` sends each recorded text-binding write to
the existing projection. That projection looks up the current relational row
in `shot_text_bindings` (`:774-780`). A legacy inline row in the accepted shot
payload has no such live relational row, so `live` is false. The proposal
requires the recorder to retain the complete raw inline row as `write.before`,
which is a present state. The guard at `:788-791` then rejects because
`before["state"] == "present"` does not match `live == false`, with
`text_binding_mismatch`.

This means adding the optional discriminator alone would not make the proposed
carrier work. The current projection has no legacy-inline pre-state adapter;
it only accepts absent state or the canonical descriptor state represented by
the relational binding. It also cannot itself carry the inline row's opaque
siblings, null-vs-absent distinctions, or list ordinal into the inverse. Those
remain Agent recorder/state responsibilities, but the present inline state
must not be handed to this projection as though it were an existing native
descriptor row.

## Existing seams that do remain compatible

- The normal ingest path hashes the supplied bytes while staging and returns
  the resulting object identity/size/media type (`service.py:4793-4813,
  4847-4861`). The migration caller must compare the exact UTF-8 bytes from the
  selected inline row with the returned descriptor before submitting the
  command. Runtime does not receive the legacy bytes, so it cannot detect a
  caller that substitutes arbitrary replacement text if that replacement is
  otherwise a valid managed object.
- The existing request-scoped `text_selection` is the right descriptor
  authority: it requires a declared selection and records it
  (`timeline_commit_port.py:276-283`); its CAS check requires exact identity,
  size, MIME, managed project ownership, unchanged bytes, and strict UTF-8
  (`:584-629`), and the captured value is rechecked during acceptance
  (`:387-403`). This preserves empty text and rejects missing, null/invalid,
  foreign, digest-mismatched, size-mismatched, or non-UTF-8 objects through
  existing refusal paths.
- For the legacy candidate specifically, a missing row, null/non-string
  `text`, or an ambiguous/malformed row must be refused by the Agent-side
  exclusive-owner preflight. Runtime only sees the resulting descriptor, so it
  cannot perform that source-row check. Empty-string text is different: it is a
  valid present source and remains a zero-byte managed object through the
  existing descriptor validator.
- Existing retained `text/plain` rows continue through
  `verify_retained_text_object` when a relational row is present, while the
  proposed new descriptor MIME `text/plain; charset=utf-8` goes through the
  strict new-object validator (`timeline_commit_store.py:796-805`). No MIME
  normalization or byte rewriting is introduced by the carrier review.
- For already-native rows, the existing before/after projection still checks
  the accepted occurrence's shot owner (`:749-764`), compares the canonical
  descriptor fields (`:788-791`), and appends the normal binding event
  (`:806-832`). It does not sort rows or create an inline authority. These
  native behaviors are not the O6 mismatch.

## Disposition

O6 is **not qualified against the current Runtime source**. Keep the proposal's
exclusive-owner guard, exact source-bytes-to-descriptor requirement, raw-row
preservation, and no-auto-migration boundary. Before implementation can be
qualified, the Agent/Runtime carrier must be coordinated so that the migration
can preserve the raw inline `before` row and its original ordinal/inverse/redo
semantics without presenting that raw state to the current native projection
as an already-live descriptor. No Runtime schema registration, public
newshape/pin/generation/activation/retirement action, endpoint, history scan,
or test change was made here.

Tests were not run: this was a source-only review and the task explicitly
forbade adding tests or running broader suites.
