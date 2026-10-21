# Runtime review: Agent transcript.associate recorded source

Date: 2026-10-21  
Runtime base: `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`  
Compatible Runtime source, explicitly separate: `3dcae1836a609363135d07ee435ce9beea975504`

## Verdict

**HOLD for the named Agent source; Runtime itself needs no new counterpart.**

The source named by both `agent-film-transcript-recorded-source.md` and
`agent-film-transcript-raw-contract-review.md` is Agent
`e83d8fc5b609e34b692cfcb9185d2594fa0706b5` (parent
`4b784c3f90a5c3f5233e564721e734ce99bf3738`). I reviewed that committed tree,
not the earlier spike and not a guessed branch tip. Its exact new/prior
`DocumentPin` use fits Runtime's existing `transcript_source` carrier, but the
implementation is not yet a native App-compatible association:

1. it writes the rejected parent-level `sourceItemsBySchemaRef` carrier instead
   of the persisted App `parent.config.bundle.itemsBySchemaRef` carrier; and
2. its caption/review refusal predicate misses the App's generated-caption
   shape when the caption clip has no own `asset` field.

The later Agent successor `9d007f26c61f11a27f5082a6147cd70f90a10612` fixes the
first carrier mismatch in its separate `agent-transcript-persisted-bundle-
carrier-fix.md` report. That successor is not silently substituted for the
named source here; it still needs the caption/review negative case and a
matched native qualification. The original broad association capability stays
**OPEN**. No full migration or positive caption/review reconciliation is
claimed.

## Runtime carrier check

The existing Runtime path is sufficient for the source inputs this command
actually consumes. Agent `_hydrate` adds both `document` and
`previous_document` pins for `transcript.associate`, then calls
`port.transcript_source` for each exact pin (`commit.py:435-453` at `e83`).
The handler separately verifies the new pin and, when replacing an existing
association, the exact prior pin and content (`native_transcript_association.py:
231-253`). It records both dependencies (`:288-290`), rather than querying
mutable latest catalog state.

Runtime's existing port then:

- requires the exact three-field pin and captures the exact transcript bytes
  through `transcript_source` (`timeline_commit_port.py:294-321`);
- checks project scope, `media.transcript/v1`, canonical transcript identity,
  source media ownership, and source ID in the document-input seam;
- requires the candidate manifest's document pins to equal the port's captured
  pins and requires every manifest pin to appear in a recorded transcript/source
  dependency (`timeline_commit_port.py:416-424`); and
- persists the captured links against the accepted publication, so the prior
  and new pins can remain in the authorized accepted closure
  (`timeline_commit_port.py:439-445`).

The retained-input evidence for the explicit `3dcae183` follow-up already
covers V1 after a V2 update, live-row removal, and Runtime restart. I did not
rerun that prior 29-test boundary set or the retained-input subset, per task
scope. The `3dca` change is a separate compatible Runtime source, not an
unreported modification to this `95bd` worktree.

The Agent handler checks that the selected parent asset's media identity equals
the transcript content's media identity. It does not consume raw media bytes;
therefore the transcript read does not justify a new media object carrier. If a
future handler consumes media bytes, it must use the existing declared media
selection/closure and manifest path. Runtime must not infer that closure from a
transcript document.

There is no Runtime-side acceptance or projection normalization of the parent
payload. The Runtime stores and validates the canonical parent payload and
document manifest as supplied. Consequently, Runtime can preserve a correct
nested source carrier, but it cannot repair an Agent producer that writes a
different carrier.

## Product-source findings

### 1. The named tree does not target the persisted App carrier

At `e83` `native_transcript_association.py:27-42`, `_source_paths()` searches
only the parent root, `parent.config`, and `parent.bundle`, and only recognizes
`transcriptReferences` plus `sourceItemsBySchemaRef`. The write paths at
`:234-235` and `:300-301` therefore target top-level parent fields when given
the real App wire shape. The App path is:

```text
parent_composition.config.bundle.transcriptReferences
parent_composition.config.bundle.itemsBySchemaRef[
  "astrid.transcript_segment/v1"
]
```

This is not a harmless spelling difference: a normal App save/reload continues
to see no association or source items, while a second root-level carrier is
created. The current App snapshot writer must remain in place until the exact
nested carrier is qualified.

### 2. Caption/review refusal is incomplete

The explicit unsupported policy is appropriate: the command must refuse before
any write when reconciliation would change generated-caption or review
provenance. However, `e83`'s `_reconciliation_needed()` only considers a
generated caption clip when `clip.asset == asset_id` (`:188-201`). App's
generated caption clips can have no own `asset`; ownership is established by
the paired media clip/fingerprint. The source therefore accepts one affected
shape instead of refusing it. This is a source guard gap, not a request for
Runtime to implement reconciliation. The minimal correction is to reuse the
App ownership predicate or conservatively refuse any affected generated/review
provenance until a native reconciler exists.

The source's positive association behavior remains useful and must not be
deleted or narrowed to avoid this case. The unsupported subcase stays an
explicit atomic refusal, while the general association remains OPEN pending
the corrected carrier and native qualification.

## What is and is not proven

The Agent source tests reported for `e83` cover exact pin hydration, owner and
stable segment/word checks, source-item order/opaque preservation, pure inverse
and replay-shaped behavior, and the explicit caption-refusal fixture. They do
not prove a normal App save/reload, accepted Runtime history, or retained
inverse after document removal/restart.

The prior Runtime compatible-source evidence proves the existing retained
transcript read/closure behavior, but does not qualify this new command's
parent writes. No Runtime DTO, endpoint, store, schema, generated client, pin,
publication, or adoption change is needed for this boundary.

## Bounded probe

I extracted the exact `e83d8fc5` tree into a private temporary directory and ran
one no-socket Python probe using an App-shaped nested bundle plus the App2
caption shape. Result:

```text
e83_nested_bundle_unchanged= True
e83_nested_association_count= 0
e83_nested_source_count= 0
e83_root_association_count= 1
e83_root_source_count= 1
e83_caption_without_asset=accepted
```

This is direct product-source evidence for both findings above. No full,
browser, live-socket, generated-client, or repeated transcript boundary suite
was run.

## Smallest next step

Review the `9d007f26` successor against the exact App nested carrier, add the
no-`asset` caption/review refusal witness, then run a matched Agent/App/Runtime
save/reload and accepted-history inverse/restart witness proving both exact
new/prior pins. Keep the App snapshot writer and catalog/document CRUD until
that qualification passes. Do not add a Runtime endpoint, DTO family, store,
alternate hash authority, or projection normalizer.
