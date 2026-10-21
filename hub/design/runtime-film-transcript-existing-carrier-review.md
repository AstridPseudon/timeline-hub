# Runtime source review: existing film transcript carrier

Date: 2026-10-21

## Verdict

**SOURCE ACK — bounded and compatible.** The Agent proposal in
`agent-film-transcript-association-recipe.md` and its exact source-only spike
at Agent commit `4b784c3f90a5c3f5233e564721e734ce99bf3738` can use Runtime's
existing exact document-input carrier. The compatible Runtime dependency is
`3dcae1836a609363135d07ee435ce9beea975504` (tree
`4fa58b2551f716c35cab6005cc8add84e59da8a9`), whose parent is the immutable
Runtime base `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`.

This is a source ACK only. It does not register `transcript.associate`, change
the schema/client/pin, publish or adopt a release, or alter Runtime source.

## Exact carrier decision

The proposal's new and replacement `previous_document` pins are compatible
with `RequestCommitPort.transcript_source(pin)` and the existing
`capture_document_input`/`persist_document_input_links` path:

- The request declaration is recursive. A pin nested in the command args is
  declared; an undeclared pin is refused before capture. A replacement must
  declare both the new and exact prior `DocumentPin` (or obtain the prior pin
  from an authorized base/history closure). Runtime does not infer either pin
  from latest catalog state.
- The accepted canonical manifest's `documents` set must equal the exact set
  captured by `transcript_source`, and every manifest pin must appear in a
  recorded `transcript` dependency. This covers both the new and old source
  document when inverse/replay needs both.
- The transcript read is exact and scoped: three-field
  `{document_id, version, content_digest}` pin; canonical content digest and
  bytes; `media.transcript/v1`; derived transcript document identity; project
  scope; and project-managed source-media ownership. Unsupported kinds,
  foreign pins, missing/corrupt retained bytes, changed headers, and first-use
  races fail closed before writes.
- Accepted input links preserve the old/current/history custody path. A V1
  source remains readable from its authorized accepted closure after a V2
  document update, live-row removal, and Runtime restart. A prior pin outside
  that closure is refused rather than reconstructed.
- The film asset's existing media identity/closure remains the authority for
  the `media_id` in the proposal. `transcript_source` verifies that the
  transcript points at a currently project-managed media object, but it is not
  a raw-media or snapshot-object read and does not silently add media bytes to
  the accepted manifest. If the handler consumes media bytes separately, it
  must use the existing declared media/closure carrier; no new transcript
  object port is justified.

## Association and caption boundary

Runtime accepts the result atomically as one canonical parent edit. The Agent
handler remains responsible for capturing the complete parent association and
source-item membership/order, stable owner/source/segment/word bindings,
opaque values, and the exact caption/review rows consumed by the existing
reconciler. Runtime will retain the exact document inputs and the accepted
parent revision together; it does not need a second DTO or a transcript store.

The handler must continue to refuse before writes when the prior association
or prior exact pin is unavailable, when owner/source/item identity is
ambiguous, or when caption destinations are occupied. Item/caption deletion
must be represented by the existing command recorder's guarded writes and
sole recorder, not by a Runtime-side cleanup. The source-only spike's
`caption_provenance` copy is semantic evidence, not a Runtime qualification of
the reconciler; that proof remains with the eventual Agent/App command
qualification.

## Evidence reused

- Agent source-only spike: commit `4b784c3f` adds only
  `tests/editing_conformance/test_recipe_film_transcript_association_spike.py`
  and reports the exact pin, owner, source-item membership/order, opaque
  preservation, inverse/rebase/retry/restart pin retention, and closed
  refusal cases. Its recorded result was **42 passed in 146.70s** together
  with the current union test.
- Runtime compatible source review: `3dcae183` changes only the existing
  `_source_kind` allowlist and the focused transcript boundary test. The
  retained-input controls reported **12 passed**; the central targeted source
  set (`test_timeline_source_document_boundary.py`,
  `test_timeline_pack_document_read.py`, and
  `test_timeline_commit_inputs.py`) reported **29 passed in 7.89s**.
- The retained transcript control includes V1-after-V2/removal/restart,
  exact HTTP read, unsupported-kind refusal, foreign-project refusal, and
  zero-write refusal snapshots. `git diff --check` for the `95bd` → `3dca`
  source pair passed.

No full, browser, socket, render, generated-contract, or public adoption suite
was run for this review.

## Smallest compatible dependency for Agent

When the native command is eventually admitted, the provider must:

1. call `transcript_source` for every exact new/prior pin it consumes;
2. put exactly those pins in `canonical_document.dependency_manifest.documents`
   and in the command dependency records;
3. retain the asset's existing media closure/selection if raw media is
   consumed; and
4. keep the association/source-item/caption reconciliation in the same parent
   command and guarded recorder transaction.

Failure of any of these conditions is a visible refusal, not a latest-document
fallback or a new Runtime carrier.
