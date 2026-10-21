# App2 M2 transcript consumer fit — 2026-10-21

## Verdict

The dormant `transcript.associate` capture covers the original ordinary,
exclusive parent-association path without loss, within its deliberate refusal
boundary. It records the nested persisted carrier, source-item membership and
order, exact new/prior transcript pins, stable segment/word bindings, and
caption/review/config writes atomically. It is not a live consumer yet.

## Original path and compatible capture shape

The film-visible selector input is `{ assetId, documentId }` at
`src/sdk/video/transcript.ts:157-160`; the panel forwards it at
`src/tools/video-editor/lib/transcript-panel-binding.ts:66-69`.
`project-transcript-host.ts:747-754` loads the selected document and calls
`associate(d, assetId)`. Import and promotion converge on the same caller at
`:756-825` and `:827-857`. The writer at `:600-651` computes the replacement
association, projects transcript rows, runs `reconcileTranscriptReferences`,
then calls `commitData(next, { save: true, semantic: true })` and flushes the
save. This is the remaining live whole-snapshot ingress.

The dormant replacement is:

```text
captureTranscriptAssociation(bundle, assetId, { pin, document }, previous?)
  -> finish/executeTranscriptAssociation(...)
  -> { command, bundle, record }
```

The exact source is `TranscriptAssociateSource = { pin, document }` and
`verifyTranscript` requires a project-scoped `media.transcript/v1` document,
canonical `transcript:<hash>` identity, exact content digest, and bounded
word timing (`transcriptAssociateCapture.ts:43,103-133`). The written carrier
is exactly `parent.config.bundle.transcriptReferences` plus
`parent.config.bundle.itemsBySchemaRef["astrid.transcript_segment/v1"]`; unrelated
bundle/opaque values and retained row order survive. Current tests also prove
the empty-primary/populated-config-clips mirror rule.

Supported ordinary shape: one parent asset with a managed media identity;
new source or replacement with the exact prior pin; well-formed persisted
source rows; and caption/review provenance that is uniquely attributable. A
generated caption without its own `asset` field is supported when its paired
media/fingerprint identifies it; text/style/timing/opaque metadata and the
review record are retained while IDs are remapped.

Explicitly unsupported/refused cases are: caption destination collision,
ambiguous caption ownership, or malformed generated-caption metadata; shared
ownership when it makes a matching review/caption provenance ambiguous;
occupied destination review keys; root/flat legacy carriers or inline rows
(including `{slot, text}` authority); malformed source-item envelopes; and
missing, foreign, swapped, digest/version-mismatched, or unavailable exact
new/prior pins. A missing or noncanonical review is preserved rather than
guessed. Shared ownership is not a qualified positive.

## Runtime08:22 decision deltas

- P1/P2 are for `text.binding`: exact text selection and Runtime-derived live
  projection/event. They do not replace or qualify `transcript.associate`.
- O1/O2/O3 (identity-only rows, new MIME `text/plain; charset=utf-8`, and
  occurrence-owned binding) apply to text.binding, not transcript source rows;
  the transcript helper keeps its existing document carrier and MIME/content
  validation.
- O4 agrees with this helper: preserve recorded source-item order; no sorting
  authority is added.
- O5 ACKs exclusive occurrence ownership only; it grants no shared transcript
  ownership positive and no deletion of the current snapshot writer.
- O6 forbids Runtime inline-text migration. Existing legacy positives/callers
  remain held. The helper must not fall back to inline or root App fields.
- O7 is a compatibility ACK, not consumer qualification, release authorization,
  or proof that App callers can retire their writer.

The retained Runtime read is compatible: it returns the exact `{ pin, document }`
carrier for `media.transcript`. PRIVATE017 generated-carrier ACKs are likewise
not transcript native-consumer proof.

## Existing evidence

- `transcriptAssociateCapture.test.ts`: 7 focused tests covering ordinary
  nested capture, replacement/prior pin, swapped-pin refusal, mirror choice,
  caption collision/shared review refusal, and malformed pinned source.
- `project-transcript-host.test.ts`: “imports rich native items once…”,
  “source corrections converge in two timelines…”, “promotes legacy opaque
  IDs…”, and “reads canonical sources on reopen…” preserve the original
  snapshot behavior and reload/retry semantics.
- `importTranscriptIdentity.test.tsx`, `timelineBundle.test.ts`, and
  `runtime-retained-transcript-verified-read.md` cover the App wire carrier
  and Runtime retained exact-read boundary. No new execution was performed
  for this report.

## One remaining blocker / owner

**App2 caller contract:** the live host receives plain `ProjectTranscriptDocument`
from `projectTranscripts.get` (`projectTranscript.ts:53-63,137-158`, backed by
`dataProvider.ts:454-458`); it has `document_id`/`version` but no
`content_digest` pin and is not the retained verified read. Therefore the
caller cannot currently supply the helper’s exact new source, or an exact
prior source for replacement, to the existing commit session/outbox.

App2’s one next source action is to adapt `associate` to obtain the existing
retained `{ pin, document }` for each exact new/prior pin and submit the dormant
command through the existing commit path, then qualify it before removing the
snapshot fallback. This needs no new DTO/op/schema/store or Agent source
change. Agent’s carrier is otherwise complete; Runtime has no additional
P1/P2/O1-O7 implementation action.
